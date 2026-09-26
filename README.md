# Phishing triage: 10 real emails

I took 10 real phishing and spam emails caught by a public honeypot (March to May 2026), worked out what each one is trying to do, and looked for links between them. The write-up is in [findings.md](findings.md) and my working notes for each email are in [notes/](notes/).

## How I worked

For each email, in this order:

1. Ran `triage.py` to get the basic facts: real sender, SPF/DKIM/DMARC, links, attachments.
2. Opened the `.eml` as plain text in VS Code and read the headers from the bottom up: the first `Received` line, whether the mail was sent with a login, the X-Mailer, the Message-ID, and Microsoft's spam score (`X-MS-Exchange-Organization-SCL`).
3. Read the HTML for tricks: invisible characters, filler text, hotlinked logos, template variables left unfilled.
4. Unwrapped every link by hand (base64 inside Bing links, the `@` trick) without clicking anything.
5. Took attachments apart in Python. For the iPhone profiles, that meant pulling the XML and certificate out of the signature wrapper.
6. Looked everything up passively: urlscan.io search (existing scans only, I didn't submit new ones), VirusTotal by hash, and RDAP for domain age and registrar.
7. Wrote the verdict and, just as important, what I couldn't confirm.

"Malicious" means it tries to steal credentials, money or data, or to install something. "Spam" means unwanted advertising that doesn't pretend to be someone else. If I couldn't decide, I'd have written "unsure". In the end I didn't need to.

## The script

`triage.py` reads each `.eml` file and pulls out the things I'd otherwise dig for by hand: who really sent it, what SPF/DKIM/DMARC said, where the links actually go, and what the attachments are. It doesn't open links or look anything up online, and it doesn't make the call.

Quick start: double-click `setup.bat` on Windows, or run `sh setup.sh` on Mac/Linux. Or step by step:

```
python get_samples.py                    # downloads the 10 emails into samples/
python triage.py samples/                # prints what it finds
python triage.py samples/ --notes notes/ # writes a notes file per email (won't overwrite)
```

Python 3.9+, standard library only.

## Known problems with the script

- **The brand check is easy to fool.** It looks for words like "microsoft" in the sender name. In samples 7978 and 8062 the "M" is a Cherokee letter, so the word doesn't match and the brand check says nothing. The look-alike character check catches it instead, but only by luck of having both checks.
- **The brand list is short and hand-written.** Anything not on it gets no brand check at all.
- **Domain grouping is a guess.** It uses a simple rule instead of the Public Suffix List, so some domains get grouped wrong.
- **The "first public IP" can be fake.** The lowest Received headers are written by the sender's side. It's a starting point for a lookup, not evidence.
- **It trusts the receiving server's SPF/DKIM/DMARC results.** These samples were all received by Microsoft, which reports "bestguesspass" when a domain has no DMARC record. That's not a real pass, and the script doesn't explain the difference.
- **It only unwraps Bing redirects and simple `?url=` style ones.** Other redirect tricks will get past it.
- **It doesn't render the HTML.** Text hidden in images or with CSS tricks won't show up, so I still read every email myself.
- **The brand check only reads the sender name and subject.** 8568 says "Nickel" in the body and gets no flag. Nickel isn't on the list either.
- **"wallet" and "bitcoin" are on the brand list, but they aren't brands.** Any email that mentions a wallet gets a brand warning.
- **It doesn't show Microsoft's spam score (SCL).** In this set, SCL was one of the most telling headers. 7 of the 9 bad emails were already in Junk.
- **It doesn't spot template mistakes** like `randomid2` or `$RAND` left in the email. I only found those by reading.
- **It found shared infrastructure, but that doesn't prove the same attacker.** A shared bulk-mail service or hosting provider means very little. See `notes/shared-infrastructure.md` for how I judged each link.

## Data and handling

The emails come from [Phishing Pot](https://github.com/rf-peixoto/phishing_pot) by rf-peixoto (CC BY-NC 4.0). They aren't included in this repo; `get_samples.py` downloads them. The set isn't fully anonymised: a couple of emails still contain the honeypot owner's real address in the body. The script replaces email addresses in body text before anything is written to my notes.

Every link in this repo is defanged (`hxxp`, `[.]`). The sender and DKIM domains in the script's output aren't, so don't paste those into a browser either. Don't visit any of them. One sender address in 8568 belongs to a student whose account was hacked, so I've masked it.

## AI use

I used Claude to speed up the lookups and first drafts of the notes. I reviewed every verdict and can explain each one.
