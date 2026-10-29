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
