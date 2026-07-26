# Software Requirements Specification (SRS)

## Smart Maintenance Assistant

| Field | Value |
|-------|--------|
| **Document title** | Software Requirements Specification |
| **Product** | Smart Maintenance Assistant |
| **Version** | 1.0 |
| **Status** | Baseline |
| **Date** | July 2026 |
| **Audience** | Product owners, developers, QA, portfolio reviewers |

---

## 1. Introduction

### 1.1 Purpose

This Software Requirements Specification (SRS) defines the functional and non-functional requirements for the **Smart Maintenance Assistant**, a Retrieval-Augmented Generation (RAG) chatbot that helps maintenance personnel answer equipment and procedure questions using plant documentation, with cited, grounded responses.

### 1.2 Scope

**In scope**

- Ingesting maintenance documents (PDF, TXT, Markdown)
- Chunking, embedding, and storing documents in a vector database
- Natural-language Q&A over indexed documentation
- Inline citations and source expanders
- Multi-provider LLM support (OpenRouter, Groq, OpenAI, Ollama) with extractive fallback
- Streamlit chat UI and CLI ingestion
- Automated unit/integration-style tests for core modules

**Out of scope (current release)**

- Live CMMS / ERP integration
- Real-time IoT sensor ingestion or dashboards
- User authentication / multi-tenant access control
- Mobile native apps
- Automated work-order creation
- Multilingual UI localization (beyond English documentation content)

### 1.3 Definitions and acronyms

| Term | Definition |
|------|------------|
| **RAG** | Retrieval-Augmented Generation — retrieve relevant docs, then generate an answer |
| **LLM** | Large Language Model used to compose natural-language answers |
| **SOP** | Standard Operating Procedure |
| **CMMS** | Computerized Maintenance Management System |
| **Chunk** | Segment of document text stored and retrieved independently |
| **Citation** | Reference `[n]` linking an answer claim to a retrieved excerpt |
| **Extractive mode** | Fallback that shows raw retrieved excerpts when no LLM is available |
| **Embedding** | Numeric vector representation of text for similarity search |

### 1.4 References

- Project README (`README.md`)
- Architecture modules under `src/`
- Automated tests under `tests/`
- Configuration via `.env` / `.env.example`

---

## 2. Overall description

### 2.1 Product perspective

The system is a standalone desktop/local web application. It consists of:

1. **Ingestion pipeline** (`ingest.py`) — parse → chunk → embed → Chroma  
2. **RAG engine** (`src/rag.py`, `src/retriever.py`, `src/llm.py`)  
3. **Chat UI** (`app.py` — Streamlit)  
4. **Persistent store** (`chroma_db/`)  
5. **Document corpus** (`data/documents/`)

```
Documents → Parse → Chunk → Embed → Chroma
                                      ↓
User question → Embed query → Similarity search (top-k)
                                      ↓
                         LLM (+ citations) or extractive fallback
                                      ↓
                              Streamlit Chat UI
```

### 2.2 User classes / personas

| Persona | Role | Goals | Tech comfort |
|---------|------|-------|--------------|
| **Maintenance Technician** | Frontline worker | Quickly find thresholds, steps, and risks while on the floor | Low–medium |
| **Reliability Engineer** | Analysis & PM planning | Verify procedures and failure indicators with sources | Medium–high |
| **Maintenance Supervisor** | Oversight | Ensure team answers are grounded in approved SOPs | Medium |
| **System Administrator** | Setup & ops | Install deps, configure LLM keys, re-index docs | High |
| **Portfolio Reviewer / Evaluator** | Assessment | Understand architecture, requirements, and testability | Varied |

### 2.3 Operating environment

- **OS:** Windows 10/11 (primary); Linux/macOS compatible via Python  
- **Runtime:** Python 3.10+ virtual environment  
- **UI:** Browser via Streamlit (local, typically `localhost:8501`)  
- **Optional services:** Groq / OpenRouter / OpenAI APIs, or local Ollama  

### 2.4 Assumptions and dependencies

- Source documents are text-extractable (scanned PDFs without OCR may yield empty text)
- At least one document exists in `data/documents/` before useful Q&A
- For generative answers, either a valid cloud API key or a running Ollama instance is available
- Embeddings run locally (`sentence-transformers`); no API key required for indexing
- Users trust the document corpus as the source of truth for maintenance decisions

### 2.5 Constraints

- Answers must be grounded in retrieved documentation (no inventing specs)
- API keys must not be committed to source control (use `.env`)
- Local prototype; not hardened for public internet exposure

---

## 3. Epics

