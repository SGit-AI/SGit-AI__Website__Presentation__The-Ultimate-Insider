// Filters for the commits page: by agent, notes only, CI and merges hidden, and a text search. Without it, every commit shows. Apache-2.0.
(function () {
  'use strict'
  var list = [].slice.call(document.querySelectorAll('.commits .cm')), agent = ''
  var $ = function (id) { return document.getElementById(id) }
  if (!list.length) return
  function apply() {
    var q = ($('f-q').value || '').toLowerCase(), n = 0
    list.forEach(function (c) {
      var show = (!agent || c.dataset.agent === agent || c.dataset.to.split(' ').indexOf(agent) >= 0)
        && (!$('f-notes').checked || c.dataset.to)
        && (!$('f-ci').checked || c.dataset.kind !== 'ci')
        && (!$('f-merge').checked || c.dataset.kind !== 'merge')
        && (!q || c.textContent.toLowerCase().indexOf(q) >= 0)
      c.hidden = !show; if (show) n++
    })
    document.querySelectorAll('table.notes tbody tr[data-from]').forEach(function (r) { r.hidden = !!agent && r.dataset.from !== agent && r.dataset.to !== agent })
    $('f-n').textContent = n + ' of ' + list.length + ' shown'
  }
  document.querySelector('.cfilters .chips').addEventListener('click', function (e) {
    var b = e.target.closest('button'); if (!b) return
    agent = b.dataset.agent
    this.querySelectorAll('button').forEach(function (x) { x.classList.toggle('on', x === b) })
    apply()
  })
  ;['f-notes', 'f-ci', 'f-merge'].forEach(function (id) { $(id).addEventListener('change', apply) })
  $('f-q').addEventListener('input', apply)
  apply()
})()
