# sample-8568

## Facts from triage.py

- Date: Sun, 19 Apr 2026 21:59:36 +0000
- From: <s######@charterschools.ae>
- Subject: Votre compte nécessite une vérification
- Reply-To: -
- Return-Path: s######@charterschools.ae
- SPF / DKIM / DMARC: pass / pass / pass (DKIM domain: charterschools.ae)
- First public IP in the relay chain: 2603:1086:300:67::12
- Start of the body: Bonjour, Conformément à la réglementation en vigueur, nous devons vérifier que votre justificatif d’identité est à jour . Afin d’éviter toute suspension de votre compte, nous vous invitons à vous connecter à votre espace client pour vérifier votre él

Links:
- `hxxps://www[.]bing[.]com/ck/a?!&&p=ba9be540dd03651973f4b01405954c0d54b9ff04ea6ae7b4c55e36a4c9462160JmltdHM9MTc3NjQ3MDQwMA&ptn=3&ver=2&hsh=4&fclid=187b` - redirect, real target is hxxps://hiremedicals[.]com/services/
- `hxxps://hiremedicals[.]com/services/`

Attachments:
- none

What the script flagged:
- nothing

## What I checked by hand

**Headers**

- The From line has no display name, just `s######@charterschools[.]ae`. The "s + 6 digits" format looks like a student account.
- The first Received line says `with mapi`, from a mailbox server inside the school's own Microsoft 365. So it was sent from Outlook while logged into that mailbox. It wasn't spoofed from outside.
- To: is "Undisclosed recipients", so everyone was in BCC.
- SPF, DKIM and DMARC all pass for charterschools[.]ae. DMARC is `p=none`, so the school only monitors and never blocks.
- **Microsoft gave it SCL 5, which means Junk.** Microsoft's filter caught it even though every authentication check passed.
- The script flagged nothing. "Nickel" isn't in its brand list, and the brand check only reads the sender name and subject, not the body.

**Body** (French)

- "Under current regulations we need to check your ID document is up to date... accounts not verified may be temporarily restricted." One button, "Accéder à mon espace client". Signed "L'équipe Nickel". Nickel is a French online bank.
- The Nickel logo is hotlinked from a presse-citron[.]net article image, not hosted by the sender.
- There are no attachments.

**The link**

- The button goes to `hxxps://www[.]bing[.]com/ck/a?...&u=a1aHR0cHM6Ly9oaXJlbWVkaWNhbHMuY29tL3NlcnZpY2VzLw`. That's a Bing search-result click link. Drop the `a1` and base64-decode the rest to get `hxxps://hiremedicals[.]com/services/`.
- The `p=` part contains `imts=1776470400`, which is 18 Apr 2026 00:00 UTC, the day before the email. It looks like the attacker searched Bing for the page and copied the result link, so the button starts with bing.com and gets past link reputation checks.

**hiremedicals[.]com** (RDAP and urlscan, 26 Sep 2026)

- Registered 2019-02-03 at GoDaddy, behind Sucuri. It's a real medical-staffing WordPress site ("Hire Medicals").
- It has 185 scans on urlscan, and most are Bing or Yahoo click links pointing at its pages, going back to Sept 2025. Where they end up changes: Temu affiliate pages, google.com, a car forum, a suspended Bluehost page, a "Security Verification" page on another site.
- 10 Apr 2026, 9 days before this email: Bing → `hiremedicals[.]com/contact-us/` (301) → `fuevwgpxwa[.]cfolks[.]pl/aa/nkl-updated/` → `Error.php`, 403 Forbidden. "nkl" matches Nickel. The scanner was in Canada, so the 403 fits a kit that only serves French visitors.
- 11 May 2026, our exact link, scanned from Canada: Bing → `/services/` (302) → `/helper/` → google.com. `/helper/` isn't a normal page on this site, and neither is `/wp-admin/css/colors/blue/post/post`, which also shows up in a scan. My read is that someone planted a script that decides where each visitor goes.
- Other Bing links on urlscan carry the same `fclid=187b27ba-23d5-6ac1-2c24-326c22036b2c` as ours, dated Mar to May 2026. So the same Bing session made a lot of these links.
- I didn't open any of it myself.

## Verdict

- Verdict: malicious
- Type: credential phishing, pretending to be Nickel (French bank)
- Confidence: high
- Why: It pretends to be a bank and uses an "ID check or your account gets restricted" threat. It came from a school student's mailbox. The link is hidden behind Bing and lands on a hacked staffing site. That same site was sending visitors to a kit folder literally named "nkl-updated" nine days earlier. A real Nickel email wouldn't come from a UAE school.

## What I'm not sure about

- I never saw the actual Nickel page. Every scan was either blocked (403) or sent to Google. The verdict rests on the lure plus the redirect chain, not on a captured login page.
- Whether the student account was phished, had a reused password, or something else. All I can say is the mail was sent from inside that mailbox.
- I didn't run WHOIS on charterschools[.]ae. urlscan shows a normal school site on Azure since 2021, which was enough for me.
- Whether hiremedicals' owner knows. The site still looked normal in Sept 2026 scans.

**Takeaway for findings:** SPF/DKIM/DMARC only prove which domain sent the mail. A hacked real account passes all three. Here, only the content and unwrapping the link showed what it was.
