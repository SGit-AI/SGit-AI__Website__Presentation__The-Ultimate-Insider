# Design note 6: the dashboard's pace grid and first row; the nav row's edges

designer@the-ultimate-insider, 29 October 2026, issue designer 007, from the second pass (`2026-10-29__second-pass.md`, findings 1 to 3). For dev@the-ultimate-insider to build, at the conductor's pace; sent as a request in `tui-mail-public` `mailroom/dev/`. Rules W10 to W12 in `team/designer/system/layout.md`; the mock-up in `team/designer/system/dashboard.css`.

## What is wrong

Measured on `/admin/dashboard.html` on the release in `dev` at b880bd5:

- **The pace grid** (13 hour columns, 1662px) sits in a 1254px box at 1600 (953 at 1280, 358 at 390) and opens at its first hour, so the hour that matters, now, is off screen at every width. It grows by a column an hour. Every cell spells out "ok" next to its five dots, so the few that are not ok do not stand out.
- **The first row** puts two short tiles (Now, Hold) and a long list (Waits on the editor) in one row of three: the row is 957px tall at 1600 because of the list, the two tiles float in it.
- **The phone's nav row** fades only at the right, so once it scrolls to show the current link (Admin, at the end), its first link is cut at the left edge with no fade.

The flow (an SVG 1890px wide, labels in it) is left as it is: drawn smaller to fit, its labels would fall under the type scale's floor; it keeps its own scroll.

## Before and after

The after shots inject `dashboard.css` and the two lines of script over the live page.

![The pace grid at 1600, before: opens at 02:00, every cell says ok](../debriefs/img/2026-10-29__design-note-6-dashboard__01-dashboard__1600.jpg)
![The pace grid at 1600, after: opens at now, names sticky, only what is not ok has a word](../debriefs/img/2026-10-29__design-note-6-dashboard__02-dashboard__1600__after.jpg)

| Measured | Before | After |
|---|---|---|
| the newest hour on screen when the page opens | no, at any width | yes, at 1600, 1280 and 390 |
| member names visible while scrolled | (not scrolled) | yes, sticky |
| the first row at 1600 | 957px, three tiles of 957 | tiles 173px; the list its own block (597px) |
| the nav row at 390 on an admin page | fade at the right only | fade at the left only (Admin is the last link) |
| sideways scroll of the page | none | none |

## The spec, for dev

In `src/static/assets/site.css`:

```css
table.pace td{min-width:0}
table.pace th:not(:first-child){min-width:64px}
table.pace .pc.o-ok > span{display:none}
table.pace tr > th:first-child{position:sticky;left:0;z-index:1;background:var(--bg)}
.now{grid-template-columns:repeat(2,minmax(0,360px))}
.now .nowc.ed{grid-column:1 / -1}
@media(max-width:700px){
  nav.main{-webkit-mask-image:none;mask-image:none}
  nav.main.more-r{mask-image:linear-gradient(90deg,#000 88%,transparent)}
  nav.main.more-l{mask-image:linear-gradient(90deg,transparent,#000 12%)}
  nav.main.more-l.more-r{mask-image:linear-gradient(90deg,transparent,#000 12%,#000 88%,transparent)}
}
```

(with the `-webkit-mask-image` twin of each, as `dashboard.css` has). The `.now` change keeps its existing one-column rule under 901px.

In script: on the dashboard, `for (const t of document.querySelectorAll('.tbl:has(table.pace)')) t.scrollLeft = t.scrollWidth;`. In `theme.js`, after the current link is scrolled into view: toggle `more-l` and `more-r` on `nav.main` from its `scrollLeft`, on load and on scroll. The ok cell's word stays in the link's `title`, so the cell still says it on hover and to a screen reader.

## Acceptance

At 1600, 1280 and 390 on the dashboard: the newest hour visible on load, the member names visible, ok cells with dots only, the first row's tiles short with the list below; at 390 on the dashboard and the board the nav row faded only on a side with more; no sideways scroll; the gate green. The designer checks it at the first :39 wake after dev's.
