# sample-8062

## Facts from triage.py

- Date: Thu, 21 May 2026 11:19:59 +0000
- From: Ꮇicrosoft Bill Teams <bd@tabayouth.com>
- Subject: Billing Information Requires Attention
- Reply-To: -
- Return-Path: bd@tabayouth.com
- SPF / DKIM / DMARC: pass / pass / pass (DKIM domain: tabayouth.com)
- First public IP in the relay chain: 2600:1f10:44b3:5b00:a845:5e8f:502f:1788
- Start of the body: Dear Customer, We recently encountered an issue while attempting to process a scheduled payment connected to your account. To help maintain uninterrupted service access, please review your current billing preferences and verify that your payment info

Links:
- `hxxps://www[.]tabayouth[.]com`

Attachments:
- `emails-g11njobs.mobileconfig` (application/octet-stream, 5396 bytes)
  - sha256 `8c0013f6ee4fe229f567469ed3f1bdaf2ee6a7a4b39a04ed28df38fa25287dfb`
  - .mobileconfig is not something a normal sender attaches
  - sets up com.apple.caldav.account on mail[.]escolagranderio[.]com[.]br
- `carddav-g11njobs.mobileconfig` (application/octet-stream, 5230 bytes)
  - sha256 `783cdb7425fbc29f5e35801d38a4782040da7f50e74d78de4b56eaa532eda82a`
  - .mobileconfig is not something a normal sender attaches
  - sets up com.apple.carddav.account on mail[.]escolagranderio[.]com[.]br:2080
- `caldav-g11njobs.mobileconfig` (application/octet-stream, 6350 bytes)
  - sha256 `ee8f15128560c2b2b4ee242026b2a2880ee604fe8489abb999ac43c969cfcdce`
  - .mobileconfig is not something a normal sender attaches
  - sets up com.apple.mail.managed on mail[.]escolagranderio[.]com[.]br, mail[.]escolagranderio[.]com[.]br

What the script flagged:
- sender name: 8 invisible characters
- sender name: look-alike letters: Ꮇ (Cherokee Letter Lu)

## What I checked by hand

Same setup as 7978, so see that note. Only the differences are here.

**Headers**

- Sender name is "Ꮇicrosoft Bill Teams", with the same Cherokee Ꮇ and 8 invisible characters. The invisible characters are in the body text as well this time ("Update billing information", "© 2026 Microsoft", the Redmond address), so phrase matching on the body fails too.
- Real sender is bd@tabayouth[.]com, sent through smtp.gmail.com from `EC2AMAZ-EJC2KS7` (another Amazon Windows box).
- SPF, DKIM and DMARC all pass. Unlike 7978, this is a real DMARC pass because tabayouth has a DMARC record. It still doesn't help, because the mail really did come from their account.
- SCL 1, so it went to the inbox.
- To: is `notification.noreply@email.microsoft[.]com`, which is fake. The real target was BCC'd.
- The Message-ID uses `@tabayouth[.]com` this time, but it has the same number layout as 7978's.
- It has the same fake X-Mailer pattern, a read receipt to `ea@tabayouth[.]com`, and a Feedback-ID with `eu-west-2...:g11njobs`.

**Body**

- The lure is "we couldn't process a scheduled payment, please update your billing info". The button goes to `hxxps://www[.]tabayouth[.]com`.
- The logo is made of the same four coloured cells.
- There are 93 empty lines, then a pasted piece of an unrelated Chinese-language email (a Taiwanese political message). It still has Outlook's `data-olk-copy-source` tag, so it was copied from someone's real mailbox. Same filler trick as 7978, different text.

**Domain** (RDAP and urlscan, 26 Sep 2026)

- tabayouth[.]com was registered on 2015-12-29 at Namecheap. Nameservers are ns1/ns2.am99[.]com[.]pk.
- On urlscan it was "TABA YOUTH FORCE" in Jan 2024. By May 2025 it redirected to taba-foundation[.]com ("TABA Foundation"). So it's a real charity.
- Someone scanned the link from the UK on 21 May 2026 at 11:39 UTC, 20 minutes after this email was sent. The page came back as just **"This IP is blocked!"**, 0 kB. A charity homepage doesn't do that. It looks like a phishing kit's anti-bot check hiding the real page from scanners.

**Attachments**

- These are the same three files as 7978, with the same SHA-256 hashes, just renamed with `g11njobs`. See 7978 for what they are.
- The mail-account profile (`ee8f...`) is on VirusTotal too: 0/61, community score -43, first seen 17 Jul 2025. Its other names include `InboxRules-8255214102.pdf`, `caldav-pakistansweets` and `caldav-vansickles`.

## Verdict

- Verdict: malicious
- Type: credential / payment-card phishing, pretending to be Microsoft
- Confidence: high
- Why: It's the same kit as 7978: the same attachments, the same header fingerprints and the same sending setup, seven weeks later from a different hacked-looking domain. The sender name is fake Microsoft, it asks you to update payment info, and the link is cloaked from scanners.

## What I'm not sure about

- "This IP is blocked!" could be a normal hosting firewall rather than the kit. I think it's the kit, because it's plain text with no branding and a real charity site shouldn't block a UK scanner, but I haven't proven it.
- I'm calling 7978 and 8062 the same operator. If this kit is sold or shared, they could be two different customers using the same tool. The matching fingerprints only prove the same software was used.
- The tag names (quarksseg, g11njobs, and on VirusTotal yosoy, vigilantprayer, pakistansweets...) look like names of other domains or accounts the kit has used. I haven't checked that.
