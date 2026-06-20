#!/usr/bin/env python3
"""Create and load the Azure AI Search index."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHUNKS = ROOT / "data" / "processed" / "search_chunks" / "search_chunks.json"
INDEX_NAME = "credit-risk-documents"
API_VERSION = "2024-07-01"


def env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise SystemExit(f"Missing required environment variable: {name}")
    return value


def request(method: str, url: str, key: str, payload: object | None = None) -> dict:
    body = None if payload is None else json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=body,
        method=method,
        headers={
            "Content-Type": "application/json",
            "api-key": key,
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            data = response.read()
            return json.loads(data.decode("utf-8")) if data else {}
    except urllib.error.HTTPError as exc:
        details = exc.read().decode("utf-8")
        raise SystemExit(f"Azure AI Search request failed: {exc.code} {details}") from exc


def create_index(endpoint: str, key: str) -> None:
    index = {
        "name": INDEX_NAME,
        "fields": [
            {"name": "id", "type": "Edm.String", "key": True, "filterable": True},
            {"name": "document_id", "type": "Edm.String", "filterable": True, "sortable": True},
            {"name": "chunk_index", "type": "Edm.Int32", "filterable": True, "sortable": True},
            {"name": "title", "type": "Edm.String", "searchable": True, "filterable": True},
            {"name": "content", "type": "Edm.String", "searchable": True},
            {"name": "source_path", "type": "Edm.String", "filterable": True, "facetable": True},
            {"name": "raw_data_lake_path", "type": "Edm.String", "filterable": True},
            {"name": "document_type", "type": "Edm.String", "filterable": True, "facetable": True},
            {"name": "department", "type": "Edm.String", "filterable": True, "facetable": True},
            {"name": "sensitivity_label", "type": "Edm.String", "filterable": True, "facetable": True},
            {"name": "owner", "type": "Edm.String", "filterable": True, "facetable": True},
            {"name": "contains_real_data", "type": "Edm.Boolean", "filterable": True},
            {"name": "generated_at", "type": "Edm.String", "filterable": True},
        ],
        "scoringProfiles": [],
    }
    url = f"{endpoint}/indexes/{INDEX_NAME}?api-version={API_VERSION}"
    request("PUT", url, key, index)


def load_documents(endpoint: str, key: str) -> int:
    if not CHUNKS.exists():
        raise SystemExit("Search chunks missing. Run src/search/build_search_chunks.py first.")

    docs = json.loads(CHUNKS.read_text(encoding="utf-8"))
    actions = [{"@search.action": "upload", **doc} for doc in docs]
    url = f"{endpoint}/indexes/{INDEX_NAME}/docs/index?api-version={API_VERSION}"
    request("POST", url, key, {"value": actions})
    return len(actions)


def main() -> None:
    endpoint = env("AZURE_SEARCH_ENDPOINT").rstrip("/")
    key = env("AZURE_SEARCH_ADMIN_KEY")
    create_index(endpoint, key)
    count = load_documents(endpoint, key)
    print(f"Loaded {count} chunks into index {INDEX_NAME}")


if __name__ == "__main__":
    main()
