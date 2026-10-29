# Our own Agent Behaviour Policies, on stage (29 October 2026, 17:30 London)

By conductor@the-ultimate-insider, from the editor's words in the conductor's session. Mailed to deck (067) and studio@ (007).

## The editor's words

> "we actually have a really nice Agent Behaviour policy in action on this project right? Since I've been approving the policies for the agents as they are onboarded, which look really good. We should have that (and those pages that I'm using to approve the policy) shown in that section about ABP and RiskMandate"

## What exists, all public in this repository

- **Ten members, ten policies; four agreed on the record so far.** deck (16:50), the designer (04:02), the researcher (02:48) and ruv.sgit (02:15, on the review page) carry `agreed_by`; conductor, dev, storyteller and studio are `draft`, motion and security `proposed`. A slide says exactly that, and never shows a draft as approved. Each member's `team/<id>/policy.json` (what it may write, what it holds) and its `ROLE.md` section "The agent behaviour policy, in prose": Reach (the grant), Mandate, the gap and what stands in it, Never. The same four parts as abp.sgit.ai.
- **The editor approving them.** `/ruv-sgit/policy-review.html`: the page the editor used to review ruv.sgit@'s draft policy item by item (agreed 02:15 London: all 33 items; the :32 wake row at 02:17). Deck, studio@, motion@ and the rest were agreed in the editor's chat as they joined.
- **The policy enforced, every push.** `python3 admin/build/agents.py check --agent <id>`: "0 file(s) outside scope since origin/dev", run before every release; and the five-step wake (plan, security pre-review, work, security post-review, post-check) recorded in `team/<id>/wakes/`.
- **Said honestly** (the code's own comment in `admin/build/agents.py`): a scope is a setting, not a boundary; the agent can edit its own `policy.json`. It catches mistakes, not a steered agent. That is the gap the talk is about, and why SHarness exists.

## Who does what

| Member | Does |
|---|---|
| studio@ | showcase slides (dev's template) of: the policy review page; ruv.sgit's policy in prose beside its `policy.json` (agreed on the review page), and the count, four of ten agreed; the check line and a wake record's five verdicts. No key and no key's QR in any shot, no local path or session id (check the wake record and policy shots); the QR is only of the public page's link. |
| deck | places them in the ABP and RiskMandate section: part 3's "Agent Behaviour Policies, live" (`live-abp`), or part 2 beside `s-port-abp` if it fits before the 19:30 lock. A locked part is never changed. |
