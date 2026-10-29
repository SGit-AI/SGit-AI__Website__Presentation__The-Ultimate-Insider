# Writes src/pages/studio/programme.html from src/static/studio/data/programme.json, so the page and the data
# cannot drift. deck@the-ultimate-insider runs it after every change to the programme. Standard library only.
#
#   python3 team/deck/tools/programme.py

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DATA = ROOT / 'src/static/studio/data/programme.json'
PAGE = ROOT / 'src/pages/studio/programme.html'


def e(text):
    return html.escape(text, quote=False)


def card(x, by_id):
    links = []
    if x.get('request'):
        links.append(f'request: <code>{e(x["request"])}</code>')
    if x['status'] in ('review', 'again', 'kept'):
        links.append(f'<a href="{{{{root}}}}ruv-sgit/{x["slug"]}/index.html">the piece</a>')
        links.append(f'<a href="{{{{root}}}}ruv-sgit/{x["slug"]}/explainer.html">its explainer</a>')
        links.append(f'<a href="reviews/{x["id"].lower()}.html">deck\'s review</a>')
    after = ', '.join(f'{a} {e(by_id[a]["title"])}' for a in x.get('after', []))
    needs = ', '.join(x.get('needs_from', [])) or 'nobody'
    return (f'<li class="exp" id="{x["id"].lower()}"><p class="kicker">{x["id"]} · <span class="st {x["status"]}">{e(x["status"])}</span> · order {x["order"]}</p>'
            f'<h3>{e(x["title"])}</h3><p class="q">{e(x["question"])}</p><p>{e(x["idea"])}</p>'
            f'<p class="note"><b>Data.</b> {e("; ".join(x["data"]))}</p>'
            f'<p class="note"><b>Made by</b> {", ".join(x["makers"])} · <b>needs data from</b> {needs}'
            + (f' · <b>after</b> {after}' if after else '') + '</p>'
            + (f'<p class="note">{" · ".join(links)}</p>' if links else '') + '</li>')


def main():
    p     = json.loads(DATA.read_text())
    exps  = p['experiments']
    by_id = {x['id']: x for x in exps}
    queue = sorted(exps, key=lambda x: x['order'])
    rows  = ''.join(f'<tr><td>{x["order"]}</td><td><a href="#{x["id"].lower()}">{x["id"]} {e(x["title"])}</a></td>'
                    f'<td>{"one" if x["part"] == "threat" else "two"}</td><td><span class="st {x["status"]}">{e(x["status"])}</span></td></tr>'
                    for x in queue)
    parts = ''
    for part in p['parts']:
        items = ''.join(card(x, by_id) for x in sorted((x for x in exps if x['part'] == part['id']), key=lambda x: x['order']))
        parts += f'<h2>{e(part["title"])}</h2><ol class="exps">{items}</ol>'
    returns = ''.join(f'<li>{e(r)}</li>' for r in p['each_experiment_returns'])
    statuses = ''.join(f'<li><span class="st {k}">{k}</span> {e(v)}</li>' for k, v in p['statuses'].items())
    body = f'''<!--meta {{"title": "The studio programme", "description": "The experiments the editor asked for: new ways to show what an agent is, how far one reaches, where injected words come from, and how a behaviour policy and a harness contain it. Paced one at a time, reviewed every pass."}} -->
<style>
.exps{{list-style:none;padding:0;margin:14px 0;display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:14px}}
.exp{{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px 18px;box-shadow:var(--shadow)}}
.exp h3{{margin:2px 0 4px}}.exp p{{margin:6px 0}}.exp .q{{font:600 17px Georgia,serif;color:var(--head)}}
.st.idea{{color:var(--dim)}}.st.asked{{color:var(--infra);border-color:var(--infra)}}.st.making{{color:var(--infra);border-color:var(--infra);background:var(--infra-t)}}
.st.again{{color:var(--agent);border-color:var(--agent)}}.st.kept{{color:var(--on-accent);background:var(--accent);border-color:var(--accent)}}
</style>
<section class="wrap studio-top">
<nav class="crumbs" aria-label="Breadcrumb"><a href="{{{{root}}}}index.html">Home</a> / <a href="index.html">Studio</a></nav>
<p class="kicker">The studio · generated from <a href="data/programme.json">programme.json</a> · updated {e(p["updated"])}</p>
<h1>The programme</h1>
<p class="lead">{e(p["vision"])}</p>
<p class="note">These are experiments, not slides. The talk itself is frozen; nothing here changes it until the editor picks what to keep.</p>

<h2>How it runs</h2>
<ol>
<li>deck writes each experiment's question and idea here, and asks the makers for it by request.</li>
<li>The conductor paces the queue: one experiment in flight with each maker at a time, in the order below unless the editor reorders it.</li>
<li>The researcher supplies the data, graded and captured; ruv.sgit makes the piece in a run.</li>
<li>deck reviews every pass and asks for another, or marks it for the editor.</li>
<li>The editor reviews in the morning: keep, change or drop.</li>
</ol>
<h3>Every experiment comes back as</h3>
<ul>{returns}</ul>
<h3>Status words</h3>
<ul class="backlog">{statuses}</ul>

<h2>The queue</h2>
<div class="tbl"><table><thead><tr><th>Order</th><th>Experiment</th><th>Part</th><th>Status</th></tr></thead><tbody>{rows}</tbody></table></div>
{parts}
</section>
'''
    PAGE.write_text(body)
    print(f'wrote {PAGE.relative_to(ROOT)}: {len(exps)} experiments')


if __name__ == '__main__':
    main()
