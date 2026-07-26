# System Architecture

## Smart Maintenance Assistant

| Field | Value |
|-------|--------|
| **Document title** | System Architecture Document |
| **Product** | Smart Maintenance Assistant |
| **Version** | 1.0 |
| **Status** | Baseline |
| **Date** | July 2026 |
| **Related docs** | [SRS.md](./SRS.md), [README.md](../README.md) |

---

## 1. Purpose

This document describes the **logical and physical architecture** of the Smart Maintenance Assistant: a Retrieval-Augmented Generation (RAG) system that answers predictive-maintenance questions from plant documentation with cited, grounded responses.

It is intended for developers, reviewers, and portfolio evaluation.

---

## 2. Architectural goals and principles

| Goal | How the architecture supports it |
|------|----------------------------------|
| **Grounded answers** | Retrieve-then-generate; LLM sees only retrieved excerpts; citations required |
| **Local-first indexing** | Embeddings via `sentence-transformers` on-device; no API key for ingest |
| **Provider flexibility** | Pluggable LLM backends (Groq, OpenRouter, OpenAI, Ollama) + extractive fallback |
| **Modularity** | Clear pipeline stages in separate `src/` modules |
| **Demo readiness** | Single-machine deploy: CLI ingest + Streamlit UI |
| **Testability** | Pure logic separable from UI; heavy deps mockable in `tests/` |

**Design principles**

1. **Separation of concerns** — parsing, chunking, embedding, storage, retrieval, generation, and UI are distinct layers  
2. **Fail soft** — missing LLM → extractive mode; empty index → clear guidance  
3. **Configuration over code** — providers and tuning via `.env`  
4. **Traceability** — every answer can point back to source chunks  

---

## 3. System context (C4 Level 1)

```mermaid
flowchart LR
  Tech["Maintenance Technician"]
  Eng["Reliability Engineer"]
  Admin["System Admin"]

  SMA["Smart Maintenance Assistant\n(Streamlit + RAG pipeline)"]

  Docs[("Maintenance Docs\nPDF / TXT / MD")]
  Chroma[("Chroma Vector DB\nchroma_db/")]
  CloudLLM["Cloud LLM APIs\nGroq / OpenRouter / OpenAI"]
  Ollama["Ollama\n(local LLM)"]

  Tech -->|Ask questions| SMA
  Eng -->|Ask / verify citations| SMA
  Admin -->|Ingest & configure| SMA

  Admin -->|Place files| Docs
  SMA -->|Read & index| Docs
  SMA -->|Store / query embeddings| Chroma
  SMA -->|Generate answers| CloudLLM
  SMA -->|Generate answers| Ollama
```

**External actors**

| Actor | Interaction |
|-------|-------------|
| Technician / Engineer | Chat Q&A via browser |
| Admin | Document drop, `ingest.py`, `.env` keys |
| Cloud LLM | Optional chat-completion API |
| Ollama | Optional local chat API |
| Document corpus | Source of truth for procedures |

---

## 4. Container view (C4 Level 2)

```mermaid
flowchart TB
  subgraph UserMachine["Single host (developer / plant PC)"]
    Browser["Web Browser"]
    UI["Streamlit App\napp.py"]
    Ingest["Ingest CLI\ningest.py"]
    Core["RAG Core Library\nsrc/*"]
    VS[("Chroma Persistent Store\nchroma_db/")]
    Files[("data/documents/")]
    Env[".env configuration"]
  end

  Cloud["External LLM HTTPS APIs"]
  LocalLLM["Ollama HTTP :11434"]

  Browser <-->|HTTP localhost:8501| UI
  UI --> Core
  Ingest --> Core
  Core --> VS
  Ingest --> Files
  Core --> Files
  UI --> Env
  Ingest --> Env
  Core -->|optional| Cloud
  Core -->|optional| LocalLLM
```

| Container | Technology | Responsibility |
|-----------|------------|----------------|
| **Streamlit App** | Python, Streamlit | Chat UI, sidebar status, session message history |
| **Ingest CLI** | Python argparse | Batch parse → chunk → embed → upsert/reset Chroma |
| **RAG Core** | Python packages under `src/` | All pipeline logic |
| **Chroma DB** | chromadb PersistentClient | Vector + document + metadata persistence |
| **Documents** | Filesystem | Authoritative SOP/manual corpus |
| **Config** | python-dotenv | Secrets and tuning parameters |

---

## 5. Component view (C4 Level 3)

