import html
from telegram import Update
from telegram.ext import ContextTypes

from i18n import t
from services.session_service import get_session, reset_session
from services.submission_service import save_submission
from services.user_store import get_user_lang
from utils.notify import notify_admins


async def handle_lead(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    session = get_session(user_id)
    lang = await get_user_lang(user_id)

    if session["lead_step"] == "company":
        session["lead_data"]["company"] = update.message.text
        session["lead_step"] = "email"
        await update.message.reply_text(t(lang, "lead_email_prompt"))
        return

    if session["lead_step"] == "email":
        session["lead_data"]["email"] = update.message.text
        session["lead_step"] = None

        save_submission(session["lead_data"])

        user_name = update.effective_user.full_name or "—"
        username = update.effective_user.username
        username_str = f"@{username}" if username else "—"
        contact_link = f"tg://user?id={user_id}"

        await notify_admins(
            context.bot,
            f"📩 [LEAD]\n\n"
            f"Şirkət: {html.escape(session['lead_data']['company'])}\n"
            f"Email: {html.escape(session['lead_data']['email'])}\n"
            f"İstifadəçi: {user_name}\n"
            f"Laqab: {username_str}\n"
            f"ID: <code>{user_id}</code>\n"
            f"Əlaqə: <a href=\"{contact_link}\">Söhbətə keç</a>",
        )

        await update.message.reply_text(t(lang, "lead_thank_you"))
        reset_session(user_id)
