"""Tests for app.py module loading (UI smoke checks)."""

import importlib
from unittest.mock import MagicMock, patch


class _FakeSessionState(dict):
    """Minimal Streamlit session_state stand-in."""

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError as exc:
            raise AttributeError(key) from exc

    def __setattr__(self, key, value):
        self[key] = value


def test_app_imports_without_running_streamlit():
    """Importing app should configure Streamlit but not crash."""
    fake_st = MagicMock()
    fake_st.session_state = _FakeSessionState()
    fake_st.chat_input.return_value = None
    fake_st.sidebar.__enter__ = MagicMock(return_value=fake_st.sidebar)
    fake_st.sidebar.__exit__ = MagicMock(return_value=False)

    with (
        patch.dict("sys.modules", {"streamlit": fake_st}),
        patch("src.vector_store.collection_count", return_value=5),
        patch(
            "src.llm.get_llm_status",
            return_value={
                "provider": "groq",
                "model": "llama-3.3-70b-versatile",
                "openrouter_configured": False,
                "groq_configured": True,
                "openai_configured": False,
                "llm_configured": True,
            },
        ),
    ):
        import sys

        sys.modules.pop("app", None)
        importlib.import_module("app")

    fake_st.set_page_config.assert_called()
    fake_st.title.assert_called()
