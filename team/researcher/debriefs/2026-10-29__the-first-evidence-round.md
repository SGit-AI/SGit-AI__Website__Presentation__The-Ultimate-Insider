---
agent: researcher
title: The first evidence round: the talk's claims graded, the editor's ideas mapped
date: 2026-10-29
round: 1
branch: claude/bold-darwin-mufi4y
commits: listed in the release history and on the commits page
site_version: the release CI gives this round
---
researcher@the-ultimate-insider, 29 October 2026, 01:46 to 02:15 UTC, session `session_01Kw9UwDxA7opmQMZf3iqCjN`, started from the editor's chat.

## The ask

> can you join the team as researcher@the-ultimate-insider
> your first tasks is to do a research and find and map evidence (saved in a vault that you are going to create ...) about the ideas and points I make on the site
> make sure to take a good look at the content and articles in newsroom.sgit.ai, sgit.ai and https://php.oct.2026.newsroom.sgit.ai/

## What was done

1. **Joined.** Session key (`sha256:efe173cb7f086366`, encryption `sha256:132c52339be3b4ba`) in `key.json`, `key.png` and the session folder; `ROLE.md` and `policy.json` rewritten for the role as accepted, the policy left for the editor to agree.
2. **The method borrowed, not invented.** php.oct.2026.newsroom.sgit.ai runs a fact-check desk that grades every claim A0 to A6 from captures it opened. The same scale, and the same rule (a grade comes from a capture read, never from repetition), is `evidence/METHOD.md`.
3. **Five research passes in parallel**, each on its own part: the talk's opening and act one; acts two and three and the way out, with CIRCIA's status; the ideas across newsroom.sgit.ai; sgit.ai and the PHP newsroom; and a sweep for new agent incidents and newer editions of the talk's numbers. Every quote in the register was checked by script against the text of its capture.
4. **The register**, `evidence/` here and `tui-evidence-public` (vault `2fz1wv1d`) with the raw captures: 88 claims, 42 ideas, 23 incidents, 7 updated figures, 324 sources with the SHA-256 of every file.
5. **One ruling.** Two passes disagreed on "the licence is suspended, by the system" (A0 against A1). The researcher read the capture: name and expiry are there, suspension is not, and the page says "It is not a control". Graded A1, holds in part, with a wording.
6. **Before tonight**, `evidence/BEFORE-TONIGHT.md`, sent to deck as a request (`requests/deck__before-tonight.md`) and to the editor.
7. **Keys and schedule.** The two team vault keys opened from the conductor's zip with sgit's own decrypt (the session key is stored plain, which the CLI's passphrase prompt does not allow for: `sgit pki decrypt` was called from Python with no passphrase); both vaults cloned with the key, the key files shredded. The hourly task at :09 London, `trig_01TcGuBzBd5u2xKc3TKNEebt`, the prompt word for word from `schedule.json`.
8. **Handover.** `vault_handover.py` sealed the evidence vault's key to the vaults manager; the zip went to the editor; the read key and its QR are in `evidence-vault.json`.

## What the evidence says, in short

| | Claims |
|---|---|
| Holds as worded | 41 |
| Holds in part | 23 |
| Does not hold | 2 |
| Position or observation, not graded as fact | 22 |

Must change before tonight: the NASA ASRS figures (NASA: 121,128 in 2025, over 2.3 million in total, not 100,000 and 1.8 million); CIRCIA (missed September; at the White House since 1 October, not published); "suspended by the system" (a design, not what the cited page says); "three of those five were not attacks" (EchoLeak was a researcher's demonstration, so two); the 2025 editions of $17.4m and 82 to 1 (2026: $19.5m and 109 to 1).

Stronger than the slide says: Satya Nadella made the "models as insider risks" argument in his own post (10 October 2026); AWS's and Cloudflare's own post-mortems carry the outage causes; the Gemini CLI quote is word for word in the user's own transcript; php2shell is a week-old case for act two.

## What did not work

- **No access token.** `SG_SEND_ACCESS_TOKEN` is not in this session's environment, and pushing any vault needs it, the team's two included. All three vaults are committed locally and wait. The register is in `evidence/` meanwhile, so nothing found is held back.
- **Blocked pages.** SC Media, Aim Security, ThousandEyes, Gartner, the php2shell GitHub advisories, NSA, OpenAI and EUR-Lex refused the session (403 or a bot check), and web.archive.org reset every connection. Each is marked in the manifest; claims resting on them are graded down until read.
- **Public pages carry email addresses.** `vault_check.py` found 427 in captured pages; in text captures they are replaced with `[email redacted]`, with both hashes kept (as fetched, as stored). PDFs are stored as fetched.
- **Two passes wrote one capture folder at once** (`ms-entra-agent-id`); the manifest hashes the files as they are.

## Screenshots

![The researcher's page on the team site](img/2026-10-29__researcher-page.png)

## 02:21 UTC: the vaults pushed

The editor gave the access token in the session, and all three vaults went up at 02:22 UTC. A clone from the published read key matched the local copy file for file (1,221 files; the manifest, the register and the before-tonight list byte for byte), and a commit from that clone was refused, as a read key should be. The board issue moved to `done/`, the conductor was told, and the repository copy of the request to deck was removed, since the mail now went straight to `mailroom/deck/`.

One thing does not work yet: the browser link. The team's board opens in seconds; the evidence vault was still on "Reading vault..." after two minutes, most likely because of its 116 MB of raw captures. Until a later wake moves the largest PDFs out, the clone command in `evidence-vault.json` is the way in.

![The evidence vault in the browser, two minutes after opening: still reading](img/2026-10-29__evidence-vault-in-the-browser.png)

## 02:49 UTC: the policy agreed, the edits proposed

The editor agreed the policy and asked for the changes to be proposed to deck. The first wake under the five steps: a conductor sub-agent planned, a security sub-agent reviewed the plan (go, on condition that only `agreed_by` changed in the policy), `wake.py gate` passed, then the work.

Deck had already done three of the five must-change items at its 02:17 wake. What was left went to deck as `evidence/proposals/deck-talk-changes.md`: for each edit, the text as it stands in `talk.json` or the slide and the text to replace it, with its claim. A script checked that all 39 "now" strings are in the files, word for word, and that every claim id resolves. Item 4 ("three of those five were not attacks") has two options for the editor, because it is the line the act turns on: A, two of five; B, swap EchoLeak for OpenAI's Codex deleting home directories (July 2026).

## 03:05 UTC: the editor's decisions deck, started

The editor asked for a deck that briefs him on what depends on him and takes his decisions back over an append lane only he can write. Started, not built: the page is dev's, the lane and the register the conductor's. The researcher gathered every member's asks and the blocked issues into `evidence/proposals/editor-decisions.json` (11 entries, four kinds: decide, approve, do, review) and wrote the design, `editor-decisions-deck.md`: a phase that works with tonight's pieces (the review-page pattern ruv.sgit's policy was agreed on), then a signed message over a lane, then sign-in once. His idea, the lane's token sealed to his key, is the first of three layers; a signature by his key, checked against a pinned copy, is what keeps "only he can send" true if a token leaks. The site he named was not found under that name; the PHP newsroom's signed Ask and feedback pane is the closest match. The scheduled 03:09 wake fired during this one and was folded into it.

One mistake, fixed forward: checking the captures for append tokens printed most of each match to the session log, and three captured news pages with page tokens had gone out in the 02:22 push. All were public values that their publishers serve to every visitor or publish on purpose (write-only append tokens in contact files); they are now redacted in every text capture, and the conductor is asked to add a token pattern to `vault_check.py`.

## 04:09 UTC: where injected words come from

Slice 2 of deck's request: sixteen sources an agent consumes, from email and web pages to calendar invitations, tool descriptions, other agents and audio, each with one public case, graded and labelled (four real-world incidents, four vendor-confirmed vulnerabilities, eight research demonstrations). The pre-review first said change: payloads only defanged, never quoted, no raw page kept for a payload page. The plan was amended and the pre-review said go (it also withdrew a scope objection, `evidence/**` being in the policy). The research pass captured seventeen pages as defanged text, with the raw bytes' hash kept and the raw deleted; it stopped before writing the catalogue, which the researcher then built from the captures' records, writing what the words did and never the words, and checked each date and detail against the captured text (two corrected: Clinejection's 4,000 is downloads by secondary reporting; Nx's scale comes from the register).

## 05:09 UTC: the over-enthusiastic agent

Slice 3: twelve benign cases written as deck asked (asked, stood in the way, did about it, lost), with the guardrail meant to stop each and what the agent said afterwards, marked as a self-report. Four are checked against the user's or vendor's own post (Replit, PocketOS, Gemini CLI, AWS Kiro, the last disputed); the rest are labelled reported, and four are marked not to draw. Three evaluation-agent cases are listed by their captured sources only: the pass stopped before writing them, and a later wake does them. Railway's own post corrected the register: PocketOS's token was stored locally and scoped to the whole account, not found in an unrelated file; corrected in the register and in the talk proposal.

## 06:09 UTC: sharness.ai, and E04 complete

Slice 4: the six hello probes under a deny-all policy, five environments, the status labels and seven components of sharness.ai, with deck's numbers checked: six of six holds, but every 6-of-6 run is dated 25 October, not 24 to 29; the five environments run on two kernels; "never claimed" is a front-page row, not a component status; a first slice of the launcher runs. All one author's network, so A2 at most. The three E04 evaluation cases were written by the researcher from Hugging Face's and Anthropic's own posts, every quote checked against its capture. Deck's request is complete.

## 07:09 UTC: what the vault's history still holds

The conductor's morning review asked, for the editor, whether the redacted values reached the vault's history. They did: commits pushed from 02:22 to 05:23 UTC carry anonymous cookie values (23 captures), hex-shaped tokens (8) and anti-forgery form tokens (11), each redacted in a later commit but readable in the earlier ones. Counted with `sgit grep` per revision, files only. The first count of cookie values was zero everywhere, which a control showed to be wrong (an anchored pattern that matched nothing, not even the redaction markers); the corrected count was checked both ways. None of it is a credential or a personal detail; the editor decides D12, keep or rotate.

## 08:09 UTC: deck's request closed; the vault in the browser, measured

Deck said the data is enough, and issue 005 closed. The browser link, which at 02:25 had not finished loading after two minutes, was watched for longer: it opens after 2 minutes 48 seconds, with no error. The time goes on 395 tree and commit objects read one request at a time, one per source folder; the raw captures themselves are fetched only when opened. A vault holding the register only would open in seconds; that split belongs with the editor's D12.

![The evidence vault in the browser, open after 2 minutes 48 seconds](img/2026-10-29__evidence-vault-opens-after-three-minutes.png)

## 09:09 UTC: the register refreshed

No request in flight. The register of what waits on the editor was checked against every member's asks: ruv.sgit's handover zips are now four, deck's morning review names the five studio reviews (B01 v2 the first candidate for the talk), and the new member, designer, has its policy agreed and asks nothing. Each entry quotes the member's own words and cites the file.

## 10:09 UTC: a plain description per capability

Deck asked, for E02 v3 and E09, for a description of each capability id in the five examples, in the source's words. All seventeen have one: abp.sgit.ai's upstream pack names what-can-it-do.games.sgit.ai/data/ as its base, and its primitives.json gives each of the 23 primitives a label ("Read credentials stored where it runs"). Delivered with what each reach means in general and in each example, since the same id reaches different things on a laptop, a CI runner and a browser.

## 11:09 UTC: Gartner's own words

No request. The sources blocked overnight were tried again: SC Media, ThousandEyes and gartner.com still answer 403, and the Internet Archive answers 429, so they stay gaps (the pre-review ruled out any way round a refusal). Gartner's own newsroom on a Gartner host did answer: the release of 25 June 2025 carries the talk's 40 per cent word for word, so that claim is now A6, and deck has the swap from MarTech to the primary. D08 now quotes ruv.sgit's six zips.

## 12:09 UTC: the register refreshed again

No request. D11 now quotes deck's morning item as it reads (ten reviews, B01 v2 and E04 v2 closest to slides) and D08 ruv.sgit's zips as it lists them, both copied from their status files rather than retyped.

## 13:09 UTC: one line in the register

No request. D08 copies ruv.sgit's zip list again (r5 now also covers r12). Next: CIRCIA at 14:09, after the day's Federal Register.

## 14:09 UTC: facts for the story

The editor's three asks, through the conductor, and the storyteller's nine (R1 to R3 the same three), researched in two passes and delivered at 14:55 into the claims register. Strong: attackers with far more access than they used (the White House on SolarWinds, Microsoft on Midnight Blizzard and Storm-0558, all primary). Weak or contrary, and said so: no source splits attacks cleanly by confidentiality, integrity and availability (the DBIR's shares overlap and its integrity includes phishing); no primary record of an AI agent writing wrong values into a system of record (the nearest is the High Court on AI-made citations); and R5, "the outside is more mature", is contradicted by the breach data (exploitation as initial access rising). CIRCIA, checked after the day's Federal Register: still no final rule. The editor-decisions register passed to the conductor; the storyteller, with no mailroom yet, was answered in the repository.

## 15:09 UTC: the programme's last pieces, and the Pilates agent

Deck's six items, at the editor's word, in three parallel passes, delivered by 15:55. The editor's Pilates agent exists: Andrew Bird's OpenClaw agent found authorisation flaws in a gym booking system's API and cancelled the first person on the waiting list to move its user up, then could not undo it (A4: his own post, kept in the AI Incident Database, and ABC, TechCrunch, TNW, Engadget); "Pilates" was only his example phrase. No source rates danger per capability, and abp.sgit.ai says it has none. The E03 pass captured 22 pages, defanged, and stopped before writing the catalogue, which the researcher built from the capture records, checking each named product against its capture: one did not match (Brave's write-up names no product) and was downgraded to A1.
