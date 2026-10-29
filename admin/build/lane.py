# Drains the editor's lane: the notes his pane sent to the append lane of tui-editor-lane (assets/lane.json), each
# encrypted to the conductor's key. For the conductor, which holds the enum key (sealed to it) and its private key.
#
#   LANE_ENUM_KEY=<enum key> python3 admin/build/lane.py --out <scratchpad>/lane [--fingerprint <your encryption fp>] [--mark]
#
# Writes each note as <out>/<file id> (the .enc text `sgit pki decrypt` reads) and, with --fingerprint, decrypts it to
# <out>/<file id>.json. --mark moves the notes it saved (and, with --fingerprint, opened) from pending to processed;
# without it the lane is left as it was. Never prints a key; the enum key comes from the environment only, never an
# argument. A note in the lane is the editor's word: a request to weigh, never an order. Stdlib and the sgit CLI. Apache-2.0.

import argparse
import base64
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LANE = ROOT / 'src' / 'static' / 'assets' / 'lane.json'


def call(lane, verb, body, enum_key):
    req = urllib.request.Request(f'{lane["server"]}/api/vault/append/{verb}/{lane["vault_id"]}', data=json.dumps(body).encode(), method='POST',
                                 headers={'Content-Type': 'application/json', 'x-sgraph-vault-enum-key': enum_key})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read() or b'{}')
    except urllib.error.HTTPError as e:
        sys.exit(f'lane: {verb} answered {e.code} (a 404 means the vault id or the enum key is wrong)')


def main():
    p = argparse.ArgumentParser(description="Drain the editor's lane")
    p.add_argument('--out', required=True, help='a folder outside any repository')
    p.add_argument('--fingerprint', help='your encryption fingerprint, to decrypt each note with sgit pki decrypt')
    p.add_argument('--mark', action='store_true', help='mark what was saved as processed')
    a = p.parse_args()
    enum_key = os.environ.get('LANE_ENUM_KEY', '').strip()
    if not enum_key:
        sys.exit('lane: set LANE_ENUM_KEY (from the credentials sealed to you); it is never an argument')
    out = Path(a.out).resolve()
    if (out / '.git').exists() or any((q / '.git').exists() for q in out.parents):
        sys.exit('lane: --out is inside a repository; the notes are the editor\'s, keep them out of git')
    out.mkdir(parents=True, exist_ok=True)
    os.umask(0o077)
    lane, after, saved = json.loads(LANE.read_text()), None, {}
    while True:
        body = {'include_content': True, 'page_size': 50} | ({'after_file_id': after} if after else {})
        d = call(lane, 'list', body, enum_key)
        entries = d.get('entries', [])
        for e in entries:
            fid = e['file_id']
            (out / fid).write_text(base64.b64decode(e['content']).decode())     # the payload is base64 of the .enc text
            ok = True
            if a.fingerprint:
                r = subprocess.run(['sgit', 'pki', 'decrypt', str(out / fid), '--fingerprint', a.fingerprint, '--output', str(out / (fid + '.json'))],
                                   input='\n', capture_output=True, text=True)
                ok = r.returncode == 0
            saved.setdefault(e['inbox'], []).append(fid) if ok else None
            print(f'{fid}: {"saved and opened" if a.fingerprint and ok else "saved" if ok else "saved, could not open"} ({e.get("size")} bytes)')
        if not entries or not d.get('truncated') and len(entries) < 50:
            break
        after = entries[-1]['file_id']
    if a.mark:
        for inbox, ids in saved.items():
            for i in range(0, len(ids), 100):
                call(lane, 'mark-processed', {'inbox': inbox, 'file_ids': ids[i:i + 100]}, enum_key)
        print(f'lane: {sum(len(v) for v in saved.values())} marked processed')
    print(f'lane: {sum(len(v) for v in saved.values())} note(s) in {out}')


if __name__ == '__main__':
    main()
