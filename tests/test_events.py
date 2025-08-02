import sys
from pathlib import Path
import yaml
from datetime import datetime

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'sunapse-bot'))
from core.events import EventManager


def test_event_rotate_not_repeat(tmp_path):
    data = {'scenarios': [
        {'id': 'a', 'duration_h': 1},
        {'id': 'b', 'duration_h': 1}
    ]}
    path = tmp_path / 'events.yaml'
    with open(path, 'w') as f:
        yaml.safe_dump(data, f)
    state = tmp_path / 'state.json'
    em = EventManager(path, state)
    first = em.rotate(now=datetime.utcnow())
    second = em.rotate(now=datetime.utcnow())
    assert first['id'] != second['id']
