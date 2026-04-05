# AzCore Assistant

Telegram chatbot for cybersecurity services and academy lead generation.

## Setup

1. Install requirements:
```
pip install python-telegram-bot --upgrade
```

2. Add your API_TOKEN in env

3. Run:
```
python bot.py
```

## Internationalization

The bot supports multiple languages per user. Each user's choice is saved across bot restarts.

### Supported languages

| Code | Language    | Flag |
|------|-------------|------|
| `en` | English     | 🇬🇧  |
| `ru` | Русский     | 🇷🇺  |
| `az` | Azərbaycan  | 🇦🇿  |

### How to add a new language

1. Add an entry to `config/languages.py`:
   ```python
   LANGUAGES = {
       ...
       "de": {"name": "Deutsch", "flag": "🇩🇪"},
   }
   ```

2. Create `locales/de.json` with all required keys:
   ```json
   {
     "welcome": "👋 Willkommen bei AzCore Assistant, {name}!\n\nBitte wählen Sie:",
     "choose_language": "🌐 Sprache wählen:",
     "language_changed": "✅ Sprache auf Deutsch geändert!",
     "help": "ℹ️ Hilfe",
     "back": "⬅ Zurück"
   }
   ```

3. No other code changes needed — the language picker and `t()` function pick it up automatically.

### Manual smoke-test checklist

- [ ] `/start` shows welcome message in the user's saved language
- [ ] `/language` shows the picker with the current language marked ✓
- [ ] Tapping a language edits the message in-place (no new message sent)
- [ ] Tapping the currently active language does not break anything
- [ ] Restarting the bot preserves each user's language choice
