"""Local embedding generation with sentence-transformers."""

from functools import lru_cache

from sentence_transformers import SentenceTransformer

from .config import EMBEDDING_MODEL


@lru_cache(maxsize=1)
def get_embedding_model() -> SentenceTransformer:
    return SentenceTransformer(EMBEDDING_MODEL)


def embed_texts(texts: list[str]) -> list[list[float]]:
    model = get_embedding_model()
    embeddings = model.encode(texts, show_progress_bar=len(texts) > 10)
    return embeddings.tolist()


def embed_query(query: str) -> list[float]:
    return embed_texts([query])[0]
