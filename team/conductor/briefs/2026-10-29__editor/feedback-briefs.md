# The editor's feedback on the talk: briefs per member

From the editor (Dinis Cruz), 29 October 2026, about 13:50 London, dictated in a claude.ai chat. The talk is tonight at 19:00 London. The editor pastes this into the conductor's session. The conductor routes each section to its member's mailroom at the 14:02 wake, and they are acted on at each member's next slot.

## The order, for every member

1. **The player, from ruv.sgit.ai, working on an iPad. This is the main priority.** It goes ahead of the append lane in `conductor-brief.md`, which becomes second.
2. **The framing.** "Nobody is presenting them as one story" goes, and "the perfect storm we are brewing" comes in.
3. **The animations** of the story below.

## The story the editor wants to tell with the animations

- **The past.** There were lots of small attackers and small events, but never mass exploitation.
- **The building.** An attacker gets into a huge building and turns left, where there are only small things, instead of right, where the gold is. Agents will turn right. (The editor's working picture is something like Lemmings, though he is not sure the analogy is right. Many small figures, each making a choice.)
- **The question for the audience.** In every incident you have seen, the attackers could have done much more damage, even where the damage was large.
- **The shift.** Past attacks were mostly against availability or confidentiality. Agents bring attacks on **integrity**. Those are far more dangerous, because a small amount of corrupted data is enough to lose trust in the whole system. Agents do damage that fast, and across everything.

---

## To dev@the-ultimate-insider: the player (main priority)

The editor wants the presenting experience he had with the ruv.sgit talk player. It is described in the article at https://ruv.sgit.ai/articles/the-talk-player.html (15 October 2026), and the code is at https://github.com/SGit-AI/SGit-AI__Website__Ruv (`talk/player.html` and `assets/clock.js`, Apache-2.0, same organisation). This site's player is 236 lines and has none of the following:

- **A talk clock and the talk's timing.** Each beat has a start and a duration, and the player checks that they add up to the talk's length.
- **Stages per slide, with two stops per step.** One stop is where the step begins, and the other is the step fully built and paused, ready to talk over.
- **Start and stop for every animation.** A virtual clock (`clock.js`) lets the player pause, speed up, step through and seek any live slide.
- **The presenter's timer.** It starts when he starts speaking and turns teal, amber or red depending on whether he is ahead of the plan or behind it.
- **It works on an iPad.** That means touch, a clicker, a presenter laptop with a projector window, and bad or no wifi (a service worker, a warm-up, and an offline single file). **This site's player does not work on an iPad today**, and it must work there tonight.

Ask: port the ruv.sgit player and clock into `src/static/talk/` under this site's gate. Copy the code into the repository, because the gate refuses scripts from another host. Test it on an iPad viewport with touch. Ask deck by mail for the start and duration of each beat in `talk.json`, which is deck's file. If the whole port cannot land and be tested before about 17:00 London, ship iPad touch and start/stop first, and say what is left in the end banner.

## To deck@the-ultimate-insider: the framing and the timings

1. **Drop "nobody is presenting them as one story" and "Three known problems, one story".** The editor finds this framing arrogant. Recast the opening around **the perfect storm we are brewing**: three things that are known separately and are now arriving together. This applies to the beat `three` and the script. The same line is on the home page's abstract; ask its owner to change it.
2. **Durations.** Give every beat a start and a duration, so that dev's new player can run the talk on its clock.
3. **The animation brief.** Turn the story above into requests to ruv.sgit, one at a time, by the pace. Suggested first: the building (left or right), then availability and confidentiality against integrity. Place them in the arc near `unreported` ("Why we do not see more of it") and `collision`.

## To ruv.sgit@the-ultimate-insider: the animations

The editor wants **many small animations and infographics** that let him tell the story above. Deck will send the requests one at a time. Read the story section now, so that the first run starts quickly:

- many small figures, attackers and agents, making choices in a building, and most of them turning left until the agents turn right;
- the counter-factual "it could have been much worse", shown on real incidents from the claims register;
- availability, confidentiality and integrity, and how little corrupted data it takes to lose trust in everything.

Every piece must run on the new player's clock (start, stop, stages, seek) and on an iPad.

## To researcher@the-ultimate-insider: the facts behind the story

Deck and ruv.sgit will need sources for:

1. Incidents where the attackers had far more access than they used.
2. The share of past attacks against availability and confidentiality, compared with integrity.
3. Cases where a small amount of corrupted data destroyed trust in a whole system, with agent cases first.

Add them to the claims register, so that every number on screen keeps its link.

## To storyteller@the-ultimate-insider (once joined)

Add **the perfect storm** as the premise's frame, and put the building, the question for the audience and **the integrity shift** into the story tree. Check them against the memo's part one, where the inside is the problem.

## To conductor@the-ultimate-insider

Route each section above to its member's mailroom at 14:02. In `pace.json`, put dev's player first, ahead of the lane and the sequence. Flag in the banner, by name, anything that will not land before 19:00.

---

## Addendum (about 14:00 London): reuse what ruv.sgit.ai already has, and a new piece for Sharness.ai

The editor says ruv.sgit.ai already has some very good animations, in particular the ones that explain **the blast radius** and **what Agent Behaviour Policies do**. Review them before making new pieces.

### To deck@the-ultimate-insider: a review of ruv.sgit.ai's pieces

Review the ruv.sgit.ai talk and studio, and sort every piece into one of three groups: **reuse as it is**, **adapt**, or **leave**. Write one line per piece saying where it would sit in this talk's arc. The candidates found so far, all listed in https://ruv.sgit.ai/llms.txt:

- `slides/abp/`, "What an Agent Behaviour Policy is" (the talk-10 deck)
- the studio, v1 to v7 (`studio/vN/`), especially **v4, the policy gate**. v7 is three.js, which this site's gate refuses as it is, so it would need a rebuild.
- "the definition, animated" (run r3-define): the equation, the layers, and one action's journey
- ruv.sgit in motion (`ruv-sgit/motion/`)
- the policy-engine result from POC1: in legacy mode all 11 actions are allowed; in enforce mode an ABP stops 6 of 11 (4 denied and 2 sent to a human)

A piece called "blast radius" has not been found on ruv.sgit.ai yet, though this site has `/ruv-sgit/blast-radius/`. Ask the editor which one he means. Reused pieces must keep their sources and run on the new player's clock.

### To dev@the-ultimate-insider

Copying pieces from the SGit-AI__Website__Ruv repo (Apache-2.0) falls under the same rule as the player: copy the code into the repository, take no scripts from another host, and check each piece on the iPad.

### To ruv.sgit@the-ultimate-insider: a new piece, what Sharness.ai can do

Make one new animation that explains **what Sharness.ai can actually do**. Its place is in the way out or the live demos, next to the behaviour policies. **Do not guess what Sharness does.** Nothing about it was found on the open web from this chat. Take its capabilities from the editor, or from the project's own repository and site, through the researcher. Deck sends the request by the pace, after the player.

### To researcher@the-ultimate-insider

Capture Sharness.ai's own description of what it does, as a source, so that the piece has something to cite.
