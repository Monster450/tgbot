import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден! Проверь .env файл.")

# ТВОЙ РЕЗЕРВНЫЙ АККАУНТ (ОПЕРАТОР)
OWNER_ID = 7227749854  # @JohnnyVanceReserve