"""Navigation structure for the bot.

Each template has:
  text_key  – i18n key for the message text
  buttons   – list of (label_key, callback_data) pairs
              label_key  : i18n key for the button label
              callback_data: stable routing token (never shown to user)

Routing rules:
  "nav:<state>"  – navigate to a named state
  "svc:<key>"    – select a service item (triggers request flow)
  "settings"     – open settings (language picker)
"""

TEMPLATES = {
    "start": {
        "text_key": "start_text",
        "buttons": [
            ("btn_services", "nav:services"),
            ("btn_incident", "nav:incident"),
            ("btn_contact",  "nav:contact"),
            ("btn_settings", "settings"),
        ],
    },

    # ===================== MAIN SERVICES =====================
    "services": {
        "text_key": "services_text",
        "buttons": [
            ("btn_web",      "nav:services_web"),
            ("btn_system",   "nav:services_system"),
            ("btn_network",  "nav:services_network"),
            ("btn_tech",     "nav:services_tech"),
            ("btn_business", "nav:services_business"),
            ("btn_offers",   "nav:services_offers"),
            ("btn_support",  "nav:services_support"),
            ("btn_back",     "nav:start"),
        ],
    },

    # ===================== WEB =====================
    "services_web": {
        "text_key": "services_web_text",
        "buttons": [
            ("btn_svc_website", "svc:website"),
            ("btn_svc_tgbot",   "svc:tgbot"),
            ("btn_svc_apps",    "svc:apps"),
            ("btn_back",        "nav:services"),
        ],
    },

    # ===================== SYSTEM =====================
    "services_system": {
        "text_key": "services_system_text",
        "buttons": [
            ("btn_svc_infra",       "svc:infra"),
            ("btn_svc_winserver",   "svc:winserver"),
            ("btn_svc_linuxserver", "svc:linuxserver"),
            ("btn_svc_backup",      "svc:backup"),
            ("btn_back",            "nav:services"),
        ],
    },

    # ===================== NETWORK =====================
    "services_network": {
        "text_key": "services_network_text",
        "buttons": [
            ("btn_svc_routing",   "svc:routing"),
            ("btn_svc_switching", "svc:switching"),
            ("btn_svc_firewall",  "svc:firewall"),
            ("btn_svc_security",  "svc:security"),
            ("btn_back",          "nav:services"),
        ],
    },

    # ===================== TECH =====================
    "services_tech": {
        "text_key": "services_tech_text",
        "buttons": [
            ("btn_svc_cctv",     "svc:cctv"),
            ("btn_svc_helpdesk", "svc:helpdesk"),
            ("btn_svc_cabling",  "svc:cabling"),
            ("btn_back",         "nav:services"),
        ],
    },

    # ===================== BUSINESS (ERP, etc.) =====================
    "services_business": {
        "text_key": "services_business_text",
        "buttons": [
            ("btn_svc_erp", "svc:erp"),
            ("btn_back",    "nav:services"),
        ],
    },

    # ===================== OFFERS =====================
    "services_offers": {
        "text_key": "services_offers_text",
        "buttons": [
            ("btn_svc_optic", "svc:optic"),
            ("btn_back",      "nav:services"),
        ],
    },

    # ===================== SUPPORT =====================
    "services_support": {
        "text_key": "services_support_text",
        "buttons": [
            ("btn_svc_write_request", "svc:write_request"),
            ("btn_back",              "nav:services"),
        ],
    },

    # ===================== CONTACT =====================
    "contact": {
        "text_key": "contact_text",
        "buttons": [
            ("btn_back", "nav:start"),
        ],
    },

    # ===================== INCIDENT =====================
    "incident": {
        "text_key": "incident_text",
        "buttons": [
            ("btn_back", "nav:start"),
        ],
    },
}