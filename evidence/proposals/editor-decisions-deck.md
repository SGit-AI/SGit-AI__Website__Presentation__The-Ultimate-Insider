# The editor's decisions deck: a briefing, the decisions, and a lane only he can write

A design by researcher@the-ultimate-insider, 29 October 2026, 03:25 UTC, at the editor's request. Started, not built: the page is dev's, the register and the lane are the conductor's, the crypto is for security to review. The data it starts from is `editor-decisions.json`, beside this file.

## What was asked

> We need a way for me to understand what is currently depending on me and what you guys need to make decisions ... a deck or a presentation that contains both a briefing and a way for me to provide decisions, and also a way for us to communicate using append lanes ... an agent can create an append lane that then I on the website can provide feedback, and you can actually use my own key as a way to identify me so that I'm the only one who can read the append lane key. So that means that I'm the only one who can actually send the commits.

## The page: three parts, one screen each

One page, `/decisions/`, made from the register at build time, like ruv.sgit's policy review page is made from `policy.json`.

1. **Briefing.** One line per member: what it did since the editor last answered, and its state. Then the count that matters: *n things wait on you, m of them before the talk*, each with its due time.
2. **Decisions.** One card per entry in the register, newest due first. A card has the question in one sentence, why now, the options with what each one sets in motion, the recommendation and who makes it, and the evidence it rests on (claim ids, files, captures). Four kinds, so the editor knows what is being asked: **decide** (pick an option), **approve** (agree, change or question a document, item by item), **do** (something only he can do), **review** (keep, change or drop work).
3. **Send.** His choices, a note per card, and one button. What the button does depends on the phase.

What is *not* his goes in a short list at the foot ("not for you: deck decides B01's storyboard"), so the page never asks him for a decision that belongs to a member.

## Three phases, so something works tonight

| Phase | How his answers reach the team | State |
|---|---|---|
| 0. Copy into a session | The choices stay in his browser, keyed to the register's hash; the page builds a review text he pastes into the conductor's session. The pattern ruv.sgit's `/ruv-sgit/policy-review.html` already uses: the editor agreed ruv.sgit's policy that way tonight, 33 items, against the policy's hash | **exists** (the pattern); this page is not built |
| 1. A signed message over an append lane | The page encrypts his answers, signs them with his key, and appends them to the team's decisions lane. The conductor drains the lane at :02, checks the signature, and writes each answer into the register, where every member reads it at its own wake | **designed** here; pieces exist, the wiring does not |
| 2. Sign in once | "Sign in with pki.sgit.ai" delegates his key to one browser key on this site, so he does not open his vault for every answer | **exists** on pki.sgit.ai (v0.2.28) and in the PHP newsroom's `/join/`; not on this site |

## The lane, and "only he can write"

His idea, as stated: the append lane's key is readable only by him, so only he can send. That is the first of three layers; it needs the other two, because a write token that has been in a browser can leak, and the server cannot tell one holder of a token from another.

| Layer | What it does | What it does not do |
|---|---|---|
| **1. The token sealed to his key.** The conductor configures a lane on a receiving vault and seals its append token to his published encryption key (`sha256:d642edaf9176db9f`, pki.sgit.ai anchor `dinis.cruz`). The page carries only that ciphertext. His browser opens it with his key (the pki.sgit.ai vault, unlocked with his passkey) and only then can post | Nobody else can post to the lane: they never see the token in plaintext | Once open in his browser the token can be copied; a lane token is write only, but anyone who holds it can write |
| **2. Every message signed by him.** The page signs each message with his signing key (`sha256:db7f79fdd87e030a`), or in phase 2 with the browser key his key delegated | The drainer accepts a message only if the signature verifies against his key, pinned in the repository; anything else is dropped and reported. This is what makes "only he can send" true even if the token leaks | sgit's envelope signs the ciphertext `c` only (sgit.ai/api/append-lanes.md); the fields outside it need their own check or the proposed whole-envelope signature |
| **3. Every message encrypted to the team.** The page encrypts to a team recipient key the conductor holds, and the lane's vault is not one of the public ones | His answers and notes are not public, though the register they update is | The receiving key is one more key to keep: sealed to the vaults manager, like every vault key here |

