"""Handle service request description: send to admin and confirm to user."""
from telegram import Update
from telegram.ext import ContextTypes
from services.session_service import get_session, reset_session
from config import ADMIN_CHAT_ID


async def handle_service_request(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    session = get_session(user_id)
    description = update.message.text.strip()
    category = session.get("selected_category", "—")
    service = session.get("selected_service", "—")

    # Admin-ə göndər
    user_name = update.effective_user.full_name or "İstifadəçi"
    username = update.effective_user.username
    username_str = f"@{username}" if username else "—"
    await context.bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        text=(
            f"📩 Xidmət sorğusu\n\n"
            f"Kateqoriya: {category}\n"
            f"Xidmət: {service}\n"
            f"İstifadəçi: {user_name} ({username_str})\n"
            f"ID: {user_id}\n\n"
            f"Təsvir:\n{description}"
        ),
    )

    await update.message.reply_text(
        "✅ Sorğunuz qeydə alındı. Komandamız tezliklə sizinlə əlaqə saxlayacaq."
    )
    reset_session(user_id)
