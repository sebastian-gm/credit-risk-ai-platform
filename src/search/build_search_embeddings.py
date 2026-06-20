#!/usr/bin/env python3
"""Generate Azure OpenAI embeddings for search chunks."""

from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
IN = ROOT / "data" / "processed" / "search_chunks" / "search_chunks.json"
OUT = ROOT / "data" / "processed" / "search_chunks" / "search_chunks_with_embeddings.json"
SUMMARY = ROOT / "data" / "processed" / "search_chunks" / "search_embeddings_summary.json"
API_VERSION = "2024-10-21"
DIMENSIONS = 1536


def env(name: str, default: str | None = None) -> str:
    value = os.environ.get(name, default)
    if not value:
        raise SystemExit(f"Missing required environment variable: {name}")
    return value


def embed_text(endpoint: str, key: str, deployment: str, text: str) -> list[float]:
    url = f"{endpoint}/openai/deployments/{deployment}/embeddings?api-version={API_VERSION}"
    payload = {"input": text, "dimensions": DIMENSIONS}
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        method="POST",
        headers={
            "Content-Type": "application/json",
            "api-key": key,
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=90) as response:
            data = json.loads(response.read().decode("utf-8"))
            return data["data"][0]["embedding"]
    except urllib.error.HTTPError as exc:
        details = exc.read().decode("utf-8")
        raise SystemExit(f"Embedding request failed: {exc.code} {details}") from exc


def main() -> None:
    if not IN.exists():
        raise SystemExit("Search chunks missing. Run src/search/build_search_chunks.py first.")

    endpoint = env("AZURE_OPENAI_ENDPOINT").rstrip("/")
    key = env("AZURE_OPENAI_API_KEY")
    deployment = env("AZURE_OPENAI_EMBEDDING_DEPLOYMENT", "text-embedding-3-small")
    docs = json.loads(IN.read_text(encoding="utf-8"))

    embedded = []
    for idx, doc in enumerate(docs, start=1):
        content = f"{doc['title']}\n\n{doc['content']}"
        vector = embed_text(endpoint, key, deployment, content)
        embedded.append({**doc, "content_vector": vector})
        print(f"Embedded {idx}/{len(docs)}: {doc['id']}")
        time.sleep(0.05)

    OUT.write_text(json.dumps(embedded, indent=2) + "\n", encoding="utf-8")
    SUMMARY.write_text(
        json.dumps(
            {
                "source_chunk_count": len(docs),
                "embedded_chunk_count": len(embedded),
                "embedding_deployment": deployment,
                "dimensions": DIMENSIONS,
                "contains_real_data": False,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {len(embedded)} embedded chunks to {OUT}")


if __name__ == "__main__":
    main()
