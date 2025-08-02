import yaml
import pathlib
import datetime
from . import storage

DATA = pathlib.Path(__file__).resolve().parent.parent / 'data' / 'shop.yaml'
SHOP = yaml.safe_load(open(DATA))['shop']

CONFIG = pathlib.Path(__file__).resolve().parent.parent / 'data' / 'config.yaml'
if CONFIG.exists():
    CONFIG_DATA = yaml.safe_load(open(CONFIG))
    GIFT_CYCLE = CONFIG_DATA.get('daily_gift_cycle', [])
else:
    GIFT_CYCLE = []


def buy(player, item_id, qty=1):
    for cat in SHOP.values():
        if item_id in cat:
            spec = cat[item_id]
            if 'price' in spec:
                cur = 'emeralds'
                cost = spec['price']
            elif 'rubies' in spec:
                cur = 'rubies'
                cost = spec['rubies']
            elif 'ender_eyes' in spec:
                cur = 'ender_eyes'
                cost = spec['ender_eyes']
            else:
                return False, 'Нельзя купить'
            total = cost * qty
            if player['wallet'].get(cur, 0) < total:
                return False, f'Не хватает {cur}!'
            player['wallet'][cur] -= total
            inv = player.setdefault('inventory', {})
            inv[item_id] = inv.get(item_id, 0) + qty
            storage.save_player(player['id'], player)
            return True, f'Куплено {qty}× {item_id}'
    return False, 'Нет такого товара.'


def daily_gift(player):
    if not GIFT_CYCLE:
        return False, 'Подарков нет'
    today = datetime.date.today().isoformat()
    if player.get('daily_gift_ts') == today:
        return False, 'Уже получено'
    idx = player.get('daily_gift_idx', 0)
    prize = GIFT_CYCLE[idx % len(GIFT_CYCLE)]
    item, qty = list(prize.items())[0]
    if item == 'emeralds':
        player['wallet']['emeralds'] = player['wallet'].get('emeralds', 0) + qty
    else:
        inv = player.setdefault('inventory', {})
        inv[item] = inv.get(item, 0) + qty
    player['daily_gift_idx'] = idx + 1
    player['daily_gift_ts'] = today
    storage.save_player(player['id'], player)
    return True, f'Подарок: {qty}\u00d7 {item}'
