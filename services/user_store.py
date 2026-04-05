"""Persist each Telegram user's chosen language across bot restarts.

Storage: data/users.json  (a plain JSON object keyed by str(user_id))
Writes are serialised through an asyncio.Lock to avoid concurrent-write corruption.
"""
import asyncio
import json
import os

from config.languages import DEFAULT_LANGUAGE

_DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "users.json")
_write_lock = asyncio.Lock()
_store: dict[str, str] = {}


def _load() -> None:
    global _store
    if os.path.exists(_DATA_FILE):
        with open(_DATA_FILE, encoding="utf-8") as f:
            _store = json.load(f)
    else:
        _store = {}


_load()


async def _flush() -> None:
    async with _write_lock:
        with open(_DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(_store, f, ensure_ascii=False, indent=2)


async def get_user_lang(user_id: int) -> str:
    """Return the saved language for *user_id*, or DEFAULT_LANGUAGE if not set."""
    return _store.get(str(user_id), DEFAULT_LANGUAGE)


async def set_user_lang(user_id: int, lang: str) -> None:
    """Persist *lang* for *user_id* and flush to disk."""
    _store[str(user_id)] = lang
    await _flush()
