# Sunapse Core

Minimal skeleton for a Telegram clicker bot. Gameplay content is stored in YAML files under `sunapse-bot/data` so the core logic stays unchanged. Item entries include their material, quality and rarity with lookup tables in `data/materials.yaml`, `data/quality.yaml` and `data/rarity.yaml`.

The entry point is `sunapse-bot/main.py` which uses aiogram. See `docs/TODO.md` for the technical specification of planned features. The main design reference is `docs/MVP_DESIGN.md` (now including the currency spec and risk rules), with extra notes in `docs/MVP_SUPPLEMENT.md`. A full project specification is collected in `docs/SPEC_v0.9.md`.

To configure the bot, copy `.env.example` to `.env` and fill in your Telegram token and admin ID. Player data will be stored in the directory specified by `BASE_DIR`.

