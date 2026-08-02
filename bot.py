import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
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

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⚠️ Command not recognized. Type /menu for list.")

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
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    logging.info("🚀 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()