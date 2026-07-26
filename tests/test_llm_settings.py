"""Tests for src.llm_settings."""

from src import llm_settings


def test_provider_default_is_string():
    assert isinstance(llm_settings.LLM_PROVIDER, str)
    assert llm_settings.LLM_PROVIDER


def test_model_defaults():
    assert llm_settings.GROQ_MODEL
    assert llm_settings.OPENROUTER_MODEL
    assert llm_settings.OPENAI_MODEL
    assert llm_settings.OLLAMA_MODEL


def test_base_urls_look_valid():
    assert llm_settings.OPENROUTER_BASE_URL.startswith("http")
    assert llm_settings.GROQ_BASE_URL.startswith("http")
    assert llm_settings.OLLAMA_BASE_URL.startswith("http")
