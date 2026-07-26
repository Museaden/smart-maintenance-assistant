"""Similarity search over the Chroma vector store."""

from dataclasses import dataclass

from .config import TOP_K
from .embeddings import embed_query
from .vector_store import get_collection


@dataclass
class SearchResult:
    text: str
    source: str
    page: int | None
    chunk_id: int
    score: float
    citation_id: int


def search(query: str, top_k: int = TOP_K) -> list[SearchResult]:
    collection = get_collection()
    if collection.count() == 0:
        return []

    query_embedding = embed_query(query)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(top_k, collection.count()),
        include=["documents", "metadatas", "distances"],
    )

    hits: list[SearchResult] = []
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    for i, (doc, meta, distance) in enumerate(zip(documents, metadatas, distances)):
        page = meta.get("page", -1)
        hits.append(
            SearchResult(
                text=doc,
                source=meta["source"],
                page=page if page >= 0 else None,
                chunk_id=meta["chunk_id"],
                score=1 - distance,
                citation_id=i + 1,
            )
        )
    return hits
