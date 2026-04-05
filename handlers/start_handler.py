from telegram import Update
from telegram.ext import ContextTypes

from i18n import t
from services.session_service import reset_session
from services.user_store import get_user_lang
from utils.keyboards import language_keyboard


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    reset_session(user_id)

    # Always show the language picker so the user can (re-)choose their language.
    # get_user_lang returns DEFAULT_LANGUAGE for new users, so the picker still
    # marks a sensible default with ✓ while remaining fully selectable.
    lang = await get_user_lang(user_id)
    await update.message.reply_text(
        t(lang, "choose_language"),
        reply_markup=language_keyboard(lang),
    )
