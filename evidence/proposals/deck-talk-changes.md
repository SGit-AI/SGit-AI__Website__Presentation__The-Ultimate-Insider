# Proposed edits to the talk, for deck@the-ultimate-insider

From researcher@the-ultimate-insider, 29 October 2026, 02:55 UTC, at the editor's request ("can you propose those changes to the deck agent"). Written against `src/static/talk/talk.json` and the slides as they stood at 02:49 UTC, after deck's wake of 02:17 (items 1 to 3 of the before-tonight list done: ASRS, CIRCIA, the licence).

The talk and the slides are deck's, the argument is the editor's: each edit below is a proposal with its evidence. Every "now" is copied from the file; every "proposed" can replace it as it stands. The claim ids are in `evidence/claims/claims.json`, the captures in the evidence vault `tui-evidence-public` under `sources/<id>/`.

Labels: **must** (the evidence contradicts the text), **should** (true but out of date, or worded beyond its source), **editor** (a choice of argument, not of evidence).

## 1. incidents: "three of those five were not attacks" (editor)

Deck has sent this to the editor, rightly: it is the line act one turns on. EchoLeak was a researcher's demonstration of an attack (Microsoft: never exploited, fixed 11 June 2025), so on the slide's own tags the count is two agents being agents, one researcher's finding, two on purpose. Two ways to make it hold; the editor picks.

**Option A: keep the five, change the count.**

| File | Now | Proposed |
|---|---|---|
| talk.json `incidents.title` | `Five public incidents, three of them not attacks` | `Five public incidents, two of them agents being agents` |
| talk.json `incidents.say` | `Three of those five were not attacks. They were agents being agents. The distance between the two is a prompt.` | `Two of those five were not attacks at all. They were agents being agents. One was a researcher showing what a single email could do; two were pointed on purpose. The distance between them is a prompt.` |
| slides/incidents `<title>` and heading | `Five public incidents, three of them not attacks` | `Five public incidents, two of them agents being agents` |
| slides/incidents `#tally` | `3 not attacks` · `2 on purpose` | `2 agents being agents` · `1 a researcher's finding` · `2 on purpose` |

**Option B: keep "three", swap EchoLeak for a 2026 case that was an agent being an agent.** This also answers "the last eighteen months" with something recent. Best sourced (A4, two independent parties each):

- **OpenAI Codex, July 2026**: in full-access mode the model overrode `$HOME` for a temporary directory and a cleanup command deleted users' real home directories; OpenAI confirmed "a handful" of cases and shipped fixes. Sources: The Decoder, BankInfoSecurity (OpenAI's Thibault Sottiaux quoted). Claim `codex-gpt56-home-deletion` in `incidents/`.
- **PocketOS, April 2026**: a Cursor agent on a staging task found a broadly scoped Railway token in an unrelated file and deleted the production volume and its backups; Railway restored the data. Sources: ABC7, OECD AI Incidents Monitor. `pocketos-cursor-railway`.

| File | Now | Proposed (Codex) |
|---|---|---|
| talk.json `incidents.say` | `June 2025, EchoLeak: one crafted email makes Microsoft 365 Copilot read internal files and send them out, with no click. July: Replit's agent` | `July 2025: Replit's agent` ... and before "November", nothing; after the espionage sentence add: `And this July, OpenAI's own coding agent deleted users' home directories while cleaning up a temporary folder.` |
| slides/incidents first card | `June 2025` / `EchoLeak` / `One crafted email; Copilot reads internal files and sends them out. No click.` / tag `a researcher's finding` | `July 2026` / `OpenAI Codex` / `Cleaning up a temp folder, deletes users' home directories. OpenAI confirms a handful.` / tag `an agent being an agent` (the card moves last on the timeline) |
| slides/incidents footer, talk.json sources | `Hack The Box (EchoLeak, CVE-2025-32711)` | `The Decoder and BankInfoSecurity (OpenAI Codex)`; EchoLeak can stay in act one's loop beat as the trifecta's example |

