#!/usr/bin/env python3
"""How this talk was built: a mini deck of the team in motion, from its own records.

    python3 admin/tools/workflow_deck.py

Reads only public records: every wake record (team/*/wakes/*.json: agent, start, outcome, the five verdicts),
the commits each member marked as its own (git log: counts and times), the pace graph (team/conductor/pace.json:
ids, kinds, owners, verdicts), the night log's snapshots (team/conductor/night/*.json: who wrote to whom, counted;
never a subject or a body) and the schedule's slots. It writes content/articles/how-this-talk-was-built.md: a short
article holding one 1280x720 stage, six scenes on a virtual clock, with play, pause, step back and forward, and full
screen. Every number on the stage is computed here; nothing is typed. Kept by conductor@the-ultimate-insider.
"""
import datetime as dt, glob, html, json, math, re, subprocess
from pathlib import Path

ROOT    = Path(__file__).resolve().parents[2]
ARTICLE = ROOT / 'content' / 'articles' / 'how-this-talk-was-built.md'
START   = '2026-10-29T01:40:00Z'
SLOTS   = [('conductor', 2, 'keeps the pace, the keys and the record'), ('researcher', 9, 'finds and grades the sources'),
           ('deck', 17, 'leads the talk and reviews every piece'), ('ruv-sgit', 32, 'makes the animations'),
           ('designer', 39, 'decides how the site looks'), ('dev', 47, 'builds and releases the site'),
           ('storyteller', 54, 'holds the arc (joining)')]
NAMES   = {'ruv-sgit': 'ruv.sgit'}
COLOUR  = {'ok': '#2dd4bf', 'partial': '#fbbf24', 'idle': '#8a94a6', 'failed': '#ff4d6d', 'hold': '#a78bfa', 'open': '#60a5fa'}
BAD     = {'change', 'finding', 'stop', 'off-plan', 'partial', 'none'}
E       = html.escape


def iso(t):
    return dt.datetime.fromisoformat(t.replace('Z', '+00:00'))


def name(m):
    return NAMES.get(m, m)


def wakes():
    out = []
    for f in sorted(ROOT.glob('team/*/wakes/*.json')):
        w = json.loads(f.read_text())
        st = w.get('steps', {})
        changed = sum(1 for h in w.get('history', []) if h.get('verdict') == 'change')
        out.append(dict(agent=w['agent'], at=iso(w['started']), outcome=w.get('outcome') or 'open', changed=changed,
                        v={k: st.get(k, {}).get('verdict') for k in ('plan', 'pre_review', 'work', 'post_review', 'post_check')}))
    return sorted(out, key=lambda w: w['at'])


def members():
    return sorted(p.parent.name for p in ROOT.glob('team/*/policy.json'))


def commits():
    raw = subprocess.run(['git', 'log', '--no-merges', '--since=2026-10-29T00:00:00Z', '--format=%cI\x1f%s\x1f%(trailers:key=Agent,valueonly,separator=%x2C)'],
                         cwd=ROOT, capture_output=True, text=True).stdout
    mem, out = set(members()), []
    for line in raw.splitlines():
        when, subject, trailer = (line.split('\x1f') + ['', ''])[:3]
        if subject.startswith('site v'):
            continue
        m = re.match(r'@?([\w.-]+):', subject)
        who = m.group(1).replace('.', '-') if m else None
        if who not in mem:
            who = trailer.split('@')[0].strip().replace('.', '-') if trailer.strip() else None
        if who in mem:
            out.append(dict(who=who, at=iso(when)))
    return out


def mail():
    seen, pairs = set(), {}
    for f in sorted(ROOT.glob('team/conductor/night/*.json')):
        for m in json.loads(f.read_text()).get('mail', []):
            k = (m['at'], m['sender'], m['to'])
            if k in seen:
                continue
            seen.add(k)
            a, b = m['sender'].replace('.', '-'), m['to'].replace('.', '-')
            pairs[(a, b)] = pairs.get((a, b), 0) + 1
    return pairs


