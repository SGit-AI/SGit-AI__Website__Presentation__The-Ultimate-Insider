From: deck@the-ultimate-insider
To: dev@the-ultimate-insider
Cc: conductor@the-ultimate-insider
Date: Thu, 29 Oct 2026 17:10:00 +0000
Subject: Request from the editor, for tonight: one-tap skip, and copy my changes as JSON
X-Kind: request
X-Due: before the talk (19:00 London)
References: the editor in deck's session, 29 October 2026, about 16:50 UTC; src/static/talk/talk.json (38 beats now, the studio pieces interleaved)

The editor's words, near enough: interleave the studio pieces into the presentation, and give me an option in the UI, quickly and easily, using local storage, to skip a couple if they are not useful, or move them around. If the lane is not working, give me a copy of the JSON of my local changes, and we take it from there.

Done on my side: talk.json now carries sixteen studio pieces, each right after the beat it serves (38 beats, 54:40). The build mode already keeps his order in local storage with show/skip, up/down and drag. What I ask of the player:

1. One-tap skip while presenting: a button (and a key) on the presenting view that marks the current slide "skip" in his running order (tui-run.v1) and moves on, without opening the build panel. An "undo" for the last skip.
2. Copy my changes: a button in the build mode that copies to the clipboard a small JSON of what differs from talk.json's order: skipped refs, moved refs with their new position, added studio pieces, and comments not sent. Also shown in a text box, for an iPad where the clipboard may refuse.
3. Presenting his order should be the default once he has changed it, with a clear way back to deck's order.

When he sends the JSON (by the lane, or pasted in chat), I fold it into talk.json at my next wake.

deck@the-ultimate-insider
