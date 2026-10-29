---
agent: conductor
title: Every member opens and closes its session with a banner, and the conductor's key is published in dev's team shape
date: 2026-10-29
round: 2
branch: claude/intelligent-volta-rcysuh
commits: this round's commits on the branch, listed in the release history once released
site_version: the release CI gives this round
tokens: unknown
tokens_how: the session does not show a token count to the agent
outside_scope: 9
out_of_scope_requests: 1
---

## What the editor asked

Use the PHP newsroom's start and end banners on this team ("exactly, and all agents should have it"), after asking for the team's pages in the admin section and for each agent's public key to be published on the site.

## What was done

1. **The banners.** `admin/tools/banner.py` prints the PHP newsroom's shapes: a double frame and `>>>` to start, with an OBJECTIVE row; a solid block and `<<<` to end, with ACHIEVED and NEXT; a rounded BLOCKERS box and a heavy FOR YOU box. Inner width 68. A field that does not fit starts its own row and is never cut (the first version cut "1 found, 1 fixed" to "1 found, 1").
2. **For every agent.** The rule is in `CLAUDE.md` and in every `ROLE.md`: conductor, dev, security and researcher. A new gate check, `banners`, fails any `team/<id>/ROLE.md` that does not name the tool. Negative control: a test role without the line failed the gate with one finding; removed, the gate was clean.
3. **The team in dev's shape.** Dev released the team as files (v0.1.1) while this branch had its own team pages. The merge kept dev's: the conductor's key moved to `team/conductor/key.json` with `key.png` and its session folder, the schedule to `team/conductor/schedule.json`, the roster file was dropped (the folders are the roster), and the conductor, security and researcher got `policy.json` (security and researcher marked proposed).
4. **Keys on the site.** Each member's page has a key section (QR image, fingerprints, session, sessions that held the role, a link to seal a secret to it); `/admin/keys.html` and `admin/keys/index.json` list every current key. Dev, security and researcher show "no key published yet".

![The team page: four members, the conductor's key on its card](img/2026-10-29__banners-and-keys__1-team.png)

![The conductor's page: its key, QR image and session](img/2026-10-29__banners-and-keys__2-conductor-key.png)

![The key register in admin](img/2026-10-29__banners-and-keys__3-key-register.png)

![The key section at 390 wide: the session id scrolls in its table](img/2026-10-29__banners-and-keys__4-key-phone.png)

## Outside scope, named

`agents.py check --agent conductor` lists 9 files. Five are dev's and were edited at the editor's word: `CLAUDE.md` (the banner and key rules), `REALITY.md` (the conductor's section), `admin/build/build.py` (the key section, the key register, and a fix so the release history does not link a team folder that is not a member), `admin/build/validate.py` (the banners check), `team/dev/ROLE.md` (the banner step and rule). Four are the proposed roles' drafts (`team/security/`, `team/researcher/`), written by the conductor until each role is agreed and held. Dev is asked to review its five in the conductor's `status.json`.

## What this does not prove

- No other agent has run a session with the banners yet; the rule is written and checked, not yet observed in use.
- The gate checks that each role names the tool, not that a session printed the banners.
- The key tool is pinned and its hash matched pki.sgit.ai, but nobody has read it line by line.
