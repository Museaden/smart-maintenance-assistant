"""Tests for src.llm."""

from unittest.mock import MagicMock, patch

import src.llm as llm


def test_valid_key_rejects_placeholders():
    assert llm._valid_key("") is False
    assert llm._valid_key("your_key_here") is False
    assert llm._valid_key("your_groq_key_here") is False
    assert llm._valid_key("gsk_real_looking_key_123") is True


def test_is_llm_configured_with_groq(monkeypatch):
    monkeypatch.setattr(llm, "OPENROUTER_API_KEY", "")
    monkeypatch.setattr(llm, "GROQ_API_KEY", "gsk_test_key")
    monkeypatch.setattr(llm, "OPENAI_API_KEY", "")
    assert llm.is_llm_configured() is True


def test_is_llm_configured_false_with_placeholders(monkeypatch):
    monkeypatch.setattr(llm, "OPENROUTER_API_KEY", "your_openrouter_key_here")
    monkeypatch.setattr(llm, "GROQ_API_KEY", "your_groq_key_here")
    monkeypatch.setattr(llm, "OPENAI_API_KEY", "your_key_here")
    assert llm.is_llm_configured() is False


def test_resolve_provider_auto_prefers_openrouter(monkeypatch):
    monkeypatch.setattr(llm, "LLM_PROVIDER", "auto")
    monkeypatch.setattr(llm, "OPENROUTER_API_KEY", "sk-or-v1-real")
    monkeypatch.setattr(llm, "GROQ_API_KEY", "gsk_real")
    assert llm.resolve_provider() == "openrouter"


def test_resolve_provider_forced(monkeypatch):
    monkeypatch.setattr(llm, "LLM_PROVIDER", "groq")
    assert llm.resolve_provider() == "groq"


def test_resolve_provider_falls_back_to_ollama(monkeypatch):
    monkeypatch.setattr(llm, "LLM_PROVIDER", "auto")
    monkeypatch.setattr(llm, "OPENROUTER_API_KEY", "")
    monkeypatch.setattr(llm, "GROQ_API_KEY", "")
    monkeypatch.setattr(llm, "OPENAI_API_KEY", "")
    assert llm.resolve_provider() == "ollama"


def test_get_llm_status_shape(monkeypatch):
    monkeypatch.setattr(llm, "LLM_PROVIDER", "groq")
    monkeypatch.setattr(llm, "GROQ_API_KEY", "gsk_abc")
    monkeypatch.setattr(llm, "OPENROUTER_API_KEY", "")
    monkeypatch.setattr(llm, "OPENAI_API_KEY", "")
    status = llm.get_llm_status()
    assert status["provider"] == "groq"
    assert status["groq_configured"] is True
    assert status["llm_configured"] is True
    assert "model" in status


def test_generate_answer_tries_providers(monkeypatch):
    monkeypatch.setattr(llm, "LLM_PROVIDER", "groq")
    monkeypatch.setattr(llm, "GROQ_API_KEY", "gsk_abc")
    monkeypatch.setattr(llm, "OPENROUTER_API_KEY", "")
    monkeypatch.setattr(llm, "OPENAI_API_KEY", "")

    with patch.object(llm, "_call_groq", return_value="Answer from Groq"):
        text, mode = llm.generate_answer("What is the limit?")

    assert text == "Answer from Groq"
    assert mode == "groq"


def test_generate_answer_raises_when_none_available(monkeypatch):
    monkeypatch.setattr(llm, "LLM_PROVIDER", "auto")
    monkeypatch.setattr(llm, "OPENROUTER_API_KEY", "")
    monkeypatch.setattr(llm, "GROQ_API_KEY", "")
    monkeypatch.setattr(llm, "OPENAI_API_KEY", "")

    with patch.object(llm, "_call_ollama", side_effect=ConnectionError("down")):
        try:
            llm.generate_answer("hi")
            raised = False
        except RuntimeError as exc:
            raised = True
            assert "No LLM provider available" in str(exc)
    assert raised
