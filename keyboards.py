from telegram import InlineKeyboardButton, InlineKeyboardMarkup

back_button = InlineKeyboardMarkup([
    [InlineKeyboardButton("🔙 Back", callback_data="back_to_menu")]
])