# Reality: what exists

What exists in this repository, kept current by whoever ships. A thing not listed here does not exist, whatever a brief or an article says.

Last updated 29 October 2026 by dev@the-ultimate-insider (round 3, carrying in conductor@, deck@ and ruv.sgit@), and by deck@the-ultimate-insider. Each member keeps its own section; dev keeps the file as a whole.

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

## Studio
- `src/pages/studio/`: the hub (loop, board, story map, shelves), how it works, techniques, and the briefs shelf with B01 (One story, not three) and B02 (The distance is a prompt), both open.
- `src/static/studio/data/incidents.json`: the five incidents of beat 5 with sources, for B02.
- `studio/lab/` is reserved for storyboards and versions and is empty; the gate treats its pages as standalone, like slides.
- No studio work has been promoted into the talk yet.

## Release
- `.github/workflows/release.yml`: gate on every push; on `dev`/`main` one release job numbers, tags, builds and deploys to GitHub Pages. First release v0.1.0 on 29 October 2026, live at the-ultimate-insider.presentation.sgit.ai.
- `admin/build/agents.py`: scope check per member, overlaps (in the gate), unowned files.
- `admin/build/validate.py`: the gate (checks listed on /about/).

## Team
- `team/dev/`: dev@the-ultimate-insider, policy draft (not yet agreed by the editor). Holds the talk files for deck@.
- `team/conductor/` (kept by conductor@the-ultimate-insider): policy draft, status, `schedule.json` (two runs, proposed, none scheduled), and the only published session key, `key.json` (`sha256:7047871c97407e2b`) with its QR image and session folder.
- `team/security/`, `team/researcher/`: proposed roles, policy marked proposed; no session holds either.
- Two public vaults on dev.send.sgraph.ai, created 29 October 2026: `tui-issues-public` (h9fh2apf, Issues-FS lite) and `tui-mail-public` (f9d5r3dp, Email-FS lite); read keys in `team/conductor/vaults.json` and on `/admin/keys.html#vaults`; vault keys sealed to the DC Vault Registry and in no file. No private vaults.
- `/admin/keys.html` and `admin/keys/index.json`: the key register, every member's current key; each member's page shows its own key.
- `admin/tools/banner.py`: the start and end banners every member's session report opens and closes with; the gate checks every `ROLE.md` carries the rule.
- `admin/tools/pki-agent.mjs`: pinned with its sha256, matched pki.sgit.ai on 29 October 2026; not yet read line by line.

- `team/deck/`: deck@the-ultimate-insider (the talk's beats, script, slide content, and the studio's briefs); `ROLE.md` only, no `policy.json` yet.

## ruv.sgit (kept by ruv.sgit@the-ultimate-insider)
- `team/ruv-sgit/`: ruv.sgit@the-ultimate-insider, joined 29 October 2026 on the editor's request; policy draft (not yet agreed). Animations and infographics, each made in a run.
- `team/ruv-sgit/tools/ruvsgit.py`: the runner (open, deliver, close, seal, delete), adapted from SGit-AI__Website__Ruv; vaults on `dev.send.sgraph.ai`; the token and vault keys only in `~/.ruv-sgit-insider/` (0600), never in the repository. Ruflo 3.56.10 and sgit-ai 0.27.0, installed outside the repository by `ruvsgit.py setup`.
- Runs: `team/ruv-sgit/runs/<run>.spec.json` and `.evidence.json`; the ledger at `/ruv-sgit/vaults.json`. One run so far, r1-article.
- Article: `/articles/how-ruv-sgit-works.html`, including how members ask for an infographic.
- No infographic made yet; none is wired into the talk.

## Does not exist yet
- `team/deck/policy.json`; keys for dev, deck, security and researcher; any scheduled task; a Stop hook.
- A `review/` folder.
- Confirmed demos for the demos slide.
