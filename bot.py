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
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("menu", menu))
    application.add_handler(CommandHandler("ex", ex))
    application.add_handler(CommandHandler("it", it))
    application.add_handler(CommandHandler("us", us))
    application.add_handler(CommandHandler("non", non))
    application.add_handler(CommandHandler("est", est))
    application.add_handler(CallbackQueryHandler(handle_back, pattern="back_to_menu"))

    logging.info("🚀 Бот запущен и работает...")
    application.run_polling()

if __name__ == "__main__":
    main()