```mermaid
flowchart TB
  subgraph Presentation
    APP["app.py\nChat UI + sidebar"]
  end

  subgraph Application
    RAG["rag.py\nOrchestrator ask()"]
    LLM["llm.py\nProvider chain"]
    RET["retriever.py\nSimilarity search"]
  end

  subgraph Domain_Pipeline["Ingestion / Indexing"]
    PAR["parsers.py"]
    CHK["chunker.py"]
    EMB["embeddings.py"]
    VST["vector_store.py"]
    ING["ingest.py"]
  end

  subgraph CrossCutting
    CFG["config.py / llm_settings.py\n.env"]
  end

  APP --> RAG
  APP --> LLM
  APP --> VST
  RAG --> RET
  RAG --> LLM
  RET --> EMB
  RET --> VST
  ING --> PAR
  ING --> CHK
  ING --> VST
  VST --> EMB
  PAR --> CFG
  CHK --> CFG
  EMB --> CFG
  LLM --> CFG
  VST --> CFG
```

### 5.1 Component catalog

| Module | Role | Key outputs |
|--------|------|-------------|
| `parsers.py` | Load PDF/TXT/MD into `ParsedDocument` | Text + source + page |
| `chunker.py` | Split text with overlap & sensible separators | `Chunk` list |
| `embeddings.py` | Local MiniLM embeddings (LRU-cached model) | `list[float]` vectors |
| `vector_store.py` | Chroma get/create/add/reset/count | Persistent collection |
| `retriever.py` | Query embed + top-k cosine search | `SearchResult` + scores + citation ids |
| `llm.py` | Resolve provider; call OpenRouter/Groq/OpenAI/Ollama | Answer text + mode name |
| `rag.py` | Compose context; call LLM; extractive fallback | `RAGResponse` |
| `config.py` | Paths, chunk/top-k, provider env defaults | Runtime constants |
| `app.py` | Presentation & status | User-visible chat |
| `ingest.py` | Offline indexing entrypoint | Updated Chroma collection |

---

## 6. End-to-end data flows

### 6.1 Ingestion pipeline (write path)

```mermaid
sequenceDiagram
  participant Admin
  participant Ingest as ingest.py
  participant Parsers
  participant Chunker
  participant Embed as embeddings.py
  participant Chroma as vector_store / Chroma

  Admin->>Ingest: python ingest.py --reset
  Ingest->>Chroma: reset_collection() (optional)
  Ingest->>Parsers: parse_directory(data/documents)
  Parsers-->>Ingest: ParsedDocument[]
  Ingest->>Chunker: chunk_documents(...)
  Chunker-->>Ingest: Chunk[]
  loop batches of chunks
    Ingest->>Embed: embed_texts(batch)
    Embed-->>Ingest: vectors
    Ingest->>Chroma: collection.add(ids, docs, embeddings, metadatas)
  end
  Ingest-->>Admin: printed counts
```

**Transformations**

| Stage | Input | Output |
|-------|-------|--------|
| Parse | Files | Plain text sections |
| Chunk | Long text | ~`CHUNK_SIZE` overlapping pieces |
| Embed | Chunk text | Dense vectors (`all-MiniLM-L6-v2`) |
| Store | Text + vector + metadata | Durable Chroma records |

### 6.2 Query pipeline (read path)

```mermaid
sequenceDiagram
  participant User
  participant UI as app.py
  participant RAG as rag.py
  participant Ret as retriever.py
  participant Emb as embeddings.py
  participant Chroma
  participant LLM as llm.py

  User->>UI: Ask maintenance question
  UI->>RAG: ask(question)
  RAG->>Ret: search(question, top_k)
  Ret->>Emb: embed_query(question)
  Emb-->>Ret: query vector
  Ret->>Chroma: query(n_results=top_k)
  Chroma-->>Ret: docs, metadatas, distances
  Ret-->>RAG: SearchResult[] (score = 1 - distance)
  alt no hits
    RAG-->>UI: mode=no_index guidance
  else hits found
    RAG->>LLM: generate_answer(context + question)
    alt LLM success
      LLM-->>RAG: natural answer + provider mode
    else LLM unavailable
      RAG-->>UI: extractive fallback + setup note
    end
    RAG-->>UI: RAGResponse(answer, citations, mode)
  end
  UI-->>User: Markdown answer + Sources expander
```

### 6.3 LLM provider resolution

