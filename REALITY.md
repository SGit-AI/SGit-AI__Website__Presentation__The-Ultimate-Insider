# Reality: what exists

What exists in this repository, kept current by whoever ships. A thing not listed here does not exist, whatever a brief or an article says.

Last updated 29 October 2026 by dev@the-ultimate-insider.

## Site
- Static site built by `admin/build/build.py` (standard library only) into `_site/`; pages from `src/pages/`, articles from `content/articles/`, static files from `src/static/`.
- Pages: home, the talk (slide list), the script, the player, articles index and one article, sources, the brief, about and disclosure, releases, 404.
- Every page has a `.md` twin; `llms.txt`, `sitemap.xml`, `robots.txt` and `version.txt` are generated.

## Talk
- `src/static/talk/talk.json`: 17 beats, planned at 38 min 30 s; script is a first draft from the newsroom article, not rehearsed.
- 17 animated slides under `src/static/talk/slides/`, on one engine (`talk/engine/slide.js`, `slide.css`): seekable, pausable, reduced-motion aware.
- `talk/player.html`: keyboard player with a presenter view (`?presenter`) kept in step by BroadcastChannel.

## Release
- `.github/workflows/release.yml`: gate on every push; on `dev`/`main` one release job numbers, tags, builds and deploys to GitHub Pages. Not yet run: no release has happened.
- `admin/build/validate.py`: the gate (checks listed on /about/).

## Does not exist yet
- The agent team (roles beyond `team/dev/`, the board, schedules).
- A `review/` folder.
- Confirmed demos for the demos slide.
- The custom domain `the-ultimate-insider.presentation.sgit.ai` pointing at Pages (DNS and the Pages setting are outside this repository).