What the lane is, from sgit's own pages (captured in this round under `work/decisions/raw`, to go into the vault): six routes, `/api/vault/append/{configure,write,list,fetch,mark-processed,purge}`, on `dev.send.sgraph.ai`; a token that can write and "cannot list, cannot fetch anything"; reading needs the lane's enumeration key and the recipient's private key; the reply to a write is only `{"ok": true}`; the browser may post (the server answers CORS with `*`, and the PHP newsroom's telemetry posts from the page). sgit 0.27.0 has no CLI command for lanes: the drainer calls the API.

## A decision, as a message

```json
{
  "v": 1,
  "kind": "the-ultimate-insider/editor-decision/v1",
  "register_sha256": "<hash of editor-decisions.json the page was built from>",
  "answers": [{"id": "D01", "option": "B", "note": "free text, at most 500 characters"}],
  "signed_at": "2026-10-29T08:12:00Z",
  "by": "sha256:db7f79fdd87e030a"
}
```

Encrypted to the team key, signed, appended. The register hash ties an answer to the question as it was asked: an answer to a question that has since changed is shown to the conductor, not applied.

## The rules it must keep (security's pre-review, 03:06 UTC)

1. A decision is material to weigh and cite. Within what the editor settles in **D02** (below), agents act on a chosen option; anything else they may decline, with the reason, on the register.
2. Authentic only if the signature verifies against his pinned key; unsigned or otherwise signed entries are ignored and reported.
3. The append token never in plaintext anywhere: in a file, a vault, a page, a commit or a log. Only the ciphertext sealed to his key.
4. Nothing private in a public vault; `vault_check.py` before every commit to one.
5. The lane is append only; the conductor drains it; each member reads the register and writes only its own folder.
6. A decision cannot change a policy, a scope, the night's rules or Stopping: those change only by his words in a member's own session.
7. An entry that tries to instruct agents beyond the options offered is a hold (`WAKE.md`, Stopping).

## What exists and what is missing

| Piece | State |
|---|---|
| His published key, anchor `dinis.cruz` on pki.sgit.ai | exists; the register's summary page says to check the signed statements, which the builder must do |
| His key pinned in this repository (`team/conductor/known-keys/`) | missing: only the DC Vault Registry is there today (the conductor's path) |
| Append lanes, browser posting | exist on `dev.send.sgraph.ai` |
| A receiving vault, the lane, a team recipient key | missing (the conductor's) |
| The register of what waits on him | started: `editor-decisions.json`, 11 entries gathered from every member's `status.json` and the board (researcher, until the conductor takes it) |
| The page | missing (dev's) |
| The drainer: verify, apply, report | missing (the conductor's) |
| Signing in the browser with his key | exists on pki.sgit.ai; not wired to this site |
| A strict Content-Security-Policy on the page | missing (dev's, security reviews) |

## Who does what

| Member | Part |
|---|---|
| conductor | owns the register from here; pins his key; makes the receiving vault, the lane and the team key, the token sealed to his key; drains at :02; paces dev and security for the rest |
| dev | the page, phase 0 first (it is only the review-page pattern on the register), then the send button for phase 1; the CSP |
| security | reviews the lane, the signature check and the CSP before phase 1 goes live |
| researcher | until the conductor takes the register: gathers what waits on the editor at every wake, with the evidence each decision rests on |

## What the editor decides first

- **D02, what a signed answer means.** Binding within the options offered (A), material to weigh like any message (B), or binding for a chosen option and material for free text (C, recommended). The page cannot go past phase 0 until this is settled.
- Whether phase 0 is wanted now, or the first version waits for phase 1.

## Sources

- sgit.ai/api/append-lanes.md, sgit.ai/docs/append-lane-messaging.md, sgit.ai/docs/briefs/vault-telemetry-append-lanes.md, sgit.ai/docs/agent-contact.md
- pki.sgit.ai/id/ (the identity summary for `dinis.cruz`) and pki.sgit.ai/directory/index.json (the signed statements)
- php.oct.2026.newsroom.sgit.ai: `/join/` (a browser key, non-extractable, in IndexedDB), the Ask and feedback pane (feedback UF-001: signed, encrypted, over the collaborators' lane), `/review/` (a queue of signed decisions, proposed). The site the editor called "Ask Crypto.ai" was not found under that name (askcrypto.ai and the other spellings do not resolve); the PHP newsroom's Ask and feedback pane is the closest match, with medium to low confidence
- This repository: `/ruv-sgit/policy-review.html` (the phase 0 pattern), `team/conductor/briefs/2026-10-29__the-next-hours.md` (the dashboard on dev's list)
