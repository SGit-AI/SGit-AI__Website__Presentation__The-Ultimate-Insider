# Part 2 on a projector: a check before the lock

designer@the-ultimate-insider, 29 October 2026, 18:45 London (part 2 locks at 19:30). Read only, as for part 1 (`2026-10-29__part-1-projector.md`): nothing in the slides, `talk.json` or a locked part was touched. For deck@the-ultimate-insider.

## What I measured

The 16 beats of part 2 in `talk.json`, each slide page on its own at 1920x1080 and 1280x720, at first view and after 6 seconds of animation, on the release in `dev` at a4a268e. Numbers: `2026-10-29__part-2-projector__check.txt`.

## Result: part 2 is ready

- **All 16 load**, with no script errors, at both sizes.
- **Nothing is cut off and nothing scrolls.** The "E13" and "E14" corner marks measure a pixel past the top edge at 1920 (their line box), as "E08" did in part 1; they show in full.
- **Text sizes**: every slide but one keeps its text at 14px or more. **s-port-journey** ("One action's journey") counts texts down to 13px, but they belong to the later acts still faded in, waiting their turn; the act on screen reads at about 20px. Nothing to change.

![s-port-journey at 1920](../debriefs/img/2026-10-29__part-2-projector-check__01-s-port-journey__1920.jpg)
