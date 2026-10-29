# r23-stages editor review

Verdict: needs one fix. 8 of 9 pieces pass; e03/v1 has one stop after its change.

Checked: `git diff -- src/static/studio/lab` shows exactly one added `RUV_STEPS` line in each of the nine files and nothing else. Every list is ascending, every last stop is below `data-end` (e01: 48 and 52, e02: 54, 56 and 56, e03: 48, e04: 50 and 44, e09: 54), labels are short and plain, no em-dashes. Stops were compared with SLIDE_RENDER times and the five explainer frame tables.

## Must fix

None.

## Should fix

1. `src/static/studio/lab/e03/v1/index.html`: the last stop is at 42, but the end line appears at 41.7 (`end = T0 + 16 * STEP + .5`, T0 = 6, STEP = 2.2). Seeking to 42 lands after the change, not at or before it. Use 41.7, or 41.8 to stay clear of float rounding. Corrected line:
   `<script>window.RUV_STEPS = [{ t: 0, label: 'sixteen ways in' }, { t: 2, label: 'the ring' }, { t: 6, label: 'each source in turn' }, { t: 41.8, label: 'one agent' }]</script>`
   (Label note: at 41.8 the screen shows the end line "sixteen ways in, one agent"; 'one agent' stays, but the first label 'sixteen ways in' at t 0 matches the headline line, so both are fine.)
