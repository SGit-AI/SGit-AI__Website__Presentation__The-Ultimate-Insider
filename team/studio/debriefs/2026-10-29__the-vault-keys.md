---
agent: studio
title: The vault keys: opened, both vaults cloned, studio's board and mail folders live
date: 2026-10-29
round: 3
branch: claude/studio-onboarding-setup-8jfp3n
commits: listed in the release history
site_version: the release CI gives this wake
tokens: unknown for the member; the review sub-agents' usage is in the wake record's comments
tokens_how: the session does not show its own token count
outside_scope: 0
out_of_scope_requests: 0
---

## What started it

The editor uploaded the conductor's zip of vault keys sealed to studio's key (made 15:46 UTC, signed with the conductor's `sha256:9568700877d11832`), in this session. Wake record: `team/studio/wakes/20261029T162902Z.json`.

## What was done

- **Opened the keys** with sgit-ai 0.27.0 (the team's pinned version, installed in the container): `sgit pki decrypt` with studio's encryption fingerprint `sha256:cc6cd6e2e5425109`, an empty passphrase on stdin (the session key is stored plain, as pki-agent makes it), each into a 0600 file in the scratchpad. Neither key was printed or written into the repository or a vault.
- **Cloned both vaults** into the scratchpad, the key read from stdin (`sgit clone -`); then the opened key files shredded and the unpacked zip removed. This was done at the upload, before the wake record opened; the plan says so.
- **The mailroom:** one message, dev's reply on the engine's iPad fit; no answer needed (the line was out of the ports at 16:14). Moved to `studio/done/`.
- **The board** in `tui-issues-public`: `studio/` with two done issues (001 the first ports, 002 the journey) and one blocked (003 the next port, on deck's sorting). Mail folders `studio/{inbox,done,outbox}`.
- `vault_check.py` clean on both before the commit; pushed with the environment's `SG_SEND_ACCESS_TOKEN` passed from the variable, never printed (the logs checked for it and deleted). A clone from each published read key shows the new files.
- deck's sorting has not landed (deck's board, 15:17 wake), so no new port.

## Screenshots

None: no page changed in this wake.

## Open

- deck's sorting decides the next port (board 003).
- The editor agrees `policy.json` (a draft).
