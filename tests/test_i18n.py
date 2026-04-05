"""Smoke tests for the i18n layer and user language store."""
import asyncio
import json
import os
import tempfile
import unittest


# ---------------------------------------------------------------------------
# t() function tests
# ---------------------------------------------------------------------------

class TestTranslation(unittest.TestCase):

    def test_returns_correct_string_for_each_locale(self):
        from i18n import t

        self.assertIn("Welcome", t("en", "welcome", {"name": "X"}))
        self.assertIn("Добро пожаловать", t("ru", "welcome", {"name": "X"}))
        self.assertIn("xoş gəlmisiniz", t("az", "welcome", {"name": "X"}))

    def test_variable_interpolation(self):
        from i18n import t

        result = t("en", "welcome", {"name": "Alex"})
        self.assertIn("Alex", result)
        self.assertNotIn("{name}", result)

    def test_fallback_to_default_language_for_unknown_lang(self):
        from i18n import t
        from config.languages import DEFAULT_LANGUAGE

        result_unknown = t("xx", "welcome", {"name": "Y"})
        result_default = t(DEFAULT_LANGUAGE, "welcome", {"name": "Y"})
        self.assertEqual(result_unknown, result_default)

    def test_missing_key_returns_key_name(self):
        from i18n import t

        self.assertEqual(t("en", "nonexistent_key"), "nonexistent_key")

    def test_all_locales_have_required_keys(self):
        from i18n import t

        required_keys = ["welcome", "choose_language", "language_changed", "help", "back"]
        for lang in ("en", "ru", "az"):
            for key in required_keys:
                result = t(lang, key, {"name": "Z"})
                self.assertNotEqual(result, key, f"Missing key '{key}' in locale '{lang}'")


# ---------------------------------------------------------------------------
# user_store tests (using a temp file to avoid touching real data/users.json)
# ---------------------------------------------------------------------------

class TestUserStore(unittest.TestCase):

    def setUp(self):
        # Patch _DATA_FILE to a temp file for isolation
        import services.user_store as us
        self._tmp = tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        )
        self._tmp.write("{}")
        self._tmp.close()
        self._orig_file = us._DATA_FILE
        us._DATA_FILE = self._tmp.name
        us._load()

    def tearDown(self):
        import services.user_store as us
        us._DATA_FILE = self._orig_file
        us._load()
        os.unlink(self._tmp.name)

    def _run(self, coro):
        return asyncio.get_event_loop().run_until_complete(coro)

    def test_get_user_lang_returns_default_for_new_user(self):
        from services.user_store import get_user_lang
        from config.languages import DEFAULT_LANGUAGE

        lang = self._run(get_user_lang(99999))
        self.assertEqual(lang, DEFAULT_LANGUAGE)

    def test_set_and_get_round_trip(self):
        from services.user_store import get_user_lang, set_user_lang

        self._run(set_user_lang(12345, "ru"))
        lang = self._run(get_user_lang(12345))
        self.assertEqual(lang, "ru")

    def test_persistence_across_reload(self):
        import services.user_store as us
        from services.user_store import get_user_lang, set_user_lang

        self._run(set_user_lang(42, "az"))
        us._load()  # simulate restart
        lang = self._run(get_user_lang(42))
        self.assertEqual(lang, "az")


# ---------------------------------------------------------------------------
# keyboard tests
# ---------------------------------------------------------------------------

class TestLanguageKeyboard(unittest.TestCase):

    def test_current_lang_has_checkmark(self):
        from utils.keyboards import language_keyboard

        kb = language_keyboard("ru")
        all_texts = [btn.text for row in kb.inline_keyboard for btn in row]
        checked = [t for t in all_texts if t.startswith("✓")]
        self.assertEqual(len(checked), 1)
        self.assertIn("Русский", checked[0])

    def test_other_langs_have_no_checkmark(self):
        from utils.keyboards import language_keyboard

        kb = language_keyboard("en")
        for row in kb.inline_keyboard:
            for btn in row:
                if "English" not in btn.text:
                    self.assertFalse(btn.text.startswith("✓"), btn.text)

    def test_callback_data_format(self):
        from utils.keyboards import language_keyboard
        from config.languages import SUPPORTED_LANGS

        kb = language_keyboard("en")
        data_values = [btn.callback_data for row in kb.inline_keyboard for btn in row]
        for code in SUPPORTED_LANGS:
            self.assertIn(f"set_lang:{code}", data_values)


# ---------------------------------------------------------------------------
# callback_router: invalid set_lang code does nothing
# ---------------------------------------------------------------------------

class TestCallbackRouter(unittest.IsolatedAsyncioTestCase):

    async def test_invalid_set_lang_answers_and_returns(self):
        """set_lang with an unsupported code must answer the query and not crash."""
        from unittest.mock import AsyncMock, MagicMock
        from handlers.callback_router import handle_callback

        query = MagicMock()
        query.data = "set_lang:xx"
        query.from_user.id = 1
        query.from_user.first_name = "Test"
        query.answer = AsyncMock()
        query.edit_message_text = AsyncMock()

        update = MagicMock()
        update.callback_query = query

        await handle_callback(update, MagicMock())

        query.answer.assert_called_once_with()
        query.edit_message_text.assert_not_called()


if __name__ == "__main__":
    unittest.main()