Epics group related capabilities into delivery themes.

| Epic ID | Epic name | Description | Priority |
|---------|-----------|-------------|----------|
| **E1** | Document ingestion | Enable admins to load and refresh maintenance documentation into the vector store | Must |
| **E2** | Semantic retrieval | Find the most relevant document chunks for a user question | Must |
| **E3** | Grounded Q&A | Generate (or extract) answers with citations from retrieved context | Must |
| **E4** | Chat experience | Provide an interactive chat UI with system status and source inspection | Must |
| **E5** | LLM provider flexibility | Support multiple LLM providers and graceful degradation | Should |
| **E6** | Quality & maintainability | Provide automated tests and clear configuration | Should |
| **E7** | Future plant integration | Prepare for CMMS/sensor extensions (roadmap) | Could |

---

## 4. User stories

Format: *As a [persona], I want [capability], so that [benefit].*

### Epic E1 — Document ingestion

| ID | User story | Acceptance criteria (summary) | Priority |
|----|------------|-------------------------------|----------|
| **US-1.1** | As an **Admin**, I want to place PDF/TXT/MD files in a documents folder, so that the system can use our plant SOPs. | Supported extensions only; unsupported files skipped or rejected | Must |
| **US-1.2** | As an **Admin**, I want to run `python ingest.py --reset`, so that I can rebuild the index after document updates. | Collection reset optional; chunk count reported | Must |
| **US-1.3** | As an **Admin**, I want parsing to preserve source filename (and PDF page when available), so that citations are traceable. | Metadata includes `source`, `page`, `chunk_id` | Must |

### Epic E2 — Semantic retrieval

| ID | User story | Acceptance criteria (summary) | Priority |
|----|------------|-------------------------------|----------|
| **US-2.1** | As a **Technician**, I want relevant SOP excerpts retrieved for my question, so that I see the right procedure. | Top-k cosine similarity search returns ranked hits | Must |
| **US-2.2** | As a **Reliability Engineer**, I want relevance scores and sources, so that I can judge answer quality. | UI/API exposes score, source, page | Should |

### Epic E3 — Grounded Q&A

| ID | User story | Acceptance criteria (summary) | Priority |
|----|------------|-------------------------------|----------|
| **US-3.1** | As a **Technician**, I want a clear natural-language answer with citations `[1]`, `[2]`, so that I can act quickly and verify the source. | LLM answer uses only provided excerpts; cites indices | Must |
| **US-3.2** | As a **Supervisor**, I want the system to admit when docs don’t cover a question, so that we avoid unsafe guesses. | Explicit “not enough information” behavior when context is weak | Must |
| **US-3.3** | As a **Technician**, I want useful excerpts even if no LLM key is configured, so that I can still look up procedures. | Extractive fallback with setup guidance | Should |

### Epic E4 — Chat experience

| ID | User story | Acceptance criteria (summary) | Priority |
|----|------------|-------------------------------|----------|
| **US-4.1** | As a **Technician**, I want a chat box to ask maintenance questions, so that interaction feels natural. | Streamlit chat input + message history | Must |
| **US-4.2** | As a **Technician**, I want an expandable Sources panel, so that I can read the underlying excerpt. | Expander lists citation id, source, page, relevance, snippet | Must |
| **US-4.3** | As an **Admin**, I want sidebar status (chunk count, LLM provider), so that I know if the system is ready. | Metrics + key/provider status messages | Should |

### Epic E5 — LLM provider flexibility

| ID | User story | Acceptance criteria (summary) | Priority |
|----|------------|-------------------------------|----------|
| **US-5.1** | As an **Admin**, I want to configure Groq/OpenRouter/OpenAI/Ollama via `.env`, so that I can choose cost/privacy tradeoffs. | Provider auto-detect or forced via `LLM_PROVIDER` | Must |
| **US-5.2** | As an **Admin**, I want placeholder keys ignored, so that misconfiguration fails safely into fallback. | Placeholder strings treated as unset | Must |

### Epic E6 — Quality & maintainability

| ID | User story | Acceptance criteria (summary) | Priority |
|----|------------|-------------------------------|----------|
| **US-6.1** | As a **Developer**, I want unit tests per module, so that regressions are caught early. | `pytest tests` runs offline with mocks where needed | Should |
| **US-6.2** | As a **Developer**, I want configurable chunk size, overlap, and top-k, so that retrieval can be tuned. | Env vars documented in README/SRS | Should |

---

## 5. User journeys

### Journey J1 — First-time setup (Admin)

**Goal:** Get the assistant running with documents and an LLM.

