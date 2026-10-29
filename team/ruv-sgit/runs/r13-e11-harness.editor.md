# Editor check, r13-e11-harness, v1

Verdict: pass with fixes. No fact outside harness.json, no "platforms", no "24 to 29", no em-dashes, nothing designed shown as measured, no text under 20px, ID large, headline and ID clear, both themes legible, no overlap at the end (checked t=2,7,15,25,34,38 and ?static, dark and light). The explainer's times match the code (1.5, 3 to 6.5, 10 + 2.5 each, probes 21 to 33.5, 36, 40). One must fix, three should fix.

## Must fix

1. src/static/studio/lab/e11/v1/index.html, the still (t >= 40 and ?static): the end frame carries the caveat and the status line but no longer says "6 of 6 held on 25 October 2026, five environments, two kernels, uid 0" (that text is only at 36 to 40 s). The request wants the still to keep the cautions, and a viewer of ?static never sees the date. Fix: in the t >= 40 branch of `q`, lead with `'<b>' + B.held + ' of ' + B.n + ' held</b>, on 25 October 2026, in ' + B.envs + ' environments on two kernels, all uid 0. <b>The honest caveat:</b> a process cannot bind its own session; only a launcher above the agent makes the policy a boundary for the agent, and that launcher is designed.'` (keep it to two lines at 20px; shorten the second sentence if it wraps to three, the tiles start at 452 so there is room to y=170).

## Should fix

1. index.html, opening frame (0 to 40 s): the agent circle is stopped by the wall with nothing saying the policy is applied to a tool the agent starts, so for 40 s it reads as "the agent is contained", which the request forbids. Fix: change the label `'the agent'` to `'the agent, and the tool it starts'`, or add under the wall text `'(for a tool it starts)'`; at 20px keep it within x 20 to 300.
2. index.html, STEPS[0]: "what it may read, write, connect to and use" is loose; the request says files, ports, memory, processes, anything not named is denied. Fix: `['Write the policy', 'files, ports, memory, processes; anything not named is denied']`.
3. index.html, foot: "Runnable: fs and net (MVPs)" drops the file's own limit (a Setting until the launcher gives it its own uid). Fix: add `(Settings, not boundaries, until the launcher)` after "fs and net (MVPs)" if it fits two lines, else put it in the explainer's component table (already there) and say so.

Pages src/pages/ruv-sgit/harness/index.html and explainer.html: no change needed. (The explainer says the player clock is not in the repo; true, src/static/talk/engine holds only slide.css and slide.js.) If Must fix 1 or Should fix 1 to 2 change the slide text, update the explainer frame table rows for 36 s and 40 s to match.
