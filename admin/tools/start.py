# The first command of every session, scheduled or started from the editor's chat: get in sync, then say so.
#
#   python3 admin/tools/start.py <you> --kind "<what this session is>" --objective "<what it is for>" --model <model> \
#       [--vaults <folder holding your vault clones>] [--scheduled HH:MM]
#
# 1. git fetch origin dev, then merge origin/dev into the session's branch (and fast-forward the branch from its own
#    remote first, if it has one). A conflict stops here: the merge is aborted, nothing is changed, and the session
#    resolves it before any other work.
# 2. sgit pull in every vault clone under --vaults (the team's public vaults: tui-issues-public, tui-mail-public).
# 3. The start banner (admin/tools/banner.py), with the commit the session now stands on, so the editor can see the
#    session started in sync. The banner is only printed when the pull succeeded.
#
# Many agents push to this repository every hour; a session that works from a stale copy undoes their work. Apache-2.0.

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def git(*args, check=True):
    r = subprocess.run(['git', *args], cwd=ROOT, capture_output=True, text=True)
    if check and r.returncode:
        sys.exit(f'start: git {" ".join(args)} failed:\n{r.stderr.strip() or r.stdout.strip()}')
    return r


def sync_repo():
    git('fetch', '-q', 'origin', 'dev')
    branch   = git('rev-parse', '--abbrev-ref', 'HEAD').stdout.strip()
    upstream = git('rev-parse', '--abbrev-ref', '--symbolic-full-name', '@{u}', check=False)
    if upstream.returncode == 0:
        git('pull', '-q', '--ff-only', check=False)                  # the branch's own remote, when it has moved
    behind = git('rev-list', '--count', 'HEAD..origin/dev').stdout.strip()
    if behind != '0':
        r = git('merge', '--no-edit', 'origin/dev', check=False)
        if r.returncode:
            git('merge', '--abort', check=False)
            sys.exit(f'start: merging origin/dev into {branch} conflicts. Nothing was changed. Resolve it before any other work:\n'
                     f'  git merge origin/dev   (then fix, build, gate, commit)')
    return branch, behind


def sync_vaults(folder):
    pulled = []
    for vault in sorted(p.parent for p in Path(folder).glob('*/.sg_vault')):
        r = subprocess.run(['sgit', 'pull'], cwd=vault, capture_output=True, text=True)
        if r.returncode:
            sys.exit(f'start: sgit pull failed in {vault.name}; nothing printed from it, as it may hold a key. Fix it before any other work.')
        pulled.append(vault.name)
    return pulled


def main():
    p = argparse.ArgumentParser(description='sync, then print the start banner')
    p.add_argument('agent')
    p.add_argument('--kind', default='session')
    p.add_argument('--objective')
    p.add_argument('--model')
    p.add_argument('--scheduled')
    p.add_argument('--vaults', help='the folder holding your vault clones (outside the repository)')
    a = p.parse_args()

    branch, behind = sync_repo()
    pulled         = sync_vaults(a.vaults) if a.vaults else []
    head           = git('rev-parse', '--short=12', 'HEAD').stdout.strip()
    synced         = f'in sync: {branch} at {head}, {behind} commit(s) from dev merged' + (f'; vaults pulled: {", ".join(pulled)}' if pulled else '; no vaults pulled')
    banner         = [sys.executable, str(ROOT / 'admin' / 'tools' / 'banner.py'), 'start', a.agent, '--kind', a.kind,
                      '--objective', (a.objective or 'not stated') + f' ({synced})']
    for flag, value in (('--model', a.model), ('--scheduled', a.scheduled)):
        if value:
            banner += [flag, value]
    sys.exit(subprocess.run(banner).returncode)


if __name__ == '__main__':
    main()
