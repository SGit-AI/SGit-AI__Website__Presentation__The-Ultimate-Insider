# Editor review: r15-e10-four-barriers

Verdict: pass with one small must-fix (the page does not say `is_control` is abp.sgit.ai's reading) and three should-fixes.

Checked against the data and in the browser (dark and light, t=6, 14, 22, 30, 38, 46 and ?static, 1280x720): counts 13/1/2/0 and 14/1/1/0 match the rows; the one mover is `execute.process.host` (setting to none), found by diffing the rows; the grant, mandate, excess, unbounded excess and irreversible figures are identical in both examples (16, 5, 12, 12, 8); the closing line is the claim `abp-cc-one-barrier-moved`; the barrier meanings and glyphs are the file's; "0 of 22 rows measured" and "No score" appear; the walls behave faithfully (none: dashed, the path goes through; expectation: the path jumps; setting: the wall breaks; boundary: it holds and the path stops); no text under 20px (measured in the DOM); the ID is large and clear of the headline; the content clears the headline in both themes; the end state has no overlaps; no em-dashes; the explainer's times (0, 9, 12.4, 15.8, 19.2, 24, 34-36, 41, 44, 52) match the code.

## Must fix

1. `src/pages/ruv-sgit/four-barriers/index.html`, the `.note` paragraph. It does not say that "a control" (`is_control`) is abp.sgit.ai's own reading; only the explainer does, and the slide's "not a control" / "a control: holds" labels are shown as plain fact. Fix: add to the note "Which kind counts as a control is abp.sgit.ai's own reading (the file's barrier_kinds_note), not a measurement." Optionally state the same in the lead as "abp.sgit.ai reads only a boundary as a control".

## Should fix

1. `src/static/studio/lab/e10/v1/index.html`, the derived caveat. "Derived, 0 of 22 rows measured" appears only after 41 s, while the 16 rows and the 13/1/2/0 counts are on screen from 24 s and look like measurements. Fix: from P2 the `q` line reads "... 16 rows, none at a boundary. Derived, 0 of 22 measured." (change the P2..P3 branch of `q`; it fits at 20px).
2. Same file, the headline "Only a boundary is a control." is the author's position drawn as fact. Fix: put "abp.sgit.ai's reading" on screen, e.g. the verdict text "a control: holds" becomes "a control (abp.sgit.ai's reading)" or add it to the first `q` line at t<9.
3. Same file, layout: the lower third (y 540-720) is empty until 41 s, so the slide does not use the whole canvas for 41 s. Fix: move the lanes down or space them wider (`LY` = [210, 320, 430, 540], with `AY` at 375), or show the (empty) table header earlier, so the table and the lanes share the canvas.

## Notes (no action needed)

- Red is kept to the agent, its path and the kicker; the kicker's red is the studio's own style. Amber marks the mover and teal the control, so no sea of red.
- A failed data fetch is silent (console only); acceptable for a lab slide, and the explainer says it needs HTTP.
