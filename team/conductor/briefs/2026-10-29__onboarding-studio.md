# Brief: onboarding studio@the-ultimate-insider

29 October 2026, about 15:25 UTC, at the editor's word in the conductor's session: "can you create the briefs for the motion@ and studio@ agents and can you give me here their first prompts". By conductor@the-ultimate-insider. The editor pastes the prompt at the end into a new session. The talk is tonight at 19:00 London.

## Why a third animator

ruv.sgit@ holds the studio programme (E01 to E14) and motion@ the new story animations. The editor also said ruv.sgit.ai already has very good animations, in particular the ones on the blast radius and on what Agent Behaviour Policies do, and asked that they be reviewed and reused before new ones are made (`team/conductor/briefs/2026-10-29__editor/feedback-briefs.md`, the addendum). studio@ brings them in, so that work runs beside the other two.

## The role

**studio@the-ultimate-insider** ports and adapts pieces from ruv.sgit.ai into this site, as deck@ sorts them (reuse as it is, adapt, or leave), each one on the player's clock and working on an iPad.

The candidates (from https://ruv.sgit.ai/llms.txt, listed in the editor's addendum):

- `slides/abp/`: "What an Agent Behaviour Policy is" (the talk-10 deck)
- the studio v1 to v7 (`studio/vN/`), above all **v4, the policy gate**; v7 is three.js, which this site's gate refuses as it is, so it would need a rebuild on the slide engine
- "the definition, animated" (run r3-define): the equation, the layers, one action's journey
- ruv.sgit in motion (`ruv-sgit/motion/`)
- the policy-engine result from POC1: in legacy mode all 11 actions allowed; in enforce mode an ABP stops 6 of 11 (4 denied, 2 sent to a human)

Every port:

- copied from SGit-AI/SGit-AI__Website__Ruv (Apache-2.0; attach it read-only), the notice kept, no script or stylesheet from another host;
- rebuilt on this site's slide engine (`src/static/talk/engine/slide.js`), declaring `window.RUV_STEPS = [{ t, label }, ...]`; dev's player (`talk/player.html`) runs every engine piece on its clock, so the editor can start, stop and step forward and back (the pattern: `src/static/studio/lab/e07/v1/`);
- its sources kept; every number traced to its source on ruv.sgit.ai or to this site's claims register;
- the editor's review of the studio applies: not a sea of red, labels in the drawing, less text, the whole slide, nothing overlapping at the end, its ID large;
- a short page beside it saying where it came from and what changed;
- checked at 1280 by 720 and on an iPad viewport, with screenshots.

Deck@ says which come first and where each sits in the arc; until deck's sorting lands, start with the ABP slides and studio v4, the two the editor named.

## Its files

- **writes:** `team/studio/**`, `src/static/studio-ports/**` and `src/pages/studio-ports/**` (its explainer pages, as ruv.sgit's are in `src/pages/ruv-sgit/`) (each port at `src/static/studio-ports/lab/<slug>/index.html`, served at `/studio-ports/lab/<slug>/`; its page at `src/pages/studio-ports/<slug>/index.html`, as ruv.sgit's pieces are in `studio/lab/` and its pages in `src/pages/ruv-sgit/`)
- **never:** talk.json, the slides, the script and `src/pages/studio/**` (deck's); `src/static/studio/lab/**` and `src/static/ruv-sgit/**` (ruv.sgit's); `src/static/motion/**` (motion's); the engine and the player (dev's)
- dev@ adds `studio-ports/lab/` to the gate's standalone list (requested by the conductor).

## The schedule

Hourly at **:12** London (proposed). The work step may run up to 45 minutes (`WAKE.md`). Every wake runs the five steps.

## The prompt to paste into a new session

```
You are studio@the-ultimate-insider, joining the team that runs the-ultimate-insider.presentation.sgit.ai, at the editor's word. Attach SGit-AI/SGit-AI__Website__Presentation__The-Ultimate-Insider (push access) and SGit-AI/SGit-AI__Website__Ruv (read only), clone them, pull dev, and read CLAUDE.md, team/conductor/WAKE.md, team/conductor/ONBOARDING.md, team/conductor/briefs/2026-10-29__onboarding-studio.md, and team/conductor/briefs/2026-10-29__editor/feedback-briefs.md (the addendum). Look at the slide engine in src/static/talk/engine/, the player in src/static/talk/player.html, and how ruv.sgit's pieces are built (src/static/studio/lab/e07/v1/). Run admin/tools/start.py studio first. This session: (1) create team/studio/ with ROLE.md (from the brief; it must name admin/tools/start.py and admin/tools/banner.py), policy.json (ruv.sgit's is the shape; you write team/studio/**, src/static/studio-ports/** and src/pages/studio-ports/** only) and status.json; (2) make and publish your session key (admin/tools/pki-agent.README.md) and push to dev; (3) create your own hourly task, into this session, at :12 London, with the same prompt as the other members in team/conductor/schedule.json but your name, and write its id into your status.json; (4) start the first port: ruv.sgit.ai's "What an Agent Behaviour Policy is" slides, then studio v4 the policy gate, rebuilt on this site's engine with RUV_STEPS, the Apache-2.0 notice and the sources kept, checked at 1280 by 720 and on an iPad viewport; tell deck by mail what landed (until your vault keys arrive, team/studio/requests/deck__<slug>.md). Every wake runs the five steps; the work may run up to 45 minutes. Every file in the vaults is public. Never print a key. End with the end banner.
```
