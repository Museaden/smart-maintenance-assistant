"""Run the 20-question RAG benchmark and score keyword overlap.

Usage (from project root):
    python evaluation_and_benchmarks/run_benchmark.py
    python evaluation_and_benchmarks/run_benchmark.py --limit 5
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.rag import ask  # noqa: E402
from src.vector_store import collection_count  # noqa: E402

QUESTIONS_PATH = Path(__file__).resolve().parent / "questions.json"
RESULTS_DIR = Path(__file__).resolve().parent / "results"


def _keyword_score(answer: str, keywords: list[str]) -> dict:
    text = answer.lower()
    hits = []
    misses = []
    for kw in keywords:
        if kw.lower() in text:
            hits.append(kw)
        else:
            misses.append(kw)
    total = len(keywords) or 1
    return {
        "hit_rate": len(hits) / total,
        "hits": hits,
        "misses": misses,
    }


def run_benchmark(limit: int | None = None) -> dict:
    payload = json.loads(QUESTIONS_PATH.read_text(encoding="utf-8"))
    questions = payload["questions"]
    if limit is not None:
        questions = questions[:limit]

    indexed = collection_count()
    rows = []
    hit_rates = []

    print(f"Indexed chunks: {indexed}")
    print(f"Running {len(questions)} question(s)...\n")

    for item in questions:
        qid = item["id"]
        question = item["question"]
        print(f"[{qid}] {question}")
        response = ask(question)
        score = _keyword_score(response.answer, item["expected_keywords"])
        hit_rates.append(score["hit_rate"])

        top_sources = [c.source for c in response.citations[:3]]
        print(
            f"  mode={response.mode}  keyword_hit_rate={score['hit_rate']:.0%}  "
            f"sources={top_sources}"
        )
        if score["misses"]:
            print(f"  missed keywords: {score['misses']}")

        rows.append(
            {
                "id": qid,
                "category": item["category"],
                "question": question,
                "gold_answer": item["gold_answer"],
                "expected_keywords": item["expected_keywords"],
                "reference_docs": item["reference_docs"],
                "answer": response.answer,
                "mode": response.mode,
                "citation_sources": [
                    {
                        "citation_id": c.citation_id,
                        "source": c.source,
                        "page": c.page,
                        "score": round(c.score, 4),
                    }
                    for c in response.citations
                ],
                "keyword_score": score,
            }
        )
        print()

    mean_hit = sum(hit_rates) / len(hit_rates) if hit_rates else 0.0
    report = {
        "benchmark": payload["benchmark_name"],
        "version": payload["version"],
        "ran_at": datetime.now(timezone.utc).isoformat(),
        "indexed_chunks": indexed,
        "questions_run": len(rows),
        "mean_keyword_hit_rate": round(mean_hit, 4),
        "results": rows,
    }
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="Run 20-question RAG benchmark")
    parser.add_argument("--limit", type=int, default=None, help="Run only first N questions")
    parser.add_argument(
        "--out",
        type=Path,
        default=None,
        help="Output JSON path (default: results/benchmark_YYYYMMDD_HHMMSS.json)",
    )
    args = parser.parse_args()

    report = run_benchmark(limit=args.limit)

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    out = args.out
    if out is None:
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        out = RESULTS_DIR / f"benchmark_{stamp}.json"

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    print("=" * 60)
    print(f"Mean keyword hit rate: {report['mean_keyword_hit_rate']:.0%}")
    print(f"Saved: {out}")


if __name__ == "__main__":
    main()
