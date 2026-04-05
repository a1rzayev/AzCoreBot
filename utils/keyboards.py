from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from config.languages import LANGUAGES, SUPPORTED_LANGS
from i18n import t


def build_nav_keyboard(
    buttons: list[tuple[str, str]], lang: str
) -> InlineKeyboardMarkup | None:
    """Build an InlineKeyboardMarkup from a TEMPLATES button list.

    Each item is (label_key, callback_data).  Returns None when the list is
    empty (e.g. contact / incident states that expect free-text input).
    """
    if not buttons:
        return None
    keyboard = [
        [InlineKeyboardButton(t(lang, label_key), callback_data=data)]
        for label_key, data in buttons
    ]
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


def new_request_keyboard(lang: str) -> InlineKeyboardMarkup:
    """Single button shown after a completed request — goes back to the start menu."""
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton(t(lang, "btn_new_request"), callback_data="nav:start")]]
    )


def back_keyboard(lang: str) -> InlineKeyboardMarkup:
    """Single-button keyboard: ← Back → back_main."""
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton(t(lang, "back"), callback_data="back_main")]]
    )
