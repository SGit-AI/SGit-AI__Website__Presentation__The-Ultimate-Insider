// The showcase slide (conductor 030, the editor's words of 16:2x): a screenshot of one part of one page, cropped,
// explained, with the article's title, its link and a QR of the link, in stages. A slide is its JSON; this draws it on
// the slide engine, so the player steps, seeks and replays it like any slide. How to fill one: showcase.md. Apache-2.0.
//
//   <script type="application/json" id="showcase"> {
//     "kicker": "The PKI", "title": "Agents that write to each other", "text": "One line on what the page shows.",
//     "image": "shot.jpg", "size": [1440, 2400],                  the screenshot and its size in pixels
//     "link": "https://pki.sgit.ai/...", "source": "The article's title", "open": "Open it",   open: an optional big link to it
//     "stages": [ { "at": 0, "crop": [0, 0, 1440, 900], "label": "the page" },
//                 { "at": 3, "crop": [80, 600, 700, 470], "label": "the mail flow", "dim": true,
//                   "callouts": [ { "box": [120, 640, 300, 120], "text": "Each letter is sealed to its reader" } ] } ],
//     "end": 12 } </script>
//
// crop and box are in screenshot pixels: [x, y, width, height]. Each stage moves the frame to its crop over 1.2 s and
// numbers its callouts; dim darkens everything outside the stage's first box. Each stage is one step in the player.
(function () {
  'use strict'
  var spec, frameW = 800, frameH = 540, MOVE = 1.2
  var el = function (tag, cls, text) { var e = document.createElement(tag); if (cls) e.className = cls; if (text != null) e.textContent = text; return e }

  function qr(text) {
    if (!window.TuiQR) return null
    var q = TuiQR.qrcode(0, 'M'); q.addData(text); q.make()
    var n = q.getModuleCount(), d = ''
    for (var r = 0; r < n; r++) for (var c = 0; c < n; c++) if (q.isDark(r, c)) d += 'M' + c + ' ' + r + 'h1v1h-1z'
    var ns = 'http://www.w3.org/2000/svg', svg = document.createElementNS(ns, 'svg'), p = document.createElementNS(ns, 'path')
    svg.setAttribute('viewBox', '0 0 ' + n + ' ' + n); svg.setAttribute('shape-rendering', 'crispEdges'); svg.setAttribute('role', 'img'); svg.setAttribute('aria-label', 'QR code of ' + text)
    p.setAttribute('d', d); p.setAttribute('fill', '#000'); svg.appendChild(p)
    return svg
  }

  function fitCrop(c) {   // the transform that puts crop c in the middle of the frame, as large as fits
    var s = Math.min(frameW / c[2], frameH / c[3])
    return { s: s, x: frameW / 2 - (c[0] + c[2] / 2) * s, y: frameH / 2 - (c[1] + c[3] / 2) * s }
  }

  window.SLIDE_INIT = function (S) {
    try { spec = JSON.parse(document.getElementById('showcase').textContent) } catch (e) { console.error('showcase: the JSON does not parse', e); return }
    var cv = document.getElementById('cv'), size = spec.size || [1440, 900], stages = (spec.stages || []).slice().sort(function (a, b) { return a.at - b.at })
    if (!stages.length) stages = [{ at: 0, crop: [0, 0, size[0], size[1]], label: 'the page' }]
    spec.stages = stages
    if (spec.end) cv.dataset.end = spec.end
    if (spec.kicker) cv.appendChild(el('div', 'kk w', spec.kicker))
    var h = el('div', 'hl', spec.title || ''); h.setAttribute('data-in', '0'); cv.appendChild(h)

    var fr = el('div', 'sc-frame'), im = el('div', 'sc-img'), img = new Image()
    im.style.width = size[0] + 'px'; im.style.height = size[1] + 'px'
    img.width = size[0]; img.height = size[1]; img.alt = spec.alt || spec.title || 'screenshot'
    img.onerror = function () { fr.appendChild(el('div', 'sc-miss', 'The screenshot (' + spec.image + ') is not here yet.')) }
    img.src = spec.image; im.appendChild(img)
    var side = el('div', 'sc-side')
    if (spec.text) { var tx = el('p', 'sc-text', spec.text); tx.setAttribute('data-in', '.4'); side.appendChild(tx) }
    var ol = el('ol', 'sc-call'), n = 0
    stages.forEach(function (st) {
      (st.callouts || []).forEach(function (c, i) {
        var k = ++n, at = String(st.at + MOVE * .8 + i * .5)
        var b = el('div', 'sc-box' + (st.dim && i === 0 ? ' dim' : '')); b.appendChild(el('b', null, String(k)))
        b.style.left = c.box[0] + 'px'; b.style.top = c.box[1] + 'px'; b.style.width = c.box[2] + 'px'; b.style.height = c.box[3] + 'px'
        b.setAttribute('data-in', at); im.appendChild(b)
        var li = el('li'); li.appendChild(el('b', null, String(k))); li.appendChild(document.createTextNode(c.text || '')); li.setAttribute('data-in', at); ol.appendChild(li)
      })
    })
    fr.appendChild(im); cv.appendChild(fr); side.appendChild(ol)
    if (spec.link) {
      var src = el('div', 'sc-src'), code = qr(spec.link), ref = el('div', 'sc-ref'), a = el('a', null, spec.link.replace(/^https?:\/\//, ''))
      src.setAttribute('data-in', '.8')
      if (code) { var q = el('div', 'sc-qr'); q.appendChild(code); src.appendChild(q) }
      if (spec.source) ref.appendChild(el('b', null, spec.source))
      a.href = spec.link; a.target = '_blank'; a.rel = 'noopener noreferrer'; ref.appendChild(a); src.appendChild(ref)
      if (spec.open) { const go = el('a', 'sc-open', spec.open); go.href = spec.link; go.target = '_blank'; go.rel = 'noopener noreferrer'; go.setAttribute('data-in', '1'); side.appendChild(go) }   // a big link: opens the page in a new tab, nothing loaded from it here
      side.appendChild(src)
    }
    cv.appendChild(side)
    if (!cv.querySelector('.bar')) { var bar = el('div', 'bar'); bar.appendChild(el('i')); cv.appendChild(bar) }
    if (!Array.isArray(window.RUV_STEPS)) window.RUV_STEPS = stages.map(function (st, i) { return { t: st.at, label: st.label || 'stage ' + (i + 1) } })
    spec.im = im
  }

  window.SLIDE_RENDER = function (t, S) {
    if (!spec || !spec.im) return
    var st = spec.stages, i = 0
    while (i + 1 < st.length && t >= st[i + 1].at) i++
    var to = fitCrop(st[i].crop || [0, 0, spec.size[0], spec.size[1]]), from = i ? fitCrop(st[i - 1].crop || st[i].crop) : to
    var k = S.ease(S.seg(t, st[i].at, st[i].at + MOVE))
    var s = S.lerp(from.s, to.s, k), x = S.lerp(from.x, to.x, k), y = S.lerp(from.y, to.y, k)
    spec.im.style.transform = 'translate(' + x.toFixed(2) + 'px,' + y.toFixed(2) + 'px) scale(' + s.toFixed(4) + ')'
    spec.im.style.setProperty('--inv', (1 / s).toFixed(4))
  }
})()
