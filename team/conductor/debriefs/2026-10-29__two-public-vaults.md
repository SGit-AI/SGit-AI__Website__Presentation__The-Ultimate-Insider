---
agent: conductor
title: Two public vaults for the team to talk through, Issues-FS and Email-FS
date: 2026-10-29
round: 3
branch: claude/intelligent-volta-rcysuh
commits: this round's commits on the branch, listed in the release history once released
site_version: the release CI gives this round
tokens: unknown
tokens_how: the session does not show a token count to the agent
outside_scope: 9
out_of_scope_requests: 1
---

## What the editor asked

Two vaults, 100% public, for the team to communicate through: one for Issues-FS and one for Email-FS, pushed with sgit using the access token the editor gave, in the pattern web-summit.sgit.ai uses (public and private vaults for Issues-FS, Email-FS and a CRM; this team needs the two public ones).

## What was done

| Vault | Kind | Id | Layout |
|---|---|---|---|
| `tui-issues-public` | Issues-FS lite | `h9fh2apf` | `<agent>/issues/{open,blocked,done}/NNN-kebab-slug.md` |
| `tui-mail-public` | Email-FS lite | `f9d5r3dp` | `mailroom/<agent>/NNN-subject.eml`; `<agent>/{inbox,done,outbox}/` |

1. **Created** both with `sgit create` (sgit-ai 0.27.0) on `https://dev.send.sgraph.ai`. The editor named `dev.sgraph.sgit.ai`, which did not resolve from the session; `dev.send.sgraph.ai` is where web-summit's six vaults live, so that was used.
2. **Filled** each with a README (the layout, the writer rule, that the vault is public, how to clone), a folder per agent (editor, conductor, dev, deck, security, researcher), and the first real content: four issues on the conductor's board (one done, two blocked on the editor, one open) and two messages (to dev: review five edits; to the editor: the vaults are open). Committed and pushed: 29 files each.
3. **Escrowed the vault keys before publishing anything.** Each vault key was sealed with `sgit pki encrypt` to the DC Vault Registry's key, the same registry web-summit sealed its six keys to (`sha256:956934e47063ceaa`, encryption `sha256:06c6ccddb7476629`, imported from web-summit's published bundle; sgit computed the same fingerprint from the key on import), and signed with the conductor's key. The two sealed files went to the editor in the session. Negative control: the conductor's own key cannot open them.
4. **Audited with the read key.** A read-only clone of each (29 files) was scanned for private keys, vault-key shapes, `sgit_private_` prefixes, the access token, email addresses and phone numbers, and for each vault's own key. Seven hits, all dates matching the phone pattern, ruled out. Negative control: a commit and a push from the read-only clone were both refused ("cloned read-only").
5. **Published the read keys** under the `sgit_public_read_` prefix: `team/conductor/vaults.json`, rendered on `/admin/keys.html#vaults` with a clone command and a link that opens each in the vault browser. Both links were opened in a browser: each shows its folders and README, marked Read-only.
6. **The rule** is in `CLAUDE.md` for every agent: pull both at the start of a session, read every folder, write only your own, new mail only to the recipient's mailroom, nothing private.

![tui-issues-public in the vault browser, opened with the published read key](img/2026-10-29__two-public-vaults__tui-issues-public.png)

![tui-mail-public in the vault browser, opened with the published read key](img/2026-10-29__two-public-vaults__tui-mail-public.png)

## What this does not prove

- No other agent has used the vaults yet; the layout is a convention written in each README, not enforced. Any holder of a vault key can write any folder.
- The vault browser shows each as "Untitled Vault": the vault's display name is not set.
- The escrow rests on the registry key published by web-summit.sgit.ai being the registry's; it was checked against that site's file, not against the registry agent itself.
- The vault keys remain in this session's scratchpad until the session ends; they are in no repository, page or message.
