"""Route all callback_query updates.

Callbacks handled here:
  set_lang:<code>  – save language, show start menu in new lang
  settings         – show language picker (alias for menu_language)
  back_main        – show start menu in current lang
  menu_language    – show language picker
  menu_help        – show help text with Back button

nav:* and svc:* are delegated to navigation_handler.
Anything else is answered silently.
"""
from telegram import Update
from telegram.ext import ContextTypes

from config.languages import SUPPORTED_LANGS
from data.templates import TEMPLATES
from i18n import t
from services.session_service import get_session
from services.user_store import get_user_lang, set_user_lang
from utils.keyboards import back_keyboard, build_nav_keyboard, language_keyboard


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    data = query.data
    user_id = query.from_user.id

    # --- Language selection ---
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
            reply_markup=build_nav_keyboard(TEMPLATES["start"]["buttons"], lang),
        )

    # --- Settings / language picker ---
    elif data in ("settings", "menu_language"):
        lang = await get_user_lang(user_id)
        await query.answer()
        await query.edit_message_text(
            t(lang, "choose_language"),
            reply_markup=language_keyboard(lang),
        )

    # --- Back to start menu ---
    elif data == "back_main":
        lang = await get_user_lang(user_id)
        name = query.from_user.first_name or ""
        await query.answer()
        await query.edit_message_text(
            t(lang, "welcome", {"name": name}),
            reply_markup=build_nav_keyboard(TEMPLATES["start"]["buttons"], lang),
        )

    # --- Help screen ---
    elif data == "menu_help":
        lang = await get_user_lang(user_id)
        await query.answer()
        await query.edit_message_text(
            t(lang, "help"),
            reply_markup=back_keyboard(lang),
        )

    # --- Leave a comment ---
    elif data == "leave_comment":
        lang = await get_user_lang(user_id)
        session = get_session(user_id)
        session["lead_step"] = "comment"
        await query.answer()
        await query.edit_message_text(t(lang, "leave_comment_prompt"))

    # --- Navigation & service callbacks ---
    elif data.startswith("nav:") or data.startswith("svc:"):
        from handlers.navigation_handler import handle_navigation
        await handle_navigation(update, context)

    # --- Unknown: dismiss spinner silently ---
    else:
        await query.answer()
