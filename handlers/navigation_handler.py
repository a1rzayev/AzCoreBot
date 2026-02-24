from telegram import Update
from telegram.error import BadRequest
from telegram.ext import ContextTypes
from data.templates import TEMPLATES
from utils.keyboards import build_keyboard
from services.session_service import get_session

async def handle_navigation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    session = get_session(user_id)

    choice = query.data
    state = session["state"]

    # Ana menyu
    if choice == "🛡 Xidmətlər":
        session["state"] = "services"
    elif choice == "📞 Əlaqə":
        session["state"] = "contact"
        session["lead_step"] = "company"
    elif choice == "🚨 İnsidentə Cavab":
        session["state"] = "incident"
        session["lead_step"] = "incident"
    # Xidmətlər alt kateqoriyaları
    elif choice == "🌐 Web":
        session["state"] = "services_web"
    elif choice == "🔗 Şəbəkə":
        session["state"] = "services_network"
    elif choice == "💻 Sistem":
        session["state"] = "services_system"
    elif choice == "👷 Texniki Komanda":
        session["state"] = "services_tech"
    elif choice == "📡 Təkliflər":
        session["state"] = "services_offers"
    elif choice == "📅 Dəstək (bir dəfəlik / aylıq)":
        session["state"] = "services_support"
    # Geri
    elif choice == "⬅ Geri":
        if state.startswith("services_"):
            session["state"] = "services"
        else:
            session["state"] = "start"
    # Seçilmiş xidmət (alt səviyyə) — təsvir soruş
    elif state.startswith("services_") and choice != "⬅ Geri":
        session["state"] = "service_request"
        session["selected_service"] = choice
        _category_names = {
            "services_web": "Web",
            "services_network": "Şəbəkə",
            "services_system": "Sistem",
            "services_tech": "Texniki Komanda",
            "services_offers": "Təkliflər",
            "services_support": "Dəstək (bir dəfəlik / aylıq)",
        }
        session["selected_category"] = _category_names.get(state, state)
        try:
            await query.edit_message_text(
                f"📩 Seçdiyiniz xidmət: {choice}\n\n"
                "Zəhmət olmasa sorğunuzun təsvirini yazın:"
            )
        except BadRequest as e:
            if "message is not modified" not in str(e).lower():
                raise
        return

    template = TEMPLATES.get(session["state"], TEMPLATES["start"])
    keyboard = build_keyboard(template["buttons"]) if template["buttons"] else None

    try:
        await query.edit_message_text(
            template["text"],
            reply_markup=keyboard
        )
    except BadRequest as e:
        if "message is not modified" not in str(e).lower():
            raise
        # User e.g. double-tapped same button; message already shows this content — ignore