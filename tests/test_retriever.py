"""Tests for src.retriever."""

from unittest.mock import MagicMock, patch

import pytest

from src.retriever import SearchResult, search


def test_search_empty_collection_returns_empty():
    fake_collection = MagicMock()
    fake_collection.count.return_value = 0

    with patch("src.retriever.get_collection", return_value=fake_collection):
        assert search("anything") == []


def test_search_maps_chroma_results():
    fake_collection = MagicMock()
    fake_collection.count.return_value = 2
    fake_collection.query.return_value = {
        "documents": [["Pump vibration limit is 7.5 mm/s.", "Filter change every 90 days."]],
        "metadatas": [
            [
                {"source": "pump.md", "page": 1, "chunk_id": 0},
                {"source": "hvac.md", "page": -1, "chunk_id": 1},
            ]
        ],
        "distances": [[0.2, 0.4]],
    }

    with (
        patch("src.retriever.get_collection", return_value=fake_collection),
        patch("src.retriever.embed_query", return_value=[0.1, 0.2]),
    ):
        hits = search("vibration", top_k=2)

    assert len(hits) == 2
    assert isinstance(hits[0], SearchResult)
    assert hits[0].citation_id == 1
    assert hits[0].score == pytest.approx(0.8)
    assert hits[0].page == 1
    assert hits[1].page is None
    assert hits[1].source == "hvac.md"
