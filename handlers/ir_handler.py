import html
from telegram import Update
from telegram.ext import ContextTypes

from config import ADMIN_CHAT_ID
from i18n import t
from services.session_service import get_session, reset_session
from services.user_store import get_user_lang


async def handle_ir(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    session = get_session(user_id)
    lang = await get_user_lang(user_id)

    if session["lead_step"] == "incident":
        description = update.message.text
        user_name = update.effective_user.full_name or "—"
        username = update.effective_user.username
        username_str = f"@{username}" if username else "—"
        contact_link = f"tg://user?id={user_id}"

        await context.bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=(
                f"🚨 İNSIDENT\n\n"
                f"İstifadəçi: {user_name}\n"
                f"Laqab: {username_str}\n"
                f"ID: <code>{user_id}</code>\n"
                f"Əlaqə: <a href=\"{contact_link}\">Söhbətə keç</a>\n\n"
                f"Təsvir: {html.escape(description)}"
            ),
            parse_mode="HTML",
        )

        await update.message.reply_text(t(lang, "ir_confirmed"))
        reset_session(user_id)
