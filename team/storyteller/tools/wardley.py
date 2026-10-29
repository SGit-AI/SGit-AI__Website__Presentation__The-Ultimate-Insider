#!/usr/bin/env python3
"""Render a Wardley map from a small JSON file to SVG.

The map file: {"title", "anchor", "components": [{"id", "label", "vis", "evo", "note"?, "move"?}],
"links": [[from, to]], "notes": [{"text", "vis", "evo"}]}. vis is 0 (invisible) to 1 (the user's need),
evo is 0 (genesis) to 1 (commodity); "move" is the evo it is heading to, drawn as a red arrow.
Usage: python3 team/storyteller/tools/wardley.py team/storyteller/maps/<name>.json
"""
import json, sys, html
from pathlib import Path

W, H, L, T, R, B = 960, 620, 70, 60, 30, 70

def xy(vis, evo):
    return L + evo * (W - L - R), T + (1 - vis) * (H - T - B)

def render(m):
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="system-ui, sans-serif" font-size="13">',
           f'<rect width="{W}" height="{H}" fill="#fff"/>',
           f'<text x="{L}" y="30" font-size="18" font-weight="600">{html.escape(m["title"])}</text>']
    for i, stage in enumerate(['Genesis', 'Custom built', 'Product (+rental)', 'Commodity (+utility)']):
        x = L + i / 4 * (W - L - R)
        if i: out.append(f'<line x1="{x}" y1="{T}" x2="{x}" y2="{H-B}" stroke="#bbb" stroke-dasharray="4 4"/>')
        out.append(f'<text x="{x + 8}" y="{H-B+20}" fill="#555">{stage}</text>')
    out.append(f'<line x1="{L}" y1="{H-B}" x2="{W-R}" y2="{H-B}" stroke="#333"/><line x1="{L}" y1="{T}" x2="{L}" y2="{H-B}" stroke="#333"/>')
    out.append(f'<text x="{W/2}" y="{H-20}" text-anchor="middle" fill="#333">Evolution</text>')
    out.append(f'<text transform="translate(22 {H/2}) rotate(-90)" text-anchor="middle" fill="#333">Value chain (visible to invisible)</text>')
    c = {x['id']: x for x in m['components']}
    for a, b in m['links']:
        (x1, y1), (x2, y2) = xy(c[a]['vis'], c[a]['evo']), xy(c[b]['vis'], c[b]['evo'])
        out.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#888"/>')
    out.append('<defs><marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="#c0392b"/></marker></defs>')
    for x in m['components']:
        px, py = xy(x['vis'], x['evo'])
        if 'move' in x:
            mx, _ = xy(x['vis'], x['move'])
            out.append(f'<line x1="{px}" y1="{py}" x2="{mx}" y2="{py}" stroke="#c0392b" stroke-dasharray="5 3" marker-end="url(#arr)"/>')
        fill = '#fdebd0' if x.get('inside') else '#fff'
        out.append(f'<circle cx="{px}" cy="{py}" r="6" fill="{fill}" stroke="#222" stroke-width="1.5"/>')
        right = x['evo'] > 0.72
        out.append(f'<text x="{px - 10 if right else px + 10}" y="{py - 8}"{" text-anchor=\"end\"" if right else ""}>{html.escape(x["label"])}</text>')
    for n in m.get('notes', []):
        px, py = xy(n['vis'], n['evo'])
        out.append(f'<text x="{px}" y="{py}" fill="#c0392b" font-style="italic">{html.escape(n["text"])}</text>')
    out.append('</svg>')
    return '\n'.join(out) + '\n'

if __name__ == '__main__':
    for p in sys.argv[1:]:
        p = Path(p)
        p.with_suffix('.svg').write_text(render(json.loads(p.read_text())))
        print('wrote', p.with_suffix('.svg'))
