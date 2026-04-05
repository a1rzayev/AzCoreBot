from telegram import Update
from telegram.ext import ContextTypes

from config.languages import DEFAULT_LANGUAGE
from data.templates import TEMPLATES
from i18n import t
from services.session_service import reset_session
from services.user_store import get_user_lang, has_user_lang
from utils.keyboards import build_nav_keyboard, language_keyboard


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    reset_session(user_id)

    if not has_user_lang(user_id):
        # First visit: ask the user to pick a language.
        # Use DEFAULT_LANGUAGE for the prompt itself.
        await update.message.reply_text(
            t(DEFAULT_LANGUAGE, "choose_language"),
            reply_markup=language_keyboard(DEFAULT_LANGUAGE),
        )
    else:
        lang = await get_user_lang(user_id)
        name = update.effective_user.first_name or ""
        await update.message.reply_text(
            t(lang, "welcome", {"name": name}),
            reply_markup=build_nav_keyboard(TEMPLATES["start"]["buttons"], lang),
        )
