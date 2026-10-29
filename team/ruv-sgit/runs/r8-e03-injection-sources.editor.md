# Editor check, r8-e03-injection-sources

Verdict: fix then ship. Facts, counts (4/4/8), order table, lit-at times (6 + (n-1)*2.2), years, labels, impacts all match the data; no payload, no em-dashes, no in-the-wild overreach; the line under the headline is two lines for all 16 cases and the end line; both themes legible, still end state clean. Two cautions are missing, and one text is under 20px.

## Must fix

1. src/static/studio/lab/e03/v1/index.html, `.it i{... font:800 18px/24px ...}`: the list numbers are 18px, under the 20px floor. Change to `font:800 20px/24px`; widen `.it i` to `width:30px` if "10" to "16" crowd.
2. src/static/studio/lab/e03/v1/index.html (end line in SLIDE_RENDER) and src/pages/ruv-sgit/injection-sources/explainer.html (cautions bullets): the cautions "no public case of a code comment steering an agent was found; rules files and READMEs are the nearest" and "the code row is a pull request" are not kept anywhere. Add to the key (`#key`, 2 lines available) or the end line: "No case found of a code comment; the code row is a pull request." Add the same bullet to the explainer's "Where every word comes from" list.
3. Same files, case 14 (ClawHavoc): the data note says "holds in part: the words steered the users, not shown to steer the agent". The slide shows it as a steered-agent case with no qualifier. In the card, when `c.note` is non-empty, append ` · ` + `c.note` (use a short form: "holds in part: it steered the users, not shown to steer the agent"); check it stays within two lines (the card is 62px high; case 14 is 132 characters today, so it will be tight, drop "what it led to:" for that case if needed). Add the note to the explainer table row 14.

## Should fix

1. src/static/studio/lab/e03/v1/index.html: unlit nodes and their numbers sit at opacity .25 (`o.g.style.opacity = .25 + .75*k`); in dark the numbers 3 to 16 are hard to read before they light (dark-10.png). Raise the floor to .5 or keep the numbers at full opacity and fade only the dot.
2. src/pages/ruv-sgit/injection-sources/explainer.html, "Every text is 20 px or larger": true only after must-fix 1; keep it.
3. Explainer frames table: "6 s to 39 s" and "42 s". The last card runs to 41.7 s (6 + 16*2.2 + .5); write "6 s to 41.7 s" and "from 41.7 s" for exactness.
4. The card gives only the impact ("what it led to"); the request asks "what it read, what it then did". The source is named and the impact is the file's; consider adding `c.what_happened` is too long, so accept as is, or say so in the explainer's left-out list.
5. Key text breaks "vendor-" / "confirmed" across lines at the right edge; set `white-space:nowrap` on the `<b>` pieces or shorten to "vendor-confirmed (4)" on its own line.
