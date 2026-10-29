#!/usr/bin/env python3
# ruv.sgit for The ultimate insider: a Ruflo hive (queen + workers) whose shared memory and output is one sgit vault per run,
# on the SG/Send vault server. Adapted from poc/ruv-sgit/ruvsgit.py in SGit-AI/SGit-AI__Website__Ruv (Apache-2.0).
#
#   setup                          install the pinned tools outside the repository (ruflo into RUVSGIT_HOME/node, sgit-ai with pip)
#   open    RUN SPEC [--vault-key-file F]   F: a pass on a kept vault (its key opened from the sealed handover); else
#                                  a new vault. hive: init, one specialist per worker, one task per worker, the brief broadcast;
#                                  vault: created on the server, the spec and the request committed and pushed
#   deliver RUN WORKER ROLE SRC    a worker's output onto its own vault branch w-<worker>, pushed, merged into `current`, pushed
#   close   RUN WORKERS.json       measure the vault (history, files, bytes, the encrypted store probed for plaintext, a fresh
#                                  clone compared byte for byte) and write the ledger and the run's evidence
#   seal    RUN                    on the editor's go only: publish the READ key, prove a read-only clone is identical and cannot
#                                  write, then destroy the vault key, so the run's vault can never change again
#   delete  RUN                    the other ending: delete the vault on the server, check a clone with the key now fails
#
# The vault key and the server token live only in RUVSGIT_HOME (mode 0600) and are never printed, logged or committed. Vault keys
# go to sgit on stdin; the token goes as --token, the only way sgit 0.27.0 takes it. Every sgit and ruflo call is timed into the run's evidence. Standard library only.

import hashlib
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone

ROOT     = pathlib.Path(__file__).resolve().parents[3]
HOME     = pathlib.Path(os.environ.get('RUVSGIT_HOME', pathlib.Path.home() / '.ruv-sgit-insider'))
SERVER   = os.environ.get('RUVSGIT_SERVER', 'https://dev.send.sgraph.ai')
VIEWER   = os.environ.get('RUVSGIT_VIEWER', 'https://dev.vault.sgraph.ai/en-gb/')
RUFLO    = os.environ.get('RUVSGIT_RUFLO', str(HOME / 'node/node_modules/.bin/ruflo'))
SGIT     = os.environ.get('RUVSGIT_SGIT', 'sgit')
PINS     = {'ruflo': '3.56.10', 'sgit-ai': '0.27.0'}
RUNS     = ROOT / 'team/ruv-sgit/runs'                               # spec and evidence of every run, in git
LEDGER   = ROOT / 'src/static/ruv-sgit/vaults.json'                  # served, so an infographic can read the runs at load time
now      = lambda: datetime.now(timezone.utc).isoformat(timespec='seconds')


def secret(name, value=None):                                        # read or write a secret file under RUVSGIT_HOME, mode 0600
    path = HOME / name
    if value is not None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(value)
        path.chmod(0o600)
    return path.read_text().strip()


def token():
    return os.environ.get('RUVSGIT_TOKEN') or secret('server.token')


def scrub(text):                                                     # never let a key or a token reach a message
    return re.sub(r'[A-Za-z0-9_-]{30,}(:[a-z0-9]{8})?', '<redacted>', text)


def hashes(root):                                                    # the plaintext tree of a working copy
    return {f.relative_to(root).as_posix(): hashlib.sha256(f.read_bytes()).hexdigest()
            for f in root.rglob('*') if f.is_file() and '.sg_vault' not in f.parts}


def store(root):                                                     # the encrypted store, as the server holds it
    bare = root / '.sg_vault' / 'bare'
    return {f.relative_to(bare).as_posix(): hashlib.sha256(f.read_bytes()).hexdigest()
            for d in ('data', 'refs', 'indexes') if (bare / d).exists() for f in (bare / d).rglob('*') if f.is_file()}


