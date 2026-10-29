# Writes src/pages/studio/lab.html: every animation in the studio lab with its beginning, middle and end, side by side,
# so the editor can review them one by one. Reads the lab folders; the times come from each slide's own data-end.
# deck@the-ultimate-insider runs it whenever a new version lands. Standard library only.
#
#   python3 team/deck/tools/lab.py

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LAB  = ROOT / 'src/static/studio/lab'
PAGE = ROOT / 'src/pages/studio/lab.html'

GROUPS = [  # (folder, title, the piece's own page, its explainer, deck's reviews)
    ('b01', 'B01 The perfect storm: the overlap fills', None, None, ['b01-v2', 'b01-v1', 'b01-storyboard']),
    ('e01', 'E01 What an agent is', 'agent-evolution', 'agent-evolution', ['e01']),
    ('e02', 'E02 The blast radius', 'blast-radius', 'blast-radius', ['e02-v3', 'e02-v2', 'e02']),
    ('e03', 'E03 Where injected words come from', 'injection-sources', 'injection-sources', ['e03']),
    ('e04', 'E04 The over-enthusiastic agent', 'over-enthusiastic-agent', 'over-enthusiastic-agent', ['e04-v2', 'e04']),
    ('e07', 'E07 A typical deployment', 'typical-deployment', 'typical-deployment', ['e07']),
    ('e09', 'E09 Mandate against grant', 'mandate-and-grant', 'mandate-and-grant', ['e09']),
    ('e10', 'E10 Only a boundary is a control', 'four-barriers', 'four-barriers', ['e10']),
    ('e11', 'E11 The kernel was told first', 'harness', 'harness', ['e11']),
    ('e13', 'E13 Five published examples', 'real-examples', 'real-examples', ['e13']),
]


def e(text):
    return html.escape(text, quote=True)


ORDER = ['three', 'opener', 'collision', 'way-out', 'brakes']   # B01's slides in the order of the talk


def key(p):
    parts = p.relative_to(LAB).parts
    beat  = parts[2] if len(parts) > 3 else ''
    return (parts[1], -ORDER.index(beat) if beat in ORDER else 0)


def slides(folder):
    out = []
    for f in sorted((LAB / folder).rglob('index.html'), key=key, reverse=True):
        text = f.read_text()
        m    = re.search(r'data-end="([0-9.]+)"', text)
        if not m:
            continue                                                  # a wrapper page, not a slide
        end   = float(m.group(1))
        title = re.search(r'<title>([^<]*)', text)
        rel   = f.relative_to(LAB).as_posix()
        out.append((rel, title.group(1) if title else rel, end))
    return out


def frame(src, label):
    return (f'<figure class="fr"><a href="{e(src)}"><span class="thumb"><iframe src="{e(src)}" title="{e(label)}" loading="lazy" tabindex="-1"></iframe></span></a>'
            f'<figcaption>{e(label)}</figcaption></figure>')


def row(rel, title, end, latest):
    base = f'lab/{rel}'
    if end <= 1:
        frames = frame(base + '?static', 'a still')
    else:
        b, m = round(end * 0.15, 1), round(end / 2, 1)
        frames = (frame(f'{base}?t={b}', f'beginning, {b:g} s') + frame(f'{base}?t={m}', f'middle, {m:g} s')
                  + frame(f'{base}?static', f'end, {end:g} s'))
    tag = '<span class="st done">latest</span> ' if latest else ''
    return (f'<li class="lab-row"><p class="kicker">{tag}{e(title)} · {end:g} s · <a href="{e(base)}">play it</a> · <a href="{{{{root}}}}talk/engine/view.html?id={e(rel[:-len('/index.html')])}">full width, replay and scrub</a></p>'
            f'<div class="frames">{frames}</div></li>')


def main():
    parts, count = [], 0
    for folder, title, piece, explainer, reviews in GROUPS:
        items = slides(folder)
        if not items:
            continue
        versions = sorted({r.split('/')[1] for r, _, _ in items}, reverse=True)
        links = []
        if piece:
            links.append(f'<a href="{{{{root}}}}ruv-sgit/{piece}/index.html">the piece</a>')
            links.append(f'<a href="{{{{root}}}}ruv-sgit/{explainer}/explainer.html">its explainer</a>')
        links += [f'<a href="reviews/{r}.html">review {r}</a>' for r in reviews]
        rows = ''.join(row(r, t, end, r.split('/')[1] == versions[0]) for r, t, end in items)
        count += len(items)
        parts.append(f'<section class="lab-group" id="{folder}"><h2>{e(title)}</h2><p class="note">{" · ".join(links)}</p><ol class="lab-rows">{rows}</ol></section>')
    toc = ' · '.join(f'<a href="#{f}">{e(t.split(" ", 1)[0])}</a>' for f, t, *_ in GROUPS)
    body = f'''<!--meta {{"title": "The lab: every animation, beginning, middle and end", "description": "Every animation the studio has made for The ultimate insider, each shown at its beginning, middle and end, newest version first, with links to play it, its explainer and deck's review."}} -->
<style>
.lab-rows{{list-style:none;padding:0;margin:10px 0 26px}}
.lab-row{{margin:0 0 22px}}
.frames{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}}
@media(max-width:760px){{.frames{{grid-template-columns:1fr}}}}
.fr{{margin:0}}
.fr .thumb{{display:block;position:relative;aspect-ratio:16/9;border:1px solid var(--line);border-radius:10px;overflow:hidden;background:#0c0f15}}
.fr a:hover .thumb{{border-color:var(--accent)}}
.fr iframe{{position:absolute;inset:0;width:100%;height:100%;border:0;pointer-events:none}}
.fr figcaption{{font-size:13px;color:var(--dim);margin-top:4px}}
</style>
<section class="wrap studio-top">
<nav class="crumbs" aria-label="Breadcrumb"><a href="{{{{root}}}}index.html">Home</a> / <a href="index.html">Studio</a></nav>
<p class="kicker">The studio · {count} slides · generated by team/deck/tools/lab.py</p>
<h1>The lab: beginning, middle and end</h1>
<div class="prose"><p class="lead">Every animation the studio has made, newest version first, each frozen at three moments: near its beginning, at its middle and at its end. Click any frame to play the slide from the start. The latest version of each piece is marked; the reviews say what was kept and why.</p></div>
<p class="note">{toc}</p>
{"".join(parts)}
</section>
'''
    PAGE.write_text(body)
    print(f'wrote {PAGE.relative_to(ROOT)}: {count} slides')


if __name__ == '__main__':
    main()
