# r3-e01-agent-evolution: the editor's check

Checked against the request, the studio checklist, the code and the screenshots (v1 and v2 end states dark and light, v1 at 10 s and 25 s, v2 at 22 s and 33 s).

## Must-fix

1. Text under 20 px on the canvas (checklist: nothing under 20 px). v2 canvas draws the "reach" label at `600 18px` (`ctx.font = '600 18px system-ui'`); raise to 20 px or more. File: src/static/studio/lab/e01/v2/index.html.
2. Text under 20 px in the HTML layer. v2: `#cap .n` (the "Step N of 6" line) is 15 px and `#quote span` (the attribution) is 16 px. v1: `#quote span` (the attribution and the sketch label) is 16 px. The attribution and the "sketch" label are the lines that carry the honesty, so they most need to be legible. Raise to 20 px or more; the v2 caption block and both quote blocks have room to grow (v1 quote sits at bottom 22 px, v2 at bottom 40 px). The engine's own `.kk` (14 px) and `.ft` are the engine's, not this work's; leave them. Files: both v1 and v2 index.html.
3. v1 does not label its shapes illustrative. The explainer says "The size of each ring ... is illustrative, and v2 says so on screen", and the checklist asks that illustrative things are labelled. v1 says only "The steps are a sketch, in order, without dates." Add "the rings are illustrative" to the v1 attribution (as v2 does: "the shapes are illustrative"), and change the explainer line to say both versions say so. Files: src/static/studio/lab/e01/v1/index.html, src/pages/ruv-sgit/agent-evolution/explainer.html.
4. The explainer says "Nothing names a product" (in "What is stated"), yet its last section names Ruflo ("a Ruflo hive"). Either reword the claim to "Nothing on screen names a product" or drop the product name from the last section. File: src/pages/ruv-sgit/agent-evolution/explainer.html.

## Should-fix

1. v1: the outer ring (r6) runs straight through the label "other agents, each with reach of its own" (text at y 48, ring top at y 22, ring crosses the text). Halo helps but the line still cuts the letters. Move the label inside the ring or outside it. File: v1 index.html.
2. v2: the small tools of the two left peers, and of the right peer, sit on or beyond the reach disc edge (peers at radius 248 plus 44 is 292, disc is 286), and "another agent" runs across the disc outline and the right small tool. Only one of three peers is labelled. Pull the peers in (about 220) or enlarge the last radius to about 300, and move the label. File: v2 index.html.
3. v2 at step 4 (22 s screenshot): the loop ring and the moving dot touch the "search" label. Nudge the label or shrink the ring (radius 62 against label baseline). File: v2 index.html.
4. v2 comment says "integrated: our systems, joined to the tools" but the code joins them to the model directly (as the explainer says). Fix the comment so the code and the explainer agree. File: v2 index.html.
5. The "tried and left out" items on v2 ("tried first; the crossing lines made the end state unreadable", "a larger reach ran into the headline") cannot be checked against the code. If they are true of the run, keep them; if not, cut them. The same for "an editor who checked all three" (this check is that). File: explainer.html.
6. Explainer, "Three colours of meaning": true as written (agent red and the heading colour, teal from the engine), but v2 also uses `--panel2` and `--agent-t` for fills. Harmless; no change needed unless you want the sentence exact.

## Checked and correct

- Quote: "LLMs using tools based on environmental feedback in a loop." is on screen in both versions, attributed "Anthropic, Building effective agents", as the request says; it is the exact phrase of that source. The explainer links the same article. It appears at 22 s in both, as the explainer says.
- Frame times: v1 `data-in`/`data-on` are 1, 8, 14, 20, 28, 35 and `data-end` 48; v2 STEPS are 1, 8, 14, 20, 29, 37 and `data-end` 52. The explainer table (1, 8, 14, 20, 28/29, 35/37; ends 48 s and 52 s) matches every value.
- No dates, no product names or logos on the canvas, no claim any product is unsafe, nothing forecasting. "Today's agentic flows" is the request's own wording and carries no date.
- Technique claims true: v1 uses `data-in`, `data-on`, `data-draw` and one `SLIDE_RENDER` for the dot; labels have a background-colour halo (paint-order stroke); v2 is one canvas redrawn from the clock in `SLIDE_RENDER`, colours read from the site tokens; no remote scripts in either (only the engine's relative script and CSS); "tools named only as kinds" is true; v2 systems join the model directly; v1 loop ring is drawn then travelled by a dot; v2 pulses go out and back without end.
- Earlier steps stay visible in both; the end states read as a still (screenshots, dark and light both fine, no clipping at 1280 by 720). Engine handles `?static`, `?t=`, reduced motion (shows the end).
- Other text in v1 SVG is 20 px (`.rl`, `.rs`), the step list is 20 and 24 px; v2 node labels, model label and caption text are 20 px or more (22 px body, 34 px title).
- Colours: agent red plus the heading colour plus the engine's teal emphasis; no new colours of meaning.
- No em-dashes in any of the four files (grep count 0). Links in the index and explainer point at pages that exist (programme.html#e01, ruv-sgit/vaults.json, how-ruv-sgit-works).
- Programme entry E01 matches: sources named (Anthropic), steps without dates and labelled a sketch.
