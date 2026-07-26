# Evaluation and Benchmarks

Benchmark set for the **Smart Maintenance Assistant** RAG pipeline: **20 fixed questions** with reference answers, source documents, and scoring keywords.

## Contents

| File | Purpose |
|------|---------|
| `questions.json` | Machine-readable benchmark (IDs, gold answers, keywords) |
| `questions.md` | Human-readable list of all 20 questions |
| `run_benchmark.py` | Run all questions through `rag.ask()` and save results |
| `results/` | Output folder for benchmark runs (generated) |

## Prerequisites

1. Documents ingested: `python ingest.py --reset`
2. Optional LLM key in `.env` (Groq/OpenRouter/etc.) for generative answers
3. Project venv activated

## Run the benchmark

From the project root (`smart-maintenance-assistant/`):

```bash
python evaluation_and_benchmarks/run_benchmark.py
```

Options:

```bash
python evaluation_and_benchmarks/run_benchmark.py --limit 5
python evaluation_and_benchmarks/run_benchmark.py --out evaluation_and_benchmarks/results/my_run.json
```

## Scoring (simple keyword check)

For each question, the runner checks whether **expected keywords** appear in the model answer (case-insensitive).  

- **Keyword hit rate** ≈ fraction of required keywords found  
- This is a lightweight faithfulness proxy — not a full LLM-as-judge eval  

Manual review: compare answers to the **Gold answer** column in `questions.md`.

## Question mix (20)

| Category | Count | Examples |
|----------|------:|----------|
| Pump-3 / vibration / temperature | 4 | Critical vibration, high-risk criteria |
| HVAC Unit-7 | 3 | Filters, motor current, delta-T |
| Motors / bearings | 3 | ISO thresholds, grease, replace vs monitor |
| Compressors / conveyors | 3 | Oil limits, belt mistrack |
| Safety / LOTO / PdM program | 4 | Seven LOTO steps, alert SLAs |
| Cross-cutting / diagnostics | 3 | Fault codes, vibration severity, compliance |

## Related docs

- [Software Requirements Specification](../docs/SRS.md)
- [System Architecture](../docs/SYSTEM_ARCHITECTURE.md)
