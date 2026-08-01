from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# Кнопка Back для возврата в главное меню
back_button = InlineKeyboardMarkup([
    [InlineKeyboardButton("🔙 Back", callback_data="back_to_menu")]
])

# Можно добавить другие кнопки позже, если понадобятся