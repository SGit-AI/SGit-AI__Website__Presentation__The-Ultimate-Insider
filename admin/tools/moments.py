#!/usr/bin/env python3
"""Moments: what changed, run by run, each opening on what you need to know.

    python3 admin/tools/moments.py

The editor's ask (29 October 2026), after php.oct.2026.newsroom.sgit.ai's day by day: a strip of moments instead
of days. A moment is one of the conductor's hourly snapshots (team/conductor/night/*.json), or, when one window
holds more than 25 commits, a batch. Each opens on what you need to know (the conductor's own one-line pace log
for that window), then what changed (every commit, tagged), the screenshots of that run, the mail as counts, and
where it stood at the end. The open window since the last snapshot is a moment too, computed but not saved.

Reads only public records; renders only counts, ids, verdicts, slot names, short escaped commit subjects and the
conductor's own log lines; never a key, a QR image, an address, a mail body or a wake comment.
Kept by conductor@the-ultimate-insider; night_log.py calls it at the end of every run.
"""
import datetime as dt, json, re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import night_log as nl                                              # one way to read wakes and commits

ROOT    = nl.ROOT
ARTICLE = ROOT / 'content' / 'articles' / 'moments.md'
PACE    = ROOT / 'team' / 'conductor' / 'pace.json'
STATUS  = ROOT / 'team' / 'conductor' / 'status.json'
BATCH   = 25                                                        # commits in one window that make it a batch


def tag(files):
    if any(f.endswith('key.json') for f in files):
        return 'KEYS'
    if any(f.startswith(('src/static/studio/lab', 'src/static/ruv-sgit', 'src/pages/ruv-sgit')) for f in files):
        return 'NEW PIECE'
    if any(f.startswith(('src/pages/studio/reviews', 'src/static/studio/reviews')) for f in files):
        return 'REVIEW'
    if any(f.startswith('team/designer') for f in files):
        return 'DESIGN'
    if any(f.startswith(('admin/build', 'src/static/assets', 'src/static/talk')) for f in files):
        return 'BUILD'
    return 'WORK'


def short(s, n=110):
    s = ' '.join(s.split())
    return s if len(s) <= n else s[:n - 3].rstrip() + '...'


def moment(since, until, snap=None, pace=None, logs=()):
    ws = nl.wakes(since, until)
    cs = nl.commits(since, until)
    items = [dict(at=c['at'][11:16], who=c['agent'], tag=tag(c['files']), text=short(re.sub(r'^@?[\w.-]+:\s*', '', c['subject']))) for c in reversed(cs)]
    log = [l.get('what') or l.get('line', '') for l in logs]
    problems = []
    for w in ws:
        bad = [f'{k} {v}' for k, v in w['verdicts'].items() if v in nl.BAD]
        if w['outcome'] not in ('ok', 'open') or bad:
            problems.append(f"{w['agent']} {w['started'][11:16]}: {w['outcome']}" + (f" ({', '.join(bad)})" if bad else ''))
    mail = {}
    for m in (snap or {}).get('mail', []):                          # headers only, and only who wrote to whom
        k = f"{m['sender']} to {m['to']}"
        mail[k] = mail.get(k, 0) + 1
    shots = [dict(img=s['img'], page=s['page']) for s in (snap or {}).get('shots', [])
             if (nl.IMG / s['img']).exists() and not nl.NO_SHOT.search(s['page'])]
    every = nl.wakes(None, until)
    arts  = [n for n in (pace or {}).get('nodes', []) if n.get('kind') == 'artifact' and n.get('at') and nl.iso(n['at']) < until]
    revs  = [n for n in (pace or {}).get('nodes', []) if n.get('kind') == 'review']
    label = (f"Batch {since.strftime('%H:%M')} to {until.strftime('%H:%M')}" if len(cs) > BATCH
             else f"Run {until.strftime('%H:%M')}")
    if log:
        head = '; '.join(log)
    else:
        n = lambda k, w: f"{k} {w}{'' if k == 1 else 's'}"
        head = f"{n(len(ws), 'wake')}, {n(sum(1 for i in items if i['tag'] == 'NEW PIECE'), 'commit')} making pieces, {n(len(problems), 'flag')}."
    return dict(id=until.strftime('%H%M'), label=label, since=nl.z(since)[11:16], until=nl.z(until)[11:16],
                wakes=len(ws), commits=len(cs), problems=problems, head=head, items=items,
                shots=shots, mail=sorted(mail.items(), key=lambda kv: -kv[1]),
                stood=dict(holds=len((snap or {}).get('holds', [])), wakes=len(every),
                           ok=sum(1 for w in every if w['outcome'] == 'ok'),
                           pieces=len(arts), reviews=len(revs)),
                open=snap is None)


