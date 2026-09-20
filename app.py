"""
Smart Maintenance Assistant — Streamlit chat UI.

How the app works:
1. Load the embedding model (used to search documents)
2. Show system status in the sidebar
3. Let the user ask a question
4. Search the docs and show the answer with sources
"""

import os
import sys

# Hide download progress bars — they can crash Streamlit on Windows
os.environ["TQDM_DISABLE"] = "1"
os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"

# Streamlit re-runs this file often. Reload LLM settings so .env changes apply,
# but keep the embedding model in memory (reloading it is slow and can crash).
for name in list(sys.modules):
    reload = name in {"src.config", "src.llm", "src.llm_settings", "src.rag"}
    reload = reload or name.startswith(("src.llm", "src.config"))
    if reload:
        del sys.modules[name]

import streamlit as st

try:
    from src.embeddings import get_embedding_model
    from src.llm import get_llm_status, get_openrouter_limits
    from src.rag import ask
    from src.vector_store import collection_count
except Exception as import_error:
    st.error(f"Failed to load app modules: {import_error}")
    st.stop()


st.set_page_config(
    page_title="Smart Maintenance Assistant",
    page_icon="🔧",
    layout="wide",
)


@st.cache_resource
def load_embedding_model():
    """Load MiniLM once per server process (first run can take a minute)."""
    return get_embedding_model()


def show_sources(citations):
    """Show the document excerpts used for an answer."""
    if not citations:
        return

    with st.expander("Sources"):
        for item in citations:
            page = f", page {item.page}" if item.page else ""
            preview = item.text[:400]
            if len(item.text) > 400:
                preview += "..."

            st.markdown(
                f"**[{item.citation_id}]** `{item.source}`{page} "
                f"(relevance: {item.score:.0%})"
            )
            st.text(preview)


def show_sidebar():
    """Left panel: document count, how RAG works, and which LLM is active."""
    with st.sidebar:
        st.header("System Status")

        doc_count = collection_count()
        st.metric("Indexed chunks", doc_count)

        st.divider()
        st.markdown("**RAG Pipeline**")
        st.markdown(
            """
            1. Document parsing (PDF, TXT, MD)
            2. Chunking with overlap
            3. Local embeddings
            4. Chroma vector store
            5. Similarity search
            6. LLM response with citations
            """
        )

        st.divider()
        st.markdown("**Re-index documents**")
        st.code("python ingest.py --reset", language="bash")
        if doc_count == 0:
            st.warning("No documents indexed. Run `python ingest.py` first.")

        st.divider()
        show_llm_status()


def show_llm_status():
    """Show which AI provider is configured."""
    st.markdown("**LLM Provider**")
    status = get_llm_status()
    st.caption(f"Active: `{status['provider']}` · model `{status['model']}`")

    keys = []
    if status["openrouter_configured"]:
        keys.append("OpenRouter")
    if status["groq_configured"]:
        keys.append("Groq")
    if status["openai_configured"]:
        keys.append("OpenAI")

    if keys:
        st.success("Keys set: " + ", ".join(keys))
    elif not status.get("llm_configured"):
        st.error(
            "No LLM API key found. Answers will be raw excerpts only. "
            "Add GROQ_API_KEY or OPENROUTER_API_KEY to `.env` and restart."
        )
    else:
        st.info("No API keys — using Ollama or extractive mode.")

    if status["openrouter_configured"]:
        show_openrouter_limits()


def show_openrouter_limits():
    """Optional credit/usage info when OpenRouter is configured."""
    with st.expander("OpenRouter limits"):
        try:
            info = get_openrouter_limits()
            if not info:
                return
            remaining = info.get("limit_remaining")
            st.write(
                f"**Credits remaining:** "
                f"{remaining if remaining is not None else 'unlimited'}"
            )
            st.write(f"**Usage today:** {info.get('usage_daily')}")
            st.caption(
                "[OpenRouter limits docs]"
                "(https://openrouter.ai/docs/api-reference/limits)"
            )
        except Exception as error:
            st.warning(f"Could not fetch limits: {error}")


def show_past_messages():
    """Replay the conversation so far."""
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            show_sources(message.get("citations"))


def answer_question(question: str):
    """Search the docs, generate an answer, and save it in chat history."""
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Searching maintenance docs..."):
            response = ask(question)

        st.markdown(response.answer)
        show_sources(response.citations)

        if response.mode != "no_index":
            st.caption(f"Response mode: {response.mode}")

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response.answer,
            "citations": response.citations,
        }
    )


# --- run the app ---
with st.spinner("Loading embedding model (first time may take a minute)..."):
    load_embedding_model()

st.title("🔧 Smart Maintenance Assistant")
st.caption("Retrieval-Augmented AI for Predictive Maintenance Decision Support")

show_sidebar()
show_past_messages()

question = st.chat_input("Ask about maintenance procedures, thresholds, or risks...")
if question:
    answer_question(question)
