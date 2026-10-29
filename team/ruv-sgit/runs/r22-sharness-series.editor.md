# r22-sharness-series: editor check

Verdict: fix first. Facts match harness.json (6 of 6, 25 Oct 2026, 5 environments, two kernels, 28.5 s, launcher first slice 28 Oct), no em-dashes, no text under 20px, ID large, both themes legible, nothing overlapping at the end. Three must-fixes: one wrong fact on the storyline, one status mismatch in SH3, one "without" labelling gap in SH1. 3 must, 8 should.

## Storyline: src/pages/ruv-sgit/sharness-storyline.html
Must fix
1. Move 2 says the tool "writes outside its workspace". Probe 3 writes IN the workspace and probe 2 in /tmp. Fix: "writes a file in /tmp and in its workspace".
Should fix
1. Moves 2 and 5 state "without" outcomes ("nothing stands in the way", "paths that went through") as fact. Add "(drawn, not measured)" to both.
2. Move 1 cites "twelve of twelve excess with no control" from E09; it is not in harness.json. Mark "to check against E09" or drop.
3. Move 3 lists "processes" in the policy; harness.json names no process limit for hello (probes: files, port, hash, memory). Say "files, ports, memory" or check against the capture.
4. Move 6 should also name fs as a Setting and net as a Boundary only for the shell `sharness-ai shell` starts.

## SH1: without-with/v1/index.html
Must fix
1. "Without" is labelled not measured only in the footer from t=34. Fix: header `#phL` span becomes "no policy, not a measured row: what a process running as the account would do", visible from t=1; also keep it in the static frame.
Should fix
1. Left column is six full-width red lines plus purple results: a sea of red. Make lines 3px and let only the dot be var(--agent), or draw the "without" lines in var(--dim).
2. Wall has no label in the drawing: add "policy wall" under the first right-hand wall; the amber gate has none either ("allowed by policy").
3. "runs: nothing checks" and "connected" are asserted outcomes; use "no check" and "no rule" wording, or italicise as "would".
4. "refused at 128 MiB: held" ends at x 1246, past the 1240 margin: shorten to "refused: held" (cap is in the row label).

## SH2: live-demo/v1/index.html
Must fix
none (no invented output, hashes or timings; 28.5 s is read from harness.json).
Should fix
1. Dashed box "on screen: the policy it runs under, and its hash" asserts what the page shows, which the storyline admits is not in the capture. Reword "expect: the policy and its hash (to confirm against the capture)".
2. Card 4 "each verdict as it comes" and the six animated rows imply live streaming order; add "as drawn by E11" to the `#rhead` line.

## SH3: components/v1/index.html
Must fix
1. Legend "Runs, but a Setting: files and network" is wrong for net: harness.json says a Boundary only for the shell `sharness-ai shell` starts, a Setting otherwise. Fix: "Runs, but a Setting: files, until the launcher gives it its own uid; network a Boundary only for the shell sharness-ai shell starts."
Should fix
1. Keys (kms) carries a tick but reads "designed, not built": add "primitives measured" (freeze/thaw 0.13 and 0.28 ms) or drop the tick.
2. Network box should say "runnable MVP since 27 Oct; Boundary only for the shell, else a Setting", fs "a Setting" on its own line.
3. "A wall that holds: the policy around the tool" is fine, but add "for the child, held in 6 of 6 probes" so it is not read as protecting the agent; the caveat line already says the agent is not bound.
