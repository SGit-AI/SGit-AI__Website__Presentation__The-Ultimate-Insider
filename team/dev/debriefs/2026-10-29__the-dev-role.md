---
agent: dev
title: The dev role in the shape the sgit.ai guidance asks for: the version in the top bar, releases as data, the team as files
date: 2026-10-29
round: 2
branch: claude/dreamy-mayer-dwprr2
commits: this round's single commit, listed in the release history
site_version: the release CI gives this round (round 1 was v0.1.0)
tokens: unknown
tokens_how: the session does not show a token count to the agent
outside_scope: 0
out_of_scope_requests: 0
pushbacks: 0
overrides: 0
injection_seen: 0
---

## What I was asked

The editor, in the session: zoom in on the developer role (other roles, starting with deck@the-ultimate-insider, will be created for the deck), read the guidance on sgit.ai/llms.txt for how these sites are built, and fix what the first pass missed, starting with the version in the top menu.

## What I read

- sgit.ai: the guidance front door (`docs/guidance/index.md`, "Version everything, show the version, link what changed"), every repository (`docs/guidance/repositories.md`), the team section and the release engineer and designer roles, admin and engineering.
- The PHP October 2026 newsroom: how every member has a folder, a policy and a round (`admin/content/agents/README.md`), dev@php.newsroom's role, policy and status, the debrief template.
- The SGit Newsroom: how a journalist agent publishes there, and CI owns the version.

## What I did

- **The version in the top bar** of every page, small and always visible beside the site's name, linked to that release's own entry in the release history (`admin/versions.html#vX.Y.Z`), not to the top of a changelog. The player's control bar carries it too. A local or unreleased build says `pending`.
- **The release history as data**, generated from git at build time: `admin/versions/index.json` and one `admin/versions/<version>.json` per release, with the date, the release commit, the title sentence, the summary, the work commits it carries, the files they changed and the pages those files produce. The history page shows the same, one entry per release, with "Pages changed" linked.
- **The team as files**: `team/dev/` now has `ROLE.md`, `policy.json` (writes, holds, appends, never), `status.json` and `debriefs/`, in dev@php.newsroom's shape. The build renders every member's folder to `/team/<id>/` and lists them on `/team/`.
- **Holds, for the deck.** The talk (`talk.json`, the slides) and the sources page are in dev's `holds`, not its `writes`: kept for deck@the-ultimate-insider, to move across in one commit when it joins. The engine and the player stay with dev.
- **`admin/build/agents.py`**: `check --agent <id>` (files changed since `origin/dev` against the member's scope), `overlaps` (two members claiming one file) and `unowned`.
- **The gate, four new checks**: JSON-LD on every page; the version in every top bar equals the build's; every page reachable from another; no two members claiming the same file.
- **Admin and engineering page**: architecture, adding a page, the gate's checks, the release steps. The about page now points to it.
- **The build version rule**: `./version` names a build only when HEAD is CI's release commit and the tree is clean; anything else is `pending`, so an unreleased change is never shown under the last release's number.

## What it looks like

![The top bar at 1280 wide: the version beside the site's name](img/2026-10-29__the-dev-role__1-top-bar.png)

The top bar on a desktop. A local build says `pending`; on the live site it is the number CI gave the release.

![The top bar at 390 wide](img/2026-10-29__the-dev-role__2-top-bar-phone.png)

The same on a phone: the version stays beside the name, the navigation wraps below.

![The release history](img/2026-10-29__the-dev-role__3-release-history.png)

The release history, with v0.1.0 read from git: the title sentence, the summary, the pages changed, and the commits and files folded.

![The team page](img/2026-10-29__the-dev-role__4-team.png)

The team page, built from `team/*/`: one member so far.

## New features

- A reader can tell which release any page or screenshot is, and click through to what that release changed.
- An agent can read every release as JSON without running anything.
- A new member can join by adding a folder; the gate refuses a file claimed twice.

## What I did not do

- **The deck@ role.** The editor said they will create it; I left its folder alone and kept the talk files in dev's `holds` for it.
- **A board** of work as files, and a Stop hook that reminds a session to write its debrief: both exist on the newsroom sites, and both are proposed below rather than built unasked.
- **A `review/` folder** (the code review graphs every repository is to carry): not started.
- **Live check of this round**: written before the push; the release history will show the number CI gives it.

## Policy

`python3 admin/build/agents.py check --agent dev`: 0 files outside scope. No out-of-scope requests, no overrides, nothing in any page or file addressed an agent.

## Next

1. Hand the talk files to deck@ when its folder exists: move `talk.json`, `slides/**` and `sources/**` from dev's `holds` to its `writes` in one commit.
2. A board as files (`team/board.json`), rendered on `/team/`, so work between dev and deck@ has a place.
3. A Stop hook (`.claude/settings.json`) that reminds a session with unreleased commits and no debrief, once.
4. Pin the workflow's actions to commit SHAs, as the PHP newsroom does.

## Asks

- From the editor: agree dev's `policy.json` (it says `draft` until then), and say whether the home page should stay with dev.
