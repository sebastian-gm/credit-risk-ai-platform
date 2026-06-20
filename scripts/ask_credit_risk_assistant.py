#!/usr/bin/env python3
"""Answer credit-risk questions using Azure AI Search citations and Azure OpenAI."""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request

SEARCH_INDEX = "credit-risk-documents"
SEARCH_API_VERSION = "2024-07-01"
OPENAI_API_VERSION = "2024-10-21"
VECTOR_DIMENSIONS = 1536


def env(name: str, default: str | None = None) -> str:
    value = os.environ.get(name, default)
    if not value:
        raise SystemExit(f"Missing required environment variable: {name}")
    return value


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


def optional_env(name: str) -> str | None:
    return os.environ.get(name)


def embed_query(question: str) -> list[float] | None:
    endpoint = optional_env("AZURE_OPENAI_ENDPOINT")
    key = optional_env("AZURE_OPENAI_API_KEY")
    deployment = optional_env("AZURE_OPENAI_EMBEDDING_DEPLOYMENT")
    if not endpoint or not key or not deployment:
        return None

    url = f"{endpoint.rstrip('/')}/openai/deployments/{deployment}/embeddings?api-version={OPENAI_API_VERSION}"
    payload = {"input": question, "dimensions": VECTOR_DIMENSIONS}
    data = post_json(url, {"api-key": key}, payload)
    return data["data"][0]["embedding"]


def search_documents(question: str, top: int = 5) -> list[dict]:
    endpoint = env("AZURE_SEARCH_ENDPOINT").rstrip("/")
    key = env("AZURE_SEARCH_ADMIN_KEY")
    url = f"{endpoint}/indexes/{SEARCH_INDEX}/docs/search?api-version={SEARCH_API_VERSION}"
    vector = embed_query(question)
    payload = {
        "search": question,
        "top": top,
        "select": "title,content,source_path,raw_data_lake_path,document_type,department,sensitivity_label",
    }
    if vector:
        payload["vectorQueries"] = [
            {
                "kind": "vector",
                "vector": vector,
                "fields": "content_vector",
                "k": top,
                "exhaustive": False,
            }
        ]
    data = post_json(url, {"api-key": key}, payload)
    return data.get("value", [])


def build_context(results: list[dict]) -> str:
    blocks = []
    for i, result in enumerate(results, start=1):
        blocks.append(
            "\n".join(
                [
                    f"[{i}] {result.get('title', 'Untitled')}",
                    f"Source: {result.get('raw_data_lake_path') or result.get('source_path')}",
                    f"Type: {result.get('document_type')} | Department: {result.get('department')}",
                    f"Sensitivity: {result.get('sensitivity_label')}",
                    "Content:",
                    result.get("content", ""),
                ]
            )
        )
    return "\n\n---\n\n".join(blocks)


def answer_question(question: str, results: list[dict]) -> str:
    endpoint = env("AZURE_OPENAI_ENDPOINT").rstrip("/")
    key = env("AZURE_OPENAI_API_KEY")
    deployment = env("AZURE_OPENAI_CHAT_DEPLOYMENT", "gpt-5-mini")
    url = f"{endpoint}/openai/deployments/{deployment}/chat/completions?api-version={OPENAI_API_VERSION}"

    system = (
        "You are a credit-risk AI assistant for a synthetic portfolio demo. "
        "Answer only from the provided context. If the context is insufficient, say so. "
        "Cite sources using the source paths exactly as provided. Keep answers concise."
    )
    user = f"Question:\n{question}\n\nContext:\n{build_context(results)}"
    payload = {
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "max_completion_tokens": 500,
    }
    data = post_json(url, {"api-key": key}, payload)
    return data["choices"][0]["message"]["content"].strip()


def main() -> None:
    question = " ".join(sys.argv[1:]).strip()
    if not question:
        raise SystemExit('Usage: python3 scripts/ask_credit_risk_assistant.py "your question"')

    results = search_documents(question)
    if not results:
        raise SystemExit("No search results returned.")

    print(answer_question(question, results))
    print("\nCitations retrieved:")
    for result in results:
        print(f"- {result.get('raw_data_lake_path') or result.get('source_path')}")


if __name__ == "__main__":
    main()
