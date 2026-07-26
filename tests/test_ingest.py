"""Tests for ingest.py."""

from pathlib import Path
from unittest.mock import patch

import pytest

from ingest import ingest


def test_ingest_missing_directory(tmp_path: Path):
    missing = tmp_path / "does_not_exist"
    with pytest.raises(FileNotFoundError):
        ingest(missing)


def test_ingest_no_documents(tmp_path: Path, capsys):
    empty = tmp_path / "empty"
    empty.mkdir()
    ingest(empty)
    captured = capsys.readouterr()
    assert "No supported documents" in captured.out


def test_ingest_happy_path(tmp_docs_dir: Path, capsys):
    with (
        patch("ingest.add_chunks", return_value=2) as mock_add,
        patch("ingest.collection_count", return_value=2),
        patch("ingest.reset_collection") as mock_reset,
    ):
        ingest(tmp_docs_dir, reset=True)

    mock_reset.assert_called_once()
    mock_add.assert_called_once()
    out = capsys.readouterr().out
    assert "Parsed" in out
    assert "chunk" in out.lower()
