#!/usr/bin/env python3
"""The night, hour by hour: one snapshot per run, the article regenerated from all of them.

    python3 admin/tools/night_log.py --mail <tui-mail-public clone> [--no-shots] [--since <ISO UTC>]

Each run covers the time since the last snapshot (the first from the schedule's start), and writes
team/conductor/night/<YYYYMMDDTHHMM>.json: every wake record started in the window, the commits each
member marked as its own, the pages its work changed (with screenshots of up to four, taken from a
local build), the mail counted by its headers, and the problems the records show. It then rewrites
content/articles/the-night-hour-by-hour.md from every snapshot, newest first, with a grid of all wakes.

Every number in the article comes from these files; nothing is typed. Mail is counted by headers
(From, To, Date, Subject, X-Kind); bodies are never read. No page that shows a key is photographed.
Kept by conductor@the-ultimate-insider.
"""
import argparse, datetime as dt, email.utils, functools, glob, http.server, json, re, subprocess, sys, threading
from pathlib import Path

ROOT    = Path(__file__).resolve().parents[2]
NIGHT   = ROOT / 'team' / 'conductor' / 'night'
IMG     = ROOT / 'team' / 'conductor' / 'debriefs' / 'img'
ARTICLE = ROOT / 'content' / 'articles' / 'the-night-hour-by-hour.md'
START   = '2026-10-29T01:40:00Z'                                   # the schedule's first hour (schedule.json)
SLOTS   = {'conductor': 2, 'researcher': 9, 'deck': 17, 'ruv-sgit': 32, 'designer': 39, 'dev': 47}
NO_SHOT = re.compile(r'(^admin/keys|key|qr|vault-qr|^team/)', re.I)   # never photograph a page that shows a key
BAD     = {'change', 'finding', 'stop', 'off-plan', 'partial', 'none'}
COLOUR  = {'ok': '#2f9e6b', 'partial': '#d9a521', 'idle': '#8a94a6', 'failed': '#d0463b', 'hold': '#7a2fb5', 'open': '#4a7bd0'}


def iso(t):
    return dt.datetime.fromisoformat(t.replace('Z', '+00:00'))


