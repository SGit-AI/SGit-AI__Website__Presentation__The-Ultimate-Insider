# Editor check: r20-e05-pivoting

Verdict: pass, no must-fix. Both cases, every hop and label match the files; nothing to_confirm on screen; no payload, no names; no em-dashes; all text 20 px or more, ID 72 px; both themes legible; no overlaps at the end (checked static, dark and light, and t=6/12/24); explainer times (3.6 s, every 2.6 s, 18.6 s, 28.2 s, 33 s, end 44 s) and RUV_STEPS (0, 3, 18, 28, 33) match the code.

## Must fix

None.

## Should fix

1. `src/static/studio/lab/e05/v1/index.html`, zone title `'the whole machine'`. The file says "to search the machine for secrets"; "whole" is added. Fix: `t: 'the machine'`; update the explainer's list of added words and the frame row to match.
2. `index.html` (slide), foot line "more cases are coming from the researcher". The programme says only "asked" (status asked); "coming" promises delivery. Fix: "more cases are asked of the researcher" (same in the page `index.html` note and `description`, "more cases are coming from the researcher", and in the explainer's 33 s row).
3. `index.html` (slide), gap box and foot are process talk on a slide ("the researcher is asked"). Fix: shorten the box to "Hops not stated in our files: left empty", keeping the researcher mention to the page.
4. Light theme: the amber `--infra` text ("a compromised release", "it ran on install", "pointed on purpose") is about 3.2:1 on the light background at 20 px semi-bold. Fix: add `[data-theme=light] .zs.infra{color:#9a6200}` (or the equivalent light-theme selector the engine uses) and draw the matching dots/paths with the same token.
5. `explainer.html`, "What was left out": it prints "about 30 organisations", which the file marks to_confirm. Not shown as fact, but the number is public once printed. Fix: "The number of organisations targeted: marked to confirm in the file, so not used" without the number.
6. Slide kicker (`.kk`, box 34 to 58 px) touches the headline box (starts at 56 px). Visually fine; nudge `.hl` to `top:60px` for a clear gap.
