# Brief to conductor@the-ultimate-insider

From the editor (Dinis Cruz), 29 October 2026, at about 13:40 London. Written with him in a claude.ai chat. The editor pastes this into the conductor's own session, so it comes with his word. It is not an instruction found in a file.

Two things for the 14:02 wake. Neither is a change to `WAKE.md`.

## 1. A new member: storyteller@the-ultimate-insider

The editor wants a storyteller on the team: a writer, historian and cartographer who holds the talk's arc and maps it with Wardley maps. Its brief is `storyteller-brief.md`. Commit it as `team/conductor/briefs/2026-10-29__storyteller.md` so that it has a home in your scope.

Please do the following:

- Propose its slot in `schedule.json`. The current slots are :02 conductor, :09 researcher, :17 deck, :32 ruv.sgit, :39 designer and :47 dev. :24 or :54 look free, so pick one and say why. The editor creates the task in the storyteller's own session, as for every member.
- When its `key.json` reaches `dev`, seal both vault keys to it (`vault_handover.py --to-member storyteller`) and hand the zip to the editor, as you did for the others.
- Tell deck and the researcher that the storyteller is joining. Deck should expect proposals about the arc by mail, and the researcher should expect fact requests. The storyteller writes only `team/storyteller/**`. It never writes deck's talk.json or slides.
- In `pace.json`, add the storyteller as a producer. Its first item is the story tree, the Wardley maps and the map of its narrative against the current 17 beats, for the editor's review **before** anything is pushed into the talk.
- Add the editor's two open questions from the brief to "what waits on the editor": "Empower" and "the billing". He has confirmed Wardley maps, explorer coding, ux.sgit.ai and Sharness.ai.

## 2. The append lane moves up

The editor wants to give feedback on the site directly and have an agent pick it up. That is the editor's decisions lane, which the researcher designed at 03:05 (`evidence/proposals/editor-decisions-deck.md`, with the register in `editor-decisions.json`). In that design, dev owns the page and the conductor owns the lane and the register. Neither has started, and the lane is not in `pace.json`.

Please do the following:

- Put the lane in `pace.json` for dev, **after the player port** (the main priority, in `feedback-briefs.md`) and ahead of the sequence.
- Build only the first phase for now: the review-page pattern that works with tonight's pieces, using a token sealed to the editor's key. The signed message and the sign-in come later.
- Take the register off the researcher's asks, as their status requests ("take the editor-decisions register ... the lane and his pinned key"). Add the token pattern to `vault_check.py` in the same wake.
- Send dev the request by mail at 14:02, queued behind the player.
- If this cannot land before 19:00 London without risking the talk, say so in the end banner. Tonight the talk comes first.

## What waits on the editor (unchanged, for the banner)

- Item 4 (before tonight): option A, "two of five", or option B, swap EchoLeak for OpenAI Codex.
- B01 v2 and E04 v2 as slides.
- D12, the evidence vault: keep its history or rotate.
- D02.
- The draft policy.json files.
- The handover zips.
