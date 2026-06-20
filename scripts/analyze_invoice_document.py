#!/usr/bin/env python3
"""Analyze a synthetic invoice with Azure AI Document Intelligence."""

from __future__ import annotations

import base64
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DOCUMENT = ROOT / "data" / "processed" / "extraction_samples" / "synthetic_invoice_lumacredit.pdf"
OUT_DIR = ROOT / "data" / "processed" / "document_intelligence"
API_VERSION = "2024-11-30"
MODEL_ID = "prebuilt-invoice"


def env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise SystemExit(f"Missing required environment variable: {name}")
    return value


def request(method: str, url: str, key: str, payload: object | None = None) -> tuple[int, dict[str, str], dict]:
    body = None if payload is None else json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=body,
        method=method,
        headers={
            "Content-Type": "application/json",
            "Ocp-Apim-Subscription-Key": key,
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=90) as response:
            raw = response.read()
            data = json.loads(raw.decode("utf-8")) if raw else {}
            return response.status, dict(response.headers), data
    except urllib.error.HTTPError as exc:
        details = exc.read().decode("utf-8")
        raise SystemExit(f"Document Intelligence request failed: {exc.code} {details}") from exc


def submit_analysis(endpoint: str, key: str, document_path: Path) -> str:
    payload = {
        "base64Source": base64.b64encode(document_path.read_bytes()).decode("ascii"),
    }
    url = (
        f"{endpoint}/documentintelligence/documentModels/{MODEL_ID}:analyze"
        f"?_overload=analyzeDocument&api-version={API_VERSION}&features=keyValuePairs"
    )
    status, headers, _ = request("POST", url, key, payload)
    if status != 202:
        raise SystemExit(f"Expected 202 Accepted, received {status}")

    operation_location = headers.get("Operation-Location") or headers.get("operation-location")
    if not operation_location:
        raise SystemExit("Document Intelligence response did not include Operation-Location.")
    return operation_location


def poll_result(operation_location: str, key: str, timeout_seconds: int = 120) -> dict:
    started = time.time()
    while time.time() - started < timeout_seconds:
        _, _, payload = request("GET", operation_location, key)
        status = payload.get("status")
        if status == "succeeded":
            return payload
        if status == "failed":
            raise SystemExit(json.dumps(payload, indent=2))
        time.sleep(2)
    raise SystemExit("Timed out waiting for Document Intelligence analysis.")


def field_value(field: dict[str, Any] | None) -> Any:
    if not field:
        return None
    for key in (
        "valueString",
        "valueDate",
        "valueTime",
        "valuePhoneNumber",
        "valueNumber",
        "valueInteger",
        "valueCurrency",
        "valueAddress",
        "content",
    ):
        if key in field:
            return field[key]
    return None


def simplify_invoice(result: dict) -> dict:
    analyze_result = result.get("analyzeResult", {})
    documents = analyze_result.get("documents", [])
    fields = documents[0].get("fields", {}) if documents else {}
    items = field_value(fields.get("Items")) or []

    return {
        "model_id": MODEL_ID,
        "status": result.get("status"),
        "fields": {
            "VendorName": field_value(fields.get("VendorName")),
            "CustomerName": field_value(fields.get("CustomerName")),
            "InvoiceId": field_value(fields.get("InvoiceId")),
            "InvoiceDate": field_value(fields.get("InvoiceDate")),
            "DueDate": field_value(fields.get("DueDate")),
            "SubTotal": field_value(fields.get("SubTotal")),
            "TotalTax": field_value(fields.get("TotalTax")),
            "InvoiceTotal": field_value(fields.get("InvoiceTotal")),
        },
        "item_count": len(items),
        "content_excerpt": analyze_result.get("content", "")[:500],
        "contains_real_data": False,
    }


def main() -> None:
    document_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_DOCUMENT
    if not document_path.exists():
        raise SystemExit(
            f"Document not found: {document_path}. Run src/extraction/create_synthetic_invoice_pdf.py first."
        )

    endpoint = env("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT").rstrip("/")
    key = env("AZURE_DOCUMENT_INTELLIGENCE_KEY")
    operation_location = submit_analysis(endpoint, key, document_path)
    result = poll_result(operation_location, key)
    summary = simplify_invoice(result)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    raw_path = OUT_DIR / "synthetic_invoice_raw.json"
    summary_path = OUT_DIR / "synthetic_invoice_summary.json"
    raw_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    summary_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")

    print(json.dumps(summary, indent=2))
    print(f"Wrote raw result to {raw_path}")
    print(f"Wrote summary to {summary_path}")


if __name__ == "__main__":
    main()
