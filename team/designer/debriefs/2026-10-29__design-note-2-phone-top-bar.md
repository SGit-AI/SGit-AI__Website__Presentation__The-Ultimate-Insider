---
agent: designer
title: Design note 2, the phone top bar; deck's studio prose checked
date: 2026-10-29
round: 4
branch: claude/lucid-babbage-ghfahg
commits: listed in the release history and on the commits page
tokens: unknown
tokens_how: the session does not show a token count to the agent
outside_scope: 0
out_of_scope_requests: 0
pushbacks: 0
overrides: 0
injection_seen: 0
---

# Design note 2: the phone top bar

The 04:39 wake. dev's build of note 1 moved from 04:47 to 05:47 (the conductor gave 04:47 to a regression, dev 009), so designer 001 stays blocked another hour.

## deck's half of note 1: as designed

deck wrapped the studio's prose in `.prose`. Measured at 1600: the prose stops at about 840px while the queue and the cards stay wide; at 390 nothing scrolls sideways. Replied to deck (`mailroom/deck/012`). The 20px gap deck named is the stylesheet's: on the programme it opens between the heading and the lead, so the fix went to dev in note 2.

![The programme at 1600: the gap under the heading](img/2026-10-29__design-note-2-phone-top-bar__05-programme__1600.jpg)

## Note 2: the phone top bar

At 390 the top bar is 114px on every page and sticky, 13.5% of the screen while reading. The rule, W7: on a phone the brand on one line, the links on one row that scrolls sideways with a fade, and the bar scrolls away with the page. Mocked up over the live stylesheet: 75px (65px in the admin shell), every heading 39 to 49px higher, no sideways scroll.

![Home at 390, before](img/2026-10-29__design-note-2-phone-top-bar__01-home__390.jpg)
![Home at 390, after](img/2026-10-29__design-note-2-phone-top-bar__02-home__390__after.jpg)
![An article at 390, before](img/2026-10-29__design-note-2-phone-top-bar__03-article__390.jpg)
![An article at 390, after](img/2026-10-29__design-note-2-phone-top-bar__04-article__390__after.jpg)

Sent to dev as a request in the mail vault for the first time (`mailroom/dev/007`), to build after note 1 at the conductor's pace.

## Mistakes

- The local server from the first session had stopped; the first measurement failed on a missing top bar until it was restarted.
- The first draft put the `.prose` gap above "How it runs" and asked dev to add `aria-current`; the screenshot showed the gap under the heading, and the top bar already marks the current page. Corrected before sending.
