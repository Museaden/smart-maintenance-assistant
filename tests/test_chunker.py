"""Tests for src.chunker."""

from src.chunker import Chunk, _find_split_point, _split_text, chunk_documents
from src.parsers import ParsedDocument


def test_chunk_short_document(sample_document: ParsedDocument):
    chunks = chunk_documents([sample_document], chunk_size=500, chunk_overlap=50)
    assert len(chunks) == 1
    assert isinstance(chunks[0], Chunk)
    assert chunks[0].source == "pump_sop.md"
    assert chunks[0].chunk_id == 0


def test_chunk_long_text_creates_multiple_chunks():
    text = ("Sentence about pump vibration. " * 40).strip()
    docs = [ParsedDocument(source="long.md", text=text, page=1)]
    chunks = chunk_documents(docs, chunk_size=100, chunk_overlap=20)
    assert len(chunks) > 1
    assert all(c.source == "long.md" for c in chunks)
    assert [c.chunk_id for c in chunks] == list(range(len(chunks)))


def test_chunk_overlap_advances():
    text = "A" * 200
    parts = _split_text(text, chunk_size=80, chunk_overlap=20)
    assert len(parts) >= 2
    # Each piece should be at most chunk_size (after strip of empties)
    assert all(len(p) <= 80 for p in parts)


def test_split_empty_text():
    assert _split_text("   ", chunk_size=50, chunk_overlap=10) == []


def test_find_split_point_prefers_paragraph():
    text = "First paragraph.\n\nSecond paragraph continues here."
    end = _find_split_point(text, 0, 30, ["\n\n", "\n", ". ", " "])
    assert end > 0
