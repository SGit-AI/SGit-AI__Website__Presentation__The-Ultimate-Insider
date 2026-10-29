// B01 v1: the storyboard's frames 2, 6, 7 and 8 as end-state slides. One drawing for all four, so the circles
// sit in exactly the same place on every slide: the motif is that they never move, and the overlap changes.
// Each page sets window.B01_FRAME before loading this file. Apache-2.0.
(function () {
  'use strict'
  var NS = 'http://www.w3.org/2000/svg'
  var C = [[568, 372], [712, 372], [640, 497]], R = 170, O = [640, 414]
  var COL = ['var(--agent)', 'var(--infra)', 'var(--risk)']
  var f = window.B01_FRAME
  function el(tag, attrs, parent) { var e = document.createElementNS(NS, tag); for (var k in attrs) e.setAttribute(k, attrs[k]); (parent || svg).appendChild(e); return e }
  function sector(k) {                                               // one third of the overlap, facing its own circle
    var a0 = (-210 + 120 * k) * Math.PI / 180, a1 = (-90 + 120 * k) * Math.PI / 180, L = 400
    return 'M' + O[0] + ' ' + O[1] + 'L' + (O[0] + L * Math.cos(a0)) + ' ' + (O[1] + L * Math.sin(a0)) + 'A' + L + ' ' + L + ' 0 0 1 ' + (O[0] + L * Math.cos(a1)) + ' ' + (O[1] + L * Math.sin(a1)) + 'Z'
  }
  var svg = document.createElementNS(NS, 'svg')
  svg.setAttribute('viewBox', '0 0 1280 720'); svg.setAttribute('id', 'b01'); svg.setAttribute('aria-hidden', 'true')
  document.getElementById('cv').insertBefore(svg, document.getElementById('cv').firstChild)
  var defs = el('defs', {})
  C.forEach(function (c, i) { var cp = el('clipPath', { id: 'k' + i }, defs); el('circle', { cx: c[0], cy: c[1], r: R }, cp) })
  C.forEach(function (c, i) { el('circle', { cx: c[0], cy: c[1], r: R, fill: COL[i], 'fill-opacity': .12, stroke: COL[i], 'stroke-width': 5 }) })
  var g = el('g', { 'clip-path': 'url(#k0)' }), g1 = el('g', { 'clip-path': 'url(#k1)' }, g), g2 = el('g', { 'clip-path': 'url(#k2)' }, g1)
  if (f.fill) for (var k = 0; k < 3; k++) el('path', { d: sector(k), fill: COL[k], 'fill-opacity': .92 }, g2)
  // the overlap's own edge: each circle's arc, drawn only where it is inside the other two
  C.forEach(function (c, i) {
    var o = [0, 1, 2].filter(function (j) { return j !== i }), ga = el('g', { 'clip-path': 'url(#k' + o[0] + ')' }), gb = el('g', { 'clip-path': 'url(#k' + o[1] + ')' }, ga)
    el('circle', { cx: c[0], cy: c[1], r: R, fill: 'none', stroke: 'var(--head)', 'stroke-width': 7, 'stroke-dasharray': f.fill ? 'none' : '16 12' }, gb)
  })
  if (f.marks) [-150, -30, 90].forEach(function (deg) {             // what stands in the way: a bar across the overlap's edge
    var a = deg * Math.PI / 180, d = 0
    while (d < 300 && C.every(function (c) { var x = O[0] + d * Math.cos(a) - c[0], y = O[1] + d * Math.sin(a) - c[1]; return x * x + y * y < R * R })) d += 1
    var x = O[0] + d * Math.cos(a), y = O[1] + d * Math.sin(a), px = -Math.sin(a) * 22, py = Math.cos(a) * 22
    el('path', { d: 'M' + (x - px) + ' ' + (y - py) + 'L' + (x + px) + ' ' + (y + py), stroke: 'var(--bg)', 'stroke-width': 16, 'stroke-linecap': 'round' })
    el('path', { d: 'M' + (x - px) + ' ' + (y - py) + 'L' + (x + px) + ' ' + (y + py), stroke: 'var(--head)', 'stroke-width': 9, 'stroke-linecap': 'round' })
  })
  if (f.fence) {                                                    // the licence: a frame with a switch, round the overlap
    var w = f.fence === 'wide' ? 340 : 150, h = f.fence === 'wide' ? 212 : 120
    el('rect', { x: O[0] - w, y: O[1] - h, width: 2 * w, height: 2 * h, rx: 18, fill: 'none', stroke: 'var(--head)', 'stroke-width': 4, 'class': 'fence' })
    el('rect', { x: O[0] + w - 58, y: O[1] - h - 17, width: 64, height: 34, rx: 17, fill: 'var(--head)' })
    el('circle', { cx: O[0] + w - 9, cy: O[1] - h, r: 12, fill: 'var(--bg)' })
  }
})()
