from telegram import Update
from telegram.ext import ContextTypes
from services.session_service import get_session, reset_session
from config import ADMIN_CHAT_ID

async def handle_ir(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    session = get_session(user_id)

    if session["lead_step"] == "incident":
        description = update.message.text

        await context.bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=f"🚨 INCIDENT ALERT\nUser: {user_id}\nDescription: {description}"
        )

        await update.message.reply_text("🚨 Incident reported. Our team is responding immediately.")
        reset_session(user_id)