class Run:
    def __init__(self, run):
        self.run   = run
        self.dir   = HOME / 'runs' / run
        self.vault = self.dir / 'vault'
        state      = self.dir / 'state.json'
        self.state = json.loads(state.read_text()) if state.exists() else {'run': run, 'ops': [], 'ruflo': [], 'branches': []}

    def save(self):
        self.dir.mkdir(parents=True, exist_ok=True)
        (self.dir / 'state.json').write_text(json.dumps(self.state, indent=1))

    def sgit(self, op, args, cwd=None, stdin=None, check=True):      # the token goes before the subcommand, as sgit wants it
        t0 = time.time()
        r  = subprocess.run([SGIT, '--token', token(), *args], cwd=cwd or self.vault, input=stdin, capture_output=True, text=True)
        self.state['ops'].append({'op': op, 'ms': round((time.time() - t0) * 1000), 'rc': r.returncode})
        if check and r.returncode:
            raise SystemExit(f'sgit {op} failed (rc {r.returncode}): ' + scrub(r.stderr or r.stdout)[-400:])
        return r

    def ruflo(self, actor, args):
        t0 = time.time()
        r  = subprocess.run([RUFLO, *args], cwd=self.state['hive_dir'], capture_output=True, text=True)
        self.state['ruflo'].append({'seq': len(self.state['ruflo']) + 1, 'actor': actor, 'cmd': ' '.join(args), 'rc': r.returncode,
                                    'ms': round((time.time() - t0) * 1000)})
        return r


def commits(R):                                                     # the vault's history, newest first
    H = json.loads(R.sgit('history', ['history', 'log', '--json', '-n', '200']).stdout or '[]')
    return H.get('commits', H) if isinstance(H, dict) else H


def setup():
    (HOME / 'node').mkdir(parents=True, exist_ok=True)
    HOME.chmod(0o700)
    subprocess.run(['npm', 'install', '--no-audit', '--no-fund', '--prefix', str(HOME / 'node'), f'ruflo@{PINS["ruflo"]}'], check=True)
    subprocess.run([sys.executable, '-m', 'pip', 'install', '-q', f'sgit-ai=={PINS["sgit-ai"]}'], check=True)
    print(subprocess.run([RUFLO, '--version'], capture_output=True, text=True).stdout.strip(), '|',
          subprocess.run([SGIT, '--version'], capture_output=True, text=True).stdout.strip())
    if not (HOME / 'server.token').exists() and not os.environ.get('RUVSGIT_TOKEN'):
        print(f'no server token yet: put the SG/Send access token in {HOME}/server.token (mode 0600) or RUVSGIT_TOKEN')


