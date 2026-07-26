"""Local embedding generation with sentence-transformers."""

from __future__ import annotations

import os
import sys
from contextlib import contextmanager

# Must be set before importing transformers / tqdm
os.environ["TQDM_DISABLE"] = "1"
os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"
os.environ["TRANSFORMERS_NO_ADVISORY_WARNINGS"] = "1"
os.environ["HF_HUB_DISABLE_TELEMETRY"] = "1"

from .config import EMBEDDING_MODEL

# Survive Streamlit's "delete src.* modules" reload pattern in app.py
_CACHE_KEY = "_sma_embedding_model_cache"


class _QuietStream:
    """Ignore invalid flush/write on Streamlit-redirected stdout/stderr (Windows)."""

    def __init__(self, real):
        self._real = real

    def write(self, data):
        try:
            return self._real.write(data)
        except OSError:
            return len(data) if isinstance(data, (str, bytes)) else 0

    def flush(self):
        try:
            self._real.flush()
        except OSError:
            pass

    def isatty(self):
        return False

    def __getattr__(self, name):
        return getattr(self._real, name)


@contextmanager
def _quiet_stdio():
    old_out, old_err = sys.stdout, sys.stderr
    sys.stdout = _QuietStream(old_out)
    sys.stderr = _QuietStream(old_err)
    try:
        yield
    finally:
        sys.stdout = old_out
        sys.stderr = old_err


def _disable_progress_bars() -> None:
    try:
        from transformers.utils.logging import disable_progress_bar

        disable_progress_bar()
    except Exception:
        pass
    try:
        import tqdm as tqdm_mod

        def _disabled_tqdm(iterable=None, *args, **kwargs):
            return iterable if iterable is not None else []

        tqdm_mod.tqdm = _disabled_tqdm
        if hasattr(tqdm_mod, "std"):
            tqdm_mod.std.tqdm = _disabled_tqdm
        if hasattr(tqdm_mod, "auto"):
            tqdm_mod.auto.tqdm = _disabled_tqdm
        if hasattr(tqdm_mod, "asyncio"):
            tqdm_mod.asyncio.tqdm = _disabled_tqdm
    except Exception:
        pass


def get_embedding_model():
    """Return a cached SentenceTransformer (process-wide, Streamlit-safe)."""
    cache = sys.modules.setdefault(_CACHE_KEY, {})
    if "model" in cache:
        return cache["model"]

    _disable_progress_bars()
    with _quiet_stdio():
        from sentence_transformers import SentenceTransformer

        cache["model"] = SentenceTransformer(EMBEDDING_MODEL)
    return cache["model"]


def embed_texts(texts: list[str]) -> list[list[float]]:
    model = get_embedding_model()
    with _quiet_stdio():
        embeddings = model.encode(texts, show_progress_bar=False)
    return embeddings.tolist()


def embed_query(query: str) -> list[float]:
    return embed_texts([query])[0]
