import yaml
import pathlib
import json
import random
import os
from datetime import datetime, timedelta

DATA = pathlib.Path(__file__).resolve().parent.parent / 'data' / 'events.yaml'
STATE = pathlib.Path(__file__).resolve().parent.parent / 'events_state.json'

class EventManager:
    def __init__(self, path=DATA, state=STATE):
        self.path = pathlib.Path(path)
        self.state_path = pathlib.Path(state)
        if self.path.exists():
            with open(self.path, 'r') as f:
                data = yaml.safe_load(f) or {}
        else:
            data = {}
        self.scenarios = data.get('scenarios', [])

    def list_events(self):
        return list(self.scenarios)

    def current(self, now=None):
        now = now or datetime.utcnow()
        if self.state_path.exists():
            with open(self.state_path) as f:
                state = json.load(f)
            end = datetime.fromisoformat(state['ends_at'])
            if now < end:
                return state['event']
        return None

    def rotate(self, now=None):
        now = now or datetime.utcnow()
        current = self.current(now)
        available = [e for e in self.scenarios if not current or e['id'] != current['id']]
        if not available:
            return None
        event = random.choice(available)
        duration = event.get('duration_h', 24)
        ends_at = now + timedelta(hours=duration)
        state = {'event': event, 'ends_at': ends_at.isoformat()}
        tmp = self.state_path.with_suffix('.tmp')
        with open(tmp, 'w') as f:
            json.dump(state, f)
        os.replace(tmp, self.state_path)
        return event
