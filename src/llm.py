"""LLM providers: OpenRouter, Groq, OpenAI, and Ollama."""

from __future__ import annotations

import os
from collections.abc import Callable
from pathlib import Path

import httpx
from dotenv import load_dotenv

# Load .env on every import (avoids stale Streamlit module cache)
_ENV_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(_ENV_ROOT / ".env", encoding="utf-8", override=True)


def _env(name: str, default: str = "") -> str:
    value = os.getenv(name)
    return default if value is None else value


LLM_PROVIDER = _env("LLM_PROVIDER", "auto").lower()
OPENAI_API_KEY = _env("OPENAI_API_KEY", "")
OPENAI_MODEL = _env("OPENAI_MODEL", "gpt-4o-mini")
OPENROUTER_API_KEY = _env("OPENROUTER_API_KEY", "")
OPENROUTER_MODEL = _env("OPENROUTER_MODEL", "openai/gpt-4o-mini")
OPENROUTER_BASE_URL = _env("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
OPENROUTER_APP_URL = _env("OPENROUTER_APP_URL", "http://localhost:8501")
OPENROUTER_APP_NAME = _env("OPENROUTER_APP_NAME", "Smart Maintenance Assistant")
GROQ_API_KEY = _env("GROQ_API_KEY", "")
GROQ_MODEL = _env("GROQ_MODEL", "llama-3.3-70b-versatile")
GROQ_BASE_URL = _env("GROQ_BASE_URL", "https://api.groq.com/openai/v1")
OLLAMA_BASE_URL = _env("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = _env("OLLAMA_MODEL", "llama3.2")

SYSTEM_PROMPT = """You are the Smart Maintenance Assistant, an expert in predictive maintenance and industrial equipment care.

Answer the user's question using ONLY the provided maintenance documentation excerpts.
Rules:
- Be concise, practical, and safety-focused.
- Cite sources inline using [1], [2], etc. matching the excerpt numbers.
- If the excerpts do not contain enough information, say so clearly.
- Never invent specifications, thresholds, or procedures not supported by the excerpts.
"""

PLACEHOLDER_KEYS = {
    "",
    "your_key_here",
    "sk-your-key-here",
    "your_openrouter_key_here",
    "your_groq_key_here",
}


def _valid_key(key: str) -> bool:
    return bool(key and key.strip() not in PLACEHOLDER_KEYS)


def is_llm_configured() -> bool:
    """True if any cloud LLM API key is set (not Ollama-only)."""
    return (
        _valid_key(OPENROUTER_API_KEY)
        or _valid_key(GROQ_API_KEY)
        or _valid_key(OPENAI_API_KEY)
    )


def resolve_provider() -> str:
    """Return the active LLM provider name."""
    if LLM_PROVIDER != "auto":
        return LLM_PROVIDER

    if _valid_key(OPENROUTER_API_KEY):
        return "openrouter"
    if _valid_key(GROQ_API_KEY):
        return "groq"
    if _valid_key(OPENAI_API_KEY):
        return "openai"
    return "ollama"


def get_llm_status() -> dict:
    """Summary for UI: which provider is configured and available."""
    provider = resolve_provider()
    return {
        "provider": provider,
        "openrouter_configured": _valid_key(OPENROUTER_API_KEY),
        "groq_configured": _valid_key(GROQ_API_KEY),
        "openai_configured": _valid_key(OPENAI_API_KEY),
        "llm_configured": is_llm_configured(),
        "model": _model_for_provider(provider),
    }


def _model_for_provider(provider: str) -> str:
    return {
        "openrouter": OPENROUTER_MODEL,
        "groq": GROQ_MODEL,
        "openai": OPENAI_MODEL,
        "ollama": OLLAMA_MODEL,
    }.get(provider, "")


def generate_answer(user_prompt: str) -> tuple[str, str]:
    """Try configured LLM providers in order. Returns (answer_text, mode)."""
    provider = resolve_provider()
    chain = _provider_chain(provider)

    for name, caller in chain:
        try:
            return caller(user_prompt), name
        except Exception:
            continue

    raise RuntimeError("No LLM provider available")


def _provider_chain(primary: str) -> list[tuple[str, Callable[[str], str]]]:
    all_providers = {
        "openrouter": ("openrouter", _call_openrouter),
        "groq": ("groq", _call_groq),
        "openai": ("openai", _call_openai),
        "ollama": ("ollama", _call_ollama),
    }

    order = [primary]
    for name in ("openrouter", "groq", "openai", "ollama"):
        if name not in order:
            order.append(name)

    chain = []
    for name in order:
        if name == "openrouter" and not _valid_key(OPENROUTER_API_KEY):
            continue
        if name == "groq" and not _valid_key(GROQ_API_KEY):
            continue
        if name == "openai" and not _valid_key(OPENAI_API_KEY):
            continue
        chain.append(all_providers[name])
    return chain


def _messages(user_prompt: str) -> list[dict]:
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ]


def _call_openai_compatible(
    *,
    api_key: str,
    base_url: str,
    model: str,
    user_prompt: str,
    extra_headers: dict | None = None,
) -> str:
    from openai import OpenAI

    headers = extra_headers or {}
    client = OpenAI(api_key=api_key, base_url=base_url, default_headers=headers)
    response = client.chat.completions.create(
        model=model,
        messages=_messages(user_prompt),
        temperature=0.2,
    )
    return response.choices[0].message.content or ""


def _call_openrouter(user_prompt: str) -> str:
    return _call_openai_compatible(
        api_key=OPENROUTER_API_KEY,
        base_url=OPENROUTER_BASE_URL,
        model=OPENROUTER_MODEL,
        user_prompt=user_prompt,
        extra_headers={
            "HTTP-Referer": OPENROUTER_APP_URL,
            "X-Title": OPENROUTER_APP_NAME,
        },
    )


def _call_groq(user_prompt: str) -> str:
    return _call_openai_compatible(
        api_key=GROQ_API_KEY,
        base_url=GROQ_BASE_URL,
        model=GROQ_MODEL,
        user_prompt=user_prompt,
    )


def _call_openai(user_prompt: str) -> str:
    return _call_openai_compatible(
        api_key=OPENAI_API_KEY,
        base_url="https://api.openai.com/v1",
        model=OPENAI_MODEL,
        user_prompt=user_prompt,
    )


def _call_ollama(user_prompt: str) -> str:
    payload = {
        "model": OLLAMA_MODEL,
        "messages": _messages(user_prompt),
        "stream": False,
        "options": {"temperature": 0.2},
    }
    with httpx.Client(timeout=120.0) as client:
        resp = client.post(f"{OLLAMA_BASE_URL}/api/chat", json=payload)
        resp.raise_for_status()
        return resp.json()["message"]["content"]


def get_openrouter_limits() -> dict | None:
    """Check OpenRouter limits via GET /api/v1/key."""
    if not _valid_key(OPENROUTER_API_KEY):
        return None

    with httpx.Client(timeout=30.0) as client:
        resp = client.get(
            f"{OPENROUTER_BASE_URL}/key",
            headers={"Authorization": f"Bearer {OPENROUTER_API_KEY}"},
        )
        resp.raise_for_status()
        payload = resp.json()
        return payload.get("data", payload)
