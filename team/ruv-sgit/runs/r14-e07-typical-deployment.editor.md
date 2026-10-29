# Editor check: r14-e07-typical-deployment

Verdict: pass with one must-fix (the first frame is empty) and three should-fixes. Data, counts, zones, barriers and explainer times all check out.

Checked and correct: 8 CI dots and 3 extension dots, each a real row with its capability label; reach zones match capabilities.json (CI: project, host, world; extension: host, tenant, world); in-mandate (authorised) teal, the rest amber; the CI boundary is `write.repository.project`, captioned "boundary: the token is contents:read" (a faithful cut of its barrier text); the extension's setting row is `authenticate-as.credential.tenant`, "setting: the site's own session controls", wall breaks and the path goes on amber; CI project zone words "the checked-out tree at this ref" are the notes' own words; counts 8: 4 and 4, and 3: 1 and 2; "measured: 8 of 8" and "derived: 0 of 3"; no score; box red only for the agent; ID 68px; no text under 20px; no em-dashes; no overlaps in the end state in either theme; explainer times (0, 5, 7, 10, 19, 20.6, 22, 26, 28, 30.5, 33, 34.4, 35, 37, 40, end 46) match the code.

## Must fix

1. `src/static/studio/lab/e07/v1/index.html`, SLIDE_RENDER: at t=0 (stage "the box") the slide shows only the headline, no box, because `band.box.style.opacity = k(.3 + bi * .6)` is 0 at 0 s. The first stage is the point of the piece. Fix: replace the line with `band.box.style.opacity = k(0, .4)` (no per-band offset), so both boxes are fully visible by 0.4 s, and have `?t=0` show them (start `k` at `-0` is still 0 at t=0, so also use `Math.max(k(0, .4), t === 0 ? 1 : 0)`).

## Should fix

1. `index.html` (slide): the CI shortfall `write.repository.tenant` (the mandate's tag push, 4 of 5 granted) is nowhere on the slide, so "4 in its mandate" reads as the whole mandate. Fix: add to the CI tag a plain line from the data, e.g. `'asked for, not granted: ' + e.shortfall + ' (push the tag)'`; keep it 20px and check it clears the extension box (CI tag ends near y=335, the extension box starts at 445). If left out, say so in one line in the explainer (it already does).
2. `index.html` (slide): the hollow dot (boundary) and the two colours have no key; a new viewer sees only the tag line's teal and amber words. Fix: make the hollow dot's meaning read from its caption, e.g. prefix the wall caption "boundary holds: the token is contents:read", and for the setting "setting, not a control: the site's own session controls" (only if it fits on one line at 20px within 460px; otherwise leave).
3. `explainer.html`: it says at 0 s "Two boxes in the middle", but at 0 to 5 s both sit at x=520, the CI box at the top and the extension at about y=445, and the second box floats mid-slide until 26 s. Fix: reword to "Two boxes, as drawn on an architecture diagram", and note the extension box waits at the right-centre until 26 s.
