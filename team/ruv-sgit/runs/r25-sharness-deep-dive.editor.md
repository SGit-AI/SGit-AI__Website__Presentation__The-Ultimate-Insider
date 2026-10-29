# r25-sharness-deep-dive: editor check

Verdict: fix first. Facts match the capture (hello storyboard probe "uid 0, all capabilities, no seccomp", exit 125, syscalls 444 to 446, 6/6 on 25 Oct vs 5/5 on 24 Oct, "not covered" list, Landlock and UDP, mTLS to fs/net/bash/llm, only net and llm to kms, "never returns a clear key", expiry 30 Oct). No em-dashes in the three files, no page errors, both themes legible, no text under 20px, no key, token, QR image, fingerprint or command (SH9 mentions "the QR" in words and "sha256:..." truncated only). SH9 is labelled designed throughout. One must-fix, in SH9 (agent colour used for a non-agent mover). 1 must, 8 should.

Panel question (SH8 builder): the capture's `without` field says "Panel 3" is the grant (root, all capabilities, NoNewPrivs 0, Seccomp 0). Its `steps` list puts it at step 2 of 7 (8 panels, so the list skips one). The explicit field wins: panel 3, not panel 2. SH8 names no panel number, so nothing to fix on the slide; if a panel number is ever added, write "panel 3".

## SH8: run-pipeline/v1 (diag-lit-run-pipeline, sb-hello-world-inside)
Must fix
none.
Should fix
1. The two lanes (PARENT, CHILD) are drawn from an article's description, not measured; only the hello result is measured. Fix: change the lane subtitles to "checks first, as sharness.ai describes it" and "walls close, then execve, as described", or add to the footer "Pipeline: described by sharness.ai, not run by us."
2. The WITH card header "WITH: measured, hello held" sits under the kernel line and can read as if the pipeline itself was measured. Fix: "WITH: measured result, hello held" and keep "6 of 6 on 25 Oct, one run, reported by the project (A2)".
3. Without card: add "storyboard panel 3" ("The probe, hello storyboard panel 3, 24 Oct 2026:") so the source is exact.
4. The "mismatch: exit 125, nothing runs" line sits 4px under the parent stations (y 260 vs boxes ending 256); lift the stations 8px or move the label to y 264.

## SH9: moving-parts/v1 (diag-moving-parts, diag-one-request)
Must fix
1. The travelling dot is drawn in --agent (pink), "the agent/its tool only", but from step 3 to step 6 it sits on net, kms and fs (one frame shows it inside net, another on kms). This says the agent reaches kms and breaks the colour rule and the slide's own point. Fix: keep the dot pink only on the app (steps 1, 2, 7); for steps 3 to 6 draw it in var(--head) (neutral) or var(--infra), and add the key "dot: where the request has got to" to the caption area or footer. Also move the app-step dot off the text (at t 20 it covers "The app" and "the agent" at 445,300): put it at 445,352 below the box text, or above the box at 445,246.
Should fix
1. Step 1 text "an image the agent cannot read as a key" and step 2 "read, not opened", step 5 "they never reach the app", step 6 "not readable by the agent" are our glosses of the design, not capture words (the capture: handover.png, sealed m1, "never a key" in the transcript). Fix: prefix each gloss "Our reading:" or change step 5 to "keys sealed to E, opened by net" and step 6 to "fs writes the tree and vault_key.sealed".
2. "Strict checks on the QR": the capture says "strict JSON checks on the QR"; say "strict JSON checks on the handover" to keep QR out of the page, no other change.
3. The dimmed non-active nodes (35% opacity) make the teal "never returns a clear key" and node labels low contrast in light and dark at t 20 and 30; raise the dim to .55.
4. The mTLS label sits on the fs line (x 545, y 244, rotated), tight against the line; shift 8px up.

## sharness-storyline.html, "deep dive, for parts 2 and 3"
Must fix
none. (Labels match: SH8 without observed, with measured; SH9 designed, not built; no command or injection reproduced; no em-dashes.)
Should fix
none.
