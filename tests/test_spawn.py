import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'sunapse-bot'))
from core import combat


def test_spawn_generic():
    player = {'universe': {'location': 'forest'}, 'hp': 100}
    seen = set()
    for _ in range(100):
        mob = combat.spawn_mob(player)
        seen.add(mob.id)
    assert any(mid in combat.COMMON_MOBS for mid in seen)
