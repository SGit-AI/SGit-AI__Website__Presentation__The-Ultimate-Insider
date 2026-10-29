# Locks one part of the talk (conductor 034, the editor at 16:55 London): a frozen copy of everything that part's slides
# load, taken from the built site, never rebuilt from changed sources. The player plays a locked part from its copy.
#
#   python3 admin/build/build.py && python3 admin/build/lock.py --part 1
#
# Opens each of the part's slides in Chromium (Playwright) from _site, records every same-origin file it loads, and copies
# those files (and each slide's whole folder) into src/static/talk/engine/locked/part<N>/, the site's tree mirrored, so
# every relative path holds. Writes part<N>/beats.json (the beats as they are in talk.json now, src pointing at the copy)
# and adds the part to talk/engine/locked/locks.json. A slide outside the slide areas (an article) stays live, said in the
# lock. Refuses to lock a part twice: a locked part is never changed again. Stdlib and Node's Playwright. Apache-2.0.

import argparse, datetime, http.server, json, posixpath, shutil, subprocess, sys, threading
from functools import partial
from pathlib import Path

ROOT   = Path(__file__).resolve().parents[2]
OUT    = ROOT / '_site'
LOCKED = ROOT / 'src' / 'static' / 'talk' / 'engine' / 'locked'
AREAS  = ('talk/slides/', 'studio/lab/', 'motion/lab/', 'studio-ports/lab/', 'ruv-sgit/')

CRAWL = r"""
const { chromium } = require('playwright');
(async () => {
  const [base, ...paths] = process.argv.slice(1), seen = new Set(), errs = [];
  const br = await chromium.launch(), p = await br.newPage({ viewport: { width: 1280, height: 720 } });
  p.on('request', r => { const u = new URL(r.url()); if (u.origin === base) seen.add(decodeURIComponent(u.pathname)) });
  p.on('pageerror', e => errs.push(e.message));
  for (const x of paths) { await p.goto(base + '/' + x + '?ruvt=0', { waitUntil: 'load' }); await p.waitForTimeout(2500); await p.goto(base + '/' + x + '?static', { waitUntil: 'load' }); await p.waitForTimeout(800) }
  await br.close(); console.log(JSON.stringify({ files: [...seen], errors: errs }));
})();
"""

def main():
    a = argparse.ArgumentParser(description='Lock one part of the talk'); a.add_argument('--part', type=int, required=True); a = a.parse_args()
    talk = json.loads((OUT / 'talk' / 'talk.json').read_text())
    beats = [b for b in talk['beats'] if b.get('part') == a.part]
    if not beats: sys.exit(f'lock: no beat in talk.json has "part": {a.part}')
    locks_path = LOCKED / 'locks.json'
    locks = json.loads(locks_path.read_text()) if locks_path.exists() else {'schema': 'the-ultimate-insider/talk-locks/v1', 'parts': {}}
    if str(a.part) in locks['parts']: sys.exit(f'lock: part {a.part} is locked already ({locks["parts"][str(a.part)]["locked_at"]}); a locked part is never changed')
    dest = LOCKED / f'part{a.part}'
    if dest.exists(): sys.exit(f'lock: {dest.relative_to(ROOT)} exists; a locked part is never changed')
    site = lambda src: posixpath.normpath('talk/' + src)            # a beat's src is relative to talk/
    frozen, live = [], []
    for b in beats:
        s = (b.get('slide') or {}).get('src')
        if s and (b.get('slide') or {}).get('layout', 'iframe') == 'iframe' and site(s.split('?')[0]).startswith(AREAS): frozen.append(site(s.split('?')[0]))
        elif s: live.append(b['id'])
    srv = http.server.ThreadingHTTPServer(('127.0.0.1', 0), partial(http.server.SimpleHTTPRequestHandler, directory=str(OUT)))
    srv.RequestHandlerClass.log_message = lambda *x: None
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    r = subprocess.run(['node', '-e', CRAWL, f'http://127.0.0.1:{srv.server_address[1]}', *frozen], capture_output=True, text=True, timeout=600)
    srv.shutdown()
    if r.returncode: sys.exit('lock: the crawl failed: ' + r.stderr[-400:])
    got = json.loads(r.stdout.strip().splitlines()[-1])
    files = {f.lstrip('/') for f in got['files']}
    for f in frozen: files |= {str(q.relative_to(OUT)) for q in (OUT / f).parent.rglob('*') if q.is_file()}
    files = sorted(f for f in files if (OUT / f).is_file() and not f.startswith(('talk/engine/locked/', 'sw.js', 'sw.json')))
    for f in files:
        (dest / f).parent.mkdir(parents=True, exist_ok=True); shutil.copy2(OUT / f, dest / f)
    out = []
    for b in beats:
        x = json.loads(json.dumps(b)); s = (x.get('slide') or {}).get('src')
        if s and site(s.split('?')[0]) in frozen: x['slide']['src'] = f'engine/locked/part{a.part}/' + site(s.split('?')[0]) + (('?' + s.split('?', 1)[1]) if '?' in s else '')
        out.append(x)
    now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    (dest / 'beats.json').write_text(json.dumps({'part': a.part, 'locked_at': now, 'version': (ROOT / 'version').read_text().strip() if (ROOT / 'version').exists() else '', 'beats': out}, indent=1) + '\n')
    locks['parts'][str(a.part)] = {'locked_at': now, 'beats': f'engine/locked/part{a.part}/beats.json', 'ids': [b['id'] for b in beats], 'files': len(files), 'live': live}
    locks_path.write_text(json.dumps(locks, indent=1) + '\n')
    print(f'lock: part {a.part} locked at {now}: {len(beats)} beats, {len(frozen)} slides frozen, {len(files)} files; live: {", ".join(live) or "none"}; page errors: {len(got["errors"])}')

if __name__ == '__main__':
    main()
