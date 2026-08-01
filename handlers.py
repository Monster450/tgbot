from telegram import Update
from telegram.ext import ContextTypes
from texts import *
from keyboards import back_button

user_sections = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(WELCOME)

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(MENU_TEXT)

async def enter_section(update: Update, context: ContextTypes.DEFAULT_TYPE, section_name: str, section_text: str):
    user_id = update.effective_user.id
    user_sections[user_id] = section_name
    await update.message.reply_text(section_text, reply_markup=back_button)

async def handle_back(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    user_sections.pop(user_id, None)
    await query.edit_message_text(MENU_TEXT, reply_markup=None)

async def ex(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await enter_section(update, context, "General Questions", WAITING_OPERATOR)

async def it(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await enter_section(update, context, "Legends & Myths", WAITING_OPERATOR)

async def us(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await enter_section(update, context, "Support", WAITING_OPERATOR)

async def non(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await enter_section(update, context, "Catalog", CATALOG)

async def est(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await enter_section(update, context, "FAQ", FAQ)