from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from core import storage, shop, tribes, utils
import yaml
import os
import pathlib

bot = Bot(os.getenv('TOKEN'), parse_mode='HTML')
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start(m: types.Message):
    uid = str(m.from_user.id)
    player = storage.load_player(uid) or storage.create_player(uid, m.from_user.first_name)
    await m.answer(f"Привет, {player['name']}! /menu пока пустой скелет.")


@dp.message_handler(commands=['shop'])
async def cmd_shop(m: types.Message):
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton('\ud83c\udf81 Daily Gift', callback_data='daily_gift'))
    await m.answer("\ud83d\udd38 Команда: /buy <item_id> <qty=1>\nПример: /buy wood_sword 1", reply_markup=kb)


@dp.message_handler(commands=['buy'])
async def cmd_buy(m: types.Message):
    try:
        _, item_id, *qty = m.text.split()
        qty = int(qty[0]) if qty else 1
    except ValueError:
        return await m.reply('Формат: /buy item_id qty')
    uid = str(m.from_user.id)
    player = storage.load_player(uid)
    ok, msg = shop.buy(player, item_id, qty)
    await m.answer(msg)


@dp.callback_query_handler(lambda c: c.data == 'daily_gift')
async def cb_daily_gift(c: types.CallbackQuery):
    uid = str(c.from_user.id)
    player = storage.load_player(uid)
    ok, msg = shop.daily_gift(player)
    await c.answer()
    await c.message.answer(msg)


@dp.message_handler(commands=['profile'])
async def cmd_profile(m: types.Message):
    uid = str(m.from_user.id)
    player = storage.load_player(uid)
    dp = player.get('dpass', {'level': 1, 'xp': 0})
    needed = int(100 * dp['level'] ** 1.15)
    bar = utils.render_bar(dp['xp'], needed, 10, '🟧', '⬜')
    next_reward = dp.get('next_reward', '?')
    text = (
        f"😎 {player['name']}\n"
        f"🏆 Dungeons PASS: {dp['level']}/30 ({dp['xp']}/{needed})\n"
        f"{bar}\n"
        f"Next reward → {next_reward}"
    )
    await m.answer(text)


@dp.message_handler(commands=['tribe'])
async def cmd_tribe(m: types.Message):
    parts = m.text.split()
    uid = str(m.from_user.id)
    player = storage.load_player(uid)
    if len(parts) < 2:
        await m.answer('/tribe create <name> | invite <tribe_id> <uid> | info <tribe_id>')
        return
    action = parts[1]
    if action == 'create' and len(parts) >= 3:
        name = ' '.join(parts[2:])
        t = tribes.create(name, uid)
        player['tribe'] = t['id']
        storage.save_player(uid, player)
        await m.answer(f"Создан клан {t['name']} ({t['id']})")
    elif action == 'invite' and len(parts) >= 4:
        tribe_id, target = parts[2], parts[3]
        ok = tribes.invite(tribe_id, target)
        await m.answer('Приглашён' if ok else 'Ошибка')
    elif action == 'info' and len(parts) >= 3:
        t = tribes.info(parts[2])
        if t:
            await m.answer(f"{t['name']}: {', '.join(t['members'])}")
        else:
            await m.answer('Нет клана')
    else:
        await m.answer('Неизвестная команда')


DATA_DIR = pathlib.Path(__file__).resolve().parent / 'data'
NOTIF_FLAGS = yaml.safe_load(open(DATA_DIR / 'notif_flags.yaml'))['flags']


@dp.message_handler(commands=['notify'])
async def cmd_notify(m: types.Message):
    uid = str(m.from_user.id)
    player = storage.load_player(uid)
    parts = m.text.split()
    flags_val = player.get('notif_flags', 0)
    if len(parts) == 1:
        lines = []
        for name, bit in NOTIF_FLAGS.items():
            enabled = bool(flags_val & bit)
            lines.append(f"{'✅' if enabled else '❌'} {name} (/notify {name})")
        await m.answer('\n'.join(lines))
    else:
        flag = parts[1]
        bit = NOTIF_FLAGS.get(flag)
        if not bit:
            await m.answer('Неизвестный флаг')
            return
        flags_val ^= bit
        player['notif_flags'] = flags_val
        storage.save_player(uid, player)
        await m.answer('Переключено')


if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp)
