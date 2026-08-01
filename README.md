# 🕵️ Exitus non est — Darknet Bot

**Exitus non est** is a Telegram bot designed for anonymity, private inquiries, and darknet-style assistance.

> **Translation from Latin:** *"There is no way out."*

---

## 📌 Features

- `/start` — Welcome message
- `/menu` — List of available commands
- `/ex` — General questions (operator will respond)
- `/it` — Legends and myths from the deep web
- `/us` — Support and operator assistance
- `/non` — Product catalog
- `/est` — FAQ

All sections support inline navigation with a **"Back"** button.

---

## 🧩 Commands Overview

| Command | Description |
|---------|-------------|
| `/start` | Greeting |
| `/menu` | Full menu |
| `/ex` | Ask general questions |
| `/it` | Explore legends & myths |
| `/us` | Contact support / operator |
| `/non` | View product catalog |
| `/est` | Frequently Asked Questions |

---

## 🛠️ Tech Stack

- **Python 3.10+**
- **python-telegram-bot** (v20.6)
- **Flask** — for Render web service
- **Gunicorn** — production WSGI server

---

## 🔐 Environment Variables

Create a `.env` file in the root directory:

```env
BOT_TOKEN=your_telegram_bot_token