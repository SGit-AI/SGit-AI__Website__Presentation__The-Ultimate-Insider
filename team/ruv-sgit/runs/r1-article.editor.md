# r1-article: the editor's check

Article checked: `content/articles/how-ruv-sgit-works.md` (line numbers below are the article's). Sources: the ruv.sgit repository at 47b4475 (`REF` below = the read-only clone), this run's spec, `team/ruv-sgit/tools/ruvsgit.py`, this site's `admin/build/validate.py` and `src/static/talk/engine/slide.js`. Ledger totals were recomputed with a short python script over `REF/site/data/vaults.json`. The article has no em-dash (U+2014): 0 found.

## Must-fix

1. **"every slide Dinis asked for was made by a ruv.sgit run"** (line 8, abstract). Overstates. Of the 26 beats in `REF/site/talk/talk-10.json`, 14 were made in runs and 7 are studio animations from studio run 1, which was not a ruv.sgit run (no vault was created: `REF/site/articles/src/the-studio.md:101`, "No vault was pushed"). The other 5 (beat `stack`, the AI image; `table`; `opensource`; `newsroom`; `thanks`) were made by the conductor. `REF/site/articles/src/how-it-was-made.md:239` says so: "Not every change was a run. The player, clock.js, the offline mode, the newsroom and open-source stills, and many fixes were made by the conductor directly". Suggested: "most of the slides Dinis asked for were made in ruv.sgit runs".

2. **"The talk's last slides showed the ledger of the runs that had made the slides before them"** (line 17). In `talk-10.json` the ledger is beat 17 of 26 and "ruv.sgit in motion" is beat 16. Nine beats follow them (city, table, services, shop, ask, visit, opensource, newsroom, thanks), and several of those (services, shop, ask, visit) were themselves made in runs. The source says only "Slides built by ruv.sgit runs show the ledger of those same runs" (`how-it-was-made.md:12`). Suggested: "Some of the talk's slides showed the ledger of the runs that had made them and the slides around them."

3. **"r6 made five slides at once"** (line 57). It was six. `REF/poc/ruv-sgit/runs/r6-talk.spec.json` lists five workers but six slides (ruvector, history, ledger, services, shop and visit; the shop worker made two). `how-it-was-made.md:37` ("Run r6 (six slides)") and `:123` ("made six slides") agree. The confusion is with the worker count: r6 had five workers.

4. **"Each run's spec quoted the feedback that started it, word for word"** (line 57), and "the spec, quoting the request word for word" (line 32, said of ruv.sgit's practice). At ruv.sgit.ai the specs paraphrase or summarise the feedback. For example, `r2-materials.spec.json` "feedback" is "Dinis, 15 Oct 2026: add a lot more animations and explanations; every change made by a ruv.sgit run (...)". The 13:18 message itself (`how-it-was-made.md:84`) reads differently. `r6-talk.spec.json` is written in the third person ("Dinis, reading the presentation: slide 4 should show ..."). The source says only "a spec that quotes his feedback" (`how-it-was-made.md:175`). Suggested: "Each run's spec recorded the feedback that started it." Keep "word for word" for this site, where r1-article's spec does quote the request verbatim (minus the redacted key).

5. **"The token and every vault key ... reach sgit on stdin"** (line 83). Not true of the token. This site's runner passes the server token on the command line as `sgit --token <token> ...` (`team/ruv-sgit/tools/ruvsgit.py:84`, on every sgit call), so it shows up in the process list while each call runs. Vault keys and read keys do go on stdin (`ruvsgit.py:181, 236, 260`). The runner's own header (`ruvsgit.py:15`), `ROLE.md` ("go to sgit on stdin") and `policy.json` (authenticate-as: "passed on stdin") make the same claim. Either change the article to "vault keys reach sgit on stdin; the token is passed as an argument and never printed", or have the runner pass the token another way, if sgit 0.27.0 allows it, and keep the sentence. (The runner is outside this worker's output; flagged here for the owner, ruv.sgit@.)

6. **"Then a new vault, with the spec and the request committed as its first commit"** (line 40), and "a vault on dev.send.sgraph.ai whose first commit is the spec quoting the editor's request" (line 87). The first commit is sgit's empty `init`. The brief is the second commit. Run r1-article's vault history (read with `sgit history log --json` in the run's working copy) shows `init` (01:04:28Z, 0 files) and then `brief: run r1-article` (01:04:31Z, 2 files). Every ruv.sgit ledger row shows the same pattern, for example smoke-1's history is `init`, `brief: run smoke-1`, ... (`REF/site/data/vaults.json`). Suggested: "the spec and the request committed as the vault's first content".

7. **"Everything a run here makes ends up public anyway, so the natural ending is a seal"** (line 85), together with the r1-article paragraph (line 87), which never says how this run ends. The run's own spec says this vault cannot be sealed: "The copy committed to the run vault at open still held it [the access key], so this run vault must end deleted, never sealed" (`team/ruv-sgit/runs/r1-article.spec.json`, `request.notes`). `ROLE.md` records the same rule ("that vault can only be deleted"). As written, the article invites a seal of the one vault that must never be published. Add one sentence to the r1-article paragraph: "Its vault will end deleted, not sealed: the request committed at open still held the access key." Soften line 85 too ("Most of what a run here makes ends up public").

## Should-fix

1. **"19.9 MB delivered"** (line 16). 19,954,075 bytes is 19.95 MB (decimal), which rounds to 20.0 MB, or 19.0 MiB. "19.9" truncates rather than rounds. Use "about 20 MB" or "19.95 MB".

2. **"423 files ... 19,954,075 bytes" (lines 16, 65).** Both are correct as sums of `files_delivered` and `bytes_delivered`. They leave out smoke-1, which has neither field (its vault holds 3 files, 285 bytes). This is the same convention as `how-it-was-made.md:191`. A footnote would let a reader reproduce the numbers: "sum of files_delivered over the 26 runs that record it". Summing `files` gives 478 and summing `bytes_plain` gives 20,001,624, because those include each brief.

3. **"4 sealed as public examples"** (line 61), and "only the sealed examples were pushed to dev.send.sgraph.ai" (line 83). Of the 4 sealed rows, 2 (example-01-hello, r14-examples) were sealed as static folders in the repository, never pushed to dev.send.sgraph.ai. They were later removed and `superseded_by` example-01-hello-v2 and example-07-meta, which are the two on dev.send.sgraph.ai (`vaults.json`, fields `superseded_by`, `static_copy_removed`, `published.server`). Suggested: "4 sealed (2 of them republished on dev.send.sgraph.ai as the public examples)".

4. **"take text fragments from the delivered files and search for each in every byte of the encrypted store"** (line 42). Both runners take the fragments from every file in the vault, the brief included: ruv's `close()` iterates over all of `R.vault` (`REF/poc/ruv-sgit/ruvsgit.py:147-157`), and this site's takes 8 per file over all files (`ruvsgit.py:173-175`). On this site the probe searches the encrypted store of the run's local working copy (`.sg_vault/bare`, `ruvsgit.py:176-178`), not the server's. The server side is covered by comparing a fresh clone's store with it (`store_identical`, `ruvsgit.py:183`). Line 32 ("what the server could see (ciphertext only, probed)") and the "What changes" list should say so, because at ruv.sgit.ai the probe read the server's own disk store (`REF/poc/ruv-sgit/ruvsgit.py:150`).

5. **"its tamper check, which ruv.sgit never worked around"** (line 40). The studio did route around it, by giving every run a fresh folder rather than reusing the path (`the-studio.md:100`: "The fix was not to remove the anchor but to give every run its own folder"). "Never disabled" or "never removed" is exact. "Never worked around" invites the objection.

6. **The ledger link and the evidence file** (lines 18, 87). `src/static/ruv-sgit/vaults.json` and `team/ruv-sgit/runs/r1-article.evidence.json` do not exist yet. Only `close` writes them (`ruvsgit.py:205-213`). Until then `validate.py` `check_links` fails on `../ruv-sgit/vaults.json`, and line 87's "written when the run closed" is not yet true. Close the run before the build and release.

7. **"The token ... live[s] in the runner's home folder"** (line 83). The runner also accepts the token from the environment, `RUVSGIT_TOKEN` (`ruvsgit.py:52`). In this session `~/.ruv-sgit-insider/server.token` is 3 bytes long, so the token in use probably came from the environment. Owner to confirm. If so, say "in the runner's home folder (0600) or its environment".

8. **What a reader cannot check.** The 13:18 quote, the message counts (30 messages, 24 of 30) and the "nine minutes later" timing rest on the session's message export, which is not public. `how-it-was-made.md:22` says the export is "one export of the session", and the articles quote it. Attribute these explicitly to [How it was made](https://ruv.sgit.ai/articles/how-it-was-made.html) at the point of use (line 55 and line 70), as line 51 does for the timeline. The r1-article figures (two workers, Ruflo 3.56.10, the vault on dev.send.sgraph.ai) can only be checked once the evidence file is committed. Also check that the repository link `github.com/SGit-AI/SGit-AI__Website__Ruv` is public. If it is not, readers cannot follow the "Where this comes from" section.

9. **"the server holds ciphertext under opaque ids"** (line 23). No source in the ruv repository was found for "opaque ids". The rest of that sentence is in `REF/docs/01-sgit-cheatsheet.md:3` ("encrypted client-side (AES-256-GCM) ... the server stores ciphertext only. The vault key ... is the one secret; there is no reset"). Cite that, or drop "under opaque ids".

10. **Quote insertion** (line 55). In the source, the bracket "[ruv.sgit]" follows the first "roof.sgit" ("a run of our roof.sgit [ruv.sgit] solution"), not the one the article quotes. Inserting it at the second occurrence is a fair editorial gloss, but it is not in the source at that point. Acceptable as is, or move the gloss outside the quote.

## Checked and correct

Ledger totals, recomputed over `REF/site/data/vaults.json` (27 rows, updated 2026-10-21T13:42:30Z):
- 27 runs: 23 with `deleted_at`, 4 with `sealed_at`. Created 2026-10-15T13:23:03Z, last closed 2026-10-21T13:42:29Z, so "15 to 21 October" holds.
- 68 worker entries; 7,347,535 worker tokens (sum of `workers[].tokens`).
- 311 Ruflo calls (`hive.ruflo_calls`); 129 vault commits; 75 branches.
- 423 files and 19,954,075 bytes delivered (`files_delivered`, `bytes_delivered`).
- 0 plaintext hits; 1,010 fragments probed (40 each for 24 runs, plus 3 + 18 + 29 for smoke-1, example-01-hello and example-01-hello-v2).
- 27 of 27 clones identical.
- 22 deletes with `delete_check.clone_after_delete == "failed"` (smoke-1 is the 23rd delete and has no check).

The talk:
- "Fourteen of the talk's slides were made in runs, beside the seven studio animations" (lines 16, 57). Of the 26 main beats in `talk-10.json`, 14 came from runs: r3 (equation, layers), r7 (claim, stack), r6 (ruvector, history, ledger, services, shop, visit), r8 (sgit, abp), r9 (ask) and r2 (motion). Seven beats are studio v1 to v7. The extra beat "case" (r2) would make 15 if extras counted.
- The event, "Agentic Engineering Live: rUv in London, 15 Oct 2026", and the title, "Autonomy with a mandate and a memory": `talk-10.json` header.
- "By the talk, eight runs had answered his feedback": r2 to r9 (`how-it-was-made.md:175`).
- What each run made:
  - r2: the ledger page, the case study, "ruv.sgit in motion" (`r2-materials.spec.json`).
  - r3: "the definition three ways" (`r3-define.spec.json`).
  - r7: "four lines of text" (`r7-claim.spec.json`).
  - r8: "between two slides he liked" (`r8-explain.spec.json`: "the RuVector slide and the layers slide are brilliant; what is missing between them").

The timeline and the quotes:
- At 13:18, the quote's words (`how-it-was-made.md:84`).
- "Nine minutes later ... smoke-1 were committed": commit at 2026-10-15T13:27:14Z, "ruv.sgit runner ... with its first measured run" (`git log` in REF). smoke-1 ran 13:23:03 to 13:23:39.
- "30 messages ... 28 releases ... 24 of the 30" (`how-it-was-made.md:11, 173-174`).

The studio (`the-studio.md:2, 79, 87, 90, 91`; `evidence/poc7-trace.jsonl`; `evidence/poc7-builders.json`):
- A queen and eight SG/Send roles, with the names as listed.
- Seven versions, ending in a three.js city: "a street per branch, a floor per commit".
- 31 Ruflo calls, all `rc` 0, 15,313 ms in total.
- Seven builders: 284 to 560 s each (4 min 44 s to 9 min 20 s), 629,857 tokens.
- "one HTML file that read its numbers from the site's data at load time" (`the-studio.md:69`).

Findings and limits:
- The memory finding: `memory -a set` printed OK, then "Key not found" (Ruflo 3.56.10), so results went back as broadcasts (`how-it-was-made.md:66`, `the-studio.md:99`).
- The r2 editor found "nothing is left to decrypt" unchecked, and `delete_check` exists from r2 on (`how-it-was-made.md:101`).
- `policy-anchor-log-missing` and `~/.config/ruflo/policy-trust/` (`the-studio.md:100`).
- `hive-mind work` and `spawn --claude` skip permission prompts by default (`studio-setup-brief.md:95`).
- The POC policy: 11 actions, 4 denied, 2 held (`REF/evidence/poc1-report.md`).
- "Token counts are the workers' only"; "the probe is a sample" (`how-it-was-made.md:237-238`).

The runners:
- ruv.sgit's runner steps: init hierarchical-mesh/byzantine; one spawn per worker; one task per worker; the purpose broadcast; a `w-<worker>` branch committed and pushed, merged into `current` and pushed again; a broadcast with a sha256; history, files and bytes; the probe; a fresh clone compared; the ledger. Seal: read key, a read-only clone identical, a write refused, the key destroyed. Delete: then a clone with the key fails. All in `REF/poc/ruv-sgit/ruvsgit.py:96-321`. This site's `ruvsgit.py:109-267` matches.
- "At ruv.sgit.ai each run's vault lived on a local vault server" (`vaults.json` `server`).
- This site's vaults are created on dev.send.sgraph.ai (`ruvsgit.py:32, 124`); key files are 0600 (`ruvsgit.py:42-48`).
- "seal only on the editor's go" (`ruvsgit.py:11`, `policy.json` `create.record.world`).
- Run r1-article: opened 2026-10-29T01:04:24Z; a hive with two workers (writer, editor), all 6 Ruflo calls `rc` 0 (run state); pins Ruflo 3.56.10, sgit-ai 0.27.0 (`ruvsgit.py:36`).

This site's rules:
- "This site's gate refuses any page that loads a script from another host" (`validate.py:108-112`, the `self-contained` check; it also refuses remote stylesheets).
- The engine: 1280 by 720 (`slide.js:27-28`); seek, pause and play by postMessage (`slide.js:56-62`); reduced motion shows the end (`slide.js:11, 73`); a light or dark theme (`slide.js:15`).
- How to ask: request path, ask shape, reading every member's folder each round (`team/ruv-sgit/ROLE.md`, "How to ask").
- `talk.json` and the slides are held by dev@ until deck@ joins (`team/dev/ROLE.md:16`, `team/dev/policy.json:42-47`).
- Repository at commit 47b4475, dated 2026-10-21 (`git log` in REF).
