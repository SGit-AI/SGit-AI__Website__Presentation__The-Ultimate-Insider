# Reality: what exists

What exists in this repository, kept current by whoever ships. A thing not listed here does not exist, whatever a brief or an article says.

Last updated 29 October 2026 (round 2) by dev@the-ultimate-insider. Each member keeps its own section; dev keeps the file as a whole.

## Site
- Static site built by `admin/build/build.py` (standard library only) into `_site/`; pages from `src/pages/`, articles from `content/articles/`, static files from `src/static/`.
- Pages: home, the talk (slide list), the script, the player, articles index and one article, sources, the brief, about and disclosure, releases, 404.
- Every page has a `.md` twin and JSON-LD; `llms.txt`, `sitemap.xml`, `robots.txt` and `version.txt` are generated.
- The version is in every top bar and in the player, linked to its entry in the release history; `pending` unless the build is CI's release commit.
- Release history generated from git: `/admin/versions.html`, `admin/versions/index.json`, one JSON per release.
- Pages: also `/admin/` (admin and engineering) and `/team/`, `/team/<id>/`, debriefs.

## Talk
- `src/static/talk/talk.json`: 17 beats, planned at 38 min 30 s; script is a first draft from the newsroom article, not rehearsed.
- 17 animated slides under `src/static/talk/slides/`, on one engine (`talk/engine/slide.js`, `slide.css`): seekable, pausable, reduced-motion aware.
- `talk/player.html`: keyboard player with a presenter view (`?presenter`) kept in step by BroadcastChannel.

## Release
- `.github/workflows/release.yml`: gate on every push; on `dev`/`main` one release job numbers, tags, builds and deploys to GitHub Pages. First release v0.1.0 on 29 October 2026, live at the-ultimate-insider.presentation.sgit.ai.
- `admin/build/agents.py`: scope check per member, overlaps (in the gate), unowned files.
- `admin/build/validate.py`: the gate (checks listed on /about/).

## Team
- `team/dev/`: dev@the-ultimate-insider, policy draft (not yet agreed by the editor). Holds the talk files for deck@.

## ruv.sgit (kept by ruv.sgit@the-ultimate-insider)
- `team/ruv-sgit/`: ruv.sgit@the-ultimate-insider, joined 29 October 2026 on the editor's request; policy draft (not yet agreed). Animations and infographics, each made in a run.
- `team/ruv-sgit/tools/ruvsgit.py`: the runner (open, deliver, close, seal, delete), adapted from SGit-AI__Website__Ruv; vaults on `dev.send.sgraph.ai`; the token and vault keys only in `~/.ruv-sgit-insider/` (0600), never in the repository. Ruflo 3.56.10 and sgit-ai 0.27.0, installed outside the repository by `ruvsgit.py setup`.
- Runs: `team/ruv-sgit/runs/<run>.spec.json` and `.evidence.json`; the ledger at `/ruv-sgit/vaults.json`. One run so far, r1-article.
- Article: `/articles/how-ruv-sgit-works.html`, including how members ask for an infographic.
- No infographic made yet; none is wired into the talk.

## Does not exist yet
- Members other than dev (deck@ is to be created by the editor); a board; schedules; a Stop hook.
- A `review/` folder.
- Confirmed demos for the demos slide.