```mermaid
flowchart TD
  Start([generate_answer]) --> Resolve{LLM_PROVIDER}
  Resolve -->|forced| UseForced[Use named provider]
  Resolve -->|auto| TryOR{OpenRouter key valid?}
  TryOR -->|yes| OR[openrouter]
  TryOR -->|no| TryGroq{Groq key valid?}
  TryGroq -->|yes| Groq[groq]
  TryGroq -->|no| TryOA{OpenAI key valid?}
  TryOA -->|yes| OA[openai]
  TryOA -->|no| Ol[ollama]
  UseForced --> Chain[Build provider chain\nprimary then fallbacks]
  OR --> Chain
  Groq --> Chain
  OA --> Chain
  Ol --> Chain
  Chain --> Call[Try each until success]
  Call -->|all fail| Err[RuntimeError → rag extractive fallback]
  Call -->|success| Ok[Return text + mode]
```

Placeholder keys such as `your_groq_key_here` are treated as **unset**.

---

## 7. Logical layered architecture

```text
┌─────────────────────────────────────────────────────────┐
│  Presentation Layer                                      │
│  app.py (Streamlit) — chat, sidebar, sources UI          │
├─────────────────────────────────────────────────────────┤
│  Application / Orchestration Layer                       │
│  rag.py — ask(), context formatting, fallbacks           │
│  ingest.py — batch indexing workflow                     │
├─────────────────────────────────────────────────────────┤
│  Domain Services                                         │
│  retriever.py · llm.py · parsers · chunker · embeddings  │
├─────────────────────────────────────────────────────────┤
│  Infrastructure                                          │
│  vector_store.py (Chroma) · httpx/OpenAI SDK · dotenv    │
│  filesystem (data/documents, chroma_db)                  │
└─────────────────────────────────────────────────────────┘
```

---

## 8. Data architecture

### 8.1 Data stores

| Store | Type | Contents | Lifetime |
|-------|------|----------|----------|
| `data/documents/` | Files | Source SOPs/manuals | Durable, human-edited |
| `chroma_db/` | Embedded DB | Chunk text, embeddings, metadata | Durable until `--reset` |
| `.env` | Config file | API keys, models, chunk/top-k | Durable secrets (local) |
| Streamlit `session_state` | In-memory | Chat transcript for browser session | Ephemeral |

### 8.2 Chunk metadata schema

| Field | Type | Description |
|-------|------|-------------|
| `source` | string | Original filename |
| `page` | int | PDF page, or `-1` if N/A |
| `chunk_id` | int | Index within parent document section |
| Document id | string | `{source}::p{page}::c{chunk_id}::{index}` |

### 8.3 Runtime response model

```text
RAGResponse
├── answer: str          # Markdown shown to user
├── citations: SearchResult[]
│   ├── text, source, page, chunk_id
│   ├── score            # cosine similarity ≈ 1 - distance
│   └── citation_id      # 1-based [n] marker
└── mode: str            # e.g. groq | extractive | no_index
```

---

## 9. Deployment architecture

### 9.1 Local single-node (current)

```mermaid
flowchart LR
  subgraph Host["Windows / Linux / macOS"]
    Venv["Python venv"]
    ST["streamlit run app.py\n:8501"]
    CLI["ingest.py"]
    Disk["Local disk\ndocs + chroma_db + .env"]
  end
  Net["Internet (optional)\nLLM APIs"]
  Ol["Ollama (optional)\n:11434"]

  Venv --> ST
  Venv --> CLI
  ST --> Disk
  CLI --> Disk
  ST -.-> Net
  ST -.-> Ol
```

**Typical startup**

1. `python -m venv venv` → `pip install -r requirements.txt`  
2. Configure `.env`  
3. `python ingest.py --reset`  
4. `streamlit run app.py`  

### 9.2 Process view

| Process | When it runs | Notes |
|---------|--------------|-------|
| Ingest | On-demand CLI | Can run while UI is stopped; restart UI not required for Chroma reads after ingest completes |
| Streamlit | Long-running | Loads `.env` via modules; hot-reload may need restart after `.env` changes |
| Ollama | Optional daemon | Must be up if selected/fallback local provider |

### 9.3 Future deployment options (not implemented)

| Option | Use case |
|--------|----------|
| Docker Compose (app + Ollama + volume for chroma) | Reproducible plant PC install |
| Internal reverse proxy + auth | Multi-user trusted network |
| Separated ingest worker | Large corpus / scheduled re-index |

---

## 10. Cross-cutting concerns

### 10.1 Configuration

Centralized in `src/config.py` (and LLM helpers in `llm.py` / `llm_settings.py`):

