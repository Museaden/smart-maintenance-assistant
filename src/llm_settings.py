"""LLM provider settings (separate module to avoid Streamlit config cache issues)."""

import os
from pathlib import Path

from dotenv import load_dotenv

# Load .env from project root
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(_PROJECT_ROOT / ".env", encoding="utf-8")
load_dotenv(encoding="utf-8")


def _str(name: str, default: str = "") -> str:
    value = os.getenv(name)
    return default if value is None else value


LLM_PROVIDER = _str("LLM_PROVIDER", "auto").lower()

OPENAI_API_KEY = _str("OPENAI_API_KEY", "")
OPENAI_MODEL = _str("OPENAI_MODEL", "gpt-4o-mini")

OPENROUTER_API_KEY = _str("OPENROUTER_API_KEY", "")
OPENROUTER_MODEL = _str("OPENROUTER_MODEL", "openai/gpt-4o-mini")
OPENROUTER_BASE_URL = _str("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
OPENROUTER_APP_URL = _str("OPENROUTER_APP_URL", "http://localhost:8501")
OPENROUTER_APP_NAME = _str("OPENROUTER_APP_NAME", "Smart Maintenance Assistant")

GROQ_API_KEY = _str("GROQ_API_KEY", "")
GROQ_MODEL = _str("GROQ_MODEL", "openai/gpt-oss-20b")
GROQ_BASE_URL = _str("GROQ_BASE_URL", "https://api.groq.com/openai/v1")

OLLAMA_BASE_URL = _str("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = _str("OLLAMA_MODEL", "llama3.2")
