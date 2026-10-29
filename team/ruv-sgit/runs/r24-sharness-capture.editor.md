# r24-sharness-capture: editor check

Verdict: fix first. Facts and numbers match the capture (6 of 6, 25 Oct 2026, 28.5 s / 32.2 s, cloud 58 to 96 s, plan for up to 90 s, Linux 6.18.58, Landlock ABI 7, 512 MiB, hash prefix e619092574cc31d0, 201/403/200 verdicts), no em-dashes in any file, no text under 20px, no page errors, both themes legible, no secret, key, QR or command anywhere (SH6 shows only "[ vault key, redacted ]"; the injection is described in words, never quoted). Moves 1, 2 and 5 are labelled as our framing, 90 s and the SH5 fallback are in. Four must-fixes (one wrong claim, one colour-budget break, one wrong endpoint, one unreadable end state). 4 must, 19 should.

## SH1 v2: without-with/v2 (playground-interceptor)
Must fix
1. The DNS leak is drawn to "the internet" (dashed line ends at x 1190). The capture says the DNS query "still does" reach the page, not the internet. Fix: end the dashed path and the ring at CX[2] (the page's fetch(), x 900) and move the "DNS, UDP" label to sit above that end; the row-3 text stays "The DNS query still leaks: Landlock does not see UDP." Add "to the page" if room.
Should fix
1. Row 2 ("off the allowlist", 403) is labelled the same as the others; it is the page's own list, not the kernel, and not the "no policy vs under a policy" contrast. Set its `sub` to "the page's own list, read from its script" so it is not mistaken for a kernel result.
2. The end line says "both measured" while the caveat below says the capture only read the page's HTML and script. Reword the bold line to "Without and with, as sharness.ai reports its own runs." and keep the caveat.
3. "Permission denied (EACCES)": the capture says "Permission denied from the kernel"; EACCES is our inference (hello reports Errno 13). Use "Permission denied from the kernel, before any TCP packet leaves."
4. Row 1 and row 4 both end on a red line and a red dot at "the internet": the agent colour is used for "the request", good, but add a one-line key under the headers ("red: the request, teal: a wall, purple: the leak") or the teal/purple meaning is only in the prose.

## SH4: one-idea/v1 (anim-one-idea)
Must fix
none.
Should fix
1. "the wall" above the right column is our label for "the kernel says no"; the capture's picture has no wall. Fine, but add "(drawn by us)" to "the wall" or to the source line: "wall drawn by us".
2. Footer says "As sharness.ai draws it: only the with state." Good; add "no without is drawn or implied here, apart from the tricked agent in the quote" only if room, else leave.

## SH5: kernel-in-a-tab/v1 (anim-kernel-in-a-tab, anim-hello-replay, browser_linux)
Must fix
none. (28.5 s, 32.2 s, 58 to 96 s, plan for up to 90 s, six probes, one allowed and five refused, Errno 13 on net, MemoryError, "nothing ran" all match; fallback status is stated in the kicker.)
Should fix
1. "one run, the editor's Chrome (measured)": the capture grades this "self-reported by the project, one run, browser and machine not recorded". Fix: "one run in the editor's Chrome, reported by the project (A2)".
2. The replay's clock (28 s for hello) is the animation's 14 s loop stretched by us; say "replay, not a live clock" in the kicker: "a replay (drawn by us from the capture), the offline fallback".
3. The timeline label row (y 612) and the footer (y 632) are 8px apart: nothing overlaps but it is cramped; lift the timeline by 12px or drop "Source:" to a fourth line.

## SH6: last-metre/v1 (sb-the-last-metre)
Must fix
1. Four colours of meaning: agent (pink), infra (yellow, key service and its arrow), accent (teal, the wall and "never holds"), risk (purple, the observed link, the threat and the redaction boxes). The rule is at most three. Fix: draw the key service border and the return arrow `#aR2` in var(--head)/var(--dim) (neutral), keep agent, risk and accent.
Should fix
1. Headline "Even with a harness, the key is in reach" is ours: the capture's observation is the comic's panel 3 (a key lands in the clear after a clone in sgit 0.24.0). Fix: "Today the key arrives in the clear, where the agent can read it." or add "(our framing)" to the kicker.
2. "The threat: an injected instruction asks the agent to print its key. It can." is our inference joined to a different comic's scripted injection. Fix: label "Our reading:" instead of "The threat:" and end "...print its key. Nothing stops it in this panel." Keep it in words only, as now.
3. The teal wall bar in the DESIGNED column reads as "a wall that holds" but the column says no running code. Add a label under it, "designed wall", and draw it dashed.
4. The agent's request line crosses the wall bar to the key service; add "asks, never receives the key" or move the bar to the return arrow only, so the picture does not say the request is blocked.

## SH7: os-of-one-process/v1 (anim-os-of-one-process, diag-lit-what-held)
Must fix
1. Wrong claim in the opening frame (t < 2.5): "Without the harness it has nothing to reach: no filesystem to write, no network stack, no key, no shell, no model API." The capture says the process box lists what it lacks UNDER the harness; "without" is not drawn. This inverts the claim. Fix: "Under the harness it has no filesystem to write, no network stack, no key, no shell, no model API of its own. (The page lists these; the without is not drawn.)"
2. The end state (the known weak spot) is unreadable as evidence: five codes (403, 403, 201, 200, 200) and EACCES, plus an unlabelled ring on the kms line, float with no request attached. Fix: label each mark with its request and make the labels part of the end state: right of each door, at x 740: "201 PUT files/src/main.py", "403 PUT files/.sg_vault/key", "200 GET api.github.com" (above the dashed line to the network, from x 760), "403 GET pastebin.com/raw", "200 POST /v1/messages", at the kms line "sealed: unwrap(op=read)", and at the wall "EACCES: connect(1.1.1.1:443) direct". Move the two 403s from x 440 (left of the doors) to the right of the doors too, so every verdict reads left to right next to its request. Keep the codes in yellow (pass) and teal (stop); add the legend "ring: passed a door, bar: stopped" to the footer.
Should fix
1. The "201" label touches its ring (ring at x 730, label at x 740): move the label to x 756. The kms ring (800, 325) overlaps the "sharness.kms" title edge: move the ring to the box edge at x 800 minus 14, or shift the title to x 828.
2. During request 5 the red dot sits on the text "sharness.llm" (visible in the t=20 frame); stop the dot at the door's left edge (x 500) and let the ring show the pass.
3. "the kernel locks: measured" over the process box: add "(applied to a child, hello 6 of 6)" or shorten the box label to "kernel locks: measured, for a child", so the measured tag is not read as covering the doors beside it (the doors are labelled runnable MVP or designed, which is right).

## Storyline: src/pages/ruv-sgit/sharness-storyline.html
Must fix
none. Moves 1, 2 and 5 are labelled as our framing; move 4 carries "plan for up to 90 s" and the SH5 fallback; the 28.5 s, 58 to 96 s and "a minute or two" figures match; "twelve of twelve excess with no control" is on the E09 explainer, so the r22 query is closed; the injection note names no command.
Should fix
1. Move 3 says "a tricked agent asks for more and the kernel says no" as a fact of the animation, then "the OS of one process, SH7". Add after SH7: "(verdicts are the design's; fs and net are runnable MVPs; only the kernel half is measured)" so the storyline carries the capture's own caution.
2. Move 6 says "a key service that holds it ... is designed, not built (SH6)" (right) but says nothing about SH6 being observed only for panel 3; add "(observed in panel 3 only)".
3. Move 4 should add that the 28.5 s is one run reported by the project, browser and machine not recorded.