| Step | Actor action | System response |
|------|--------------|-----------------|
| 1 | Create venv and install `requirements.txt` | Dependencies available |
| 2 | Copy `.env.example` → `.env` and set `GROQ_API_KEY` (or other) | Config loaded on app start |
| 3 | Add SOP files under `data/documents/` | Files ready for ingest |
| 4 | Run `python ingest.py --reset` | Parses, chunks, embeds, stores; prints counts |
| 5 | Run `streamlit run app.py` | Chat UI opens; sidebar shows chunk count and “Keys set: Groq” |
| 6 | Ask a sample question (e.g., Pump-3 vibration) | Cited answer appears |

**Success:** Sidebar shows indexed chunks > 0 and LLM configured; answers include citations.  
**Failure paths:** Missing docs → warning; missing API key → extractive mode / setup note.

---

### Journey J2 — Floor lookup during troubleshooting (Technician)

**Goal:** Find the critical threshold and next action for abnormal equipment behavior.

| Step | Actor action | System response |
|------|--------------|-----------------|
| 1 | Opens chat UI on a workshop PC/tablet browser | Chat ready |
| 2 | Types: “What vibration level is critical for Pump-3?” | Spinner: searching docs |
| 3 | Reads concise answer with `[1]` citation | Actionable threshold + source |
| 4 | Expands **Sources** | Sees excerpt, filename, relevance |
| 5 | Follows SOP action (e.g., inspect bearings) | *(outside system)* |

**Success:** Answer grounded in plant docs within seconds; technician can verify source.  
**Failure paths:** Empty index → prompt to run ingest; off-topic question → guidance toward maintenance topics / low-relevance message.

---

### Journey J3 — Document refresh after SOP revision (Admin + Engineer)

**Goal:** Keep answers aligned after a procedure update.

| Step | Actor action | System response |
|------|--------------|-----------------|
| 1 | Reliability Engineer updates `compressor_sop.md` | File changed on disk |
| 2 | Admin runs `python ingest.py --reset` | Old collection cleared; new chunks indexed |
| 3 | Engineer asks a question about the changed limit | Answer reflects new content |
| 4 | Engineer checks Sources expander | Confirms revised excerpt |

**Success:** Post-ingest answers match the new SOP.  
**Failure paths:** Forgot `--reset` / re-ingest → stale answers until re-index.

---

### Journey J4 — Operate without cloud LLM (Privacy-sensitive site)

**Goal:** Use retrieval without sending prompts to a cloud API.

| Step | Actor action | System response |
|------|--------------|-----------------|
| 1 | Admin leaves cloud keys unset; installs Ollama and pulls model **or** uses extractive mode | Provider resolves to Ollama or extractive |
| 2 | Technician asks a maintenance question | Local LLM answer **or** raw excerpts with citations |
| 3 | Admin sees status in sidebar | Indicates Ollama / no API key path |

**Success:** Plant data/questions stay local (embeddings always local; generation local if Ollama).  
**Failure paths:** Ollama not running → extractive fallback with guidance.

---

### Journey J5 — Portfolio / demo walkthrough (Reviewer)

**Goal:** Understand and demonstrate the RAG pipeline.

| Step | Actor action | System response |
|------|--------------|-----------------|
| 1 | Reviewer reads README + this SRS | Understands scope and requirements |
| 2 | Runs `pytest tests -q` | Automated tests pass |
| 3 | Runs ingest + Streamlit demo questions | Live cited Q&A |
| 4 | Optionally opens `rag_step_by_step*.ipynb` | Sees pipeline steps explained |

---

## 6. Functional requirements

Requirements use MoSCoW priority: **Must / Should / Could / Won’t (this release)**.

### 6.1 Document processing

| ID | Requirement | Priority | Related stories |
|----|-------------|----------|-----------------|
| **FR-01** | The system shall parse `.pdf`, `.txt`, `.md` (and configured supported extensions) from a documents directory. | Must | US-1.1 |
| **FR-02** | The system shall reject or skip unsupported file types during directory parse. | Must | US-1.1 |
| **FR-03** | The system shall split documents into overlapping chunks of configurable size. | Must | US-1.2, US-6.2 |
| **FR-04** | The system shall attach metadata: source name, page (if PDF), and chunk id. | Must | US-1.3 |
| **FR-05** | The system shall generate local embeddings for chunks using a sentence-transformer model. | Must | US-2.1 |
| **FR-06** | The system shall persist embeddings and documents in a Chroma collection. | Must | US-1.2 |
| **FR-07** | The system shall support resetting the collection before re-ingest (`--reset`). | Must | US-1.2 |

