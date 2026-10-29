// The site's offline cache (dev, 29 October 2026, the editor's word at 15:25 UTC: "Yes, add offline cache because that
// would also speed up a bunch of things too"). Registered by assets/theme.js on every page and by the talk player.
// The rules it keeps (the security pre-review of that wake):
//   - same-origin GET requests only; never a Range request, an error or an opaque response; never anything under /api/,
//     the lane's vault server or openrouter.ai (other hosts are not touched at all);
//   - pages and data (HTML, JSON, text) network-first, so an online reader always gets the latest, the cache only when
//     the network fails; scripts, styles, images, fonts and media from the cache, refreshed in the background;
//   - one cache per release ({{version}}), the older ones deleted when this one takes over;
//   - a kill switch: /sw.json, fetched no-store and never cached; {"enabled": false} empties every cache and unregisters
//     this worker on the next page load. ?nosw on any page does the same for one browser (assets/theme.js).
// Apache-2.0.
const VERSION = '{{version}}', CACHE = 'tui-' + VERSION
const PAGE_LIKE = /\.(html?|json|txt|md|xml)$/i

self.addEventListener('install', e => { self.skipWaiting() })
self.addEventListener('activate', e => {
  e.waitUntil((async () => {
    for (const k of await caches.keys()) if (k !== CACHE && k.startsWith('tui-')) await caches.delete(k)
    await self.clients.claim()
    await killSwitch()
  })())
})

let lastCheck = 0
async function killSwitch() {
  try {
    const r = await fetch('/sw.json', { cache: 'no-store' })
    if (!r.ok) return
    const j = await r.json()
    if (j && j.enabled === false) {
      for (const k of await caches.keys()) if (k.startsWith('tui-')) await caches.delete(k)
      await self.registration.unregister()
    }
  } catch (e) {}
}

function cacheable(req, url) {
  return req.method === 'GET' && url.origin === self.location.origin && !req.headers.has('range')
    && !url.pathname.startsWith('/api/') && url.pathname !== '/sw.json' && url.pathname !== '/sw.js'
}
async function keep(req, res) {
  if (res && res.ok && res.status === 200 && res.type === 'basic') { const c = await caches.open(CACHE); await c.put(req, res.clone()) }
  return res
}
async function networkFirst(req) {
  try { return await keep(req, await fetch(req)) }
  catch (e) { const hit = await caches.match(req, { ignoreSearch: req.mode === 'navigate' }); if (hit) return hit; throw e }
}
async function cacheThenRefresh(req, ev) {
  const hit = await caches.match(req)
  const fresh = fetch(req).then(res => keep(req, res)).catch(() => null)
  if (hit) { ev.waitUntil(fresh); return hit }
  return (await fresh) || fetch(req)
}

self.addEventListener('fetch', ev => {
  const req = ev.request, url = new URL(req.url)
  if (!cacheable(req, url)) return                                       // the browser handles it, untouched
  if (req.mode === 'navigate' && Date.now() - lastCheck > 300000) { lastCheck = Date.now(); ev.waitUntil(killSwitch()) }
  const pageLike = req.mode === 'navigate' || PAGE_LIKE.test(url.pathname) || url.pathname.endsWith('/')
  ev.respondWith(pageLike ? networkFirst(req) : cacheThenRefresh(req, ev))
})
