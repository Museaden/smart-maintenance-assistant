# Smart Maintenance Assistant

**Retrieval-Augmented AI Chatbot for Predictive Maintenance Decision Support**

A RAG-powered chatbot that answers maintenance questions from your documentation with **cited, grounded responses**.

## Author & AI assistance

This project was developed with assistance from **Cursor (AI)** for parts of the coding and documentation. The author remains responsible for the overall project.

**AI assistance (Cursor) was used for:**

- Drafting and refining some application and test code
- Drafting project documentation (README, SRS, system architecture, CI/CD guide)
- Helping structure the evaluation benchmark and GitHub Actions workflow

**Author responsibilities:**

- Defining the project idea, goals, and predictive-maintenance use case
- Designing the RAG pipeline approach and choosing tools (Chroma, embeddings, Streamlit, LLM providers)
- Reviewing, testing, and validating all code and documentation
- Configuring the environment (`.env`, API keys, document ingest, app run)
- Running unit tests and the 20-question evaluation benchmark
- Owning final decisions on requirements, architecture, and portfolio presentation

## Architecture

```
Documents (PDF/TXT/MD)
        ↓
   Document Parsing
        ↓
   Text Chunking (overlap)
        ↓
   Embeddings (sentence-transformers)
        ↓
   Chroma Vector Database
        ↓
   Similarity Search (top-k)
        ↓
   LLM + Citations → Chat UI
```

Full design write-up: [docs/SYSTEM_ARCHITECTURE.md](docs/SYSTEM_ARCHITECTURE.md)  
Requirements (epics, user stories, journeys): [docs/SRS.md](docs/SRS.md)

## Features

- Document parsing (PDF, TXT, Markdown)
- Chunking with configurable size and overlap
- Local embeddings (`all-MiniLM-L6-v2`) — no API key required for indexing
- Chroma persistent vector database
- Cosine similarity search (top-k)
- LLM answers with inline citations `[1]`, `[2]`, etc.
- Streamlit chat UI with Sources expander and sidebar status
- Multi-provider LLM support: Groq, OpenRouter, OpenAI, Ollama (+ extractive fallback)
- Unit tests (`pytest`) and a 20-question evaluation benchmark
- GitHub Actions CI/CD workflow

## Quick Start

### 1. Install dependencies

```bash
cd smart-maintenance-assistant
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS / Linux
pip install -r requirements.txt
```

### 2. Add maintenance documents

Place PDF, TXT, or MD files in `data/documents/`. Sample SOPs are included.

### 3. Ingest documents into Chroma

```bash
python ingest.py --reset
```

### 4. Configure LLM

Copy `.env.example` to `.env`:

```bash
copy .env.example .env        # Windows
# cp .env.example .env        # macOS / Linux
```

