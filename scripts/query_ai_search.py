#!/usr/bin/env python3
"""Run a test Azure AI Search query and print citation-ready results."""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request

INDEX_NAME = "credit-risk-documents"
SEARCH_API_VERSION = "2024-07-01"
OPENAI_API_VERSION = "2024-10-21"
VECTOR_DIMENSIONS = 1536


def env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise SystemExit(f"Missing required environment variable: {name}")
    return value


def optional_env(name: str) -> str | None:
    return os.environ.get(name)


def post_json(url: str, headers: dict[str, str], payload: object) -> dict:
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", **headers},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=90) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        details = exc.read().decode("utf-8")
        raise SystemExit(f"Request failed: {exc.code} {details}") from exc


def embed_query(query: str) -> list[float] | None:
    endpoint = optional_env("AZURE_OPENAI_ENDPOINT")
    key = optional_env("AZURE_OPENAI_API_KEY")
    deployment = optional_env("AZURE_OPENAI_EMBEDDING_DEPLOYMENT")
    if not endpoint or not key or not deployment:
        return None

    url = f"{endpoint.rstrip('/')}/openai/deployments/{deployment}/embeddings?api-version={OPENAI_API_VERSION}"
    payload = {"input": query, "dimensions": VECTOR_DIMENSIONS}
    data = post_json(url, {"api-key": key}, payload)
    return data["data"][0]["embedding"]


def main() -> None:
    query = " ".join(sys.argv[1:]) or "What policy applies when debt-to-income is above 45%?"
    endpoint = env("AZURE_SEARCH_ENDPOINT").rstrip("/")
    key = env("AZURE_SEARCH_ADMIN_KEY")
    vector = embed_query(query)
    mode = "hybrid vector + keyword" if vector else "keyword"
    url = f"{endpoint}/indexes/{INDEX_NAME}/docs/search?api-version={SEARCH_API_VERSION}"
    request_payload: dict[str, object] = {
        "search": query,
        "top": 5,
        "select": "title,content,source_path,document_type,department,sensitivity_label,raw_data_lake_path",
    }
    if vector:
        request_payload["vectorQueries"] = [
            {
                "kind": "vector",
                "vector": vector,
                "fields": "content_vector",
                "k": 5,
                "exhaustive": False,
            }
        ]

    payload = post_json(url, {"api-key": key}, request_payload)

    print(f"Query: {query}")
    print(f"Mode: {mode}\n")
    for idx, result in enumerate(payload.get("value", []), start=1):
        content = result["content"].replace("\n", " ")
        excerpt = content[:260] + ("..." if len(content) > 260 else "")
        score = result.get("@search.score")
        score_text = f" | score: {score:.4f}" if isinstance(score, float) else ""
        print(f"{idx}. {result['title']}{score_text}")
        print(f"   source: {result['source_path']}")
        print(f"   type: {result['document_type']} | department: {result['department']}")
        print(f"   citation: {result['raw_data_lake_path']}")
        print(f"   excerpt: {excerpt}\n")


if __name__ == "__main__":
    main()
