from telegram import Update
from telegram.ext import ContextTypes

from i18n import t
from services.user_store import get_user_lang
from utils.keyboards import language_keyboard


async def handle_language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    lang = await get_user_lang(user_id)

    await update.message.reply_text(
        t(lang, "choose_language"),
        reply_markup=language_keyboard(lang),
    )
