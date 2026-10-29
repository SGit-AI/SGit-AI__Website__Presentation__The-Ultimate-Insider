#!/usr/bin/env python3
# The editor's review page for ruv.sgit@'s policy: reads team/ruv-sgit/policy.json and writes the page fragment
# src/pages/ruv-sgit/policy-review.html, with the policy embedded and its sha256 shown, so the page always says which
# version is under review. Run it after every change to policy.json:   python3 team/ruv-sgit/tools/review_page.py
# The page keeps the editor's choices in the browser only, and builds a review to paste into the session. Apache-2.0.

import hashlib
import json
import pathlib

ROOT   = pathlib.Path(__file__).resolve().parents[3]
POLICY = ROOT / 'team/ruv-sgit/policy.json'
OUT    = ROOT / 'src/pages/ruv-sgit/policy-review.html'

VERBS  = {'read': 'read', 'write': 'write or change', 'execute': 'run', 'send': 'send to', 'create': 'create', 'delete': 'delete',
          'authenticate-as': 'act with the identity of'}
OBJECTS = {'file': 'files', 'process': 'programs', 'endpoint': 'network hosts', 'record': 'records (here: vaults, releases)',
           'credential': 'credentials (tokens, keys)', 'repository': 'git branches', 'message': 'messages', 'schedule': 'scheduled tasks'}
REACH  = {'project': 'in this repository', 'host': 'on the machine it runs on', 'allowed': 'on an allow-list', 'tenant': 'inside our own accounts',
          'world': 'visible to anyone', 'self': 'its own', 'main': 'on main'}


def plain(cap):                                                      # verb.object.reach, in words
    parts = cap.split('.')
    if len(parts) != 3:
        return cap
    v, o, r = parts
    return f"{VERBS.get(v, v)} {OBJECTS.get(o, o)}, {REACH.get(r, r)}"


def items(P):
    out, scope = [], P.get('scope', {})
    for w in P['mandate']['wanted']:
        out.append({'group': 'May do', 'title': w['capability'], 'plain': plain(w['capability']), 'text': w['within']})
    for n in P['mandate'].get('not_wanted', []):
        out.append({'group': 'Does not want', 'title': n, 'plain': plain(n), 'text': 'asked not to have this, even where the session could'})
    for k in ('writes', 'holds'):
        for f in scope.get(k, []):
            out.append({'group': 'Files it writes', 'title': f, 'plain': '', 'text': 'held until its owner joins' if k == 'holds' else 'owned by ruv.sgit@; the gate fails if another member claims it'})
    for a in scope.get('appends', []):
        path, _, how = a.partition(':')
        out.append({'group': 'Files it appends to', 'title': path.strip(), 'plain': '', 'text': how.strip()})
    for k, v in P.get('endings', {}).items():
        if k != 'decided_by':
            out.append({'group': 'How a run vault ends', 'title': k, 'plain': '', 'text': v})
    for n in P.get('never', []):
        out.append({'group': 'Never', 'title': n, 'plain': '', 'text': ''})
    for i, it in enumerate(out):
        it['id'] = f'i{i + 1}'
    return out


def main():
    raw  = POLICY.read_bytes()
    P    = json.loads(raw)
    sha  = hashlib.sha256(raw).hexdigest()
    data = json.dumps({'sha': sha[:16], 'address': P['address'], 'status': P.get('status'), 'agreed_by': P.get('agreed_by'),
                       'decided_by': P.get('endings', {}).get('decided_by', ''), 'items': items(P)}, indent=1).replace('</', '<\\/')
    meta = {'title': 'Review: ruv.sgit@\'s draft policy', 'description': 'A page for the editor to review ruv.sgit@the-ultimate-insider\'s draft policy, item by item, and produce a review to paste into the session.'}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(TEMPLATE.replace('@@META@@', json.dumps(meta)).replace('@@DATA@@', data).replace('@@SHA@@', sha[:16])
                   .replace('@@ADDRESS@@', P['address']).replace('@@STATUS@@', P.get('status', '?')))
    print(f'wrote {OUT.relative_to(ROOT)} from policy.json sha256:{sha[:16]} ({len(items(P))} items)')


