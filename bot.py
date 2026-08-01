import os
import threading
import logging
from flask import Flask
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from config import BOT_TOKEN
from handlers import (
    start, menu,
    ex, it, us, non, est,
    handle_back
)

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Flask-сервер для Render (чтобы бот не падал)
app = Flask(__name__)

@app.route('/')
def home():
    return "Darknet Bot is running!"

@app.route('/health')
def health():
    return "OK", 200

def run_bot():
    """Запуск Telegram бота"""
    application = Application.builder().token(BOT_TOKEN).build()

    # Команды
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("menu", menu))
    application.add_handler(CommandHandler("ex", ex))
    application.add_handler(CommandHandler("it", it))
    application.add_handler(CommandHandler("us", us))
    application.add_handler(CommandHandler("non", non))
    application.add_handler(CommandHandler("est", est))

    # Инлайн-кнопка Back
    application.add_handler(CallbackQueryHandler(handle_back, pattern="back_to_menu"))

    logging.info("🚀 Бот запущен и работает...")
    application.run_polling()

if __name__ == "__main__":
    # Запускаем бота в отдельном потоке
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.start()

    # Запускаем Flask-сервер для Render
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)