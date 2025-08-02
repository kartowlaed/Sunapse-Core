import sys
from pathlib import Path
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'sunapse-bot'))
from core.quests import DailyGenerator

def test_daily_filters_level(tmp_path):
    data = {
        'daily': [
            {'id': 'low', 'requirements': {'min_level': 1}},
            {'id': 'high', 'requirements': {'min_level': 5}}
        ]
    }
    path = tmp_path / 'tasks.yaml'
    with open(path, 'w') as f:
        yaml.safe_dump(data, f)
    gen = DailyGenerator(path)
    player = {'level': 1}
    ids = {q['id'] for q in gen.generate(player)}
    assert 'high' not in ids
    player = {'level': 5}
    ids = {q['id'] for q in gen.generate(player)}
    assert 'high' in ids
