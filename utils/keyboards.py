from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def build_keyboard(buttons):
    keyboard = []
    for btn in buttons:
        keyboard.append([InlineKeyboardButton(btn, callback_data=btn)])
    return InlineKeyboardMarkup(keyboard)