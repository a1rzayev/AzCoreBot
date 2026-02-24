import os
import json
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from templates import templates
from datetime import datetime
from pathlib import Path

load_dotenv()
TOKEN = os.getenv("API_TOKEN")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")

if not TOKEN:
    raise ValueError("❌ API_TOKEN is missing! Add it to your .env file.")

SUBMISSIONS_FILE = "submissions.json"
user_context = {}

FORM_FLOWS = {
    "service_request": {
        "fields": ["company_name", "email", "phone", "service_type", "description", "infrastructure", "timeline"],
        "prompts": {
            "company_name": "📝 Şirkət / Tam adınızı daxil edin:",
            "email": "📧 E-mail ünvanınızı daxil edin:",
            "phone": "📞 Telefon nömrənizi daxil edin:",
            "service_type": "🛡️ Xidmət növünü daxil edin:",
            "description": "📄 Qısa izah daxil edin:",
            "infrastructure": "🖥️ İnfrastruktur haqqında məlumat:",
            "timeline": "📅 Preferred timeline:"
        }
    },
    "registration": {
        "fields": ["full_name", "email", "phone", "course", "experience"],
        "prompts": {
            "full_name": "📝 Tam adınızı daxil edin:",
            "email": "📧 E-mail ünvanınızı daxil edin:",
            "phone": "📞 Telefon nömrənizi daxil edin:",
            "course": "🎓 Hansı kursa qeydiyyatdan keçmək istəyirsiniz?",
            "experience": "💼 IT təcrübəniz haqqında qısa məlumat:"
        }
    },
    "cv_submission": {
        "fields": ["full_name", "email", "phone", "position", "experience", "cv_link"],
        "prompts": {
            "full_name": "📝 Tam adınızı daxil edin:",
            "email": "📧 E-mail ünvanınızı daxil edin:",
            "phone": "📞 Telefon nömrənizi daxil edin:",
            "position": "💼 Hansı vəzifə üçün müraciət edirsiniz?",
            "experience": "📊 Təcrübəniz (illə):",
            "cv_link": "📄 CV linki və ya məlumatları göndərin:"
        }
    },
    "contact": {
        "fields": ["full_name", "email", "phone", "subject", "message"],
        "prompts": {
            "full_name": "📝 Tam adınızı daxil edin:",
            "email": "📧 E-mail ünvanınızı daxil edin:",
            "phone": "📞 Telefon nömrənizi daxil edin:",
            "subject": "📋 Mövzu:",
            "message": "💬 Mesajınız:"
        }
    },
    "emergency_ir": {
        "fields": ["company_name", "contact_person", "phone", "incident_description", "incident_time"],
        "prompts": {
            "company_name": "🏢 Şirkət adı:",
            "contact_person": "👤 Əlaqə şəxsi:",
            "phone": "📞 Təcili əlaqə nömrəsi:",
            "incident_description": "🚨 İnsident təsviri:",
            "incident_time": "⏰ Baş verən vaxt:"
        }
    },
    "demo_request": {
        "fields": ["full_name", "email", "phone", "demo_type", "preferred_date"],
        "prompts": {
            "full_name": "📝 Tam adınızı daxil edin:",
            "email": "📧 E-mail ünvanınızı daxil edin:",
            "phone": "📞 Telefon nömrənizi daxil edin:",
            "demo_type": "🎬 Demo növü (kurs/xidmət):",
            "preferred_date": "📅 Tərcih etdiyiniz tarix:"
        }
    },
    "scholarship": {
        "fields": ["full_name", "email", "phone", "program", "reason", "financial_need"],
        "prompts": {
            "full_name": "📝 Tam adınızı daxil edin:",
            "email": "📧 E-mail ünvanınızı daxil edin:",
            "phone": "📞 Telefon nömrənizi daxil edin:",
            "program": "🎓 Hansı proqram üçün?",
            "reason": "📄 Scholarship səbəbi:",
            "financial_need": "💰 Maliyyə ehtiyacı haqqında:"
        }
    }
}

