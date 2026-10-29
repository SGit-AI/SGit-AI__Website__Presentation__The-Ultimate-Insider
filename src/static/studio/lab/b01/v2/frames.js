// B01 v2: the overlap motif, built on the engine and timed to the script. One drawing for every slide, so the circles
// sit in the same place throughout; each page describes what changes when, and SLIDE_RENDER draws it. Apache-2.0.
(function () {
  'use strict'
  var NS = 'http://www.w3.org/2000/svg'
  var NEAR = [[568, 372], [712, 372], [640, 497]], FAR = [[300, 404], [640, 404], [980, 404]], R = 170, O = [640, 414]
  var COL = ['var(--agent)', 'var(--infra)', 'var(--risk)']
  var svg, E = {}
  function el(tag, attrs, parent) { var e = document.createElementNS(NS, tag); for (var k in attrs) e.setAttribute(k, attrs[k]); (parent || svg).appendChild(e); return e }
  function sector(k, L) {
    var a0 = (-210 + 120 * k) * Math.PI / 180, a1 = (-90 + 120 * k) * Math.PI / 180
    return 'M' + O[0] + ' ' + O[1] + 'L' + (O[0] + L * Math.cos(a0)) + ' ' + (O[1] + L * Math.sin(a0)) + 'A' + L + ' ' + L + ' 0 0 1 ' + (O[0] + L * Math.cos(a1)) + ' ' + (O[1] + L * Math.sin(a1)) + 'Z'
  }
  function badge(n) {
    var g = el('g', {}); el('circle', { r: 21, fill: 'var(--head)' }, g)
    var t = el('text', { 'text-anchor': 'middle', y: 8, 'font-size': 24, 'font-weight': 800, fill: 'var(--bg)' }, g); t.textContent = n; return g
  }
  function build() {
    svg = document.createElementNS(NS, 'svg'); svg.setAttribute('viewBox', '0 0 1280 720'); svg.setAttribute('id', 'b01'); svg.setAttribute('aria-hidden', 'true')
    var cv = document.getElementById('cv'); cv.insertBefore(svg, cv.firstChild)
    var defs = el('defs', {})
    E.clip = [0, 1, 2].map(function (i) { var cp = el('clipPath', { id: 'k' + i }, defs); return el('circle', { r: R }, cp) })
    E.circ = [0, 1, 2].map(function (i) { return el('circle', { r: R, fill: COL[i], 'fill-opacity': .12, stroke: COL[i], 'stroke-width': 5 }) })
    var g = el('g', { 'clip-path': 'url(#k0)' }), g1 = el('g', { 'clip-path': 'url(#k1)' }, g), g2 = el('g', { 'clip-path': 'url(#k2)' }, g1)
    E.sec = [0, 1, 2].map(function (k) { return el('path', { fill: COL[k] }, g2) })
    E.edge = [0, 1, 2].map(function (i) {                            // the overlap's own edge: each arc, only where it is inside the other two
      var o = [0, 1, 2].filter(function (j) { return j !== i }), ga = el('g', { 'clip-path': 'url(#k' + o[0] + ')' }), gb = el('g', { 'clip-path': 'url(#k' + o[1] + ')' }, ga)
      return el('circle', { r: R, fill: 'none', stroke: 'var(--head)', 'stroke-width': 7 }, gb)
    })
    E.marks = el('g', {})
    ;[-150, -30, 90].forEach(function (deg) {
      var a = deg * Math.PI / 180, d = 0
      while (d < 300 && NEAR.every(function (c) { var x = O[0] + d * Math.cos(a) - c[0], y = O[1] + d * Math.sin(a) - c[1]; return x * x + y * y < R * R })) d += 1
      var x = O[0] + d * Math.cos(a), y = O[1] + d * Math.sin(a), px = -Math.sin(a) * 22, py = Math.cos(a) * 22, p = 'M' + (x - px) + ' ' + (y - py) + 'L' + (x + px) + ' ' + (y + py)
      el('path', { d: p, stroke: 'var(--bg)', 'stroke-width': 16, 'stroke-linecap': 'round' }, E.marks); el('path', { d: p, stroke: 'var(--head)', 'stroke-width': 9, 'stroke-linecap': 'round' }, E.marks)
    })
    E.fence = el('rect', { rx: 18, fill: 'none', stroke: 'var(--head)', 'stroke-width': 4 })
    E.sw = el('rect', { width: 64, height: 34, rx: 17, fill: 'var(--head)' }); E.swk = el('circle', { r: 12, fill: 'var(--bg)' })
    E.badge = [1, 2, 3, 4].map(badge)
  }
  // state: pos (0 far .. 1 near), op [3], sop [3] (sector opacity), fill [3] (0..1), edge (0..1), dash (bool), marks, fence {w, h, op}, badges [4]
  window.B01 = { set: function (s) {
    if (!svg) build()
    var P = [0, 1, 2].map(function (i) { return [FAR[i][0] + (NEAR[i][0] - FAR[i][0]) * s.pos, FAR[i][1] + (NEAR[i][1] - FAR[i][1]) * s.pos] })
    var r = R * (.72 + .28 * s.pos)                                    // smaller while apart, so they clear the labels
    for (var i = 0; i < 3; i++) {
      E.clip[i].setAttribute('r', r); E.circ[i].setAttribute('r', r); E.edge[i].setAttribute('r', r)
      E.clip[i].setAttribute('cx', P[i][0]); E.clip[i].setAttribute('cy', P[i][1])
      E.circ[i].setAttribute('cx', P[i][0]); E.circ[i].setAttribute('cy', P[i][1]); E.circ[i].style.opacity = s.op[i]
      E.edge[i].setAttribute('cx', P[i][0]); E.edge[i].setAttribute('cy', P[i][1]); E.edge[i].style.opacity = s.edge
      E.edge[i].setAttribute('stroke-dasharray', s.dash ? '16 12' : 'none')
      E.sec[i].setAttribute('d', sector(i, 400 * s.fill[i])); E.sec[i].style.opacity = s.sop[i]
    }
    E.marks.style.opacity = s.marks
    var f = s.fence; E.fence.setAttribute('x', O[0] - f.w); E.fence.setAttribute('y', O[1] - f.h); E.fence.setAttribute('width', 2 * f.w); E.fence.setAttribute('height', 2 * f.h)
    E.sw.setAttribute('x', O[0] + f.w - 58); E.sw.setAttribute('y', O[1] - f.h - 17); E.swk.setAttribute('cx', O[0] + f.w - 9); E.swk.setAttribute('cy', O[1] - f.h)
    ;[E.fence, E.sw, E.swk].forEach(function (e) { e.style.opacity = f.op })
    var B = [[640, 306], [522, 330], [O[0] + f.w + 34, O[1] - f.h], [O[0] + f.w, O[1] + f.h]]
    E.badge.forEach(function (b, j) { b.setAttribute('transform', 'translate(' + B[j][0] + ' ' + B[j][1] + ')'); b.style.opacity = s.badges[j] })
  } }
})()
