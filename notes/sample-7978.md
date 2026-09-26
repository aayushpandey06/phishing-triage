# sample-7978

## Facts from triage.py

- Date: Mon, 30 Mar 2026 17:45:19 +0000
- From: Ꮇicrosoft Ꮇail Supports <co@brighthomedaycare.com>
- Subject: Terms Update Effective Mon, March 30, 2026
- Reply-To: -
- Return-Path: co@brighthomedaycare.com
- SPF / DKIM / DMARC: pass / pass / bestguesspass (DKIM domain: brighthomedaycare.com)
- First public IP in the relay chain: 2a05:d01c:f37:6300:569f:d15f:9569:3e0b
- Start of the body: Important Update to Service Terms Hello, We have made important changes to our Service Terms that now apply to your account and the services you are using. These revisions were created to make the terms easier to understand and to include recent impr

Links:
- `hxxps://www[.]v2[.]brighthomedaycare[.]com/`

Attachments:
- `emails-quarksseg.mobileconfig` (application/octet-stream, 5396 bytes)
  - sha256 `8c0013f6ee4fe229f567469ed3f1bdaf2ee6a7a4b39a04ed28df38fa25287dfb`
  - .mobileconfig is not something a normal sender attaches
  - sets up com.apple.caldav.account on mail[.]escolagranderio[.]com[.]br
- `carddav-quarksseg.mobileconfig` (application/octet-stream, 5230 bytes)
  - sha256 `783cdb7425fbc29f5e35801d38a4782040da7f50e74d78de4b56eaa532eda82a`
  - .mobileconfig is not something a normal sender attaches
  - sets up com.apple.carddav.account on mail[.]escolagranderio[.]com[.]br:2080
- `caldav-quarksseg.mobileconfig` (application/octet-stream, 6350 bytes)
  - sha256 `ee8f15128560c2b2b4ee242026b2a2880ee604fe8489abb999ac43c969cfcdce`
  - .mobileconfig is not something a normal sender attaches
  - sets up com.apple.mail.managed on mail[.]escolagranderio[.]com[.]br, mail[.]escolagranderio[.]com[.]br

What the script flagged:
- sender name: 7 invisible characters
- sender name: look-alike letters: Ꮇ (Cherokee Letter Lu)

## What I checked by hand

**Headers**

- Sender name is "Ꮇicrosoft Ꮇail Supports". The Ꮇ is Cherokee (U+13B7), and there are 7 invisible characters (U+E0139) mixed into the name. Both are there so a filter looking for "Microsoft" doesn't match.
- Real sender is co@brighthomedaycare[.]com. It was sent through smtp.gmail.com with a login (ESMTPSA) from a machine called `EC2AMAZ-A9QNUAT`. That's the default name Windows servers get on Amazon EC2, so someone rented a cloud box and logged into the daycare's Google account from it.
- SPF and DKIM pass. The DKIM selector is `google`, so the domain uses Google Workspace. DMARC says `bestguesspass`, which only means the domain has no DMARC record. It's not a real pass.
- Microsoft gave it SCL 1, so it landed in the inbox.
- To: is `customer@postmaster.microsoft365[.]com`. That's fake. The honeypot address was in BCC.
- Message-ID ends in `@csp-obgw-0005a.ser.ppops[.]net`. ppops.net belongs to Proofpoint, but the Received chain shows the mail never touched Proofpoint. So it was made up. My guess is it's meant to look like it already passed a mail filter, but I don't know.
- ``X-Mailer: Gmail Default Mailer`s - **<random>**``. Gmail doesn't add that. It's a fingerprint of whatever tool sent this.
- `Disposition-Notification-To: ca@brighthomedaycare[.]com` asks for a read receipt, so the sender finds out which addresses are real.
- `Feedback-ID` ends in `eu-west-2...:quarksseg`. "quarksseg" is also in the attachment names.

**Body**

- It starts as a "terms update" and then pushes you to "sign in and review your payment method". The only link is the button, which goes to `hxxps://www[.]v2[.]brighthomedaycare[.]com/`.
- The Microsoft logo is four coloured table cells, not an image.
- The HTML is also stuffed into the text/plain part, which is sloppy.
- Under the message there are 94 empty lines and then a chunk of somebody else's real email (a law-firm thread from Nov 2024). I think it's filler to confuse spam filters. It has real names and a phone number in it, so I'm not copying it here.

**Domain** (RDAP and urlscan, 26 Sep 2026)

- brighthomedaycare[.]com was registered on 2008-10-24 at GoDaddy. Nameservers are ns1/ns2.peacesoft[.]in.
- On urlscan it was a normal "Bright Home DayCare" site in April 2025.
- In Oct/Nov 2019 someone scanned `/kim/mfile/` on the same site. That's not a normal path for a daycare, so it may have been hacked before.
- Nobody has scanned the `v2.` subdomain. I didn't open it. A subdomain means whoever did this can probably change the domain's DNS too, not just use its email.

**Attachments**

- There are three `.mobileconfig` files. They're cPanel's "set up this mailbox on iPhone" profiles for `blutrgr@eu40.escolagranderio[.]com[.]br`:
  - one mail account (IMAP 993, SMTP 465)
  - one calendar (CalDAV, port 2080)
  - one contacts account (CardDAV)
- The names don't match what's inside: `emails-` sets up the calendar and `caldav-` sets up the mail account.
- There's no password in any of them.
- They're signed with a Let's Encrypt cert for `*.escolagranderio[.]com[.]br`, valid 2 Feb to 3 May 2025. The signing time is 16 Feb 2025, so the cert had been expired for about 11 months when this email went out.
- registro.br RDAP returns 404 for escolagranderio[.]com[.]br. The domain doesn't exist anymore.
- VirusTotal gives 0/62 detections, but that doesn't say much because it's a config file, not malware. First seen 27 Jun 2025, under 20+ names like `KYC_Policy_Agreement`, `Compliance...`, `Apple Devices Installer.exe`, `emails-yosoy` and `emails-vigilantprayer`. `email-blutrgr.mobileconfig` is probably the original name.
- I couldn't test them on an iPhone.

## Verdict

- Verdict: malicious
- Type: credential / payment-card phishing, pretending to be Microsoft
- Confidence: high
- Why: The sender name is made to look like Microsoft and built to get past filters. It was really sent from a daycare's Google account through an Amazon cloud server. The only link goes to a subdomain of the daycare's site and asks me to sign in and check my payment method. Nothing here is actually Microsoft.

## What I'm not sure about

- Whether the daycare's Google account was hacked or the domain was sold. The registration has run since 2008 without a break and the site looked normal in 2025, so I lean towards hacked.
- What's on `v2.brighthomedaycare`. I didn't open it and nobody has scanned it.
- The attachments. I think they're leftovers the kit keeps attaching: no password, expired cert, domain gone. I can't rule out that the idea was to get someone to type a password into the iPhone's login prompt, though. I'd need a test phone to check.
- Why the Message-ID pretends to be Proofpoint.
