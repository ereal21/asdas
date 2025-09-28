
# Aiogram v2 Shop Bot

A minimal shop-style Telegram bot built with **aiogram v2** that keeps every interaction to **a single edited message** after `/start`.
It supports English, Russian, and Lithuanian, a simple user store (SQLite), and a `.env` for configuration.

## Features
- `/start` → language selection (EN / RU / LT)
- Pretty main menu with emojis, showing:
  - Welcome @Username 👋
  - Status: None
  - Bots owned: 0
- Four buttons: **Purchase**, **Config**, **Support**, **Language**
- Optional **Admin Panel** with user lookup and balance management (requires `ADMIN_ID` in `.env`)
- **Purchase** → two options:
  - Template bot (299 EUR)
  - Full‑service bot (999 EUR)
- **Support** → opens your support username in Telegram
- **Language** → change language anytime
- **Config** → shows "feature disabled" message
- Uses **message editing** to keep the chat clean.
- Uses SQLite to remember user language.
- Uses `.env` file for secrets.

## Quickstart

1. **Python 3.10+** recommended.

2. Install deps:
   ```bash
   pip install -r requirements.txt
   ```

3. Copy `.env.example` to `.env` and edit:
   ```bash
   cp .env.example .env
   # then open .env and set BOT_TOKEN, ADMIN_ID and other values
   ```

4. Run the bot:
   ```bash
   python main.py
   ```

## Project structure
```
.
├── main.py
├── config.py
├── database.py
├── keyboards.py
├── texts.py
├── requirements.txt
├── .env.example
└── README.md
```

## Notes
- The bot uses **aiogram v2 style executor** (`from aiogram.utils import executor`).
- This sample does **not** process payments; it only shows purchase options.
- To deploy, run the bot on a server and keep the process alive (e.g., systemd, pm2, Docker).