| Variable | Affects |
|----------|---------|
| `EMBEDDING_MODEL` | Vector space (re-ingest required if changed) |
| `CHUNK_SIZE` / `CHUNK_OVERLAP` | Index granularity |
| `TOP_K` | Retrieval breadth |
| `LLM_PROVIDER` + `*_API_KEY` / `*_MODEL` | Generation backend |

### 10.2 Security

| Concern | Approach |
|---------|----------|
| API secrets | `.env` only; not hardcoded |
| Network exposure | Local Streamlit by default |
| Prompt safety | System prompt restricts answers to excerpts |
| Operational safety | Citations for human verification; NFR decision-support disclaimer |

### 10.3 Observability

| Signal | Where |
|--------|-------|
| Indexed chunk count | Sidebar metric |
| Active provider / model | Sidebar caption |
| Response mode | Caption under assistant message |
| Ingest logs | CLI stdout |
| OpenRouter limits | Optional sidebar expander |

### 10.4 Error handling strategy

| Condition | Behavior |
|-----------|----------|
| Empty Chroma | `mode=no_index` message |
| Invalid/missing LLM keys | Skip provider; try next; then extractive |
| LLM HTTP/runtime failure | Next provider in chain → extractive |
| Unsupported file type | Skip (directory) or raise (single file) |

---

## 11. Technology stack

| Layer | Choice | Rationale |
|-------|--------|-----------|
| UI | Streamlit | Fast chat prototype, low boilerplate |
| Language | Python 3.10+ | ML/RAG ecosystem |
| Embeddings | sentence-transformers MiniLM | Local, free, sufficient for SOP retrieval |
| Vector DB | Chroma | Persistent, simple Python API, cosine space |
| PDF | pypdf | Lightweight text extraction |
| LLM clients | OpenAI SDK (compatible) + httpx (Ollama) | One pattern for multiple hosts |
| Config | python-dotenv | Portable local secrets |
| Tests | pytest | Module isolation with mocks |

---

## 12. Quality attributes mapping

| Quality attribute | Architectural mechanism |
|-------------------|-------------------------|
| **Accuracy / trust** | RAG + citations + anti-hallucination system prompt |
| **Availability** | Extractive fallback when LLMs fail |
| **Maintainability** | Thin UI over modular `src/` pipeline |
| **Portability** | Pure Python + local Chroma files |
| **Performance** | Cached embedding model; batched ingest; small top-k |
| **Privacy** | Local embeddings; optional fully local Ollama path |
| **Testability** | `tests/` per module; mocks for Chroma/LLM/embeddings |

---

## 13. Repository structure (architecture map)

```text
smart-maintenance-assistant/
├── app.py                 # Presentation
├── ingest.py              # Write-path entrypoint
├── src/
│   ├── parsers.py         # Document I/O
│   ├── chunker.py         # Text segmentation
│   ├── embeddings.py      # Vectorization
│   ├── vector_store.py    # Persistence adapter
│   ├── retriever.py       # Read-path search
│   ├── llm.py             # Generation adapters
│   ├── rag.py             # Use-case orchestration
│   └── config.py          # Settings
├── data/documents/        # Knowledge corpus
├── chroma_db/             # Vector index (generated)
├── tests/                 # Architecture verification
├── docs/
│   ├── SRS.md
│   └── SYSTEM_ARCHITECTURE.md
└── requirements.txt
```

---

## 14. Architectural risks and mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Poor PDF text extraction | Empty/noisy chunks | Prefer MD/TXT; future OCR |
| Embedding model change without re-ingest | Bad retrieval | Document re-ingest requirement |
| Cloud LLM outage / rate limits | No generative answer | Provider chain + extractive mode |
| Stale index after SOP edit | Wrong thresholds | Admin journey: `--reset` re-ingest |
| Over-trust in AI answers | Safety incidents | Citations + decision-support disclaimer |

---

## 15. Summary

The Smart Maintenance Assistant follows a classic **RAG architecture** on a **single-node deployment**:

1. **Index** documents locally into Chroma with MiniLM embeddings  
2. **Retrieve** top-k similar chunks for each question  
3. **Generate** a cited answer via a configurable LLM, or show excerpts if none is available  
4. **Present** results in Streamlit with transparent sources  

This keeps the design simple enough for a portfolio demo while remaining extensible toward CMMS, sensors, and multi-user plant deployments described in the SRS roadmap.

---

*End of System Architecture Document — Smart Maintenance Assistant v1.0*