### 6.2 Retrieval and answering

| ID | Requirement | Priority | Related stories |
|----|-------------|----------|-----------------|
| **FR-08** | The system shall embed the user query and retrieve the top-k most similar chunks by cosine similarity. | Must | US-2.1 |
| **FR-09** | The system shall return an empty / guidance response when no documents are indexed. | Must | US-3.2 |
| **FR-10** | When an LLM is available, the system shall generate an answer using only retrieved excerpts. | Must | US-3.1 |
| **FR-11** | Generated answers shall include inline citation markers matching retrieved excerpt numbers. | Must | US-3.1 |
| **FR-12** | When no LLM is available, the system shall fall back to extractive display of retrieved excerpts. | Should | US-3.3 |
| **FR-13** | The system shall instruct the LLM not to invent specifications absent from excerpts. | Must | US-3.2 |
| **FR-14** | The system shall expose citation details (source, page, score, text snippet) to the UI. | Must | US-2.2, US-4.2 |

### 6.3 User interface

| ID | Requirement | Priority | Related stories |
|----|-------------|----------|-----------------|
| **FR-15** | The system shall provide a Streamlit chat interface for multi-turn conversation display. | Must | US-4.1 |
| **FR-16** | The system shall show a Sources expander for assistant messages that have citations. | Must | US-4.2 |
| **FR-17** | The sidebar shall display indexed chunk count and LLM provider/status. | Should | US-4.3 |
| **FR-18** | The sidebar shall warn when the index is empty and show how to re-index. | Should | US-4.3 |
| **FR-19** | The UI shall indicate response mode (e.g., provider name or extractive) when applicable. | Could | US-5.1 |

### 6.4 Configuration and providers

| ID | Requirement | Priority | Related stories |
|----|-------------|----------|-----------------|
| **FR-20** | The system shall load configuration from environment / `.env`. | Must | US-5.1 |
| **FR-21** | The system shall support providers: OpenRouter, Groq, OpenAI, Ollama, and `auto` selection. | Must | US-5.1 |
| **FR-22** | The system shall treat known placeholder API key values as unset. | Must | US-5.2 |
| **FR-23** | Chunk size, overlap, top-k, and embedding model shall be configurable. | Should | US-6.2 |

### 6.5 Quality assurance

| ID | Requirement | Priority | Related stories |
|----|-------------|----------|-----------------|
| **FR-24** | The repository shall include automated tests covering core modules (parsers, chunker, RAG, LLM config, ingest, etc.). | Should | US-6.1 |

---

## 7. Non-functional requirements

### 7.1 Performance

| ID | Requirement | Priority |
|----|-------------|----------|
| **NFR-01** | Query round-trip (retrieve + generate) should typically complete within **10 seconds** on a developer laptop for default top-k, excluding cold model download. | Should |
| **NFR-02** | First embedding-model load may be slower; subsequent queries shall reuse the cached model in-process. | Must |
| **NFR-03** | Ingestion shall support batching chunk embeddings (e.g., batches of 64) to avoid excessive memory spikes. | Should |

### 7.2 Reliability & availability

| ID | Requirement | Priority |
|----|-------------|----------|
| **NFR-04** | If the primary LLM call fails, the system shall try alternate configured providers or fall back to extractive mode rather than crashing the UI. | Must |
| **NFR-05** | Vector store data shall persist across application restarts (`chroma_db/`). | Must |
| **NFR-06** | The chat UI shall surface clear errors when modules fail to import or the index is empty. | Should |

### 7.3 Usability

| ID | Requirement | Priority |
|----|-------------|----------|
| **NFR-07** | Primary actions (ask question, view sources) shall be discoverable without training beyond a short caption/README. | Must |
| **NFR-08** | Setup instructions for API keys and ingest shall be documented in README and reflected in UI guidance when misconfigured. | Must |
| **NFR-09** | Example maintenance questions shall be provided for demos. | Should |

### 7.4 Security & privacy

| ID | Requirement | Priority |
|----|-------------|----------|
| **NFR-10** | Secrets (API keys) shall be stored in `.env` and excluded from version control patterns where applicable. | Must |
| **NFR-11** | The application is intended for **local/trusted network** use; it shall not assume hardened public multi-user auth in this release. | Must |
| **NFR-12** | Users shall be able to prefer local Ollama to avoid sending prompts to third-party clouds. | Should |
| **NFR-13** | The system shall not log full API keys in UI messages. | Must |

### 7.5 Maintainability & portability

