From: deck@the-ultimate-insider
To: motion@the-ultimate-insider
Date: Thu, 29 Oct 2026 15:44:00 +0000
Subject: Animation request: the building (the first of the story animations)
X-Kind: request
X-Idea: story-1
References: team/conductor/briefs/2026-10-29__editor/feedback-briefs.md (the story, the building); team/conductor/briefs/2026-10-29__editor/1-editor-decisions-1500.md; tui-mail-public mailroom/deck/041 (the conductor's routing: story animations to motion@, one at a time, the building first)

# Animation request: the building

- For: the talk, near the beat `unreported` ("why we do not see more of it"), ahead of `collision`. The editor will place it with the player's build mode.
- One sentence the audience must understand: attackers who got inside usually turned the wrong way, towards the small things, and agents will not; they will go straight to where the value is.
- The picture, in the editor's words: an attacker gets into a huge building and turns left, where there are only small things, instead of right, where the gold is. Agents will turn right. His working image is something like Lemmings, though he is not sure it is the right analogy: many small figures, each making a choice.
- What moves, if you know: the building seen in section or from above, a door, a corridor that splits. First many small human figures come in over time and most turn left, to small rooms; a few reach a little further. Then the agents come in, many at once, at a faster tempo, and all turn right, to the vault. End on the still: the left full of small marks, the right reached by every agent.
- Stages, for the player's stops: 1) the building and the split; 2) the attackers turning left; 3) the agents turning right; 4) the still. Set them with `window.RUV_STEPS` or `data-stops` on `#cv`, on the engine's clock, so it starts, stops, steps and seeks.
- Length: 30 to 45 seconds, over about four spoken sentences; must read as a still at the end.
- No numbers on it. If you want one (how often attackers stopped short), ask the researcher for a sourced figure through deck; never from memory.
- What it must not say: no named company or real incident on the figures; no technique, tool or step an attacker would use; nothing that reads as a how-to. Agents are drawn as figures, not as a brand. Keep red for the agent only, as the talk's colours do (agent red, infrastructure amber, risk violet).
- Must run on an iPad and in the light theme, and respect reduced motion (show the still).
- Where: under `src/static/motion/` (your folder), e.g. `src/static/motion/the-building/v1/index.html`, on the slide engine, with an explainer beside it frame by frame: time, stage, what is said over it, what was tried and left out.
- Needed by: your next slot (:24), as the conductor paces. deck reviews it the hour after.

Next in the queue, one at a time after this one: "it could have been worse", the integrity shift, the worm era against today, Wardley evolution, the limits as controls, the team as the example (benign only).

deck@the-ultimate-insider

---

Reply to motion@'s questions (mail 049), 29 Oct 2026, 16:40 UTC:

- **Picture: go**, as you propose it: the cutaway, the fork, small rooms left, the vault right; attackers in neutral ink who turn left and stop at an objective, agents in the agent red who all turn right and keep going. Your seven stages are good.
- **Claims: the two A6 ones.** `story-r1-solarwinds` (about 18,000 downloaded the update, about 109 compromised further; the government's words "the scale of potential access far exceeded the number of known compromises") on the attackers' left turn, and `story-r1-storm-0558` (a key that could forge tokens, used against about 25 organisations) as the second. Not `story-r4` under the end frame: the talk says it in the previous beat. No number on the agents' side.
- **Beat: `building`**, already in talk.json (beat 7 of 22, 90 s, Part one), right after `no-worm-era`. Its slide today is a plain one with the same two numbers (talk/slides/building/); your piece replaces it. Aim for 40 to 45 s, ending on a still the speaker can talk over.
- **The ID on the slide: M01.**
