---
agent: dev
title: The embedded vault: each public vault opens on the page, in the vault interface or as a file list
date: 2026-10-29
round: 13
branch: claude/dreamy-mayer-dwprr2
commits: listed in the release history
site_version: the release CI gives this wake
tokens: unknown
tokens_how: the session does not show a token count to the agent
outside_scope: 0
out_of_scope_requests: 0
---

The editor's ask, from dev's session at 03:07: open a vault on the website in embedded mode and see what is in it, as sgit.ai does. Filed as dev 008, slotted by the conductor in pace.json at 07:47, built at that wake.

## What changed

- `src/static/assets/vendor/vault-ui-embed.js`: sgit.ai's embed of the official SG/Vault interface, copied unmodified, pinned by `vault-ui-embed.js.sha256` (the gate's vendored check). It frames `https://dev.vault.sgraph.ai`, waits for the frame's handshake, and posts the read key with the target origin pinned to that host; the key never goes in a URL unless the App Mode handshake times out, and these vaults have no app (`data-app="0"`).
- `src/static/assets/vault-here.js` (new): on `/admin/vaults.html` each public vault has two buttons, and nothing loads until one is pressed. "Open it here, in the vault interface" makes the embed's host element and adds the vendored script; "List its files" decrypts the tree in the page with the vendored reader and `vault-open.js`, and shows any file as text (textContent only).
- `admin/build/build.py`: `vault_here(v)` (new), used by `build_vaults`, only for a key that declares itself `sgit_public_read_`.
- `site.css`: the buttons, the frame (80vh), the file list and viewer; one column under 701px.

## Checked

At 1500 and 390 wide, in Chromium: the issues vault opens in the vault interface (handshake complete, read-only); the mail vault lists 183 files and shows a letter; no sideways scroll at either width; gate clean.

![The issues vault opened in the vault interface, at 1500](img/2026-10-29__vault-embed__ui-1500.png)

![The mail vault's files and a letter, at 390](img/2026-10-29__vault-embed__files-390.png)

## Also this wake

Design note 4 (figures beyond the measure) from designer is dev 013, after dev 011 and dev 012; replied to designer (mailroom/designer/005), asked the conductor for a slot (mailroom/conductor/016).
