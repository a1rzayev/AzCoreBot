"""Handle nav:* and svc:* inline button callbacks."""
from telegram import Update
from telegram.error import BadRequest
from telegram.ext import ContextTypes

from data.templates import TEMPLATES
from i18n import t
from services.session_service import get_session, reset_session
from services.user_store import get_user_lang
from utils.keyboards import build_nav_keyboard


async def handle_navigation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    data = query.data
    user_id = query.from_user.id
    lang = await get_user_lang(user_id)

    if data.startswith("nav:"):
        state = data[4:]
        session = get_session(user_id)

        if state == "start":
            reset_session(user_id)
            session = get_session(user_id)
        elif state == "contact":
            session["state"] = "contact"
            session["lead_step"] = "company"
        elif state == "incident":
            session["state"] = "incident"
            session["lead_step"] = "incident"
        else:
            session["state"] = state

        template = TEMPLATES.get(state, TEMPLATES["start"])
        keyboard = build_nav_keyboard(template["buttons"], lang)

        try:
            await query.edit_message_text(
                t(lang, template["text_key"]),
                reply_markup=keyboard,
            )
        except BadRequest as e:
            if "message is not modified" not in str(e).lower():
                raise

    elif data.startswith("svc:"):
        label_key = data[4:]
        session = get_session(user_id)

        service_name = t(lang, label_key)
        # Capture the category from the current state before switching
        current_state = session.get("state", "services")
        category_tmpl = TEMPLATES.get(current_state, {})
        category_key = category_tmpl.get("text_key")
        category_name = t(lang, category_key) if category_key else "—"

        session["state"] = "service_request"
        session["selected_service"] = service_name
        session["selected_category"] = category_name

        try:
            await query.edit_message_text(
                t(lang, "service_request_prompt", {"service": service_name})
            )
        except BadRequest as e:
            if "message is not modified" not in str(e).lower():
                raise
