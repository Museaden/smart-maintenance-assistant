"""Tests for src.config."""

from pathlib import Path

from src import config


def test_project_paths_exist_as_paths():
    assert isinstance(config.PROJECT_ROOT, Path)
    assert config.PROJECT_ROOT.is_dir()
    assert config.DATA_DIR.name == "documents"
    assert config.CHROMA_DIR.name == "chroma_db"


def test_collection_name():
    assert config.COLLECTION_NAME == "maintenance_docs"


def test_supported_extensions():
    assert ".pdf" in config.SUPPORTED_EXTENSIONS
    assert ".md" in config.SUPPORTED_EXTENSIONS
    assert ".txt" in config.SUPPORTED_EXTENSIONS


def test_defaults_are_positive_ints():
    assert config.TOP_K > 0
    assert config.CHUNK_SIZE > 0
    assert config.CHUNK_OVERLAP >= 0
    assert config.CHUNK_OVERLAP < config.CHUNK_SIZE


def test_int_env_helpers(monkeypatch):
    monkeypatch.setenv("TEST_INT_OK", "12")
    assert config._int_env("TEST_INT_OK", 1) == 12

    monkeypatch.setenv("TEST_INT_BAD", "not-a-number")
    assert config._int_env("TEST_INT_BAD", 7) == 7

    monkeypatch.delenv("TEST_INT_MISSING", raising=False)
    assert config._int_env("TEST_INT_MISSING", 3) == 3


def test_str_env_helpers(monkeypatch):
    monkeypatch.setenv("TEST_STR", "hello")
    assert config._str_env("TEST_STR", "default") == "hello"

    monkeypatch.delenv("TEST_STR_MISSING", raising=False)
    assert config._str_env("TEST_STR_MISSING", "default") == "default"
