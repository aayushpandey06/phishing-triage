# Things seen in more than one email

| What | Value | Emails | My take (strong link / weak link / coincidence) |
|---|---|---|---|
| attachment hash | `783cdb7425fbc29f5e35801d38a4782040da7f50e74d78de4b56eaa532eda82a` | sample-7978, sample-8062 | Strong. Same file 7 weeks apart. |
| attachment hash | `8c0013f6ee4fe229f567469ed3f1bdaf2ee6a7a4b39a04ed28df38fa25287dfb` | sample-7978, sample-8062 | Strong. On VirusTotal since Jun 2025 under 20+ names, so the kit is older than these two emails. |
| attachment hash | `ee8f15128560c2b2b4ee242026b2a2880ee604fe8489abb999ac43c969cfcdce` | sample-7978, sample-8062 | Strong. On VirusTotal since Jul 2025. |
| link domain | `kyempapu[.]org` | sample-8265, sample-8582 | On its own, weak: it's a tracker that carries lots of lists and offers. |
| server in attachment | `mail[.]escolagranderio[.]com[.]br` | sample-7978, sample-8062 | Same as the hashes, not extra evidence. The domain is gone now, so it's useless as a blocklist entry. |
| X-Mailer pattern | ``Gmail Default Mailer`s - **<random>**`` | sample-7978, sample-8062 | Strong. Not a real Gmail header, so it comes from the sending tool. |
| Feedback-ID format | `::1.eu-west-2.<random>=:<tag>` | sample-7978, sample-8062 | Strong. The tag matches the attachment names. |
| sending setup | Google Workspace login from an `EC2AMAZ-*` host, read receipt to a 2-letter address on the sender domain | sample-7978, sample-8062 | Strong together. Each one alone would be weak. |

**7978 + 8062:** I'm treating these as one campaign by one operator. The caveat is that if the kit is sold, the fingerprints only prove the same tool was used, not the same person.
| list + recipient ID | `lid=466`, `cid=6983baaef125cc1528f7e2f6` (also in the Sender header) | sample-8265, sample-8582 | Strong. The same person on the same list, mailed two different offers 5 days apart. |
| sending setup | Azure IPs with a HELO name borrowed from an unrelated .it / .si domain, no DKIM | sample-8265, sample-8582 | Weak. Lots of spammers rent Azure boxes. |

**8265 + 8582:** one mailing operation. Both came from the same list, to the same recipient ID, through the same tracker. What differs is the offer (`ofid`) and the sending account (`uid` 1007 vs 1008). My call is one list owner sending traffic to different scam offers, like a spam affiliate setup. That's not one scammer running both fake pages. The iCloud and Chronopost pages could belong to different people.
