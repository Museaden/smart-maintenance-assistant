"""Smart Maintenance Assistant — RAG chatbot UI."""

import sys

# Force fresh imports when Streamlit hot-reloads (prevents stale src.config cache)
for _mod in list(sys.modules):
    if _mod == "src" or _mod.startswith("src."):
        del sys.modules[_mod]

import streamlit as st

try:
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

st.title("🔧 Smart Maintenance Assistant")
st.caption(
    "Retrieval-Augmented AI for Predictive Maintenance Decision Support"
)

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
    st.markdown("**LLM Provider**")
    llm = get_llm_status()
    st.caption(f"Active: `{llm['provider']}` · model `{llm['model']}`")

    configured = []
    if llm["openrouter_configured"]:
        configured.append("OpenRouter")
    if llm["groq_configured"]:
        configured.append("Groq")
    if llm["openai_configured"]:
        configured.append("OpenAI")
    if configured:
        st.success("Keys set: " + ", ".join(configured))
    elif not llm.get("llm_configured"):
        st.error(
            "No LLM API key found. Answers will be raw excerpts only. "
            "Add GROQ_API_KEY or OPENROUTER_API_KEY to `.env` and restart."
        )
    else:
        st.info("No API keys — using Ollama or extractive mode.")

    if llm["openrouter_configured"]:
        with st.expander("OpenRouter limits"):
            try:
                info = get_openrouter_limits()
                if info:
                    remaining = info.get("limit_remaining")
                    usage_daily = info.get("usage_daily")
                    st.write(f"**Credits remaining:** {remaining if remaining is not None else 'unlimited'}")
                    st.write(f"**Usage today:** {usage_daily}")
                    st.caption("[OpenRouter limits docs](https://openrouter.ai/docs/api-reference/limits)")
            except Exception as exc:
                st.warning(f"Could not fetch limits: {exc}")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message.get("citations"):
            with st.expander("Sources"):
                for c in message["citations"]:
                    loc = f", page {c.page}" if c.page else ""
                    st.markdown(
                        f"**[{c.citation_id}]** `{c.source}`{loc} "
                        f"(relevance: {c.score:.0%})"
                    )
                    st.text(c.text[:400] + ("..." if len(c.text) > 400 else ""))

if prompt := st.chat_input("Ask about maintenance procedures, thresholds, or risks..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Searching maintenance docs..."):
            response = ask(prompt)

        st.markdown(response.answer)

        if response.citations:
            with st.expander("Sources"):
                for c in response.citations:
                    loc = f", page {c.page}" if c.page else ""
                    st.markdown(
                        f"**[{c.citation_id}]** `{c.source}`{loc} "
                        f"(relevance: {c.score:.0%})"
                    )
                    st.text(c.text[:400] + ("..." if len(c.text) > 400 else ""))

        if response.mode != "no_index":
            st.caption(f"Response mode: {response.mode}")

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response.answer,
            "citations": response.citations,
        }
    )
