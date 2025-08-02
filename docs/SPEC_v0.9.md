# Sunapse G — Dungeons Bot Spec v0.9 (Full Detail)

> **Цель.** Один JSON-ямл-ориентированный репозиторий, который Codex может превратить в рабочий Telegram-бот-кликер сонтом механик, вдохновлённый *Minecraft Dungeons*
>
> **Модульность.** Любая система lives-in-YAML → легко патчить/отключать. Только runtime-ядро в `core/` содержит код.

---

## 0. Дерево проекта

```
sunapse-bot/
├─ core/
│  ├─ __init__.py
│  ├─ storage.py          # read/write sqlite
│  ├─ helpers.py          # bar(), uid(), i18n
│  ├─ combat.py           # turn loop, effects
│  ├─ mine.py             # click‑mine loop
│  ├─ loot.py             # chest roll logic
│  ├─ dungeons_pass.py    # Dungeons PASS XP+rewards
│  ├─ auction.py          # P2P auction (rubies fee)
│  ├─ stats.py            # daily aggregates
│  └─ tutorial.py         # interactive onboarding
├─ data/
│  ├─ materials.yaml      # wood…adamantite
│  ├─ quality.yaml        # потрёпанный…мастерский
│  ├─ rarity.yaml         # common/rare/mythic/chromatic
│  ├─ items.yaml          # weapons, pickaxes, armor, artifacts
│  ├─ drops.yaml          # chests + bosses loot tables
│  ├─ mobs.yaml           # 8 биомов × моб-пулы
│  ├─ chests.yaml         # emoji + colour map for UI
│  ├─ tutorial.yaml       # step → expectation → reward
│  ├─ titles.yaml         # store + premium titles
│  ├─ dungeons_pass.yaml  # 3 первых сезонов PASS
│  └─ config.yaml         # misc constants (auction fee, slots…)
├─ langs/
│  ├─ ru.yml
│  └─ en.yml
├─ tests/                 # pytest
└─ main.py                # aiogram entry‑point
```

---

## 1. UID‑система (предметы)

```
<category>-<material>-<quality>-<rarity>-<serial>
SW-DI-PL-R-7B4E   # полированный редкий Алмазный меч
```

* **category** (`SW`,`PX`,`AX`,`AR`,`AF`) – префикс из `data/category.yaml`.
* **material** (`DI`, `CU`, …) – первые две ASCII-буквы из `materials.yaml`.
* **quality**: `PK`/`NM`/`PL`/`MS` (потрёпанный…мастерский).
* **rarity**: `C/R/M/H` (common/rare/mythic/chromatic).
* **serial**: 4 hex (`secrets.token_hex(2)`).

### Рендер в чате

```
⭐ [Dungeon#] полированный Алмазный меч (30 dmg)
UID: SW-DI-PL-M-7B4E
```

---

## 2. Материалы

```yaml
materials:
  wood:       {tier:0, tag:WO, dmg:10, hp:12}
  stone:      {tier:1, tag:ST, dmg:14, hp:18}
  copper:     {tier:2, tag:CU, dmg:16, hp:24}
  iron:       {tier:3, tag:FE, dmg:18, hp:32}
  steel:      {tier:4, tag:SL, dmg:20, hp:40}
  gold:       {tier:5, tag:AU, dmg:22, hp:36}
  diamond:    {tier:6, tag:DI, dmg:26, hp:48}
  netherite:  {tier:7, tag:NE, dmg:30, hp:60}
  adamantite: {tier:8, tag:AD, dmg:34, hp:72}
```

Материал задаёт базовые статы.

## 3. Качество

```yaml
quality:
  0: {tag:" потрёпанный", dmg_mult:0.95, hp_mult:0.95}
  1: {tag:"",            dmg_mult:1.00, hp_mult:1.00}
  2: {tag:" полированный", dmg_mult:1.07, hp_mult:1.07}
  3: {tag:" мастерский",   dmg_mult:1.15, hp_mult:1.15}
```

## 4. Редкость

```yaml
rarity:
  common: {tag:"",          dmg_mul:1.00, weight:{wooden:0.8, gold:0.6, ender:0.4}}
  rare:   {tag:"редкий",     dmg_mul:1.03, weight:{wooden:0.18, gold:0.25, ender:0.35}}
  mythic: {tag:"мифический", dmg_mul:1.07, weight:{wooden:0.02, gold:0.12, ender:0.20}}
  chromatic:{tag:"хроматический", dmg_mul:1.12, weight:{wooden:0, gold:0.03, ender:0.05}}
```

---

## 5. Оружие / кирки / артефакты

Файл `items.yaml` содержит:

* мечи (`*_sword`), кирки (`*_pickaxe`), спец-оружие.
* 10 артефактов (2 фиксировано chromatic).

Пример артефакта:

```yaml
artifacts:
  wind_horn:
    name: "Рог ветра"
    cooldown: 6
    effect: "knockback_cone"
    rarity: common
```

---

## 6. Лут-система

```yaml
drops.yaml
chests:
  wooden:
    slots:3
    weapon_roll:
      wood_sword:0.05
    pickaxe_roll:
      wood_pickaxe:0.04
  gold:
    slots:4
    rarity_weights:{common:0.6, rare:0.25, mythic:0.12, chromatic:0.03}
    artifact_roll:
      corrupted_beacon:0.02
```

Функция `loot.roll_chest(chest_id)` возвращает dict emeralds/items.

---

## 7. Валюты

| Код      | Emoji | Источник                 | Траты               |
| -------- | ----- | ------------------------ | ------------------- |
| emeralds | 🟢    | клик/бой/сундуки         | магазин / аукцион   |
| rubies   | ♦     | редстоун шахта / сундуки | fee за аукцион      |
| eyes     | 🧡    | донат / редкие ивенты    | премиум DP / титулы |

