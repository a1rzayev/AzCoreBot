"""Handle service request description: send to admin and confirm to user."""
import html
from telegram import Update
from telegram.ext import ContextTypes

from i18n import t
from services.session_service import get_session, reset_session
from services.user_store import get_user_lang
from utils.notify import notify_admins


async def handle_service_request(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    session = get_session(user_id)
    lang = await get_user_lang(user_id)

    description = update.message.text.strip()
    category = session.get("selected_category", "—")
    service = session.get("selected_service", "—")

    user_name = update.effective_user.full_name or "İstifadəçi"
    username = update.effective_user.username
    username_str = f"@{username}" if username else "—"
    contact_link = f"tg://user?id={user_id}"

    await notify_admins(
        context.bot,
        f"📩 Xidmət sorğusu\n\n"
        f"Kateqoriya: {category}\n"
        f"Xidmət: {service}\n"
        f"İstifadəçi: {user_name}\n"
        f"Laqab: {username_str}\n"
        f"ID: <code>{user_id}</code>\n"
        f"Əlaqə: <a href=\"{contact_link}\">Söhbətə keç</a>\n\n"
        f"Təsvir:\n{html.escape(description)}",
    )

    await update.message.reply_text(t(lang, "service_request_confirmed"))
    reset_session(user_id)
