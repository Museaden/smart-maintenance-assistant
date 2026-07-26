"""Tests for src.rag."""

from unittest.mock import patch

from src.rag import (
    RAGResponse,
    _format_context,
    _looks_like_maintenance_question,
    ask,
)
from src.retriever import SearchResult


def _hit(text: str = "Pump-3 critical vibration is 7.5 mm/s.", score: float = 0.9) -> SearchResult:
    return SearchResult(
        text=text,
        source="pump.md",
        page=1,
        chunk_id=0,
        score=score,
        citation_id=1,
    )


def test_looks_like_maintenance_question():
    assert _looks_like_maintenance_question("What vibration for Pump-3?") is True
    assert _looks_like_maintenance_question("What is the weather?") is False


def test_format_context_includes_citation_ids():
    ctx = _format_context([_hit()])
    assert "[1]" in ctx
    assert "pump.md" in ctx
    assert "7.5 mm/s" in ctx


def test_ask_no_index():
    with patch("src.rag.search", return_value=[]):
        response = ask("Any question")

    assert isinstance(response, RAGResponse)
    assert response.mode == "no_index"
    assert "ingest.py" in response.answer
    assert response.citations == []


def test_ask_uses_llm_when_available():
    with (
        patch("src.rag.search", return_value=[_hit()]),
        patch("src.rag.generate_answer", return_value=("Critical limit is 7.5 [1]", "groq")),
    ):
        response = ask("What is critical vibration for Pump-3?")

    assert response.mode == "groq"
    assert "7.5" in response.answer
    assert len(response.citations) == 1


def test_ask_extractive_fallback_when_no_llm():
    with (
        patch("src.rag.search", return_value=[_hit(score=0.9)]),
        patch("src.rag.generate_answer", side_effect=RuntimeError("No LLM")),
        patch("src.rag.is_llm_configured", return_value=False),
    ):
        response = ask("What vibration level is critical for Pump-3?")

    assert response.mode == "extractive"
    assert "No LLM is configured" in response.answer or "7.5" in response.answer
