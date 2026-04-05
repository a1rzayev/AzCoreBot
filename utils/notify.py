"""Send a message to every configured admin chat."""
from telegram import Bot

from config import ADMIN_CHAT_IDS


async def notify_admins(bot: Bot, text: str, parse_mode: str = "HTML") -> None:
    for chat_id in ADMIN_CHAT_IDS:
        await bot.send_message(chat_id=chat_id, text=text, parse_mode=parse_mode)
