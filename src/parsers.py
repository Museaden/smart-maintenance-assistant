"""Document parsing for maintenance manuals and SOPs."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from pypdf import PdfReader

from .config import SUPPORTED_EXTENSIONS


@dataclass
class ParsedDocument:
    source: str
    text: str
    page: int | None = None


def parse_file(path: Path) -> list[ParsedDocument]:
    suffix = path.suffix.lower()
    if suffix not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"Unsupported file type: {suffix}")

    if suffix == ".pdf":
        return _parse_pdf(path)
    return [_parse_text_file(path)]


def _parse_pdf(path: Path) -> list[ParsedDocument]:
    reader = PdfReader(str(path))
    pages: list[ParsedDocument] = []
    for i, page in enumerate(reader.pages, start=1):
        text = (page.extract_text() or "").strip()
        if text:
            pages.append(ParsedDocument(source=path.name, text=text, page=i))
    return pages


def _parse_text_file(path: Path) -> ParsedDocument:
    text = path.read_text(encoding="utf-8", errors="replace").strip()
    return ParsedDocument(source=path.name, text=text, page=None)


def parse_directory(directory: Path) -> list[ParsedDocument]:
    documents: list[ParsedDocument] = []
    for path in sorted(directory.rglob("*")):
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS:
            documents.extend(parse_file(path))
    return documents
