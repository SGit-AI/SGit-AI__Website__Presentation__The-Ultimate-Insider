# The player: what the editor asked for, and what it ports

dev@the-ultimate-insider, 29 October 2026, about 14:55 UTC, from the editor's words in dev's session. The brief behind it: `team/conductor/briefs/2026-10-29__editor/feedback-briefs.md` (To dev, the main priority) and `conductor-notes.md` (the build mode, 14:10); deck's request of 14:45 (mailroom/dev/001, the studio's animations in the talk). The source: ruv.sgit.ai's talk player, `talk/player.html` and `assets/clock.js` (SGit-AI/SGit-AI__Website__Ruv, Apache-2.0), described feature by feature in https://ruv.sgit.ai/articles/the-talk-player.html.

## The editor's words, summarised (14:50)

- **Timing on screen, as a countdown.** ruv.sgit's player had one, and he wants it here. He will say how much time he has; the player counts that down and keeps him on track section by section.
- **Two levels of navigation:** slides forward and back, and the steps inside a slide forward and back.
- **Every step has two stops: its beginning and its end.** Going back lands on those stops, the built end of a step, not on a blank frame. "Quite an important concept": it is the one from his note at 17:49 on 15 October ("for each step you need to have two moments, the beginning of the step and the end of the step").
- **The UI is part of what he shows.** A presenting interface customised to what he wants to do is itself the point: it loses a little screen space, and that is worth it.
- **Interactive navigation.** He may show all the studio's pieces or some; he needs a good way to skip forward.
- **A REPL for a talk.** Bret Victor's *Inventing on Principle*: the feedback between the creator and the creation. He wants to interact heavily with the presentation, and to give feedback through his lane (the pane) as he goes.

## What the port keeps from ruv.sgit.ai (the article's table)

Play and pause, and nothing plays unless he presses play · « » slides (PageUp and PageDown for a clicker, swipe) · ‹ › steps (tap) · **two stops per step**, and on live slides only built frames · the step track, one labelled segment per step · speed 0.75× to 2×, and per-slide speed · auto or hold (hold by default), animations finish while holding, stop at the end of the deck · **the countdown** ("next in N s" or "ends in N s", amber under 10 s, red under 5 s) · **the talk timer**, his own clock, teal ahead, amber late, red more than 20 s behind · the slide picker with each slide's steps · portrait layout for an upright iPad · review mode · presenter notes · the audience window over BroadcastChannel · black screen · the rehearsal log · themes · extras after a gap · the loading indicator · the service worker and warm-up for bad wifi · timeline validation · the virtual clock contract.

## What is new here

1. **The time he has.** He sets it (`?have=40` or the ⏱ button, kept in his browser); the countdown shows what is left of it, and the plan is scaled to it, so ahead and behind are measured against his time, not the talk's planned 38:30.
2. **Sections.** `act` in `talk.json` (Opening, the insider, the infrastructure, ...) is a level above slides in the picker and on the timeline.
3. **The studio's pieces as slides.** This site's slide engine (`talk/engine/slide.js`) answers the clock's contract itself: `window.RuvClock` (pause, play, seek, rate, elapsed), `?ruvt=`, `?ruvpaused`, `?review`, `?once`, and the steps a page declares, `window.RUV_STEPS = [{ t, label }]` or `data-stops="2 12 30"` on `#cv`; with neither, three stops: the beginning, the middle and the end. So every slide and every lab piece is pausable, seekable and steppable, and stepping back needs no reload.
4. **The build mode** (next): every beat and every studio piece in one list; his order by dragging, show or hide, a comment on each through his lane; the player runs his running order straight away.
5. **The viewer** (after): `talk/view.html?src=<path from the site root>`, one piece with replay, a scrub bar, speed, its stops, its id, previous and next.
