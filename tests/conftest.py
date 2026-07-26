"""Shared fixtures for Smart Maintenance Assistant tests."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

# Ensure project root is on sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.chunker import Chunk
from src.parsers import ParsedDocument


@pytest.fixture
def sample_text() -> str:
    return (
        "Pump-3 critical vibration threshold is 7.5 mm/s RMS. "
        "If vibration exceeds this level, schedule bearing inspection within 48 hours. "
        "Record readings in the CMMS work order before returning equipment to service."
    )


@pytest.fixture
def sample_document(sample_text: str) -> ParsedDocument:
    return ParsedDocument(source="pump_sop.md", text=sample_text, page=None)


@pytest.fixture
def sample_documents(sample_text: str) -> list[ParsedDocument]:
    return [
        ParsedDocument(source="pump_sop.md", text=sample_text, page=None),
        ParsedDocument(
            source="hvac_guide.md",
            text="HVAC Unit-7 filters must be replaced every 90 days or when differential pressure exceeds 1.5 inWG.",
            page=2,
        ),
    ]


@pytest.fixture
def sample_chunks() -> list[Chunk]:
    return [
        Chunk(
            text="Pump-3 critical vibration is 7.5 mm/s RMS.",
            source="pump_sop.md",
            page=None,
            chunk_id=0,
        ),
        Chunk(
            text="Replace HVAC Unit-7 filters every 90 days.",
            source="hvac_guide.md",
            page=1,
            chunk_id=0,
        ),
    ]


@pytest.fixture
def tmp_docs_dir(tmp_path: Path) -> Path:
    docs = tmp_path / "documents"
    docs.mkdir()
    (docs / "sample.md").write_text(
        "# Maintenance SOP\n\nMotor current above 20A requires inspection.\n",
        encoding="utf-8",
    )
    (docs / "notes.txt").write_text(
        "Bearing temperature above 80C is a warning condition.\n",
        encoding="utf-8",
    )
    (docs / "ignore.bin").write_bytes(b"\x00\x01\x02")
    return docs
