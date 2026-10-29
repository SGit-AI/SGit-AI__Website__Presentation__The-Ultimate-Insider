# Publishing a vault’s decks onto a website, build brief

> A build brief for an agent with a vault full of presentations: the decks/v2 contract a vault must publish, the split that keeps it safe (the viewer is the site’s, the data is the vault’s), the two sandboxed frames and their CSPs, why a PDF must be a download rather than an embed, the two bugs we hit, and the prompt to hand the builder.

*Source: <https://sgit.ai/docs/briefs/vault-decks-on-a-site.html> · site v0.7.87 · this file is generated from the same content as the page, so the two cannot drift. Every page on this site has a `.md` twin; internal links below point at them.*

---

[Home](../../index.md) / [Briefs](index.md) / Decks from a vault, on a site

**Surface:** a page on a `*.sgit.ai` site, outside every vault host. [The other surfaces →](../surfaces.md)

# Publishing a vault's decks onto a website

A build brief for an agent who has a vault containing presentations and wants them to *play on a web page*: not as screenshots, not as a PDF on a file server, but read out of the encrypted vault as the reader clicks. It states the contract a vault must satisfy, the split that keeps it safe, the two mistakes we made building it, and the prompt to hand the agent who will do the work.

**What this produces.** A page like [this one](../../demos/vaults/aiuc-1-conformance/decks/aiuc1.md): slide list, prev and next, speaker notes, a focus mode for presenting, a PDF download, and a deep link to a single slide, over slides that live in vault `2wzct4k7` and are fetched and decrypted in the reader's browser. No account, nothing installed, and the server serving the bytes cannot read them.

## What to read first

- [**Reading one file out of a vault**](../vault/reading-a-vault-file.md), the primitive underneath all of this: derive the address from a read key, fetch ciphertext over CORS, decrypt with Web Crypto. If you only read one thing, read this.
- [**Publishing a vault: the method**](../../demos/vaults/publishing.md), how a vault gets a published read key in the first place, including escrowing the write key *before* publishing.
- The working implementation, ~380 lines, which you may copy: `assets/vault-deck.js` on this site, with the reader it builds on in `assets/vault-embed.js`.

## The one rule: the viewer is the site's, the data is the vault's

A read key is public, so anyone can read the vault. The risk runs the other way: **the bytes coming out of the vault were written by whoever holds the write key, and they are untrusted input to your page.** Rendering them into your own document hands a vault author your origin, your cookies, your storage, your DOM, your users.

| From the vault | From the site |
|---|---|
| The deck manifest, each deck's slides, the speaker notes, the screenshots, the printed PDF | The deck tabs, the slide list, prev and next, the notes toggle, focus, the PDF button, the deep links, and the sandbox policy the whole thing runs under |

Stated as a test you can apply to any design: **a vault must be able to change what is shown and never what the page does.** If a vault can add a button, change where a link goes, or read anything belonging to the host page, the split is wrong.

## The contract: what the vault must publish

This is the `decks/v2` layout, as published by the two vaults on this site. A viewer written to it will render any vault that follows it.

| Path | Required | What it holds |
|---|---|---|
| `decks/decks.json` or `decks.json` at the root | **Yes** | The manifest. `type: "decks/v2"`, an optional `levels` array, and a `decks` array |
| `decks/<id>.js` | Preferred | One deck's slides as source. Tens of KB, because screenshots are not in it |
| `decks/shell.html` | Preferred | Its `<style>` block is the deck's look. Its `<script>` is the vault's own viewer and is never read by the host |
| `deck/img/<name>.jpg` | If slides use images | One file per screenshot, named exactly as the slide references it |
| `deck/<file>.pdf` | Optional | The printed deck, offered as a download |

Each entry in `decks` needs `id` and `title`. Everything else is optional but earns its keep, because a host can build a page around it rather than around prose somebody has to write twice: `short` (a tab label), `level`, `one_line`, `pdf`, `file`, `introduces`, `ends_on`, `audience`, `minutes`, `stops_before`. The deck pages on this site are generated from exactly those fields.

### The slide contract

A deck source is a classic script that pushes onto a global `S`:

```
S.push({ t: 'What AIUC-1 is', notes: `the speaker notes`, html: `…the slide markup…` });
```

Three keys, and only three: `t` is the title the slide list shows, `notes` are the speaker notes, and `html` is the slide's markup as a string.

- **The stage is 1600×900.** Slide CSS is written against that viewport and nothing else. A host should size its frame to exactly that and scale the *element*, not the document, then a slide looks identical at any column width, with no reflow and no script inside the frame.
- **Images are named, never pathed.** The helper `img(name, style)` emits `<img data-img="name">` with no `src`. This is the single most important detail in the whole contract, because a slide names an image instead of pointing at a URL, the host can resolve it to decrypted bytes without the slide ever being able to make a network request. **Do not put a URL in a slide.**
- **Slides are static markup.** The deck's *build* runs JavaScript; a rendered slide must not need any.

### If your vault published only its built decks

One of the two vaults here shipped `decks/` sources; the other shipped only the assembled `deck-<id>.html` files, with screenshots already base64 inside them. Both work, and a host should handle both: prefer the source, and fall back to the built file **truncated at the literal comment `/* ---------- shell */`**, which is where the vault's own viewer begins and the declarations end. The cost of the fallback is size, hundreds of KB per deck rather than tens.

