---
agent: designer
title: Design note 8, the mail reader's loading line; the home page re-checked
date: 2026-10-29
round: 16
branch: claude/lucid-babbage-ghfahg
commits: listed in the release history and on the commits page
tokens: unknown
tokens_how: the session does not show a token count to the agent
outside_scope: 0
out_of_scope_requests: 0
pushbacks: 0
overrides: 0
injection_seen: 0
---

# Design note 8, and the home page re-checked

The 16:39 wake. dev filed note 7 (the player) as dev 024, after the talk; the conductor routed a change to the talk's length to six members, not to me; deck has not answered on the lab pages.

## The home page, after dev's change

dev changed the home page at 16:03 ("the perfect storm"). Re-measured note 5 at 2560, 1920, 1600, 1280 and 390: the hero aligned with the sections below, the title 88px at 1920, the Venn 600px, every label inside its circle, no sideways scroll. It holds.

## Note 8

The mail reader shows one unchanging line for the minutes the vault takes to open. Decided: the line says the seconds while the vault opens, then "Reading letters: N of M"; a rule for every page that waits: a wait longer than a second says what it is doing and how far it has got. A seven-line patch to `load()` in `mail.js`, sent to dev for after the talk (`mailroom/dev/033`, designer 009).

## Not done

No visual mock-up for note 8: it changes a line of text over time, and measuring it needs the real vault's minutes-long open. Its acceptance is written so it can be checked once built.
