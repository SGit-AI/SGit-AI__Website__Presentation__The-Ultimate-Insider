// Light or dark: follows the system until the reader picks one; the pick is kept in this browser only. Apache-2.0.
(function () {
  var KEY = 'ui-theme', root = document.documentElement, saved = null
  try { saved = localStorage.getItem(KEY) } catch (e) {}
  if (saved === 'light' || saved === 'dark') root.setAttribute('data-theme', saved)
  document.addEventListener('DOMContentLoaded', function () {
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
