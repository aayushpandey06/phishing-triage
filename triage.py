"""
triage.py - pulls the useful facts out of .eml files so triage goes faster.

Read-only: it never opens links, looks anything up online, or runs attachments.
It doesn't give a verdict. That part is done by hand in notes/.

    python triage.py samples/                  print a summary per email
    python triage.py samples/ --notes notes/   also write a notes file per email
                                               (existing notes are never overwritten)
"""
import argparse
import base64
import email
import hashlib
import html
import ipaddress
import plistlib
import re
import sys
import unicodedata
from collections import defaultdict
from email import policy
from email.utils import getaddresses, parseaddr
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

# Windows terminals choke on emoji and Cherokee letters without this
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# mail services that real companies use too, so a mismatch with these means little
BULK_MAIL = {"amazonses.com", "sendgrid.net", "mailgun.org", "mtasv.net", "mcsv.net",
             "getdrip.com", "brevo.com", "mailjet.com"}

# attachment types a normal sender has no reason to send
RISKY = {".html", ".htm", ".svg", ".js", ".vbs", ".hta", ".lnk", ".exe", ".scr", ".iso",
         ".img", ".one", ".mobileconfig", ".docm", ".xlsm", ".zip", ".rar", ".7z"}

# short on purpose, I add brands as they show up
BRANDS = ["microsoft", "apple", "icloud", "paypal", "dhl", "chronopost", "revolut",
          "bitcoin", "wallet", "supabase", "kinguin", "netflix", "amazon"]

URL = re.compile(r"(?i)\bhttps?://[!#-&*-;=?-~]+")
ANCHOR = re.compile(r"<a\b[^>]*?href\s*=\s*[\"']?([^\"'\s>]+)[^>]*>(.*?)</a>", re.I | re.S)
BRACKETED_IP = re.compile(r"[\[(]\s*(?:IPv6:)?([0-9a-fA-F:.]{7,45})\s*[\])]")
IGNORE_HOSTS = {"fonts.googleapis.com", "fonts.gstatic.com"}


def defang(s):
    return re.sub(r"(?i)^http", "hxxp", s).replace(".", "[.]")


def domain(addr):
    return addr.rsplit("@", 1)[-1].lower().strip(" >.") if "@" in addr else ""


def root(host):
    # rough guess at the "real" domain. Not the Public Suffix List, so it
    # gets some domains wrong (see README)
    parts = host.lower().strip(".").split(".")
    two_part_tld = len(parts) >= 3 and parts[-2] in {"co", "com", "org", "net", "edu", "gov", "ac", "ne"} and len(parts[-1]) == 2
    shared_platform = ".".join(parts[-2:]) in {"onmicrosoft.com", "vercel.app", "web.app", "pages.dev", "github.io"}
    return ".".join(parts[-3:] if two_part_tld or shared_platform else parts[-2:])


def clean(text):
    # drop invisible characters so I see what the recipient saw
    return "".join(c for c in text if unicodedata.category(c) != "Cf" and not 0xE0000 <= ord(c) <= 0xE01EF)


def odd_characters(text):
    found = []
    invisible = [c for c in text if unicodedata.category(c) == "Cf" or 0xE0000 <= ord(c) <= 0xE01EF]
    if invisible:
        found.append(f"{len(invisible)} invisible characters")
    # letters from other alphabets hidden in otherwise Latin text (e.g. Cherokee 'Ꮇ' for 'M')
    lookalikes = {c for c in text if c.isalpha() and ord(c) > 0x24F
                  and not any(s in unicodedata.name(c, "") for s in ("CJK", "HIRAGANA", "KATAKANA", "HANGUL"))}
    if lookalikes and sum(c.isascii() and c.isalpha() for c in text) >= 3:
        found.append("look-alike letters: " + ", ".join(f"{c} ({unicodedata.name(c, '?').title()})" for c in lookalikes))
    return found