def build():
    pace  = json.loads(PACE.read_text()) if PACE.exists() else {}
    snaps = [json.loads(p.read_text()) for p in sorted(nl.NIGHT.glob('*.json'))]
    now  = dt.datetime.now(dt.timezone.utc).replace(microsecond=0)
    ends = [nl.iso(s['until']) for s in snaps] + [now]
    logs = [[] for _ in ends]
    for l in (pace or {}).get('log', []):                           # a log line belongs to the first moment ending after it
        t = nl.iso(l['at'])
        i = next((i for i, e in enumerate(ends) if t <= e + dt.timedelta(minutes=5)), len(ends) - 1)
        logs[i].append(l)
    ms = [moment(nl.iso(s['since']), nl.iso(s['until']), s, pace, logs[i]) for i, s in enumerate(snaps)]
    last = nl.iso(snaps[-1]['until']) if snaps else nl.iso(nl.START)
    if (now - last).total_seconds() > 20 * 60:
        m = moment(last, now, None, pace, logs[-1])
        m['label'] = 'Now'
        ms.append(m)
    if ms:
        st = json.loads(STATUS.read_text()) if STATUS.exists() else {}
        ms[-1]['waits'] = [a.get('what', '') for a in st.get('asks', [])]
    return ms


CSS = ('.mo{width:min(1200px,94vw);margin:1.5em 0 1.5em 50%;transform:translateX(-50%);font-size:16px}'
       '.mo *{box-sizing:border-box}'
       '.mo-strip{display:flex;gap:8px;overflow-x:auto;padding:4px 2px 10px}'
       '.mo-card{flex:0 0 112px;border:1px solid #8a94a666;border-radius:10px;padding:8px 10px;background:none;color:inherit;font:inherit;font-size:14px;text-align:left;cursor:pointer;position:relative}'
       '.mo-card[aria-pressed=true]{border:2px solid currentColor}'
       '.mo-card b{display:block;font-size:15px}.mo-card span{display:block;opacity:.75}'
       '.mo-bars{display:flex;align-items:flex-end;gap:4px;height:34px;margin-bottom:6px}'
       '.mo-bars i{display:block;width:12px;border-radius:2px 2px 0 0;background:#2f9e6b}.mo-bars i+i{background:#8a94a6}'
       '.mo-flag{position:absolute;top:8px;right:8px;width:9px;height:9px;border-radius:50%;background:#d9a521}'
       '.mo-head{display:grid;grid-template-columns:auto 1fr;gap:4px 20px;align-items:start;margin:18px 0 6px}'
       '.mo-head .k{font-size:14px;letter-spacing:.06em;text-transform:uppercase;opacity:.75}'
       '.mo-head h2{margin:0;font-size:clamp(20px,2.6vw,30px);line-height:1.25}'
       '.mo-sub{font-size:15px;opacity:.8;margin:6px 0 14px}'
       '.mo-cols{display:grid;grid-template-columns:minmax(0,1.6fr) minmax(0,1fr);gap:28px}'
       '@media (max-width:760px){.mo-cols{grid-template-columns:1fr}.mo-head{grid-template-columns:1fr}}'
       '.mo h3{font-size:14px;letter-spacing:.06em;text-transform:uppercase;opacity:.75;margin:10px 0 8px}'
       '.mo-item{display:grid;grid-template-columns:48px 1fr;gap:10px;padding:7px 0;border-top:1px solid #8a94a633;font-size:15px}'
       '.mo-item time{font-family:ui-monospace,monospace;opacity:.75}'
       '.mo-tag{display:inline-block;font-size:12px;font-weight:700;letter-spacing:.05em;padding:1px 6px;border-radius:4px;border:1px solid currentColor;margin-right:6px}'
       '.mo-who{opacity:.75;font-size:14px}'
       '.mo-stat{border:1px solid #8a94a666;border-radius:10px;padding:10px 12px;margin-bottom:10px}'
       '.mo-stat .k{font-size:13px;letter-spacing:.06em;text-transform:uppercase;opacity:.75}'
       '.mo-stat .v{font-size:22px;font-weight:700}.mo-stat li{font-size:15px}'
       '.mo-shots{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:10px}'
       '.mo-shots img{width:100%;border:1px solid #8a94a666;border-radius:6px}.mo-shots figure{margin:0;font-size:14px}'
       '.mo-more{background:none;border:1px solid #8a94a666;border-radius:6px;color:inherit;font:inherit;font-size:14px;padding:4px 10px;cursor:pointer;margin-top:6px}')

