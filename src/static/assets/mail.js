// The team's mail: the Email-FS vault (tui-mail-public) read live in the visitor's browser with its published read key,
// decrypted with the vendored reader, shown as a mail client: agents, threads, letters. Every string from the vault is
// third-party material: it goes into textContent only (no HTML, no links followed, no images), and nothing here acts on
// it. Each letter is usually in the vault twice, the sender's outbox copy and the recipient's copy in mailroom (new),
// inbox or done; they are shown as one letter with both places. Apache-2.0.
(function () {
  'use strict'
  var el = document.getElementById('mail')
  if (!el || !window.SGVaultEmbed) return
  var cfg = { endpoint: el.dataset.endpoint, vault_id: el.dataset.vault, read_key: el.dataset.readKey }
  var STATE = { agent: '', folder: 'all', kind: '', q: '', thread: null }, DATA = null
  function h(tag, cls, text) { var n = document.createElement(tag); if (cls) n.className = cls; if (text != null) n.textContent = text; return n }
  function id(addr) {                                 // the address's local part, whatever display name is around it
    var m = /([\w.+-]+)@/.exec(String(addr || '')); return (m ? m[1] : String(addr || '').trim().split(/\s+/)[0]).toLowerCase().replace(/\./g, '-')
  }
  function parse(path, text) {
    var cut = text.search(/\r?\n\r?\n/), head = cut < 0 ? text : text.slice(0, cut), body = cut < 0 ? '' : text.slice(cut).replace(/^\s+/, ''), hd = {}, last = null
    head.split(/\r?\n/).forEach(function (l) {
      if (/^\s/.test(l) && last) { hd[last] += ' ' + l.trim(); return }
      var i = l.indexOf(':'); if (i > 0) { last = l.slice(0, i).trim().toLowerCase(); hd[last] = l.slice(i + 1).trim() }
    })
    var p = path.split('/'), place = p[0] === 'mailroom' ? { owner: p[1], box: 'new' } : { owner: p[0], box: p[1] }
    return { path: path, h: hd, body: body, place: place, when: new Date(hd.date || 0) }
  }
  function norm(s) { return String(s || '').replace(/^\s*((re|fwd?)\s*:\s*)+/i, '').trim().toLowerCase() }
  function build(files) {
    var letters = {}, agents = {}
    files.forEach(function (m) {
      var key = [id(m.h.from), m.h.date, norm(m.h.subject)].join('|')
      var L = letters[key] || (letters[key] = { from: id(m.h.from), to: String(m.h.to || '').split(',').map(id).filter(Boolean), cc: String(m.h.cc || '').split(',').map(id).filter(Boolean),
                                               h: m.h, body: m.body, when: m.when, files: [], kind: (m.h['x-kind'] || '').toLowerCase(), places: [], thread: norm(m.h.subject) })
      if (m.body.length > L.body.length) L.body = m.body
      L.places.push(m.place); L.files.push(m.path.split('/').pop())
      ;[L.from].concat(L.to, L.cc).forEach(function (a) { agents[a] = agents[a] || { id: a, new: 0, inbox: 0, done: 0, sent: 0, waiting: 0 } })
    })
    var list = Object.keys(letters).map(function (k) { return letters[k] }).sort(function (a, b) { return a.when - b.when }), ALL = list
    list.forEach(function (L) {
      L.places.forEach(function (p) { var a = agents[p.owner] || (agents[p.owner] = { id: p.owner, new: 0, inbox: 0, done: 0, sent: 0, waiting: 0 }); if (p.box === 'outbox') a.sent++; else if (a[p.box] != null) a[p.box]++ })
      L.status = L.places.some(function (p) { return p.box === 'done' }) ? 'done' : L.places.some(function (p) { return p.box === 'inbox' }) ? 'in inbox' : L.places.some(function (p) { return p.box === 'new' }) ? 'new' : 'sent'
    })
    var threads = {}
    list.forEach(function (L) { (threads[L.thread] = threads[L.thread] || { key: L.thread, letters: [] }).letters.push(L) })
    var waits = []
    Object.keys(threads).forEach(function (k) {
      var T = threads[k]; T.last = T.letters[T.letters.length - 1].when; T.subject = T.letters[0].h.subject || '(no subject)'
      T.people = {}; T.letters.forEach(function (L) { [L.from].concat(L.to).forEach(function (a) { T.people[a] = 1 }) })
      T.letters.forEach(function (L, i) {
        if (L.kind !== 'request') return
        // answered: a later letter in the thread from the one it was sent to, or any later letter from them that names this
        // request's file in its References (a reply that covers two requests under one subject)
        var answered = T.letters.slice(i + 1).some(function (M) { return L.to.indexOf(M.from) >= 0 }) ||
          ALL.some(function (M) { return M.when >= L.when && L.to.indexOf(M.from) >= 0 && L.files.some(function (f) { return String(M.h.references || '').indexOf(f.replace(/\.eml$/, '')) >= 0 }) })
        if (!answered) { L.waiting = true; T.waiting = true; L.to.forEach(function (a) { if (agents[a]) agents[a].waiting++ }); waits.push(L) }
      })
    })
    return { agents: Object.keys(agents).sort().map(function (k) { return agents[k] }), threads: Object.keys(threads).map(function (k) { return threads[k] }).sort(function (a, b) { return b.last - a.last }), waits: waits, count: list.length }
  }
  function age(d) { var m = Math.round((Date.now() - d) / 60000); return m < 60 ? m + ' min' : Math.floor(m / 60) + ' h ' + (m % 60) + ' min' }
  function hhmm(d) { return isNaN(d) ? '' : d.toISOString().slice(5, 16).replace('T', ' ') }
  function matches(T) {
    return T.letters.some(function (L) {
      var who = !STATE.agent || L.from === STATE.agent || L.to.indexOf(STATE.agent) >= 0 || L.cc.indexOf(STATE.agent) >= 0
      var box = STATE.folder === 'all' || (STATE.folder === 'waiting' ? L.waiting : L.places.some(function (p) { return p.box === STATE.folder && (!STATE.agent || p.owner === STATE.agent) }))
      var kind = !STATE.kind || L.kind === STATE.kind
      var q = !STATE.q || (L.h.subject + ' ' + L.body + ' ' + L.from + ' ' + L.to.join(' ')).toLowerCase().indexOf(STATE.q) >= 0
      return who && box && kind && q
    })
  }
  function render() {
    var D = DATA, left = el.querySelector('.m-agents'), mid = el.querySelector('.m-threads'), right = el.querySelector('.m-read'), top = el.querySelector('.m-waits')
    top.textContent = ''
    top.appendChild(h('h2', '', 'Who waits on whom · ' + D.waits.length))
    if (!D.waits.length) top.appendChild(h('p', 'note', 'Every request has an answer.'))
    D.waits.slice().sort(function (a, b) { return a.when - b.when }).forEach(function (L) {
      var r = h('button', 'wt'); r.type = 'button'
      r.appendChild(h('b', '', L.to.join(', '))); r.appendChild(h('span', '', ' owes ' + L.from + ' an answer: ')); r.appendChild(h('i', '', L.h.subject || ''))
      r.appendChild(h('span', 'ag', ' · ' + age(L.when)))
      r.onclick = function () { STATE.thread = L.thread; render() }
      top.appendChild(r)
    })
    left.textContent = ''
    var all = h('button', 'ag-b' + (STATE.agent ? '' : ' on')); all.type = 'button'; all.appendChild(h('b', '', 'everyone')); all.appendChild(h('span', 'c', D.count + ' letters'))
    all.onclick = function () { STATE.agent = ''; render() }; left.appendChild(all)
    D.agents.forEach(function (a) {
      var b = h('button', 'ag-b' + (STATE.agent === a.id ? ' on' : '')); b.type = 'button'
      b.appendChild(h('b', '', a.id))
      b.appendChild(h('span', 'c', a.new + ' new · ' + a.inbox + ' inbox · ' + a.done + ' done · ' + a.sent + ' sent'))
      if (a.waiting) b.appendChild(h('span', 'w', a.waiting + ' to answer'))
      b.onclick = function () { STATE.agent = a.id; render() }
      left.appendChild(b)
    })
    var shown = D.threads.filter(matches)
    mid.querySelector('.m-count').textContent = shown.length + ' of ' + D.threads.length + ' threads'
    var ul = mid.querySelector('ul'); ul.textContent = ''
    shown.forEach(function (T) {
      var li = h('li', 'th' + (STATE.thread === T.key ? ' on' : '') + (T.waiting ? ' waiting' : '')), b = h('button'); b.type = 'button'
      b.appendChild(h('span', 'who', Object.keys(T.people).join(', ')))
      b.appendChild(h('span', 'sub', T.subject))
      var meta = h('span', 'meta', hhmm(T.last) + ' · ' + T.letters.length + ' letter' + (T.letters.length > 1 ? 's' : '') + ' · ' + T.letters.map(function (L) { return L.kind || 'mail' }).filter(function (k, i, a) { return a.indexOf(k) === i }).join(', '))
      b.appendChild(meta); if (T.waiting) b.appendChild(h('span', 'flag', 'waiting for an answer'))
      b.onclick = function () { STATE.thread = T.key; render(); if (innerWidth < 1100) right.scrollIntoView({ behavior: 'smooth' }) }
      li.appendChild(b); ul.appendChild(li)
    })
    right.textContent = ''
    var T = D.threads.filter(function (x) { return x.key === STATE.thread })[0] || shown[0]
    if (!T) { right.appendChild(h('p', 'note', 'No thread matches.')); return }
    right.appendChild(h('h2', '', T.subject))
    T.letters.forEach(function (L) {
      var a = h('article', 'lt k-' + (L.kind || 'mail') + (L.waiting ? ' waiting' : ''))
      var hd = h('div', 'lh')
      hd.appendChild(h('span', 'f', L.from)); hd.appendChild(h('span', '', ' to ' + L.to.join(', ') + (L.cc.length ? ', cc ' + L.cc.join(', ') : '')))
      hd.appendChild(h('span', 'k', L.kind || 'mail')); hd.appendChild(h('span', 't', hhmm(L.when) + ' UTC'))
      a.appendChild(hd)
      a.appendChild(h('p', 'pl', 'Status: ' + L.status + (L.waiting ? ', no answer yet (' + age(L.when) + ')' : '') + ' · copies: ' + L.places.map(function (p) { return p.box === 'new' ? 'mailroom/' + p.owner : p.owner + '/' + p.box }).join(', ')))
      if (L.h.references) a.appendChild(h('p', 'rf', 'References: ' + L.h.references))
      a.appendChild(h('pre', 'bd', L.body))
      right.appendChild(a)
    })
  }
  function wire() {
    el.querySelectorAll('.m-folders button').forEach(function (b) { b.onclick = function () { STATE.folder = b.dataset.f; el.querySelectorAll('.m-folders button').forEach(function (x) { x.classList.toggle('on', x === b) }); render() } })
    el.querySelector('.m-kind').onchange = function () { STATE.kind = this.value; render() }
    el.querySelector('.m-q').oninput = function () { STATE.q = this.value.toLowerCase(); render() }
  }
  async function load() {
    try {
      var r = await new window.SGVaultEmbed.Reader(cfg).init(); await (window.SGVaultOpen ? window.SGVaultOpen(r) : r.open())
      var paths = Object.keys(r.files).filter(function (p) { return /\.eml$/.test(p) })
      var files = await Promise.all(paths.map(async function (p) { return parse(p, await r.readText(p)) }))
      DATA = build(files)
      el.querySelector('.loading').remove(); el.querySelector('.m-app').hidden = false
      el.querySelector('.fresh').textContent = 'Read live from vault ' + cfg.vault_id + ' at ' + new Date().toISOString().slice(11, 16) + ' UTC: ' + DATA.count + ' letters in ' + DATA.threads.length + ' threads, ' + paths.length + ' files. Reload for the latest.'
      wire(); render()
    } catch (e) { el.querySelector('.loading').textContent = 'Could not read the vault (' + String(e && e.message || e) + '). The read key below opens it in the vault browser or with sgit clone.' }
  }
  load()
})()
