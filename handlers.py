from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from texts import *
from keyboards import back_button
from config import OWNER_ID

user_sections = {}
banned_users = set()
operator_sessions = {}  # user_id -> True

async def notify_owner(context: ContextTypes.DEFAULT_TYPE, message: str, reply_markup=None):
    await context.bot.send_message(chat_id=OWNER_ID, text=message, reply_markup=reply_markup)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user.id in banned_users:
        await update.message.reply_text(BANNED_MESSAGE)
        return
    await update.message.reply_text(WELCOME)

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user.id in banned_users:
        await update.message.reply_text(BANNED_MESSAGE)
        return
    await update.message.reply_text(MENU_TEXT)

async def enter_section(update: Update, context: ContextTypes.DEFAULT_TYPE, section_name: str, section_text: str):
    user = update.effective_user
    if user.id in banned_users:
        await update.message.reply_text(BANNED_MESSAGE)
        return

    user_id = user.id
    user_sections[user_id] = section_name

    if section_name != "Support":
        await notify_owner(
            context,
            f"🚪 USER ENTERED SECTION [{section_name}]\n"
            f"👤 @{user.username or 'no_username'} | ID: {user.id} | Name: {user.first_name}"
        )

    await update.message.reply_text(section_text, reply_markup=back_button)

async def handle_back(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user = query.from_user
    user_id = user.id
    section = user_sections.pop(user_id, None)

    if section == "Support":
        operator_sessions.pop(user_id, None)
        await notify_owner(
            context,
            f"❌ USER DISCONNECTED\n"
            f"👤 @{user.username or 'no_username'} | ID: {user.id} | Name: {user.first_name}"
        )
    elif section:
        await notify_owner(
            context,
            f"🚪 USER LEFT SECTION [{section}]\n"
            f"👤 @{user.username or 'no_username'} | ID: {user.id} | Name: {user.first_name}"
        )

    await query.delete_message()

async def ex(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user.id in banned_users:
        await update.message.reply_text(BANNED_MESSAGE)
        return

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ Accept", callback_data=f"accept_{user.id}"),
            InlineKeyboardButton("❌ Decline", callback_data=f"decline_{user.id}")
        ]
    ])

    await notify_owner(
        context,
        f"📩 GENERAL QUESTION (/ex)\n"
        f"👤 @{user.username or 'no_username'} | ID: {user.id} | Name: {user.first_name}\n"
        f"💬 Message: {update.message.text or 'no text'}",
        reply_markup=keyboard
    )

    await enter_section(update, context, "General Questions", WAITING_OPERATOR)

async def it(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user.id in banned_users:
        await update.message.reply_text(BANNED_MESSAGE)
        return

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ Accept", callback_data=f"accept_{user.id}"),
            InlineKeyboardButton("❌ Decline", callback_data=f"decline_{user.id}")
        ]
    ])

    await notify_owner(
        context,
        f"📩 LEGENDS & MYTHS (/it)\n"
        f"👤 @{user.username or 'no_username'} | ID: {user.id} | Name: {user.first_name}\n"
        f"💬 Message: {update.message.text or 'no text'}",
        reply_markup=keyboard
    )

    await enter_section(update, context, "Legends & Myths", WAITING_OPERATOR)

async def us(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user.id in banned_users:
        await update.message.reply_text(BANNED_MESSAGE)
        await notify_owner(
            context,
            f"📩 OPERATOR CALL (BANNED USER)\n"
            f"👤 @{user.username or 'no_username'} | ID: {user.id} | Name: {user.first_name}"
        )
        return

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ Accept", callback_data=f"accept_{user.id}"),
            InlineKeyboardButton("❌ Decline", callback_data=f"decline_{user.id}")
        ]
    ])

    await notify_owner(
        context,
        f"📩 OPERATOR CALL\n"
        f"👤 @{user.username or 'no_username'} | ID: {user.id} | Name: {user.first_name}",
        reply_markup=keyboard
    )

    operator_sessions[user.id] = False
    await enter_section(update, context, "Support", WAITING_OPERATOR)

async def non(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await enter_section(update, context, "Catalog", CATALOG)

async def est(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await enter_section(update, context, "FAQ", FAQ)

async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user.id != OWNER_ID:
        await update.message.reply_text("⛔ You don't have permission.")
        return

    try:
        target_id = int(context.args[0])
        banned_users.add(target_id)
        await update.message.reply_text(f"✅ User {target_id} banned.")
    except:
        await update.message.reply_text("❌ Use: /ban ID")

async def handle_operator_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data
    action, user_id_str = data.split('_')
    user_id = int(user_id_str)
    user = await context.bot.get_chat(user_id)

    if action == "accept":
        operator_sessions[user_id] = True
        await context.bot.send_message(
            chat_id=user_id,
            text="✅ Operator found. You can now communicate."
        )
        await query.edit_message_text(
            text=query.message.text + "\n\n✅ **ACCEPTED**",
            parse_mode="Markdown"
        )
    elif action == "decline":
        operator_sessions[user_id] = False
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔄 Call again", callback_data=f"recall_{user_id}")]
        ])
        await context.bot.send_message(
            chat_id=user_id,
            text="❌ Operator declined your request.",
            reply_markup=keyboard
        )
        await query.edit_message_text(
            text=query.message.text + "\n\n❌ **DECLINED**",
            parse_mode="Markdown"
        )

async def handle_recall(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data
    _, user_id_str = data.split('_')
    user_id = int(user_id_str)
    user = await context.bot.get_chat(user_id)

    await query.delete_message()

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ Accept", callback_data=f"accept_{user_id}"),
            InlineKeyboardButton("❌ Decline", callback_data=f"decline_{user_id}")
        ]
    ])

    await notify_owner(
        context,
        f"📩 OPERATOR CALL (RECALL)\n"
        f"👤 @{user.username or 'no_username'} | ID: {user.id} | Name: {user.first_name}",
        reply_markup=keyboard
    )

    await context.bot.send_message(
        chat_id=user_id,
        text="⏳ Operator is being notified again. Please wait."
    )

async def handle_end_session(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data
    _, user_id_str = data.split('_')
    user_id = int(user_id_str)

    await query.delete_message()

    await notify_owner(
        context,
        f"✅ Session ended for user ID: {user_id}"
    )

    try:
        await context.bot.send_message(
            chat_id=user_id,
            text="⛔ The operator has ended the session. You have been returned to the main menu."
        )
    except:
        pass

    operator_sessions.pop(user_id, None)
    user_sections.pop(user_id, None)

async def forward_to_operator(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    if update.message.reply_to_message:
        for uid, active in operator_sessions.items():
            if active:
                try:
                    await context.bot.send_message(
                        chat_id=uid,
                        text=update.message.text
                    )
                    return
                except:
                    pass

    if operator_sessions.get(user.id, False):
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("END SESSION💢", callback_data=f"end_{user.id}")]
        ])

        await notify_owner(
            context,
            f"💬 {update.message.text}\n\n\n\n"
            f"👤 @{user.username or 'no_username'} | ID: {user.id} | Name: {user.first_name}",
            reply_markup=keyboard
        )
        return

    await update.message.reply_text("⚠️ Command not recognized. Type /menu.")