# The handover of vaults an agent created: a zip of QR codes the editor stores, and the public read keys for the site.
#
#   python3 admin/tools/vault_handover.py --agent <you> --out <scratchpad dir> <vault dir> [<vault dir> ...]
#
# For each vault folder (an sgit clone made with the vault key) it writes, never printing a key:
#   <name>__vault-key__sealed-to-<fp>.png   the vault key sealed to the vaults manager (pki-agent.mjs seal --from-vault),
#                                           a QR only the vaults manager can open: write access, so it stays out of git
#   <name>__read-key.png                    the read key as a QR: public, read only, safe to publish
#   manifest.json                           names, ids, server, read keys, the sealed links, who sealed what and when
# and zips them as <date>__<agent>__vault-handover.zip. The editor stores the zip and hands it to the vaults manager,
# which opens it with `node pki-agent.mjs open <zip>`. The read-key QR images may be published; the sealed ones never are.
#
# The vaults manager is the known key in team/conductor/known-keys/dc-vault-registry.json, confirmed by the editor on
# 29 October 2026. Sealing passes --unverified because the team does not pin a pki.sgit.ai root (paused, 28 October
# 2026): the fingerprint is trusted because the editor confirmed it, not because the register chains it. Apache-2.0.

import argparse
import datetime
import json
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT     = Path(__file__).resolve().parents[2]
TOOLS    = ROOT / 'admin' / 'tools'
KNOWN    = ROOT / 'team' / 'conductor' / 'known-keys' / 'dc-vault-registry.json'
VAULT_RX = re.compile(r'sgit_private_vault_[A-Za-z0-9]+:[a-z0-9]+')


def run(args, cwd=None):
    r = subprocess.run(args, cwd=cwd, capture_output=True, text=True)
    if r.returncode:
        sys.exit(f'failed: {args[0]} {args[1] if len(args) > 1 else ""} (exit {r.returncode}); nothing printed from it, it may hold a key')
    return r.stdout


def read_key(vault_dir):                                            # derived in this process from the vault key, never printed
    from sgit_ai.crypto.Vault__Crypto import Vault__Crypto
    m = VAULT_RX.search(run(['sgit', 'vault', 'show-key'], cwd=vault_dir))
    if not m:
        sys.exit(f'{vault_dir}: sgit vault show-key gave no vault key: is it a clone made with the vault key?')
    crypto  = Vault__Crypto()
    pw, vid = crypto.parse_vault_key(m.group(0))
    rk      = crypto.derive_keys(pw, vid)['read_key']
    return vid, f'sgit_public_read_{rk.hex() if isinstance(rk, bytes) else rk}:{vid}'


def main():
    p = argparse.ArgumentParser(description='seal and zip the keys of vaults an agent created')
    p.add_argument('vaults', nargs='+')
    p.add_argument('--agent', required=True)
    p.add_argument('--out', required=True, help='a folder outside the repository, such as the session scratchpad')
    p.add_argument('--server', default='https://dev.send.sgraph.ai')
    a = p.parse_args()

    out = Path(a.out).resolve()
    if ROOT in out.parents or out == ROOT:
        sys.exit('refused: --out is inside the repository; sealed vault keys never go in git')
    run(['sha256sum', '-c', str(TOOLS / 'pki-agent.mjs.sha256')], cwd=ROOT)
    known = json.loads(KNOWN.read_text())
    to    = known['signing_fingerprint']
    now   = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    work  = Path(tempfile.mkdtemp(prefix='handover-', dir=out))
    entries = []
    for v in a.vaults:
        vdir    = Path(v).resolve()
        name    = vdir.name
        vid, rk = read_key(vdir)
        sealed  = work / f'{name}__vault-key__sealed-to-{to.split(":")[1]}.png'
        said    = run(['node', str(TOOLS / 'pki-agent.mjs'), 'seal', '--to', to, '--from-vault', str(vdir), '--unverified',
                       '--name', f'vault key: {name} ({vid})', '--qr', str(sealed)])
        link    = next((l.strip() for l in said.splitlines() if l.strip().startswith('https://')), '')
        rk_file = work / f'{name}__read-key.txt'
        rk_file.write_text(rk)
        run(['node', str(TOOLS / 'qr.mjs'), 'text', str(rk_file), str(work / f'{name}__read-key.png')])
        entries.append({'name': name, 'vault_id': vid, 'server': a.server, 'read_key': rk,
                        'vault_key': {'sealed_to': f'{known["label"]} ({to})', 'qr': sealed.name, 'link': link},
                        'read_key_qr': f'{name}__read-key.png'})
        print(f'{name} ({vid}): vault key sealed to {to}; read key QR made')
    manifest = {'made_by': f'{a.agent}@the-ultimate-insider', 'made_at': now, 'vaults': entries,
                'open_with': 'node pki-agent.mjs open <this zip>   (only the vaults manager can open the sealed QR codes)',
                'publish': 'the read keys and their QR images only; never the sealed vault-key images or links'}
    (work / 'manifest.json').write_text(json.dumps(manifest, indent=1) + '\n')
    zpath = out / f'{now[:10]}__{a.agent}__vault-handover.zip'
    with zipfile.ZipFile(zpath, 'w', zipfile.ZIP_DEFLATED) as z:
        for f in sorted(work.iterdir()):
            z.write(f, f.name)
    print(f'zip: {zpath}')
    print(f'read-key QR images (publishable): {work}')


if __name__ == '__main__':
    main()
