# The ultimate insider: the evidence (public)

This folder is the register from the evidence vault `tui-evidence-public`, everything but the raw captures, which stay in the vault (116 MB). Each source's files and hashes are in `sources/manifest.json`. One change from the vault: this repository's gate refuses the long dash, so where a quoted source used one it is written here as a hyphen; the vault keeps the exact words.

Kept by researcher@the-ultimate-insider for the talk "The ultimate insider" (Dinis Cruz, hack::soho, IOActive London, 29 October 2026) and its site, https://the-ultimate-insider.presentation.sgit.ai.

**This vault is 100% public.** Its read key is published on the site. Everything in it is a capture of a public page or the researcher's reading of one.

## What is here

| Folder | What it holds |
|---|---|
| `claims/` | The claims register: every claim the talk and its source article make, graded A0 to A6, with whether it holds as worded and a suggested wording where it does not |
| `ideas/` | The editor's ideas across newsroom.sgit.ai, sgit.ai and php.oct.2026.newsroom.sgit.ai, each with the outside evidence for and against it |
| `incidents/` | Public AI agent incidents since May 2025, candidates for the talk, benign ("agents being agents") and attacks kept apart; and newer editions of the numbers the talk uses |
| `sources/` | Every source captured: raw bytes and a text extraction per source, and `manifest.json` with the SHA-256 of every file |
| `METHOD.md` | How a source is captured and a claim graded |
| `updates/` | One dated note per research session: what changed |

## How to read a grade

The scale is the one the fact-check desk of php.oct.2026.newsroom.sgit.ai uses. A0 unsupported, A1 weak signal, A2 reported (one named party, checked), A3 echoed (several outlets, one origin), A4 corroborated (two independent parties), A5 confirmed (two independent primary sources), A6 established (the authoritative primary record). A position is shown as a position: the facts under it are graded, the argument is not.

A grade is earned from captures the researcher opened and read, never from how often a thing is repeated.

## Where it comes from

Every capture records its URL, the time it was fetched (UTC), the HTTP status and the hash. Pages change; the capture is what the page said when it was read. Quoted material keeps its own licence; the register's own text is CC BY 4.0.
