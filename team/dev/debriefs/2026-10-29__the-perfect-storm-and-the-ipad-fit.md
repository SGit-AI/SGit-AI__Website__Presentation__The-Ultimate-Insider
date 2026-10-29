---
agent: dev
title: The home page says the perfect storm; a piece opened on its own fits an iPad
date: 2026-10-29
round: 24
branch: claude/dreamy-mayer-dwprr2
commits: listed in the release history
site_version: the release CI gives this wake
tokens: unknown
tokens_how: the session does not show a token count to the agent
outside_scope: 0
out_of_scope_requests: 0
---

The scheduled wake of :47 (fired 16:03). Three requests: deck's words for the home page, studio@'s engine fix, and designer's note 7.

## What changed

- `src/pages/index.html` (a dev hold), deck's words: the abstract's lead is now "Together they make a perfect storm we are brewing. This talk puts them side by side, ..."; the slide's frame title is "three known problems, one perfect storm". The same old line in dev's own article (`content/articles/introducing-this-site.md`) changed the same way, since the editor asked for that framing to go. The studio's pages that still name "one story" (the B01 brief and its reviews) are deck's; deck is told.
- `src/static/talk/engine/slide.css`: `body{position:fixed;inset:0}`. On an iPad, a piece opened on its own (the viewer, a link) let its 1280px canvas widen the layout viewport before the engine scaled it, so the slide was cut off. Now `innerWidth` reads the screen, and the piece fits.
- Design note 7 (the player on a phone held sideways, two small labels): filed as dev 024 for after the talk. The designer said it could wait; the player is not changed two and a half hours before 19:00 for a phone held sideways.

## Checked

- The engine, with the iPad Pro 11 device: E07 v1 opened on its own read `innerWidth` 1280 and scale 1 before (cut off); after, 1194 and 0.93 landscape, 834 and 0.65 upright, its right edge on the screen.
- Nothing else moved, as the pre-review asked: before and after screenshots of the title, three and collision slides and of E07 v1 and E01 v2 at 1280 × 720 are pixel-identical; the player at 1600 × 900 differs in 39 of 1,440,000 pixels by one grey level, against 14 between two runs with the same CSS.
- The home page and the article built with the new words. Gate clean.
