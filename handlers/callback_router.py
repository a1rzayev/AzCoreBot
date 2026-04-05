"""Route callback_query updates.

i18n callbacks handled here:
  set_lang:<code>  – change language, edit message to main menu in new lang
  back_main        – edit message to main menu in current lang
  menu_language    – edit message to language picker
  menu_help        – edit message to help text with Back button

All other callback_data values are forwarded to the legacy navigation_handler.
"""
from telegram import Update
from telegram.ext import ContextTypes

from config.languages import SUPPORTED_LANGS
from i18n import t
from services.user_store import get_user_lang, set_user_lang
from utils.keyboards import back_keyboard, language_keyboard, main_menu_keyboard


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    data = query.data
    user_id = query.from_user.id

    if data.startswith("set_lang:"):
        code = data.split(":", 1)[1]
        if code not in SUPPORTED_LANGS:
            await query.answer()
            return
        await set_user_lang(user_id, code)
        lang = code
        name = query.from_user.first_name or ""
        await query.answer(t(lang, "language_changed"))
        await query.edit_message_text(
            t(lang, "welcome", {"name": name}),
            reply_markup=main_menu_keyboard(lang),
        )

    elif data == "back_main":
        lang = await get_user_lang(user_id)
        name = query.from_user.first_name or ""
        await query.answer()
        await query.edit_message_text(
            t(lang, "welcome", {"name": name}),
            reply_markup=main_menu_keyboard(lang),
        )

    elif data == "menu_language":
        lang = await get_user_lang(user_id)
        await query.answer()
        await query.edit_message_text(
            t(lang, "choose_language"),
            reply_markup=language_keyboard(lang),
        )

    elif data == "menu_help":
        lang = await get_user_lang(user_id)
        await query.answer()
        await query.edit_message_text(
            t(lang, "help"),
            reply_markup=back_keyboard(lang),
        )

    else:
        # Delegate to the legacy navigation handler for all existing callbacks.
        from handlers.navigation_handler import handle_navigation
        await handle_navigation(update, context)
