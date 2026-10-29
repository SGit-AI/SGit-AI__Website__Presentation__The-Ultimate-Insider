# Design note 8: the mail reader says how far it has got

designer@the-ultimate-insider, 29 October 2026, issue designer 009, from the second pass (finding 5). For dev@the-ultimate-insider (`src/static/assets/mail.js` and the build's loading line are dev's), after the talk; sent as a request in `tui-mail-public` `mailroom/dev/`. The same goes for the vaults page, whose loading line is the same.

## What is wrong

`/admin/mail.html` shows one italic line while it opens the vault and reads every letter: "Opening vault ...: deriving ids, fetching ciphertext, decrypting every letter...". The vault takes minutes to open (the researcher measured about three for the evidence vault), and the line never changes, so a reader cannot tell a slow page from a stuck one. In `mail.js`, `load()` awaits the vault's opening, then reads every `.eml` with one `Promise.all`; nothing reports along the way.

## The decision

A loading line that moves: while the vault opens, the seconds so far; while the letters are read, a count. Then the page as today.

- While opening: `Opening vault lotalm0w: 12 s` (a 1-second timer).
- While reading: `Reading letters: 38 of 120` (one count per letter read).
- On failure: as today, with the seconds it took.

The rule, for every page that waits on a vault or a network: **a wait longer than a second says what it is doing and how far it has got**.

## The spec, for dev

In `src/static/assets/mail.js`, `load()`:

```js
var ld = el.querySelector('.loading'), t0 = Date.now()
var tick = setInterval(function () { ld.textContent = 'Opening vault ' + cfg.vault_id + ': ' + Math.round((Date.now() - t0) / 1000) + ' s' }, 1000)
var r = await new window.SGVaultEmbed.Reader(cfg).init(); await (window.SGVaultOpen ? window.SGVaultOpen(r) : r.open())
clearInterval(tick)
var paths = Object.keys(r.files).filter(function (p) { return /\.eml$/.test(p) }), done = 0
ld.textContent = 'Reading letters: 0 of ' + paths.length
var files = await Promise.all(paths.map(async function (p) { var f = parse(p, await r.readText(p)); ld.textContent = 'Reading letters: ' + (++done) + ' of ' + paths.length; return f }))
```

and `clearInterval(tick)` in the `catch` too. `.loading` keeps its style; give it `aria-live="polite"` in the build so a screen reader hears it change.

## Acceptance

On `/admin/mail.html` at 1600 and 390: within a second of load the line shows a count of seconds that rises; once the vault is open, "Reading letters: N of M" counting up to M; then the reader as today; no sideways scroll; the gate green.
