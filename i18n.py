"""Load locale files at startup and expose t() for translated strings."""
import json
import os
from config.languages import DEFAULT_LANGUAGE

_locales: dict[str, dict] = {}


def _load_locales() -> None:
    locales_dir = os.path.join(os.path.dirname(__file__), "locales")
    for filename in os.listdir(locales_dir):
        if filename.endswith(".json"):
            lang = filename[:-5]
            with open(os.path.join(locales_dir, filename), encoding="utf-8") as f:
                _locales[lang] = json.load(f)


_load_locales()


def t(lang: str, key: str, vars: dict | None = None) -> str:
    """Return the translated string for *key* in *lang*, interpolating *vars*.

    Falls back to DEFAULT_LANGUAGE when *lang* is unknown, and returns *key*
    unchanged when the key itself is missing from both locales.
    """
    if vars is None:
        vars = {}
    locale = _locales.get(lang) or _locales.get(DEFAULT_LANGUAGE, {})
    text = locale.get(key)
    if text is None:
        text = _locales.get(DEFAULT_LANGUAGE, {}).get(key, key)
    for k, v in vars.items():
        text = text.replace(f"{{{k}}}", str(v))
    return text