def z(t):
    return t.astimezone(dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def members():
    return sorted(p.parent.name for p in ROOT.glob('team/*/policy.json'))


def wakes(since=None, until=None):
    out = []
    for f in sorted(ROOT.glob('team/*/wakes/*.json')):
        w = json.loads(f.read_text())
        t = iso(w['started'])
        if (since and t < since) or (until and t >= until):
            continue
        steps = w.get('steps', {})
        out.append(dict(agent=w['agent'], started=w['started'], kind=w.get('kind', ''), outcome=w.get('outcome') or 'open',
                        record=str(f.relative_to(ROOT)),
                        verdicts={k: steps.get(k, {}).get('verdict') for k in ('plan', 'pre_review', 'work', 'post_review', 'post_check')},
                        plan=(steps.get('plan', {}).get('comment') or '')[:400]))
    return out


def git(*args):
    return subprocess.run(['git', *args], cwd=ROOT, capture_output=True, text=True).stdout


def commits(since, until):
    out, raw = [], git('log', f'--since={z(since)}', f'--until={z(until)}', '--no-merges', '--name-only',
                       '--format=\x1e%H\x1f%cI\x1f%s\x1f%(trailers:key=Agent,valueonly,separator=%x2C)')
    for chunk in raw.split('\x1e')[1:]:
        head, _, files = chunk.partition('\n')
        sha, when, subject, trailer = (head.split('\x1f') + [''] * 4)[:4]
        m = re.match(r'@([\w.-]+):', subject)
        who = m.group(1).replace('.', '-') if m else (trailer.split('@')[0].strip().replace('.', '-') if trailer.strip() else None)
        if not who or subject.startswith('site v'):
            continue
        out.append(dict(agent=who, sha=sha[:7], at=when, subject=subject, files=[f for f in files.split('\n') if f.strip()]))
    return out


def url_of(path):                                                  # the page a changed source file shows up on
    p = Path(path)
    if path.startswith('src/pages/') and p.suffix == '.html':
        return str(p.relative_to('src/pages'))
    if path.startswith('src/static/') and p.suffix == '.html':
        return str(p.relative_to('src/static'))
    if path.startswith('content/articles/') and p.suffix == '.md' and p.stem != ARTICLE.stem:
        return f'articles/{p.stem}.html'
    return None


def mail(clone, since, until):
    seen, out = set(), []
    if not clone:
        return out
    for f in sorted(Path(clone).glob('**/*.eml')):
        if '.sg_vault' in f.parts:
            continue
        head = {}
        for line in f.read_text(errors='replace').split('\n'):
            if not line.strip():
                break                                              # headers only: the body is never read
            k, _, v = line.partition(':')
            if k.lower() in ('from', 'to', 'date', 'subject', 'x-kind'):
                head[k.lower()] = v.strip()
        try:
            t = email.utils.parsedate_to_datetime(head['date'])
        except (KeyError, TypeError, ValueError):
            continue
        key = (head.get('from'), head.get('to'), head.get('date'), head.get('subject'))
        if key in seen or not (since <= t < until):
            continue
        seen.add(key)
        name = lambda a: (a or '').split('@')[0]
        out.append(dict(at=z(t), sender=name(head.get('from')), to=name(head.get('to')), kind=head.get('x-kind', ''), subject=head.get('subject', '')))
    return sorted(out, key=lambda m: m['at'])


def shoot(pages, tag):
    if not pages:
        return []
    subprocess.run([sys.executable, 'admin/build/build.py'], cwd=ROOT, check=True, capture_output=True)
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a):
            pass
    handler = functools.partial(Quiet, directory=str(ROOT / '_site'))
    srv = http.server.ThreadingHTTPServer(('127.0.0.1', 0), handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    js = ("const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1280,height:800}});"
          "for(const [u,o] of JSON.parse(process.argv[1])){try{await p.goto(u,{waitUntil:'load',timeout:15000});await p.waitForTimeout(1200);"
          "await p.screenshot({path:o});}catch(e){console.error('miss',u)}}await b.close();})();")
    IMG.mkdir(parents=True, exist_ok=True)
    jobs = [(f'http://127.0.0.1:{srv.server_port}/{u}' + ('?static' if '/lab/' in u or '/slides/' in u else ''), str(IMG / f'night-{tag}-{n}.png')) for n, u in enumerate(pages, 1)]
    subprocess.run(['node', '-e', js, json.dumps(jobs)], cwd=ROOT, capture_output=True, text=True)
    srv.shutdown()
    return [dict(page=u, img=Path(o).name) for (_, o), u in zip(jobs, pages) if Path(o).exists()]


def snapshot(args):
    NIGHT.mkdir(parents=True, exist_ok=True)
    prior = sorted(NIGHT.glob('*.json'))
    since = iso(args.since) if args.since else (iso(json.loads(prior[-1].read_text())['until']) if prior else iso(START))
    until = dt.datetime.now(dt.timezone.utc).replace(microsecond=0)
    tag   = until.strftime('%Y%m%dT%H%M')
    ws, cs = wakes(since, until), commits(since, until)
    made, pages = {}, []
    for c in cs:
        for f in c['files']:
            u = url_of(f)
            if u and not NO_SHOT.search(u) and u not in made:
                made[u] = c['agent']
                pages.append(u)
    rank  = lambda u: (0 if '/lab/' in u else 1 if u.startswith('articles/') else 2 if u.count('/') > 1 else 3)
    shots = [] if args.no_shots else shoot(sorted(pages, key=rank)[:4], tag)
    problems = []
    for w in ws:
        bad = {k: v for k, v in w['verdicts'].items() if v in BAD}
        if w['outcome'] not in ('ok', 'open') or bad:
            problems.append(dict(agent=w['agent'], started=w['started'], outcome=w['outcome'], verdicts=bad, record=w['record']))
    holds = [str(p.relative_to(ROOT)) for p in ROOT.glob('team/**/HOLD.md')]
    snap = dict(schema='the-ultimate-insider/night/v1', since=z(since), until=z(until), wakes=ws,
                commits=[{k: v for k, v in c.items() if k != 'files'} | {'changed': len(c['files'])} for c in cs],
                made=[dict(page=u, by=made[u]) for u in pages], shots=shots, mail=mail(args.mail, since, until),
                problems=problems, holds=holds,
                asks={m: json.loads((ROOT / 'team' / m / 'status.json').read_text()).get('asks', [])
                      for m in members() if (ROOT / 'team' / m / 'status.json').exists()})
    (NIGHT / f'{tag}.json').write_text(json.dumps(snap, indent=1) + '\n')
    return tag


def grid():                                                        # every wake so far: members by hour, coloured by outcome
    ws = wakes()
    if not ws:
        return ''
    first = iso(START).replace(minute=0, second=0)
    last  = max(iso(w['started']) for w in ws).replace(minute=0, second=0)
    hours = int((last - first).total_seconds() // 3600) + 1
    names = members()
    cw, ch, lw, top = 74, 34, 96, 26
    w_, h_ = lw + hours * cw + 8, top + len(names) * ch + 30
    s = ['<style>.night-grid svg{max-width:100%;height:auto}.night-collage{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:12px;margin:1em 0}'
         '.night-collage figure{margin:0}.night-collage img{width:100%;border:1px solid #8a94a666;border-radius:6px}.night-collage figcaption{font-size:.8em;opacity:.75}</style>'
         f'<figure class="night-grid"><svg viewBox="0 0 {w_} {h_}" width="100%" role="img" aria-label="Every wake of the night, members by hour, coloured by outcome">']
    for i in range(hours):
        s.append(f'<text x="{lw + i * cw + cw / 2}" y="16" text-anchor="middle" font-size="12" fill="currentColor">{(first + dt.timedelta(hours=i)).strftime("%H:00")}</text>')
    for r, m in enumerate(names):
        y = top + r * ch
        s.append(f'<text x="{lw - 8}" y="{y + ch / 2 + 4}" text-anchor="end" font-size="12" fill="currentColor">{m}</text>')
        for i in range(hours):
            cell = [w for w in ws if w['agent'] == m and int((iso(w['started']).replace(minute=0, second=0) - first).total_seconds() // 3600) == i]
            x = lw + i * cw + 3
            if not cell:
                s.append(f'<rect x="{x}" y="{y + 3}" width="{cw - 6}" height="{ch - 6}" rx="4" fill="none" stroke="#8a94a6" stroke-dasharray="3 3"/>')
                continue
            worst = next((o for o in ('hold', 'failed', 'partial', 'open', 'idle', 'ok') if any(w['outcome'] == o for w in cell)), 'ok')
            flags = sum(1 for w in cell for v in w['verdicts'].values() if v in BAD)
            s.append(f'<rect x="{x}" y="{y + 3}" width="{cw - 6}" height="{ch - 6}" rx="4" fill="{COLOUR.get(worst, "#8a94a6")}"><title>{m} {(first + dt.timedelta(hours=i)).strftime("%H:00")}: {len(cell)} wake(s), {worst}, {flags} flag(s)</title></rect>')
            s.append(f'<text x="{x + (cw - 6) / 2}" y="{y + ch / 2 + 4}" text-anchor="middle" font-size="12" fill="#fff">{len(cell)}{" ⚑" + str(flags) if flags else ""}</text>')
    lx = lw
    for o in ('ok', 'partial', 'open', 'idle', 'failed', 'hold'):
        s.append(f'<rect x="{lx}" y="{h_ - 18}" width="12" height="12" rx="2" fill="{COLOUR[o]}"/><text x="{lx + 16}" y="{h_ - 8}" font-size="11" fill="currentColor">{o}</text>')
        lx += 74
    s.append('</svg><figcaption>Every wake record so far, by member and hour (UTC). The number is the wakes that hour; ⚑ counts verdicts other than go, clean, done or as-planned. A dashed cell is an hour with no wake.</figcaption></figure>')
    return ''.join(s)


def row(cells):
    return '| ' + ' | '.join(str(c).replace('|', '/').replace('\n', ' ') for c in cells) + ' |'


def section(snap):
    since, until = iso(snap['since']), iso(snap['until'])
    out = [f'## {since.strftime("%H:%M")} to {until.strftime("%H:%M")} UTC', '']
    ws = snap['wakes']
    who = sorted({w['agent'] for w in ws})
    out.append(f'{len(ws)} wakes by {len(who)} members, {len(snap["commits"])} commits, {len(snap["made"])} pages changed, '
               f'{len(snap["mail"])} messages, {len(snap["problems"])} wakes with a flag, {len(snap["holds"])} holds.')
    out.append('')
    if ws:
        out += ['### The wakes', '', row(['Member', 'Started', 'Kind', 'Plan', 'Pre', 'Work', 'Post', 'Check', 'Outcome']), row(['---'] * 9)]
        for w in ws:
            v = w['verdicts']
            out.append(row([w['agent'], w['started'][11:16], w['kind'], *(v[k] or '-' for k in ('plan', 'pre_review', 'work', 'post_review', 'post_check')),
                            w['outcome']]))
        out.append('')
        out += ['What each planned, in its own record:', '']
        for w in ws:
            if w['plan']:
                out.append(f'- **{w["agent"]}, {w["started"][11:16]}**: {w["plan"].rstrip()}{"..." if len(w["plan"]) >= 400 else ""}')
        out.append('')
    if snap['made']:
        out += ['### What was made', '']
        for m in snap['made']:
            out.append(f'- [{m["page"]}](../{m["page"]}), by {m["by"]}')
        out.append('')
    if snap['shots']:
        figs = ''.join(f'<figure><a href="../{s["page"]}"><img src="../team/conductor/debriefs/img/{s["img"]}" alt="Screenshot of {s["page"]}" loading="lazy"></a><figcaption>{s["page"]}</figcaption></figure>'
                       for s in snap['shots'])
        out += [f'<div class="night-collage">{figs}</div>', '']
    if snap['commits']:
        out += ['### Commits', '']
        for c in snap['commits']:
            out.append(f'- `{c["sha"]}` {c["at"][11:16]} {c["subject"]}')
        out.append('')
    if snap['mail']:
        out += ['### Messages', '', row(['At', 'From', 'To', 'Kind', 'Subject']), row(['---'] * 5)]
        for m in snap['mail']:
            out.append(row([m['at'][11:16], m['sender'], m['to'], m['kind'], m['subject']]))
        out.append('')
    out += ['### Problems', '']
    if snap['problems']:
        for p in snap['problems']:
            flags = ', '.join(f'{k} {v}' for k, v in p['verdicts'].items()) or 'no step flagged'
            out.append(f'- **{p["agent"]}, {p["started"][11:16]}**: outcome {p["outcome"]}; {flags} (`{p["record"]}`)')
    else:
        out.append('- None in the records.')
    if snap['holds']:
        out.append('- **Hold**: ' + ', '.join(f'`{h}`' for h in snap['holds']))
    out.append('')
    return out


def article():
    snaps = [json.loads(p.read_text()) for p in sorted(NIGHT.glob('*.json'))]
    every = wakes()
    latest = snaps[-1]
    flagged = sum(1 for w in every for v in w['verdicts'].values() if v in BAD)
    outcomes = {}
    for w in every:
        outcomes[w['outcome']] = outcomes.get(w['outcome'], 0) + 1
    asks = [(m, a) for m, xs in latest['asks'].items() for a in xs if 'editor' in str(a.get('from', ''))]
    head = ['---',
            'title: The night, hour by hour',
            'kicker: The team',
            f'date: {latest["until"][:10]}',
            'author: conductor@the-ultimate-insider, generated by admin/tools/night_log.py',
            f'minutes: {max(3, len(snaps) * 2)}',
            "description: What the agent team did overnight, hour by hour: every wake and its five verdicts, what each member made, with screenshots, the messages between members, and what went wrong.",
            f"abstract: The team of agents behind this site works through the night on an hourly schedule while the editor sleeps. This log is regenerated after each round from the team's own records: {len(every)} wakes so far, {len({w['agent'] for w in every})} members, editions so far: {len(snaps)}. Nothing in it is typed by hand.",
            '---', '']
    body = ['## At a glance', '',
            f'Last edition {latest["until"][11:16]} UTC. Since {START[11:16]} UTC: **{len(every)} wakes** by **{len({w["agent"] for w in every})} members**, '
            + ', '.join(f'{n} {o}' for o, n in sorted(outcomes.items())) + f'; **{flagged} verdicts** other than go, clean, done or as-planned; '
            f'**{len(latest["holds"])} holds** now. Each member wakes hourly at its own minute: '
            + ', '.join(f'{m} :{SLOTS[m]:02d}' for m in sorted(SLOTS, key=SLOTS.get) if m in members()) + '.', '',
            grid(), '',
            '## Waiting on the editor', '',
            'What each member asks of the editor, from its `status.json` at the latest edition:', '']
    body += [f'- **{m}**: {a["what"]}' for m, a in asks] or ['- Nothing.']
    body += ['']
    for s in reversed(snaps):
        body += section(s)
    body += ['## How this is made', '',
             'After each round the conductor runs `python3 admin/tools/night_log.py --mail <its clone of tui-mail-public>`. '
             'It reads every wake record (`team/*/wakes/*.json`), the commits each member marked as its own (`@<id>:` or the `Agent:` trailer), '
             'the headers of the messages in the public mail vault (never their bodies), and each member\'s `status.json`; it builds the site and '
             'photographs up to four pages that changed in the hour, never a page that shows a key. Each run is kept as `team/conductor/night/<time>.json`, '
             'and this article is rewritten from all of them. The protocol behind the verdicts is in [the guide](running-this-agent-team.html).', '']
    ARTICLE.write_text('\n'.join(head + body))


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--mail', help='a clone of tui-mail-public, read for headers only')
    ap.add_argument('--since', help='start of the window (ISO UTC); default: the end of the last snapshot')
    ap.add_argument('--no-shots', action='store_true', help='skip the screenshots')
    ap.add_argument('--article-only', action='store_true', help='rewrite the article from the snapshots, take none')
    args = ap.parse_args()
    if not args.article_only:
        print('snapshot', snapshot(args))
    article()
    print('wrote', ARTICLE.relative_to(ROOT))


if __name__ == '__main__':
    main()
