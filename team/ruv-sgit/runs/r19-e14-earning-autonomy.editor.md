# Editor check: r19-e14-earning-autonomy

Verdict: pass with fixes. 1 must fix, 3 should fix. Checked in both themes at t=5, 10, 22, 36, 40, 50 and ?static; no em-dashes; no text under 20px; ID (72px) and headline clear of each other; explainer times match the code (9, 13/19/25 rounds, 32.5 stop, 34, 37, 38.2, 39.4, 44, end 52).

What holds: "illustrative" in the kicker, on the card tag and in the line under the headline from 44 s and at the end; no real agent, person or date; the licence rows match the talk (authorised by, held by, policy, expiry, accepted risks that expire); suspension drawn dashed in the third colour and boxed "Designed, not shipped", with the end line quoting the talk; levels are plain placeholders; no evidence claimed beyond "level N held"; red only for the agent, its path and its step outside.

## Must fix

1. src/static/studio/lab/e14/v1/index.html, `b.ag` ("the agent" label): at the end it sits at x 1088 to about 1180 and the mandate's right border (x 1110) runs through it. Nothing may overlap at the end. Fix: place the label left of the dot, above the tread: `B.ag.setAttribute('text-anchor','end'); B.ag.setAttribute('x', pt.x - 18); B.ag.setAttribute('y', pt.y - 14)` (it then sits over the level-4 tread, clear of "act alone" at y 282, since the label is at y about 294). Or set `FX` to 1050 and keep the label inside 1110 with a shorter text.

## Should fix

1. src/static/studio/lab/e14/v1/index.html, gates: the two 14x16 rects read as teal blobs, and open they are hard to tell from a smudge on the path; the "gate" is never named on screen. Fix: draw each gate as two taller posts (width 8, height 36) and, once open, add a small label "gate" (20px, `var(--dim)`) or fold it into the evidence text ("gate opens: level 1 held").
2. src/static/studio/lab/e14/v1/index.html, the step outside: the editor's favourite is the path jumping the wall and changing colour or breaking. Here the dashed red path crosses the mandate's top border and nothing changes. Fix: at 35.4 s switch the mandate outline (the `rect` in `b.man`) from `var(--line2)` to `var(--risk)` dashed, `stroke-dasharray` "10 8", and end the red dashed line at the ring, so the crossing visibly breaks the wall; the box then answers it.
3. src/pages/ruv-sgit/earning-autonomy/explainer.html, 13 s row: it says the agent walks "its level to the gate (2 s)" in each round, but the first walk runs 11.5 to 15 s (3.5 s). Fix: write "the first walk takes 3.5 s (from 11.5 s), later ones 2 s", and add the same line to the 9 s row ("at 11 s the agent appears, and from 11.5 s it walks").