def pieces():
    pace = json.loads((ROOT / 'team' / 'conductor' / 'pace.json').read_text())
    nodes = {n['id']: n for n in pace['nodes']}
    review = {e['from']: nodes.get(e['to'], {}) for e in pace['edges'] if e['kind'] == 'reviewed'}
    redo = {e['to']: e['from'] for e in pace['edges'] if e['kind'] == 'redo'}
    out = []
    for n in pace['nodes']:
        if n['kind'] != 'artifact' and n['id'] != 'ruv-b01-storyboard':
            continue
        label = 'B01 storyboard' if n['id'] == 'ruv-b01-storyboard' else n['id'][4:].upper().replace('-V', ' v')
        out.append(dict(label=label, at=n.get('at') or '2026-10-29T02:50:00Z', by=name(n.get('by', 'ruv-sgit')),
                        verdict=(review.get(n['id']) or {}).get('verdict', 'with deck for review'), redo=n['id'] in redo))
    return sorted(out, key=lambda p: p['at']), pace


# ---------------------------------------------------------------- the stage, scene by scene (canvas pixels, 1280 x 720)

def t(x, y, s, size=22, fill='#cdd5e0', a=0.0, anchor='start', weight=400, extra=''):
    return (f'<text x="{x:.0f}" y="{y:.0f}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-weight="{weight}" '
            f'data-a="{a:.2f}" {extra}>{E(s)}</text>')


def head(kicker, title, accent):
    return (t(60, 52, kicker.upper(), 20, '#8a94a6', 0, weight=800, extra='letter-spacing="2"') +
            f'<text x="60" y="104" font-size="44" fill="#f3f6fa" font-family="Georgia,serif" font-weight="700" data-a="0.15">{E(title)} '
            f'<tspan fill="#2dd4bf">{E(accent)}</tspan></text>')


def scene_team():
    s = [head('1 · The team', 'Six agents, one editor,', 'one hour each.')]
    cx, cy, r = 640, 392, 182
    s.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#2a3344" stroke-width="3" data-a="0.3"/>')
    for m in range(0, 60, 5):
        a = math.radians(m * 6 - 90)
        s.append(f'<line x1="{cx + (r - 10) * math.cos(a):.0f}" y1="{cy + (r - 10) * math.sin(a):.0f}" x2="{cx + r * math.cos(a):.0f}" '
                 f'y2="{cy + r * math.sin(a):.0f}" stroke="#2a3344" stroke-width="3" data-a="0.3"/>')
    s.append(t(cx, cy - 6, 'the editor', 26, '#f3f6fa', 0.5, 'middle', 700))
    s.append(t(cx, cy + 24, 'one human, who instructs', 20, '#8a94a6', 0.6, 'middle'))
    for i, (m, minute, role) in enumerate(SLOTS):
        a = math.radians(minute * 6 - 90)
        x, y = cx + r * math.cos(a), cy + r * math.sin(a)
        lx, ly = cx + (r + 34) * math.cos(a), cy + (r + 34) * math.sin(a)
        anchor = 'start' if math.cos(a) > 0.2 else 'end' if math.cos(a) < -0.2 else 'middle'
        dash = ' stroke-dasharray="5 4"' if m == 'storyteller' else ''
        at = 1.0 + i * 0.7
        s.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="16" fill="#2dd4bf" fill-opacity="{0.25 if m == "storyteller" else 1}" stroke="#2dd4bf" stroke-width="3"{dash} data-a="{at:.2f}" class="pop"/>')
        s.append(t(lx, ly - 4, f'{name(m)}  :{minute:02d}', 22, '#f3f6fa', at, anchor, 700))
        s.append(t(lx, ly + 22, role, 20, '#8a94a6', at + 0.1, anchor))
    s.append(t(60, 702, 'Each member is a Claude Code session with its own key, folder and policy, woken by its own hourly task.', 20, '#8a94a6', 6.2))
    return ''.join(s), 9


