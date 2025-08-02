import json
import os
import uuid
import pathlib

DATA = pathlib.Path(os.getenv('BASE_DIR', '.')) / 'tribes.json'


def _load():
    if DATA.exists():
        with open(DATA) as f:
            return json.load(f)
    return {}


def _save(data):
    tmp = DATA.with_suffix('.tmp')
    with open(tmp, 'w') as f:
        json.dump(data, f, indent=2)
    os.replace(tmp, DATA)


def create(name, owner_uid):
    tribes = _load()
    tid = str(uuid.uuid4())
    tribes[tid] = {'id': tid, 'name': name, 'members': [owner_uid]}
    _save(tribes)
    return tribes[tid]


def invite(tid, uid):
    tribes = _load()
    t = tribes.get(tid)
    if not t:
        return False
    if uid not in t['members']:
        t['members'].append(uid)
        _save(tribes)
    return True


def info(tid):
    tribes = _load()
    return tribes.get(tid)
