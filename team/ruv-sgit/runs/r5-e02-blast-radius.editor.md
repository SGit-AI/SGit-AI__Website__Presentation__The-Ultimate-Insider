# r5-e02-blast-radius: the editor's check

Checked: the slide (src/static/studio/lab/e02/v1/index.html), the page and the explainer under src/pages/ruv-sgit/blast-radius/, against the request, abp-examples.json (claude-code-cli-confirmations-enabled) and the studio checklist. Rendered in Playwright at 1280 by 720, dark and light, with ?static, ?t=20 and ?t=40; font sizes measured from computed style, with the SVG scale applied.

## Must-fix

1. The word "model" in the disc is under 20 px. The SVG has viewBox 560 by 520 shown at 470 by 436 (scale 0.84), and its text has font-size 20, so it renders at 16.8 px on the 1280 by 720 canvas. The checklist says nothing under 20 px. Fix: set the SVG text to about 24 in viewBox units (24 x 0.84 = 20.2), or make the viewBox match the box size (470 by 436) so 20 means 20. This is the only text under 20 px that I measured, in both themes.
2. The explainer states "Every text is 20 px or larger on the 1280 by 720 canvas." That is false until must-fix 1 is done. Fix the slide, then the sentence stays true.

## Should-fix

1. The still (?static, and everything from 34 s) no longer shows the arithmetic. The summary line is replaced at each step, so at the end it reads only "12 of 12 have no control", and "16 minus 4 = 12" and the shortfall sentence are gone from the final frame. The request says it must read as a still at the end. The headings (mandate granted 4, excess 12) and the struck-through send.endpoint.allowed row carry some of it, but the grant of 16 appears nowhere in the end state. Suggest a fixed second line, such as "Grant 16, mandate granted 4, excess 12", kept from 19 s on.
2. The shortfall marker is a dashed dot of radius 11 sitting on the core outline, next to a red dot, and it has no label on the disc. On a projector it reads as noise. Suggest a larger dashed ring or a short label (20 px or more) beside it.
3. The explainer's last paragraph says the run's row is in the ledger (/ruv-sgit/vaults.json). The ledger has no r5-e02-blast-radius row yet (r1 to r4 only). The conductor writes the row at close; check the link is not dead-ending before release. The paragraph also says "a builder and an editor", while the spec has three workers (v1, explainer, editor).
4. The slide's note and the page both write "A description, not a risk score." That is a negation and is allowed, but it puts the words "risk score" on screen; consider "No score or rating is given."
5. The data note for this example also says 8 of the rows are irreversible and the widest reach is "world"; neither is used. Not required, just a missed hook for the "damage reaches" sentence. The summary line at the end ("only nothing, a rule in prose, or a switch...") is long for the back of the room.
6. The dots are placed in three rings only (mandate, unstated, refused). "Placed by how far from what the agent is for" is true to the data (mandate_stance), but the ordering inside a ring is arbitrary, and the dots carry no barrier kind. Fine for v1; the explainer already says it.

## Checked and correct

- Numbers: grant 16, mandate 5, aligned 4, excess 12, unbounded_excess 12, shortfall 1, 0 of 22 rows measured, all match the file; the slide reads them from D at run time, none is typed in the HTML. The page and the explainer use 16, 4, 12, 5, 2, 10, 22, 0, 54, all in the file or counted from its 16 rows (2 unstated and 10 refused, matching the file's note).
- Shortfall arithmetic: 16 minus 4 = 12 is right, and the 16 minus 5 = 11 trap is explained in the explainer, as the file's note does. send.endpoint.allowed is not among the 16 rows, and the slide draws it as struck through, "asked, not granted".
- "12 of 12 excess rows have no control": the 12 excess rows (stance unstated or refused) have barrier_kind none (10), expectation (1, write.repository.tenant) and setting (1, grant.credential.self). In barrier_kinds only boundary has is_control true, and no row is boundary. So 12 of 12 holds. The slide's wording (nothing, a rule in prose, a switch its own account can flip) matches the file's definitions. execute.process.host (mandate) at setting is shown in the core list with its glyph.
- The 16 rows are all drawn: 4 core, 2 unstated, 10 refused, on screen as dots and as list rows, with grouping and glyphs from the file.
- No "measured" claim for the rows: the word appears only as "0 of 22 rows measured" and "not a measurement". No risk score or level, no logo (the text names the Claude Code CLI as the example, which the request asks for).
- "A published draft" is on screen in the bottom note, visible in the end state in both themes. Derived, 0 of 22 rows measured, is also there.
- Explainer frame times (0, 5, 13, 19, 27, 34 s, end at 54 s) match the code: dots 5 s on, core and mandate rows 13 s, excess 19 s, shortfall 27 s, barrier kinds when t is 34 or more, data-end 54. 54 s is inside the requested 40 to 60.
- Text sizes: every HTML text and every other SVG text measures 20 px or more (headline 40, summary 22, rows 20, note 20, kicker 20). Nothing overflows: the rows end at 623 and the note starts at 633 and ends at 708, and the summary, rows and disc do not overlap at 1280 wide.
- Both themes render cleanly (colours from the engine tokens; the red excess, the heading-colour core, one accent). Three colours of meaning at most.
- Console: no errors or page errors in 12 loads (?static, ?t=20, ?t=40, each dark and light).
- No em-dashes in the slide, the page or the explainer. No scripts or styles from another host; the page uses the engine's own slide.css and slide.js. The page and the explainer return 200 on the built site; the E01 link, the programme link (#e02 exists) and the data link resolve.
