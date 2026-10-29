# The four review briefs of the five-step wake

Every wake runs five steps (`team/conductor/WAKE.md`, "The five steps"); four of them are sub-agents started by the member with these briefs, each on a smaller model (Sonnet), read only, a few minutes each. Fill `<you>`, `<record>` (the wake record `start.py` opened) and the context in angle brackets; never paste a key, a token or a raw message into a brief.

| Step | Brief | Sees | Verdicts |
|---|---|---|---|
| 1 plan | `plan.md` | the member's mail, board, requests, role and status | `go`, `stop` |
| 2 pre-review | `pre_review.md` | the plan, the member's policy, the rules: never the raw messages | `go`, `change`, `stop` |
| 4 post-review | `post_review.md` | the diff and the vault changes, the gate, the rules | `clean`, `finding`, `stop` |
| 5 post-check | `post_check.md` | the plan and the diff | `as-planned`, `partial`, `off-plan`, `stop` |

Each reply is two lines, `VERDICT:` and `COMMENT:`, recorded with `wake.py step`. A `change` sends the plan back: amend it, keep the first verdict under `history` in the record, and run the pre-review again. A `stop` writes the member's `HOLD.md` (`wake.py` does it) and stops every member's wake until the editor lifts it.

It is defence in depth inside one session, not a second identity: the reviewers have the same reach as the member. What they add is a second reading before and after, and the question the editor asked for above all: does this wake turn one member's problem into another member's?
