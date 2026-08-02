import os
import logging
from flask import Flask
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from config import BOT_TOKEN
from handlers import (
    start, menu,
    ex, it, us, non, est,
    handle_back, ban, forward_to_operator,
    handle_operator_action, handle_recall,
    handle_end_session
)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

@app.route('/health')
def health():
    return "OK", 200

# Создаём приложение бота
application = Application.builder().token(BOT_TOKEN).build()

application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("menu", menu))
application.add_handler(CommandHandler("ex", ex))
application.add_handler(CommandHandler("it", it))
application.add_handler(CommandHandler("us", us))
application.add_handler(CommandHandler("non", non))
application.add_handler(CommandHandler("est", est))
application.add_handler(CommandHandler("ban", ban))

application.add_handler(CallbackQueryHandler(handle_back, pattern="back_to_menu"))
application.add_handler(CallbackQueryHandler(handle_operator_action, pattern="^(accept|decline)_"))
application.add_handler(CallbackQueryHandler(handle_recall, pattern="^recall_"))
application.add_handler(CallbackQueryHandler(handle_end_session, pattern="^end_"))

application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, forward_to_operator))

# Запускаем бота при старте приложения
def run_bot():
    logging.info("🚀 Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    # Запускаем бота в фоне
    import threading
    threading.Thread(target=run_bot, daemon=True).start()

    # Запускаем Flask для Render
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)