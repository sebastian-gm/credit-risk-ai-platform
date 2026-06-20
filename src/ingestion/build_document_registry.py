#!/usr/bin/env python3
"""Build a document registry for the synthetic credit-risk dataset."""

from __future__ import annotations

import csv
import hashlib
import json
import mimetypes
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "data" / "synthetic"
OUT = ROOT / "data" / "processed" / "document_registry"


TYPE_RULES = [
    ("loan_applications", "loan_application", "Credit Risk", "pii_synthetic"),
    ("underwriting_memos", "underwriting_memo", "Credit Risk", "confidential_synthetic"),
    ("policies", "policy", "Compliance", "internal"),
    ("compliance", "governance_document", "Compliance", "internal"),
    ("fraud_notes", "fraud_review_note", "Fraud / Risk Ops", "confidential_synthetic"),
    ("operations", "operations_report", "Operations", "internal"),
    ("structured", "structured_dataset", "Analytics", "internal"),
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def classify(relative_path: str) -> tuple[str, str, str]:
    if relative_path == "README.md":
        return "dataset_note", "Analytics", "internal"
    for path_part, document_type, department, sensitivity_label in TYPE_RULES:
        if relative_path.startswith(f"{path_part}/"):
            return document_type, department, sensitivity_label
    return "unknown", "Unknown", "internal"


def owner_for(document_type: str) -> str:
    return {
        "loan_application": "loan_intake",
        "underwriting_memo": "credit_risk",
        "policy": "policy_owner",
        "governance_document": "compliance",
        "fraud_review_note": "fraud_ops",
        "operations_report": "loan_operations",
        "structured_dataset": "analytics",
    }.get(document_type, "unknown")


def retention_for(sensitivity_label: str) -> str:
    return {
        "pii_synthetic": "demo_pii_synthetic",
        "confidential_synthetic": "demo_confidential",
        "internal": "demo_internal",
    }.get(sensitivity_label, "demo_internal")


def build_registry() -> list[dict[str, object]]:
    if not SOURCE.exists():
        raise SystemExit("Synthetic data does not exist. Run scripts/generate_synthetic_data.py first.")

    ingestion_timestamp = datetime.now(UTC).replace(microsecond=0).isoformat()
    records: list[dict[str, object]] = []

    files = sorted(path for path in SOURCE.rglob("*") if path.is_file())
    for index, path in enumerate(files, start=1):
        relative_path = path.relative_to(SOURCE).as_posix()
        document_type, department, sensitivity_label = classify(relative_path)
        mime_type, _ = mimetypes.guess_type(path.name)

        records.append(
            {
                "document_id": f"DOC-{index:04d}",
                "file_name": path.name,
                "relative_path": relative_path,
                "raw_data_lake_path": f"raw/synthetic/{relative_path}",
                "document_type": document_type,
                "department": department,
                "sensitivity_label": sensitivity_label,
                "owner": owner_for(document_type),
                "retention_category": retention_for(sensitivity_label),
                "source_system": "synthetic_generator",
                "mime_type": mime_type or "application/octet-stream",
                "file_size_bytes": path.stat().st_size,
                "sha256": sha256(path),
                "ingestion_timestamp": ingestion_timestamp,
                "contains_real_data": False,
                "ready_for_search_index": document_type not in {"unknown"},
            }
        )

    return records


def write_outputs(records: list[dict[str, object]]) -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    json_path = OUT / "document_registry.json"
    csv_path = OUT / "document_registry.csv"
    summary_path = OUT / "document_registry_summary.json"

    json_path.write_text(json.dumps(records, indent=2) + "\n", encoding="utf-8")

    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(records[0].keys()))
        writer.writeheader()
        writer.writerows(records)

    summary: dict[str, object] = {
        "generated_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
        "document_count": len(records),
        "contains_real_data": False,
        "document_types": {},
        "departments": {},
        "sensitivity_labels": {},
    }

    for record in records:
        for key, output_key in [
            ("document_type", "document_types"),
            ("department", "departments"),
            ("sensitivity_label", "sensitivity_labels"),
        ]:
            bucket = summary[output_key]
            assert isinstance(bucket, dict)
            value = str(record[key])
            bucket[value] = bucket.get(value, 0) + 1

    summary_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    records = build_registry()
    write_outputs(records)
    print(f"Wrote {len(records)} document registry records to {OUT}")


if __name__ == "__main__":
    main()
