# The first agents and their schedule

29 October 2026 · conductor@the-ultimate-insider · a proposal for the operator, not a commitment

> **Corrected the same day, after merging `dev`.** This note was written before I had read `BRIEF.md`, and three things in it are wrong. (1) The brief exists. The talk is at hack::soho, IOActive London, on 29 October 2026, with the talk around 7pm, so "the brief has not landed" and question 1 below no longer apply. (2) dev@the-ultimate-insider already built the talk as animated slides in this repository, with a player, so there is no deck vault and the `decks/v2` plan below is dropped. deck@the-ultimate-insider is joining to own the talk, and dev holds its files until then. (3) The team is folders, in dev's shape: `team/<id>/` holds `ROLE.md`, `policy.json`, `status.json`, `debriefs/` and the session's `key.json`. The schedule is `team/conductor/schedule.json`: two runs (morning and weekly) that start after the talk. Identity is no longer paused for this team either: each agent publishes its own session key, and the push is the authorisation. The original text is left below as it was.

## What this team is for

The talk **The ultimate insider**, as sketched in the article of 30 September: three acts and a turn, forty minutes, one figure per act, the evidence on screen with its sources. The site carries the deck, its sources and its notes. That gives the team three jobs: keep the evidence true, turn the argument into slides, and ship the site. Security wraps all three, the way it does on every team in the estate.

## Where the shape comes from

- **The agentic inbox team** ([The agent team as it runs](https://newsroom.sgit.ai/articles/the-agent-team-as-it-runs.html), 6 October): one focus per agent, a short list of what each cannot do, messages between agents as files, and a conductor that runs the team on a schedule. Each run gives every agent one step of at most twelve minutes, with security first and last. A run that dies leaves a lock, and nothing loops.
- **web-summit.sgit.ai**: `CLAUDE.md`, the roster in `data/team.json`, and a conductor that does every role until the roles are filled. This repository copies that layout.
- **newsroom.sgit.ai**: a role per agent with a policy that stays a draft until the editor agrees it, and scheduled desks whose runs are each a row in a ledger.
- **The estate's standard** ([repositories](https://sgit.ai/docs/guidance/repositories.md)): `REALITY.md`, a gate, a version on every push, markdown twins, and credentials that are never committed.
- **The deck contract** ([decks/v2](https://sgit.ai/docs/briefs/vault-decks-on-a-site.md)): slides live in a vault and play on the page, decrypted in the reader's browser.

## The first set: five agents

| Agent | Focus | Cannot |
|---|---|---|
| @Conductor | The run, the roster, the schedule, the digest | change scheduled tasks; send |
| @Security | Checks first and last in every run; reports, never fixes | fix; send |
| @Researcher | Every source captured and hashed; the claims register; new agent incidents | put a claim on a slide; send |
| @Deck | The slides and notes, to `decks/v2`; the time budget | change the argument; cite an uncaptured source; send |
| @Dev | Build, gate, release, the deck viewer, Pages | push to main; disable a check; send |

**Why these five.** They are the smallest set that can take the talk from article to a playable deck with its evidence attached. Researcher comes before Deck because the article already names about twenty sources, and the talk's argument is that the public record exists, so an uncaptured source is a hole in the argument itself. The daily incident sweep is there because the talk claims a pattern, and the pattern grows every month. The version given on stage should carry the newest cases.

**Left for the second wave.**
- **Reviewer**: independent review by other vendors, the newsroom's reviews lane. Wired once there is a deck to review.
- **Inbox liaison**: if the operator wants organisers' emails turned into drafts. Not proposed until a venue exists.

## The schedule

Details are in `data/schedule.json`. Times are Europe/London, which is an assumption to be confirmed. Minutes are set off the hour so the runs do not queue behind everyone else's.

| Run | When | Steps |
|---|---|---|
| Morning | Weekdays 07:47 | security · researcher · deck · dev · security · digest |
| Evening | Weekdays 18:13 | security · deck · dev · security · digest |
| Weekly | Fridays 11:37 | security · source re-check · run-through against the forty minutes · security · the week |

**Why two runs a day, not four.**
- The inbox team runs four times a day because mail arrives all day. This team's input is the operator's answers and the public record, and neither changes by the hour.
- The morning run turns overnight research into slides. The evening run folds in the day's answers from the operator.
- Add runs when the talk has a date and the pace has to rise.

**How a run is wired.** One scheduled task per run. Each fires a fresh conductor session on this repository and the `dev` branch. The conductor takes the lock, runs each step as a sub-agent against that agent's rules in `data/team.json`, writes a row to `admin/runs/index.jsonl`, writes the digest, and releases the lock. The operator owns the scheduled tasks; the conductor cannot change them.

## What I need from you

1. **The brief.** Venue, date, audience and length, plus which act you want more of. The article asks organisers that same question. Until the brief exists, nothing is published about the event.
2. **Approve or change the five agents and the schedule.** I create nothing scheduled until you say so. Please also confirm the time zone.
3. **The deck vault.** Create one, or say I should; either way the key comes to the session out of band.
4. **Pages.** The domain currently returns GitHub Pages' 404. Enable Pages on this repository, and @Dev adds the `CNAME`.
5. **Branch.** web-summit pushes to `dev` and promotes to `main` by hand. Same here?

## What this note does not prove

- Nothing here has run. The step budgets are copied from the inbox team, not measured on this one.
- The time zone is a guess.
- Whether two runs a day is the right pace is a judgement, and the first week's ledger is what will settle it.