JS = r"""(function(){
var D=JSON.parse(document.getElementById('mo-data').textContent),root=document.getElementById('mo');
function el(t,c,x){var e=document.createElement(t);if(c)e.className=c;if(x!=null)e.textContent=x;return e}
var strip=el('div','mo-strip'),view=el('div');root.appendChild(strip);root.appendChild(view);
var mw=Math.max.apply(null,D.map(function(m){return m.wakes}).concat([1])),mc=Math.max.apply(null,D.map(function(m){return m.commits}).concat([1]));
var cards=D.map(function(m,i){var b=el('button','mo-card');b.type='button';b.setAttribute('aria-pressed','false');
 var bars=el('div','mo-bars'),a=el('i'),c=el('i');a.style.height=(4+30*m.wakes/mw)+'px';c.style.height=(4+30*m.commits/mc)+'px';a.title=m.wakes+' wakes';c.title=m.commits+' commits';bars.appendChild(a);bars.appendChild(c);b.appendChild(bars);
 b.appendChild(el('b',null,m.label));b.appendChild(el('span',null,m.since+' to '+m.until));if(m.problems.length){var f=el('i','mo-flag');f.title=m.problems.length+' flagged';b.appendChild(f)}
 b.addEventListener('click',function(){location.hash='m'+m.id;show(i)});strip.appendChild(b);return b});
function stat(k,v,list){var s=el('div','mo-stat');s.appendChild(el('div','k',k));if(v!=null)s.appendChild(el('div','v',v));if(list){var u=el('ul');list.forEach(function(x){u.appendChild(el('li',null,x))});s.appendChild(u)}return s}
function show(i){var m=D[i];cards.forEach(function(c,j){c.setAttribute('aria-pressed',j===i?'true':'false')});cards[i].scrollIntoView({block:'nearest',inline:'nearest'});
 view.textContent='';var h=el('div','mo-head');h.appendChild(el('div','k',m.open?'Now':'Moment'));h.appendChild(el('h2',null,m.head));view.appendChild(h);
 view.appendChild(el('p','mo-sub',m.label+' · '+m.since+' to '+m.until+' UTC · '+m.wakes+' wakes · '+m.commits+' commits'+(m.problems.length?' · '+m.problems.length+' flagged':'')));
 var cols=el('div','mo-cols'),L=el('div'),R=el('div');cols.appendChild(L);cols.appendChild(R);view.appendChild(cols);
 L.appendChild(el('h3',null,'What changed in this moment'));var shown=0,box=el('div');L.appendChild(box);
 function add(n){m.items.slice(shown,shown+n).forEach(function(it){var r=el('div','mo-item');r.appendChild(el('time',null,it.at));var d=el('div');d.appendChild(el('span','mo-tag',it.tag));d.appendChild(document.createTextNode(it.text+' '));d.appendChild(el('span','mo-who',it.who));r.appendChild(d);box.appendChild(r)});shown+=n}
 add(14);if(m.items.length>shown){var more=el('button','mo-more','Show all '+m.items.length);more.type='button';more.addEventListener('click',function(){add(1e4);more.remove()});L.appendChild(more)}
 if(!m.items.length)L.appendChild(el('p',null,'No commits in this moment.'));
 if(m.shots.length){L.appendChild(el('h3',null,'What it looked like'));var g=el('div','mo-shots');m.shots.forEach(function(s){var f=el('figure'),a=el('a'),im=el('img');a.href='../'+s.page;im.src='../team/conductor/debriefs/img/'+s.img;im.alt='Screenshot of '+s.page;im.loading='lazy';a.appendChild(im);f.appendChild(a);f.appendChild(el('figcaption',null,s.page));g.appendChild(f)});L.appendChild(g)}
 R.appendChild(el('h3',null,'Where it stood at the end'));var S=m.stood;
 R.appendChild(stat('Holds',S.holds?S.holds+' held':'None'));R.appendChild(stat('Wakes so far',S.wakes+' ('+S.ok+' ok)'));R.appendChild(stat('Studio pieces delivered so far',String(S.pieces)));
 R.appendChild(stat('Flagged in this moment',m.problems.length?null:'None',m.problems.length?m.problems:null));
 if(m.mail.length)R.appendChild(stat('Letters in this moment',null,m.mail.map(function(kv){return kv[0]+': '+kv[1]})));
 if(m.waits&&m.waits.length)R.appendChild(stat('Waits on the editor',null,m.waits))}
function fromHash(){var id=location.hash.replace('#m','');for(var i=0;i<D.length;i++)if(D[i].id===id)return i;return D.length-1}
show(fromHash());addEventListener('hashchange',function(){show(fromHash())});
})();"""


