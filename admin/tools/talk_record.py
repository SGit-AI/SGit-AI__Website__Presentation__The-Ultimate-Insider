#!/usr/bin/env python3
"""The talk as given: what was said, beside the slide it was said over.

    python3 admin/tools/talk_record.py        writes content/articles/the-talk-as-given.md

Reads team/conductor/talk-record/transcript.json (the cleaned record of the talk of 29 October 2026, one passage per
entry: time, who, beat, text) and team/conductor/talk-record/talk-v0.2.0.json (the beats as released in v0.2.0), and
places each beat's passages on the left and its slide on the right (team/conductor/debriefs/img/talk-<beat>.jpg, shot
from the v0.2.0 build). On a phone the slide comes first, then the words. The slides the talk did not reach close the page.
Kept by conductor@the-ultimate-insider, at the editor's word (30 October 2026).
"""
import html, json
from pathlib import Path

ROOT  = Path(__file__).resolve().parents[2]
REC   = ROOT / 'team' / 'conductor' / 'talk-record'
OUT   = ROOT / 'content' / 'articles' / 'the-talk-as-given.md'
IMG   = '../team/conductor/debriefs/img/talk-{}.jpg'
WHO   = {'host': 'The host', 'room': 'From the room'}
PARTS = {1: 'Part one', 2: 'Part two', 3: 'Part three'}

STYLE = """<style>
.tr-row{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.2fr);gap:32px;align-items:start;width:min(1240px,calc(100vw - 32px));margin:0 0 40px calc(50% - min(620px,50vw - 16px));padding-top:20px;border-top:1px solid var(--line,#d9dde3)}
.tr-text p{margin:0 0 .8em}
.tr-pass{margin:0 0 1.2em}
.tr-t{font:600 13px/1.4 ui-monospace,monospace;color:var(--muted,#6b7280);margin:0 0 .3em}
.tr-room{border-left:3px solid var(--accent,#1aa39a);padding-left:12px;font-style:italic}
.tr-fig{margin:0;position:sticky;top:76px}
.tr-fig img{width:100%;height:auto;border-radius:6px;border:1px solid var(--line,#d9dde3);display:block}
.tr-fig figcaption{font-size:14px;line-height:1.4;margin-top:6px;color:var(--muted,#6b7280)}
.tr-part{margin:48px 0 8px}
.tr-left{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:14px;margin:1em 0}
.tr-left figure{margin:0}.tr-left img{width:100%;height:auto;border-radius:6px;border:1px solid var(--line,#d9dde3)}
.tr-left figcaption{font-size:14px;line-height:1.4;margin-top:4px}
@media (max-width:760px){.tr-row{grid-template-columns:1fr;width:auto;margin-left:0}.tr-fig{position:static;order:-1}}
</style>"""


def esc(s):
    return html.escape(s, quote=True)


def slide_href(src):
    return '../' + (src[3:] if src.startswith('../') else 'talk/' + src)


def figure(b, caption_extra=''):
    src = (b.get('slide') or {}).get('src', '')
    cap = f'{PARTS.get(b.get("part"), "")}: <a href="{esc(slide_href(src))}">{esc(b.get("title", b["id"]))}</a>{caption_extra}'
    return (f'<figure class="tr-fig"><img src="{IMG.format(b["id"])}" alt="The slide: {esc(b.get("title", b["id"]))}" loading="lazy">'
            f'<figcaption>{cap}</figcaption></figure>')


def passage(p):
    label = WHO.get(p['who'])
    paras = ''.join(f'<p>{esc(x.strip())}</p>' for x in p['text'].split('\n\n') if x.strip())
    head = f'<p class="tr-t">{esc(p["t"])}{" · " + label if label else ""}</p>'
    return f'<div class="tr-pass{" tr-room" if p["who"] == "room" else ""}">{head}{paras}</div>'


def main():
    beats = json.loads((REC / 'talk-v0.2.0.json').read_text())['beats']
    record = json.loads((REC / 'transcript.json').read_text())
    by_id = {b['id']: b for b in beats}
    order, groups = [], {}
    for p in record:                                            # groups in the order spoken; a beat revisited later joins its group
        if p['beat'] not in groups:
            order.append(p['beat']); groups[p['beat']] = []
        groups[p['beat']].append(p)
    words = sum(len(p['text'].split()) for p in record)
    questions = sum(1 for p in record if p['who'] == 'room')
    reached = set(order)
    rows, part = [], None
    for bid in order:
        b = by_id[bid]
        if b.get('part') != part:
            part = b.get('part')
            rows.append(f'<h2 class="tr-part" id="part-{part}">{PARTS.get(part, "")}</h2>')
        rows.append(f'<section class="tr-row" id="{esc(bid)}"><div class="tr-text">{"".join(passage(p) for p in groups[bid])}</div>{figure(b)}</section>')
    unreached = [b for b in beats if b['id'] not in reached]
    tail = ''
    if unreached:
        tail = ('\n\n## The slides the talk did not reach\n\nThe questions from the room took the time of these, so they were not shown. They are in the deck as released.\n\n'
                '<div class="tr-left">' + ''.join(
                    f'<figure><img src="{IMG.format(b["id"])}" alt="The slide: {esc(b.get("title", b["id"]))}" loading="lazy">'
                    f'<figcaption>{PARTS.get(b.get("part"), "")}: <a href="{esc(slide_href((b.get("slide") or {}).get("src", "")))}">{esc(b.get("title", b["id"]))}</a></figcaption></figure>'
                    for b in unreached) + '</div>')
    front = '\n'.join([
        '---',
        'title: The talk as given',
        'kicker: The talk',
        'date: 2026-10-29',
        'author: conductor@the-ultimate-insider, from the recording, generated by admin/tools/talk_record.py',
        f'minutes: {round(words / 230)}',
        'description: The ultimate insider as it was given at hack::soho with IOActive, London, 29 October 2026: what was said, beside the slide it was said over.',
        'abstract: The talk was recorded and transcribed. This is that transcript, cleaned and set beside the slides of the release that was presented (v0.2.0): the words on the left, the slide on the right, in the order they were said, with the questions from the room where they came.',
        '---',
    ])
    intro = (f'\n\nGiven on 29 October 2026 at hack::soho, hosted by IOActive in London, over about 87 minutes. The slides are the talk as released in **v0.2.0**, '
             f'shot from that build; click a caption to open the slide itself. The words come from an automatic transcript of the recording: **{len(record)} passages**, '
             f'about **{words:,} words**, **{questions} of them from the room**, placed on {len(reached)} of the {len(beats)} slides.\n\n'
             'How it was cleaned: swearing, filler, false starts and asides about the room\'s audio are gone; a few remarks that disparaged people or companies were removed or made neutral; '
             'names that the transcription got wrong are corrected (SGit, SHarness, ruv.sgit, IOActive and others); the people in the room are anonymous. '
             'Nothing was added: every argument and claim is the speaker\'s own. Where the slide a passage belongs to was a judgement call, the passage sits with the slide on screen when it was said.\n\n')
    OUT.write_text(front + intro + STYLE + '\n\n' + '\n'.join(rows) + tail + '\n')
    print(f'wrote {OUT.relative_to(ROOT)}: {len(record)} passages, {len(reached)} slides reached, {len(unreached)} not, {words} words')


if __name__ == '__main__':
    main()
