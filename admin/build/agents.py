# The team, read from the folders under team/<id>/. Standard library only. Apache-2.0.
#
#   python3 admin/build/agents.py check --agent dev [--base origin/dev]   files changed since base, against dev's scope
#   python3 admin/build/agents.py overlaps                                two members claiming the same file (the gate fails)
#   python3 admin/build/agents.py unowned                                 tracked files no member writes or holds
#
# A scope is a setting, not a boundary: the agent can edit its own policy.json. It catches mistakes, not a steered agent.

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TEAM = ROOT / 'team'


class Team:
    def __init__(self):
        self.members = {}
        for folder in sorted(p for p in TEAM.iterdir() if p.is_dir()) if TEAM.exists() else []:
            policy = folder / 'policy.json'
            if policy.exists():
                self.members[folder.name] = json.loads(policy.read_text())

    def pattern(self, glob):                                         # ** crosses folders, * does not
        rx = re.escape(glob).replace(r'\*\*', '\u0000').replace(r'\*', '[^/]*').replace('\u0000', '.*')
        return re.compile('^' + rx + '$')

    def owns(self, agent, path, kinds=('writes', 'holds')):
        scope = self.members[agent].get('scope', {})
        return any(self.pattern(g).match(path) for kind in kinds for g in scope.get(kind, []))

    def appends(self, agent, path):
        return any(path == a.split(':')[0].split('#')[0].strip() for a in self.members[agent].get('scope', {}).get('appends', []))

    def tracked(self):
        out = subprocess.run(['git', 'ls-files'], cwd=ROOT, capture_output=True, text=True).stdout
        return [f for f in out.splitlines() if f]

    def changed(self, base):
        diff  = subprocess.run(['git', 'diff', '--name-only', f'{base}...HEAD'], cwd=ROOT, capture_output=True, text=True).stdout
        local = subprocess.run(['git', 'status', '--porcelain'], cwd=ROOT, capture_output=True, text=True).stdout
        files = set(diff.split()) | {line[3:].split(' -> ')[-1] for line in local.splitlines()}
        return sorted(f for f in files if f and f != 'version')

    def check(self, agent, base):
        if agent not in self.members:
            sys.exit(f'no member "{agent}": its folder is team/{agent}/ with a policy.json')
        outside = [f for f in self.changed(base) if not self.owns(agent, f) and not self.appends(agent, f)]
        for f in outside:
            print(f'outside scope: {f}')
        print(f'{agent}: {len(outside)} file(s) outside scope since {base}')
        return len(outside)

    def overlaps(self):
        found = []
        for f in self.tracked():
            owners = [a for a in self.members if self.owns(a, f)]
            if len(owners) > 1:
                found.append(f'{f}: claimed by {", ".join(owners)}')
        return found

    def unowned(self):
        shared = {'BRIEF.md', 'BRIEF-CORRECTIONS.md', 'version'}
        return [f for f in self.tracked() if f not in shared and not any(self.owns(a, f) for a in self.members)]


if __name__ == '__main__':
    args, team = sys.argv[1:], Team()
    cmd  = args[0] if args else ''
    if cmd == 'check':
        agent = args[args.index('--agent') + 1]
        base  = args[args.index('--base') + 1] if '--base' in args else 'origin/dev'
        sys.exit(1 if team.check(agent, base) else 0)
    elif cmd == 'overlaps':
        found = team.overlaps()
        print('\n'.join(found) or 'no overlaps')
        sys.exit(1 if found else 0)
    elif cmd == 'unowned':
        print('\n'.join(team.unowned()) or 'every tracked file has an owner')
    else:
        sys.exit(__doc__ or 'usage: agents.py check --agent <id> [--base <ref>] | overlaps | unowned')
