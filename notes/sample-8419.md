# sample-8419

## Facts from triage.py

- Date: Fri, 01 May 2026 08:46:33 +0000
- From: Supabase Auth <noreply@mail.app.supabase.io>
- Subject: Your account access — action needed
- Reply-To: -
- Return-Path: pm_bounces@pm-bounces.mail.app.supabase.io
- SPF / DKIM / DMARC: pass / pass / pass (DKIM domain: pm.mtasv.net)
- First public IP in the relay chain: 104.245.209.246
- Start of the body: Hi there, I hope this finds you well. I wanted to reach out because I think what we offer at HDOTV might genuinely be useful for you. We run a streaming service that gives you access to a large collection of channels covering sports, entertainment, n

Links:
- `hxxps://hdoiptv[.]com`
- `hxxps://hdoiptv[.]com/#ourprices`
- `hxxps://hdoiptv[.]com/unsubscribe`
- `hxxps://supabase[.]com/?utm_source=auth-email&utm_medium=email&utm_campaign=powered-by-supabase`
- `hxxps://supabase[.]com/opt-out/njdbogzkmnnonpujrgio`

Attachments:
- none

What the script flagged:
- DKIM signed by pm.mtasv.net, not the sender's domain

## What I checked by hand

**Headers**

- From: "Supabase Auth" at `noreply@mail.app.supabase[.]io`. It's really Supabase's mail, sent through **Postmark** (`mtasv.net`, Feedback-ID ends in `postmark`).
- DKIM passes twice, for `mail.app.supabase[.]io` and for `pm.mtasv[.]net`. SPF passes and DMARC passes. Nothing is spoofed.
- **Microsoft SCL 5, so it went to Junk.**

**Body**

- The subject is "Your account access — action needed", which sounds like a security email to get it opened. The body is actually an IPTV sales pitch: "HDOTV", channels from the US, UK, France, Spain and Arabic regions, "8K", 3 months for 19 instead of 29, signed "Alex".
- The links go to `hdoiptv[.]com` (home, prices, unsubscribe).
- At the bottom is Supabase's own footer ("You're receiving this email because you signed up for an application powered by Supabase ⚡️") and a Supabase opt-out link with the project ID `njdbogzkmnnonpujrgio`.

**How a spammer got Supabase to send it**

- Supabase gives every project a login system that sends emails (sign-up confirmation, invite, magic link), and the project owner can edit what those emails say.
- The most likely setup: someone made a Supabase project, replaced the email text with this ad, and triggered sign-ups or invites for addresses from a list. Supabase then sends it from its own well-trusted domain, and the footer shows it's a project email.
- I haven't reproduced it, and Supabase may limit this on free projects, so this is my best explanation, not something I confirmed.

**hdoiptv[.]com** (urlscan)

- "Hdoiptv BEST IPTV Service USA - UK And Worldwide", scanned Feb and Mar 2026. It was hosted on Contabo and before that behind Cloudflare. urlscan puts the domain at about 2.5 years old.
- Cheap subscriptions for "thousands of channels from everywhere" are usually unlicensed resellers. I didn't check if this one is.

## Verdict

- Verdict: spam
- Type: unsolicited advertising (IPTV) through a trusted platform's email system
- Confidence: high
- Why: There's no fake login, no request for credentials, no malware and no fake brand. The subject is misleading, and it abuses Supabase to get a trusted sender, but what it wants is for you to buy an IPTV subscription.

## What I'm not sure about

- Whether "spam" is too soft. If the IPTV service is illegal or just takes the money, it's closer to a scam. I didn't buy anything, so I can't say.
- Whether the subject line alone should push it up a category. I kept it at spam because the body doesn't pretend to be anything else.
- For a defender, the useful part is the project ID in the opt-out link. That's what you'd report to Supabase to get the project shut down.
