import random
import yaml
import pathlib

# daily tasks live in data/daily_tasks.yaml
DATA = pathlib.Path(__file__).resolve().parent.parent / 'data' / 'daily_tasks.yaml'

class DailyGenerator:
    def __init__(self, path=DATA):
        self.path = pathlib.Path(path)
        if self.path.exists():
            with open(self.path, 'r') as f:
                data = yaml.safe_load(f) or {}
        else:
            data = {}
        self.pool = data.get('daily', [])

    def generate(self, player, count=6):
        """Return up to ``count`` quests filtered by player stats."""
        if not self.pool:
            return []
        level = player.get('level', 1)
        mine_level = player.get('mine_level', 0)
        available = []
        for q in self.pool:
            req = q.get('requirements', {})
            if req.get('level_min', 0) > level:
                continue
            if req.get('min_level', 0) > level:  # some specs use min_level
                continue
            if req.get('min_mine_level', 0) > mine_level:
                continue
            available.append(q)
        if len(available) <= count:
            random.shuffle(available)
            return available[:count]
        return random.sample(available, count)
