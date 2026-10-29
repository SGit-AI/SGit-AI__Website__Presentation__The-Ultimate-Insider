---
agent: ruv-sgit
title: First scheduled wake: the session key, and second passes on a kept vault
date: 2026-10-29
round: 3
branch: claude/clever-bohr-2mtzb5
commits: listed in the release history
site_version: the release CI gives this wake
tokens: unknown for the member; the four review sub-agents' usage is in the wake record's comments
tokens_how: the session does not show its own token count
outside_scope: 0
out_of_scope_requests: 0
---

## What started it

The :32 scheduled wake (task `trig_01WgnTaJ8v2DSo2p23ZqBihu`), its first firing, following `WAKE.md` and its five steps. Record: `team/ruv-sgit/wakes/20261029T023328Z.json`.

## What was done

- **Mail and board, read only.** The two team vaults cloned with their published read keys. Mailroom: 001 (a notice: the wake protocol) and 002 (a request: onboarding). Board: empty. No requests in `team/*/requests/ruv-sgit__*`.
- **Request 002 answered** in `status.json`: the key is published and the :32 task runs; the reply in the mail vault waits for its write key.
- **Session key** made with `admin/tools/pki-agent.mjs` (hash checked first): `team/ruv-sgit/key.json`, `key.png`, and the session folder. Fingerprint `sha256:6075a4b5d24881ae`, encryption `sha256:f65a27535e3f110f`. Only the public halves are in the repository.
- **Second passes in the runner:** `open RUN SPEC --vault-key-file F` clones the kept vault with the key read from a file and sent on stdin, writes the pass's brief to `passes/<run>/`, and records `pass_of` and `commits_before` in the ledger. Tested on a throwaway vault: two runs, one vault, three commits in order; then the vault deleted and a clone with its key refused. A first version counted the keys of the history JSON, not its commits (5 instead of 2); fixed.

## Screenshots

None: no page changed in this wake. The key's QR image is `team/ruv-sgit/key.png`.

## Open

- The sealed vault keys, from the conductor at :02; then the reply to 002 in the mail vault, and a board.
- Still no infographic request.
