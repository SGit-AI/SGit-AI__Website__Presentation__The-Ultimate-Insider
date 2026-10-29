# Type: the scale

designer@the-ultimate-insider, 29 October 2026, design note 3. Eight sizes for the whole site, as tokens beside the colours in `src/static/assets/tokens.css`. Every `font-size` (and the size in every `font:` shorthand) uses one of them; a size that is not on the scale is a bug.

| Token | Size | For |
|---|---|---|
| `--t-0` | `clamp(36px, 4.6vw, 88px)` | display: the home page's title only (raised from 64px by design note 5) |
| `--t-1` | `clamp(30px, 4.4vw, 48px)` | `h1` |
| `--t-2` | `clamp(22px, 2.6vw, 30px)` | `h2`, card and beat titles |
| `--t-l` | `20px` | `h3`, the lead, the abstract |
| `--t-body` | `17px` | running text, and the script's lines |
| `--t-ui` | `15px` | navigation, buttons, side navigation, notes, table text, card text |
| `--t-s` | `14px` | dense dashboards (commits, wakes), meta lines, chips, code in tables |
| `--t-xs` | `12px` | uppercase labels and kickers only: the floor; nothing smaller |

One exception, figures: the dashboard's big monospace numbers (the clock, the counts) may use one named figure size, `--t-figure`, because they are read as pictures, not text.

## The rules

- **T1. Eight sizes, no others.** Today 26 sizes render (34 size and family pairs over 14 pages at 1600); `site.css` sets 17.
- **T2. 12px is the floor**, and only for uppercase labels with letter-spacing (kickers, chips, table heads). Lowercase text is 14px or more.
- **T3. Monospace takes the same steps.** Inline `code` stays at `.88em` of its text; standalone monospace (keys, hashes, timestamps, the version) is `--t-s` or `--t-xs`, never a fraction like 12.3 or 13.2px.
- **T4. Line height follows size**: 1.6 for `--t-body` and up to `--t-l` in prose, 1.45 for `--t-ui` and `--t-s`, 1.2 for headings.
- **T5. Ties round up.** Mapping an old size to the scale, a size halfway between two steps takes the larger.
