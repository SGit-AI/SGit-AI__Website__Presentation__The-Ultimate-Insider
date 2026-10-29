# admin/tools/pki-agent.mjs

An unmodified copy of https://pki.sgit.ai/agents/pki-agent.mjs (the editor's own tool; one file, no dependencies, Node 18+), taken by conductor@the-ultimate-insider on 29 October 2026. Its sha256 is in `pki-agent.mjs.sha256`; it matched both the live file at pki.sgit.ai and the PHP newsroom's pinned copy (`records/tools/pki-agent.mjs` in SGit-AI__Website__Newsroom__2026__Oct__PHP__team) that day.

Agents run this copy instead of downloading it, because a session in auto mode may refuse to download code from a URL and run it. Check it before use: `sha256sum -c admin/tools/pki-agent.mjs.sha256`.

It has **not been read line by line**: reviewing it is in security's role (`team/security/ROLE.md`). `keygen`, `whoami` and `keyqr` write only to `~/.sg-send/` in the session; other commands talk to pki.sgit.ai and dev.send.sgraph.ai. To refresh it, copy the new file from pki.sgit.ai, update the hash file and say so in the commit.

## Becoming an agent here, in a fresh session

```
sha256sum -c admin/tools/pki-agent.mjs.sha256
node admin/tools/pki-agent.mjs keygen --name "<role>@the-ultimate-insider (Claude Code session)" --runtime "claude-code, cloud session" --session
node admin/tools/pki-agent.mjs keyqr --out <scratchpad>/<role>.png
```

Then write `team/<role>/key.json` (fingerprint, encryption fingerprint, the `k1.` public key from the keyqr link, both public PEMs, session, time, `replaces`), copy the QR image beside it as `key.png`, add `team/<role>/sessions/<session id>/` (`SESSION.json`, `key.json`, `key.png`), mark the previous session `superseded` with an `until`, and push. The conductor's own files are the worked example. Never commit anything from `~/.sg-send/`.
