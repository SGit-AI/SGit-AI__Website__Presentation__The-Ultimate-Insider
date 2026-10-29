// QR images in the shapes pki.sgit.ai's agent tool reads, using that tool's own code: nothing new is installed.
//
//   node admin/tools/qr.mjs key  <bundle.json> <out.png>   a public key as a key QR (what `pki-agent.mjs read-qr` checks)
//   node admin/tools/qr.mjs text <file> <out.png>          any short public text as a QR, e.g. a published read key
//
// It loads admin/tools/pki-agent.mjs only after checking its sha256 against pki-agent.mjs.sha256, swaps the tool's
// command dispatch for the two commands above, and runs that copy from a temporary file. Never pass it a secret:
// a sealed secret is made with `pki-agent.mjs seal`, which never prints the key. Apache-2.0.

import crypto from 'node:crypto'
import fs from 'node:fs'
import os from 'node:os'
import path from 'node:path'
import { pathToFileURL } from 'node:url'

const here   = path.dirname(new URL(import.meta.url).pathname)
const tool   = path.join(here, 'pki-agent.mjs')
const pinned = fs.readFileSync(path.join(here, 'pki-agent.mjs.sha256'), 'utf8').split(/\s+/)[0]
const source = fs.readFileSync(tool, 'utf8')
const actual = crypto.createHash('sha256').update(source).digest('hex')
if (actual !== pinned) { console.error(`qr.mjs: pki-agent.mjs does not match its pinned sha256 (${actual}): refusing`); process.exit(1) }

const [mode, input, out] = process.argv.slice(2)
if (!['key', 'text'].includes(mode) || !input || !out) { console.error('usage: qr.mjs key <bundle.json> <out.png> | qr.mjs text <file> <out.png>'); process.exit(2) }

const dispatch = "if (!commands[cmd]) die(`unknown command ${cmd}: node pki-agent.mjs help`)\nawait commands[cmd]()"
if (!source.includes(dispatch)) { console.error('qr.mjs: the tool\'s dispatch has changed; update qr.mjs'); process.exit(1) }
const ours = `
{
    const [mode, input, out] = JSON.parse(process.env.QR_ARGS)
    if (mode === 'key') {
        const raw = JSON.parse(fs.readFileSync(input, 'utf8')), b = raw.bundle || raw
        const k = M.keyCode(b), back = await M.parseKeyCode(k.code)
        if (back.signing_fingerprint !== b.signing_fingerprint) die('the key code does not round-trip to the bundle\\'s fingerprint: refusing')
        await qrOut(M.qrKey({ fp: b.signing_fingerprint, label: b.label, code: k.code }), out)
        say('link: ' + k.url)
        say('fingerprint: ' + b.signing_fingerprint + ' (encryption ' + b.fingerprint + ')')
    } else {
        await qrOut(fs.readFileSync(input, 'utf8').trim(), out)
    }
}`
const tmp = path.join(fs.mkdtempSync(path.join(os.tmpdir(), 'qr-')), 'pki-agent-qr.mjs')
fs.writeFileSync(tmp, source.replace(dispatch, ours))
process.env.QR_ARGS = JSON.stringify([mode, path.resolve(input), path.resolve(out)])
try { await import(pathToFileURL(tmp).href) } finally { fs.rmSync(path.dirname(tmp), { recursive: true, force: true }) }
