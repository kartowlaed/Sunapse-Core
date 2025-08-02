# Sunapse Core: Tech Specification (MVP)

This document summarizes the minimal game skeleton to implement before adding content.

## Core Systems
- Player storage with HP, wallet, inventory and current location
- Locations and sublocations loaded from `data/locations.yaml`
- Battle logic with attack, artifact usage and flee option
- Mining sessions with energy and random mob encounters
- Daily quest generator reading `data/quests.yaml`

## Planned Features
- Chest opening system with wooden, gold and ender chests
- Economy with basic currencies: emeralds, rubies and ender eyes
- Simple auction house and NPC vendor interfaces
- Clan creation and bonuses
- Event framework with global bosses and rewards
- Notification service for daily quests and events
- Leaderboards by player progress
- Player settings for notifications and quiet hours

Content such as mob stats, item lists and quest descriptions will be supplied later via YAML files without changing the core code.

## Initial Locations
- 🌲 Лес Криперов — Лесная шахта
- 🐸 Топкое Болото — Болотоходная шахта
- 🎃 Тыквенные Поля — Поля с тыквами
- 🪨 Краснокаменные Шахты — Краснокаменные разломы
- ⚙️ Пылающая Кузня — Огненные штольни
- 🏜 Храм Пустыни — Песчаный карьер
- 🏰 Залы Хайблока — Катакомбы Хайблока
- 🟪 Обсидиановая Вершина — Эндер-разлом

