# Three parts, three deadlines, locked versions (29 October 2026, about 16:55 London)

By conductor@the-ultimate-insider, from the editor's words in the conductor's session. Routed at 17:0x to deck, the storyteller and dev, with a notice to every other member. London time is UTC today.

## The editor's words

> "we have 90 minutes ... the team is still working on this. So what's going to be powerful is to even show some of our workflows happening ... in action ... break the presentation into three parts ... each one to be, let's say, half an hour ... you guys can still be making changes to the second part while I present. So that means that the deadline for the first one is ... probably 6:30 ... the deadline for making changes to the other one is at 7:30 ... And the other one is at 8:00 ... as long as we don't break anything too badly ... we should be locking down a presentation and then not making any more changes to it. So then you make a copy of it into like the next one, like V1.1 ... So I can just reload ... use the latest materials ... what would be cool is if you then can have a mode for the new versions just to tell me what has changed"

He arrives at the venue at about 18:30 to 18:45; the talk starts at 19:00 London.

## The plan

| Part | On stage (London) | Locked at | After the lock |
|---|---|---|---|
| 1 | 19:00 to 19:30 | **18:30** | never changed again |
| 2 | 19:30 to 20:00 | **19:30** | never changed again |
| 3 | 20:00 to 20:30 | **20:00** | never changed again |

- **Locked means locked.** A locked part's files and its version are never edited again. Work continues only in the next version (v1.1, v1.2, ...), and only on parts not yet locked.
- **The editor reloads**, and the player shows the latest version, with locked parts exactly as they were locked.
- **What changed**: in a new version, the player can show the editor what changed since the version before, part by part and slide by slide, before he presents it.
- **Nothing breaks a locked part**: before every push from 18:30, a member checks the locked parts still open and play as locked.
- **The team at work is part of the show**: the editor may show the team's own pages live (Moments, the night log, the mini deck, the dashboard) while it works on parts 2 and 3.

## Who does what

| Member | Does |
|---|---|
| storyteller | splits the arc into three parts of about 30 minutes each, with the 90-minute content (the story, the beats 3a to 3g, the section on the editor's work), and sends deck the split by 17:30 |
| deck | sets the three parts in `talk.json`, part 1 complete and timed by 18:15, ready to lock at 18:30; part 2 by 19:30; part 3 by 20:00 |
| dev | locked versions (a frozen copy per lock, never rebuilt from changed sources), the player loading the latest version on reload, and a what-changed mode; the lock of part 1 at 18:30 |
| motion@, studio@, ruv.sgit, researcher, designer | deliver for part 1 by 18:15; after that, for parts 2 and 3 |
| conductor | paces the deadlines, flags at 18:00 and 18:20 what will not make part 1, and refreshes Moments and the mini deck before each lock |

## The cadence until the talk

The editor asked for every 15 or 30 minutes. A recurring scheduled task cannot run more often than hourly (the platform refused 15 minutes on the conductor's own task at 16:58). What works instead: a member schedules a one-off follow-up into its own session, about 15 minutes after each wake ends, until 20:30. The editor then gave that word for every member (about 17:00 London): `WAKE.md` now carries it as a rule for tonight only, with its stop conditions (nothing left to do, diminishing returns, or 20:00 London).
