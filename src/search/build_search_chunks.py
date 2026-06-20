#!/usr/bin/env python3
"""Build metadata-rich chunks for Azure AI Search."""

from __future__ import annotations

import csv
import json
import re
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "data" / "synthetic"
REGISTRY = ROOT / "data" / "processed" / "document_registry" / "document_registry.csv"
OUT = ROOT / "data" / "processed" / "search_chunks"

INDEXABLE_TYPES = {
    "dataset_note",
    "governance_document",
    "fraud_review_note",
    "loan_application",
    "operations_report",
    "policy",
    "underwriting_memo",
}


def read_registry() -> dict[str, dict[str, str]]:
    if not REGISTRY.exists():
        raise SystemExit("Document registry missing. Run src/ingestion/build_document_registry.py first.")

    with REGISTRY.open(newline="", encoding="utf-8") as f:
        return {row["relative_path"]: row for row in csv.DictReader(f)}


def read_content(path: Path) -> str:
    if path.suffix == ".json":
        payload = json.loads(path.read_text(encoding="utf-8"))
        return json.dumps(payload, indent=2)
    return path.read_text(encoding="utf-8")


def normalize(text: str) -> str:
    text = text.replace("\r\n", "\n")
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def chunk_text(text: str, max_chars: int = 1400, overlap: int = 150) -> list[str]:
    text = normalize(text)
    if len(text) <= max_chars:
        return [text]

    chunks: list[str] = []
    start = 0
    while start < len(text):
        end = min(start + max_chars, len(text))
        if end < len(text):
            paragraph_break = text.rfind("\n\n", start, end)
            sentence_break = text.rfind(". ", start, end)
            split_at = max(paragraph_break, sentence_break)
            if split_at > start + max_chars * 0.55:
                end = split_at + 1
        chunks.append(text[start:end].strip())
        if end >= len(text):
            break
        start = max(0, end - overlap)
    return [chunk for chunk in chunks if chunk]


def title_for(path: str) -> str:
    return Path(path).stem.replace("_", " ").replace("-", " ").title()


def main() -> None:
    registry = read_registry()
    generated_at = datetime.now(UTC).replace(microsecond=0).isoformat()
    chunks: list[dict[str, object]] = []

    for relative_path, record in sorted(registry.items()):
        if record["document_type"] not in INDEXABLE_TYPES:
            continue

        source_path = SOURCE / relative_path
        if not source_path.exists():
            continue

        content = read_content(source_path)
        for chunk_index, chunk in enumerate(chunk_text(content), start=1):
            chunks.append(
                {
                    "id": f"{record['document_id']}-{chunk_index:03d}",
                    "document_id": record["document_id"],
                    "chunk_index": chunk_index,
                    "title": title_for(relative_path),
                    "content": chunk,
                    "source_path": relative_path,
                    "raw_data_lake_path": record["raw_data_lake_path"],
                    "document_type": record["document_type"],
                    "department": record["department"],
                    "sensitivity_label": record["sensitivity_label"],
                    "owner": record["owner"],
                    "contains_real_data": False,
                    "generated_at": generated_at,
                }
            )

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "search_chunks.json").write_text(json.dumps(chunks, indent=2) + "\n", encoding="utf-8")
    (OUT / "search_chunks_summary.json").write_text(
        json.dumps(
            {
                "generated_at": generated_at,
                "chunk_count": len(chunks),
                "contains_real_data": False,
                "index_name": "credit-risk-documents",
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {len(chunks)} search chunks to {OUT}")


if __name__ == "__main__":
    main()