def open_run(run, spec_path, key_file=None):                       # key_file: a second (or later) pass on a kept vault
    R, spec = Run(run), json.loads(pathlib.Path(spec_path).read_text())
    if R.state.get('created_at'):
        raise SystemExit(f'{run}: already open')
    R.state.update(purpose=spec['purpose'], request=spec.get('request', {}), created_at=now())
    hive = R.dir / f'hive-{int(time.time())}'                        # a fresh folder per run: Ruflo anchors each project's policy
    hive.mkdir(parents=True)                                         # ledger outside it, and refuses a recreated path (its tamper check)
    R.state['hive_dir'] = str(hive)
    R.ruflo('queen', ['hive-mind', 'init', '-t', 'hierarchical-mesh', '-c', 'byzantine', '-m', '12'])
    for w in spec['workers']:
        R.ruflo('queen', ['hive-mind', 'spawn', '-n', '1', '-t', w['role'], '-r', 'specialist', '-p', w['id']])
    for w in spec['workers']:
        R.ruflo('conductor', ['hive-mind', 'task', '-d', f"{w['id']}: {w['task']}", '-p', 'high'])
    R.ruflo('conductor', ['hive-mind', 'broadcast', '-m', f"run {run}: {spec['purpose']}", '-f', 'conductor'])
    R.dir.mkdir(parents=True, exist_ok=True)
    if key_file:                                                     # the key opened from its sealed handover, read from a file, sent on stdin
        key = pathlib.Path(key_file).read_text().strip()
        secret(f'runs/{run}/vault.key', key)
        R.sgit('clone', ['clone', '--base-url', SERVER, '-', str(R.vault)], cwd=R.dir, stdin=key)
        R.state.update(vault_id=key.rsplit(':', 1)[-1], pass_of=key.rsplit(':', 1)[-1],
                       commits_before=len(commits(R)))
        brief = R.vault / 'passes' / run                             # each pass keeps its own brief; earlier passes stay as they were
    else:
        r = R.sgit('create', ['create', '--base-url', SERVER, run], cwd=R.dir)
        key, vid = re.search(r'Vault key:\s*(\S+)', r.stdout), re.search(r'Vault ID:\s*(\S+)', r.stdout)
        if not key:
            raise SystemExit('sgit create printed no vault key; its output changed (not shown: it may hold the key)')
        secret(f'runs/{run}/vault.key', key.group(1))
        (R.dir / run).rename(R.vault)
        R.state['vault_id'] = vid.group(1) if vid else None
        brief = R.vault / 'brief'
    brief.mkdir(parents=True)
    shutil.copy(spec_path, brief / 'spec.json')
    req = spec.get('request', {})
    (brief / 'request.md').write_text(f"# The request that started run {run}\n\nFrom: {req.get('from', '?')}, {req.get('date', '?')}\n\n{req.get('text', '')}\n")
    R.sgit('commit', ['commit', '-m', f"{'pass' if key_file else 'brief'}: run {run}"])
    R.sgit('push', ['push'])
    R.save()
    print(f"run {run} open: vault {R.state['vault_id']} on {SERVER}, {len(spec['workers'])} workers, hive in {hive.name}")


def deliver(run, worker, role, src):
    R, src, branch = Run(run), pathlib.Path(src), f'w-{worker}'
    t0 = time.time()
    R.sgit('branch-new', ['branch', 'new', branch])
    dest = R.vault / 'workers' / worker
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(src, dest) if src.is_dir() else (dest.mkdir(parents=True), shutil.copy(src, dest))
    files = sorted(f for f in dest.rglob('*') if f.is_file())
    R.sgit('commit', ['commit', '-m', f'{role} {worker}: delivered {len(files)} files'])
    R.sgit('push', ['push'])
    write_ms, t1 = round((time.time() - t0) * 1000), time.time()
    R.sgit('branch-switch', ['branch', 'switch', 'current'])
    R.sgit('merge', ['branch', 'merge', branch])
    R.sgit('push', ['push'])
    merge_ms = round((time.time() - t1) * 1000)
    digest   = hashlib.sha256(b''.join(f.read_bytes() for f in files)).hexdigest()[:16]
    R.ruflo(role, ['hive-mind', 'broadcast', '-m', f'delivered {worker} sha256:{digest} files:{len(files)}', '-f', role])   # memory -a set
    R.state['branches'] = [b for b in R.state['branches'] if b['name'] != branch] + [                                          # did not persist
        {'name': branch, 'role': role, 'files': len(files), 'bytes': sum(f.stat().st_size for f in files), 'write_ms': write_ms, 'merge_ms': merge_ms}]
    R.save()
    print(f'{worker}: {len(files)} files on {branch}, merged into current ({write_ms} + {merge_ms} ms)')