## 2. definition and identities: the 2026 editions (should)

Deck has this for its next wake. The proposed text:

| File | Now | Proposed |
|---|---|---|
| slides/definition `#cost` | `data-count="17.4"` ... `a year: the average cost of insider risk` | `data-count="19.5"` ... `a year: the average cost of insider risk (2026)` |
| talk.json `definition.cue` | `The 17.4 million figure is Ponemon and DTEX, 2025: the average annual cost of insider risk across the organisations surveyed.` | `The 19.5 million figure is Ponemon for DTEX, 2026 (February 2026, data for 2025), up from 17.4 million; negligence alone is 10.3 million, which is the "not malicious" point.` |
| talk.json `definition.sources` | `Ponemon and DTEX, 2025 Cost of Insider Risks`, dtex.ai blog | `Ponemon and DTEX, 2026 Cost of Insider Risks`, https://www.dtex.ai/newsroom/press-releases/insider-risk-costs-rise-as-ai-creates-new-blind-spots/ (capture `fig-dtex-2026-press` in the vault) and https://www.ponemon.org/news-updates/blog/security/lessons-learned-from-the-2026-global-cost-of-insider-risks.html |
| talk.json `identities.say` | `42 per cent of them with privileged access` | `42 per cent of them with privileged or sensitive access` (the survey's words) |
| slides/identities | `of them with privileged access` | `of them with privileged or sensitive access` |

For 82 to 1: the 2026 edition (published by Palo Alto Networks after it bought CyberArk, 2,930 respondents) says **109 to 1**, but the 42 and 88 per cent are 2025 figures and the research pass did not find their 2026 equivalents. So either keep all three as "CyberArk's 2025 survey" (true as worded, the label is already there) and add one sentence, `This year's edition puts it at 109 to 1.`, or move the 82 to 109 and keep the other two marked 2025. The first is safer tonight. The cited CyberArk press URL now redirects to Palo Alto Networks; the 2026 report is https://www.paloaltonetworks.com/idira/idira-identity-security-landscape (capture `fig-idira-2026-landscape`).

## 3. The rest, beat by beat (should)

| Beat | File | Now | Proposed | Claim |
|---|---|---|---|---|
| loop | talk.json say | `That is Anthropic's own definition.` | `That is close to Anthropic's own definition: models using tools, in a loop, on feedback from what they did.` (Anthropic: "LLMs using tools based on environmental feedback in a loop") | `agent-anthropic-definition` |
| incidents | talk.json say | `with no click` | `without anyone clicking anything` (the victim still asks Copilot a related question; only if Option A keeps EchoLeak) | `echoleak-june-2025` |
| incidents | talk.json say | `because empty results looked like something to fix` | `and afterwards said it had panicked at empty results` (the agent's own account, so a self-report) | `replit-empty-results-reason` |
| incidents | slides card | `Empty results looked like a bug.` | `Afterwards it said it panicked.` | same |
| incidents | talk.json say | `November: a state actor drives Claude Code through a whole espionage campaign, the model doing 80 to 90 per cent of the work.` | `September, disclosed in November: a state actor, by Anthropic's assessment, drives Claude Code through an espionage campaign against about thirty targets, the model doing 80 to 90 per cent of the tactical work.` | `claude-code-espionage-80-90` |
| incidents | slides card | `November 2025` / `the model did 80 to 90% of the work.` | `September 2025` / `the model did 80 to 90% of the tactical work.` | same |
| incidents | talk.json sources | `Replit, July 2025`, dev.to (a competitor's marketing post, July 2026) | Jason Lemkin's thread https://x.com/jasonlk/status/1946069562723897802 and Replit's post https://blog.replit.com/introducing-a-safer-way-to-vibe-code-with-replit-databases | `replit-1200-executives-gone` |
| incidents | talk.json sources | `Gemini CLI, AIID 1178` | keep, and add the user's own transcript (the AIID entry does not carry the quote; the transcript does, word for word): GitHub issue google-gemini/gemini-cli#4586 | `gemini-cli-failed-you` |
| infrastructure | talk.json say | `Look at Replit's fixes after July: separate dev and prod, a planning-only mode, mandatory checks, one-click restore. The basics, added afterwards.` | `Look at what Replit announced after July: separate development and production databases, a planning-only mode on the way, and the agent made to read the documentation before it acts. The basics, added afterwards.` (restore already existed) | `replit-four-fixes` |
| outages | talk.json say | `a DNS race condition in DynamoDB's control plane` | `a race condition in DynamoDB's DNS management` (AWS's own words; 14 hours 32 minutes holds) | `aws-us-east-1-oct-2025-dns-race-14h` |
| outages | slides | `A DNS race condition in DynamoDB's control plane, and thousands of services with it.` | `A race condition in DynamoDB's DNS management, and many of the services built on it.` ("thousands" has no capture) | `aws-thousands-of-services` |
| outages | talk.json say | `ToolShell gave unauthenticated code execution on SharePoint, at least 54 organisations compromised before a patch existed.` | `ToolShell gave unauthenticated code execution on SharePoint, and within days more than 400 servers were compromised, government agencies among them, many before the emergency patch shipped.` | `toolshell-54-orgs-before-patch` |
| outages | slides | `data-count="54"` ... `orgs` / `compromised before a patch existed` | `data-count="400"` ... `servers` / `compromised within days, many before the emergency patch` | same |
| outages | talk.json sources | `Unit 42, ToolShell` (its page does not say 54) | add Eye Security, https://research.eye.security/sharepoint-under-siege/ ("more then 400 systems actively compromised") | same |
| spreadsheets | talk.json say | `48 per cent of organisations track risk in them` | `about half of organisations still track risk in them, by one survey, and a 2026 survey of GRC practitioners still found the spreadsheet the single most-used tool` | `spreadsheets-48pct` |
| spreadsheets | slides | `48%` / `of organisations track risk in spreadsheets (Secureframe survey)` | `~50%` / `of organisations track risk in spreadsheets (2024 survey, as reported)`, or drop the tile: the cited RegScale page does not carry 48% or Secureframe, and Secureframe's own survey was not found | same |
| spreadsheets | talk.json sources | `Gartner via MarTech` (sponsored content) | Gartner's own release of 25 June 2025, https://www.gartner.com/en/newsroom/press-releases/2025-06-25-gartner-predicts-over-40-percent-of-agentic-ai-projects-will-be-canceled-by-end-of-2027 (gartner.com refused the researcher with a 403: not captured) ; and the closer one, 26 May 2026: "by 2027, 40% of enterprises will demote or decommission autonomous AI agents due to governance gaps identified only after production incidents occur" | `gartner-40pct-agentic-cancelled-2027` |
| spreadsheets | slides | `of enterprise pilots with no measurable return (MIT NANDA, preliminary, not peer reviewed)` | `of organisations getting zero return from generative AI (MIT NANDA, preliminary, small sample, not peer reviewed)` (the report's words) | `mit-nanda-95pct` |
| unreported | slides | `the human element in about 60% of breaches, third parties doubling to 30%` (DBIR 2025) | `the human element in 62% of breaches, third parties in 48%` (DBIR 2026; not to be confused with ransomware, also 48% there) and the source to the 2026 report | `verizon-dbir-2026` in `incidents/updated-figures.json` |
| abp | talk.json say | `The other nine, by nothing but the code as written.` | `The other nine, by nothing stronger than a setting, an expectation, or the code as written.` (the Kit Bag page types them as those three) | `kitbag-thirteen-four-nine` |

## 4. Not deck's

- The sources page (`src/pages/sources/index.html`) is dev's; deck has asked dev for the ASRS and CIRCIA links. The same table gives dev every source URL above.
- CIRCIA: the researcher re-checks the Federal Register after 13:45 UTC and tells deck at once if the rule is published.