def auth_results(msg):
    # the top Authentication-Results header is the one the receiving server added.
    # Lower ones could have been written by the sender, so they're ignored
    res = {"spf": "-", "dkim": "-", "dmarc": "-", "dkim_domain": ""}
    headers = msg.get_all("Authentication-Results") or []
    if headers:
        text = str(headers[0])
        for key in ("spf", "dkim", "dmarc"):
            m = re.search(rf"\b{key}=(\w+)", text, re.I)
            if m:
                res[key] = m.group(1).lower()
        m = re.search(r"header\.d=([\w.-]+)", text, re.I)
        if m and m.group(1).lower() != "none":
            res["dkim_domain"] = m.group(1).lower()
    return res


def first_public_ip(msg):
    # walk Received headers from the bottom up. The bottom ones can be faked
    # by the sender, so this is a lead, not a fact
    for header in reversed(msg.get_all("Received") or []):
        for candidate in BRACKETED_IP.findall(str(header)):
            try:
                ip = ipaddress.ip_address(candidate.strip("."))
            except ValueError:
                continue
            if ip.is_global:
                return str(ip)
    return ""


def bodies(msg):
    text, htm = "", ""
    for part in msg.walk():
        if part.is_multipart() or part.get_filename() or not part.get_content_type().startswith("text/"):
            continue
        try:
            content = part.get_content()
        except Exception:
            content = (part.get_payload(decode=True) or b"").decode("utf-8", "replace")
        if part.get_content_type() == "text/html":
            htm += content
        else:
            text += content
    return text, htm


def visible_text(text, htm):
    body = text if text.strip() else htm
    body = re.sub(r"(?is)<(style|script|head)\b.*?</\1>", " ", body)
    body = html.unescape(re.sub(r"<[^>]+>", " ", body))
    body = re.sub(r"\s+", " ", clean(body)).strip()
    # the sample set isn't fully anonymised: some bodies still contain the real
    # recipient's address, so hide every address before it lands in my notes
    return re.sub(r"[\w.+-]+@[\w-]+\.[\w.-]+", "[email removed]", body)


def find_links(text, htm):
    found = {}  # url -> the text the reader sees on the link
    for href, shown in ANCHOR.findall(htm):
        href = html.unescape(href)
        if href.lower().startswith("http"):
            found.setdefault(href, html.unescape(re.sub(r"<[^>]+>", "", shown)).strip())
    for u in URL.findall(text + " " + html.unescape(re.sub(r"<[^>]+>", " ", htm))):
        found.setdefault(u.rstrip(".,;"), "")
    return found


def real_destination(url):
    # some links pass through a trusted site first (Bing, Google) and hide the
    # real target in the query string
    try:
        parts = urlsplit(url)
    except ValueError:
        return ""
    query = parse_qs(parts.query)
    host = parts.hostname or ""
    bing_target = query.get("u", [""])[0]
    if host.endswith("bing.com") and parts.path.startswith("/ck/") and bing_target.startswith("a1"):
        encoded = bing_target[2:]  # Bing puts 'a1' in front of base64 of the real URL
        try:
            return base64.urlsafe_b64decode(encoded + "=" * (-len(encoded) % 4)).decode()
        except Exception:
            return ""
    for key in ("url", "u", "q", "redirect", "target", "dest"):
        for value in query.get(key, []):
            if value.startswith("http"):
                return value
    return ""


def link_problems(url, shown):
    try:
        parts = urlsplit(url)
        host = (parts.hostname or "").lower()
    except ValueError:
        return ["can't parse this URL"]
    problems = []
    if "@" in parts.netloc:
        fake = parts.netloc.split("@")[0]
        problems.append(f"'@' trick: starts with {defang(fake)} but the real host is {defang(host)}")
    if re.match(r"^\d{1,3}[-.]\d{1,3}[-.]\d{1,3}[-.]\d{1,3}", host):
        problems.append("host is an IP address dressed up as a hostname")
    if host.startswith("xn--") or ".xn--" in host:
        problems.append("punycode domain")
    real = real_destination(url)
    if real:
        problems.append(f"redirect, real target is {defang(real)}")
    shown_url = URL.search(shown or "")
    if shown_url:
        shown_host = urlsplit(shown_url.group(0)).hostname or ""
        if shown_host and root(shown_host) != root(host):
            problems.append(f"link text says {defang(shown_host)}")
    return problems


