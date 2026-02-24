from telegram import Update
from telegram.ext import ContextTypes
from services.session_service import get_session, reset_session
from services.submission_service import save_submission
from config import ADMIN_CHAT_ID

async def handle_lead(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    session = get_session(user_id)

    if session["lead_step"] == "company":
        session["lead_data"]["company"] = update.message.text
        session["lead_step"] = "email"
        await update.message.reply_text("Enter your email:")
        return

    elif session["lead_step"] == "email":
        session["lead_data"]["email"] = update.message.text
        session["lead_step"] = None

        save_submission(session["lead_data"])

        await context.bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=f"[LEAD]\nCompany: {session['lead_data']['company']}\nEmail: {session['lead_data']['email']}"
        )

        await update.message.reply_text("✅ Thank you. Our team will contact you shortly.")
        reset_session(user_id)