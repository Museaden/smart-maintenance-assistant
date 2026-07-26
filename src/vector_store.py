"""Chroma vector database for maintenance document chunks."""

from __future__ import annotations

from typing import TYPE_CHECKING

import chromadb
from chromadb.config import Settings
from chromadb.errors import NotFoundError

from .chunker import Chunk
from .config import CHROMA_DIR, COLLECTION_NAME
from .embeddings import embed_texts

if TYPE_CHECKING:
    from chromadb.api import ClientAPI


def get_client() -> chromadb.PersistentClient:
    CHROMA_DIR.mkdir(parents=True, exist_ok=True)
    return chromadb.PersistentClient(
        path=str(CHROMA_DIR),
        settings=Settings(anonymized_telemetry=False),
    )


def get_collection(client: ClientAPI | None = None):
    client = client or get_client()
    return client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )


def add_chunks(chunks: list[Chunk], batch_size: int = 64) -> int:
    if not chunks:
        return 0

    collection = get_collection()
    added = 0

    for i in range(0, len(chunks), batch_size):
        batch = chunks[i : i + batch_size]
        texts = [c.text for c in batch]
        embeddings = embed_texts(texts)
        ids = [_chunk_doc_id(c, i + j) for j, c in enumerate(batch)]
        metadatas = [
            {
                "source": c.source,
                "page": c.page if c.page is not None else -1,
                "chunk_id": c.chunk_id,
            }
            for c in batch
        ]
        collection.add(
            ids=ids,
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas,
        )
        added += len(batch)

    return added


def collection_count() -> int:
    return get_collection().count()


def reset_collection() -> None:
    client = get_client()
    try:
        client.delete_collection(COLLECTION_NAME)
    except (ValueError, NotFoundError):
        pass
    get_collection(client)


def _chunk_doc_id(chunk: Chunk, index: int) -> str:
    page = chunk.page if chunk.page is not None else 0
    return f"{chunk.source}::p{page}::c{chunk.chunk_id}::{index}"
