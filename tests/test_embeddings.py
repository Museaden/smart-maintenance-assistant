"""Tests for src.embeddings (mocked model — no download)."""

from unittest.mock import MagicMock, patch

import numpy as np


def test_embed_texts_returns_list_of_vectors():
    fake_model = MagicMock()
    fake_model.encode.return_value = np.array([[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]])

    with patch("src.embeddings.get_embedding_model", return_value=fake_model):
        from src.embeddings import embed_texts

        result = embed_texts(["hello", "world"])

    assert len(result) == 2
    assert result[0] == [0.1, 0.2, 0.3]
    fake_model.encode.assert_called_once()


def test_embed_query_returns_single_vector():
    fake_model = MagicMock()
    fake_model.encode.return_value = np.array([[0.9, 0.8]])

    with patch("src.embeddings.get_embedding_model", return_value=fake_model):
        from src.embeddings import embed_query

        result = embed_query("pump vibration")

    assert result == [0.9, 0.8]
