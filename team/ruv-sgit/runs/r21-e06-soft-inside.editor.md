# Editor check: r21 E06 soft-inside

**Verdict: pass, with no must-fix items.** Two should-fix items on wording and timing. Checked in both themes at 6, 9, 27 and 39 s and in the end state (screenshots in the ed21 scratchpad).

What holds: no number, product, organisation or incident anywhere. The "Illustrative: the shape, not a measurement; the data is coming from the researcher." line fades in at 0.6 s and stays to the end. The pages say "illustrative" as well. Nothing claims a measurement. The ID is large (72 px, top right). Agent red is used only for the agent and its path. The wall tick is teal, the reached systems amber, everything else neutral. All labels sit inside the drawing. Every text is 20 px or larger. Nothing overlaps the headline, the ID or the note. The end state is clear and legible in dark and light. No em-dashes. RUV_STEPS (0, 5, 13, 21, 24, 41) matches the explainer. The other times match the code: shell 1 to 4 s, wall tick 7.2 s, second path 8.4 to 10.6 s, agent 21 s, hops at 24, 28, 32, 36 s, lit at 26, 30, 34, 38 s, end line 41 s, end 50 s.

## Must fix
None.

## Should fix
1. `src/static/studio/lab/e06/v1/index.html`, the SYS row for the service account: "broad rights to everything" says more than the programme's idea, which says "broad service accounts". Fix: change the string to `'broad rights'`. Then change the matching text in `src/pages/ruv-sgit/soft-inside/explainer.html` (the 13 s row, "broad rights to everything") and the `aria-label` is already fine.
2. `src/pages/ruv-sgit/soft-inside/explainer.html`, the 13 s row: the code shows the systems at 13.5, 15, 16.5 and 18 s (SHOW), so "13 s ... 1.5 s apart" is off by half a second. Fix: write "From 13.5 s, four systems appear as quiet boxes, 1.5 s apart (13.5, 15, 16.5, 18 s)". In the same file's 5 s row, "the wall where it was met turns the accent colour" is not what the code does: a teal tick fades in on the wall at 7.2 s. Fix: "a teal mark appears on the wall where it was met".
