# Parts 2 and 3: the attacks, the solution in depth, live content (29 October 2026, about 17:10 London)

By conductor@the-ultimate-insider, from the editor's words in the conductor's session. For work behind the scenes while part 1 is on stage (19:00); part 2 locks at 19:30, part 3 at 20:00.

## The editor's words, in short

The hack::soho and IOActive crowd is technical. They need:

- **Infographics and explanations of the documented attacks, as blast radius**: "fundamentally, that's what it is ... on all the documented stuff".
- **The solution, in depth**: SGit's architecture, the PKI, the vault applications, the scale SGit has now, and its features over Git.
- **SHarness, technical**: the process behaviour policy; a new process gets nothing it does not need; a KMS; a virtual file system from the user's point of view; the network controlled at packet level; digital twins; running locally, or distributed across machines, Kubernetes, cloud and distributed cloud environments; and what is done to defend it.
- **An invitation to the room**: "try to escape the harness, and let me know the use cases".
- **Live vaults in the slides**: "this bit in the middle is actually a vault that is just being opened up using a ... read key"; the researcher surveys the public vaults on sgit.ai and newsroom.sgit.ai for embeddable demos (the behaviour policies before and after).
- **New slides as he presents**: the player checks every minute for new slides or content, so he can say "there's a new slide here, just added".
- **The team's board inside his slide environment**, to show the work happening.

## Who does what

| Member | Does |
|---|---|
| researcher | the vault survey (public read keys already published by their owners on sgit.ai and newsroom.sgit.ai, what each shows, which suit an embed); SGit's architecture, scale and features over Git; SHarness's capabilities from its own pages (no guessing); the documented attacks' reach, for the blast-radius pieces |
| storyteller | places these in parts 2 and 3: the attacks first, then the solution, the SHarness challenge near the close |
| deck | the beats for parts 2 and 3; asks the makers one piece at a time; part 2 ready by 19:30, part 3 by 20:00 |
| ruv.sgit | the blast radius of the documented attacks (its programme's pieces, extended), and its SHarness series as the technical deep dive |
| studio@ | showcase slides: SGit's architecture, the PKI, the vault applications, newsroom.sgit.ai and its API, from the editor's own pages |
| motion@ | after the prelude: SHarness from the inside (a process asking, the policy deciding, the packet-level network, the twin) as a moving diagram |
| dev | the player checks every minute for new slides or content and shows a "new" mark; a slide that embeds a public vault by its published read key; the team's board as a slide |

## Rules

- **Only read keys their owners have already published.** Never a write key, a vault key or anything private, on a slide or in a screenshot.
- **The minute check loads nothing from a host the gate refuses**: it reads this site's own files.
- **The invitation to escape SHarness says what is in scope and where to report** (the project's own pages say how), and is the editor's own invitation about his own software.
- **Documented, public incidents only**: no new attack technique built or described.
- **Locked parts are never touched.**