---

## 8. Аукцион (P2P)

* 3 слота / игрок.
* Лот — цена **только🟢**.
* Плата за выставление: ♦ платёж (224h→1, 48h→2, 72h→3, 96h→5).
* Комиссия 0 %. UID лочится пока лот активен.

---

## 9. Dungeons PASS (DP)

* Сезон → `passes[]` (дата + награды).
* 30 уровней; XP формула: `100 * lvl ** 1.15`.
* Free-трасса Dungeon×, Premium Dungeon# (🧯30).
* UI-бар: оранжевые квадраты 🟧 + стрелка «Next reward».

---

## 10. Streak

* `login_streak` counter.
* Награды: 5d → wooden\_chest, 10d → gold\_chest.
* Сброс если пропуск >24h.

---

## 11. Tutorial (5 шагов)

1. Welcome → 2. Открыть сундук → 3. Шахта → 4. Бой → 5. Магазин / финал. `/tutorial` перезапускает.

---

## 12. Профиль

```
😎 Nikita_228 🌲
🔖 LVL 23 (336/350)
[🟩🟩🟩🟩🟩🟩🟩🟩🟩⬜]
🟢 1240  ♦ 23  🧡 7
🏰 Traibe: CreepersGang
🔥 Стрик: 12д (🎁 gold chest)
⚔️ Мобов: 784
🏆 Dungeons PASS: 7/30 Dungeon#
[🟧🟧🟧🟧⭐🟧🟧⬜⬜⬜]
🎁 Next reward → Gold Chest (LVL 8)
📆 С нами с 01.08.2025 (2 дн.)
👞 Предметов: 46
```

---

## 13. Команды (RU/EN локализованы)

| Команда                  | Что делает             |
| ------------------------ | ---------------------- |
| `/start`                 | язык RU/EN → тутор T0  |
| `/menu`                  | Главное меню           |
| `/profile`               | Показать профиль       |
| `/dp`                    | Панель Dungeons PASS   |
| `/dppremium`             | Купить Dungeon#        |
| `/mine`                  | клик-майнинг           |
| `/battle`                | случайный моб          |
| `/ah` / `/sell` / `/buy` | аукцион                |
| `/tutorial`              | перезапустить обучение |

---

## 14. Админ

* `/adminstats` — онлайн/килы/майн/валюта day‑aggregates.
* `/admin addxp nick1|50` и т. д.
* All privileged routes guarded by `@admin_only`.

---

## 15. Безопасность (quick‑wins)

1. BOT_TOKEN via `.env`.
2. Move JSON ⇒ SQLite WAL.
3. Link whitelist (`https://t.me/` only).
4. Encrypt birthdates.
5. Trim traceback tokens from logs.

---

## 16. Backlog (α‑план)

* PvP‑arena (duel Elo, wagers).
* Enchant/Rune system.
* Gear durability & repair.
* Seasonal world‑events (raid bosses).
* Multi‑language ≥3.
* Cloud deploy (Docker + GH Actions).

---

## 17. Daily‑Quests (60 шт.)

* **6 слотов каждый день.** YAML‑ключ `dailies:` → список из 60 задач.
* При логине бот выбирает 6, фильтруя по `min_level` и `min_mine_level`.
* **Автозачёт.** Как только условие выполнено → награда падает в инвентарь.
* **Категории.** `kill`, `mine`, `open_chest`, `trade_ah`, `earn_emeralds`, `enchant`.
* **Пример `data/daily_tasks.yaml`:**

```yaml
dailies:
  - id: kill_easy
    desc_ru: "Убей 20 зомби"
    desc_en: "Kill 20 zombies"
    type: kill
    mob: zombie
    qty: 20
    min_level: 1
    reward: {emeralds: 25}

  - id: mine_redstone
    desc_ru: "Добыть 40 красного камня"
    type: mine
    block: redstone_ore
    qty: 40
    min_mine_level: 2
    reward: {rubies: 1}

  # … всего 60 …
```

## 18. Weekly Events (15 шт.)

* Файл `data/events.yaml` описывает ротацию. 1–3 события в неделю, воркер выбирает случайно.
* **Типы событий:**

| ID                 | Длительность | Механика                  | Награда          |
| ------------------ | ------------ | ------------------------- | ---------------- |
| `raid_enderman`    | 24h          | world‑boss, dmg‑ranking   | Ender Chest + 🧿 |
| `fiery_forge_rush` | 12h          | Double‑drop в Fiery Forge | 2× rubies        |
| `catch_the_pig`    | 6h           | мини‑игра «поймай свинью» | random artifact  |
| …                  | …            | …                         | …                |

* **YAML‑пример**

```yaml
events:
  - id: raid_enderman
    window_h: 24
    reward: {ender_chest: 1, eyes: 2}
  - id: swamp_mining
    window_h: 12
    reward: {emeralds: 100}
  # 15 total
```

* **HP full.** Во всех ивентах здоровье игрока восстанавливается до max.

## 19. Магазин и Daily‑Gift

* `data/shop.yaml` — разделы: cases, titles, boosts.
* Команда `/shop` ➜ inline‑кнопки.
* **Daily Gift.** Таблица `daily_gift_cycle` (строка из item‑id); бот выдаёт по индексу `day % len(cycle)`.

## 20. Tribes (кланы)

* CRUD: `/tribe create`, `/tribe invite`, `/tribe info`.
* Поля: `id`, `name`, `level`, `xp`, `chat_link` (whitelisted).
* Пассив: +5 % emerald drop / уровень.

## 21. Notification Flags

`notif_flags` bitmask (bot_updates, technical, tribe, server_news, gov_news). `/notify` меню — включ/выключ.

---

### Done — версию зафиксировали: **0.9**.

