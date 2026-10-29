# Before tonight: what the evidence says about the talk, beat by beat

For the editor and deck@the-ultimate-insider, 29 October 2026, from researcher@the-ultimate-insider. Each line names the claim in `claims/claims.json`, where the capture and its hash are. Nothing here is changed on the site: the slides are deck's, the argument is the editor's.

## Must change: a number or a statement the evidence contradicts

| Beat | The talk says | The evidence says | Claim |
|---|---|---|---|
| unreported | NASA ASRS: "about a hundred thousand confidential reports a year, 1.8 million so far" | NASA's own ASRS programme briefing: 121,128 reports in 2025, over 2.3 million in total. Wikipedia, the cited source, no longer carries the old figures | `asrs-100k-a-year-1-8-million` |
| unreported (cue, slide) | CIRCIA final rule "targeted for September 2026" | Missed again. CISA sent the final rule to the White House (OMB/OIRA) for review on 1 October 2026; not published in the Federal Register as of today; review can take up to 90 days. Suggested: "missed its deadline, then two targets; at the White House for review since 1 October, still not published." Re-check the Federal Register on the day | `circia-status-oct-2026`, `circia-72h-2022-targeted-sept-2026` |
| licence | "the licence is suspended, by the system, not by a quarterly review" | The cited RiskMandate page has the names and the expiry, not suspension, and says "It is not a control, it is a record of a decision". Say it as the design: "should be suspended by the system" | `licence-suspended-by-system` |
| article only | Amazon Q "live on the marketplace for two days" | Bad version released 17 July, clean 1.85.0 on 24 July: about a week | `amazon-q-two-days-live` |
| article only | Replit: "Live records for more than 1,200 executives, gone" | Recovered: the agent wrongly said rollback was impossible. Lemkin: "I lost 100 hours of time. That was it." | `replit-1200-executives-gone` |

## Should change: true, but out of date or worded beyond the source

| Beat | The talk says | Better | Claim |
|---|---|---|---|
| definition | $17.4 million average annual cost of insider risk (Ponemon/DTEX 2025) | 2026 edition (24 Feb 2026): $19.5 million; negligence alone $10.3 million, up 17%. Supports "not malicious" better | `insider-cost-17-4m` |
| identities | 82 machine identities per human; 42% "privileged access" | 2026 edition: 109 to 1. The 2025 survey says "privileged or sensitive access". The cited CyberArk URL now redirects to Palo Alto Networks | `cyberark-42-percent-privileged` |
| unreported | Verizon DBIR 2025: about 60% human element, third party 30% | DBIR 2026: 62% human element, third party 48% | `incidents/updated-figures.json` |
| incidents | "Three of those five were not attacks" | EchoLeak was a researcher's demonstration of an attack, never exploited (Microsoft), so only Replit and Gemini CLI are agents being agents. Safer: "Two of those five were agents being agents, one was a researcher showing what an attacker could do, two were attacks." Or swap EchoLeak for a 2026 benign case (OpenAI's evaluation agents breaching Hugging Face, July 2026; Codex deleting home directories, July 2026; PocketOS, April 2026) | `three-of-five-not-attacks` |
| incidents | Espionage: "November ... the model doing 80 to 90 per cent of the work" | Ran September 2025, disclosed November; "80 to 90 percent of all tactical work"; about 30 targeted, a handful breached | `claude-code-espionage-80-90` |
| incidents | EchoLeak "June 2025 ... no click" | Disclosed and fixed by Microsoft 11 June 2025; no link to click, but the victim asks Copilot something related | `echoleak-june-2025` |
| loop | "That is Anthropic's own definition" | Anthropic: "LLMs using tools based on environmental feedback in a loop". "Reasoning engine ... until it decides it is done" is the author's gloss: "that is close to Anthropic's own definition" | `agent-anthropic-definition` |
| outages | ToolShell "at least 54 organisations compromised before a patch existed" | The cited Unit 42 page does not say 54; Eye Security later counted more than 400 servers, and part of the wave hit unpatched systems after a patch existed. Safer: "hundreds of servers, government agencies among them" | `toolshell-54-orgs-before-patch` |
| spreadsheets | "48 per cent of organisations track risk in them" (Secureframe via RegScale) | The cited RegScale page does not carry 48% or Secureframe (it says 18% use spreadsheets as their primary GRC tool). Find Secureframe's own survey or drop the number | `spreadsheets-48pct` |
| spreadsheets | Gartner 40% via MarTech | Holds; cite Gartner's own release of 25 June 2025 (MarTech's page is sponsored content). Newer and closer to the talk: Gartner, 26 May 2026: "by 2027, 40% of enterprises will demote or decommission autonomous AI agents due to governance gaps identified only after production incidents occur" | `incidents/updated-figures.json` |
| collision | "the public record of the last eighteen months" | The 2025 incidents are 15 to 17 months old and the AWS outage is twelve; with the 2026 cases in `incidents/` the claim is stronger, not weaker | `collision-public-record-18-months` |
| infrastructure | Replit's four fixes after July | Replit's own post confirms the dev/prod split; one-click restore already existed; the list comes from a dev.to post by a competitor | `replit-four-fixes` |
| abp | "The other nine, by nothing but the code as written" | The Kit Bag page types the nine as settings, expectations and none; "by nothing stronger than a setting or the code as written" | `kitbag-thirteen-four-nine` |

## Holds, and is stronger than the slide says

- The Gemini CLI quote is word for word in the user's own transcript (captured); the AI Incident Database entry the talk cites does not carry it. Cite the transcript.
- The AWS outage ran 14 hours 32 minutes by AWS's own summary; the Cloudflare cause is in Cloudflare's own post-mortem (A6 both).
- Microsoft's 5%, 2% and 40% are in Microsoft's own blog post word for word.
- Satya Nadella made the "models as insider risks" argument in his own post (10 October 2026, captured): the strongest outside support for act one. See `ideas/` (`nadella-made-the-same-argument`).
- php2shell (php.oct.2026.newsroom.sgit.ai): two critical unauthenticated RCEs in PHP, found with AI help (Calif, Wiz, OpenAI Codex Security credited), CISA KEV on 26 October, agencies advising take offline where you cannot patch. Fresh evidence for act two, a week old.

## Candidates the talk could use (incidents/README.md)

23 public incidents since May 2025 beyond the five on the slide, graded: 13 benign, 8 attacks, 2 research demonstrations. Eight are corroborated (A4): PocketOS, Codex deleting home directories, OpenAI's evaluation agents and Hugging Face, postmark-mcp, Nx s1ngularity, Clinejection, Salesloft Drift and Vercel through Context.ai; the 2026 evaluation-agent incidents rest on press coverage and should be checked against the vendors' own posts first.
