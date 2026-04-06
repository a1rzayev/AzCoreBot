import html
from telegram import Update
from telegram.ext import ContextTypes

from i18n import t
from services.session_service import get_session, reset_session
from services.user_store import get_user_lang
from utils.keyboards import post_request_keyboard
from utils.notify import notify_admins


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

        await notify_admins(
            context.bot,
            f"🚨 İNSIDENT\n\n"
            f"İstifadəçi: {user_name}\n"
            f"Laqab: {username_str}\n"
            f"ID: <code>{user_id}</code>\n"
            f"Əlaqə: <a href=\"{contact_link}\">Söhbətə keç</a>\n\n"
            f"Təsvir: {html.escape(description)}",
        )

        await update.message.reply_text(
            t(lang, "ir_confirmed"),
            reply_markup=post_request_keyboard(lang),
        )
        reset_session(user_id)
