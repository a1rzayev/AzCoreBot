"""Routes text messages to lead, incident, or service request handler based on session state."""
from telegram import Update
from telegram.ext import ContextTypes
from services.session_service import get_session

from handlers.lead_handler import handle_lead
from handlers.ir_handler import handle_ir
from handlers.service_request_handler import handle_service_request


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    session = get_session(user_id)
    step = session.get("lead_step")
    state = session.get("state")

    if state == "service_request":
        await handle_service_request(update, context)
    elif step in ("company", "email"):
        await handle_lead(update, context)
    elif step == "incident":
        await handle_ir(update, context)
    # else: user sent text while on menu — ignore
