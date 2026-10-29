// Light or dark: follows the system until the reader picks one; the pick is kept in this browser only. Apache-2.0.
(function () {
  var KEY = 'ui-theme', root = document.documentElement, saved = null
  try { saved = localStorage.getItem(KEY) } catch (e) {}
  if (saved === 'light' || saved === 'dark') root.setAttribute('data-theme', saved)
  document.addEventListener('DOMContentLoaded', function () {
    // the side navigation starts closed on a phone, so each page shows its own heading first (designer@, design note 1, item 5);
    // it is rendered open, so a wide screen shows it even without script
    if (window.matchMedia && !matchMedia('(min-width:861px)').matches) document.querySelectorAll('.side > details[open]').forEach(function (d) { d.removeAttribute('open') })
    // on a phone the links are one row that scrolls: bring the current section's link into view (design note 2)
    if (window.matchMedia && !matchMedia('(min-width:701px)').matches) { var cur = document.querySelector('nav.main a[aria-current]'); if (cur) cur.parentNode.scrollLeft = cur.offsetLeft - cur.parentNode.offsetLeft - 16 }
    var btn = document.querySelector('button.theme')
    if (!btn) return
    btn.addEventListener('click', function () {
      var dark = root.getAttribute('data-theme') ? root.getAttribute('data-theme') === 'dark' : matchMedia('(prefers-color-scheme: dark)').matches
      var next = dark ? 'light' : 'dark'
      root.setAttribute('data-theme', next)
      try { localStorage.setItem(KEY, next) } catch (e) {}
    })
  })
})()
