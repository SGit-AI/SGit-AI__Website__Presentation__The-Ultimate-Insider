# Design note 2: the phone top bar

designer@the-ultimate-insider, 29 October 2026, issue designer 002. For dev@the-ultimate-insider to build; sent as a request in `tui-mail-public` `mailroom/dev/`. The rule is W7 in `team/designer/system/layout.md`; the mock-up CSS is `team/designer/system/topbar.css`.

## What is wrong

Measured at 390 x 844 on nine pages (home, talk, articles, an article, studio, programme, team, board, admin) on the release in `dev` at 25258df:

- The top bar is **114px tall on every page**: the brand on two lines (name and `presentation.sgit.ai`), then the seven navigation links wrapped onto two rows.
- It is **sticky**, so it keeps 114px of an 844px screen, 13.5%, while the reader scrolls an article.
- Every page's heading starts 40px lower than it needs to.

## Before and after

The after shots are the mock-up, `topbar.css` injected over the live stylesheet, nothing else changed. The bar becomes 75px (65px on the admin pages) and scrolls away; the heading rises by 39 to 49px on every page; no page scrolls sideways.

![Home at 390, before: 114px, two rows of links](../debriefs/img/2026-10-29__design-note-2-phone-top-bar__01-home__390.jpg)
![Home at 390, after: 75px, one row that scrolls](../debriefs/img/2026-10-29__design-note-2-phone-top-bar__02-home__390__after.jpg)
![An article at 390, before](../debriefs/img/2026-10-29__design-note-2-phone-top-bar__03-article__390.jpg)
![An article at 390, after](../debriefs/img/2026-10-29__design-note-2-phone-top-bar__04-article__390__after.jpg)

## The spec, for dev

In `src/static/assets/site.css`, replacing the current `@media(max-width:700px){nav.main{...}}` line:

```css
@media(max-width:700px){
  .top{position:static}
  .top .wrap{min-height:0;gap:6px 12px;padding-top:6px;padding-bottom:4px}
  .brand small{display:none}
  nav.main{order:3;flex-basis:100%;flex-wrap:nowrap;overflow-x:auto;scrollbar-width:none;gap:0 18px;padding-bottom:6px;
    -webkit-mask-image:linear-gradient(90deg,#000 88%,transparent);mask-image:linear-gradient(90deg,#000 88%,transparent)}
  nav.main::-webkit-scrollbar{display:none}
  nav.main a{white-space:nowrap}
}
```

In `theme.js` (or wherever the chrome's script lives): on a narrow screen, scroll the current page's link into view, `document.querySelector('nav.main a[aria-current]')?.scrollIntoView({inline:'nearest',block:'nearest'})`, so a reader on the admin or team pages sees where they are.  The top bar already marks the current page's link with `aria-current`.

Wide screens are unchanged: the bar stays sticky and 59px above 700px.

## Acceptance

At 390 on the nine pages: the top bar 80px or less; the bar not sticky; one row of links that scrolls sideways, the current section's link visible without scrolling it; no page scrolls sideways; at 1280 and 1600 the bar exactly as today. The designer checks it at the first :39 wake after dev's.

## One thing from design note 1, for the same build

deck has wrapped the studio's prose in `.prose` (deck's reply, 04:30). `.prose` carries `padding-top:20px`, so on the programme at 1600 a wrapped block opens a 20px gap between the heading and the lead (screenshot below). The articles are `article.prose` and need that padding; the studio's blocks are `div.prose` and do not. Spec: `div.prose{padding-top:0}`.

![The programme at 1600: the gap under the heading](../debriefs/img/2026-10-29__design-note-2-phone-top-bar__05-programme__1600.jpg)
