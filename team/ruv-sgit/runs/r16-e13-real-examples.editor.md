# Editor check: r16-e13-real-examples

Verdict: fix, then ship. Numbers, barrier kinds, host reaches, measured vs derived and the explainer's times all match the data and the code. One styling problem reads as a ranking (must fix). No em-dashes, no text under 20px (checked in the DOM, both themes), nothing overlaps at the end, both themes legible. Checked: counts 16/5/4/12/12, 16/5/4/12/12, 1/1/1/0/0, 3/1/1/2/2, 8/5/4/4/3; rows measured 0 of 22, 0 of 22, 0 of 1, 0 of 3, 8 of 8; the one boundary (write.repository.project, CI); host reaches are each example's own, and the chat panel honestly says "not in its grant".

## Must fix

1. `src/static/studio/lab/e13/v1/index.html`, CSS `.pn.mea{border-color:var(--head)}` and `.pn.der{border-style:dashed;...}`. At 36 s the CI card gets a bright white (dark) or black (light) border while the other four go dashed and dim. That reads as "this one is the good one" and breaks the no-rating rule, and the explainer's "turns solid and the other four dashed" describes it. Fix: give all five panels the same border (solid, `var(--line)`) at all times; delete the `.der` and `.mea` rules and the `classList.toggle` line in `SLIDE_RENDER`. Measured vs derived stays in the panel text ("measured" / "derived", "8 of 8 rows measured"), which already says it. Then in `explainer.html`, row "36 s", replace "the CI job's frame turns solid and the other four dashed; each panel says" with "each panel says".

## Should fix

1. `index.html` `#id{...color:var(--dim)}`: the E13 ID is large (72px) but dim grey and the faintest thing on the slide. Fix: `color:var(--head)` (or `var(--text)`).
2. `index.html`, the `ms` line: "0 of 22 rows measured" sits under "grant 16" with no word on why 22. The explainer explains it, the slide does not. Fix: for the two coding panels only, show `0 of 22 rows (tool-level)`, if it fits at 20px in 236px; otherwise add one line to the 28 s...36 s question text: "22 rows = 16 capabilities across the tools that reach them".
3. `explainer.html`, "Technique": "Every text is 20 px or larger" is true of the slide as measured; keep, but add that the E13 ID is the one large element (72 px) so the editor's rule is visibly met.
4. Minor crowding at 18 s to 20 s in the two coding panels: the top-left excess dot sits close to the "mandate" label (about 20px). Fix: raise `gap` from `.62` to `.75` in `build` so no dot lands beside the label.
