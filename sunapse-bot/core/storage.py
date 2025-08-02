import json
import os
import uuid
import datetime
import pathlib

BASE = pathlib.Path(os.getenv('BASE_DIR', '.')) / 'players'
BASE.mkdir(exist_ok=True, parents=True)


def _p(uid):
    return BASE / f"{uid}.json"


def load_player(uid):
    try:
        with open(_p(uid)) as f:
            return json.load(f)
    except FileNotFoundError:
        return None


def save_player(uid, data):
    tmp = _p(uid).with_suffix('.tmp')
    with open(tmp, 'w') as f:
        json.dump(data, f, indent=2)
    os.replace(tmp, _p(uid))


def create_player(uid, name):
    player = {
        'id': uid,
        'name': name,
        'hp': 100,
        'level': 1,
        'mine_level': 0,
        'wallet': {'emeralds': 0, 'rubies': 0, 'ender_eyes': 0},
        'inventory': {},
        'universe': {'location': None},
        'notif_flags': 0,
        'dpass': {'level': 1, 'xp': 0},
        'daily_gift_idx': 0,
        'daily_gift_ts': None,
        'created': datetime.datetime.utcnow().isoformat(),
    }
    save_player(uid, player)
    return player


def list_player_ids():
    return [p.stem for p in BASE.glob('*.json')]
