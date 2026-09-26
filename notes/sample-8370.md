# sample-8370

## Facts from triage.py

- Date: Thu, 07 May 2026 14:00:59 +0000
- From: DHL Express <info@yoourcargo.com>
- Subject: DHL Delivery Update: Outstanding Customs Fees Required
- Reply-To: -
- Return-Path: -
- SPF / DKIM / DMARC: pass / pass / pass (DKIM domain: yoourcargo.com)
- First public IP in the relay chain: 159.183.43.205
- Start of the body: Your DHL Express shipment is on hold awaiting customs clearance. Tracking: KRJALKJ. Action required within 48 hours. Action Required: Your shipment is pending customs clearance. A duty payment is required to release your parcel. Shipment Update Dear 

Links:
- `hxxps://nuepilates[.]com[.]au/play[.]php?r=$RAND`
- `hxxps://fonts[.]googleapis[.]com/css2?family=Inter:wght@400;500;600;700;800&display=swap`

Attachments:
- none

What the script flagged:
- mentions dhl but sends from yoourcargo.com

## What I checked by hand

**Headers**

- From: "DHL Express" at `info@yoourcargo[.]com`.
- It really went through **SendGrid**, account `u13555177`. The first hop is `geopod-ismtpd-4 (SG)`, then it left from `outbound-mail.sendgrid[.]net`. The `X-SG-EID` header and the bounce address `em1635.yoourcargo[.]com` fit a normal SendGrid setup.
- SPF, DKIM (`s1`, d=yoourcargo.com) and DMARC all pass. SendGrid is set up properly on this domain.
- **Microsoft SCL 5, so it went to Junk.**

**Is yoourcargo a typosquat?**

- My starting hint said "yoourcargo" was a misspelling. **The WHOIS doesn't support that.** yoourcargo[.]com was registered on 2023-11-29 at GoDaddy and uses Cloudflare DNS. On urlscan it's a real Turkish logistics startup ("YoourCargo | Hızlı ve Güvenilir Dijital Lojistik"), seen from Nov 2024 to Aug 2025, and yorkargo[.]com redirects to it.
- So the domain isn't pretending to be anything. It's a real small company, and someone is **using their SendGrid account**, probably through a leaked API key. That's a lot more likely than the company sending DHL scams itself.

**Body**

- "Your DHL Express shipment is on hold awaiting customs clearance... duty payment required... returned to sender if not paid within 48 hours". It has made-up tracking numbers, the weight and size of the parcel, and DHL's real Bonn address in the footer.
- The images are hotlinked from dhl[.]com and from a WordPress plugin banner (`ps.w[.]org/dhl-for-woocommerce`), and the icons from flaticon.
- The button "Pay Customs Duty & Track Shipment" goes to **`hxxps://nuepilates[.]com[.]au/play[.]php?r=$RAND`**.
- **`$RAND` is a template variable that never got filled in.** The sending tool was meant to put a random ID there.

**nuepilates[.]com[.]au** (urlscan)

- It's a real Pilates studio site ("Nue Pilates") on WHG hosting.
- There are 30 scans in May 2026 of `play.php`, `read.php` and click links from a **different SendGrid account** (`u37822859`), all landing on it. Every one ended at `page-not-found.php` or `404-not-found.php` with a 404. Scans using the literal `$RAND` got the same 404.
- A Pilates studio doesn't need `play.php` and `read.php`. It looks hacked and used as a redirector that shows scanners a fake 404.

## Verdict

- Verdict: malicious
- Type: payment-card phishing (fake DHL customs fee)
- Confidence: high
- Why: It pretends to be DHL and demands a customs payment within 48h. It was sent through another company's SendGrid account, and the pay button goes to a script planted on an unrelated Pilates studio's site.

## What I'm not sure about

- **The link in this particular email might not have worked.** Because of the `$RAND` bug, scans of that exact URL returned 404. The redirector might ignore the parameter for real visitors, but I can't tell.
- Whether yoourcargo knows their SendGrid account is being used. It'd be worth telling them and SendGrid.
- The same redirector turns up behind two SendGrid accounts. That could be one operator with several stolen keys, or a shared kit. I'm not calling it.
