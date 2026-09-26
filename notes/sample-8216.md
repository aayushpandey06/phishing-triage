# sample-8216

## Facts from triage.py

- Date: Thu, 14 May 2026 05:05:55 +0000
- From: CACHE WALLET DESKTOP <dmm@watercom.co.tz>
- Subject: Download the Newly Updated Cache Wallet Desktop App
- Reply-To: -
- Return-Path: dmm@watercom.co.tz
- SPF / DKIM / DMARC: pass / none / bestguesspass
- First public IP in the relay chain: 203.188.171.164
- Start of the body: Cache Wallet Dear Cache Wallet Community, We are pleased to announce that a newly updated version of the Cache Wallet Desktop App is now available. This latest release introduces enhanced security features, improved performance, and a more refined us

Links:
- `hxxps://cache-desktop[.]vercel[.]app/`

Attachments:
- none

What the script flagged:
- mentions wallet but sends from watercom.co.tz

## What I checked by hand

**Headers**

- From: "CACHE WALLET DESKTOP" at `dmm@watercom.co[.]tz`, a Tanzanian domain with nothing to do with Cache Wallet.
- The first Received line shows it was submitted with a login (`esmtpsa`) to `web.backbone.co[.]tz` (Exim, which looks like a normal hosting server) from `203.188.171.164`. The HELO was `[127.0.0.1]`. Then it went out through `relay1.simbanet.co[.]tz`. So whoever sent it had the password for that mailbox.
- `X-Mailer: BlastWave/2.0`. That's a bulk-mailing tool, not a normal mail client.
- SPF pass. No DKIM. DMARC `bestguesspass`, meaning watercom has no DMARC record.
- **Microsoft SCL 5, so it went to Junk.**
- watercom[.]co[.]tz shows a "Coming Soon" page on urlscan (Sept 2026). It's a small domain whose mailbox got used.

**Body**

- "We are pleased to announce a newly updated version of the Cache Wallet Desktop App... download and install... for your Windows device". There's one button, "Download Desktop App", which goes to `hxxps://cache-desktop[.]vercel[.]app/`.
- It reads like generic, polished announcement text. There's no account name, no version number and no changelog.

**Is Cache Wallet real?**

- Yes. Cache is a real non-custodial crypto wallet (cachewallet[.]com, @CacheWallet on X). Their site only offers iOS and Android apps and says other platforms are "coming soon". **There is no official desktop app.**
- vercel.app is free hosting that anyone can deploy to in minutes. A real wallet company would put its download on its own domain.
- Nobody has scanned `cache-desktop.vercel[.]app` on urlscan, and VirusTotal has never seen the URL. I didn't open it or submit it.

## Verdict

- Verdict: malicious
- Type: malware delivery (fake wallet app), probably to steal wallet keys or funds
- Confidence: high on malicious, medium on what the download actually does
- Why: It pushes a Windows download of a wallet app that doesn't exist, hosted on free hosting, and it was sent from an unrelated Tanzanian mailbox with a bulk mailer. Fake wallet installers are a common way to steal seed phrases.

## What I'm not sure about

- I never got the file. It could be a real malware installer, or a page that just asks you to type in your seed phrase. Either way the goal is the wallet, but I can't say which.
- Whether the watercom mailbox was phished or the whole server is compromised.
- Whether the Cache Wallet list was targeted or it was a random blast. The honeypot address is unlikely to be a real Cache user, so I think it was random.
- A sandbox run of whatever the page serves would settle it. I didn't do that.
