"""Tests for src.parsers."""

from pathlib import Path

import pytest

from src.parsers import ParsedDocument, parse_directory, parse_file


def test_parse_markdown_file(tmp_docs_dir: Path):
    docs = parse_file(tmp_docs_dir / "sample.md")
    assert len(docs) == 1
    assert docs[0].source == "sample.md"
    assert "Motor current" in docs[0].text
    assert docs[0].page is None


def test_parse_txt_file(tmp_docs_dir: Path):
    docs = parse_file(tmp_docs_dir / "notes.txt")
    assert len(docs) == 1
    assert "Bearing temperature" in docs[0].text


def test_parse_unsupported_extension(tmp_path: Path):
    bad = tmp_path / "data.csv"
    bad.write_text("a,b,c\n", encoding="utf-8")
    with pytest.raises(ValueError, match="Unsupported"):
        parse_file(bad)


def test_parse_directory_skips_unsupported(tmp_docs_dir: Path):
    docs = parse_directory(tmp_docs_dir)
    sources = {d.source for d in docs}
    assert sources == {"sample.md", "notes.txt"}
    assert all(isinstance(d, ParsedDocument) for d in docs)


def test_parse_empty_directory(tmp_path: Path):
    empty = tmp_path / "empty"
    empty.mkdir()
    assert parse_directory(empty) == []
