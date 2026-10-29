# r2-b01-storyboard: the editor's check

Checked: `src/static/studio/lab/b01/storyboard/index.html` (frames from the array F), `notes.md`, the three screenshots, against the brief, `how-it-works.html` and `talk.json`. No file edited except this one.

## Must-fix

1. **A source number on screen.** Frame 2 (index.html, F[1].m): "Nothing explains it yet: that is the next seventeen minutes." The only source for "seventeen" is the brief's prose ("about seventeen minutes"), and the brief says it needs no numbers on screen. The page header also claims "there are no numbers in it", which this sentence contradicts. Fix: "that is what the acts are for", or drop the clause. (The talk.json beat durations do not sum to a verifiable seventeen for the three acts, so the figure is also unchecked: definition 120 s, infrastructure 150 s, spreadsheets 150 s is 420 s of allotted time, not 17 minutes.)

## Should-fix

1. **A fourth colour of meaning.** Frame 7 and 8 (index.html, `fence` and `moves`) use `var(--accent)` (teal) for the licence frame, its switch and the four move labels, plus white (`--head`) for the filled overlap. The brief and checklist say keep the three colours, three at most. The teal is the site's chrome accent, not agent red, infrastructure amber or risk violet. Suggest drawing the fence and labels in white or the head colour so the three colours stay the only colours of meaning.
2. **Frames 3 to 5 contradict themselves on words.** Each shows "(before) <first line of the beat>" as its quote, but the cost note says "no words over it" and the table says the opener sits in "the first 3 s ... before the speaker starts". State once that the opener runs in silence before the beat's first word, and that the beat's own length in talk.json (120, 150, 150 s against about 36 s to 55 s of words) already has room for it, so nothing lengthens. Today the claim "no beat gets longer" is asserted, not shown.
3. **Frame 7 "reach measured: its edge is traced exactly."** The talk says "measure what the agent can actually reach"; the picture traces the overlap's edge. That implies the overlap is the reach, which the script does not say. Soften the note to "the overlap is outlined; the measurement is of what the agent can reach", or label it as a picture of the idea.
4. **Frame 8 adds a small claim.** "The overlap moves freely inside it" and "because it can be closed" go past the script ("let it act freely inside it ... once it fits inside your appetite"). Add "once it fits the appetite" or drop "freely". It is marked optional, so low risk.
5. **Frame labels touch the circles** (screenshot 1, frames 3, 4, 5): "act one: the insider", "act two: the infrastructure", "act three: the decision" sit on the bottom edge of the lower circle (label y=318, circle bottom near 305, scaled in the viewBox). Move the label down or the circles up so nothing overlaps.
6. **Frame 6 short forms** "cannot tell, stop or replay" and "could not see it, a row afterwards" are accurate but drop "cannot decide during it"; fine as short forms, but say on the frame that they are cut-downs (the note does) and keep "a row afterwards" close to the script's "a spreadsheet row", or the room loses the word spreadsheet at the moment it should return. Optional.

## Checked and correct

- Quotes: frame 1 (beat three, "One: ... Two: the infrastructure ... Three: the risk management ..."), frame 2 ("Where they overlap is the scenario this talk is about."), frames 3, 4, 5 (first lines of definition, infrastructure, spreadsheets), frame 6 (collision, three ellipsised clauses), frame 7 (way-out, all four moves verbatim), frame 8 ("We put brakes in cars so that we can go faster.") are the script's words in order. No paraphrase in quote position.
- Times from 150 words a minute, from the beat start, all follow: three "One" at 6.4 s (0:06), "Each one is a known problem" at 28.4 s (0:28), "Where they overlap" at 30.8 s (0:31); collision "An entity" at 3.6 s (0:04), "None of this is hypothetical" at 30.0 s (0:30); way-out "Measure" at 2.4 s (0:02), end at 14.4 s (0:14); brakes "We put brakes" at 26.0 s (0:26).
- Colours of the circles: agent red, infrastructure amber, risk violet via tokens, same positions throughout.
- Way-out frame keeps the brief's limit: "governed, not gone", the overlap stays.
- The eight frames match the brief's list in order, with the optional close; the four points are carried (three problems named in frame 1, arriving together in 1 and 2, the overlap as the scenario in 2 to 6, the way out on the overlap in 7).
- Act-opener cost is stated (3 s each, 9 s in all) with the open question for deck, as the brief asks.
- No em-dash (U+2014) in index.html, notes.md or this file. No numbers from a source on screen other than the one in must-fix 1 (the "3 s", "eight frames", "one third" are the storyboard's own).
- Page stays standalone (tokens.css only, inline script, no other host), works in dark and light by `?theme=`, and at phone width the frames stack without horizontal scroll (screenshot 3).
- Frame text in the SVG is 16 to 18 units on a 640 viewBox, so 32 to 36 px at 1280: above the 20 px floor.