def close(run, workers_json):
    R  = Run(run)
    H  = commits(R)
    history = [{'id': str(c.get('commit_id') or c.get('id') or '').replace('obj-cas-imm-', '')[:12], 'message': c.get('message', ''),
                'time': c.get('timestamp_iso')} for c in H]
    plain   = hashes(R.vault)
    files   = [R.vault / p for p in plain]
    probes  = []                                                     # text from the delivered files, looked for in the encrypted store
    for f in files:
        probes += [m.group(0)[:32] for m in re.finditer(rb'[A-Za-z][A-Za-z ,.]{24,}', f.read_bytes())][:8]
    bare  = R.vault / '.sg_vault' / 'bare'
    blob  = b''.join(f.read_bytes() for f in bare.rglob('*') if f.is_file())
    hits  = sum(1 for p in probes if p in blob)
    tmp   = pathlib.Path(tempfile.mkdtemp(prefix='ruvsgit-clone-'))
    t0    = time.time()
    R.sgit('clone', ['clone', '--base-url', SERVER, '-', str(tmp / 'c')], cwd=tmp, stdin=secret(f'runs/{run}/vault.key'))
    clone = {'ms': round((time.time() - t0) * 1000), 'files': len(hashes(tmp / 'c')), 'identical': hashes(tmp / 'c') == plain,
             'store_identical': store(tmp / 'c') == store(R.vault)}
    shutil.rmtree(tmp)
    R.ruflo('queen', ['hive-mind', 'status'])
    R.ruflo('queen', ['daemon', 'stop'])
    st = R.state
    st['closed_at'] = now()
    spec  = RUNS / f'{run}.spec.json'                                 # the repository's copy, where a secret in a request is redacted;
    req   = json.loads(spec.read_text()).get('request', {}) if spec.exists() else {}   # the run's own state may still hold it
    entry = {'run': run, 'purpose': st['purpose'], 'request': req, 'pass_of': st.get('pass_of'), 'commits_before': st.get('commits_before'), 'server': SERVER, 'vault_id': st['vault_id'],
             'created_at': st['created_at'], 'closed_at': st['closed_at'], 'ending': None,
             'hive': {'workers': sum(1 for x in st['ruflo'] if 'hive-mind spawn' in x['cmd'] and x['rc'] == 0),
                      'tasks': sum(1 for x in st['ruflo'] if 'hive-mind task' in x['cmd'] and x['rc'] == 0),
                      'ruflo_calls': len(st['ruflo']), 'ruflo_failed': sum(1 for x in st['ruflo'] if x['rc']), 'ruflo_ms': sum(x['ms'] for x in st['ruflo'])},
             'branches': st['branches'], 'commits': len(history), 'files': len(plain), 'bytes_plain': sum(f.stat().st_size for f in files),
             'files_delivered': sum(b['files'] for b in st['branches']), 'bytes_delivered': sum(b['bytes'] for b in st['branches']),
             'store': {'objects': len(store(R.vault)), 'bytes': len(blob), 'plaintext_hits': hits,
                       'probe': f'{len(probes)} text fragments from the vault\'s files, searched for in every byte of the encrypted store'},
             'clone': clone, 'ops': st['ops'], 'ruflo': st['ruflo'], 'history': history, 'workers': json.loads(pathlib.Path(workers_json).read_text())}
    evidence(entry)
    R.save()
    print(f"closed {run}: {entry['commits']} commits, {entry['files']} files, {entry['bytes_plain']} B; store {entry['store']['objects']} objects, "
          f"plaintext hits {hits} of {len(probes)}; fresh clone identical {clone['identical']} (store {clone['store_identical']}) in {clone['ms']} ms")


def evidence(entry):                                                 # the run's own file, and its row in the ledger
    RUNS.mkdir(parents=True, exist_ok=True)
    (RUNS / f"{entry['run']}.evidence.json").write_text(json.dumps(entry, indent=1) + '\n')
    L = json.loads(LEDGER.read_text()) if LEDGER.exists() else {'vaults': []}
    L.update(schema='the-ultimate-insider/ruv-sgit-ledger/v1', updated=now(), server=SERVER, viewer=VIEWER,
             note='one row per ruv.sgit run, written by team/ruv-sgit/tools/ruvsgit.py; no vault key is ever recorded, a read key only once a run is sealed')
    L['vaults'] = [v for v in L['vaults'] if v['run'] != entry['run']] + [{k: v for k, v in entry.items() if k not in ('ruflo', 'ops')}]
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    LEDGER.write_text(json.dumps(L, indent=1) + '\n')


def ending(run, **fields):
    path = RUNS / f'{run}.evidence.json'
    e    = json.loads(path.read_text())
    e.update(fields)
    evidence(e)


