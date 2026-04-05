"""Navigation structure for the bot.

Each template has:
  text_key  – i18n key for the message text
  buttons   – list of (label_key, callback_data) pairs
              label_key  : i18n key for the button label
              callback_data: stable routing token (never shown to user)
                "nav:<state>"  – navigate to a named state
                "svc:<key>"    – select a service item
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
    "services": {
        "text_key": "services_text",
        "buttons": [
            ("btn_web",     "nav:services_web"),
            ("btn_network", "nav:services_network"),
            ("btn_system",  "nav:services_system"),
            ("btn_tech",    "nav:services_tech"),
            ("btn_offers",  "nav:services_offers"),
            ("btn_support", "nav:services_support"),
            ("btn_back",    "nav:start"),
        ],
    },
    "services_web": {
        "text_key": "services_web_text",
        "buttons": [
            ("btn_svc_website", "svc:btn_svc_website"),
            ("btn_svc_tgbot",   "svc:btn_svc_tgbot"),
            ("btn_svc_apps",    "svc:btn_svc_apps"),
            ("btn_back",        "nav:services"),
        ],
    },
    "services_network": {
        "text_key": "services_network_text",
        "buttons": [
            ("btn_svc_routing",   "svc:btn_svc_routing"),
            ("btn_svc_switching", "svc:btn_svc_switching"),
            ("btn_svc_firewall",  "svc:btn_svc_firewall"),
            ("btn_svc_security",  "svc:btn_svc_security"),
            ("btn_back",          "nav:services"),
        ],
    },
    "services_system": {
        "text_key": "services_system_text",
        "buttons": [
            ("btn_svc_infra",       "svc:btn_svc_infra"),
            ("btn_svc_winserver",   "svc:btn_svc_winserver"),
            ("btn_svc_linuxserver", "svc:btn_svc_linuxserver"),
            ("btn_svc_backup",      "svc:btn_svc_backup"),
            ("btn_back",            "nav:services"),
        ],
    },
    "services_tech": {
        "text_key": "services_tech_text",
        "buttons": [
            ("btn_svc_cctv",     "svc:btn_svc_cctv"),
            ("btn_svc_helpdesk", "svc:btn_svc_helpdesk"),
            ("btn_svc_cabling",  "svc:btn_svc_cabling"),
            ("btn_back",         "nav:services"),
        ],
    },
    "services_offers": {
        "text_key": "services_offers_text",
        "buttons": [
            ("btn_svc_optic", "svc:btn_svc_optic"),
            ("btn_back",      "nav:services"),
        ],
    },
    "services_support": {
        "text_key": "services_support_text",
        "buttons": [
            ("btn_back", "nav:services"),
        ],
    },
    "contact": {
        "text_key": "contact_text",
        "buttons": [],
    },
    "incident": {
        "text_key": "incident_text",
        "buttons": [],
    },
}
