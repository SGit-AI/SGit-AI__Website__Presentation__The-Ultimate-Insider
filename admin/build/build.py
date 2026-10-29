# Builds the site into _site/ from src/ and content/. Standard library only, so CI needs nothing installed.
#
#   python3 admin/build/build.py                 # version from ./version (written only by CI), else "pending"
#   python3 admin/build/build.py --version v0.1.3
#
# What it does, in order: copy src/static verbatim (stamping {{version}}), wrap every src/pages fragment in the
# chrome, render content/articles/*.md, generate the articles index, the talk script, the release history,
# llms.txt and sitemap.xml, and write a .md twin next to every page. Apache-2.0.

import html
import json
import re
import shutil
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT       = Path(__file__).resolve().parents[2]
SRC        = ROOT / 'src'
CONTENT    = ROOT / 'content'
OUT        = ROOT / '_site'
TEXT_TYPES = {'.html', '.js', '.css', '.json', '.txt', '.md', '.svg', '.xml'}
PENDING    = 'pending'


class Markdown:                                                     # just enough markdown for articles written here
    INLINE = [(re.compile(r'`([^`]+)`'),                    lambda m: '<code>' + m.group(1) + '</code>'),
              (re.compile(r'\*\*([^*]+)\*\*'),              lambda m: '<strong>' + m.group(1) + '</strong>'),
              (re.compile(r'(?<![*\w])\*([^*\s][^*]*)\*'),  lambda m: '<em>' + m.group(1) + '</em>'),
              (re.compile(r'!\[([^\]]*)\]\(([^)\s]+)\)'),    lambda m: '<img src="' + m.group(2) + '" alt="' + m.group(1) + '" loading="lazy">'),
              (re.compile(r'\[([^\]]+)\]\(([^)\s]+)\)'),     lambda m: '<a href="' + m.group(2) + '">' + m.group(1) + '</a>')]

    def inline(self, text):
        parts = re.split(r'(`[^`]+`)', text)                        # never touch what is inside code spans
        out   = []
        for part in parts:
            if part.startswith('`') and part.endswith('`') and len(part) > 1:
                out.append('<code>' + html.escape(part[1:-1]) + '</code>')
                continue
            part = html.escape(part, quote=False)
            for pattern, repl in self.INLINE[1:]:
                part = pattern.sub(repl, part)
            out.append(part)
        return ''.join(out)

    def to_html(self, text):
        lines, out, i = text.split('\n'), [], 0
        while i < len(lines):
            line = lines[i]
            if not line.strip():
                i += 1
                continue
            if line.startswith('```'):
                block = []
                i += 1
                while i < len(lines) and not lines[i].startswith('```'):
                    block.append(lines[i])
                    i += 1
                out.append('<pre><code>' + html.escape('\n'.join(block)) + '</code></pre>')
                i += 1
                continue
            m = re.match(r'(#{1,4}) (.*)', line)
            if m:
                level  = len(m.group(1))
                anchor = re.sub(r'[^a-z0-9]+', '-', m.group(2).lower()).strip('-')
                out.append(f'<h{level} id="{anchor}">{self.inline(m.group(2))}</h{level}>')
                i += 1
                continue
            if line.startswith('<'):                                # a raw html block, up to the next blank line
                block = []
                while i < len(lines) and lines[i].strip():
                    block.append(lines[i])
                    i += 1
                out.append('\n'.join(block))
                continue
            if line.startswith('> '):
                block = []
                while i < len(lines) and lines[i].startswith('> '):
                    block.append(lines[i][2:])
                    i += 1
                out.append('<blockquote><p>' + self.inline(' '.join(block)) + '</p></blockquote>')
                continue
            if line.startswith('|'):
                rows = []
                while i < len(lines) and lines[i].startswith('|'):
                    cells = [c.strip() for c in lines[i].strip().strip('|').split('|')]
                    if not all(re.fullmatch(r':?-{3,}:?', c) for c in cells):
                        rows.append(cells)
                    i += 1
                head = ''.join('<th>' + self.inline(c) + '</th>' for c in rows[0])
                body = ''.join('<tr>' + ''.join('<td>' + self.inline(c) + '</td>' for c in r) + '</tr>' for r in rows[1:])
                out.append(f'<div class="tbl"><table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>')
                continue
            m = re.match(r'(\s*)([-*]|\d+\.) ', line)
            if m:
                tag   = 'ol' if m.group(2)[0].isdigit() else 'ul'
                items = []
                while i < len(lines) and re.match(r'\s*([-*]|\d+\.) ', lines[i]):
                    item = re.sub(r'^\s*([-*]|\d+\.) ', '', lines[i])
                    i += 1
                    while i < len(lines) and lines[i].startswith('  ') and lines[i].strip():
                        item += ' ' + lines[i].strip()
                        i += 1
                    items.append('<li>' + self.inline(item) + '</li>')
                out.append(f'<{tag}>' + ''.join(items) + f'</{tag}>')
                continue
            block = []
            while i < len(lines) and lines[i].strip() and not re.match(r'(#{1,4} |```|> |\||\s*([-*]|\d+\.) |<)', lines[i]):
                block.append(lines[i].strip())
                i += 1
            out.append('<p>' + self.inline(' '.join(block)) + '</p>')
        return '\n'.join(out)


class Html_To_Markdown(HTMLParser):                                 # the .md twin of a page written in html
    SKIP  = {'script', 'style', 'svg', 'nav', 'button', 'template', 'iframe'}
    BLOCK = {'p', 'div', 'section', 'article', 'header', 'footer', 'main', 'ul', 'ol', 'table', 'figure', 'blockquote', 'aside', 'figcaption', 'details', 'summary', 'dl', 'dd', 'dt'}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out, self.skip, self.href, self.row = [], 0, [], None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in self.SKIP or 'data-md-skip' in a:
            self.skip += 1
            return
        if self.skip:
            return
        if tag in ('h1', 'h2', 'h3', 'h4'):
            self.out.append('\n\n' + '#' * int(tag[1]) + ' ')
        elif tag == 'li':
            self.out.append('\n- ')
        elif tag == 'br':
            self.out.append('\n')
        elif tag in ('strong', 'b'):
            self.out.append('**')
        elif tag in ('em', 'i'):
            self.out.append('*')
        elif tag == 'code':
            self.out.append('`')
        elif tag == 'a':
            self.href.append(a.get('href', ''))
            self.out.append('[')
        elif tag == 'tr':
            self.row = []
        elif tag in ('td', 'th') and self.row is not None:
            self.row.append('')
        elif tag in self.BLOCK:
            self.out.append('\n\n')

    def handle_endtag(self, tag):
        if tag in self.SKIP:
            self.skip = max(0, self.skip - 1)
            return
        if self.skip:
            return
        if tag in ('strong', 'b'):
            self.out.append('**')
        elif tag in ('em', 'i'):
            self.out.append('*')
        elif tag == 'code':
            self.out.append('`')
        elif tag == 'a' and self.href:
            href = re.sub(r'\.html(#|$)', r'.md\1', self.href.pop()) if not self.href[-1].startswith('http') else self.href.pop()
            self.out.append(f']({href})')
        elif tag == 'tr' and self.row is not None:
            self.out.append('\n| ' + ' | '.join(c.strip() for c in self.row) + ' |')
            self.row = None
        elif tag in self.BLOCK or tag in ('h1', 'h2', 'h3', 'h4'):
            self.out.append('\n')

    def handle_data(self, data):
        if self.skip:
            return
        text = re.sub(r'\s+', ' ', data)
        if self.row is not None and self.row:
            self.row[-1] += text
        else:
            self.out.append(text)

    def convert(self, fragment):
        self.feed(fragment)
        text = ''.join(self.out)
        text = re.sub(r'\[\s*\]\([^)]*\)', '', text)
        text = re.sub(r'[ \t]+\n', '\n', text)
        text = re.sub(r'\n[ \t]+', '\n', text)
        text = re.sub(r'\n{3,}', '\n\n', text)
        return text.strip() + '\n'


