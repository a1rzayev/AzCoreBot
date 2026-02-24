import logging
import time
from telegram import Update
from telegram.error import Conflict
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

from config import BOT_TOKEN
from handlers.start_handler import start
from handlers.navigation_handler import handle_navigation
from handlers.text_handler import handle_text

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

RETRY_DELAY = 15  # seconds before restart after a crash


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.error and isinstance(context.error, Conflict):
        logger.warning(
            "Conflict (another instance may be running). This process will keep retrying."
        )
        return
    logger.exception("Exception while handling an update: %s", context.error)


def build_app():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_navigation))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_error_handler(error_handler)
    return app


if __name__ == "__main__":
    while True:
        try:
            app = build_app()
            logger.info("AzCore Assistant is running...")
            app.run_polling()
        except Conflict as e:
            logger.warning("Polling conflict: %s. Restarting in %ss...", e, RETRY_DELAY)
        except Exception as e:
            logger.exception("Bot stopped: %s. Restarting in %ss...", e, RETRY_DELAY)
        time.sleep(RETRY_DELAY)