**Option A — Groq (fast free tier):** [console.groq.com/keys](https://console.groq.com/keys)

```env
LLM_PROVIDER=groq
GROQ_API_KEY=gsk_...
GROQ_MODEL=llama-3.3-70b-versatile
```

**Option B — OpenRouter:** [openrouter.ai/keys](https://openrouter.ai/keys)

```env
LLM_PROVIDER=openrouter
OPENROUTER_API_KEY=sk-or-v1-...
OPENROUTER_MODEL=openai/gpt-4o-mini
```

**Option C — OpenAI:** set `OPENAI_API_KEY` in `.env`

**Option D — Ollama (local):** install [Ollama](https://ollama.com), run `ollama pull llama3.2`

**Option E — No LLM:** extractive mode shows retrieved excerpts with citations

Default `LLM_PROVIDER=auto` tries OpenRouter → Groq → OpenAI → Ollama.

### 5. Run the chatbot

```bash
streamlit run app.py
```

Open http://localhost:8501

## Example Questions

- What vibration level is critical for Pump-3?
- When should I replace HVAC Unit-7 filters?
- What indicates high bearing failure risk?
- What should I do if motor current exceeds 20A?

More evaluation questions: [evaluation_and_benchmarks/questions.md](evaluation_and_benchmarks/questions.md)

## Testing

```bash
pytest tests -q
```

Run one file:

```bash
pytest tests/test_rag.py -q
```

## Evaluation & Benchmarks

20 grounded questions with gold answers and keyword scoring:

```bash
python evaluation_and_benchmarks/run_benchmark.py
python evaluation_and_benchmarks/run_benchmark.py --limit 5
```

Results are saved under `evaluation_and_benchmarks/results/`.

## Learning notebook

Step-by-step RAG walkthrough:

- `rag_step_by_step.ipynb` — editable notebook  
- Select the project **venv** kernel before running cells

## CI / CD

Workflow: [`.github/workflows/ci-cd.yml`](.github/workflows/ci-cd.yml)

- **Test** — pytest + compile check + benchmark JSON validation (Python 3.11 & 3.12)
- **Deploy Notes** — Streamlit Cloud reminders after tests on `main`

Guide: [docs/CI_CD.md](docs/CI_CD.md)

## Project Structure

```
smart-maintenance-assistant/
├── app.py                          # Streamlit chat UI
├── ingest.py                       # Document ingestion CLI
├── data/documents/                 # Maintenance manuals & SOPs
├── chroma_db/                      # Persisted vector store (generated)
├── src/
│   ├── parsers.py                  # Document parsing
│   ├── chunker.py                  # Text chunking
│   ├── embeddings.py               # Sentence-transformer embeddings
│   ├── vector_store.py             # Chroma operations
│   ├── retriever.py                # Similarity search
│   ├── llm.py                      # Groq / OpenRouter / OpenAI / Ollama
│   ├── rag.py                      # Orchestration + citations
│   └── config.py                   # Settings from .env
├── tests/                          # Unit tests (pytest)
├── evaluation_and_benchmarks/      # 20-question RAG benchmark
├── docs/
│   ├── SRS.md                      # Software Requirements Specification
│   ├── SYSTEM_ARCHITECTURE.md      # System architecture
│   └── CI_CD.md                    # CI/CD guide
├── .github/workflows/ci-cd.yml     # GitHub Actions
├── rag_step_by_step.ipynb          # Pipeline tutorial notebook
├── .env.example                    # Config template
└── requirements.txt
```

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `LLM_PROVIDER` | auto | `openrouter`, `groq`, `openai`, `ollama`, or `auto` |
| `GROQ_API_KEY` | — | Groq API key |
| `GROQ_MODEL` | llama-3.3-70b-versatile | Groq model name |
| `OPENROUTER_API_KEY` | — | OpenRouter API key |
| `OPENROUTER_MODEL` | openai/gpt-4o-mini | Model ID on OpenRouter |
| `OPENAI_API_KEY` | — | OpenAI API key |
| `OLLAMA_MODEL` | llama3.2 | Local Ollama model |
| `EMBEDDING_MODEL` | all-MiniLM-L6-v2 | Local embedding model |
| `TOP_K` | 4 | Chunks retrieved per query |
| `CHUNK_SIZE` | 500 | Characters per chunk |
| `CHUNK_OVERLAP` | 50 | Overlap between chunks |

## Documentation

| Document | Description |
|----------|-------------|
| [docs/SRS.md](docs/SRS.md) | Epics, user stories, journeys, functional & non-functional requirements |
| [docs/SYSTEM_ARCHITECTURE.md](docs/SYSTEM_ARCHITECTURE.md) | C4 views, data flows, components, deployment |
| [docs/CI_CD.md](docs/CI_CD.md) | GitHub Actions and Streamlit Cloud deploy steps |
| [evaluation_and_benchmarks/README.md](evaluation_and_benchmarks/README.md) | How to run the 20-question benchmark |

## CV / Portfolio Highlights

- End-to-end RAG pipeline for industrial decision support
- Grounded answers with source citations (reduces hallucination)
- Works offline for embeddings and retrieval; optional cloud/local LLM
- Software requirements (SRS), architecture docs, tests, and evaluation suite
- Extensible toward CMMS integration, sensor dashboards, and failure prediction models