## The host side: two frames, and why

A deck cannot simply be inserted into the page, and it cannot simply be trusted. Two sandboxed, opaque-origin iframes, each with its own CSP:

|  | Sandbox | CSP | Job |
|---|---|---|---|
| **Parse frame** | `allow-scripts` | `default-src 'none'; script-src 'unsafe-inline' 'unsafe-eval'` | A deck builds its slides by running, so it runs here (no origin, no network) and posts back a plain array. **The site never evals vault code.** |
| **Render frame** | `sandbox=""`, no `allow-scripts` at all | `default-src 'none'; img-src data:; style-src 'unsafe-inline'` | Slide markup, with images already resolved to `data:` URIs by the host. Nothing in a slide can phone home |

Hand the deck source to the parse frame **over `postMessage`, not baked into the `srcdoc`**: otherwise a deck containing the characters `</script>` breaks out of the bootstrap that runs it.

### The PDF is a download, and this is not a preference

The obvious move (decrypt the PDF, wrap it in a blob, point a sandboxed iframe at it) does not work. Chrome refuses, in every sandbox combination:

> `Failed to load 'blob:…' as a plugin, because the frame into which the plugin is loading is sandboxed.`

The browser's PDF viewer is a plugin, and plugins do not run in sandboxed frames. Your three options are: drop the sandbox (gives vault bytes your origin, do not), ship a JavaScript PDF renderer (works, costs about a megabyte of vendored dependency), or **decrypt in the page and hand the bytes to the browser's own download**, which is what this site does. Trigger the download from the page and not from inside a frame: a sandbox without `allow-downloads` blocks it, and granting that to untrusted content is the wrong way round.

## Two mistakes we made, so you do not

1. **An image-name pattern that excluded underscores.** Fifteen slides rendered with a silently missing screenshot, no console error, no gap in the layout, nothing to notice by clicking through a few slides. Accept `[A-Za-z0-9_.-]` in image names, and **assert that the count of unresolved images is zero** rather than trusting the page to look right.
2. **An unscoped `closest('[data-deck]')` in the click router.** On a page dedicated to one deck the mount element itself carries `data-deck`, so every click inside the viewer matched it and returned early: prev, next, notes, focus and the PDF button were all dead, on exactly the pages just built, with nothing thrown. Scope event delegation to the control you mean, and **test the effect of a click, not that the click landed**.

## Before you call it done

- Walk **every slide of every deck** in a real browser and assert zero unresolved images. Ours is 113 slides across 9 decks; the walk takes under a minute and found the bug above.
- Confirm the render frame has **no** `allow-scripts`, and that the parse frame has **no** `allow-same-origin`.
- Download a PDF and check the byte count against the file in the vault. Ours matches exactly at 2,220,725 bytes.
- Check that a deep link to a slide restores that deck and that slide.
- **Check what you published.** Read keys on the page are fine and are the point; a vault key on a page is a catastrophe, because it is write access. Grep the built site for vault-key shapes before every release, and note that a scan built for *sgit* credential shapes will not catch an unrelated API key sitting in a vault file, which is how we once nearly published an OpenRouter key.

## The prompt to hand the builder agent

Copy this, replace the uppercase placeholders, and give it to the agent that owns the site:

```
Add a deck viewer to SITE so the presentations in vault VAULT_ID play on the page,
read live with the published read key READ_KEY.

Read https://sgit.ai/briefs/vault-decks-on-a-site.md and
https://sgit.ai/vault/reading-a-vault-file.md first. A working implementation is
assets/vault-deck.js and assets/vault-embed.js on sgit.ai; copying it is expected.

The rule that governs the design: the viewer is the site's and the data is the
vault's. Every control belongs to the site. Vault content renders only inside
sandboxed opaque-origin iframes — the deck source in one with allow-scripts and
default-src 'none', the slide markup in one with scripting off entirely and only
data: images permitted. Never eval vault code in the page origin. Never put a
decrypted PDF in an iframe; decrypt it in the page and hand it to the browser's
own download.

The vault publishes decks/v2: a manifest at decks/decks.json or decks.json, deck
sources at decks/DECK_ID.js pushing {t, notes, html} onto S, screenshots at
deck/img/NAME.jpg referenced symbolically by a data-img attribute, the deck's CSS
in the style block of decks/shell.html, and PDFs at deck/FILE.pdf. If the vault
published only built decks, take the largest script block out of the deck's HTML
file and truncate it at the comment /* ---------- shell */.

The stage is 1600x900: size the frame to that and scale the element.

Done means: every slide of every deck walked in a browser with zero unresolved
images asserted, a PDF downloaded and byte-count-checked against the vault, deep
links restoring deck and slide, and the built site grepped for vault-key shapes.
Report the slide count, the deck count and the missing-image count.
```

Written from building exactly this, at [v0.2.67 and v0.2.68](../../admin/versions.md). If you follow it and something here is wrong, that is worth telling us, the last brief on this site was corrected by the team that read it, and [the correction sits above the mistake](vault-telemetry-append-lanes.md). [All briefs](index.md) · [Reading one file out of a vault](../vault/reading-a-vault-file.md) · [The live result](../../demos/vaults/aiuc-1-conformance/decks/index.md)


---

*[Site index for agents](../../llms.txt) · [HTML version](https://sgit.ai/docs/briefs/vault-decks-on-a-site.html)*
