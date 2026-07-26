"""Tests for src.vector_store."""

from unittest.mock import MagicMock, patch

from src.chunker import Chunk
from src.vector_store import _chunk_doc_id, add_chunks


def test_chunk_doc_id_format():
    chunk = Chunk(text="x", source="sop.md", page=2, chunk_id=3)
    assert _chunk_doc_id(chunk, 10) == "sop.md::p2::c3::10"

    no_page = Chunk(text="y", source="a.txt", page=None, chunk_id=0)
    assert _chunk_doc_id(no_page, 0) == "a.txt::p0::c0::0"


def test_add_chunks_empty_returns_zero():
    assert add_chunks([]) == 0


def test_add_chunks_calls_collection(sample_chunks: list[Chunk]):
    fake_collection = MagicMock()
    fake_embeddings = [[0.1, 0.2], [0.3, 0.4]]

    with (
        patch("src.vector_store.get_collection", return_value=fake_collection),
        patch("src.vector_store.embed_texts", return_value=fake_embeddings),
    ):
        added = add_chunks(sample_chunks)

    assert added == 2
    fake_collection.add.assert_called_once()
    kwargs = fake_collection.add.call_args.kwargs
    assert len(kwargs["ids"]) == 2
    assert kwargs["documents"][0] == sample_chunks[0].text
