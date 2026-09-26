# sample-8582

## Facts from triage.py

- Date: Sun, 17 May 2026 08:01:12 +0100
- From: Chronopost ✅ <no-reply@dxxdguoogrctsl>
- Subject: Votre colis est bloqué au centre 📦
- Reply-To: reply-4WN707E7L8XH0Y5UFO1FK0YW@in2.getdrip.com
- Return-Path: return@maks-viktor.si
- SPF / DKIM / DMARC: softfail / none / none
- First public IP in the relay chain: 20.205.190.185
- Start of the body: LOGISTICS EXPRESS GLOBAL TRACKING SYSTEM ⚠️ ACTION REQUISE Votre colis est bloqué au centre Référence de suivi #FR-9822-TK Bonjour phishing@pot , Une erreur d'adresse ou des frais de douane impayés (0,99€) empêchent la livraison. Statut actuel En att

Links:
- `hxxps://kyempapu[.]org/?act=cl&pid=1313_rd&uid=1008&cmpid=0&ofid=5114&lid=466&cid=6983baaef125cc1528f7e2f6`
- `hxxps://kyempapu[.]org/?act=un&pid=1313_rd&uid=1008&cmpid=0&ofid=5114&lid=466&cid=6983baaef125cc1528f7e2f6`

Attachments:
- none

What the script flagged:
- mentions chronopost but sends from dxxdguoogrctsl
- sender domain 'dxxdguoogrctsl' isn't a real domain, so the From line is made up
- replies go to in2.getdrip.com
- bounces go to maks-viktor.si

## What I checked by hand

**Headers**

- From: "Chronopost ✅" at `no-reply@dxxdguoogrctsl`. That's no domain at all, since there's no .com or .fr on the end.
- The Sender header is `<6983baaef125cc1528f7e2f6-466@...>`, **the exact same cid and list number as 8265**.
- The Message-ID ends `@geopod-ismtpd-4-4`. That looks copied from SendGrid's Message-IDs (SendGrid uses host names like that). The mail never went near SendGrid.
- Reply-To is `...@in2.getdrip[.]com`. Drip is a real email marketing company. This looks copied from a real Drip email to make the headers look normal.
- Return-Path is `return@maks-viktor[.]si`. It came from `20.205.190.185` (Azure again) with the HELO name `fptg.maks-viktor[.]si`. SPF softfail. No DKIM, no DMARC.
- **SCL 9** again, straight to Junk.

**Body** (French)

- "Your parcel is stuck at the depot". It blames a wrong address or **€0.99 unpaid customs fees**, says "expires in 14 hours" and has a button, "RÉGLER MA LIVRAISON MAINTENANT" (pay for my delivery now). It says the parcel goes back with storage fees if you don't act within 24h.
- It greets the recipient by their email address.
- Apart from the From name, the body doesn't actually say Chronopost. It says "LOGISTICS EXPRESS GLOBAL TRACKING SYSTEM" and "Global Logistics". So the template is generic and only the sender name gets swapped.
- All three links are `kyempapu[.]org` again: `pid=1313_rd`, `uid=1008`, `ofid=5114`, `lid=466`, `cid=6983baaef125cc1528f7e2f6`.

**Compared with 8265**

| | 8265 | 8582 |
|---|---|---|
| Lure | iCloud storage | Chronopost parcel |
| Language | English | French |
| Sent | 12 May 2026 | 17 May 2026 |
| uid | 1007 | 1008 |
| ofid (offer) | 4626 | 5114 |
| lid (list) | 466 | 466 |
| cid | 6983baae... | 6983baae... (same) |
| Sending IP | Azure | Azure |

Different lure, language and offer, but the same list and the same recipient ID. See 8265 for what I found on kyempapu[.]org.

## Verdict

- Verdict: malicious
- Type: scam, a fake parcel "customs fee" to get card details
- Confidence: high
- Why: It's a classic small-fee parcel scam. The sender address isn't even a valid domain, the headers are borrowed from real mail services, and it goes through the same tracker, list and recipient ID as the iCloud one.

## What I'm not sure about

- Same as 8265: I didn't see the payment page. The €0.99 fee is the usual trick to get a card number, often for a hidden subscription or to reuse the card. I'm going by the pattern.
- Whether "uid" is two different senders renting the same platform, or one operator with two accounts. See `shared-infrastructure.md` for how I called it.
