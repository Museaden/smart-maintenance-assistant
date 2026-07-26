"""Text chunking with overlap for retrieval."""

from dataclasses import dataclass

from .config import CHUNK_OVERLAP, CHUNK_SIZE
from .parsers import ParsedDocument


@dataclass
class Chunk:
    text: str
    source: str
    page: int | None
    chunk_id: int


def chunk_documents(
    documents: list[ParsedDocument],
    chunk_size: int = CHUNK_SIZE,
    chunk_overlap: int = CHUNK_OVERLAP,
) -> list[Chunk]:
    chunks: list[Chunk] = []
    for doc in documents:
        doc_chunks = _split_text(doc.text, chunk_size, chunk_overlap)
        for i, text in enumerate(doc_chunks):
            chunks.append(
                Chunk(text=text, source=doc.source, page=doc.page, chunk_id=i)
            )
    return chunks


def _split_text(text: str, chunk_size: int, chunk_overlap: int) -> list[str]:
    if len(text) <= chunk_size:
        return [text] if text.strip() else []

    separators = ["\n\n", "\n", ". ", " "]
    chunks: list[str] = []
    start = 0

    while start < len(text):
        end = min(start + chunk_size, len(text))
        if end < len(text):
            split_at = _find_split_point(text, start, end, separators)
            if split_at > start:
                end = split_at

        piece = text[start:end].strip()
        if piece:
            chunks.append(piece)

        if end >= len(text):
            break
        start = max(end - chunk_overlap, start + 1)

    return chunks


def _find_split_point(text: str, start: int, end: int, separators: list[str]) -> int:
    window = text[start:end]
    best_idx = -1
    best_sep = ""
    for sep in separators:
        idx = window.rfind(sep)
        if idx > best_idx:
            best_idx = idx
            best_sep = sep
    if best_idx > 0:
        return start + best_idx + len(best_sep)
    return end
