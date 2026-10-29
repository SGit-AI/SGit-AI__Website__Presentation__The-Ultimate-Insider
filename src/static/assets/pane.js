// The editor's feedback pane (dev, 29 October 2026, the editor's brief): on every page, notes on this page and the phrase
// selected, kept in this browser, then sent to the editor's lane, a write-only append lane on dev.send.sgraph.ai drained
// by the conductor. newsroom.sgit.ai's pattern. The rules this file keeps:
//   - the lane's append token is unlocked here from assets/lane.json with the editor's four words (PBKDF2-SHA256, then
//     AES-GCM) and kept in this browser's localStorage; the OpenRouter key is typed into the pane and kept there too;
//   - neither ever goes into a URL, the page, the console or a log; neither is shown back; the token goes only in the body
//     of a POST to the lane's server, the OpenRouter key only in the Authorization header of a POST to openrouter.ai;
//   - each note is encrypted to the conductor's public key (sgit pki v2: RSA-OAEP-SHA256 wraps AES-256-GCM) before it
//     leaves, so the server stores ciphertext; the write is blind ({"ok": true}).
// textContent only. Apache-2.0.
(function () {
  'use strict'
  var BASE = document.currentScript.src.replace(/pane\.js.*$/, '')
  var K = { token: 'tui.lane.token', or: 'tui.openrouter.key', model: 'tui.openrouter.model', notes: 'tui.notes.v1', open: 'tui.pane.open' }
  var MODEL = 'google/gemini-2.5-flash'
  var store = {
    get: function (k) { try { return localStorage.getItem(k) } catch (e) { return null } },
    set: function (k, v) { try { localStorage.setItem(k, v); return true } catch (e) { return false } },
    del: function (k) { try { localStorage.removeItem(k) } catch (e) {} }
  }
  function notes() { try { return JSON.parse(store.get(K.notes) || '[]') } catch (e) { return [] } }
  function saveNotes(n) { store.set(K.notes, JSON.stringify(n)) }
  function h(tag, cls, text) { var e = document.createElement(tag); if (cls) e.className = cls; if (text != null) e.textContent = text; return e }
  var b64 = function (buf) { var s = '', a = new Uint8Array(buf); for (var i = 0; i < a.length; i++) s += String.fromCharCode(a[i]); return btoa(s) }
  var unb64 = function (s) { var b = atob(s), a = new Uint8Array(b.length); for (var i = 0; i < b.length; i++) a[i] = b.charCodeAt(i); return a }
  var enc = new TextEncoder(), dec = new TextDecoder()
  var lane = null
  function getLane() { return lane ? Promise.resolve(lane) : fetch(BASE + 'lane.json', { cache: 'no-cache' }).then(function (r) { if (!r.ok) throw new Error('lane.json ' + r.status); return r.json() }).then(function (j) { lane = j; return j }) }

  // the four words open the append token
  function normalise(words) { return words.toLowerCase().split(/[\s-]+/).filter(Boolean).join(' ') }
  async function unlock(words) {
    var L = await getLane(), k = L.kdf, w = L.wrap
    var base = await crypto.subtle.importKey('raw', enc.encode(normalise(words)), 'PBKDF2', false, ['deriveKey'])
    var kek = await crypto.subtle.deriveKey({ name: 'PBKDF2', hash: k.hash, salt: unb64(k.salt), iterations: k.iterations }, base, { name: 'AES-GCM', length: 256 }, false, ['decrypt'])
    var pt = await crypto.subtle.decrypt({ name: 'AES-GCM', iv: unb64(w.iv), additionalData: enc.encode(w.aad) }, kek, unb64(w.ciphertext))
    var token = dec.decode(pt)
    if (!/^[0-9a-f]{16,128}$/.test(token)) throw new Error('not a lane token')
    return token
  }

  // a note, encrypted to the conductor the way `sgit pki encrypt` does, so `sgit pki decrypt` opens it
  async function seal(text) {
    var L = await getLane()
    var der = unb64(L.recipient.encrypt_pem.replace(/-----[^-]+-----/g, '').replace(/\s+/g, ''))
    var pub = await crypto.subtle.importKey('spki', der, { name: 'RSA-OAEP', hash: 'SHA-256' }, false, ['encrypt'])
    var aes = await crypto.subtle.generateKey({ name: 'AES-GCM', length: 256 }, true, ['encrypt'])
    var iv = crypto.getRandomValues(new Uint8Array(12))
    var c = await crypto.subtle.encrypt({ name: 'AES-GCM', iv: iv }, aes, enc.encode(text))
    var w = await crypto.subtle.encrypt({ name: 'RSA-OAEP' }, pub, await crypto.subtle.exportKey('raw', aes))
    var envelope = btoa(JSON.stringify({ v: 2, w: b64(w), i: b64(iv), c: b64(c) }))
    return btoa(envelope)                                         // the payload is base64 of the .enc text, as the lane's drainers expect
  }
  async function sendOne(note, token) {
    var L = await getLane()
    var payload = await seal(JSON.stringify({ schema: 'the-ultimate-insider/editor-note/v1', id: note.id, kind: note.kind, page: note.page, title: note.title, phrase: note.phrase, text: note.text, at: note.at, sent: new Date().toISOString() }))
    var r = await fetch(L.server + '/api/vault/append/write/' + L.vault_id, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ append_token: token, payload: payload }) })
    if (!r.ok) throw new Error('the lane answered ' + r.status)
  }

  // voice: record, make a small WAV, ask OpenRouter for the words
  var rec = null, chunks = []
  async function toWav(blob) {
    var ctx = new (window.AudioContext || window.webkitAudioContext)()
    var buf = await new Promise(function (ok, no) { blob.arrayBuffer().then(function (a) { ctx.decodeAudioData(a, ok, no) }) })
    var rate = 16000, src = buf.getChannelData(0), n = Math.floor(src.length * rate / buf.sampleRate), pcm = new Int16Array(n)
    for (var i = 0; i < n; i++) { var s = src[Math.floor(i * buf.sampleRate / rate)]; pcm[i] = Math.max(-1, Math.min(1, s)) * 0x7fff }
    if (ctx.close) ctx.close()
    var out = new DataView(new ArrayBuffer(44 + pcm.length * 2)), wr = function (o, s) { for (var j = 0; j < s.length; j++) out.setUint8(o + j, s.charCodeAt(j)) }
    wr(0, 'RIFF'); out.setUint32(4, 36 + pcm.length * 2, true); wr(8, 'WAVE'); wr(12, 'fmt '); out.setUint32(16, 16, true); out.setUint16(20, 1, true); out.setUint16(22, 1, true)
    out.setUint32(24, rate, true); out.setUint32(28, rate * 2, true); out.setUint16(32, 2, true); out.setUint16(34, 16, true); wr(36, 'data'); out.setUint32(40, pcm.length * 2, true)
    for (var k = 0; k < pcm.length; k++) out.setInt16(44 + k * 2, pcm[k], true)
    return b64(out.buffer)
  }
  async function transcribe(blob) {
    var key = store.get(K.or)
    if (!key) throw new Error('add your OpenRouter key below first')
    var r = await fetch('https://openrouter.ai/api/v1/chat/completions', {
      method: 'POST', headers: { 'Content-Type': 'application/json', Authorization: 'Bearer ' + key, 'X-Title': 'the ultimate insider: the editor\'s pane' },
      body: JSON.stringify({ model: store.get(K.model) || MODEL, messages: [{ role: 'user', content: [
        { type: 'text', text: 'Transcribe this voice note exactly, in its language. Reply with the transcript only.' },
        { type: 'input_audio', input_audio: { data: await toWav(blob), format: 'wav' } }] }] })
    })
    if (!r.ok) throw new Error('OpenRouter answered ' + r.status)
    var j = await r.json()
    return ((j.choices && j.choices[0] && j.choices[0].message && j.choices[0].message.content) || '').trim()
  }

  // the selection, kept as it changes, outside the pane
  var phrase = ''
  document.addEventListener('selectionchange', function () {
    var s = window.getSelection && window.getSelection()
    if (!s || !s.rangeCount) return
    var t = String(s).trim(), n = s.anchorNode
    if (t && !(n && n.parentElement && n.parentElement.closest('.tui-pane'))) { phrase = t.slice(0, 600); paint() }
  })

  // the pane
  var root, body, phraseEl, ta, kindSel, statusEl, listEl, setupEl, micBtn, sendBtn, toggle
  function say(t, bad) { statusEl.textContent = t; statusEl.className = 'tp-status' + (bad ? ' bad' : '') }
  function build() {
    toggle = h('button', 'tui-pane-toggle', 'Notes'); toggle.type = 'button'; toggle.setAttribute('aria-expanded', 'false'); toggle.setAttribute('aria-controls', 'tui-pane')
    root = h('aside', 'tui-pane'); root.id = 'tui-pane'; root.hidden = true; root.setAttribute('aria-label', 'Notes for the editor\'s lane')
    var head = h('div', 'tp-head'); head.appendChild(h('b', '', 'Notes')); var x = h('button', 'tp-x', 'close'); x.type = 'button'; head.appendChild(x)
    body = h('div', 'tp-body')
    var here = h('p', 'tp-here'); here.appendChild(h('span', 'tp-k', 'This page')); here.appendChild(h('span', '', ' ' + (document.title || location.pathname)))
    phraseEl = h('blockquote', 'tp-phrase')
    kindSel = h('div', 'tp-kinds')
    ;['note', 'fix this', 'idea', 'question', 'keep'].forEach(function (k, i) { var b = h('button', i ? '' : 'on', k); b.type = 'button'; b.dataset.kind = k; kindSel.appendChild(b) })
    kindSel.addEventListener('click', function (e) { var b = e.target.closest('button'); if (!b) return; kindSel.querySelectorAll('button').forEach(function (y) { y.classList.toggle('on', y === b) }) })
    ta = h('textarea', 'tp-text'); ta.rows = 5; ta.placeholder = 'Your note on this page, or a message'
    var row = h('div', 'tp-row')
    micBtn = h('button', 'tp-mic', 'Speak'); micBtn.type = 'button'
    var keep = h('button', 'tp-keep', 'Keep note'); keep.type = 'button'
    row.appendChild(micBtn); row.appendChild(keep)
    statusEl = h('p', 'tp-status')
    listEl = h('div', 'tp-list')
    sendBtn = h('button', 'tp-send', 'Send'); sendBtn.type = 'button'
    setupEl = h('div', 'tp-setup')
    ;[here, phraseEl, kindSel, ta, row, statusEl, sendBtn, listEl, setupEl].forEach(function (e) { body.appendChild(e) })
    root.appendChild(head); root.appendChild(body)
    document.body.appendChild(toggle); document.body.appendChild(root)
    toggle.addEventListener('click', function () { show(root.hidden) })
    x.addEventListener('click', function () { show(false) })
    keep.addEventListener('click', function () {
      var t = ta.value.trim()
      if (!t && !phrase) { say('Write something, or select a phrase on the page.', true); return }
      var n = notes()
      n.push({ id: Date.now().toString(36) + Math.random().toString(36).slice(2, 6), kind: (kindSel.querySelector('.on') || {}).dataset.kind || 'note', page: location.pathname, title: document.title, phrase: phrase, text: t, at: new Date().toISOString(), sent: null })
      saveNotes(n); ta.value = ''; phrase = ''; say('Kept in this browser. Send when you are ready.'); paint()
    })
    sendBtn.addEventListener('click', sendAll)
    micBtn.addEventListener('click', mic)
    if (store.get(K.open) === '1') show(true)
    paint()
  }
  function show(on) { root.hidden = !on; toggle.setAttribute('aria-expanded', on ? 'true' : 'false'); document.body.classList.toggle('tui-pane-on', on); store.set(K.open, on ? '1' : '0'); if (on) paint() }
  function secretRow(label, has, placeholder, onSave, onForget, type) {
    var d = h('div', 'tp-secret')
    d.appendChild(h('p', 'tp-k', label))
    if (has) {
      var p = h('p', 'tp-ok', 'Set on this device.'); var f = h('button', 'tp-forget', 'forget'); f.type = 'button'
      f.addEventListener('click', function () { onForget(); paint() }); p.appendChild(document.createTextNode(' ')); p.appendChild(f); d.appendChild(p)
    } else {
      var form = h('form', 'tp-form'), i = h('input'); i.type = type || 'password'; i.autocomplete = 'off'; i.spellcheck = false; i.placeholder = placeholder
      i.setAttribute('autocapitalize', 'none'); i.setAttribute('autocorrect', 'off')
      var b = h('button', '', 'Save'); b.type = 'submit'; form.appendChild(i); form.appendChild(b)
      form.addEventListener('submit', function (e) { e.preventDefault(); var v = i.value; i.value = ''; onSave(v) })
      d.appendChild(form)
    }
    return d
  }
  function paint() {
    if (!root || root.hidden) return
    phraseEl.textContent = phrase ? phrase : 'Select a phrase on the page to quote it in the note.'
    phraseEl.classList.toggle('empty', !phrase)
    var n = notes(), pending = n.filter(function (x) { return !x.sent }), sent = n.filter(function (x) { return x.sent }).slice(-8).reverse()
    sendBtn.textContent = pending.length ? 'Send ' + pending.length + ' note' + (pending.length > 1 ? 's' : '') + ' to the lane' : 'Nothing to send'
    sendBtn.disabled = !pending.length
    listEl.textContent = ''
    pending.concat(sent).forEach(function (x) {
      var c = h('div', 'tp-note' + (x.sent ? ' sent' : ''))
      var m = h('p', 'tp-meta', (x.sent ? 'sent ' + x.sent.slice(11, 16) : 'kept ' + x.at.slice(11, 16)) + ' UTC · ' + x.kind + ' · ' + x.page)
      c.appendChild(m)
      if (x.phrase) c.appendChild(h('blockquote', '', x.phrase))
      if (x.text) c.appendChild(h('p', '', x.text))
      if (!x.sent) { var d = h('button', 'tp-del', 'delete'); d.type = 'button'; d.addEventListener('click', function () { saveNotes(notes().filter(function (y) { return y.id !== x.id })); paint() }); m.appendChild(document.createTextNode(' ')); m.appendChild(d) }
      listEl.appendChild(c)
    })
    setupEl.textContent = ''
    setupEl.appendChild(secretRow('The lane: your four words', !!store.get(K.token), 'four words', async function (v) {
      say('Opening the lane on this device…')
      try { store.set(K.token, await unlock(v)); say('The lane is open on this device.') } catch (e) { say('Those words do not open the lane.', true) }
      paint()
    }, function () { store.del(K.token); say('The lane is closed on this device.') }, 'text'))
    setupEl.appendChild(secretRow('Voice: your OpenRouter key', !!store.get(K.or), 'sk-or-v1-…', function (v) {
      v = v.trim(); if (!/^sk-or-/.test(v)) { say('That does not look like an OpenRouter key.', true); return }
      store.set(K.or, v); say('The OpenRouter key is kept in this browser only.'); paint()
    }, function () { store.del(K.or); say('The OpenRouter key is forgotten.') }))
    setupEl.appendChild(h('p', 'tp-fine', 'Both stay in this browser. Notes are encrypted to the conductor before they leave; the lane only accepts them, nobody can read them back from here.'))
  }
  async function sendAll() {
    var token = store.get(K.token)
    if (!token) { say('Open the lane first: your four words, below.', true); return }
    sendBtn.disabled = true
    var n = notes(), done = 0
    for (var i = 0; i < n.length; i++) {
      if (n[i].sent) continue
      try { say('Sending ' + (done + 1) + '…'); await sendOne(n[i], token); n[i].sent = new Date().toISOString(); saveNotes(n); done++ }
      catch (e) { say('Stopped: ' + e.message + '. ' + done + ' sent; the rest are kept.', true); paint(); return }
    }
    say(done + ' sent to the lane.'); paint()
  }
  async function mic() {
    if (rec && rec.state === 'recording') { rec.stop(); return }
    if (!store.get(K.or)) { say('Add your OpenRouter key below to speak a note.', true); return }
    try {
      var stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      chunks = []; rec = new MediaRecorder(stream)
      rec.ondataavailable = function (e) { if (e.data && e.data.size) chunks.push(e.data) }
      rec.onstop = async function () {
        stream.getTracks().forEach(function (t) { t.stop() })
        micBtn.textContent = 'Speak'; micBtn.classList.remove('rec'); say('Transcribing…')
        try { var t = await transcribe(new Blob(chunks, { type: rec.mimeType })); ta.value = (ta.value ? ta.value + ' ' : '') + t; say('Transcribed. Keep the note when it reads right.') }
        catch (e) { say('Could not transcribe: ' + e.message, true) }
      }
      rec.start(); micBtn.textContent = 'Stop'; micBtn.classList.add('rec'); say('Listening… press Stop when you are done.')
    } catch (e) { say('No microphone: ' + e.message, true) }
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', build); else build()
})()
