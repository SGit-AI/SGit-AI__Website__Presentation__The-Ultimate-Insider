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
        self.articles = []

    def root_of(self, rel):                                         # the relative path back to the site root
        return '../' * (len(Path(rel).parts) - 1)

    def stamp(self, text, rel):
        return text.replace('{{version}}', self.version).replace('{{root}}', self.root_of(rel))

    def chrome(self, rel, title, description, body, kind='page'):
        root  = self.root_of(rel)
        name  = self.config['name']
        nav   = ''.join(f'<a href="{root}{href}"{" aria-current=\"page\"" if href == rel else ""}>{label}</a>' for label, href in self.config['nav'])
        full  = title if rel == 'index.html' else f'{title} · {self.config["short"]}'
        canon = self.config['url'] + '/' + rel
        md    = Path(rel).with_suffix('.md').name
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
<link rel="icon" href="{root}assets/favicon.svg">
<link rel="stylesheet" href="{root}assets/site.css">
<script src="{root}assets/theme.js"></script>
</head>
<body class="{kind}">
<a class="skip" href="#main">Skip to the content</a>
<header class="top"><div class="wrap">
<a class="brand" href="{root}index.html"><b>the ultimate insider</b><small>presentation.sgit.ai</small></a>
<nav class="main" aria-label="Site">{nav}</nav>
<button class="theme" type="button" aria-label="Switch between light and dark">theme</button>
</div></header>
<main id="main">
{body}
</main>
<footer class="foot"><div class="wrap">
<p><b>{name}</b> · <a href="{root}admin/versions.html" class="ver">site {self.version}</a> · version numbered by CI, never by hand</p>
<p>Part of the <a href="https://sgit.ai/">sgit.ai</a> network · written with the agents of <a href="https://newsroom.sgit.ai/">the SGit Newsroom</a> · <a href="{self.config['repo']}">source</a> · <a href="{md}">this page as markdown</a> · <a href="{root}llms.txt">llms.txt</a> · <a href="{root}about/index.html">about and disclosure</a></p>
<p>Text CC BY 4.0, code Apache-2.0. © 2026 Dinis Cruz.</p>
</div></footer>
</body>
</html>
'''

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
        if listed:
            self.pages.append((rel, title, description))

    def copy_static(self):
        for path in sorted((SRC / 'static').rglob('*')):
            if path.is_dir():
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

    def build_versions(self):                                       # counted from git, never typed
        try:
            log = subprocess.run(['git', 'log', '--format=%cs%x09%s'], cwd=ROOT, capture_output=True, text=True, check=True).stdout
        except (OSError, subprocess.CalledProcessError):
            log = ''
        rows = []
        for line in log.splitlines():
            date, _, subject = line.partition('\t')
            m = re.match(r'site (v\d+\.\d+\.\d+): (.*)', subject)
            if m:
                rows.append((m.group(1), date, m.group(2)))
        if rows:
            table = ''.join(f'<tr><td><code>{v}</code></td><td>{d}</td><td>{html.escape(s)}</td></tr>' for v, d, s in rows)
            table = f'<div class="tbl"><table><thead><tr><th>Release</th><th>Date</th><th>What changed</th></tr></thead><tbody>{table}</tbody></table></div>'
        else:
            table = '<p class="note">No release yet. The first push to <code>dev</code> is numbered by CI as v0.1.0.</p>'
        body = (f'<section class="wrap narrow"><p class="kicker">Admin</p><h1>Releases</h1>'
                f'<p class="lead">This build is <b>site {self.version}</b>. {len(rows)} releases so far, read from the release commits CI made, newest first.</p>'
                f'<p>Nobody but CI writes the version. A push to <code>dev</code> bumps the last number and a push to <code>main</code> the middle one; '
                f'the release job tags its own commit and deploys that commit, never the pushed one. The scheme and its history are in '
                f'<a href="https://newsroom.sgit.ai/articles/ci-owns-the-version.html">CI owns the version</a>.</p>{table}</section>')
        self.page('admin/versions.html', 'Releases', f'Every release of this site, numbered by CI. This build is site {self.version}.', body)

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
        self.build_articles()
        self.build_script()
        self.build_brief()
        self.build_versions()
        self.build_indexes()
        print(f'built {len(self.pages)} pages at site {self.version} into {OUT.relative_to(ROOT)}/')


if __name__ == '__main__':
    args    = sys.argv[1:]
    version = args[args.index('--version') + 1] if '--version' in args else None
    if version is None:
        vfile   = ROOT / 'version'
        version = vfile.read_text().strip() if vfile.exists() else PENDING
    Site_Build(version).build()
