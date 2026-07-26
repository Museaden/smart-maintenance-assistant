"""RAG pipeline: retrieve context and generate cited LLM responses."""

from dataclasses import dataclass

from .config import TOP_K
from .llm import generate_answer, is_llm_configured
from .retriever import SearchResult, search

# Below this relevance score, retrieved chunks are likely off-topic
RELEVANCE_THRESHOLD = 0.35

MAINTENANCE_HINTS = (
    "pump", "motor", "hvac", "bearing", "vibration", "filter", "maintenance",
    "compressor", "conveyor", "chiller", "boiler", "loto", "inspection",
    "failure", "temperature", "pressure", "gearbox", "hydraulic", "transformer",
    "pm-", "sop", "risk", "replace", "service", "equipment", "machine",
)


@dataclass
class RAGResponse:
    answer: str
    citations: list[SearchResult]
    mode: str


def ask(question: str, top_k: int = TOP_K) -> RAGResponse:
    citations = search(question, top_k=top_k)
    if not citations:
        return RAGResponse(
            answer=(
                "No maintenance documents are indexed yet. "
                "Run `python ingest.py` to load documents into Chroma, then try again."
            ),
            citations=[],
            mode="no_index",
        )

    context = _format_context(citations)
    answer, mode = _generate_answer(question, context, citations)
    return RAGResponse(answer=answer, citations=citations, mode=mode)


def _format_context(citations: list[SearchResult]) -> str:
    blocks = []
    for c in citations:
        loc = f", page {c.page}" if c.page else ""
        blocks.append(f"[{c.citation_id}] Source: {c.source}{loc}\n{c.text}")
    return "\n\n".join(blocks)


def _looks_like_maintenance_question(question: str) -> bool:
    q = question.lower()
    return any(hint in q for hint in MAINTENANCE_HINTS)


def _generate_answer(
    question: str,
    context: str,
    citations: list[SearchResult],
) -> tuple[str, str]:
    user_prompt = f"""Maintenance documentation excerpts:
{context}

User question: {question}

Provide a helpful answer with inline citations like [1], [2]."""

    try:
        return generate_answer(user_prompt)
    except RuntimeError:
        pass

    return _extractive_fallback(question, context, citations), "extractive"


def _extractive_fallback(
    question: str,
    context: str,
    citations: list[SearchResult],
) -> str:
    best_score = citations[0].score if citations else 0.0
    q_lower = question.lower()

    # Personal / off-topic questions
    personal_phrases = ("my name", "who am i", "what is my name", "do you know me")
    if any(p in q_lower for p in personal_phrases):
        return (
            "No — I'm the **Smart Maintenance Assistant**. I answer questions about "
            "equipment maintenance using your plant documentation. I don't have access "
            "to personal information such as your name.\n\n"
            "**Example questions:**\n"
            "- What vibration level is critical for Pump-3?\n"
            "- When should HVAC Unit-7 filters be replaced?\n\n"
            + _llm_setup_note()
        )

    if not is_llm_configured():
        if not _looks_like_maintenance_question(question) or best_score < RELEVANCE_THRESHOLD:
            return (
                "I couldn't find a strong match in the maintenance documentation for "
                f"that question (best relevance: {best_score:.0%}).\n\n"
                "I'm designed for **predictive maintenance** topics — pumps, motors, "
                "HVAC, bearings, SOPs, and inspection procedures.\n\n"
                + _llm_setup_note()
            )

        return (
            f"**Question:** {question}\n\n"
            "⚠️ **No LLM is configured** — I can only show raw document excerpts "
            "instead of a natural-language answer.\n\n"
            f"{context}\n\n"
            + _llm_setup_note()
        )

    # Ollama configured but unreachable
    return (
        f"**Question:** {question}\n\n"
        "Could not reach an LLM (Ollama may not be running). "
        "Showing the closest documentation excerpts:\n\n"
        f"{context}\n\n"
        "Start Ollama, or add `GROQ_API_KEY` / `OPENROUTER_API_KEY` to `.env`."
    )


def _llm_setup_note() -> str:
    return (
        "**To get natural-language answers**, create a `.env` file in the project folder:\n\n"
        "```\n"
        "LLM_PROVIDER=groq\n"
        "GROQ_API_KEY=gsk_your_key_here\n"
        "```\n\n"
        "Free Groq key: https://console.groq.com/keys  \n"
        "Then restart: `streamlit run app.py`"
    )