def attachment_info(part):
    name = clean(part.get_filename() or "?")
    data = part.get_payload(decode=True) or b""
    info = {"name": name, "type": part.get_content_type(), "size": len(data),
            "sha256": hashlib.sha256(data).hexdigest(), "notes": [], "servers": []}
    ext = Path(name.lower()).suffix
    if ext in RISKY:
        info["notes"].append(f"{ext} is not something a normal sender attaches")
    if ext == ".mobileconfig":
        # Apple configuration profile. Signed ones wrap the XML in binary, so cut it out first
        m = re.search(rb"<\?xml.*?</plist>", data, re.S)
        try:
            profile = plistlib.loads(m.group(0))
            for payload in profile.get("PayloadContent", []):
                servers = [str(v) for k, v in payload.items() if k.endswith("HostName")]
                info["servers"] += [s.split(":")[0] for s in servers]
                info["notes"].append(f"sets up {payload.get('PayloadType')} on {', '.join(defang(s) for s in servers)}")
        except Exception:
            info["notes"].append("couldn't read the profile")
    if data[:4] == b"%PDF":
        if any(x in data for x in (b"/JavaScript", b"/OpenAction", b"/Launch")):
            info["notes"].append("PDF contains JavaScript or an auto-run action")
        uris = sorted({u.decode("latin-1") for u in re.findall(rb"/URI\s*\(([^)]+)\)", data)})
        if uris:
            info["notes"].append("PDF links to: " + ", ".join(defang(u) for u in uris))
    return info


def analyse(path):
    with open(path, "rb") as f:
        msg = email.message_from_binary_file(f, policy=policy.default)

    name, addr = parseaddr(str(msg["From"] or ""))
    reply_to = [a for _, a in getaddresses([str(h) for h in msg.get_all("Reply-To") or []])]
    return_path = parseaddr(str(msg["Return-Path"] or ""))[1]
    subject = str(msg["Subject"] or "")
    auth = auth_results(msg)
    text, htm = bodies(msg)
    links = find_links(text, htm)
    for url in list(links):  # list hidden redirect targets as their own links
        real = real_destination(url)
        if real:
            links.setdefault(real, "")
    attachments = [attachment_info(p) for p in msg.walk() if p.get_filename()]

    sender_domain = domain(addr)
    flags = []
    for where, value in (("sender name", name), ("subject", subject)):
        flags += [f"{where}: {x}" for x in odd_characters(value)]
    brands = [b for b in BRANDS if re.search(rf"\b{b}\b", clean(name + " " + subject).lower())]
    if brands and not any(b in sender_domain for b in brands):
        flags.append(f"mentions {', '.join(brands)} but sends from {sender_domain or '?'}")
    labels = sender_domain.split(".")
    if sender_domain and (len(labels) < 2 or not labels[-1].isalpha()):
        flags.append(f"sender domain '{sender_domain}' isn't a real domain, so the From line is made up")
    for r in reply_to:
        if domain(r) and root(domain(r)) != root(sender_domain or "-"):
            flags.append(f"replies go to {domain(r)}")
    if return_path and root(domain(return_path)) != root(sender_domain or "-"):
        rp = root(domain(return_path))
        flags.append(f"bounces go to {rp}" + (" (a bulk mail service, normal for real senders too)" if rp in BULK_MAIL else ""))
    if auth["dkim_domain"] and root(auth["dkim_domain"]) != root(sender_domain or "-"):
        flags.append(f"DKIM signed by {auth['dkim_domain']}, not the sender's domain")

    hosts = {(urlsplit(u).hostname or "").lower() for u in links} - IGNORE_HOSTS - {""}
    return {
        "id": Path(path).stem,
        "date": str(msg["Date"] or ""),
        "from": f"{clean(name)} <{addr}>".strip(),
        "subject": clean(subject),
        "reply_to": reply_to,
        "return_path": return_path,
        "auth": auth,
        "ip": first_public_ip(msg),
        "links": [(u, link_problems(u, shown)) for u, shown in links.items()],
        "attachments": attachments,
        "flags": flags,
        "preview": visible_text(text, htm)[:300],
        # things worth comparing across emails
        "infra": {"link domain": {root(h) for h in hosts},
                  "reply-to domain": {root(domain(r)) for r in reply_to if domain(r)},
                  "sending IP": {first_public_ip(msg)} - {""},
                  "attachment hash": {a["sha256"] for a in attachments},
                  "server in attachment": {s for a in attachments for s in a["servers"]}},
    }


