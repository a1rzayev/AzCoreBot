from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from config.languages import LANGUAGES, SUPPORTED_LANGS
from i18n import t


def build_keyboard(buttons: list[str]) -> InlineKeyboardMarkup:
    """Legacy builder: one button per row, callback_data == label text."""
    keyboard = [[InlineKeyboardButton(btn, callback_data=btn)] for btn in buttons]
    return InlineKeyboardMarkup(keyboard)


def language_keyboard(current_lang: str) -> InlineKeyboardMarkup:
    """One button per supported language, 2 per row.

    The currently active language is prefixed with ✓.
    callback_data format: "set_lang:<code>"
    """
    buttons = []
    for code, info in LANGUAGES.items():
        prefix = "✓ " if code == current_lang else ""
        label = f"{prefix}{info['flag']} {info['name']}"
        buttons.append(InlineKeyboardButton(label, callback_data=f"set_lang:{code}"))

    cols = 1 if len(SUPPORTED_LANGS) <= 2 else 2
    rows = [buttons[i : i + cols] for i in range(0, len(buttons), cols)]
    return InlineKeyboardMarkup(rows)


def main_menu_keyboard(lang: str) -> InlineKeyboardMarkup:
    """Main menu with Help and Change language buttons, labels from locale."""
    rows = [
        [InlineKeyboardButton(t(lang, "help"), callback_data="menu_help")],
        [InlineKeyboardButton(t(lang, "choose_language"), callback_data="menu_language")],
    ]
    return InlineKeyboardMarkup(rows)


def back_keyboard(lang: str) -> InlineKeyboardMarkup:
    """Single-button keyboard: ← Back → back_main."""
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton(t(lang, "back"), callback_data="back_main")]]
    )
