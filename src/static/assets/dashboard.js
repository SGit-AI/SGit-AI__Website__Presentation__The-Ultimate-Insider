// The dashboard's live parts: the clock, and each member's next wake from its slot minute (London time). Apache-2.0.
(function () {
  'use strict'
  function london(d) { return d.toLocaleTimeString('en-GB', { timeZone: 'Europe/London', hour: '2-digit', minute: '2-digit' }) }
  function tick() {
    var now = new Date(), c = document.getElementById('dash-clock')
    if (c) c.textContent = london(now) + ' London'
    document.querySelectorAll('.nx[data-minute]').forEach(function (el) {
      var m = +el.dataset.minute, n = new Date(now.getTime()), mins
      n.setSeconds(0, 0); n.setMinutes(m)
      if (n <= now) n.setHours(n.getHours() + 1)
      mins = Math.round((n - now) / 60000)
      el.textContent = ':' + el.dataset.minute + ', next ' + london(n) + ' (in ' + mins + ' min)'
    })
  }
  tick(); setInterval(tick, 20000)
})()
