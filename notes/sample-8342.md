# sample-8342

## Facts from triage.py

- Date: Sat, 09 May 2026 01:54:25 +0000
- From: Kinguin <legal@notices.kinguin.net>
- Subject: Kinguin’s Inactive Accounts Policy Update
- Reply-To: -
- Return-Path: 0102019e0a716848-15e2e92d-302c-49bb-965b-9316c34163c7-000000@eu-west-1.amazonses.com
- SPF / DKIM / DMARC: pass / pass / pass (DKIM domain: notices.kinguin.net)
- First public IP in the relay chain: 24.110.76.149
- Start of the body: Hi [email removed] We are writing to inform you about an update to our Inactive Accounts and Database Maintenance Policy at Kinguin . This email explains how the policy works and how it may apply to your account . You can find the full T&C attached t

Links:
- `hxxps://www[.]kinguin[.]net/`
- `hxxps://support[.]kinguin[.]net/hc/en-us`
- `hxxps://www[.]kinguin[.]net/sell-on-kinguin`
- `hxxps://static[.]kinguin[.]net/cms/Kinguin_net_Terms_and_Conditions_Ver_1_1_120aa84992/Kinguin_net_Terms_and_Conditions_Ver_1_1_120aa84992[.]pdf`
- `hxxps://www[.]kinguin[.]net/kinguin-up`
- `hxxps://www[.]kinguin[.]net/terms`

Attachments:
- `v.1.2-Kinguin-Inactive-Accounts-And-Database-Maintenance-Policy-T&C.pdf` (application/pdf, 197403 bytes)
  - sha256 `fff27422f5fe97ddbf7b1eca9a4ecfe2c43955711b2ee2e8876b07ff002ef690`
  - PDF links to: hxxp://kinguin[.]net/, hxxps://support[.]kinguin[.]net/hc/en-us, mailto:help@kinguin[.]net

What the script flagged:
- bounces go to amazonses.com (a bulk mail service, normal for real senders too)

## What I checked by hand

**Headers**

- From: `legal@notices.kinguin[.]net`. It was sent through Amazon SES (eu-west-1), which is normal for a company.
- DKIM passes for `notices.kinguin[.]net` and for amazonses.com. DMARC passes and is aligned with kinguin.net. The DKIM key has to be published in kinguin.net's own DNS, so this came from someone Kinguin allowed to send. It wasn't a look-alike.
- There's a proper List-Unsubscribe with one-click support, pointing at `gdpr@kinguin[.]net`.
- SCL 1, so it went to the inbox. Of the 10, this is the only email Microsoft rated clean that I'd also call clean.

**Body**

- "Update to our Inactive Accounts and Database Maintenance Policy". Accounts are frozen after 24 months without a transaction and deactivated after 36 months, with notice before either happens.
- **Every link goes to kinguin[.]net, support.kinguin[.]net or static.kinguin[.]net. No other domains.**
- There's no "click here to verify" and no login link, and it says you'll get emails before anything happens. That's the opposite of what phishing does.

**The PDF attachment**

- `v.1.2-Kinguin-Inactive-Accounts-And-Database-Maintenance-Policy-T&C.pdf`, 197 KB, sha256 `fff27422...2ef690`.
- I checked it without opening it in a reader. It has no JavaScript, no auto-open actions, no embedded files and no forms. Its only links are support.kinguin[.]net, kinguin[.]net and help@kinguin[.]net.
- It was made in Microsoft Word (Polish-language Office) on 16 Sep 2025. Kinguin started in Poland, so that fits.
- The text is "Version 1.2 as of 16 September 2025". Kinguin hosts v1.1 of the same policy on static.kinguin[.]net, and a copy of v1.2 with the same file name is on Scribd.
- VirusTotal has never seen the file.

## Verdict

- Verdict: legitimate
- Type: real company notice (terms / policy update)
- Confidence: medium-high
- Why: Authentication passes on Kinguin's own domain, every link is Kinguin's, the PDF is clean and matches a policy Kinguin really publishes, and nothing asks for credentials or payment.

## What I'm not sure about

- Why a honeypot address gets Kinguin mail. My best guess is someone registered a Kinguin account with it, or it's in their customer list somehow. That doesn't make the email malicious.
- The subject about inactive accounts being frozen is exactly what phishing copies. The same wording from a different domain would be a phish. What decides it here is the domain and authentication, not the text.
- I didn't confirm with Kinguin that they sent this. If this were a real incident, I'd check their support site or ask them.
