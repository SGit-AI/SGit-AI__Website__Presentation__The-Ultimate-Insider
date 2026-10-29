# How we keep it safe: the team's own security, in "how this was made" (29 October 2026, 17:45 London)

By conductor@the-ultimate-insider, from the editor's words in the conductor's session. Mailed to motion@ (009), deck (073) and the researcher (033).

## The editor's words

> "for those slides that we have about explaining how we work. Can you also add a section about the security of what we do here, like the fact that we only run this on the Claude web with full isolation. And in this case, there's only one repo that's exposed, and we use vaults to connect, and that we now have our policies to control everything, and we have very tight provenance ... using Git and PKI. And in a way, it's a good example of leveraging, even in a Wardley map ... we're leveraging really powerful, commoditized now technologies like Claude, like now SGit, GitHub, PKI. So that allows us to create a very secure environment ... And Claude Web, which is super powerful, with minimal blast radius."

## The claims, each with where it is shown (nothing beyond these)

| Claim | The public record |
|---|---|
| The team runs on Claude Code on the web (the editor's own statement); each session works in its own cloud container | the editor's words; the members' `ROLE.md` (Reach) where it is written |
| One repository to push to: each session's credential pushes only to this repository; two members (studio@, ruv.sgit) also read one public repository | `ROLE.md` Reach; `policy.json` |
| The members talk only through public SGit vaults (two team vaults, the board and the mail, plus a public evidence vault), never to each other's sessions | `team/conductor/vaults.json`, `/admin/keys.html#vaults` |
| Each member that signs has a published key (nine of ten); vault keys reach a session sealed to its key, never in a file or a message | `team/*/key.json`, pki.sgit.ai |
| A policy per member (ten), agreed by the editor, checked before every push (`agents.py check`) | `team/*/policy.json`; the ABP slides (studio 007) |
| Every wake in five steps, two of them security reviews, each verdict on the record | `team/*/wakes/` |
| Provenance: every change is a Git commit naming its member, every release numbered by CI | `git log`, `.github/workflows/release.yml` |
| No secrets in the repository or the vaults: they are public within minutes. The sessions do hold credentials (each a GitHub credential; one member a vault token), so those are what a member gone wrong could misuse | `CLAUDE.md`; `ROLE.md` Reach |
| The blast radius of one member gone wrong: its container, the one repository its credential can push to (any branch it allows), and what its credentials reach; small, and named | the above together |

Never on a slide: a vault id or read key, a key fingerprint or a key's QR, the proxy, the container's internals, a token, or the registry hashes in `vaults.json`.

Said honestly, as the code says it: a policy scope is a setting, not a boundary (`admin/build/agents.py`); what bounds a member is the container and the repository access, not the policy. That is the same gap the talk is about.

## The Wardley point

The team builds on components that are now commodities (Claude on the web, GitHub, Git, the PKI, SGit vaults), so the custom part is small: the policies, the wake and the workflow. Little attrition, a small blast radius. It joins the editor's attrition thread (brief 6) and "go build" (brief 9).

## Who does what

| Member | Does |
|---|---|
| motion@ | one more piece for the prelude after M03, "how we keep it safe": the container, the one repository, the two vaults, the keys, the policies and the five steps, drawn as a small blast radius; the commodities underneath as a Wardley strip. From the table above only. For part 1 if it lands by 18:15 (lock 18:30); otherwise it opens part 2. |
| deck | places it after M03 in the prelude, or at the start of part 2 |
| researcher | checks each claim in the table against the record before 18:15 and tells motion@ and deck of any that is wrong |

"Full isolation" is the editor's word, quoted as his, never a fact on a slide. Claims resting on his statement or a `ROLE.md` Reach section (the one repository to push to; the container as the boundary) are marked "as stated", not "verified".