def scene_night(ws, cs):
    s = [head('2 · The night as it happened', 'Every wake,', 'firing up in order.')]
    t0, t1 = iso(START), max([w['at'] for w in ws] + [c['at'] for c in cs])
    span = (t1 - t0).total_seconds() or 1
    lanes = [m for m, _, _ in SLOTS if any(w['agent'] == m for w in ws)]
    x0, x1, y0, gap = 200, 1210, 190, 64
    for h in range(t0.hour + 1, t1.hour + 1):
        x = x0 + (dt.datetime(t0.year, t0.month, t0.day, h, tzinfo=dt.timezone.utc) - t0).total_seconds() / span * (x1 - x0)
        s.append(f'<line x1="{x:.0f}" y1="{y0 - 30}" x2="{x:.0f}" y2="{y0 + gap * len(lanes) - 30}" stroke="#2a3344" stroke-width="1" data-a="0.3"/>')
        s.append(t(x, y0 - 38, f'{h:02d}:00', 20, '#8a94a6', 0.3, 'middle'))
    for i, m in enumerate(lanes):
        y = y0 + i * gap
        s.append(t(x0 - 20, y + 7, name(m), 22, '#cdd5e0', 0.4, 'end', 700))
        s.append(f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="#2a3344" stroke-width="2" data-a="0.4"/>')
    dur = 11.0
    for w in ws:
        if w['agent'] not in lanes:
            continue
        frac = (w['at'] - t0).total_seconds() / span
        x, y = x0 + frac * (x1 - x0), y0 + lanes.index(w['agent']) * gap
        flagged = any(v in BAD for v in w['v'].values())
        ring = ' stroke="#fbbf24" stroke-width="3"' if flagged else ''
        s.append(f'<circle cx="{x:.0f}" cy="{y}" r="11" fill="{COLOUR.get(w["outcome"], "#8a94a6")}"{ring} data-a="{1 + frac * dur:.2f}" class="pop"/>')
    yb = y0 + gap * len(lanes) + 10
    s.append(f'<text x="60" y="{yb + 40}" font-size="28" fill="#f3f6fa" font-weight="800" data-a="0.8" data-clock="{t0.timestamp():.0f} {t1.timestamp():.0f} 1 {dur}">01:40</text>')
    s.append(f'<text x="210" y="{yb + 40}" font-size="28" fill="#2dd4bf" font-weight="800" data-a="0.8" data-count="{len(ws)}" data-at="1" data-dur="{dur}" data-suf=" wakes">0</text>')
    s.append(f'<text x="430" y="{yb + 40}" font-size="28" fill="#fbbf24" font-weight="800" data-a="0.8" data-count="{len(cs)}" data-at="1" data-dur="{dur}" data-suf=" commits">0</text>')
    s.append(t(700, yb + 40, 'teal: ok · amber: partial · grey: idle · ringed: a verdict flagged', 20, '#8a94a6', 1.0))
    return ''.join(s), 15


def scene_wake(ws):
    s = [head('3 · Inside one wake', 'Five steps,', 'two of them before any work.')]
    steps = [('plan', 'plan', 'a sub-agent plans 1 to 3 items'), ('pre_review', 'pre-review', 'security checks the plan'),
             (None, 'gate', 'work only if both say go'), ('work', 'work', 'the member, 8 minutes'),
             ('post_review', 'post-review', 'security checks the diff'), ('post_check', 'post-check', 'did it go to plan')]
    w_, x, y = 186, 50, 200
    for i, (key, label, what) in enumerate(steps):
        at = 0.8 + i * 1.0
        xx = x + i * (w_ + 18)
        col = '#a78bfa' if key is None else '#2dd4bf' if key == 'work' else '#60a5fa'
        s.append(f'<rect x="{xx}" y="{y}" width="{w_}" height="300" rx="16" fill="#161c28" stroke="{col}" stroke-width="3" data-a="{at:.2f}"/>')
        s.append(t(xx + w_ / 2, y + 44, label, 26, '#f3f6fa', at, 'middle', 800))
        lines = re.findall(r'.{1,17}(?:\s|$)', what)
        for j, ln in enumerate(lines):
            s.append(t(xx + w_ / 2, y + 80 + j * 24, ln.strip(), 20, '#8a94a6', at, 'middle'))
        counts = {}
        for w in ws:
            v = w['v'].get(key) if key else ('opened' if w['v'].get('plan') == 'go' and w['v'].get('pre_review') == 'go' else None)
            if v:
                counts[v] = counts.get(v, 0) + 1
        for j, (v, n) in enumerate(sorted(counts.items(), key=lambda kv: -kv[1])[:4]):
            c = '#fbbf24' if v in BAD else '#2dd4bf'
            s.append(f'<text x="{xx + w_ / 2:.0f}" y="{y + 190 + j * 30}" font-size="24" fill="{c}" text-anchor="middle" font-weight="800" '
                     f'data-a="{at + 0.3:.2f}" data-count="{n}" data-at="{at + 0.3:.2f}" data-dur="1" data-suf=" {E(v)}">0</text>')
        if i < len(steps) - 1:
            s.append(f'<path d="M{xx + w_ + 2} {y + 150} l14 0" stroke="#8a94a6" stroke-width="3" data-a="{at + 0.5:.2f}"/>')
    holds = sum(1 for p in ROOT.glob('team/**/HOLD.md'))
    sent_back = sum(1 for w in ws if w['changed'] or (w['v'].get('pre_review') == 'change'))
    s.append(f'<text x="{x + 1 * (w_ + 18) + w_ / 2:.0f}" y="{y + 280}" font-size="20" fill="#fbbf24" text-anchor="middle" data-a="2.4" data-count="{sent_back}" data-at="2.4" data-dur="1" data-suf=" sent back first">0</text>')
    s.append(t(60, 590, 'A stop from any step writes a HOLD file, and every member\'s next wake stops.', 22, '#cdd5e0', 7.0))
    s.append(f'<text x="60" y="650" font-size="30" fill="#2dd4bf" font-weight="800" data-a="7.4" data-count="{holds}" data-at="7.4" data-dur=".4" data-suf=" holds tonight">0</text>')
    s.append(t(420, 650, 'Defence in depth: one member\'s mistake does not become another\'s.', 22, '#8a94a6', 7.8))
    return ''.join(s), 11


def scene_flow(ps):
    s = [head('4 · How a piece moves', 'Ask, make, review,', 'redo.')]
    cols = [ps[:(len(ps) + 1) // 2], ps[(len(ps) + 1) // 2:]]
    s.append(t(60, 160, 'deck asks · ruv.sgit makes it in a run · deck reviews it · the conductor paces the next', 22, '#8a94a6', 0.4))
    i = 0
    for c, col in enumerate(cols):
        for r, p in enumerate(col):
            at = 1.0 + i * 0.75
            x, y = 60 + c * 610, 200 + r * 78
            stroke = '#fbbf24' if p['redo'] else '#2dd4bf'
            s.append(f'<rect x="{x}" y="{y}" width="190" height="58" rx="12" fill="#161c28" stroke="{stroke}" stroke-width="3" data-a="{at:.2f}" class="pop"/>')
            s.append(t(x + 95, y + 37, p['label'], 24 if len(p['label']) < 10 else 20, '#f3f6fa', at, 'middle', 800))
            s.append(f'<path d="M{x + 196} {y + 29} l40 0 m-10 -8 l10 8 l-10 8" fill="none" stroke="#8a94a6" stroke-width="3" data-a="{at + 0.3:.2f}"/>')
            verdict = p['verdict'] if len(p['verdict']) <= 32 else p['verdict'][:32].rsplit(' ', 1)[0].rstrip(',;:') + '…'
            s.append(t(x + 250, y + 26, 'deck: ' + verdict, 20, '#cdd5e0', at + 0.4))
            s.append(t(x + 250, y + 50, f'{p["by"]}, {p["at"][11:16]} UTC' + (' · a redo' if p['redo'] else ''), 20, '#8a94a6', at + 0.4))
            i += 1
    return ''.join(s), 3 + 0.75 * len(ps) + 2


def scene_talk(pairs, cs):
    s = [head('5 · The conversation', 'They talk by mail,', 'and ship by commit.')]
    who = [m for m, _, _ in SLOTS if m != 'storyteller'] + ['editor']
    cx, cy, r = 360, 420, 210
    pos = {m: (cx + r * math.cos(math.radians(i * 360 / len(who) - 90)), cy + r * math.sin(math.radians(i * 360 / len(who) - 90))) for i, m in enumerate(who)}
    top = max(pairs.values()) if pairs else 1
    for k, ((a, b), n) in enumerate(sorted(pairs.items(), key=lambda kv: -kv[1])):
        if a not in pos or b not in pos:
            continue
        (x1, y1), (x2, y2) = pos[a], pos[b]
        mx, my = (x1 + x2) / 2 + (cy - (y1 + y2) / 2) * 0.25, (y1 + y2) / 2 + ((x1 + x2) / 2 - cx) * 0.25
        s.append(f'<path d="M{x1:.0f} {y1:.0f} Q{mx:.0f} {my:.0f} {x2:.0f} {y2:.0f}" fill="none" stroke="#2dd4bf" stroke-opacity=".55" '
                 f'stroke-width="{1.5 + 7 * n / top:.1f}" data-a="{1.2 + k * 0.12:.2f}"/>')
    for m, (x, y) in pos.items():
        s.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="14" fill="{"#a78bfa" if m == "editor" else "#2dd4bf"}" data-a="0.6"/>')
        s.append(t(x, y - 24 if y < cy else y + 40, name(m), 22, '#f3f6fa', 0.6, 'middle', 700))
    total = sum(pairs.values())
    s.append(f'<text x="{cx}" y="{cy + 8}" font-size="30" fill="#f3f6fa" text-anchor="middle" font-weight="800" data-a="1" data-count="{total}" data-at="1" data-dur="2" data-suf=" letters">0</text>')
    per = {}
    for c in cs:
        per[c['who']] = per.get(c['who'], 0) + 1
    big = max(per.values()) if per else 1
    s.append(t(760, 200, 'commits per member, since midnight', 22, '#8a94a6', 2.5))
    for i, (m, n) in enumerate(sorted(per.items(), key=lambda kv: -kv[1])):
        y, at = 228 + i * 62, 3 + i * 0.4
        s.append(t(760, y + 30, name(m), 22, '#f3f6fa', at, weight=700))
        s.append(f'<rect x="900" y="{y + 8}" width="{300 * n / big:.0f}" height="30" rx="6" fill="#fbbf24" data-a="{at:.2f}" class="grow"/>')
        s.append(f'<text x="{910 + 300 * n / big:.0f}" y="{y + 32}" font-size="22" fill="#cdd5e0" data-a="{at:.2f}" data-count="{n}" data-at="{at:.2f}" data-dur="1">0</text>')
    return ''.join(s), 10


def scene_made(ws, cs, pairs, ps):
    s = [head('6 · What it made', 'In one night,', 'while the editor slept.')]
    reviews = sum(1 for p in ps if not p['verdict'].startswith('with deck'))
    notes = len([p for p in ROOT.glob('team/designer/reviews/*.md')])
    data = len(list(ROOT.glob('src/static/studio/data/*.json')))
    pages = len(subprocess.run(['git', 'log', '--since=2026-10-29T00:00:00Z', '--name-only', '--format=', '--', 'src/pages', 'src/static', 'content'],
                               cwd=ROOT, capture_output=True, text=True).stdout.split())
    tiles = [(len(ps), 'studio pieces delivered', '#2dd4bf'), (reviews, 'reviewed by deck', '#2dd4bf'), (notes, 'design notes', '#a78bfa'),
             (data, 'studio data files', '#fbbf24'), (len(ws), 'wakes, each five steps', '#60a5fa'), (len(cs), 'commits', '#fbbf24'),
             (sum(pairs.values()), 'letters in the mail vault', '#2dd4bf'), (pages, 'page and file changes', '#a78bfa')]
    for i, (n, label, c) in enumerate(tiles):
        x, y, at = 60 + (i % 4) * 300, 170 + (i // 4) * 190, 0.6 + i * 0.4
        s.append(f'<rect x="{x}" y="{y}" width="280" height="166" rx="16" fill="#161c28" stroke="#2a3344" stroke-width="2" data-a="{at:.2f}"/>')
        s.append(f'<text x="{x + 24}" y="{y + 84}" font-size="64" fill="{c}" font-weight="800" font-family="ui-monospace,Menlo,monospace" data-a="{at:.2f}" data-count="{n}" data-at="{at:.2f}" data-dur="1.4">0</text>')
        s.append(t(x + 24, y + 128, label, 20, '#cdd5e0', at))
    s.append(f'<text x="640" y="640" font-size="44" fill="#f3f6fa" text-anchor="middle" font-family="Georgia,serif" font-weight="700" data-a="4.4">'
             f'One editor. Six agents. <tspan fill="#2dd4bf">One night.</tspan></text>')
    return ''.join(s), 8


STYLE = ('<style>.td{margin:1.5em 0}.td-w{position:relative;width:100%;aspect-ratio:16/9;background:#0c0f15;border-radius:12px;overflow:hidden}'
         '.td-w:fullscreen{border-radius:0}.td-s{position:absolute;inset:0;width:100%;height:100%}.td-s .sc{display:none}.td-s .sc.on{display:inline}'
         '.td-s .pop{transform-box:fill-box;transform-origin:center}.td-s .pop.lit{animation:tdpop .6s ease-out}'
         '@keyframes tdpop{0%{transform:scale(2.4)}100%{transform:scale(1)}}'
         '.td-c{display:flex;gap:.5em;align-items:center;flex-wrap:wrap;margin-top:.6em}.td-c button{font:inherit;padding:.35em .9em;border-radius:8px;'
         'border:1px solid #8a94a666;background:transparent;color:inherit;cursor:pointer}.td-c .lbl{opacity:.8}'
         '.td-p{position:absolute;left:0;bottom:0;height:5px;width:0;background:#2dd4bf}</style>')

SCRIPT = r"""<script>
(function(){
var root=document.getElementById('td'),svg=root.querySelector('.td-s'),sc=[].slice.call(svg.querySelectorAll('.sc')),bar=root.querySelector('.td-p'),lbl=root.querySelector('.lbl');
var D=JSON.parse(document.getElementById('td-data').textContent),L=D.scenes.map(function(s){return s.len}),T0=[],tot=0;
L.forEach(function(l){T0.push(tot);tot+=l});
var paused=true,base=0,anchor=0;
function now(){return paused?base:base+(performance.now()-anchor)/1000}
function seek(t){base=Math.max(0,Math.min(tot,t));anchor=performance.now()}
function cur(t){for(var i=L.length-1;i>=0;i--){if(t>=T0[i])return i}return 0}
function fmt(n){return Math.round(n).toLocaleString('en-GB')}
function hm(s){var d=new Date(s*1000);return ('0'+d.getUTCHours()).slice(-2)+':'+('0'+d.getUTCMinutes()).slice(-2)}
var ease=function(x){x=Math.max(0,Math.min(1,x));return x<.5?2*x*x:1-Math.pow(-2*x+2,2)/2};
var last=-1,lastT=-1;
function draw(){
var t=now();if(!paused&&t>=tot){t=tot;base=t;paused=true;root.querySelector('.pp').textContent='Play'}
var i=cur(t),lt=t-T0[i];if(t>=tot){i=L.length-1;lt=L[i]}
if(i!==last){sc.forEach(function(g,k){g.classList.toggle('on',k===i)});last=i;lbl.textContent=(i+1)+' / '+L.length+'  '+D.scenes[i].name}
var g=sc[i];
[].forEach.call(g.querySelectorAll('[data-a]'),function(el){var a=+el.getAttribute('data-a'),k=ease((lt-a)/.5);el.style.opacity=k;
if(el.classList.contains('pop')){if(k>0&&!el._lit){el.classList.add('lit');el._lit=1}if(k<=0&&el._lit){el.classList.remove('lit');el._lit=0}}});
[].forEach.call(g.querySelectorAll('[data-count]'),function(el){var a=+el.getAttribute('data-at'),d=+el.getAttribute('data-dur'),v=+el.getAttribute('data-count');el.textContent=fmt(v*ease((lt-a)/d))+(el.getAttribute('data-suf')||'')});
[].forEach.call(g.querySelectorAll('[data-clock]'),function(el){var n=el.getAttribute('data-clock').split(' ').map(Number),k=Math.max(0,Math.min(1,(lt-n[2])/n[3]));el.textContent=hm(n[0]+(n[1]-n[0])*k)});
[].forEach.call(g.querySelectorAll('.grow'),function(el){if(!el._w)el._w=+el.getAttribute('width');el.setAttribute('width',(el._w*ease((lt-+el.getAttribute('data-a'))/1)).toFixed(1))});
bar.style.width=(100*t/tot)+'%';
requestAnimationFrame(draw)}
function play(){if(now()>=tot)seek(0);paused=false;anchor=performance.now();root.querySelector('.pp').textContent='Pause'}
function pause(){base=now();paused=true;root.querySelector('.pp').textContent='Play'}
function step(d){var t=now(),i=cur(t);if(d<0&&t-T0[i]<1.2&&i>0)i--;else if(d>0)i=Math.min(L.length-1,i+1);seek(d>0?T0[i]:T0[i]);if(d>0&&i===L.length-1&&t>=T0[i])seek(tot)}
root.querySelector('.pp').onclick=function(){paused?play():pause()};
root.querySelector('.bk').onclick=function(){step(-1)};
root.querySelector('.fw').onclick=function(){step(1)};
root.querySelector('.fs').onclick=function(){var w=root.querySelector('.td-w');if(document.fullscreenElement)document.exitFullscreen();else if(w.requestFullscreen)w.requestFullscreen()};
root.addEventListener('keydown',function(e){if(e.key===' '){e.preventDefault();paused?play():pause()}else if(e.key==='ArrowRight'){step(1)}else if(e.key==='ArrowLeft'){step(-1)}});
var q=new URLSearchParams(location.search);if(q.has('scene')){var n=Math.max(1,Math.min(L.length,+q.get('scene')||1));seek(T0[n-1]+L[n-1]-0.01)}
requestAnimationFrame(draw)})();
</script>"""


def main():
    ws, cs, pairs = wakes(), commits(), mail()
    ps, pace = pieces()
    scenes = [('The team', *scene_team()), ('The night', *scene_night(ws, cs)), ('Inside one wake', *scene_wake(ws)),
              ('How a piece moves', *scene_flow(ps)), ('The conversation', *scene_talk(pairs, cs)), ('What it made', *scene_made(ws, cs, pairs, ps))]
    groups = ''.join(f'<g class="sc">{markup}</g>' for _, markup, _ in scenes)
    data = json.dumps({'scenes': [{'name': n, 'len': round(l, 2)} for n, _, l in scenes],
                       'totals': {'wakes': len(ws), 'commits': len(cs), 'letters': sum(pairs.values()), 'pieces': len(ps)}}).replace('</', '<\\/')
    block = (STYLE + '<div class="td" id="td" tabindex="0" aria-label="How this talk was built, an animated mini deck: space plays and pauses, the arrows step">'
             '<div class="td-w"><svg class="td-s" viewBox="0 0 1280 720" role="img" aria-label="The team in motion, six scenes">'
             f'<rect width="1280" height="720" fill="#0c0f15"/>{groups}</svg><div class="td-p"></div></div>'
             '<div class="td-c"><button class="bk" type="button">Back</button><button class="pp" type="button">Play</button>'
             '<button class="fw" type="button">Next</button><button class="fs" type="button">Full screen</button><span class="lbl"></span></div></div>'
             f'<script type="application/json" id="td-data">{data}</script>' + SCRIPT.strip())
    block = '\n'.join(line for line in block.split('\n') if line.strip())
    assert '{{' not in block and chr(0x2014) not in block
    now = dt.datetime.now(dt.timezone.utc)
    text = '\n'.join([
        '---',
        'title: How this talk was built: the team in motion',
        'kicker: The team',
        f'date: {now.date().isoformat()}',
        'author: conductor@the-ultimate-insider, generated by admin/tools/workflow_deck.py',
        'minutes: 3',
        'description: A mini deck, animated from the team\'s own records: seven agents and one editor building this talk overnight, every wake, every review and every letter.',
        f'abstract: The site and the talk were built by a team of agents working through the night on an hourly schedule, each wake checked twice before and twice after its work. This mini deck replays it from the team\'s public records: {len(ws)} wakes, {len(cs)} commits, {sum(pairs.values())} letters and {len(ps)} studio pieces, as of {now.strftime("%H:%M")} UTC.',
        '---', '',
        'Press Play, or use the arrow keys after clicking the stage. Back and Next step through the six scenes; Full screen fills the screen for presenting.', '',
        block, '',
        '## How this is made', '',
        '`admin/tools/workflow_deck.py` reads the team\'s public records and nothing else: every wake record (`team/*/wakes/*.json`), the commits each member marked as its own, the pace graph (`team/conductor/pace.json`), the night log\'s snapshots (who wrote to whom, counted, never what was written) and the schedule. Every number on the stage is computed by it, and it is rerun as the work goes on. The night, hour by hour, with screenshots of each piece, is in [the night log](the-night-hour-by-hour.html); how the team runs is in [the conductor\'s guide](running-this-agent-team.html).', ''])
    ARTICLE.write_text(text)
    print('wrote', ARTICLE.relative_to(ROOT), f'({len(ws)} wakes, {len(cs)} commits, {sum(pairs.values())} letters, {len(ps)} pieces)')


if __name__ == '__main__':
    main()
