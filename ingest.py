"""Ingest maintenance documents: parse → chunk → embed → Chroma."""

import argparse
from pathlib import Path

from src.chunker import chunk_documents
from src.config import DATA_DIR
from src.parsers import parse_directory
from src.vector_store import add_chunks, collection_count, reset_collection


def ingest(data_dir: Path, reset: bool = False) -> None:
    if not data_dir.exists():
        raise FileNotFoundError(f"Document directory not found: {data_dir}")

    documents = parse_directory(data_dir)
    if not documents:
        print(f"No supported documents found in {data_dir}")
        return

    print(f"Parsed {len(documents)} document section(s) from {data_dir}")

    chunks = chunk_documents(documents)
    print(f"Created {len(chunks)} chunk(s)")

    if reset:
        reset_collection()
        print("Reset Chroma collection")

    added = add_chunks(chunks)
    total = collection_count()
    print(f"Added {added} chunk(s). Collection now has {total} total.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Ingest maintenance documents into Chroma vector DB"
    )
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=DATA_DIR,
        help="Folder containing PDF, TXT, or MD files",
    )
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Clear existing collection before ingesting",
    )
    args = parser.parse_args()
    ingest(args.data_dir, reset=args.reset)


if __name__ == "__main__":
    main()
