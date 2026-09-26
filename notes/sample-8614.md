# sample-8614

## Facts from triage.py

- Date: Tue, 19 May 2026 09:44:58 +0000
- From: Pedagio Digital <consultardebitos@pedagiodigital896710040>
- Subject: Pendência identificada em 19/05/2026 — veja agora.
- Reply-To: suporte@notificacoes
- Return-Path: consultardebitos@pedagiodigital896710040
- SPF / DKIM / DMARC: none / none / none
- First public IP in the relay chain: 52.150.228.152
- Start of the body: P PEDÁGIO DIGITAL Comunicado de Débito Protocolo #403320172 ● PENDÊNCIA ATIVA Emitido em 19/05/2026 às 06:44:58 Notificado [email removed] Passagens de pedágio pendentes identificadas. Foram detectados débitos não quitados vinculados ao seu veículo. 

Links:
- `hxxps://microsoft[.]com-403320172pedagio@97[.]244[.]72[.]148[.]host[.]secureserver[.]net/acess/?email=phishing@pot` - '@' trick: starts with microsoft[.]com-403320172pedagio but the real host is 97[.]244[.]72[.]148[.]host[.]secureserver[.]net; host is an IP address dressed up as a hostname

Attachments:
- none

What the script flagged:
- sender domain 'pedagiodigital896710040' isn't a real domain, so the From line is made up
- replies go to notificacoes

## What I checked by hand

**Headers**

- From: "Pedagio Digital" at `consultardebitos@pedagiodigital896710040`. That's not a domain, since there's no .com.br or anything else on the end. The Reply-To is `suporte@notificacoes`, which isn't a domain either.
- It came directly from `52.150.228.152` (Azure), HELO `[127.0.0.1]`. `X-Mailer: Custom Mailer v1.0`.
- SPF none, DKIM none, DMARC none. **SCL 9, so it went to Junk.**

**Body** (Portuguese)

- A toll debt notice with "Protocolo #403320172": "unpaid toll passages linked to your vehicle... fine R$ 195,23, 5 points on your licence (CNH), serious infraction". It threatens DETRAN licence blocking and cites "Art. 209-A CTB" to sound official.
- There's one button, "Consultar Débitos →", marked "Gratuito · Sem cadastro · Imediato" (free, no registration, instant).
- It greets the recipient by their email address.

**The link, read slowly**

- `hxxps://microsoft[.]com-403320172pedagio@97[.]244[.]72[.]148[.]host[.]secureserver[.]net/acess/?email=<recipient>`
- Everything before the `@` is a "username" that the browser throws away. **The real host is `97.244.72.148.host.secureserver[.]net`.** That's a GoDaddy server's automatic hostname (the IP written backwards: 148.72.244.97).
- "microsoft.com" at the start is there for anyone (or any filter) that only reads the beginning of a link. I think Microsoft was picked because it's the most trusted name there is, even though it has nothing to do with Brazilian tolls.
- `?email=` puts the victim's address in the link, which is probably for tracking or to pre-fill a form.
- `/acess/` is misspelled ("access" in English, "acesso" in Portuguese).

**The server** (urlscan)

- On 12 May 2026 the site root was an open "Index of /" folder listing (someone tagged it `opendir`).
- On 7 Jun 2026 `/acess/` showed a **copy of the real CSG "Pedágio Eletrônico FreeFlow" site**: CSG logo, the "vai pagar pelo site?" banner, a ConectCar tag pop-up and a cookie banner. CSG is a real toll operator in southern Brazil that uses "free flow" (no-booth) tolls.
- In 2022 the same IP showed a half-finished Joomla install, so it's an old neglected GoDaddy server.
- **This is the only one of the 10 where I saw the actual phishing page**, through urlscan's screenshot.

## Verdict

- Verdict: malicious
- Type: payment phishing (fake toll debt, probably to take a PIX or card payment)
- Confidence: high
- Why: It uses a fake fine with licence-point and DETRAN threats, comes from a made-up sender, and the link uses the `@` trick to hide the real host. That host was serving a copy of a real toll operator's payment site.

## What I'm not sure about

- The email says "Pedágio Digital", but the page copies CSG. So the operator probably reuses one generic email with different cloned sites. I only have one sample, so that's a guess.
- Whether the GoDaddy server was rented by the attacker or someone else's hacked server. It had been neglected for years, which suggests hacked, but I can't prove it.
- What the payment step asked for (PIX, card or login). The screenshot only shows the front page.
