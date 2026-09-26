# sample-8265

## Facts from triage.py

- Date: Tue, 12 May 2026 12:50:14 +0100
- From: iCloud Support ☁️ <5Z5P865V@NU8RBO9APG0AENFJT0HAMSUVHSJU.com>
- Subject: Urgent: Your data is scheduled for deletion ⚠️
- Reply-To: reply-
- Return-Path: -
- SPF / DKIM / DMARC: none / none / none
- First public IP in the relay chain: 20.75.95.202
- Start of the body: Scheduled for Deletion Your account has been inactive and over-limit. Per our retention policy, your files are scheduled to be removed. Permanent Data Loss If you do not renew your storage plan soon, your data will be permanently deleted from our ser

Links:
- `hxxps://kyempapu[.]org/?act=cl&pid=1094_rd&uid=1007&cmpid=0&ofid=4626&lid=466&cid=6983baaef125cc1528f7e2f6`
- `hxxps://kyempapu[.]org/?act=un&pid=1094_rd&uid=1007&cmpid=0&ofid=4626&lid=466&cid=6983baaef125cc1528f7e2f6`

Attachments:
- none

What the script flagged:
- mentions icloud but sends from nu8rbo9apg0aenfjt0hamsuvhsju.com

## What I checked by hand

**Headers**

- From: "iCloud Support ☁️" at a random 30-character .com domain. The Sender header uses another random domain. Nothing is on Apple's domains.
- Message-ID is `randomid2@n96k.dolcevento[.]it`. "randomid2" is a template placeholder somebody forgot to fill in.
- Return-Path is empty (`<>`), and Reply-To is just `reply-`, which is broken.
- It came straight from `20.75.95.202`, which is a Microsoft Azure IP, with the HELO name `n96k.dolcevento[.]it`. I didn't check whether that .it domain is real. Nobody has scanned it on urlscan.
- SPF none, DKIM none, DMARC none, compauth fail. **Microsoft gave it SCL 9**, which is as spammy as it gets. So this one was never going to reach the inbox.
- X-Priority 1 (marked "urgent").

**Body**

- "Your data is scheduled for deletion". It says the account is over its storage limit and photos, documents and backups are "at risk". One button, "Keep My Files".
- The iCloud icon is hotlinked from freeiconspng[.]com.
- Every link goes to `kyempapu[.]org`: `/track/?act=op` (a tracking pixel), `?act=cl` (the click) and `?act=un` (unsubscribe).

**The tracking link**

- The parameters are `pid=1094_rd`, `uid=1007`, `ofid=4626`, `lid=466` and `cid=6983baaef125cc1528f7e2f6`.
- `cid` is 24 hex characters. That's the format of a MongoDB ObjectId, and the first 8 characters are a timestamp: 4 Feb 2026 21:31 UTC. My guess is that it's the ID of the honeypot address in their mailing list, and it was added that day.
- The Sender header's local part is `6983baaef125cc1528f7e2f6-466`, which is the same cid plus the same list number.

**kyempapu[.]org** (RDAP and urlscan, 26 Sep 2026)

- Registered 2023-06-27 at Namecheap. Since Aug 2026 its nameservers are parklogic[.]com, a parking service, so it looks abandoned now.
- It was hosted on OVH in France (57.129.35.27). The homepage redirects to `/brand/`, titled "Agency", which looks like a filler page.
- It has 55 scans on urlscan, from March to June 2026. Almost all are tracking links with the same `act/pid/uid/ofid/lid/cid` layout, spread over lots of different lists (272, 456, 466, 467, 506, 610...) and offers (ofid 2696 to 6082). They nearly all return 401 or 403 to the scanner, so the tracker won't show where it leads.

## Verdict

- Verdict: malicious
- Type: scam, a fake iCloud storage warning to get a payment
- Confidence: high that it's a scam, medium on the exact kind of scam
- Why: It pretends to be Apple from a random domain, has no authentication at all, and the "keep my files" link goes through a tracking server that also carries hundreds of other offers. Apple doesn't email you from a 30-letter .com.

## What I'm not sure about

- I never saw the landing page. Every scan of the tracker was blocked. "Pay a small fee for storage" is the usual pattern and would put a subscription on your card, but that's a guess based on how these usually work, not something I saw.
- My read of the parameters (uid = sender account, ofid = offer, lid = list, cid = recipient) comes from the names and how they change between scans. I haven't confirmed which tracking software this is.
- Whether dolcevento[.]it is a real Italian domain someone is borrowing the name of, or made up.
