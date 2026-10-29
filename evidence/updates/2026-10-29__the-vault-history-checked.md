# 29 October 2026, 07:25 UTC: what the evidence vault's history still holds

Asked by the conductor's morning review, for the editor: did any earlier capture with the cookie values or anti-forgery tokens since redacted reach the evidence vault's history? Yes. Every commit of this vault stays readable with the published read key, so what a commit carried is public for good, whatever later commits remove.

Counted with `sgit grep` on each revision, files only, no value printed; each count checked with a control (the redaction marker found where it should be, and nothing found after the redaction).

| Commit | Pushed (UTC) | Cookie values | Hex-shaped tokens | Anti-forgery form tokens |
|---|---|---|---|---|
| 836dfa34559e, 29d955228b9d | 02:22 | 23 files | 8 | 11 |
| d5c79f956dc5 | 03:00 | 23 | 8 | 11 |
| 9777d723e290 | 03:18 | 23 | 0 (redacted) | 11 |
| e73993e7d0dd | 04:25 | 0 (redacted) | 0 | 11 |
| ca452275ae79 | 05:23 | 0 | 0 | 11 |
| a34f9d5b9d35 (now) | 06:23 | 0 | 0 | 0 (redacted) |

What they are:

- **Cookie values**: anonymous cookies (Cloudflare bot management and similar) that websites set on the researcher's fetcher, recorded in the response headers saved beside each capture. They identify that fetch, nobody's account, and expire within hours.
- **Hex-shaped tokens**: the write-only append tokens that sgit.ai and riskmandate.ai publish on purpose in their own contact files, and page tokens from news sites.
- **Anti-forgery form tokens**: the values a website puts in its own forms for every visitor, issued to the researcher's fetcher.

None is a key, a credential to an account, a vault key or a personal detail. The only email-shaped strings in any commit are five role addresses printed by their publishers in their own reports (Verizon's DBIR, NIST's security and zero-trust contacts), inside the PDFs as published. The security pre-review of this wake judged it a finding for the editor, not a stop.

The editor's choice is D12 in `proposals/editor-decisions.json`: keep the history as it is, or move the vault to a fresh one without it (`sgit vault move`, as the conductor did for the mail vault), which changes the read key on the site.
