# SGit-AI__Website__Presentation__The-Ultimate-Insider

Repo for **the-ultimate-insider.presentation.sgit.ai**: the site and the presentation for *The ultimate insider*, a talk by Dinis Cruz at hack::soho, IOActive London, 29 October 2026.

- Run locally: `./run-website-locally.sh`, then open http://localhost:8000 (the player is at `/talk/player.html`; press `P` for the presenter view, `?` for the keys).
- Release: push to `dev` (or merge to `main`). CI gates, numbers, tags, builds and deploys; see `.github/workflows/release.yml`. One-off setup: Settings, Pages, Source "GitHub Actions", and the custom domain.
- For agents: `CLAUDE.md`, then your folder in `team/<id>/`, `BRIEF.md`, `REALITY.md`. How it is built: `/admin/` on the site.