def article(ms):
    data = json.dumps(ms, ensure_ascii=True, separators=(',', ':')).replace('</', '<\\/')
    total_w = ms[-1]['stood']['wakes'] if ms else 0
    block = (f'<div class="mo" id="mo"><style>{CSS}</style>'
             f'<script type="application/json" id="mo-data">{data}</script>'
             f'<noscript>{len(ms)} moments; the page needs JavaScript to open them.</noscript>'
             f'<script>{JS}</script></div>')
    assert '\n\n' not in block and '{{' not in block and chr(0x2014) not in block
    head = ['---',
            'title: Moments: what changed, run by run',
            'kicker: The team',
            f'date: {dt.date.today().isoformat()}',
            'author: conductor@the-ultimate-insider, generated by admin/tools/moments.py',
            'minutes: 3',
            'description: The team behind this talk, moment by moment: each hourly run or batch of work, what you need to know about it, what changed, and where things stood at the end.',
            f'abstract: Pick a moment on the strip: an hourly run of the agent team, or a batch of work. It opens on what you need to know, then every change in it, tagged, with screenshots, and where things stood when it ended. {len(ms)} moments and {total_w} wakes so far; nothing here is typed by hand.',
            '---', '',
            'Each card is a moment: an hourly run of the team, or a batch when one window holds more than 25 commits. The green bar is wakes, the grey one commits; a yellow dot means a step flagged something. The newest opens first.', '',
            block, '',
            '## How this is made', '',
            "`admin/tools/moments.py` reads the conductor's hourly snapshots (`team/conductor/night/`), its own one-line pace log, every wake record and the commits each member marked as its own; the headline of each moment is the conductor's log line for that window. Letters are counted by who wrote to whom, never read. It is rewritten at the end of every conductor run, with [the night, hour by hour](the-night-hour-by-hour.html), its longer companion.", '']
    ARTICLE.write_text('\n'.join(head))


def main():
    ms = build()
    article(ms)
    print('wrote', ARTICLE.relative_to(ROOT), f'({len(ms)} moments)')


if __name__ == '__main__':
    main()
