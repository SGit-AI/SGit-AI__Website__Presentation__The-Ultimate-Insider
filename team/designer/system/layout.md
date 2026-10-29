# Layout rules: width

designer@the-ultimate-insider, 29 October 2026. Rules dev applies everywhere; a page that needs an exception says why in its own design note. Made from the design pass at 1600, 1280 and 390 (`team/designer/debriefs/2026-10-29__first-design-pass.md`). The CSS form, as mocked up and screenshotted, is `width.css` beside this file.

## The principle

**Wide where the reader scans, a measure where the reader reads.** Grids, tables, boards, dashboards, galleries and card lists take the whole frame; running prose never runs wider than a comfortable line. Width is decided by what a block is, not by which page it is on, so one page can hold both.

## Tokens

| Token | Value | What it is |
|---|---|---|
| `--gutter` | `clamp(16px, 3vw, 48px)` | the side margin of every frame: 16 on a phone, 48 on a wide screen |
| `--frame` | `1920px` | the widest any frame goes; below it, the frame is the viewport minus two gutters |
| `--measure` | `68ch` | the longest line of running prose (about 640 to 700px at 17px) |
| `--card-min` | `360px` | the narrowest a card in a card grid gets before the grid drops a column |
| `--thumb-min` | `280px` | the same for slide thumbnails and image tiles |

They live in `src/static/assets/tokens.css` (dev's), beside the colour tokens.

## The rules

1. **W1. One frame for every page.** `.wrap` is `max-width: var(--frame); padding: 0 var(--gutter)`. The 1140px cap goes. The top bar and the footer use the same frame on every page, so the brand and the navigation never jump between a public page and an admin page.
2. **W2. The reading measure is per block.** `.lead`, and `p`, `li`, `blockquote` and `dl` inside `.prose`, get `max-width: var(--measure)`. A page made mostly of prose (an article, the script, a brief, a debrief) keeps a reading column: `.narrow` is `max-width: calc(var(--measure) + 2 * var(--gutter))`, centred. Prose on a wide page (the programme's lists, the studio's explainers, the admin docs) is wrapped in `.prose` so it gets the measure while its grids do not. The admin section's `95ch` becomes `var(--measure)`.
3. **W3. Lists of things are grids, not stacks.** A list of cards fills the frame in columns: `grid-template-columns: repeat(auto-fill, minmax(min(100%, var(--card-min)), 1fr))`. Applies to `.cards` (the articles index, the team, the studio's briefs and reviews, the release history when it is cards). Slide thumbnails and galleries do the same with `--thumb-min`. One column on a phone falls out of the `min(100%, ...)` with no media query.
4. **W4. Tables and boards go to the edge of the frame**, inside a horizontal scroller (`.tbl`) on a narrow screen; never squeezed until a column wraps a word per line. The board keeps its three columns from 861px up.
5. **W5. Inside the admin shell, the main column is a frame.** `.shell-main .narrow` loses its cap (the side navigation already takes the left 250px); prose in it still gets the measure (W2).
6. **W6. On a phone, content comes first.** Under 861px the admin side navigation starts closed (`<details>` without `open`, the summary "Admin menu" visible), so the first screen of every admin and team page is the page, not the menu.

## Where each part of the site stands

| Part | Width | Why |
|---|---|---|
| Home | frame | a hero beside a figure, then three cards and a grid |
| Talk index | frame | 17 slide thumbnails: a gallery |
| Script | reading column | a document read top to bottom |
| Articles index | frame, card grid | a list scanned for one title |
| An article | reading column, centred | prose; figures may break out to the frame later (a later note) |
| Studio, programme, briefs, reviews | frame; prose blocks at the measure | a mix: loops and queues are grids, explanations are prose |
| Team, a member page | frame (in the shell), card grid | cards and tables |
| Board, schedule, wakes, commits, releases, keys, vaults | frame (in the shell) | dashboards and tables |
| Admin docs (rules, reality, wake protocol) | shell frame, prose at the measure | documents |

## Checking it

Every page at 1600, 1280 and 390: no line of prose longer than the measure, no horizontal scroll of the page, no card grid with one column above 800px, and on a phone the page's heading on the first screen.

## The top bar (design note 2, 29 October 2026)

7. **W7. On a phone the top bar gives the screen back.** Under 701px: one row for the brand, the version and the theme switch (the `presentation.sgit.ai` line hidden), one row of navigation that scrolls sideways with a fade at its right edge, and the bar scrolls away with the page (`position: static`) instead of staying. About 75px, once, instead of 114px on every screen. The current page's link is scrolled into view. CSS form: `topbar.css` beside this file.

## Type

The type scale and its rules (T1 to T5) are in `type.md` beside this file (design note 3).
