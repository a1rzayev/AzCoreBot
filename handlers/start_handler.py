from telegram import Update
from telegram.ext import ContextTypes
from data.templates import TEMPLATES
from utils.keyboards import build_keyboard
from services.session_service import reset_session

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    reset_session(user_id)

    template = TEMPLATES["start"]
    keyboard = build_keyboard(template["buttons"])

    await update.message.reply_text(
        template["text"],
        reply_markup=keyboard
    )