// Light or dark: follows the system until the reader picks one; the pick is kept in this browser only. Apache-2.0.
(function () {
  var KEY = 'ui-theme', root = document.documentElement, saved = null
  // the offline cache (sw.js at the site's root): pages and data from the network first, the rest from the cache, so the
  // site is fast and works on bad wifi; ?nosw turns it off in this browser. The rules are in sw.js.
  try {
    var swUrl = new URL('../sw.js', document.currentScript.src)
    if ('serviceWorker' in navigator && (location.protocol === 'https:' || location.hostname === 'localhost')) {
      if (/[?&]nosw\b/.test(location.search)) navigator.serviceWorker.getRegistrations().then(function (rs) { rs.forEach(function (r) { r.unregister() }) })
      else addEventListener('load', function () {   // the kill switch first: sw.json, never cached; enabled false clears and unregisters
        fetch(new URL('sw.json', swUrl).href, { cache: 'no-store' }).then(function (r) { return r.ok ? r.json() : {} }).catch(function () { return {} }).then(function (j) {
          if (j && j.enabled === false) {
            navigator.serviceWorker.getRegistrations().then(function (rs) { rs.forEach(function (r) { r.unregister() }) })
            if (window.caches) caches.keys().then(function (ks) { ks.forEach(function (k) { if (k.indexOf('tui-') === 0) caches.delete(k) }) })
          } else navigator.serviceWorker.register(swUrl.href, { scope: new URL('./', swUrl).pathname, updateViaCache: 'none' }).catch(function () {})
        })
      })
    }
  } catch (e) {}
  try { saved = localStorage.getItem(KEY) } catch (e) {}
  if (saved === 'light' || saved === 'dark') root.setAttribute('data-theme', saved)
  document.addEventListener('DOMContentLoaded', function () {
    // the side navigation starts closed on a phone, so each page shows its own heading first (designer@, design note 1, item 5);
    // it is rendered open, so a wide screen shows it even without script
    if (window.matchMedia && !matchMedia('(min-width:861px)').matches) document.querySelectorAll('.side > details[open]').forEach(function (d) { d.removeAttribute('open') })
    // on a phone the links are one row that scrolls: bring the current section's link into view (design note 2)
    if (window.matchMedia && !matchMedia('(min-width:701px)').matches) { var cur = document.querySelector('nav.main a[aria-current]'); if (cur) cur.parentNode.scrollLeft = cur.offsetLeft - cur.parentNode.offsetLeft - 16 }
    // the nav row fades only on a side where there is more to scroll to (designer@, design note 6)
    var nav = document.querySelector('nav.main')
    if (nav) { var edges = function () { nav.classList.toggle('more-l', nav.scrollLeft > 2); nav.classList.toggle('more-r', nav.scrollLeft + nav.clientWidth < nav.scrollWidth - 2) }; nav.addEventListener('scroll', edges, { passive: true }); addEventListener('resize', edges); edges() }
    // the GitHub link's star count, from GitHub's public API once per browser session; "Star" if it cannot be had
    var gh = document.querySelector('a.gh[data-repo]')
    if (gh) {
      var put = function (n) { if (typeof n === 'number') gh.querySelector('.gh-n').textContent = n }
      var cached = null
      try { cached = sessionStorage.getItem('gh-stars') } catch (e) {}
      if (cached !== null) put(+cached)
      else if (window.fetch) fetch('https://api.github.com/repos/' + gh.dataset.repo, { headers: { Accept: 'application/vnd.github+json' } })
        .then(function (r) { return r.ok ? r.json() : null })
        .then(function (d) { if (d && typeof d.stargazers_count === 'number') { put(d.stargazers_count); try { sessionStorage.setItem('gh-stars', d.stargazers_count) } catch (e) {} } })
        .catch(function () {})
    }
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
