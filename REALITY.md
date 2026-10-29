# Reality: what exists

What exists in this repository, kept current by whoever ships. A thing not listed here does not exist, whatever a brief or an article says.

Last updated 29 October 2026 by deck@the-ultimate-insider.

## Site
- Static site built by `admin/build/build.py` (standard library only) into `_site/`; pages from `src/pages/`, articles from `content/articles/`, static files from `src/static/`.
- Pages: home, the talk (slide list), the script, the player, articles index and one article, sources, the brief, about and disclosure, releases, 404.
- Every page has a `.md` twin; `llms.txt`, `sitemap.xml`, `robots.txt` and `version.txt` are generated.

## Talk
- `src/static/talk/talk.json`: 17 beats, planned at 38 min 30 s; script is a first draft from the newsroom article, not rehearsed.
- 17 animated slides under `src/static/talk/slides/`, on one engine (`talk/engine/slide.js`, `slide.css`): seekable, pausable, reduced-motion aware.
- `talk/player.html`: keyboard player with a presenter view (`?presenter`) kept in step by BroadcastChannel.

## Studio
- `src/pages/studio/`: the hub (loop, board, story map, shelves), how it works, techniques, and the briefs shelf with B01 (One story, not three) and B02 (The distance is a prompt), both open.
- `src/static/studio/data/incidents.json`: the five incidents of beat 5 with sources, for B02.
- `studio/lab/` is reserved for storyboards and versions and is empty; the gate treats its pages as standalone, like slides.
- No studio work has been promoted into the talk yet.

## Release
- `.github/workflows/release.yml`: gate on every push; on `dev`/`main` one release job numbers, tags, builds and deploys to GitHub Pages. Not yet run: no release has happened.
- `admin/build/validate.py`: the gate (checks listed on /about/).

## Team
- `team/dev/`: dev@the-ultimate-insider (site, build, gate, CI, player, slide engine).
- `team/deck/`: deck@the-ultimate-insider (the talk's beats, script, slide content, and the studio's briefs).
- ruv.sgit@the-ultimate-insider is being onboarded by the editor to build in the studio; it has no `team/` folder yet.

## Does not exist yet
- The rest of the agent team (further roles, the board, schedules).
- A `review/` folder.
- Confirmed demos for the demos slide.
- The custom domain `the-ultimate-insider.presentation.sgit.ai` pointing at Pages (DNS and the Pages setting are outside this repository).
