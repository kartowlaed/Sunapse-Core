import asyncio
import os
from aiogram import Bot
from core import events, storage

async def main():
    em = events.EventManager()
    ev = em.rotate()
    if not ev:
        return
    bot = Bot(os.getenv('TOKEN'), parse_mode='HTML')
    text = f"Новое событие: {ev['name']}"
    for uid in storage.list_player_ids():
        try:
            await bot.send_message(uid, text)
        except Exception:
            pass
    await bot.session.close()

if __name__ == '__main__':
    asyncio.run(main())
