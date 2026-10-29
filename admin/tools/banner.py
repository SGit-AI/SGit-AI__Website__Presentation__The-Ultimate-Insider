# Start and end banners for an agent's session report, so the editor can see where each one begins and ends.
#
#   python3 admin/tools/banner.py start <agent> --kind "<what this session is>" --objective "<what it is for>" \
#       [--started <ISO UTC>] [--scheduled HH:MM] [--model <model>]
#   python3 admin/tools/banner.py end <agent> --started <ISO UTC> [--outcome ok|partial|failed] [--release <commit>] \
#       [--problems "<n found, n fixed>"] [--achieved "a|b"] [--blockers "a|b"] [--for-you "a|b"] [--next "<next run>"]
#
# The shape is the PHP newsroom's (records/briefs/2026-10-27__brief__wake-banners.md in its team repository): a double
# frame and >>> to start, a solid block and <<< to end, then a rounded box for blockers and a heavy box for what waits on
# the editor. Inner width 68, so it reads inside a code block on a phone. Standard library only. Apache-2.0.

import argparse
import datetime
import subprocess
import textwrap
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[2]
W    = 68


def box(rows, top, side, bottom):
    lines = [top]
    for row in rows:
        lines.append(f'{side} {row[:W].ljust(W)} {side}')
    lines.append(bottom)
    return '\n'.join(lines)


def items(label, text, none):
    pad   = ' ' * (len(label) + 2)
    parts = [p.strip() for p in (text or '').split('|') if p.strip()]
    if not parts:
        return [f'{label}  {none}']
    rows = []
    for n, part in enumerate(parts, 1):
        lead    = f'{n}. ' if len(parts) > 1 else ''
        wrapped = textwrap.wrap(lead + part, W - len(pad)) or ['']
        rows   += [(f'{label}  ' if not rows else pad) + wrapped[0]] + [pad + ' ' * len(lead) + w for w in wrapped[1:]]
    return rows


def head():
    try:
        return subprocess.run(['git', 'rev-parse', '--short=12', 'HEAD'], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return '?'


def when(text):
    if not text:
        return datetime.datetime.now(datetime.timezone.utc)
    return datetime.datetime.strptime(text[:19], '%Y-%m-%dT%H:%M:%S').replace(tzinfo=datetime.timezone.utc)


def start(a):
    t    = when(a.started)
    rows = [f'>>> SESSION START   {a.agent}@the-ultimate-insider',
            f'{a.kind}',
            f'{t.strftime("%a %d %b %Y")}   started {t.strftime("%H:%M")} UTC / {t.astimezone(ZoneInfo("Europe/London")).strftime("%H:%M")} London'
            + (f'   due {a.scheduled}' if a.scheduled else ''),
            f'model {a.model or "?"}   repo {head()}']
    rows += items('OBJECTIVE', a.objective, none='not stated')
    return box(rows, '╔' + '═' * (W + 2) + '╗', '║', '╚' + '═' * (W + 2) + '╝')


def end(a):
    t0   = when(a.started)
    now  = datetime.datetime.now(datetime.timezone.utc)
    mins = int((now - t0).total_seconds() // 60)
    rows = [f'<<< SESSION END   {a.agent}@the-ultimate-insider   {a.outcome.upper()}']
    line = f'{t0.strftime("%H:%M")} -> {now.strftime("%H:%M")} UTC  ({mins if mins >= 0 else "?"} min)'
    for part in ([f'released {a.release}'] if a.release else []) + ([f'problems {a.problems}'] if a.problems else []):
        if len(line) + 3 + len(part) > W:                           # a field that does not fit starts its own row, never cut
            rows.append(line)
            line = part
        else:
            line += '   ' + part
    rows.append(line)
    rows += items('ACHIEVED', a.achieved, none='nothing recorded')
    if a.next:
        rows.append(f'NEXT      {a.next}')
    out  = box(rows, '▛' + '▀' * (W + 2) + '▜', '▌', '▙' + '▄' * (W + 2) + '▟')
    out += '\n' + box(items('BLOCKERS', a.blockers, none='none'), '╭' + '─' * (W + 2) + '╮', '│', '╰' + '─' * (W + 2) + '╯')
    out += '\n' + box(items('FOR YOU', a.for_you, none='nothing needed from you'), '┏' + '━' * (W + 2) + '┓', '┃', '┗' + '━' * (W + 2) + '┛')
    return out


def main():
    p = argparse.ArgumentParser(description='start and end banners for an agent session report')
    p.add_argument('which', choices=('start', 'end'))
    p.add_argument('agent')
    p.add_argument('--started')
    p.add_argument('--kind', default='session')
    p.add_argument('--scheduled')
    p.add_argument('--model')
    p.add_argument('--objective')
    p.add_argument('--outcome', default='ok')
    p.add_argument('--release')
    p.add_argument('--problems')
    p.add_argument('--achieved')
    p.add_argument('--blockers')
    p.add_argument('--for-you', dest='for_you')
    p.add_argument('--next')
    a = p.parse_args()
    print('```\n' + (start(a) if a.which == 'start' else end(a)) + '\n```')


if __name__ == '__main__':
    main()