class Site_Build:
    def __init__(self, version):
        self.version  = version
        self.config   = json.loads((ROOT / 'site.json').read_text())
        self.pages    = []                                           # (path, title, description) of every page built
        self.titles   = {}                                           # path -> title, for the release history
        self.articles = []

    def root_of(self, rel):                                         # the relative path back to the site root
        return '../' * (len(Path(rel).parts) - 1)

    def stamp(self, text, rel):
        return text.replace('{{version}}', self.version).replace('{{root}}', self.root_of(rel))

    def chrome(self, rel, title, description, body, kind='page'):
        root  = self.root_of(rel)
        name  = self.config['name']
        hrefs = [href for _, href in self.config['nav']]                # the page's own link, or else its section's (design note 2)
        here  = rel if rel in hrefs else next((h for h in hrefs if '/' in h and rel.startswith(h.rsplit('/', 1)[0] + '/')), None)
        nav   = ''.join(f'<a href="{root}{href}"{(" aria-current=\"page\"" if href == rel else " aria-current=\"true\"") if href == here else ""}>{label}</a>' for label, href in self.config['nav'])
        full  = title if rel == 'index.html' else f'{title} · {self.config["short"]}'
        canon = self.config['url'] + '/' + rel
        md    = Path(rel).with_suffix('.md').name
        ver   = 'pending' if self.version == PENDING else self.version
        ld    = json.dumps({'@context': 'https://schema.org', '@type': 'Article' if kind == 'article' else 'WebPage', 'name': title,
                            'description': description, 'url': canon, 'version': self.version, 'isPartOf': {'@type': 'WebSite', 'name': name, 'url': self.config['url']},
                            'author': {'@type': 'Person', 'name': 'Dinis Cruz'}, 'license': 'https://creativecommons.org/licenses/by/4.0/'}).replace('</', '<\\/')
        return f'''<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(full)}</title>
<meta name="description" content="{html.escape(description)}">
<meta name="site-version" content="{self.version}">
<link rel="canonical" href="{canon}">
<link rel="alternate" type="text/markdown" href="{md}">
<meta property="og:type" content="{'article' if kind == 'article' else 'website'}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(description)}">
<meta property="og:url" content="{canon}">
<script type="application/ld+json">{ld}</script>
<link rel="icon" href="{root}assets/favicon.svg">
<link rel="stylesheet" href="{root}assets/site.css">
<link rel="stylesheet" href="{root}assets/pane.css">
<script src="{root}assets/theme.js"></script>
<script src="{root}assets/pane.js" defer></script>
</head>
<body class="{kind}{' adm' if self.in_admin(rel) or self.in_studio(rel) else ''}">
<a class="skip" href="#main">Skip to the content</a>
<header class="top"><div class="wrap">
<a class="brand" href="{root}index.html"><b>the ultimate insider</b><small>presentation.sgit.ai</small></a>
<a class="ver" href="{root}admin/versions.html#{ver}" title="Release history: what {self.version} changed">{self.version}</a>
<nav class="main" aria-label="Site">{nav}</nav>
<a class="gh" href="{self.config['repo']}" title="This site's source on GitHub: star it there" data-repo="{self.config['repo'].split('github.com/')[-1]}"><svg viewBox="0 0 16 16" width="16" height="16" aria-hidden="true"><path fill="currentColor" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/></svg><span class="gh-s" aria-hidden="true">\u2605</span><span class="gh-n">Star</span><span class="vh"> this site on GitHub</span></a>
<button class="theme" type="button" aria-label="Switch between light and dark">theme</button>
</div></header>
<main id="main">
{self.shell(rel, body)}
</main>
<footer class="foot"><div class="wrap">
<p><b>{name}</b> · <a href="{root}admin/versions.html" class="ver">site {self.version}</a> · version numbered by CI, never by hand</p>
<p>Part of the <a href="https://sgit.ai/">sgit.ai</a> network · written with the agents of <a href="https://newsroom.sgit.ai/">the SGit Newsroom</a> · <a href="{self.config['repo']}">source</a> · <a href="{md}">this page as markdown</a> · <a href="{root}llms.txt">llms.txt</a> · <a href="{root}about/index.html">about and disclosure</a></p>
<p>Text CC BY 4.0, code Apache-2.0. © 2026 Dinis Cruz.</p>
</div></footer>
</body>
</html>
'''

    DOCS = [('reality',           'REALITY.md',                    'What exists',              'What exists in this repository, kept current by whoever ships.'),
            ('rules-for-agents',  'CLAUDE.md',                     'Rules for agents',         'The rules every agent working in this repository reads first (CLAUDE.md).'),
            ('corrections',       'BRIEF-CORRECTIONS.md',          'Corrections to the brief', 'Where the brief turned out to be wrong, and what was done instead.'),
            ('onboarding',        'team/conductor/ONBOARDING.md',  'Onboarding',               'How each member\'s schedule is started and how it gets the vault keys.'),
            ('wake-protocol',     'team/conductor/WAKE.md',        'The wake protocol',        'Every member\'s checklist for every session, and how any member stops the team.'),
            ('the-next-hours',    'team/conductor/briefs/2026-10-29__the-next-hours.md', 'The next hours (brief)', 'The conductor\'s brief for the night: the themes, the flow of ideas, the dashboard, and backlog then schedule then execute.')]

    def in_admin(self, rel):                                        # the admin section: everything about who does what, with a side navigation
        return rel.startswith(('admin/', 'team/', 'brief/'))

    def in_studio(self, rel):
        return rel.startswith('studio/') and (SRC / 'pages' / 'studio').exists()

    def page_title(self, path):
        m = re.match(r'\s*<!--meta\s+(\{.*?\})\s*-->', path.read_text(), re.S)
        return json.loads(m.group(1)).get('title', path.stem) if m else path.stem

    def studio_nav(self):
        st    = SRC / 'pages' / 'studio'
        top   = [(f'studio/{n}.html', self.page_title(st / f'{n}.html')) for n in ('index', 'programme', 'how-it-works', 'techniques') if (st / f'{n}.html').exists()]
        brief = [('studio/briefs/index.html', 'All briefs')] + [(f'studio/briefs/{p.stem}.html', self.page_title(p) if self.page_title(p).upper().startswith(p.stem.split('-')[0].upper()) else p.stem.split('-')[0].upper() + ': ' + self.page_title(p))
                                                               for p in sorted((st / 'briefs').glob('*.html')) if p.stem != 'index'] if (st / 'briefs').exists() else []
        lab   = []
        for p in sorted((SRC / 'static' / 'studio' / 'lab').rglob('index.html')) if (SRC / 'static' / 'studio' / 'lab').exists() else []:
            t = re.search(r'<title>(.*?)</title>', p.read_text(), re.S)
            lab.append((str(p.relative_to(SRC / 'static')), html.unescape(t.group(1).strip()) if t else p.parent.name))
        return [('The studio', top), ('Briefs', brief), ('The lab', lab)]

    def side_nav(self):
        team = [(f'team/{p.name}/index.html', json.loads((p / 'policy.json').read_text()).get('address', p.name).split('@')[0])
                for p in sorted((ROOT / 'team').iterdir()) if p.is_dir() and (p / 'policy.json').exists()]
        docs = [(f'admin/docs/{slug}.html', label) for slug, src, label, _ in self.DOCS if (ROOT / src).exists()]
        docs += [('admin/docs/pace.html', 'The pace (pace.json)')] if (ROOT / 'team/conductor/pace.json').exists() else []
        return [('Overview',          [('admin/index.html', 'Admin and engineering')]),
                ('Activity',          [('admin/dashboard.html', 'Dashboard'), ('admin/wakes.html', 'Wakes'), ('admin/mail.html', 'Mail'), ('admin/commits.html', 'Commits and messages'), ('admin/versions.html', 'Releases'), ('team/board.html', 'The board')]
                                      + ([('team/schedule.html', 'The schedule')] if (ROOT / 'team/conductor/schedule.json').exists() else [])),
                ('Team',              [('team/index.html', 'Everyone')] + team),
                ('Keys and vaults',   [('admin/keys.html', 'The key register')] + ([('admin/vaults.html', 'The public vaults')] if (ROOT / 'team/conductor/vaults.json').exists() else [])),
                ('Sources of truth',  [('brief/index.html', 'The brief')] + docs)]

    def shell(self, rel, body):
        if not (self.in_admin(rel) or self.in_studio(rel)):
            return body
        groups = self.side_nav() if self.in_admin(rel) else self.studio_nav()
        label  = 'Admin' if self.in_admin(rel) else 'Studio'
        root  = self.root_of(rel)
        here  = lambda href: href == rel or (href.startswith('team/') and href.endswith('/index.html') and href != 'team/index.html' and rel.startswith(href[:-len('index.html')]))
        nav   = ''.join(f'<p class="sg">{html.escape(group)}</p><ul>' + ''.join(
                    f'<li><a href="{root}{href}"{" aria-current=\"page\"" if here(href) else ""}>{html.escape(label)}</a></li>' for href, label in items) + '</ul>'
                    for group, items in groups)
        return (f'<div class="shell"><aside class="side" aria-label="{label}"><details open><summary>{label} menu</summary>{nav}</details></aside>'
                f'<div class="shell-main">{body}</div></div>')

    STEP_NAMES = [('plan', 'plan'), ('pre_review', 'pre-review'), ('work', 'work'), ('post_review', 'post-review'), ('post_check', 'post-check')]

    def wakes(self, agent=None):                                    # the five-step wake records, newest first
        out = []
        for path in sorted((ROOT / 'team').glob(f'{agent or "*"}/wakes/*.json'), reverse=True):
            try:
                rec = json.loads(path.read_text())
            except ValueError:
                continue
            if rec.get('schema') == 'the-ultimate-insider/wake/v1':
                out.append(rec)
        return sorted(out, key=lambda r: r.get('started', ''), reverse=True)

    def wakes_html(self, recs, root, show_agent=True):              # every step's verdict and comment, as text
        esc, rows = html.escape, ''
        for r in recs:
            steps = ''.join(
                (lambda st: f'<div class="wst v-{esc(st.get("verdict", "missing"))}"><b>{label}</b> <span class="vd">{esc(st.get("verdict", "missing"))}</span>'
                            f'<span class="by">{esc(st.get("by", ""))}{" · " + esc(st.get("model", "")) if st.get("model") else ""}</span>'
                            f'<p>{esc(st.get("comment", "not recorded"))}</p></div>')(r.get('steps', {}).get(key, {}))
                for key, label in self.STEP_NAMES)
            who = f'<a href="{root}team/{esc(r["agent"])}/index.html">{esc(r["agent"])}</a> · ' if show_agent else ''
            rows += (f'<section class="wake o-{esc(r.get("outcome") or "open")}" id="wake-{esc(r["agent"])}-{esc(r.get("started", ""))}"><header>{who}'
                     f'<span class="t">{esc(r.get("started", "")[:16].replace("T", " "))} UTC</span> · {esc(r.get("kind", ""))} · '
                     f'<span class="oc">{esc(r.get("outcome") or "still open")}</span></header><div class="wsteps">{steps}</div></section>')
        return rows or '<p class="note">No wake records yet.</p>'

    FLOW_COLS = [('Briefs', ('brief',)), ('Themes', ('theme',)), ('Ideas', ('experiment',)), ('Requests', ('request', 'backlog')),
                 ('Artifacts', ('artifact',)), ('Reviews', ('review',)), ('Decisions', ('decision',))]

    def flow_graph(self, pace):                                     # dashboard part 3 (dev, the conductor's brief): pace.json drawn, read at build time
        esc, nodes, edges = html.escape, pace.get('nodes', []), pace.get('edges', [])
        if not nodes:
            return ''
        def owner(n):                                               # only id, title, kind, status and owner are shown (the pre-review's condition)
            return str(n.get('owner') or n.get('by') or ('editor' if 'editor' in str(n.get('for', '')) else ''))
        def label(n):
            return str(n.get('title') or n.get('verdict') or n['id'])
        def state(n):
            st = str(n.get('status') or ('reviewed' if n.get('verdict') else ''))
            low = st.lower()
            return st, ('done' if low in ('delivered', 'published', 'given', 'sent', 'done', 'reviewed') else
                        'wait' if any(w in low for w in ('review', 'flight', 'scheduled', 'asked')) else 'idle')
        W, H, CW, RH, TOP = 210, 44, 270, 54, 34
        pos, cols = {}, []
        for c, (name, kinds) in enumerate(self.FLOW_COLS):
            mine = sorted((n for n in nodes if n.get('kind') in kinds), key=lambda n: (owner(n), str(n.get('at', '')), n['id']))
            cols.append((name, len(mine)))
            for r, n in enumerate(mine):
                pos[n['id']] = (c * CW + 10, TOP + r * RH, n)
        width  = len(self.FLOW_COLS) * CW
        height = TOP + max(n for _, n in cols) * RH + 10
        lines, dangling = '', []
        for e in edges:
            a, b = pos.get(e.get('from')), pos.get(e.get('to'))
            if not a or not b:
                dangling.append(e)
                continue
            k = esc(str(e.get('kind', '')))
            if a[0] == b[0]:                                        # same column (a redo): an arc on the left
                x, y1, y2 = a[0], a[1] + H / 2, b[1] + H / 2
                d = f'M{x},{y1} C{x - 40},{y1} {x - 40},{y2} {x},{y2}'
            else:
                (x1, y1), (x2, y2) = ((a[0] + W, a[1] + H / 2), (b[0], b[1] + H / 2)) if a[0] < b[0] else ((a[0], a[1] + H / 2), (b[0] + W, b[1] + H / 2))
                m = (x1 + x2) / 2
                d = f'M{x1},{y1} C{m},{y1} {m},{y2} {x2},{y2}'
            lines += f'<path class="fe e-{k}" d="{d}"><title>{esc(str(e.get("from")))} {k} {esc(str(e.get("to")))}</title></path>'
        boxes = ''.join(f'<text class="fh" x="{c * CW + 10}" y="18">{esc(name)} · {n}</text>' for c, (name, n) in enumerate(cols))
        for nid, (x, y, n) in pos.items():
            st, cls = state(n)
            t = label(n)
            short = t if len(t) <= 27 else t[:26] + '\u2026'
            meta = ' · '.join(v for v in (nid if nid != t else '', owner(n), st) if v)
            boxes += (f'<g class="fn s-{cls}"><title>{esc(nid)}: {esc(t)} ({esc(str(n.get("kind")))}, {esc(owner(n) or "no owner")}, {esc(st or "no status")})</title>'
                      f'<rect x="{x}" y="{y}" width="{W}" height="{H}" rx="8"/><text class="ft" x="{x + 10}" y="{y + 18}">{esc(short)}</text>'
                      f'<text class="fm" x="{x + 10}" y="{y + 35}">{esc(meta if len(meta) <= 27 else meta[:26] + '\u2026')}</text></g>')
        reviewed = {e.get('from') for e in edges if e.get('kind') == 'reviewed'}
        waits = [n for n in nodes if n.get('kind') == 'artifact' and n['id'] not in reviewed and n['id'] in pos]
        back  = [n for n in nodes if n.get('kind') == 'artifact' and state(n)[1] == 'done']
        li    = lambda ns: ''.join(f'<li><b>{esc(n["id"])}</b> {esc(owner(n))} · {esc(state(n)[0])}{(" " + esc(str(n.get("at", ""))[11:16]) + " UTC") if n.get("at") else ""}</li>' for ns_ in [ns] for n in ns_)
        miss  = ''.join(f'<li><code>{esc(str(e.get("from")))}</code> {esc(str(e.get("kind")))} <code>{esc(str(e.get("to")))}</code></li>' for e in dangling)
        return (f'<h2 id="flow">The flow</h2><p class="note">The conductor\'s <a href="docs/pace.html">pace.json</a> drawn, read when the site was built: '
                f'{len(nodes)} nodes and {len(edges)} edges, from briefs and themes to ideas, requests, artifacts, reviews and the editor\'s decisions. '
                f'Green came back or is done, amber waits (in flight, scheduled, in review), grey is an idea or open. Lines: asks and delivers solid, reviewed dotted, redo red, sets faint. '
                f'Hover a box for its id, full title, kind, owner and status, or a line for what it joins.</p>'
                f'<div class="flowlists"><div><p class="kk">Waits on review · {len(waits)}</p><ul>{li(waits) or "<li>nothing</li>"}</ul></div>'
                f'<div><p class="kk">Came back · {len(back)}</p><ul>{li(back)}</ul></div>'
                + (f'<div><p class="kk">Edges to no node · {len(dangling)}</p><ul>{miss}</ul></div>' if dangling else '') + '</div>'
                f'<div class="tbl flow"><svg class="flowg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" role="img" aria-label="The flow graph of pace.json">{lines}{boxes}</svg></div>')

    def build_dashboard(self):                                      # dev 006, the conductor's brief: part 1, Now and the pace grid
        import datetime
        esc, team = html.escape, ROOT / 'team'
        sched = json.loads((team / 'conductor' / 'schedule.json').read_text()) if (team / 'conductor' / 'schedule.json').exists() else {'runs': []}
        pace  = json.loads((team / 'conductor' / 'pace.json').read_text()) if (team / 'conductor' / 'pace.json').exists() else {}
        if pace:
            self.write('admin/pace.json', json.dumps(pace, indent=1) + '\n')
        built = datetime.datetime.now(datetime.timezone.utc)
        holds = sorted(team.glob('*/HOLD.md')) + ([team / 'HOLD.md'] if (team / 'HOLD.md').exists() else [])
        hold  = ''.join(f'<li><b>{esc(h.parent.name)}</b>: {esc(h.read_text().splitlines()[0].lstrip("# "))}</li>' for h in holds)
        wakes = self.wakes()
        members, asks = [], []
        for folder in sorted(p for p in team.iterdir() if p.is_dir()):
            st = json.loads((folder / 'status.json').read_text()) if (folder / 'status.json').exists() else {}
            for a in st.get('asks', []):
                if 'editor' in str(a.get('from', '')).lower():
                    asks.append((folder.name, a.get('what', '')))
            run  = next((r for r in sched['runs'] if r['agent'] == folder.name), None)
            last = next((w for w in wakes if w['agent'] == folder.name), None)
            members.append((folder.name, st, run, last))
        rows = ''
        for aid, st, run, last in members:
            slot = f'<span class="nx" data-minute="{esc(run["minute"])}">:{esc(run["minute"])}</span>' if run else '<span class="c-dim">no slot</span>'
            live = '' if not run else (' <span class="c-dim">(not running yet)</span>' if not str(run.get('status', '')).startswith('running') else '')
            lw   = (f'<a href="wakes.html#wake-{esc(aid)}-{esc(last.get("started", ""))}">{esc(last.get("started", "")[11:16])}</a> {esc(last.get("outcome") or "open")}' if last else '<span class="c-dim">none yet</span>')
            page = f'<a href="../team/{esc(aid)}/index.html">{esc(aid)}</a>' if (team / aid / 'policy.json').exists() else esc(aid)
            rows += f'<tr><td>{page}</td><td>{slot}{live}</td><td>{lw}</td><td>{esc(st.get("state", ""))}</td></tr>'
        # the pace grid: members by hour, one cell per wake, five dots for its five verdicts
        hours = sorted({w.get('started', '')[:13] for w in wakes if w.get('started')})
        cells = ''
        for aid, *_ in members:
            mine = [w for w in wakes if w['agent'] == aid]
            if not mine:
                continue
            cells += f'<tr><th>{esc(aid)}</th>'
            for h in hours:
                inh = [w for w in mine if w.get('started', '').startswith(h)]
                dots = ''.join(
                    f'<a class="pc o-{esc(w.get("outcome") or "open")}" href="wakes.html#wake-{esc(aid)}-{esc(w.get("started", ""))}" title="{esc(aid)} {esc(w.get("started", ""))}: {esc(w.get("outcome") or "open")}">'
                    + ''.join(f'<i class="d v-{esc(w.get("steps", {}).get(k, {}).get("verdict", "missing"))}" title="{lbl}: {esc(w.get("steps", {}).get(k, {}).get("verdict", "missing"))}"></i>' for k, lbl in self.STEP_NAMES)
                    + f'<span>{esc(w.get("outcome") or "open")}</span></a>' for w in inh)
                cells += f'<td>{dots}</td>'
            cells += '</tr>'
        head  = ''.join(f'<th>{h[11:13]}:00</th>' for h in hours)
        q     = pace.get('schedule', {})
        queue = ''.join(f'<li><b>{esc(m)}</b>: ' + ' · '.join(f'{esc(i.get("at", ""))} {esc(i.get("item", ""))}' for i in (v if isinstance(v, list) else [])) + '</li>' for m, v in q.items() if isinstance(v, list)) if isinstance(q, dict) else ''
        body = (f'<section class="wrap"><p class="kicker">Activity</p><h1>Dashboard</h1>'
                f'<p class="lead">Where the team is, read from its own files: the hour, the next wake of each member, any hold, what waits on the editor, and every wake as a grid. '
                f'Built at {built.strftime("%H:%M")} UTC with site {self.version}; the clock and the next wakes below run live in your browser. Part 3, the flow, is below; parts 4 and 5 of the brief (the sequence, the artifacts) follow at later wakes.</p>'
                f'<div class="now"><div class="nowc"><p class="kk">Now</p><p class="clock" id="dash-clock">{built.strftime("%H:%M")} UTC</p><p class="c-dim">London time; built {built.strftime("%Y-%m-%d %H:%M")} UTC</p></div>'
                f'<div class="nowc {"held" if holds else "free"}"><p class="kk">Hold</p>' + (f'<ul>{hold}</ul><p>Every wake stops until the editor lifts it.</p>' if holds else '<p class="big2">none</p><p class="c-dim">every member\'s wake runs</p>') + '</div>'
                f'<div class="nowc ed"><p class="kk">Waits on the editor</p>' + (('<ul>' + ''.join(f'<li><b>{esc(a)}</b>: {esc(w)}</li>' for a, w in asks) + '</ul>') if asks else '<p class="c-dim">nothing asked</p>') + '</div></div>'
                f'<h2 id="members">Each member</h2><div class="tbl"><table class="dash"><thead><tr><th>Member</th><th>Slot, next wake</th><th>Last wake</th><th>State, from its status.json</th></tr></thead><tbody>{rows}</tbody></table></div>'
                f'<h2 id="pace">The pace</h2><p class="note">One cell per wake, by member and hour (UTC). The five dots are plan, pre-review, work, post-review and post-check; '
                f'green is go, done, clean or as-planned, amber is change, partial, finding or off-plan, red is stop, grey is missing. Click a cell for the record.</p>'
                + (f'<div class="tbl"><table class="pace"><thead><tr><th></th>{head}</tr></thead><tbody>{cells}</tbody></table></div>' if hours else '<p class="note">No wakes recorded yet.</p>')
                + self.flow_graph(pace)
                + (f'<h2 id="queue">The queue</h2><p class="note">From the conductor\'s <a href="docs/pace.html">pace.json</a>, which sets each member\'s order.</p><ul>{queue}</ul>' if queue else '')
                + '</section><script src="../assets/dashboard.js"></script>')
        self.page('admin/dashboard.html', 'Dashboard', 'Where the team is: the hour, each member\'s next wake, holds, what waits on the editor, and every wake as a grid.', body)
        if pace:
            bmd = '```json\n' + json.dumps(pace, indent=1) + '\n```\n'
            self.page('admin/docs/pace.html', 'The pace (pace.json)', 'The conductor\'s pace.json: the queue, the schedule, the ideas and the requests of the night, as data.',
                      f'<article class="prose wrap"><p class="kicker">Sources of truth · <code>team/conductor/pace.json</code></p><h1>The pace</h1>'
                      f'<p>The conductor\'s working file for the night, rendered as it is at site {self.version}. As data: <a href="../pace.json">pace.json</a>.</p>'
                      f'<pre class="msg">{esc(json.dumps(pace, indent=1))}</pre></article>', body_md=bmd)

    def build_wakes(self):
        recs = self.wakes()
        body = (f'<section class="wrap"><p class="kicker">Activity</p><h1>Wakes</h1>'
                f'<p class="lead">Every wake of every member, newest first: the five steps the editor asked for on 29 October 2026, each with its verdict and comment. '
                f'Plan and pre-review come before the work, post-review and post-check after it; a stop from any step holds the team. {len(recs)} wakes recorded. '
                f'The steps are in <a href="docs/wake-protocol.html">the wake protocol</a>; the gate fails a closed wake that skipped one.</p>'
                f'{self.wakes_html(recs, "../")}</section>')
        md = '\n'.join(f'## {r["agent"]} · {r.get("started", "")} · {r.get("outcome") or "open"}\n\n' + '\n'.join(
                 f'- **{label}**: {r.get("steps", {}).get(k, {}).get("verdict", "missing")}: {r.get("steps", {}).get(k, {}).get("comment", "")}' for k, label in self.STEP_NAMES) + '\n'
             for r in recs)
        self.page('admin/wakes.html', 'Wakes', 'Every wake of every member, with the five steps: plan, pre-review, work, post-review and post-check.', body, body_md=md or 'No wakes yet.')

    LAB_AREAS = ('studio/lab/', 'motion/lab/', 'studio-ports/lab/')        # full-screen pieces on the engine: ruv.sgit's, motion@'s and studio@'s

    def build_pieces(self):                                          # the studio's pieces, for the player's build mode: talk/pieces.json
        out = []
        for area in self.LAB_AREAS:
            lab = SRC / 'static' / area.rstrip('/')
            for p in sorted(lab.rglob('index.html')) if lab.exists() else []:
                text = p.read_text()
                if '<header class="top"' in text or 'storyboard' in p.parts:
                    continue                                        # documents and storyboards are not pieces to present
                t, e = re.search(r'<title>(.*?)</title>', text, re.S), re.search(r'id="cv"[^>]*data-end="([0-9.]+)"', text)
                rel = p.relative_to(lab).parent
                pid = str(rel) if area == 'studio/lab/' else area.split('/')[0] + '/' + str(rel)   # the studio's ids as before; motion/<slug>, studio-ports/<slug>
                out.append({'id': pid, 'title': html.unescape(t.group(1).strip()) if t else pid, 'src': f'../{area}{rel}/index.html',
                            'end': float(e.group(1)) if e else None, 'engine': 'engine/slide.js' in text})
        self.write('talk/pieces.json', json.dumps({'about': "The studio's lab pieces, listed when the site is built, for the player's build mode.", 'pieces': out}, indent=1) + '\n')

    def build_lab_documents(self):                                  # the studio's documents get the top bar, the footer and a way back (dev 009)
        briefs = {p.stem.split('-')[0]: p for p in (SRC / 'pages' / 'studio' / 'briefs').glob('*.html')} if (SRC / 'pages' / 'studio' / 'briefs').exists() else {}
        for path in sorted((SRC / 'static').rglob('*.html')):
            if not self.lab_document(path):
                continue
            rel   = str(path.relative_to(SRC / 'static'))
            text  = path.read_text()
            title = re.search(r'<title>(.*?)</title>', text, re.S)
            title = html.unescape(title.group(1).strip()) if title else Path(rel).parent.name
            desc  = re.search(r'<meta name="description" content="([^"]*)"', text)
            head  = re.search(r'<head[^>]*>(.*?)</head>', text, re.S)
            head  = head.group(1) if head else ''
            keep  = ''.join(re.findall(r'<style[^>]*>.*?</style>|<script\b[^>]*>.*?</script>', head, re.S))
            body  = re.search(r'<body[^>]*>(.*)</body>', text, re.S)
            body  = body.group(1) if body else text
            keep  = re.sub(r'(?<![\w.-])main(?=[\s{,.:#\[>])', '.lab-doc', keep)          # its own main becomes a block inside the site's main
            body  = re.sub(r'<main\b', '<div class="lab-doc"', body).replace('</main>', '</div>')
            plain = re.sub(r'<[^>]+>', ' ', body)
            desc  = html.unescape(desc.group(1)) if desc else ' '.join(plain.split())[:200]
            bid   = Path(rel).parts[2] if len(Path(rel).parts) > 3 else ''
            brief = briefs.get(bid)
            root  = self.root_of(rel)
            crumb = (f'<nav class="crumbs lab-crumbs" aria-label="Breadcrumb"><a href="{root}studio/index.html">Studio</a> / '
                     f'<a href="{root}studio/briefs/index.html">Briefs</a>'
                     + (f' / <a href="{root}studio/briefs/{brief.stem}.html">{html.escape(bid.upper())}</a>' if brief else '') + f' / {html.escape(title)}</nav>')
            self.page(rel, title, desc, f'{keep}<div class="lab-wrap">{crumb}{body}</div>', kind='lab')

    def build_docs(self):                                           # the files that steer the agents, readable as pages
        md = Markdown()
        for slug, src, label, desc in self.DOCS:
            path = ROOT / src
            if not path.exists():
                continue
            text  = path.read_text()
            title = text.split('\n', 1)[0].lstrip('# ').strip() if text.startswith('#') else label
            body  = text.split('\n', 1)[1] if text.startswith('#') else text
            base  = str(Path(src).parent).replace('.', '')                # links between repository files go to GitHub, not to the site
            body  = re.sub(r'\]\((?!https?:|#|mailto:)([^)\s]+)\)', lambda m: '](' + self.config['repo'] + '/blob/dev/' + str(Path(base) / m.group(1)).lstrip('/') + ')', body)
            body  = body.replace('{{', '{\u200b{')                      # the docs talk about the placeholders; they must not be stamped
            html_ = (f'<article class="prose wrap"><p class="kicker">Sources of truth · <code>{html.escape(src)}</code></p><h1>{html.escape(title)}</h1>'
                     f'{md.to_html(body)}<p class="note">Rendered from <code>{html.escape(src)}</code> at site {self.version}: '
                     f'<a href="{self.config["repo"]}/blob/dev/{src}">the file on GitHub</a>.</p></article>')
            self.page(f'admin/docs/{slug}.html', label, desc, html_, body_md=body)

    def build_vaults(self):                                         # the two public vaults, a page of their own (conductor's To-dev, 29 October)
        path = ROOT / 'team' / 'conductor' / 'vaults.json'
        if not path.exists():
            return
        data, esc = json.loads(path.read_text()), html.escape
        if (path.parent / 'vault-qr').exists():
            shutil.copytree(path.parent / 'vault-qr', OUT / 'admin' / 'vault-qr', dirs_exist_ok=True)
        cards = ''
        for v in data['vaults']:
            qr = (f'<img class="qr" src="vault-qr/{esc(Path(v["read_key_qr"]).name)}" alt="QR code of the read key of {esc(v["name"])}" width="220" height="220">'
                  if v.get('read_key_qr') and (path.parent / 'vault-qr' / Path(v['read_key_qr']).name).exists() else '')
            see = '<a href="../team/board.html">read it as the board</a> · ' if v['kind'] == 'Issues-FS' else ''
            cards += (f'<section class="vault" id="{esc(v["name"])}"><div class="vq">{qr}</div><div class="vt"><p class="kicker">{esc(v["kind"])} · vault {esc(v["vault_id"])}</p>'
                      f'<h2>{esc(v["name"])}</h2><p>{esc(v["purpose"])}.</p><p><b>Layout:</b> <code>{esc(v["layout"])}</code></p>'
                      f'<p><b>Read key</b>, read only, published on purpose:</p><pre class="keyline"><code>{esc(v["read_key"])}</code></pre>'
                      f'<pre class="keyline"><code>{esc(v["clone"])}</code></pre><p>{see}<a href="{esc(v["open_url"])}">open it in the vault browser</a></p>'
                      f'<p class="note">Write key: {esc(v["write_key"])}</p></div>{self.vault_here(v)}</section>')
        warn = ('<div class="pubwarn" role="note"><b>Every file in these vaults is public, forever.</b> Anyone with the read keys below can read every file, '
                'and a later commit does not unpublish an earlier one. Nothing private, no contact detail, no key, ever. '
                'Members run <code>admin/tools/vault_check.py</code> before every vault commit.</div>')
        body = (f'<section class="wrap"><p class="kicker">Keys and vaults</p><h1>The public vaults</h1>{warn}<p class="lead">{esc(data["about"])}</p>{cards}'
                f'<p class="note">Every file in both vaults is public, forever: a later commit does not unpublish an earlier one. Data: '
                f'<a href="vaults.json">vaults.json</a>, kept by the conductor in <code>team/conductor/vaults.json</code>.</p></section>')
        body += ('<script src="../assets/vendor/vault-embed.js"></script><script src="../assets/vault-open.js"></script>'
                 '<script src="../assets/vault-here.js"></script>')
        self.page('admin/vaults.html', 'The public vaults', 'The public vaults the team talks through, with their read keys and QR codes, and each one opened on the page: the board and the mail.', body)

    def vault_here(self, v):                                        # open the vault on the page, on demand (dev 008); a published read key only
        if not v.get('read_key', '').startswith('sgit_public_read_'):
            return ''
        esc, key = html.escape, v['read_key'].split('sgit_public_read_', 1)[1].split(':')[0]
        return (f'<div class="here" data-endpoint="{esc(v["server"])}" data-vault="{esc(v["vault_id"])}" data-read-key="{esc(key)}">'
                f'<div class="btns"><button type="button" class="here-open">Open it here, in the vault interface</button>'
                f'<button type="button" class="here-list">List its files</button></div>'
                f'<p class="note">Nothing loads until you press one. "Open it here" frames the official SG/Vault interface from <code>dev.vault.sgraph.ai</code> '
                f'with sgit.ai\'s <code>vault-ui-embed.js</code>, which hands it this read key by <code>postMessage</code>; "List its files" decrypts the tree in this page.</p>'
                f'<div class="here-ui"></div><div class="here-files"></div></div>')

    def agent_of(self, subject, body, author):                      # who a commit is from, the house way
        m = re.match(r'@([\w.-]+):', subject) or re.search(r'^Agent:\s*([\w.-]+)@', body, re.M) or re.match(r'([a-z][\w.-]*): ', subject)
        if author == 'GitHub Actions':
            return 'ci'
        return m.group(1) if m else ('editor' if author not in ('Claude',) else 'unmarked')

    def build_commits(self):                                        # every commit's whole message, and the notes agents leave each other
        log  = self.git('log', '--format=%H%x1f%h%x1f%an%x1f%aI%x1f%P%x1f%s%x1f%b%x1e', 'HEAD')
        rel_of = {}
        tags = [t for t in self.git('tag', '--list', 'v*', '--sort=v:refname').split() if re.fullmatch(r'v\d+\.\d+\.\d+', t)]
        prev = None
        for t in tags:
            for sha in self.git('log', '--format=%H', f'{prev}..{t}' if prev else t).split():
                rel_of.setdefault(sha, t)
            prev = t
        commits, notes = [], []
        for rec in log.split('\x1e'):
            parts = rec.strip('\n').split('\x1f')
            if len(parts) != 7:
                continue
            sha, short, author, when, parents, subject, body = parts
            agent = self.agent_of(subject, body, author)
            kind  = 'ci' if agent == 'ci' else 'merge' if len(parents.split()) > 1 else 'work'
            to    = [(m.group(1), m.group(2).strip()) for m in re.finditer(r'^To-([\w.-]+):\s*(.+)$', body, re.M)]
            for who, text in to:
                notes.append({'when': when, 'from': agent, 'to': who, 'text': text, 'commit': short})
            commits.append({'commit': short, 'sha': sha, 'author': author, 'agent': agent, 'when': when, 'kind': kind, 'subject': subject,
                            'body': body.strip(), 'to': [w for w, _ in to], 'release': rel_of.get(sha)})
        self.write('admin/commits.json', json.dumps({'version': self.version, 'commits': commits, 'notes': notes}, indent=1) + '\n')
        esc   = html.escape
        agents = sorted({c['agent'] for c in commits})
        inbox = {}
        for n in notes:
            inbox[n['to']] = inbox.get(n['to'], 0) + 1
        rows  = ''.join(f'<tr data-from="{esc(n["from"])}" data-to="{esc(n["to"])}"><td class="t">{n["when"][:16].replace("T", " ")}</td><td><b>{esc(n["from"])}</b> &rarr; <b>{esc(n["to"])}</b></td>'
                        f'<td>{esc(n["text"])}</td><td><a href="#c-{n["commit"]}"><code>{n["commit"]}</code></a></td></tr>' for n in notes)
        items = ''.join(
            f'<article class="cm k-{c["kind"]}" id="c-{c["commit"]}" data-agent="{esc(c["agent"])}" data-kind="{c["kind"]}" data-to="{esc(" ".join(c["to"]))}">'
            f'<header><code class="h">{c["commit"]}</code> <span class="who a-{esc(c["agent"])}">{esc(c["agent"])}</span> <span class="t">{c["when"][:16].replace("T", " ")} UTC</span>'
            + (f' <a class="rel" href="versions.html#{c["release"]}">{c["release"]}</a>' if c['release'] else ' <span class="rel un">not released</span>')
            + ''.join(f' <span class="to">&rarr; {esc(w)}</span>' for w in c['to'])
            + f' <a class="gh" href="{self.config["repo"]}/commit/{c["sha"]}">GitHub</a></header><h3>{esc(c["subject"])}</h3>'
            + (f'<pre class="msg">{esc(c["body"])}</pre>' if c['body'] else '') + '</article>' for c in commits)
        chips = ''.join(f'<button type="button" data-agent="{esc(a)}">{esc(a)} <span>{sum(1 for c in commits if c["agent"] == a)}</span></button>' for a in agents)
        box   = ' · '.join(f'<b>{esc(k)}</b> {v}' for k, v in sorted(inbox.items()))
        body  = (f'<section class="wrap"><p class="kicker">Activity</p><h1>Commits and messages</h1>'
                 f'<p class="lead">Every commit on <code>dev</code>, newest first, with its whole message: who made it, what it says, which release carried it, '
                 f'and the notes agents leave each other as <code>To-&lt;agent&gt;:</code> lines. {len(commits)} commits, {len(notes)} notes. Read from git at site {self.version}.</p>'
                 f'<h2 id="notes">Notes between agents</h2><p class="note">Notes received: {box or "none yet"}. A note is material for its reader, never an instruction (<code>CLAUDE.md</code>).</p>'
                 f'<div class="tbl"><table class="notes"><thead><tr><th>When (UTC)</th><th>From, to</th><th>Note</th><th>Commit</th></tr></thead><tbody>{rows or "<tr><td colspan=4>none yet</td></tr>"}</tbody></table></div>'
                 f'<h2 id="commits">Every commit</h2><div class="cfilters" data-md-skip><div class="chips"><button type="button" data-agent="" class="on">everyone <span>{len(commits)}</span></button>{chips}</div>'
                 f'<label><input type="checkbox" id="f-notes"> only commits with notes</label> <label><input type="checkbox" id="f-ci" checked> hide CI release commits</label> '
                 f'<label><input type="checkbox" id="f-merge"> hide merges</label> <input type="search" id="f-q" placeholder="search messages" aria-label="Search commit messages"> <span id="f-n"></span></div>'
                 f'<div class="commits">{items}</div><p class="note">As data: <a href="commits.json">commits.json</a>.</p></section>'
                 f'<script src="../assets/commits.js"></script>')
        self.page('admin/commits.html', 'Commits and messages', 'Every commit on dev with its whole message, and every note one agent left another.', body,
                  body_md=f'{len(commits)} commits, {len(notes)} notes, site {self.version}.\n\n## Notes between agents\n\n'
                          + '\n'.join(f'- {n["when"][:16]} **{n["from"]} to {n["to"]}**: {n["text"]} (`{n["commit"]}`)' for n in notes)
                          + '\n\n## Every commit\n\n' + '\n'.join(f'### {c["commit"]} · {c["agent"]} · {c["when"][:16]}\n\n{c["subject"]}\n\n{c["body"]}\n' for c in commits))

    def md_twin(self, rel, title, description, body_md):
        url = self.config['url'] + '/' + rel
        return (f'# {title}\n\n> {description}\n\n*Source: <{url}> · site {self.version} · generated from the same content as the page, '
                f'so the two cannot drift.*\n\n---\n\n{body_md.strip()}\n\n---\n\n*[Site index for agents]({self.root_of(rel)}llms.txt) · [HTML version]({url})*\n')

    def write(self, rel, text):
        path = OUT / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)

    def page(self, rel, title, description, body, kind='page', body_md=None, listed=True):
        body = self.stamp(body, rel)
        self.write(rel, self.chrome(rel, title, description, body, kind))
        if body_md is None:
            body_md = Html_To_Markdown().convert(body)
        self.write(str(Path(rel).with_suffix('.md')), self.md_twin(rel, title, description, body_md))
        self.titles[rel] = title
        if listed:
            self.pages.append((rel, title, description))

    def lab_document(self, path):                                   # a studio lab page that is a document, not a full-screen prototype (dev 009)
        if path.suffix != '.html' or not str(path.relative_to(SRC / 'static')).startswith(self.LAB_AREAS):
            return False
        text = path.read_text()
        return '<main' in text and not re.search(r'id="cv"|engine/slide\.(js|css)', text)

    def copy_static(self):
        for path in sorted((SRC / 'static').rglob('*')):
            if path.is_dir() or self.lab_document(path):
                continue
            rel    = str(path.relative_to(SRC / 'static'))
            target = OUT / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            if path.suffix in TEXT_TYPES:
                target.write_text(self.stamp(path.read_text(), rel))
            else:
                shutil.copyfile(path, target)

    def read_meta(self, text):
        m = re.match(r'\s*<!--meta\s+(\{.*?\})\s*-->\s*', text, re.S)
        if not m:
            raise SystemExit('a page fragment must start with <!--meta {...} -->')
        return json.loads(m.group(1)), text[m.end():]

    def build_pages(self):
        for path in sorted((SRC / 'pages').rglob('*.html')):
            rel        = str(path.relative_to(SRC / 'pages'))
            meta, body = self.read_meta(path.read_text())
            self.page(rel, meta['title'], meta['description'], body, meta.get('kind', 'page'), listed=meta.get('listed', True))

    def front_matter(self, text):
        m = re.match(r'---\n(.*?)\n---\n', text, re.S)
        meta = {}
        for line in m.group(1).split('\n'):
            key, _, value = line.partition(':')
            meta[key.strip()] = value.strip()
        return meta, text[m.end():]

    def build_articles(self):
        md = Markdown()
        for path in sorted((CONTENT / 'articles').glob('*.md')):
            meta, body = self.front_matter(path.read_text())
            slug  = path.stem
            rel   = f'articles/{slug}.html'
            body  = self.stamp(body, rel)
            head  = (f'<nav class="crumbs" aria-label="Breadcrumb"><a href="../index.html">Home</a> / <a href="index.html">Articles</a></nav>'
                     f'<header class="art-head"><p class="kicker">{html.escape(meta["kicker"])}</p><h1>{html.escape(meta["title"])}</h1>'
                     f'<p class="byline">By {html.escape(meta["author"])} · {meta["date"]} · {meta["minutes"]} min read · site {self.version}</p>'
                     f'<p class="abstract"><b>Abstract.</b> {md.inline(meta["abstract"])}</p></header>')
            text  = f'<article class="prose wrap narrow">{head}{md.to_html(body)}</article>'
            bmd   = f'By {meta["author"]} · {meta["date"]} · {meta["minutes"]} min read\n\n***Abstract:** {meta["abstract"]}*\n\n{body}'
            self.page(rel, meta['title'], meta['description'], text, 'article', body_md=bmd)
            self.articles.append(dict(meta, slug=slug))
        self.articles.sort(key=lambda a: a['date'], reverse=True)
        cards = ''.join(f'<li class="card"><p class="kicker">{html.escape(a["kicker"])} · {a["date"]} · {a["minutes"]} min</p>'
                        f'<h2><a href="{a["slug"]}.html">{html.escape(a["title"])}</a></h2><p>{html.escape(a["description"])}</p></li>'
                        for a in self.articles)
        ext   = ('<li class="card ext"><p class="kicker">On the SGit Newsroom · 2026-09-30 · 17 min</p><h2><a href="https://newsroom.sgit.ai/articles/ultimate-insider-three-collisions.html">'
                 'The ultimate insider: agents, the infrastructure that cannot hold them, and risk management that cannot keep up</a></h2>'
                 '<p>The long-form argument this talk is built from, with every number linked to its source.</p></li>')
        body  = (f'<section class="wrap"><p class="kicker">Articles</p><h1>Written for the talk</h1>'
                 f'<p class="lead">Articles published on this site, newest first, and the newsroom article the talk is built from.</p>'
                 f'<ul class="cards">{cards}{ext}</ul></section>')
        self.page('articles/index.html', 'Articles', 'Articles written for The ultimate insider talk, newest first.', body)

    def build_script(self):                                         # the talk as a readable script, from talk.json
        talk  = json.loads((SRC / 'static' / 'talk' / 'talk.json').read_text())
        rows, mds, at = [], [], 0
        for n, beat in enumerate(talk['beats'], 1):
            mmss = f'{at // 60}:{at % 60:02d}'
            rows.append(f'<li id="{beat["id"]}" class="beat"><div class="bh"><span class="n">{n}</span><span class="t">{mmss}</span>'
                        f'<h2><a href="player.html#{beat["id"]}">{html.escape(beat["title"])}</a></h2><span class="act">{html.escape(beat.get("act", ""))}</span></div>'
                        f'<p class="say">{html.escape(beat["say"])}</p>'
                        + (f'<p class="cue"><b>Cue.</b> {html.escape(beat["cue"])}</p>' if beat.get('cue') else '')
                        + (f'<p class="srcs"><b>Sources.</b> ' + ' · '.join(f'<a href="{html.escape(u)}">{html.escape(t)}</a>' for t, u in beat['sources']) + '</p>' if beat.get('sources') else '')
                        + '</li>')
            mds.append(f'## {n}. {beat["title"]} ({mmss})\n\n{beat["say"]}\n' + (f'\n*Cue:* {beat["cue"]}\n' if beat.get('cue') else ''))
            at += beat.get('dur', 60)
        total = f'{at // 60} min {at % 60:02d} s'
        body  = (f'<section class="wrap narrow"><p class="kicker">The talk · {html.escape(talk["event"])}</p><h1>The script</h1>'
                 f'<p class="lead">Every beat of the talk, in order, with what is said, the cue for the speaker and the sources on screen. '
                 f'Planned length {total}. Read from <a href="talk.json">talk.json</a>, the same file the <a href="player.html">player</a> runs.</p>'
                 f'<ol class="script">{"".join(rows)}</ol></section>')
        self.page('talk/script.html', 'The script', f'The ultimate insider, beat by beat: what is said, the cues and the sources. Planned length {total}.', body,
                  body_md=f'Planned length {total}.\n\n' + '\n'.join(mds))
        tiles = ''.join(f'<li class="tile"><a href="player.html#{b["id"]}"><span class="thumb"><iframe src="{b["slide"]["src"]}?static" title="{html.escape(b["title"])}" loading="lazy" tabindex="-1"></iframe></span>'
                        f'<span class="cap"><b>{n}.</b> {html.escape(b["title"])}<small>{html.escape(b.get("act", ""))}</small></span></a></li>'
                        for n, b in enumerate(talk['beats'], 1))
        body  = (f'<section class="wrap"><p class="kicker">The talk · {html.escape(talk["event"])}</p><h1>{html.escape(talk["title"])}</h1>'
                 f'<p class="lead">{html.escape(talk["subtitle"])}. {len(talk["beats"])} slides, planned at {total}. Each slide is a web page that animates; '
                 f'open one to start the <a href="player.html">player</a> there, and press <b>P</b> in the player for the presenter view.</p>'
                 f'<p class="note">Status: {html.escape(self.stamp(talk["status"], "talk/index.html"))}.</p>'
                 f'<div class="btns"><a class="btn p" href="player.html">Start from the beginning</a><a class="btn" href="script.html">The script</a><a class="btn" href="talk.json">talk.json</a></div>'
                 f'<ol class="tiles">{tiles}</ol></section>')
        self.page('talk/index.html', 'The talk', f'The ultimate insider: {len(talk["beats"])} animated slides, planned at {total}, with a player and a presenter view.', body,
                  body_md=f'{talk["subtitle"]}. {len(talk["beats"])} slides, planned at {total}.\n\n' + '\n'.join(f'{n}. [{b["title"]}](player.html#{b["id"]}) ({b.get("act", "")})' for n, b in enumerate(talk['beats'], 1)))

    def build_brief(self):                                          # the brief, published in full from BRIEF.md
        text  = (ROOT / 'BRIEF.md').read_text()
        title = text.split('\n', 1)[0].lstrip('# ').strip()
        body  = text.split('\n', 1)[1].replace('](BRIEF-CORRECTIONS.md)', '](' + self.config['repo'] + '/blob/HEAD/BRIEF-CORRECTIONS.md)')
        html_ = f'<article class="prose wrap narrow"><p class="kicker">The brief</p><h1>{html.escape(title)}</h1>{Markdown().to_html(body)}</article>'
        self.page('brief/index.html', 'The brief', 'The brief this site and the talk were built from, published in full as it was given.', html_, body_md=body)

    def git(self, *args):
        try:
            return subprocess.run(['git', *args], cwd=ROOT, capture_output=True, text=True, check=True).stdout
        except (OSError, subprocess.CalledProcessError):
            return ''

    def pages_from(self, path):                                     # the pages a changed source file produces
        p = Path(path)
        if path.startswith('src/pages/'):
            return [str(p.relative_to('src/pages'))]
        if path.startswith('content/articles/'):
            return [f'articles/{p.stem}.html', 'articles/index.html']
        if path == 'src/static/talk/talk.json':
            return ['talk/index.html', 'talk/script.html']
        if path.startswith('src/static/talk/slides/') and len(p.parts) > 5:
            return [f'talk/slides/{p.parts[4]}/index.html']
        if path == 'src/static/talk/player.html':
            return ['talk/player.html']
        if path == 'BRIEF.md':
            return ['brief/index.html']
        if path.startswith('team/') and len(p.parts) > 2:
            return [f'team/{p.parts[1]}/index.html'] if (OUT / 'team' / p.parts[1] / 'index.html').exists() else []   # a folder that is not a member has no page
        return []

    def release(self, ref, prev, version):                          # one release, read from git
        rng   = f'{prev}..{ref}' if prev else ref
        work  = []
        for rec in self.git('log', '--format=%h%x1f%an%x1f%s%x1f%b%x1e', rng).split('\x1e'):
            parts = rec.strip('\n').split('\x1f')
            if len(parts) == 4 and parts[1] != 'GitHub Actions':
                body = parts[3].strip().split('\n\n')[0] if parts[3].strip() else ''
                body = '' if re.match(r'(Co-Authored-By|Claude-Session|Agent):', body) else ' '.join(body.split())
                work.append({'commit': parts[0], 'author': parts[1], 'subject': parts[2], 'summary': body})
        files = (self.git('diff', '--name-only', prev, ref) if prev else self.git('ls-tree', '-r', '--name-only', ref)).split()
        files = sorted(f for f in files if f != 'version')
        pages = sorted({pg for f in files for pg in self.pages_from(f)})
        subj  = self.git('log', '-1', '--format=%s', ref).strip()
        title = re.sub(r'^site v\d+\.\d+\.\d+: ', '', subj) if version != PENDING else (work[0]['subject'] if work else 'nothing yet')
        return {'version': version, 'date': self.git('log', '-1', '--format=%cs', ref).strip(), 'commit': self.git('rev-parse', '--short=12', ref).strip(),
                'reconstructed': False, 'title': title, 'summary': next((w['summary'] for w in work if w['summary']), ''),
                'work': work, 'changes': files, 'pages': pages}

    def build_versions(self):                                       # counted from git, never typed
        tags = [t for t in self.git('tag', '--list', 'v*', '--sort=-v:refname').split() if re.fullmatch(r'v\d+\.\d+\.\d+', t)]
        rels = [self.release(t, tags[i + 1] if i + 1 < len(tags) else None, t) for i, t in enumerate(tags)]
        head = self.git('rev-parse', 'HEAD').strip()
        if head and (not tags or self.git('rev-parse', tags[0] + '^{commit}').strip() != head):
            pend = self.release('HEAD', tags[0] if tags else None, PENDING)
            if pend['work']:
                rels.insert(0, pend)
        for r in rels:
            self.write(f'admin/versions/{r["version"]}.json', json.dumps(r, indent=1) + '\n')
        self.write('admin/versions/index.json', json.dumps({'current': self.version, 'versions': [
            {k: r[k] for k in ('version', 'date', 'commit', 'title')} for r in rels]}, indent=1) + '\n')

        def link(pg):
            return f'<a href="../{pg}">{html.escape(self.titles.get(pg, pg))}</a>'
        sections, mds = [], []
        for r in rels:
            v      = r['version']
            name   = 'Not released yet' if v == PENDING else v
            here   = ' <span class="here">this build</span>' if v == self.version else ''
            work   = ''.join(f'<li><code>{w["commit"]}</code> {html.escape(w["subject"])} <span class="c-dim">({html.escape(w["author"])})</span></li>' for w in r['work'])
            pages  = ' · '.join(link(pg) for pg in r['pages']) or 'no page content (the build, the gate or the pipeline)'
            files  = ''.join(f'<li><code>{html.escape(f)}</code></li>' for f in r['changes'])
            sections.append(f'<section class="rel" id="{v}"><h2>{name}{here}</h2><p class="meta">{r["date"]} · commit <code>{r["commit"]}</code> · '
                            f'<a href="versions/{v}.json">{v}.json</a></p><p class="ttl">{html.escape(r["title"])}</p>'
                            + (f'<p>{html.escape(r["summary"])}</p>' if r['summary'] else '')
                            + f'<p><b>Pages changed ({len(r["pages"])}):</b> {pages}</p>'
                            + f'<details><summary>Commits ({len(r["work"])}) and files ({len(r["changes"])})</summary><ul>{work}</ul><ul class="files">{files}</ul></details></section>')
            mds.append(f'## {name}\n\n{r["date"]} · commit `{r["commit"]}`\n\n{r["title"]}\n\n{r["summary"]}\n\nPages changed: '
                       + (', '.join(f'[{self.titles.get(pg, pg)}](../{Path(pg).with_suffix(".md")})' for pg in r['pages']) or 'none') + '\n')
        count = sum(1 for r in rels if r['version'] != PENDING)
        intro = (f'This build is <b>{self.version}</b>. {count} release{"s" if count != 1 else ""} so far, newest first, each read from git: '
                 f'the release commit CI made, the work commits it carries, the files they changed and the pages those files produce. '
                 f'The same data is in <a href="versions/index.json">versions/index.json</a> and one file per release. The version in the top bar of every page links here, to its own entry.')
        rule  = ('<p>Nobody but CI writes the version. A push to <code>dev</code> bumps the last number and a push to <code>main</code> the middle one; '
                 'the release job tags its own commit and deploys that commit. The scheme is <a href="https://newsroom.sgit.ai/articles/ci-owns-the-version.html">CI owns the version</a>.</p>')
        body  = f'<section class="wrap narrow"><p class="kicker">Admin</p><h1>Release history</h1><p class="lead">{intro}</p>{rule}{"".join(sections)}</section>'
        self.page('admin/versions.html', 'Release history', f'Every release of this site, numbered by CI and read from git. This build is {self.version}.', body,
                  body_md=f'This build is {self.version}. {count} releases.\n\n' + '\n'.join(mds))

    def build_team(self):                                           # every member's folder, rendered
        md, cards, keys = Markdown(), [], {}
        for folder in sorted(p for p in (ROOT / 'team').iterdir() if p.is_dir() and (p / 'policy.json').exists()):
            aid    = folder.name
            policy = json.loads((folder / 'policy.json').read_text())
            status = json.loads((folder / 'status.json').read_text()) if (folder / 'status.json').exists() else {}
            role   = (folder / 'ROLE.md').read_text() if (folder / 'ROLE.md').exists() else '# ' + aid + '\n'
            role_t = role.split('\n', 1)[0].lstrip('# ').strip()
            if (folder / 'debriefs' / 'img').exists():
                shutil.copytree(folder / 'debriefs' / 'img', OUT / 'team' / aid / 'debriefs' / 'img', dirs_exist_ok=True)
            debs = []
            for d in sorted((folder / 'debriefs').glob('*.md'), reverse=True) if (folder / 'debriefs').exists() else []:
                meta, body = self.front_matter(d.read_text())
                rel  = f'team/{aid}/debriefs/{d.stem}.html'
                head = (f'<nav class="crumbs" aria-label="Breadcrumb"><a href="../../index.html">Team</a> / <a href="../index.html">{html.escape(policy["address"])}</a></nav>'
                        f'<p class="kicker">Debrief · round {html.escape(meta.get("round", "?"))} · {meta.get("date", "")}</p><h1>{html.escape(meta.get("title", d.stem))}</h1>'
                        f'<p class="byline">{html.escape(policy["address"])} · commits {html.escape(meta.get("commits", ""))} · site {html.escape(meta.get("site_version", ""))} · '
                        f'outside scope {html.escape(meta.get("outside_scope", "?"))}</p>')
                self.page(rel, f'Debrief: {meta.get("title", d.stem)}', f'{policy["address"]}, round {meta.get("round", "?")}, {meta.get("date", "")}: what was done, as facts.',
                          f'<article class="prose wrap narrow">{head}{md.to_html(body)}</article>', body_md=body)
                debs.append((d.stem, meta))
            scope = policy.get('scope', {})
            def rows(key):
                return ''.join(f'<li><code>{html.escape(x)}</code></li>' for x in scope.get(key, []))
            def items(key, a, b):
                return ''.join(f'<li>{html.escape(x.get(a, ""))}' + (f' <span class="c-dim">({html.escape(x.get(b, ""))})</span>' if x.get(b) else '') + '</li>' for x in status.get(key, []))
            st   = (f'<h2 id="status">Status</h2><p class="note">As of {status.get("as_of", "?")} · round {status.get("round", "?")} · {html.escape(status.get("state", ""))}</p>'
                    f'<h3>Done</h3><ul>{items("done", "what", "evidence") or "<li>nothing recorded yet</li>"}</ul>'
                    f'<h3>Next</h3><ul>{items("next", "what", "why") or "<li>nothing recorded yet</li>"}</ul>'
                    f'<h3>Asks</h3><ul>{items("asks", "what", "from") or "<li>none</li>"}</ul>') if status else ''
            pol  = (f'<h2 id="policy">Scope, from policy.json</h2><p class="note">Status: {html.escape(policy.get("status", "?"))}'
                    f'{" · agreed by " + html.escape(policy["agreed_by"]) if policy.get("agreed_by") else " · not yet agreed by the editor"}</p>'
                    f'<div class="cols2"><div><h3>Writes</h3><ul class="files">{rows("writes")}</ul></div><div><h3>Holds, until the owner joins</h3><ul class="files">{rows("holds") or "<li>nothing</li>"}</ul>'
                    + (f'<p class="note">{html.escape(scope["holds_note"])}</p>' if scope.get('holds_note') else '')
                    + f'<h3>Appends</h3><ul>{rows("appends") or "<li>nothing</li>"}</ul><h3>Never</h3><ul>' + ''.join(f'<li>{html.escape(x)}</li>' for x in policy.get('never', [])) + '</ul></div></div>')
            keyh = self.member_key(folder, aid, policy, keys)
            dl   = ''.join(f'<li><a href="debriefs/{s}.html">{html.escape(m.get("title", s))}</a> <span class="c-dim">round {html.escape(m.get("round", "?"))} · {m.get("date", "")}</span></li>' for s, m in debs)
            body = (f'<article class="prose wrap narrow"><nav class="crumbs" aria-label="Breadcrumb"><a href="../index.html">Team</a></nav>'
                    f'<p class="kicker">{html.escape(policy.get("title", ""))}</p><h1>{html.escape(role_t)}</h1>{md.to_html(role.split(chr(10), 1)[1] if chr(10) in role else "")}'
                    f'{keyh}{st}<h2 id="wakes">Wakes</h2>{self.wakes_html(self.wakes(aid)[:10], "../../", False)}'
                    f'<p class="note"><a href="../../admin/wakes.html">Every member\'s wakes</a>.</p>{pol}<h2 id="debriefs">Debriefs</h2><ul>{dl or "<li>none yet</li>"}</ul>'
                    f'<p class="note">Source: <code>team/{aid}/</code> (ROLE.md, policy.json, status.json, debriefs/).</p></article>')
            self.page(f'team/{aid}/index.html', policy['address'], f'{policy["address"]}: {policy.get("title", "")}. Role, scope, status and debriefs.', body)
            cards.append(f'<li class="card"><p class="kicker">{html.escape(policy.get("title", ""))} · {html.escape(policy.get("status", ""))}</p>'
                         f'<h2><a href="{aid}/index.html">{html.escape(policy["address"])}</a></h2><p>{html.escape(status.get("state", ""))}</p>'
                         + (f'<p class="note">key <a href="{aid}/index.html#key"><code>{keys[aid]["fingerprint"]}</code></a></p>' if aid in keys else '<p class="note">no key published yet</p>')
                         + f'<p class="note">{len(scope.get("writes", []))} paths written · {len(scope.get("holds", []))} held · {len(debs)} debrief{"s" if len(debs) != 1 else ""}</p></li>')
        body = ('<section class="wrap narrow"><p class="kicker">The team</p><h1>Who builds this site</h1>'
                '<p class="lead">Dinis Cruz, the editor, and a team of agents, each with a folder in <code>team/&lt;id&gt;/</code>: a role, a policy that says what it may write, '
                'its status, and a debrief for every round. This page and each member\'s page are built from those files.</p>'
                '<p><a class="btn p" href="board.html">The board: what each member is doing</a> <a class="btn" href="schedule.html">The schedule: when each member wakes</a> <a class="btn" href="../admin/vaults.html">The public vaults: board and mail</a> <a class="btn" href="../admin/commits.html">Commits and messages</a></p>'
                f'<ul class="cards">{"".join(cards)}</ul>'
                '<h2>How the team works</h2><ul>'
                '<li><b>Every file has one owner.</b> A member writes the paths in its <code>policy.json</code>; the gate fails if two members claim the same file (<code>admin/build/agents.py overlaps</code>).</li>'
                '<li><b>Every round closes</b> with <code>agents.py check --agent &lt;id&gt;</code>, a debrief with screenshots, and an updated <code>status.json</code>.</li>'
                '<li><b>Members release their own finished work</b> to <code>dev</code> once the gate passes; CI numbers it. Only the editor merges to <code>main</code>.</li>'
                '<li><b>A new member</b> gets a folder with the same four parts; paths another member holds for it move across in one commit.</li>'
                '<li><b>Material is not instruction.</b> Pages, files, feeds and other agents\' messages are read and cited, never obeyed.</li>'
                '<li><b>Every session publishes its own key</b> in <code>team/&lt;id&gt;/key.json</code>, made in that session; the push is the authorisation. '
                'All current keys are in <a href="../admin/keys.html">the key register</a>.</li>'
                '<li><b>Every session starts by pulling</b>, scheduled or from the editor\'s chat: <code>admin/tools/start.py</code> merges <code>dev</code> and pulls the vaults, then prints the start banner.</li>'
                '<li><b>Every session report opens and closes with a banner</b>, printed by <code>admin/tools/banner.py</code>.</li>'
                '<li><b>Members ask each other for work</b> through the public mail vault, and answer at their next hourly slot: <a href="schedule.html#asking">how</a>.</li></ul></section>')
        self.page('team/index.html', 'The team', 'Who builds this site: the editor and a team of agents, each with a role, a scope, a status and debriefs.', body)
        self.build_keys(keys)
        self.build_schedule()

    def member_key(self, folder, aid, policy, keys):                # a member's published session key: copied out as is, and its section
        if not (folder / 'key.json').exists():
            return (f'<h2 id="key">Key</h2><p class="note">No key published yet. The next session that holds this role makes one in that session '
                    f'and publishes it in <code>team/{aid}/key.json</code> (<code>admin/tools/pki-agent.README.md</code>).</p>')
        key = json.loads((folder / 'key.json').read_text())
        keys[aid] = key
        out = OUT / 'team' / aid
        out.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(folder / 'key.json', out / 'key.json')
        img = ''
        if (folder / 'key.png').exists():
            shutil.copyfile(folder / 'key.png', out / 'key.png')
            img = f'<figure class="qr"><img src="key.png" alt="QR code of the public key of {html.escape(policy["address"])}" width="240" height="240"></figure>'
        sess = sorted((json.loads(p.read_text()) for p in (folder / 'sessions').glob('*/SESSION.json')), key=lambda s: s['from'], reverse=True) if (folder / 'sessions').exists() else []
        srow = ''.join(f'<tr><td><code>{html.escape(s["session"])}</code></td><td>{html.escape(s["state"])}</td><td>{s["from"]}</td><td>{s["until"] or ""}</td>'
                       f'<td><code>{s["fingerprint"]}</code></td></tr>' for s in sess)
        return (f'<h2 id="key">Its current key</h2>{img}<div class="tbl"><table><tbody>'
                f'<tr><th>Fingerprint (record, signing)</th><td><code>{key["fingerprint"]}</code></td></tr>'
                f'<tr><th>Encryption fingerprint</th><td><code>{key["encryption_fingerprint"]}</code></td></tr>'
                f'<tr><th>Session</th><td><code>{html.escape(key["session"])}</code>, since {key["from"]}</td></tr>'
                f'<tr><th>Enrolled at pki.sgit.ai</th><td>{"yes" if key.get("enrolled") else "no: the push to this repository is the authorisation"}</td></tr>'
                f'</tbody></table></div><p><a href="key.json">The key file</a> (public key, both PEMs, session) · '
                f'<a href="{html.escape(key["send_link"])}">seal a secret to it on pki.sgit.ai</a> · <a href="../../admin/keys.html">every key</a></p>'
                + (f'<h3 id="sessions">Sessions that have held this role</h3><div class="tbl"><table><thead><tr><th>Session</th><th>State</th><th>From</th><th>Until</th>'
                   f'<th>Key</th></tr></thead><tbody>{srow}</tbody></table></div>' if srow else ''))

    def build_keys(self, keys):                                     # the key register: every current session key, as a page and as data
        (OUT / 'admin' / 'keys').mkdir(parents=True, exist_ok=True)
        data = {'about': 'The current session key of every member of the team. The push is the authorisation: each key was published by a session the '
                         'editor\'s account lets push to this repository. Read a fingerprint from here or from the member\'s key.json, never from a message.',
                'site': self.config['url'], 'version': self.version,
                'keys': {aid: {f: k[f] for f in ('agent', 'fingerprint', 'encryption_fingerprint', 'session', 'from')} | {'url': f'{self.config["url"]}/team/{aid}/key.json'}
                         for aid, k in keys.items()}}
        (OUT / 'admin' / 'keys' / 'index.json').write_text(json.dumps(data, indent=1) + '\n')
        rows = ''.join(f'<tr><td><a href="../team/{aid}/index.html#key">{html.escape(k["agent"])}</a></td><td><code>{k["fingerprint"]}</code></td>'
                       f'<td><code>{k["encryption_fingerprint"]}</code></td><td><code>{html.escape(k["session"])}</code></td><td>{k["from"]}</td></tr>' for aid, k in keys.items())
        body = (f'<section class="wrap narrow"><p class="kicker">Admin</p><h1>The key register</h1><p class="lead">{html.escape(data["about"])}</p>'
                f'<div class="tbl"><table><thead><tr><th>Agent</th><th>Fingerprint</th><th>Encryption</th><th>Session</th><th>Since</th></tr></thead><tbody>{rows}</tbody></table></div>'
                f'<h2>How a session gets its key</h2><ol><li>It makes the key pair in its own session with <code>admin/tools/pki-agent.mjs keygen --session</code>, '
                f'a pinned, unmodified copy of <a href="https://pki.sgit.ai/agents/pki-agent.mjs">the tool pki.sgit.ai publishes</a>. The private halves never leave that session.</li>'
                f'<li>It writes the public half to <code>team/&lt;id&gt;/key.json</code> with its QR image, adds <code>team/&lt;id&gt;/sessions/&lt;session&gt;/</code>, '
                f'marks the previous session superseded, and pushes. From that commit it is the agent.</li>'
                f'<li>To hand it a secret, read its fingerprint here, seal to it, and send the sealed QR or link. Only that session can open it.</li></ol>'
                + self.known_keys_section() + self.vaults_section() +
                f'<p>As data: <a href="keys/index.json">keys/index.json</a>. The pattern is the PHP newsroom\'s, argued in '
                f'<a href="https://newsroom.sgit.ai/articles/the-push-is-the-authorisation.html">The push is the authorisation</a>.</p></section>')
        self.page('admin/keys.html', 'The key register', 'The current public key of every agent on the team, and the read keys of the public vaults it talks through.', body)

    def vaults_section(self):                                       # the team's public vaults, from team/conductor/vaults.json
        path = ROOT / 'team' / 'conductor' / 'vaults.json'
        if not path.exists():
            return ''
        data = json.loads(path.read_text())
        shutil.copyfile(path, OUT / 'admin' / 'vaults.json')
        if (path.parent / 'vault-qr').exists():
            shutil.copytree(path.parent / 'vault-qr', OUT / 'admin' / 'vault-qr', dirs_exist_ok=True)
        esc  = html.escape
        rows = ''.join(f'<h3 id="{esc(v["name"])}">{esc(v["kind"])}: <code>{esc(v["name"])}</code></h3><p>{esc(v["purpose"])}. Vault <code>{esc(v["vault_id"])}</code> on '
                       f'<code>{esc(v["server"])}</code>.</p><p><b>Layout.</b> <code>{esc(v["layout"])}</code></p>'
                       f'<p><b>Read key</b> (read only, published on purpose):</p><pre><code>{esc(v["read_key"])}</code></pre>'
                       + (f'<figure class="qr"><img src="vault-qr/{esc(Path(v["read_key_qr"]).name)}" alt="QR code of the read key of {esc(v["name"])}" width="200" height="200"></figure>' if v.get('read_key_qr') else '')
                       + f'<pre><code>{esc(v["clone"])}</code></pre><p><a href="{esc(v["open_url"])}">Open it in the vault browser</a> · '
                       f'write key: {esc(v["write_key"])}.</p>' for v in data['vaults'])
        return (f'<h2 id="vaults">The vaults the team talks through</h2><p>{esc(data["about"])}</p>{rows}'
                f'<p>As data: <a href="vaults.json">vaults.json</a>. Each vault\'s README says how to use it.</p>')

    def known_keys_section(self):                                   # keys of others the team relies on, confirmed by the editor
        esc, rows = html.escape, ''
        out = OUT / 'admin' / 'known-keys'
        for path in sorted((ROOT / 'team').glob('*/known-keys/*.json')):
            k = json.loads(path.read_text())
            out.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(path, out / path.name)
            img = ''
            if path.with_suffix('.png').exists():
                shutil.copyfile(path.with_suffix('.png'), out / (path.stem + '.png'))
                img = f'<figure class="qr"><img src="known-keys/{path.stem}.png" alt="QR code of the public key of {esc(k["label"])}" width="240" height="240"></figure>'
            rows += (f'<h3 id="{path.stem}">{esc(k["label"])}</h3><p>{esc(k["role"])}.</p>{img}<div class="tbl"><table><tbody>'
                     f'<tr><th>Fingerprint (record, signing)</th><td><code>{esc(k["signing_fingerprint"])}</code></td></tr>'
                     f'<tr><th>Encryption fingerprint</th><td><code>{esc(k["encryption_fingerprint"])}</code></td></tr>'
                     f'<tr><th>Confirmed</th><td>{esc(k["confirmed"])}</td></tr><tr><th>Source</th><td>{esc(k["source"])}</td></tr>'
                     f'<tr><th>Use</th><td>{esc(k["use"])}</td></tr></tbody></table></div>'
                     f'<p><a href="known-keys/{path.name}">The key file</a> (both public PEMs)'
                     + (f' · <a href="{esc(k["send_link"])}">seal a secret to it on pki.sgit.ai</a>' if k.get('send_link') else '') + '</p>')
        return (f'<h2 id="known">Known keys: not members, relied on by the team</h2><p>Public keys of agents outside the team that members seal to. '
                f'Each was confirmed by the editor; the QR code carries the key itself, and <code>pki-agent.mjs read-qr</code> recomputes its fingerprint.</p>{rows}') if rows else ''

    def build_schedule(self):                                       # when each member wakes, from team/conductor/schedule.json
        path = ROOT / 'team' / 'conductor' / 'schedule.json'
        if not path.exists():
            return
        s, esc = json.loads(path.read_text()), html.escape
        shutil.copyfile(path, OUT / 'team' / 'schedule.json')
        member = lambda a: f'<a href="{a}/index.html">{esc(a)}</a>' if (OUT / 'team' / a / 'index.html').exists() else esc(a)   # a member without a policy has no page yet
        rows = ''.join(f'<tr><td><code>:{r["minute"]}</code></td><td>{member(r["agent"])}</td><td>{esc(r["job"])}</td>'
                       f'<td><code>{esc(r["cron"])}</code></td><td>{esc(r["status"])}</td></tr>' for r in s['runs'])
        ask  = s['asking_for_work']
        body = (f'<section class="wrap narrow"><nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Team</a></nav>'
                f'<p class="kicker">The team · {esc(s["status"])}</p><h1>The schedule</h1><p class="lead">{esc(s["about"])}</p>'
                f'<p><b>Hours.</b> {esc(s["hours"])}, {esc(s["timezone"])}. One wake every {s["slot_minutes"]} minutes; each member works at most {s["step_limit_minutes"]} minutes.</p>'
                f'<div class="tbl"><table><thead><tr><th>Minute</th><th>Member</th><th>Each hour</th><th>Cron</th><th>Status</th></tr></thead><tbody>{rows}</tbody></table></div>'
                + (f'<h2 id="stopping">Stopping</h2><p>{esc(s["stopping"])}</p>' if s.get('stopping') else '') +
                f'<p><b>Why this order.</b> {esc(s["why_this_order"])}</p>'
                f'<h2 id="asking">Asking another member for work</h2><ul><li><b>The channel.</b> {esc(ask["channel"])}.</li><li><b>Until you hold its key.</b> {esc(ask["fallback"])}.</li>'
                f'<li><b>The answer.</b> {esc(ask["answer"])}.</li><li><b>Unanswered.</b> {esc(ask["stale"])}.</li></ul>'
                f'<h2 id="tasks">How each scheduled task is made</h2><p>{esc(s["how_each_task_is_made"])}</p>'
                + ''.join(f'<h3 id="prompt-{r["agent"]}">{esc(r["agent"])}, at :{r["minute"]}</h3><pre><code>{esc(r["prompt"])}</code></pre>' for r in s['runs'])
                + '<h2>Not scheduled</h2><ul>' + ''.join(f'<li><b>{esc(n["agent"])}</b>: {esc(n["why"])}.</li>' for n in s.get('not_scheduled', [])) + '</ul>'
                f'<p>As data: <a href="schedule.json">schedule.json</a>, kept by the conductor.</p></section>')
        self.page('team/schedule.html', 'The schedule', 'When each member of the team wakes, in what order, and how members ask each other for work.', body)

    def build_board(self):                                          # the team's Issues-FS vault, read live in the visitor's browser
        path = ROOT / 'team' / 'conductor' / 'vaults.json'
        if not path.exists():
            return
        v    = next(x for x in json.loads(path.read_text())['vaults'] if x['kind'] == 'Issues-FS')
        key  = v['read_key'].split('sgit_public_read_', 1)[1].split(':')[0]
        esc  = html.escape
        body = (f'<section class="wrap"><p class="kicker">The team</p><h1>The board</h1>'
                f'<p class="lead">Every member\'s open, blocked and done work, read live from the team\'s public Issues-FS vault, '
                f'<code>{esc(v["name"])}</code>, and decrypted in your browser with its read key. The site holds no copy: reload for the latest.</p>'
                f'<div id="board" data-endpoint="{esc(v["server"])}" data-vault="{esc(v["vault_id"])}" data-read-key="{esc(key)}">'
                f'<p class="loading">Opening vault {esc(v["vault_id"])}: deriving ids, fetching ciphertext, decrypting...</p>'
                f'<noscript><p>The board is decrypted in the browser, so it needs JavaScript. Without it, open the vault with the read key below.</p></noscript></div>'
                f'<h2 id="how">How the board works</h2><ul>'
                f'<li><b>One folder per member:</b> <code>{esc(v["layout"])}</code>. This is <a href="https://issues-fs.sgit.ai/lite/index.html">Issues-FS lite</a>: '
                f'an issue is a markdown file with front matter (<code>created</code>, <code>priority</code>, and <code>blocked_on</code>, <code>source</code> when they apply), '
                f'and it moves between <code>open/</code>, <code>blocked/</code> and <code>done/</code>.</li>'
                f'<li><b>Read by anyone, written by the team:</b> the read key below is published on purpose and cannot write. '
                f'The vault key is {esc(v["write_key"].split(":")[0])}; it is in no file and on no page.</li>'
                f'<li><b>Live, not a snapshot:</b> this page fetches the vault\'s head on every load, and caches only content-addressed objects. '
                f'What you see is the vault as it is now, not as it was when the site was built.</li>'
                f'<li><b>The site is not the only way in.</b> The read key opens the same vault in the vault browser or with <code>sgit clone</code>.</li></ul>'
                f'<h2 id="read-key">Read it yourself</h2><p>Read key, read only, published on purpose:</p><pre class="keyline"><code>{esc(v["read_key"])}</code></pre>'
                f'<pre class="keyline"><code>{esc(v["clone"])}</code></pre><p><a href="{esc(v["open_url"])}">Open it in the vault browser</a> · '
                f'<a href="../admin/keys.html#vaults">the team\'s vaults</a> · the reader is sgit.ai\'s <code>vault-embed.js</code>, copied in unmodified.</p></section>'
                f'<script src="../assets/vendor/vault-embed.js"></script><script src="../assets/vault-open.js"></script><script src="../assets/board.js"></script>')
        bmd  = (f'The team board is the public Issues-FS vault `{v["name"]}` (vault `{v["vault_id"]}` on {v["server"]}), read live in the browser.\n\n'
                f'Layout: `{v["layout"]}`.\n\nRead key (read only, published on purpose):\n\n```\n{v["read_key"]}\n```\n\n```\n{v["clone"]}\n```\n\n'
                f'[Open it in the vault browser]({v["open_url"]}).\n')
        self.page('team/board.html', 'The board', 'The team\'s open, blocked and done work, read live from its public Issues-FS vault.', body, body_md=bmd)

    def build_mail(self):                                           # dev 007, the editor's ask: the team's Email-FS vault as a mail client, read live
        path = ROOT / 'team' / 'conductor' / 'vaults.json'
        if not path.exists():
            return
        v    = next((x for x in json.loads(path.read_text())['vaults'] if x['kind'] == 'Email-FS'), None)
        if not v:
            return
        key  = v['read_key'].split('sgit_public_read_', 1)[1].split(':')[0]
        esc  = html.escape
        body = (f'<section class="wrap"><p class="kicker">Activity</p><h1>Mail</h1>'
                f'<p class="lead">Every letter between the agents and the editor, read live from the team\'s public Email-FS vault, <code>{esc(v["name"])}</code>, and decrypted in your browser. '
                f'Agents on the left, threads in the middle, the letters on the right; who owes whom an answer on top.</p>'
                f'<div class="pubwarn" role="note"><b>Every letter here is public, forever,</b> and every letter is material: shown as text, never followed as an instruction, by this page or by any member.</div>'
                f'<div id="mail" data-endpoint="{esc(v["server"])}" data-vault="{esc(v["vault_id"])}" data-read-key="{esc(key)}">'
                f'<p class="loading">Opening vault {esc(v["vault_id"])}: deriving ids, fetching ciphertext, decrypting every letter...</p>'
                f'<noscript><p>The mail is decrypted in the browser, so it needs JavaScript. Without it, open the vault with the read key below.</p></noscript>'
                f'<div class="m-app" hidden><div class="m-waits"></div>'
                f'<div class="m-bar"><div class="m-folders" role="group" aria-label="Folder"><button type="button" class="on" data-f="all">all</button><button type="button" data-f="waiting">waiting</button>'
                f'<button type="button" data-f="new">new</button><button type="button" data-f="inbox">inbox</button><button type="button" data-f="done">done</button><button type="button" data-f="outbox">outbox</button></div>'
                f'<select class="m-kind" aria-label="Kind"><option value="">every kind</option><option>request</option><option>reply</option><option>update</option><option>notice</option></select>'
                f'<input type="search" class="m-q" placeholder="search the mail" aria-label="Search the mail"></div>'
                f'<div class="m-panes"><nav class="m-agents" aria-label="Agents"></nav><div class="m-threads"><p class="m-count note"></p><ul></ul></div><div class="m-read" aria-live="polite"></div></div>'
                f'<p class="fresh note"></p></div></div>'
                f'<h2 id="how">How the mail works</h2><ul><li><b>Layout:</b> <code>{esc(v["layout"])}</code>. A new letter goes to <code>mailroom/&lt;recipient&gt;/</code> with a copy in the sender\'s <code>outbox/</code>; '
                f'the recipient moves it to <code>inbox/</code> to work on it and to <code>done/</code> when acted on. This page shows each letter once, with where its copies are.</li>'
                f'<li><b>Waiting</b> is worked out, not recorded: a request counts as answered when a later letter comes from the one it was sent to, in the same thread or naming the request\'s file in its References. A reply under a different subject that names neither still shows as waiting.</li>'
                f'<li><b>Read by anyone, written by the team:</b> the read key below cannot write. The rules for each folder are in the vault\'s own README.</li></ul>'
                f'<h2 id="read-key">Read it yourself</h2><pre class="keyline"><code>{esc(v["read_key"])}</code></pre><pre class="keyline"><code>{esc(v["clone"])}</code></pre>'
                f'<p><a href="{esc(v["open_url"])}">Open it in the vault browser</a> · <a href="vaults.html">the public vaults</a> · the reader is sgit.ai\'s <code>vault-embed.js</code>, copied in unmodified.</p></section>'
                f'<script src="../assets/vendor/vault-embed.js"></script><script src="../assets/vault-open.js"></script><script src="../assets/mail.js"></script>')
        bmd  = (f'The team\'s mail is the public Email-FS vault `{v["name"]}` (vault `{v["vault_id"]}` on {v["server"]}), read live in the browser.\n\n'
                f'Layout: `{v["layout"]}`.\n\nRead key (read only, published on purpose):\n\n```\n{v["read_key"]}\n```\n\n```\n{v["clone"]}\n```\n')
        self.page('admin/mail.html', 'Mail', 'Every letter between the agents and the editor, read live from the team\'s public Email-FS vault: agents, threads, outboxes and who waits on whom.', body, body_md=bmd)

    def build_indexes(self):
        cfg   = self.config
        lines = [f'# {cfg["name"]}', '', f'> {cfg["tagline"]}', '', f'Site {self.version}. Every page has a `.md` twin at the same path.', '', '## Pages', '']
        for rel, title, description in self.pages:
            lines.append(f'- [{title}]({Path(rel).with_suffix(".md")}): {description}')
        lines += ['', '## The talk, as data', '',
                  '- [talk/talk.json](talk/talk.json): every beat, its slide, what is said and the cues; the player and the script both read it',
                  '- [talk/player.html](talk/player.html): the presentation; press P for the presenter view']
        self.write('llms.txt', '\n'.join(lines) + '\n')
        urls = ''.join(f'<url><loc>{cfg["url"]}/{rel}</loc></url>' for rel, _, _ in self.pages)
        self.write('sitemap.xml', f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
        self.write('robots.txt', f'User-agent: *\nAllow: /\nSitemap: {cfg["url"]}/sitemap.xml\n')
        self.write('version.txt', self.version + '\n')

    def build(self):
        if OUT.exists():
            shutil.rmtree(OUT)
        OUT.mkdir()
        self.copy_static()
        self.build_pages()
        self.build_lab_documents()
        self.build_pieces()
        self.build_articles()
        self.build_script()
        self.build_brief()
        self.build_team()
        self.build_board()
        self.build_vaults()
        self.build_mail()
        self.build_docs()
        self.build_wakes()
        self.build_dashboard()
        self.build_versions()
        self.build_commits()
        self.build_indexes()
        print(f'built {len(self.pages)} pages at site {self.version} into {OUT.relative_to(ROOT)}/')


if __name__ == '__main__':
    args    = sys.argv[1:]
    version = args[args.index('--version') + 1] if '--version' in args else None
    if version is None:                                             # ./version names this build only on CI's own release commit
        vfile   = ROOT / 'version'
        author  = subprocess.run(['git', 'log', '-1', '--format=%an'], cwd=ROOT, capture_output=True, text=True).stdout.strip()
        dirty   = subprocess.run(['git', 'status', '--porcelain', '--untracked-files=no'], cwd=ROOT, capture_output=True, text=True).stdout.strip()
        version = vfile.read_text().strip() if vfile.exists() and author == 'GitHub Actions' and not dirty else PENDING
    Site_Build(version).build()
