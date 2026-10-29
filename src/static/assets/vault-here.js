// The public vaults, opened on the page (dev 008), two ways, both on demand, nothing fetched until a reader asks:
//   "Open it here" frames the official SG/Vault interface with sgit.ai's vault-ui-embed.js (vendored, unmodified), which
//   hands the frame the read key by postMessage, target origin pinned; "List its files" decrypts the tree in this page with
//   the vendored reader (vault-embed.js and vault-open.js) and shows any file as text. Read keys only. textContent only. Apache-2.0.
(function () {
  'use strict'
  var EMBED = document.currentScript.src.replace(/vault-here\.js.*$/, 'vendor/vault-ui-embed.js')
  function h(tag, cls, text) { var e = document.createElement(tag); if (cls) e.className = cls; if (text != null) e.textContent = text; return e }
  function frameIt(box, btn) {
    btn.disabled = true
    document.querySelectorAll('.sgv-uiembed').forEach(function (m) { m.className = 'sgv-uiembed-mounted' })   // the embed mounts every .sgv-uiembed it finds: only this one is new
    var host = h('div', 'sgv-uiembed')
    host.setAttribute('data-vault', box.dataset.vault)
    host.setAttribute('data-readkey', box.dataset.readKey)
    host.setAttribute('data-app', '0')
    box.querySelector('.here-ui').appendChild(host)
    var s = document.createElement('script'); s.src = EMBED; document.body.appendChild(s)
  }
  async function listIt(box, btn) {
    btn.disabled = true
    var out = box.querySelector('.here-files'), note = h('p', 'note', 'Decrypting the tree in your browser…')
    out.appendChild(note)
    try {
      var r = await new window.SGVaultEmbed.Reader({ endpoint: box.dataset.endpoint, vault_id: box.dataset.vault, read_key: box.dataset.readKey }).init()
      await window.SGVaultOpen(r)
      var paths = Object.keys(r.files).sort(), view = h('pre', 'here-view'), list = h('ul', 'here-tree')
      note.textContent = paths.length + ' files at ' + new Date().toISOString().slice(11, 16) + ' UTC. Pick one to read it.'
      paths.forEach(function (p) {
        var li = h('li'), b = h('button', '', p); b.type = 'button'
        b.addEventListener('click', async function () {
          list.querySelectorAll('button.on').forEach(function (x) { x.classList.remove('on') }); b.classList.add('on')
          view.textContent = 'reading ' + p + '…'
          try { var t = await r.readText(p); view.textContent = /\.(png|jpe?g|gif|webp|zip|pdf)$/i.test(p) ? p + ' is not text' : t.slice(0, 200000) }
          catch (e) { view.textContent = 'could not read ' + p + ': ' + e.message }
        })
        li.appendChild(b); list.appendChild(li)
      })
      var grid = h('div', 'here-grid'); grid.appendChild(list); grid.appendChild(view); out.appendChild(grid)
    } catch (e) { note.textContent = 'Could not open the vault: ' + e.message; btn.disabled = false }
  }
  document.querySelectorAll('.here').forEach(function (box) {
    box.querySelector('.here-open').addEventListener('click', function (e) { frameIt(box, e.currentTarget) })
    box.querySelector('.here-list').addEventListener('click', function (e) { listIt(box, e.currentTarget) })
  })
})()
