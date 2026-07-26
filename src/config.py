from pathlib import Path

from dotenv import load_dotenv
import os

load_dotenv(encoding="utf-8")

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "documents"
CHROMA_DIR = PROJECT_ROOT / "chroma_db"
COLLECTION_NAME = "maintenance_docs"


def _int_env(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None or value.strip() == "":
        return default
    try:
        return int(value)
    except ValueError:
        return default


def _str_env(name: str, default: str) -> str:
    value = os.getenv(name)
    return default if value is None else value


EMBEDDING_MODEL = _str_env("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
TOP_K = _int_env("TOP_K", 4)
CHUNK_SIZE = _int_env("CHUNK_SIZE", 500)
CHUNK_OVERLAP = _int_env("CHUNK_OVERLAP", 50)

OPENAI_API_KEY = _str_env("OPENAI_API_KEY", "")
OPENAI_MODEL = _str_env("OPENAI_MODEL", "gpt-4o-mini")

# LLM provider: auto | openrouter | groq | openai | ollama
LLM_PROVIDER = _str_env("LLM_PROVIDER", "auto").lower()

# OpenRouter - https://openrouter.ai/docs/api-reference/limits
OPENROUTER_API_KEY = _str_env("OPENROUTER_API_KEY", "")
OPENROUTER_MODEL = _str_env("OPENROUTER_MODEL", "openai/gpt-4o-mini")
OPENROUTER_BASE_URL = _str_env("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
OPENROUTER_APP_URL = _str_env("OPENROUTER_APP_URL", "http://localhost:8501")
OPENROUTER_APP_NAME = _str_env("OPENROUTER_APP_NAME", "Smart Maintenance Assistant")

# Groq - https://console.groq.com/docs/rate-limits
GROQ_API_KEY = _str_env("GROQ_API_KEY", "")
GROQ_MODEL = _str_env("GROQ_MODEL", "llama-3.3-70b-versatile")
GROQ_BASE_URL = _str_env("GROQ_BASE_URL", "https://api.groq.com/openai/v1")

OLLAMA_BASE_URL = _str_env("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = _str_env("OLLAMA_MODEL", "llama3.2")

SUPPORTED_EXTENSIONS = {".pdf", ".txt", ".md", ".html"}
