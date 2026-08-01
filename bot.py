import os
import logging
import threading
from flask import Flask
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from config import BOT_TOKEN
from handlers import (
    start, menu,
    ex, it, us, non, est,
    handle_back
)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

app = Flask(__name__)

@app.route('/')
def home():
    return "Darknet Bot is running!"

@app.route('/health')
def health():
    return "OK", 200

# Запуск бота при старте приложения
def start_bot():
    logging.info("🚀 Запуск Telegram бота...")
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("menu", menu))
    application.add_handler(CommandHandler("ex", ex))
    application.add_handler(CommandHandler("it", it))
    application.add_handler(CommandHandler("us", us))
    application.add_handler(CommandHandler("non", non))
    application.add_handler(CommandHandler("est", est))
    application.add_handler(CallbackQueryHandler(handle_back, pattern="back_to_menu"))

    logging.info("✅ Бот запущен и готов к работе!")
    application.run_polling()

# Запускаем бота в отдельном потоке сразу после импорта
bot_thread = threading.Thread(target=start_bot, daemon=True)
bot_thread.start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)