# The showcase slide: how to fill one

dev@the-ultimate-insider, 29 October 2026, for the conductor's request 030 (the editor's work section). A showcase is one part of one page: a screenshot, cropped, explained, with the article's title, its link and a QR of the link, in stages. The player steps through the stages like any slide.

## Make one

1. Copy `talk/engine/showcase-example/` to your own folder (studio@: `studio/lab/<id>/`; deck: `talk/slides/<id>/`) and fix the five relative paths to `slide.css`, `showcase.css`, `slide.js`, `qrcode.js` and `showcase.js`.
2. Put the screenshot beside it (`shot.jpg`, JPEG at quality 80 or so; a page at 1440 wide, as tall as the part you need). Write its size in pixels in `"size"`.
3. Edit the JSON in `<script id="showcase">`:
   - `kicker`, `title`, `text`: the line above the title, the title, one or two sentences on the right.
   - `link` and `source`: the page's address and its title. The QR is drawn from `link`, in the browser, by `qrcode.js`.
   - `stages`: one per step. `at` (seconds), `crop` `[x, y, width, height]` in screenshot pixels (the frame moves there over 1.2 s), `label` (the step's name in the player), `dim` (darken outside the first box), `callouts` (each a `box` `[x, y, width, height]` in screenshot pixels and its `text`; they are numbered in order across the slide).
   - `end`: the slide's length in seconds.
4. Open it on its own (`?t=4` freezes at 4 s) and in the viewer (`talk/engine/view.html?src=<path from the site root>`), then build and gate.

## The rule (the security pre-review, 16:3x)

**No screenshot captures a key**, a key's QR, a read key, a vault key, a token or anything private. pki.sgit.ai and the vault pages show keys: crop them out of the image itself before you commit it (a crop in the JSON is not enough: the whole image is published), or skip that page. The QR on the slide is of the public link only.

## How it works

`showcase.js` reads the JSON at `SLIDE_INIT`, builds the frame, the boxes, the list and the QR as ordinary slide elements with `data-in` times, and moves the frame between crops in `SLIDE_RENDER`. Its stages become `RUV_STEPS`, so the player's ← and → land on each one. Nothing in the player changes.
