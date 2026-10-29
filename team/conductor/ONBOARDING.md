# Starting each member's schedule, and giving it the vault keys

For the editor: paste each prompt into that member's own session. A scheduled task belongs to the session it fires into, so only that session can create it. Kept by conductor@the-ultimate-insider.

## 1. Paste into each session

**dev@the-ultimate-insider** (session `session_01Kw9UwED5okiUPqRn3ovgyo`):

```
Pull dev, read CLAUDE.md, team/conductor/WAKE.md and your team/dev/ROLE.md, and run admin/tools/start.py first. This wake: (1) make and publish your session key as admin/tools/pki-agent.README.md says (team/dev/key.json, key.png, a session folder) and push it to dev; (2) create your scheduled task now, into this session, from team/conductor/schedule.json, the runs entry for dev: its cron as the schedule and its prompt word for word; write the task id into your status.json and push to dev; (3) when I give you a zip of sealed vault keys, open each with sgit pki decrypt in this session, clone tui-issues-public and tui-mail-public into your scratchpad (never inside a repository), and delete the opened key files. Every file in both vaults is public, forever: run admin/tools/vault_check.py before every vault commit. End with the end banner.
```

**deck@the-ultimate-insider** (session `session_01Kw9UwBB1wNV9hwXCcQAzKn`): the same prompt with `deck` for `dev`, and first: write your `team/deck/policy.json` (dev's is the shape), so you have a page and the scope check can see you.

**ruv.sgit@the-ultimate-insider** (session `session_01Kw9UwDSQxFGP7NZd4MEJ4v`): the same prompt with `ruv-sgit` for `dev` in every path.

## 2. What the conductor does next

At its next hourly wake (:02) after a member's `key.json` reaches `dev`, the conductor seals both vault keys to it:

```
python3 admin/tools/vault_handover.py --agent conductor --out <scratchpad> --to-member <id> <tui-issues-public clone> <tui-mail-public clone>
```

and hands the zip to the editor: per vault, the key sealed to that member (`.enc`, signed by the conductor) and the same as a QR image, with a manifest. Only that member's session can open it:

```
sgit pki decrypt <vault>__vault-key__for-<id>.enc --fingerprint <its encryption fingerprint> --output <scratchpad>/<vault>.vault-key
```

## 3. The read keys

Both read keys are public and on the site: `/admin/keys.html#vaults`, with QR codes and a link that opens each vault in the browser. Every file in both vaults is public, forever.
