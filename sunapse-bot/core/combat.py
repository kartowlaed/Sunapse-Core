import random
import yaml
import pathlib
from .utils import dice

DATA_DIR = pathlib.Path(__file__).resolve().parent.parent / 'data'

with open(DATA_DIR / 'locations.yaml', 'r') as f:
    _locs = yaml.safe_load(f) or {}
    LOCATIONS = {l['id']: l for l in _locs.get('locations', [])}
    ORDER = [l['id'] for l in _locs.get('locations', [])]
    BIOME_INDEX = {lid: idx for idx, lid in enumerate(ORDER)}

with open(DATA_DIR / 'mobs.yaml', 'r') as f:
    _mobs = yaml.safe_load(f) or {}
    COMMON_MOBS = _mobs.get('common_mobs', {})
    UNIQUE_MOBS = {}
    for lid, lst in (_mobs.get('mobs') or {}).items():
        for m in lst or []:
            UNIQUE_MOBS[m['id']] = m

class Mob:
    def __init__(self, mid, name, hp, damage):
        self.id = mid
        self.name = name
        self.hp = hp
        self.damage = damage

    def is_alive(self):
        return self.hp > 0


class Battle:
    def __init__(self, player, mob: Mob):
        self.player = player  # expecting dict with 'hp'
        self.mob = mob

    def turn(self, action):
        """Perform one turn of battle.
        action: 'attack', 'artifact', or 'flee'.
        Returns outcome string: 'ongoing', 'escaped', 'won', or 'lost'.
        """
        if action == 'attack':
            dmg = dice(5, 15)
            self.mob.hp -= dmg
        elif action == 'artifact':
            dmg = dice(10, 25)
            self.mob.hp -= dmg
        elif action == 'flee':
            if random.random() < 0.5:
                return 'escaped'
        else:
            raise ValueError('unknown action')

        if self.mob.is_alive():
            self.player['hp'] -= self.mob.damage
            if self.player['hp'] <= 0:
                return 'lost'
            return 'ongoing'
        return 'won'


def spawn_mob(player):
    """Return a Mob instance according to the player's location."""
    loc_id = player.get('universe', {}).get('location')
    if not loc_id:
        raise ValueError('player has no location')
    loc = LOCATIONS.get(loc_id)
    if not loc:
        raise ValueError(f'unknown location {loc_id}')

    roll = random.randint(1, 100)
    gen_ch = loc.get('generic_chance', 0)

    if roll <= gen_ch * 100:
        mid = random.choice(list(COMMON_MOBS.keys()))
        data = COMMON_MOBS[mid]
        idx = BIOME_INDEX.get(loc_id, 0)
        hp = int(data['hp_base'] * (1 + data.get('scale_hp', 0) * idx))
        dmg = int(data['dmg_base'] * (1 + data.get('scale_dmg', 0) * idx))
        return Mob(mid, data['name'], hp, dmg)

    elif roll <= (gen_ch + 0.10) * 100:
        pool = loc.get('elite_pool') or []
        if pool:
            mid = random.choice(pool)
        else:
            pool = loc.get('unique_pool') or []
            mid = random.choice(pool) if pool else random.choice(list(COMMON_MOBS.keys()))
    else:
        if roll > 97 and loc.get('miniboss'):
            mid = loc['miniboss']
        else:
            pool = loc.get('unique_pool') or []
            mid = random.choice(pool) if pool else random.choice(list(COMMON_MOBS.keys()))

    data = UNIQUE_MOBS.get(mid, {'name': mid, 'hp': 50, 'damage': 5})
    return Mob(mid, data.get('name', mid), data.get('hp', 50), data.get('damage', 5))
