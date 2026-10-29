// The team board: the Issues-FS lite folders of the team's public vault, read live in the visitor's browser with the
// published read key, decrypted here, rendered as three columns. Nothing is cached but immutable objects (the reader
// fetches the ref with no-store), and every string from the vault goes into textContent. Apache-2.0.
//
//   <div id="board" data-endpoint data-vault data-read-key> ... </div>   the page carries the vault; this file only reads it
(function () {
  'use strict'
  var COLS = ['open', 'blocked', 'done'], el = document.getElementById('board')
  if (!el || !window.SGVaultEmbed) return
  var cfg = { endpoint: el.dataset.endpoint, vault_id: el.dataset.vault, read_key: el.dataset.readKey }
  function h(tag, cls, text) { var n = document.createElement(tag); if (cls) n.className = cls; if (text != null) n.textContent = text; return n }
  function parse(path, text) {                        // NNN-slug.md with YAML-ish front matter, then '# title', then the plan
    var m = /^---\n([\s\S]*?)\n---\n?([\s\S]*)$/.exec(text), meta = {}, body = m ? m[2] : text
    if (m) m[1].split('\n').forEach(function (l) { var i = l.indexOf(':'); if (i > 0) meta[l.slice(0, i).trim()] = l.slice(i + 1).trim() })
    var t = /^#\s+(.+)$/m.exec(body), parts = path.split('/')
    return { path: path, agent: parts[0], col: parts[2], id: parts[3].replace(/\.md$/, ''), num: (parts[3].match(/^\d+/) || [''])[0],
             title: t ? t[1].trim() : parts[3], meta: meta, body: (t ? body.replace(t[0], '') : body).trim() }
  }
  function card(it) {
    var c = h('details', 'issue p-' + (it.meta.priority || 'none')), s = h('summary')
    s.appendChild(h('span', 'who', it.agent + ' · ' + it.num))
    s.appendChild(h('span', 'ttl', it.title))
    var tags = h('span', 'tags')
    if (it.meta.priority) tags.appendChild(h('span', 'pri', it.meta.priority))
    if (it.meta.blocked_on) tags.appendChild(h('span', 'wait', 'waits on ' + it.meta.blocked_on))
    if (it.meta.created) tags.appendChild(h('span', 'when', it.meta.created.slice(0, 10)))
    s.appendChild(tags); c.appendChild(s)
    if (it.body) c.appendChild(h('pre', 'plan', it.body))
    if (it.meta.source) c.appendChild(h('p', 'src', 'source: ' + it.meta.source))
    c.appendChild(h('p', 'path', it.path))
    c.dataset.agent = it.agent
    return c
  }
  function render(items, agents, at) {
    el.textContent = ''
    var bar = h('div', 'filters'), all = h('button', 'on', 'everyone (' + items.length + ')')
    all.type = 'button'; all.dataset.agent = ''; bar.appendChild(all)
    agents.forEach(function (a) { var n = items.filter(function (i) { return i.agent === a }).length, b = h('button', '', a + ' (' + n + ')'); b.type = 'button'; b.dataset.agent = a; bar.appendChild(b) })
    bar.addEventListener('click', function (e) {
      var b = e.target.closest('button'); if (!b) return
      bar.querySelectorAll('button').forEach(function (x) { x.classList.toggle('on', x === b) })
      el.querySelectorAll('.issue').forEach(function (c) { c.hidden = !!b.dataset.agent && c.dataset.agent !== b.dataset.agent })
      el.querySelectorAll('.col').forEach(function (box) {               // the counts follow the filter, and an empty column says so
        var n = box.querySelectorAll('.issue:not([hidden])').length, none = box.querySelector('.none')
        box.querySelector('h2').textContent = box.dataset.col + ' · ' + n
        if (!none) { none = h('p', 'none'); box.appendChild(none) }
        none.textContent = 'nothing ' + box.dataset.col + (b.dataset.agent ? ' for ' + b.dataset.agent : ''); none.hidden = n > 0
      })
    })
    el.appendChild(bar)
    var grid = h('div', 'cols')
    COLS.forEach(function (col) {
      var mine = items.filter(function (i) { return i.col === col }), box = h('section', 'col c-' + col)
      box.dataset.col = col
      box.appendChild(h('h2', '', col + ' · ' + mine.length))
      mine.forEach(function (i) { box.appendChild(card(i)) })
      if (!mine.length) box.appendChild(h('p', 'none', 'nothing ' + col))
      grid.appendChild(box)
    })
    el.appendChild(grid)
    el.appendChild(h('p', 'fresh', 'Read live from vault ' + cfg.vault_id + ' at ' + at + ', ' + items.length + ' issues from ' + agents.length + ' agents. Reload for the latest; nothing here is a snapshot.'))
  }
  async function load() {
    try {
      var r = await new window.SGVaultEmbed.Reader(cfg).init()
      await (window.SGVaultOpen ? window.SGVaultOpen(r) : r.open())   // either vault layout (assets/vault-open.js)
      var paths = Object.keys(r.files).filter(function (p) { return /^[^/]+\/issues\/(open|blocked|done)\/\d+[^/]*\.md$/.test(p) }).sort()
      var items = await Promise.all(paths.map(async function (p) { return parse(p, await r.readText(p)) }))
      var agents = Object.keys(r.files).map(function (p) { return p.split('/')[0] }).filter(function (a, i, all) { return /^[\w.-]+$/.test(a) && a !== 'README.md' && all.indexOf(a) === i && r.files[a + '/README.md'] }).sort()
      items.sort(function (a, b) { return (a.meta.created || '').localeCompare(b.meta.created || '') || a.path.localeCompare(b.path) })
      render(items, agents, new Date().toISOString().slice(11, 16) + ' UTC')
    } catch (e) {
      el.querySelector('.loading').textContent = 'Could not read the vault (' + String(e && e.message || e) + '). The read key below opens it in the vault browser or with sgit clone.'
    }
  }
  load()
})()