def seal(run):
    R, kf = Run(run), HOME / 'runs' / run / 'vault.key'
    if not R.state.get('closed_at') or not kf.exists():
        raise SystemExit(f'{run}: close it first, or it is already sealed or deleted')
    plain = hashes(R.vault)
    R.sgit('publish', ['publish', '--visibility', 'public', '--yes', '.'])
    pub  = R.vault / '.sg_vault' / 'publish'
    rk   = [p.name for p in pub.iterdir() if re.fullmatch(r'sgit_public_read_[0-9a-f]{64}', p.name)] if pub.exists() else []
    if len(rk) != 1:
        raise SystemExit(f'{run}: publish wrote {len(rk)} read-key files; expected 1. The vault key is kept')
    read_key = f"{rk[0]}:{R.state['vault_id']}"
    tmp = pathlib.Path(tempfile.mkdtemp(prefix='ruvsgit-sealed-'))
    try:
        c = R.sgit('clone-read-only', ['clone', '--base-url', SERVER, '-', str(tmp / 'c')], cwd=tmp, stdin=read_key, check=False)
        same = c.returncode == 0 and hashes(tmp / 'c') == plain
        if c.returncode == 0:
            (tmp / 'c' / 'write-probe.md').write_text('a write after the seal\n')
            w = R.sgit('write-with-read-key', ['commit', '-m', 'write after seal'], cwd=tmp / 'c', check=False).returncode
            p = R.sgit('push-with-read-key', ['push'], cwd=tmp / 'c', check=False).returncode
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    if not same or not (w and p):
        raise SystemExit(f'{run}: the read-only clone was not identical, or it could write. The vault key is kept')
    kf.unlink()
    shutil.rmtree(R.vault, ignore_errors=True)                       # its .sg_vault/local holds the key too
    R.state['sealed_at'] = now()
    R.save()
    ending(run, ending='sealed', sealed_at=R.state['sealed_at'],
           published={'read_key': read_key, 'viewer_url': f'{VIEWER}#{read_key}', 'clone': f'sgit clone {read_key}'},
           seal_check={'clone_read_only_identical': True, 'write_with_read_key': 'refused (commit and push)', 'vault_key_left': kf.exists()})
    print(f'{run}: sealed. read-only clone identical, a write with the read key refused, vault key destroyed')


def delete(run):
    R, kf = Run(run), HOME / 'runs' / run / 'vault.key'
    R.sgit('delete-on-remote', ['vault', 'delete-on-remote', '--base-url', SERVER, '--yes', '--json', '.'])
    tmp = pathlib.Path(tempfile.mkdtemp(prefix='ruvsgit-gone-'))
    r   = R.sgit('clone-after-delete', ['clone', '--base-url', SERVER, '-', str(tmp / 'c')], cwd=tmp, stdin=secret(f'runs/{run}/vault.key'), check=False)
    shutil.rmtree(tmp, ignore_errors=True)
    kf.unlink(missing_ok=True)
    shutil.rmtree(R.vault, ignore_errors=True)
    R.state['deleted_at'] = now()
    R.save()
    ending(run, ending='deleted', deleted_at=R.state['deleted_at'], delete_check={'clone_after_delete': 'failed' if r.returncode else 'SUCCEEDED (not deleted)'})
    print(f"{run}: deleted; a clone with the key afterwards {'failed, as it should' if r.returncode else 'SUCCEEDED: not deleted'}")


if __name__ == '__main__':
    a = sys.argv[1:]
    commands = {'setup': lambda: setup(), 'open': lambda: open_run(a[1], a[2], a[a.index('--vault-key-file') + 1] if '--vault-key-file' in a else None), 'deliver': lambda: deliver(a[1], a[2], a[3], a[4]),
                'close': lambda: close(a[1], a[2]), 'seal': lambda: seal(a[1]), 'delete': lambda: delete(a[1])}
    if not a or a[0] not in commands:
        sys.exit('usage: ruvsgit.py setup | open RUN SPEC [--vault-key-file F] | deliver RUN WORKER ROLE SRC | close RUN WORKERS.json | seal RUN | delete RUN')
    commands[a[0]]()
