# The five-step wake, recorded: every wake leaves one record, team/<you>/wakes/<started>.json, with five steps.
#
#   python3 admin/tools/wake.py open  <you> --kind "<what this wake is>"            starts the record (start.py calls it)
#   python3 admin/tools/wake.py step  <you> plan        --by conductor --model sonnet --verdict go|stop --comment "<the plan: 1-3 items>"
#   python3 admin/tools/wake.py step  <you> pre_review  --by security  --model sonnet --verdict go|change|stop --comment "..."
#   python3 admin/tools/wake.py gate  <you>                                         exit 0 only if plan and pre_review both say go
#   python3 admin/tools/wake.py step  <you> work        --by <you>     --model <m>  --verdict done|partial|none --comment "<what changed, commits>"
#   python3 admin/tools/wake.py step  <you> post_review --by security  --model sonnet --verdict clean|finding|stop --comment "..."
#   python3 admin/tools/wake.py step  <you> post_check  --by conductor --model sonnet --verdict as-planned|partial|off-plan --comment "<plan vs actual>"
#   python3 admin/tools/wake.py close <you> --outcome ok|partial|failed|idle|hold    exit 1 if a step is missing
#
# The editor's rule (29 October 2026): every wake runs the conductor and security before and after the work, each as a
# sub-agent with its own comment, so a mistake, a steered message or one member's problem does not spread to another
# member. It is defence in depth inside one session, not a separate identity: the reviewers have the same reach, so
# they are given the plan, the diff and the rules, never the raw messages. A verdict of `stop` from any step writes
# team/<you>/HOLD.md, which stops every member's wake (start.py) until the editor lifts it. Apache-2.0.

import argparse
import datetime
import json
import sys
from pathlib import Path

ROOT  = Path(__file__).resolve().parents[2]
STEPS = {'plan':        ('conductor', {'go', 'stop'}),
         'pre_review':  ('security',  {'go', 'change', 'stop'}),
         'work':        (None,        {'done', 'partial', 'none'}),
         'post_review': ('security',  {'clean', 'finding', 'stop'}),
         'post_check':  ('conductor', {'as-planned', 'partial', 'off-plan', 'stop'})}


def now():
    return datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def folder(agent):
    return ROOT / 'team' / agent / 'wakes'


def current(agent):                                                 # the newest record that is not closed
    for path in sorted(folder(agent).glob('*.json'), reverse=True):
        rec = json.loads(path.read_text())
        if not rec.get('closed'):
            return path, rec
    sys.exit(f'wake: no open wake record for {agent}: run `wake.py open {agent}` (start.py does)')


def save(path, rec):
    path.write_text(json.dumps(rec, indent=1) + '\n')


def hold(agent, step, comment):
    path = ROOT / 'team' / agent / 'HOLD.md'
    path.write_text(f'# HOLD: {step} said stop in a wake of {agent}\n\nWhen: {now()}\nStep: {step}\nWhy: {comment}\n\n'
                    f'Lifted only by the editor: delete this file and re-enable the paused tasks (team/conductor/WAKE.md, Stopping).\n')
    print(f'wake: {step} said stop: wrote {path.relative_to(ROOT)}; commit it and push it to dev now, then pause your task')


def main():
    p = argparse.ArgumentParser(description='the five-step wake record')
    p.add_argument('action', choices=('open', 'step', 'gate', 'close'))
    p.add_argument('agent')
    p.add_argument('step', nargs='?', choices=list(STEPS))
    p.add_argument('--kind', default='wake')
    p.add_argument('--by')
    p.add_argument('--model')
    p.add_argument('--verdict')
    p.add_argument('--comment', default='')
    p.add_argument('--outcome', choices=('ok', 'partial', 'failed', 'idle', 'hold'))
    a = p.parse_args()

    if a.action == 'open':
        folder(a.agent).mkdir(parents=True, exist_ok=True)
        started = now()
        path    = folder(a.agent) / (started.replace(':', '').replace('-', '') + '.json')
        save(path, {'schema': 'the-ultimate-insider/wake/v1', 'agent': a.agent, 'kind': a.kind, 'started': started,
                    'steps': {}, 'closed': None, 'outcome': None})
        print(path.relative_to(ROOT))
        return

    path, rec = current(a.agent)
    if a.action == 'step':
        if not a.step or not a.verdict or not a.comment.strip():
            sys.exit('wake: a step needs its name, --verdict and a --comment')
        by, allowed = STEPS[a.step]
        if a.verdict not in allowed:
            sys.exit(f'wake: {a.step} takes {", ".join(sorted(allowed))}, not {a.verdict}')
        if a.step in ('work', 'post_review', 'post_check') and not gate_ok(rec):
            sys.exit(f'wake: {a.step} before the plan and the pre-review both said go: refused')
        rec['steps'][a.step] = {'by': a.by or by or a.agent, 'model': a.model or '', 'verdict': a.verdict, 'comment': a.comment.strip(), 'at': now()}
        save(path, rec)
        print(f'wake: {a.step} recorded ({a.verdict}) in {path.relative_to(ROOT)}')
        if a.verdict == 'stop':
            hold(a.agent, a.step, a.comment.strip())
            sys.exit(3)
    elif a.action == 'gate':
        if gate_ok(rec):
            print('wake: plan and pre-review both say go: do the work')
            return
        sys.exit(f'wake: no go yet (plan: {verdict(rec, "plan")}, pre_review: {verdict(rec, "pre_review")}): do no work')
    elif a.action == 'close':
        missing = [s for s in STEPS if s not in rec['steps']]
        if missing and a.outcome != 'hold':
            sys.exit(f'wake: cannot close, missing {", ".join(missing)}: every wake runs all five steps')
        rec['closed'], rec['outcome'] = now(), a.outcome or 'ok'
        save(path, rec)
        print(f'wake: closed {path.relative_to(ROOT)} ({rec["outcome"]})')


def verdict(rec, step):
    return rec['steps'].get(step, {}).get('verdict', 'missing')


def gate_ok(rec):
    return verdict(rec, 'plan') == 'go' and verdict(rec, 'pre_review') == 'go'


if __name__ == '__main__':
    main()
