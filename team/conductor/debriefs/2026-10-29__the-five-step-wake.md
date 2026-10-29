---
agent: conductor
title: The five-step wake, built and run on itself
date: 2026-10-29
round: 8
branch: claude/intelligent-volta-rcysuh
commits: 8c66751 (wake.py and the open record), 5700bab (the work), and the record's close
site_version: the release CI gives this round
tokens: unknown
tokens_how: the session does not show a token count to the agent
outside_scope: 1
out_of_scope_requests: 1
---

## What the editor asked

Every wake runs five steps: the conductor plans, security reviews the plan, the member works only if both agree, security reviews again, the conductor checks it went to plan; each with a comment and a view. Defence in depth in one session, above all so one member's issue does not become another member's. And: where do deck and ruv.sgit find their onboarding?

## What was done

The five steps are built (`admin/tools/wake.py`, the briefs in `team/conductor/reviews/`, the section in `WAKE.md`, a line in `CLAUDE.md`, `start.py` opening the record), and this wake ran through them. Its record is `team/conductor/wakes/20261029T021416Z.json`:

| Step | By | Verdict | What it said |
|---|---|---|---|
| plan | conductor sub-agent (Sonnet) | go | three items; it missed the editor's main ask, the five-step machinery, which the member added and marked as an amendment |
| pre-review | security sub-agent (Sonnet) | change, then go | five conditions (onboarding stays in the conductor's folder, only a read key and only after an audit, nothing written in researcher's files, the check in admin/tools for new records only, the CLAUDE.md edit named); the plan was amended to adopt all five and passed |
| work | conductor | partial | everything planned, except tui-evidence-public's read key: the vault is not on the server yet, so it could not be audited (condition kept) |
| post-review | security sub-agent (Sonnet) | finding | clean, except that the commit message did not name the CLAUDE.md edit as outside scope |
| post-check | conductor sub-agent (Sonnet) | partial | items 0, 1, 3 done; 2 not done for want of the vault on the server; every condition kept; nothing unplanned |

The gate held twice in practice: `wake.py gate` refused the work before the second `go`, and the `change` sent the plan back.

**Onboarding** is on the site at `/admin/docs/onboarding.html` (dev renders the conductor's `ONBOARDING.md` there), linked now from `WAKE.md` and the conductor's role; deck and ruv.sgit have a request each in the mail vault.

## Outside scope, named

`CLAUDE.md`: one line, the five-step rule, at the editor's word. The post-review found it was not named in the commit message; it is named here and in the conductor's status.

## What this does not prove

The reviewers share the session's reach: a second reading, not a second identity. No other member has run a five-step wake yet, and the gate does not run `wake.py check` until dev wires it in.