def shared_infrastructure(results):
    seen = defaultdict(set)
    for r in results:
        for kind, values in r["infra"].items():
            for v in values:
                seen[(kind, v)].add(r["id"])
    return [(kind, v, sorted(ids)) for (kind, v), ids in sorted(seen.items()) if len(ids) > 1]


def facts(r):
    a = r["auth"]
    lines = [f"- Date: {r['date']}",
             f"- From: {r['from']}",
             f"- Subject: {r['subject']}",
             f"- Reply-To: {', '.join(r['reply_to']) or '-'}",
             f"- Return-Path: {r['return_path'] or '-'}",
             f"- SPF / DKIM / DMARC: {a['spf']} / {a['dkim']} / {a['dmarc']}"
             + (f" (DKIM domain: {a['dkim_domain']})" if a["dkim_domain"] else ""),
             f"- First public IP in the relay chain: {r['ip'] or '-'}",
             f"- Start of the body: {r['preview'][:250]}", "",
             "Links:"]
    lines += [f"- `{defang(u)[:150]}`" + (f" - {'; '.join(p)}" if p else "") for u, p in r["links"]] or ["- none"]
    lines += ["", "Attachments:"]
    for att in r["attachments"]:
        lines.append(f"- `{att['name']}` ({att['type']}, {att['size']} bytes)")
        lines.append(f"  - sha256 `{att['sha256']}`")
        lines += [f"  - {n}" for n in att["notes"]]
    if not r["attachments"]:
        lines.append("- none")
    lines += ["", "What the script flagged:"]
    lines += [f"- {f}" for f in r["flags"]] or ["- nothing"]
    return lines


NOTES_TEMPLATE = """# {id}

## Facts from triage.py

{facts}

## What I checked by hand

<!-- urlscan.io / VirusTotal / WHOIS results, what the email looks like, translation if needed -->

## Verdict

- Verdict: <!-- malicious / scam / spam / legitimate / unsure -->
- Type: <!-- e.g. credential phishing, malware delivery, fee scam, marketing spam -->
- Confidence: <!-- high / medium / low -->
- Why:

## What I'm not sure about

"""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("folder")
    parser.add_argument("--notes", help="folder to write one notes file per email into")
    args = parser.parse_args()

    results = []
    for path in sorted(Path(args.folder).glob("*.eml")):
        try:
            results.append(analyse(path))
        except Exception as e:
            print(f"!! couldn't read {path.name}: {e}")

    for r in results:
        print(f"\n=== {r['id']}")
        print("\n".join(facts(r)))

    shared = shared_infrastructure(results)
    print("\n=== Seen in more than one email")
    for kind, value, ids in shared:
        print(f"- {kind}: {value if kind == 'attachment hash' else defang(value)} -> {', '.join(ids)}")

    if args.notes:
        out = Path(args.notes)
        out.mkdir(exist_ok=True)
        for r in results:
            note = out / f"{r['id']}.md"
            if not note.exists():
                note.write_text(NOTES_TEMPLATE.format(id=r["id"], facts="\n".join(facts(r))), encoding="utf-8")
        shared_note = out / "shared-infrastructure.md"
        if not shared_note.exists():
            rows = [f"| {k} | `{v if k == 'attachment hash' else defang(v)}` | {', '.join(ids)} | |" for k, v, ids in shared]
            shared_note.write_text("# Things seen in more than one email\n\n"
                                   "| What | Value | Emails | My take (strong link / weak link / coincidence) |\n"
                                   "|---|---|---|---|\n" + "\n".join(rows) + "\n", encoding="utf-8")
        print(f"\nnotes written to {out}/ (existing files left alone)")


if __name__ == "__main__":
    main()
