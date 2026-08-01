import logging
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

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu", menu))
    app.add_handler(CommandHandler("ex", ex))
    app.add_handler(CommandHandler("it", it))
    app.add_handler(CommandHandler("us", us))
    app.add_handler(CommandHandler("non", non))
    app.add_handler(CommandHandler("est", est))
    app.add_handler(CallbackQueryHandler(handle_back, pattern="back_to_menu"))

    logging.info("🚀 Бот запущен и работает...")
    app.run_polling()

if __name__ == "__main__":
    main()