BUTTON_FORM_MAPPING = {
    "Sorğu göndər": "service_request",
    "PenTest sorğusu": "service_request",
    "Konsultasiya tələb et": "service_request",
    "Cloud audit sorğula": "service_request",
    "Uyğunluq auditini sifariş et": "service_request",
    "Kod yoxlanışı sifariş et": "service_request",
    "Pilot kampaniya başlat": "service_request",
    "Korporativ təlim üçün sorğu": "service_request",
    "Ətraflı təklif": "service_request",
    "Qiymət sorğula": "service_request",
    "Qeydiyyat": "registration",
    "Online qeydiyyat": "registration",
    "Bootcamp qeydiyyatı": "registration",
    "Webinar qeydiyyatı": "registration",
    "Lab qeydiyyatı": "registration",
    "CTF qeydiyyatı": "registration",
    "CV göndər": "cv_submission",
    "Müraciət et": "cv_submission",
    "Əlaqə göndər": "contact",
    "Biznes konsultasiya": "contact",
    "Texniki dəstək": "contact",
    "Konsultasiya": "contact",
    "İnsident bildir": "emergency_ir",
    "Kritik insident bildir": "emergency_ir",
    "Demo": "demo_request",
    "Demo dərs": "demo_request",
    "Demo + Case Study": "demo_request",
    "Demo + qiymət sorğula": "demo_request",
    "Scholarship": "scholarship"
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question = templates["start"]["question"]
    buttons = [[b] for b in templates["start"]["buttons"]]
    markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    await update.message.reply_text(question, reply_markup=markup)
    
    user_id = update.effective_user.id
    if user_id in user_context:
        del user_context[user_id]

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.effective_user.id
    
    if user_id in user_context and user_context[user_id].get("in_flow"):
        await handle_form_input(update, context)
        return
    
    if text == "Geri":
        if user_id in user_context:
            del user_context[user_id]
        await start(update, context)
        return
    
    if text in BUTTON_FORM_MAPPING:
        await start_form_flow(update, context, text)
        return
    
    if text in templates:
        template = templates[text]
        
        if isinstance(template, dict) and "content" in template:
            content = template["content"]
            buttons = template.get("buttons", [])
            
            if buttons:
                button_rows = []
                for i in range(0, len(buttons), 2):
                    row = buttons[i:i+2]
                    button_rows.append(row)
                markup = ReplyKeyboardMarkup(button_rows, resize_keyboard=True)
                await update.message.reply_text(content, reply_markup=markup, parse_mode='Markdown')
            else:
                await update.message.reply_text(content, parse_mode='Markdown')
        
        elif isinstance(template, str):
            await update.message.reply_text(template)
    
    else:
        await update.message.reply_text("Bağışlayın, bu suala cavabım yoxdur 🤖\n\nƏsas menyuya qayıtmaq üçün /start yazın.")

async def start_form_flow(update: Update, context: ContextTypes.DEFAULT_TYPE, button_text: str):
    user_id = update.effective_user.id
    form_type = BUTTON_FORM_MAPPING[button_text]
    flow = FORM_FLOWS[form_type]
    
    user_context[user_id] = {
        "form_type": form_type,
        "button_text": button_text,
        "in_flow": True,
        "current_field_index": 0,
        "fields": flow["fields"],
        "prompts": flow["prompts"],
        "data": {},
        "started_at": datetime.now().isoformat()
    }
    
    first_field = flow["fields"][0]
    first_prompt = flow["prompts"][first_field]
    cancel_markup = ReplyKeyboardMarkup([["❌ Ləğv et"]], resize_keyboard=True)
    
    await update.message.reply_text(
        f"✅ **{button_text}**\n\n{first_prompt}",
        reply_markup=cancel_markup,
        parse_mode='Markdown'
    )

COURSE_LIST = [
    "Kiber Təhlükəsizlik Bootcamp",
    "Penetration Testing",
    "SOC Analyst",
    "Secure Development",
    "Cloud Security",
    "Red Team Operations",
    "Security Awareness"
]

async def handle_form_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text
    
    if text == "❌ Ləğv et":
        del user_context[user_id]
        await update.message.reply_text("❌ Əməliyyat ləğv edildi.")
        await start(update, context)
        return
    
    user_data = user_context[user_id]
    fields = user_data["fields"]
    prompts = user_data["prompts"]
    current_index = user_data["current_field_index"]
    current_field = fields[current_index]
    
    # Validate course selection - only accept button clicks
    if current_field == "course" and user_data["form_type"] == "registration":
        if text not in COURSE_LIST:
            course_buttons = [[course] for course in COURSE_LIST + ["❌ Ləğv et"]]
            markup = ReplyKeyboardMarkup(course_buttons, resize_keyboard=True)
            await update.message.reply_text(
                "❌ Zəhmət olmasa düymələrdən birini seçin!",
                reply_markup=markup
            )
            return
    
    user_data["data"][current_field] = text
    current_index += 1
    user_data["current_field_index"] = current_index
    
    if current_index >= len(fields):
        await complete_form(update, context)
    else:
        next_field = fields[current_index]
        next_prompt = prompts[next_field]
        
        # Show course selection as buttons for registration forms
        if next_field == "course" and user_data["form_type"] == "registration":
            course_buttons = [[course] for course in COURSE_LIST + ["❌ Ləğv et"]]
            markup = ReplyKeyboardMarkup(course_buttons, resize_keyboard=True)
        else:
            markup = ReplyKeyboardMarkup([["❌ Ləğv et"]], resize_keyboard=True)
        
        await update.message.reply_text(
            f"{next_prompt}",
            reply_markup=markup,
            parse_mode='Markdown'
        )

def save_submission_to_file(submission_data):
    try:
        submissions = []
        if Path(SUBMISSIONS_FILE).exists():
            with open(SUBMISSIONS_FILE, 'r', encoding='utf-8') as f:
                try:
                    submissions = json.load(f)
                except json.JSONDecodeError:
                    submissions = []
        
        submissions.append(submission_data)
        
        with open(SUBMISSIONS_FILE, 'w', encoding='utf-8') as f:
            json.dump(submissions, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Saved to {SUBMISSIONS_FILE}")
    except Exception as e:
        print(f"❌ Error saving: {e}")

async def complete_form(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_data = user_context[user_id]
    user_info = update.effective_user
    form_type = user_data["form_type"]
    button_text = user_data["button_text"]
    data = user_data["data"]
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    admin_message = f"""
🔔 **YENİ SORĞU: {button_text}**

👤 **İstifadəçi:**
• ID: {user_id}
• Username: @{user_info.username or 'N/A'}
• Ad: {user_info.first_name} {user_info.last_name or ''}
• Tarix: {timestamp}

📋 **Növ:** {form_type}

📝 **Məlumatlar:**
"""
    
    for field, value in data.items():
        field_name = user_data["prompts"][field].replace(":", "").replace("📝 ", "").replace("📧 ", "").replace("📞 ", "").replace("🛡️ ", "").replace("📄 ", "").replace("🖥️ ", "").replace("📅 ", "").replace("🎓 ", "").replace("💼 ", "").replace("📊 ", "").replace("📋 ", "").replace("💬 ", "").replace("🏢 ", "").replace("👤 ", "").replace("🚨 ", "").replace("⏰ ", "").replace("🎬 ", "").replace("💰 ", "")
        admin_message += f"• {field_name}: {value}\n"
    
    submission_data = {
        "timestamp": timestamp,
        "submission_id": f"{user_id}_{int(datetime.now().timestamp())}",
        "user_info": {
            "user_id": user_id,
            "username": user_info.username,
            "first_name": user_info.first_name,
            "last_name": user_info.last_name
        },
        "form_type": form_type,
        "button_text": button_text,
        "data": data
    }
    
    save_submission_to_file(submission_data)
    
    if ADMIN_CHAT_ID:
        try:
            await context.bot.send_message(
                chat_id=ADMIN_CHAT_ID,
                text=admin_message,
                parse_mode='Markdown'
            )
            print(f"✅ Sent to Chat ID: {ADMIN_CHAT_ID}")
        except Exception as e:
            print(f"❌ Chat ID error: {e}")
    
    if ADMIN_USERNAME:
        try:
            username = ADMIN_USERNAME.lstrip('@')
            await context.bot.send_message(
                chat_id=f"@{username}",
                text=admin_message,
                parse_mode='Markdown'
            )
            print(f"✅ Sent to @{username}")
        except Exception as e:
            print(f"❌ Username error: {e}")
            print(f"💡 Send /start to bot first!")
    
    print("\n" + "="*60)
    print(admin_message)
    print("="*60 + "\n")
    
    await update.message.reply_text(
        "✅ **Təşəkkürlər!**\n\nMüraciətiniz qeydə alındı. Komandamız ən qısa müddətdə sizinlə əlaqə saxlayacaq.\n\n📧 Email: info@huntech.az\n📞 Telefon: +994 50 123 45 67",
        parse_mode='Markdown'
    )
    
    del user_context[user_id]
    await start(update, context)

async def handle_callback_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    print(f"❌ Error: {context.error}")

def main():
    app = Application.builder().token(TOKEN).build()
    
    app.add_error_handler(error_handler)
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(handle_callback_query))
    
    print("🤖 HunTech Bot başladılır...")
    print(f"📊 {len(templates)} səhifə | {len(BUTTON_FORM_MAPPING)} forma")
    print(f"📧 Admin: {ADMIN_USERNAME or ADMIN_CHAT_ID or 'Qeyd edilməyib'}")
    print("✅ Bot işə salındı!")
    print("🛑 Dayandırmaq üçün Ctrl+C basın\n")
    
    try:
        app.run_polling(drop_pending_updates=True)
    except KeyboardInterrupt:
        print("\n🛑 Bot dayandırıldı.")
    except Exception as e:
        print(f"❌ Xəta: {e}")

if __name__ == "__main__":
    main()