TEMPLATE = r'''<!--meta @@META@@ -->
<style>
.rv-item{border:1px solid var(--line);border-radius:12px;background:var(--card);padding:14px 16px;margin:10px 0;box-shadow:var(--shadow)}
.rv-item[data-v="agree"]{border-color:var(--accent);background:var(--accent-t)}
.rv-item[data-v="change"]{border-color:var(--infra);background:var(--infra-t)}
.rv-item[data-v="question"]{border-color:var(--risk);background:var(--risk-t)}
.rv-t{font:600 15px ui-monospace,SFMono-Regular,Menlo,monospace;color:var(--head);word-break:break-word}
.rv-p{font-size:14px;color:var(--dim);margin:2px 0 0}
.rv-x{margin:8px 0 10px;color:var(--text)}
.rv-b{display:flex;flex-wrap:wrap;gap:8px}
.rv-b button,.rv-bar button{font:inherit;font-size:14px;border:1px solid var(--line2);background:var(--panel);color:var(--ink);border-radius:999px;padding:6px 14px;cursor:pointer}
.rv-b button[aria-pressed="true"]{background:var(--ink);color:var(--bg);border-color:var(--ink)}
.rv-n{width:100%;box-sizing:border-box;margin-top:10px;font:inherit;font-size:14px;padding:8px 10px;border:1px solid var(--line2);border-radius:8px;background:var(--panel);color:var(--ink);min-height:56px}
.rv-n[hidden]{display:none}
.rv-bar{position:sticky;bottom:0;z-index:5;background:var(--bg);border-top:1px solid var(--line);padding:12px 0;margin-top:24px;display:flex;flex-wrap:wrap;gap:8px;align-items:center}
.rv-bar .grow{flex:1 1 160px;font-size:14px;color:var(--dim)}
.rv-meter{height:6px;border-radius:3px;background:var(--line);overflow:hidden;margin:6px 0 0}
.rv-meter i{display:block;height:100%;background:var(--accent);width:0}
#rv-out{white-space:pre-wrap;font:13px ui-monospace,SFMono-Regular,Menlo,monospace;background:var(--bg2);border:1px solid var(--line);border-radius:10px;padding:14px;max-height:420px;overflow:auto}
.rv-verdict label{display:block;margin:6px 0}
</style>
<section class="wrap narrow">
<nav class="crumbs" aria-label="Breadcrumb"><a href="{{root}}team/index.html">Team</a> / <a href="{{root}}team/ruv-sgit/index.html">@@ADDRESS@@</a></nav>
<p class="kicker">For the editor · policy review</p>
<h1>Review ruv.sgit@'s draft policy</h1>
<p class="lead">Every line of <code>team/ruv-sgit/policy.json</code>, one card each: what the member may do, what it does not want, the files it writes, how its run vaults end, and what it must never do. Mark each one <b>agree</b>, <b>change</b> or <b>question</b>, add a note where you want one, then copy the review and paste it into the session. ruv.sgit@ applies it and sets <code>agreed_by</code> only when you agree the whole policy.</p>
<p class="note">Under review: <code>policy.json</code> sha256:<code>@@SHA@@</code>, status <b>@@STATUS@@</b>. Your choices stay in this browser only, kept against that hash: if the policy changes, the page starts a fresh review. The rendered policy, with the role in prose, is on <a href="{{root}}team/ruv-sgit/index.html#policy">the member's page</a>.</p>
<div id="rv-list"></div>
<h2 id="verdict">Your verdict</h2>
<div class="rv-verdict">
<label><input type="radio" name="rv-v" value="agree"> Agree the policy as it is</label>
<label><input type="radio" name="rv-v" value="agree-with-changes"> Agree it, with the changes marked</label>
<label><input type="radio" name="rv-v" value="not-yet"> Not yet: answer the questions and change it first</label>
<textarea class="rv-n" id="rv-general" placeholder="Anything else (optional)"></textarea>
</div>
<h2 id="review">The review to paste</h2>
<pre id="rv-out"></pre>
<div class="rv-bar">
<div class="grow"><span id="rv-count">0 of 0 reviewed</span><div class="rv-meter"><i id="rv-bar"></i></div></div>
<button type="button" id="rv-all">Agree all the rest</button>
<button type="button" id="rv-copy">Copy the review</button>
<button type="button" id="rv-reset">Start again</button>
</div>
</section>
<script type="application/json" id="rv-data">@@DATA@@</script>
<script>
(function () {
  'use strict'
  var D = JSON.parse(document.getElementById('rv-data').textContent)
  var KEY = 'ruv-sgit-policy-review:' + D.sha
  var S = { items: {}, verdict: '', general: '' }
  try { S = JSON.parse(localStorage.getItem(KEY)) || S } catch (e) {}
  var save = function () { try { localStorage.setItem(KEY, JSON.stringify(S)) } catch (e) {} ; render() }
  var esc = function (s) { var d = document.createElement('div'); d.textContent = s; return d.innerHTML }
  var list = document.getElementById('rv-list'), group = ''
  D.items.forEach(function (it) {
    if (it.group !== group) { group = it.group; var h = document.createElement('h2'); h.textContent = group; list.appendChild(h) }
    var el = document.createElement('div'); el.className = 'rv-item'; el.id = it.id
    el.innerHTML = '<div class="rv-t">' + esc(it.title) + '</div>' + (it.plain ? '<p class="rv-p">' + esc(it.plain) + '</p>' : '') +
      (it.text ? '<p class="rv-x">' + esc(it.text) + '</p>' : '<div style="height:8px"></div>') +
      '<div class="rv-b"><button type="button" data-v="agree">Agree</button><button type="button" data-v="change">Change</button><button type="button" data-v="question">Question</button></div>' +
      '<textarea class="rv-n" hidden placeholder="What should change, or what is the question?"></textarea>'
    var note = el.querySelector('textarea')
    el.querySelectorAll('button').forEach(function (b) {
      b.addEventListener('click', function () {
        var cur = S.items[it.id] || {}
        cur.v = cur.v === b.dataset.v ? '' : b.dataset.v
        S.items[it.id] = cur; save()
        if (cur.v && cur.v !== 'agree') note.focus()
      })
    })
    note.addEventListener('input', function () { var cur = S.items[it.id] || {}; cur.note = note.value; S.items[it.id] = cur; save() })
    list.appendChild(el)
  })
  document.querySelectorAll('input[name="rv-v"]').forEach(function (r) { r.addEventListener('change', function () { S.verdict = r.value; save() }) })
  var gen = document.getElementById('rv-general')
  gen.addEventListener('input', function () { S.general = gen.value; save() })
  document.getElementById('rv-all').addEventListener('click', function () {
    D.items.forEach(function (it) { var c = S.items[it.id] || {}; if (!c.v) { c.v = 'agree'; S.items[it.id] = c } }); save()
  })
  document.getElementById('rv-reset').addEventListener('click', function () {
    if (confirm('Clear every choice and note on this page?')) { S = { items: {}, verdict: '', general: '' }; save() }
  })
  document.getElementById('rv-copy').addEventListener('click', function () {
    var t = document.getElementById('rv-out').textContent, b = this
    var done = function () { b.textContent = 'Copied'; setTimeout(function () { b.textContent = 'Copy the review' }, 1500) }
    if (navigator.clipboard) navigator.clipboard.writeText(t).then(done, function () { select() })
    else select()
    function select() { var r = document.createRange(); r.selectNodeContents(document.getElementById('rv-out')); var s = getSelection(); s.removeAllRanges(); s.addRange(r) }
  })
  function render() {
    var n = 0, lines = { agree: [], change: [], question: [] }
    D.items.forEach(function (it) {
      var c = S.items[it.id] || {}, el = document.getElementById(it.id), note = el.querySelector('textarea')
      el.dataset.v = c.v || ''
      el.querySelectorAll('button').forEach(function (b) { b.setAttribute('aria-pressed', String(b.dataset.v === c.v)) })
      note.hidden = !c.v || c.v === 'agree'
      if (note.value !== (c.note || '')) note.value = c.note || ''
      if (c.v) { n++; lines[c.v].push('- [' + it.group + '] ' + it.title + (c.note ? ': ' + c.note : '')) }
    })
    document.querySelectorAll('input[name="rv-v"]').forEach(function (r) { r.checked = r.value === S.verdict })
    if (gen.value !== (S.general || '')) gen.value = S.general || ''
    document.getElementById('rv-count').textContent = n + ' of ' + D.items.length + ' reviewed'
    document.getElementById('rv-bar').style.width = (100 * n / D.items.length) + '%'
    var verdict = { 'agree': 'agree the policy as it is', 'agree-with-changes': 'agree it, with the changes below', 'not-yet': 'not yet: answer the questions and change it first' }[S.verdict] || '(no verdict yet)'
    var out = ['Policy review for ' + D.address + ', policy.json sha256:' + D.sha, 'Verdict: ' + verdict, '',
      'Change (' + lines.change.length + '):'].concat(lines.change.length ? lines.change : ['- none'],
      ['', 'Question (' + lines.question.length + '):'], lines.question.length ? lines.question : ['- none'],
      ['', 'Agreed: ' + lines.agree.length + ' of ' + D.items.length + ' items' + (n < D.items.length ? '; not reviewed: ' + (D.items.length - n) : '')])
    if (S.general) out.push('', 'Also: ' + S.general)
    document.getElementById('rv-out').textContent = out.join('\n')
  }
  render()
})()
</script>
'''

if __name__ == '__main__':
    main()
