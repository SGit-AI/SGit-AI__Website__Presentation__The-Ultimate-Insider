# Run before every commit to one of the team's vaults: every file in them is PUBLIC, readable by anyone with the
# published read key, forever (a later commit does not unpublish an earlier one).
#
#   python3 admin/tools/vault_check.py <vault clone> [<vault clone> ...]     exit 0 clean, 1 on any finding
#
# It scans every file in the working copy (not .sg_vault/) with the site gate's leak patterns (private keys, cloud and
# API keys, sgit vault keys), plus sgit_private_ credentials and email addresses (agent addresses such as
# conductor@the-ultimate-insider have no dot after the @ and do not match). A finding names the file and line, never
# the match. Remove what it found before committing; if it was already pushed, stop: team/conductor/WAKE.md, Stopping.
# Apache-2.0.

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'build'))
from validate import Gate                                           # one list of leak patterns for the site and the vaults

EXTRA = [('sgit private credential', re.compile(r'sgit_private_[a-z]+_')),
         ('email address',           re.compile(r'\b[\w.+-]+@[\w-]+(\.[\w-]+)+\b'))]


def scan(vault):
    findings = []
    for path in sorted(Path(vault).rglob('*')):
        if not path.is_file() or '.sg_vault' in path.parts:
            continue
        try:
            lines = path.read_text().splitlines()
        except (UnicodeDecodeError, OSError):
            continue
        for n, line in enumerate(lines, 1):
            for name, pattern in Gate.LEAKS + EXTRA:
                if pattern.search(line):
                    findings.append(f'{path.relative_to(vault)}:{n}: looks like {name}')
    return findings


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit('usage: vault_check.py <vault clone> [...]')
    total = 0
    for vault in sys.argv[1:]:
        found = scan(Path(vault))
        total += len(found)
        print('\n'.join(f'{Path(vault).name}: {f}' for f in found) or f'{Path(vault).name}: clean, and public: every file here is readable by anyone')
    sys.exit(1 if total else 0)
