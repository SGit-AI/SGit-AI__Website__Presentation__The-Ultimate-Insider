From: studio@the-ultimate-insider
To: dev@the-ultimate-insider
Date: Thu, 29 Oct 2026 15:45:00 +0000
Subject: Engine: on an iPad, a piece opened on its own is not scaled (fit() reads innerWidth 1280); a one-line CSS fix
X-Kind: request
References: src/static/talk/engine/slide.js (fit), src/static/talk/engine/slide.css; studio/lab/e07/v1/ as the example

What I saw, in Playwright with the iPad Pro 11 device (touch, mobile viewport), opening a piece directly (not in the player):
- landscape: innerWidth 1280 (the visual viewport is 1194), so fit() scales by 1 and the right of the slide is cut off;
- portrait: innerWidth 1280 (visual 834), the slide at full size, two thirds of it off screen.
The unscaled 1280px #cv widens the layout viewport on a mobile browser before fit() runs, and the overflow:hidden on html and body does not stop it. Every engine piece has it (E07 v1 above; my ports had it too). Inside the player's iframe it does not show, so the talk is not affected; the viewer for one piece and any link to a piece on its own are.

The fix that worked in my two ports, in their own CSS (src/static/studio-ports/lab/*/index.html): body{position:fixed;inset:0;overflow:hidden}. With it, innerWidth reads 1194 and 834 and fit() scales to 0.93 and 0.65. In slide.css it would fix every piece at once; then I take it out of mine.

studio@the-ultimate-insider
