# Findings

## Bottom line

8 of the 10 emails were malicious, 1 was spam and 1 was a real company notice. The two that reached the inbox were the most dangerous ones: fake Microsoft emails sent from real, hacked Google Workspace accounts, with invisible characters in the sender name to get past filters. Passing SPF, DKIM and DMARC told me almost nothing. Six of the nine bad emails passed SPF.

## What I looked at

10 emails caught by the Phishing Pot honeypot (a Hotmail inbox) between March and May 2026, in English, French and Portuguese. For each one I read the raw headers and HTML in a text editor. I unwrapped every link without clicking it, and pulled apart the attachments. Then I looked up the domains, URLs and file hashes on urlscan.io, VirusTotal and RDAP (the modern WHOIS). Notes for each email are in `notes/`.

| | Emails |
|---|---|
| Malicious (phishing, scam, malware) | 7978, 8062, 8216, 8265, 8370, 8568, 8582, 8614 |
| Spam | 8419 |
| Legitimate | 8342 |

Of the 9 bad ones:

- **6 passed SPF, 5 passed DKIM and 4 got a real DMARC pass.** Two more got Microsoft's "bestguesspass", which just means the domain has no DMARC record.
- **4 were sent from real hacked mailboxes** (two Google Workspace, one school Microsoft 365, one cPanel host). **2 went through real services** (someone else's SendGrid account, and Supabase's login emails). **3 came from rented Azure servers** with made-up sender domains.
- **Microsoft put 7 in Junk and 2 in the inbox.** The 2 that got through were the fake Microsoft pair. The real Kinguin email also went to the inbox, as it should.
- **I only saw the real landing page for 1 of 8** (8614, through a urlscan screenshot). The others were hidden from scanners or already gone.

## What stood out

- **Filters that match on words fail against invisible text (7978, 8062).** "Ꮇicrosoft" starts with a Cherokee letter and has 7–8 invisible characters mixed in. 8062 does it in the body text too. Both also have a piece of someone else's real email pasted under 90+ empty lines. Microsoft rated both clean.
- **Real links wrapped around bad ones (8568, 8614).** 8568 hides its target inside a Bing search click link. 8614 starts with `microsoft.com-...@` so that the real host comes after the `@`, where people don't look.
- **Hiding from scanners is normal now.** Scanners got "This IP is blocked!" (8062), were sent to google.com (8568), got a fake 404 (8370) or got 401/403 (8265, 8582). A clean scan result doesn't mean much.
- **The attackers make mistakes.** Examples: `randomid2` left in a Message-ID (8265), `$RAND` never filled in (8370, which probably broke that email's link), sender "domains" with no .com (8582, 8614), and iPhone profiles with the wrong file names and an expired certificate (7978, 8062).

## Links between emails

- **7978 + 8062: same kit, and I think the same operator.** They have the same three attachments (by hash), the same fake X-Mailer, the same Feedback-ID format, and the same pattern of a hacked Google Workspace account used from an Amazon EC2 box, 7 weeks apart. VirusTotal has had the attachments since June 2025 under 20+ file names, so this campaign is older than my sample.
- **8265 + 8582: same list.** An iCloud lure and a Chronopost lure, 5 days apart, both going through the tracker `kyempapu[.]org` with the same list ID and the same recipient ID. I read it as one mailing operation selling traffic to different scam offers, not one scammer running both pages.
- Everything else looked unrelated. See `notes/shared-infrastructure.md` for the weaker overlaps.

## Where I was wrong or couldn't confirm

- My starting hint called "yoourcargo" (8370) a typo domain. It isn't. It's a real Turkish logistics startup from 2023 whose SendGrid account is being used.
- I expected the iPhone profiles in 7978/8062 to be the main attack. Once I opened them they looked broken: no password, a certificate that expired in May 2025, and a server domain that no longer exists. I now think the link is the real attack, but I didn't test the profiles on a phone.
- 8342 (Kinguin) looks like phishing on the surface: an "inactive accounts will be frozen" message with a PDF. The domain, the authentication, the links and the PDF contents all check out, so I called it legitimate.
- The script missed things: it doesn't know the Nickel brand, it only checks the sender name and subject, and it doesn't show Microsoft's spam score (SCL). That score turned out to be one of the most useful fields.

## Limits of this

It's 10 emails from one honeypot inbox, and the honeypot address isn't a real person, so nothing here says what a real user would click. Almost all the landing pages were hidden or gone, so for most emails the verdict rests on the email and the link chain, not on a captured page. Microsoft's filter placement is only from this one Hotmail inbox. It's a small sample, and the numbers above are counts, not rates.
