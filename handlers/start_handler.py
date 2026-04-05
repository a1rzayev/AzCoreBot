from telegram import Update
from telegram.ext import ContextTypes

from i18n import t
from services.session_service import reset_session
from services.user_store import get_user_lang
from utils.keyboards import main_menu_keyboard


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    reset_session(user_id)

    lang = await get_user_lang(user_id)
    name = update.effective_user.first_name or ""

    await update.message.reply_text(
        t(lang, "welcome", {"name": name}),
        reply_markup=main_menu_keyboard(lang),
    )