| ID | Requirement | Priority |
|----|-------------|----------|
| **NFR-14** | Code shall be modular (`parsers`, `chunker`, `embeddings`, `vector_store`, `retriever`, `llm`, `rag`). | Must |
| **NFR-15** | Dependencies shall be declared in `requirements.txt`. | Must |
| **NFR-16** | Core logic shall be testable with mocks (no mandatory live LLM calls in unit tests). | Should |
| **NFR-17** | The solution shall run on Windows as the primary demo environment. | Must |

### 7.6 Accuracy & safety (domain)

| ID | Requirement | Priority |
|----|-------------|----------|
| **NFR-18** | Answers must be **grounded** in retrieved documentation; the system prompt shall forbid inventing thresholds or procedures. | Must |
| **NFR-19** | Citations shall be available so a human can verify safety-critical values before acting. | Must |
| **NFR-20** | The assistant is a **decision-support** tool, not a replacement for certified procedures, lockout/tagout, or human judgment. | Must |

### 7.7 Scalability (current targets)

| ID | Requirement | Priority |
|----|-------------|----------|
| **NFR-21** | The prototype shall comfortably support on the order of **tens to low hundreds of documents** / thousands of chunks on a single machine. | Should |
| **NFR-22** | Horizontal multi-user scale-out is **Won’t** for this release. | Won’t |

---

## 8. Data requirements

| Data item | Description | Storage |
|-----------|-------------|---------|
| Source documents | PDF/TXT/MD maintenance manuals & SOPs | `data/documents/` |
| Chunks + embeddings + metadata | Indexed retrieval units | Chroma `chroma_db/` |
| Runtime config | Provider keys, models, chunk/top-k settings | `.env` / environment |
| Chat session messages | In-memory UI history for current browser session | Streamlit `session_state` (not durable) |

---

## 9. External interfaces

### 9.1 User interfaces

- Streamlit web chat (title, caption, sidebar status, chat input, sources expander)

### 9.2 Software interfaces

| Interface | Purpose |
|-----------|---------|
| Chroma PersistentClient | Vector storage & similarity query |
| sentence-transformers | Local embeddings |
| OpenAI-compatible HTTP APIs | Groq / OpenRouter / OpenAI chat completions |
| Ollama `/api/chat` | Local LLM generation |
| pypdf | PDF text extraction |

### 9.3 CLI interfaces

```text
python ingest.py [--data-dir PATH] [--reset]
streamlit run app.py
pytest tests
```

---

## 10. Requirements traceability (summary)

| Epic | Key user stories | Key FRs | Key NFRs | Primary journeys |
|------|------------------|---------|----------|------------------|
| E1 Ingestion | US-1.1–1.3 | FR-01–07 | NFR-03, NFR-05 | J1, J3 |
| E2 Retrieval | US-2.1–2.2 | FR-08–09, FR-14 | NFR-01–02 | J2 |
| E3 Grounded Q&A | US-3.1–3.3 | FR-10–13 | NFR-18–20 | J2, J4 |
| E4 Chat UI | US-4.1–4.3 | FR-15–19 | NFR-07–09 | J2, J5 |
| E5 LLM flexibility | US-5.1–5.2 | FR-20–22 | NFR-04, NFR-12 | J1, J4 |
| E6 Quality | US-6.1–6.2 | FR-23–24 | NFR-14–16 | J5 |

---

## 11. Acceptance test ideas (high level)

| Scenario | Expected result |
|----------|-----------------|
| Ingest sample docs with `--reset` | Chunk count > 0 in sidebar |
| Ask Pump-3 vibration question with Groq configured | Natural answer + citations + sources expander |
| Remove/invalidate API keys; ask maintenance question | Extractive fallback or Ollama path; no crash |
| Ask question with empty Chroma | Message instructing to run `ingest.py` |
| Run `pytest tests -q` | All tests pass |

---

## 12. Roadmap (Could / future)

| ID | Idea | Notes |
|----|------|-------|
| **F-01** | CMMS work-order deep links | Tie citations to asset IDs |
| **F-02** | Sensor threshold alerts → RAG explanation | Combine IoT with SOP lookup |
| **F-03** | Role-based access & audit log | Needed for plant production deploy |
| **F-04** | OCR for scanned PDFs | Expand document coverage |
| **F-05** | Evaluation harness (faithfulness / citation accuracy) | Continuous quality metrics |

---

## 13. Document approval

| Role | Name | Signature / date |
|------|------|------------------|
| Author | Project team | July 2026 |
| Reviewer | *(to be assigned)* | |
| Approver | *(to be assigned)* | |

---

*End of Software Requirements Specification — Smart Maintenance Assistant v1.0*
