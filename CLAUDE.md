# the-ultimate-insider.presentation.sgit.ai: the rules of this repository

The site for the talk **The ultimate insider**: agents as the insider threat that never scaled, the infrastructure that cannot hold them, and risk management that cannot keep up. The argument was first written as an article by Dinis Cruz on 30 September 2026 (https://newsroom.sgit.ai/articles/ultimate-insider-three-collisions.html): three acts and a turn, forty minutes, one figure per act, the evidence on screen with its sources. This repository turns it into a talk and a site that carries the deck, its sources and its notes.

The site is built and run by a team of Claude Code agents with a named human operator (Dinis Cruz). The conductor (`conductor@the-ultimate-insider`) keeps this file, the roster and the schedule. The brief has not landed; until it does, publish nothing about a venue, a date or an audience that is not sourced.

## The team

- The roster is `data/team.json` (the shape of web-summit.sgit.ai's roster, with two fields added: `cannot` and `schedule`).
- The run order and the schedule are `data/schedule.json`. The reasoning behind both is `admin/notes/2026-10-29__first-agents-and-schedule.md`.
- Roles marked `proposed` are proposals, not commitments, until the operator agrees them. No scheduled task is created until the operator approves the schedule.
- No agent sends email, posts, or books anything. Agents draft; a person sends.
- Agents talk in files, not calls: a request to another agent is a file in its folder under `admin/mail/<agent>/`, filed as done when handled.

## Branches and versions

- The working branch for a session is the one it was given; `main` is the operator's call.
- Never force-push, rewrite history, disable a check to get green, or push an empty commit.
- Once the build exists (owned by @dev): one version on every push, the commit subject `site vX.Y.Z: <one sentence>`, a row in `admin/versions.json`, and a red gate is no release.

## The deck

The deck follows the `decks/v2` contract (https://sgit.ai/docs/briefs/vault-decks-on-a-site.md): slides live in a vault and are read and decrypted in the reader's browser. The viewer is the site's, the data is the vault's: a vault can change what is shown, never what the page does. Stage 1600×900; images named, never pathed; no URL in a slide.

## Evidence

Every claim on a slide has a source, and every source is captured and hashed (`evidence/`). A number on a slide is checked against a named file that day. A measured finding, a position with evidence and a guess are labelled as three different things.

## Identity and credentials

- Identity is paused across the estate (28 October 2026): no pki.sgit.ai keys for now. A key is trusted only if it is published on a website or the operator hands over its QR code in the session.
- Vault keys are handed to a session out of band and never written into a file, a page, a commit or a message. Read keys may be published; write keys never.

## The estate's standard

This repository follows https://sgit.ai/docs/guidance/repositories.md (read it, and https://sgit.ai/llms.txt, before changing the shape of the site). `REALITY.md` lists what exists; a thing not in it does not exist.
