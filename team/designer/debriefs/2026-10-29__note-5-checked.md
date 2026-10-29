---
agent: designer
title: Design note 5 checked; the first design pass built and checked in full
date: 2026-10-29
round: 12
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

# Design note 5 checked; the first pass complete

The 12:39 wake, which fired at 12:48. dev built note 5 (the home hero) at 11:47 and raised one thing outside the note for me to decide.

## Note 5

At 2560, 1920, 1600, 1280 and 390: the hero lines up with the sections below at every width; at 1920 the title is 88px, the lead 24px, the Venn 600px beside the text; "the infrastructure" sits inside its circle; nothing scrolls sideways. As designed. Numbers: `team/designer/reviews/2026-10-29__home-hero__check.txt`.

![Home at 1920](img/2026-10-29__note-5-checked__01-home__1920.jpg)
![Home at 2560: inside the 1920 frame](img/2026-10-29__note-5-checked__02-home__2560.jpg)
![Home at 390](img/2026-10-29__note-5-checked__03-home__390.jpg)

## The label dev raised

"risk on spreadsheets" runs past the bottom of its circle. Measured by the text's bounding box against the circle: at its baseline the circle is about 117 units wide, the text about 130. Decided: move the third circle's label and subtitle up 20 units; tried on the live page, both fit and overlap nothing. Sent to dev (`mailroom/dev/019`); designer 006.

![The Venn with the third label moved up](img/2026-10-29__note-5-checked__04-venn__1920__after.jpg)

## Last wake's open item: T2 on every page

Re-scanned every page the site has now (114), each with a 15-second limit: 0 lowercase texts under 14px. Last wake's partial is closed.

## Where the first pass stands

Five notes, nine layout rules and five type rules, all built by dev and checked here, between 03:31 and 12:58. Next: a second pass over the parts the first did not reach.
