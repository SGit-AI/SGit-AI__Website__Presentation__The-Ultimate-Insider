# Editor check, r9-e04-over-enthusiastic

Verdict: fix first (9 must fix, 7 should fix). Layout is clean: no overlaps, nothing under 20px, headline clear (bottom 97px, table top 112px), both themes legible, 50s, static shows the whole table, no em-dashes. Tiers and the do-not-draw exclusions are correct. The words need tightening to the file.

## Must fix

1. `src/static/studio/lab/e04/v1/index.html` SHORT pocketos fix: "used a stored, account-wide token" drops the correction. File: token stored locally, scoped to the whole account; "what proved to be" production. Fix: `'found a token stored locally, scoped to the whole account; deleted what proved to be production'` (shorten to fit two lines). Explainer bullet quotes the slide text, update it too.
2. index.html SHORT pocketos goal: drop of "(per the founder)". Fix: `'a routine task in staging (per the founder)'`.
3. index.html SHORT replit loss: "1,206 records" misstates the unit; file says records for 1,206 executives and 1,196+ companies (agent's own count). Fix: `"1,206 executives, 1,196+ companies (agent's count); recovered"`.
4. index.html SHORT meta loss: "unauthorised engineers saw data" says more than "visible to". Fix: `'data visible to unauthorised engineers, 2 hours'`.
5. index.html SHORT hf goal/fix: "OpenAI's models" drops that the attribution is OpenAI's, per press, not checked here. Fix the name cell to `"OpenAI's models (per press)"` or the in-way/fix text to carry it; the file field `agent` says attributed by OpenAI, per press.
6. index.html SHORT fourth-incident name: file says "an early version of Claude Opus 4.6". Fix: `'early Claude Opus 4.6'`.
7. index.html count "9 of 11": not honest as worded. It counts Meta's "(inferred)" obstacle and Codex's "needed a temporary folder" (not an obstacle in the file, OpenAI's account) as "something stood in its way", and the Irregular/Fourth rows as obstacles when the file says the environment limits "should have" held. Fix: either count only rows whose obstacle is not inferred and is an actual stop (then say the number from the code, e.g. "In 6 of the 11 the file names an obstacle; in 3 it is inferred or an account"), or reword the line to "In 9 of the 11 the file names something in its way (2 of those inferred or the vendor's account)". Keep `past` derived from a flag, and mark Codex "(OpenAI's account)" and OpenClaw "(reported)" in SHORT. Update the explainer 42 s row and last bullet to match.
8. explainer.html table row 10: the date is cut: "(2026 (d)". Fix: use the file's "(2026, disclosed 30 July)"; the generator is clipping at 8 chars of the date.
9. explainer.html "No blame. The slide names products, not people." is false: the Replit box prints "Lemkin: 'I lost 100 hours of time.'" and "his instruction". Fix: in the slide's Replit loss box, replace the file text with a version without the named user's quote (build the box from a short edited string, or strip the "Lemkin: ..." sentence in `esc(b[1])`), and keep the explainer sentence true; also check "his trial app" is fine (no blame, keep).

## Should fix

1. index.html: struck-through obstacle text is dim and hard to read in dark theme (the obstacle is the point). Fix: keep `color:var(--text)` on `.gone`, only the line-through in `var(--dim)`.
2. index.html SHORT openclaw obstacle: "(reported)" in the file is lost; `'its rule, dropped from its context (reported)'`.
3. index.html SHORT codex fix: "cleaned up the real home" reads as the agent's intent; file: "a cleanup command then deleted the real home directory". Fix: `'overrode $HOME; a cleanup command then deleted the real home'`.
4. index.html row tags "reported, 2026" shorter than the request's "reported, not checked against a primary" (full text only in the footer, after 15s). Fix: tag `'reported, unchecked'` at least, or put a thin tier label in the sep row.
5. index.html SHORT gemini loss: add "none recovered" (file). `'every file in the project folder; none recovered'`.
6. index.html SHORT pocketos loss: file says Railway restored the data. Fix: `'production data and backups; about 30 hours; restored'`.
7. index.html foot: bottom 10px leaves the second line touching the progress bar (baseline about 705). Fix `bottom:18px`.
