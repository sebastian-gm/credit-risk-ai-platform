#!/usr/bin/env python3
"""Evaluate retrieval and grounded assistant behavior against a small test set."""

from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "src" / "evaluation" / "rag_eval_cases.json"
OUT_DIR = ROOT / "data" / "processed" / "evaluation"
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


def embed_query(question: str) -> list[float]:
    endpoint = env("AZURE_OPENAI_ENDPOINT").rstrip("/")
    key = env("AZURE_OPENAI_API_KEY")
    deployment = env("AZURE_OPENAI_EMBEDDING_DEPLOYMENT", "text-embedding-3-small")
    url = f"{endpoint}/openai/deployments/{deployment}/embeddings?api-version={OPENAI_API_VERSION}"
    payload = {"input": question, "dimensions": VECTOR_DIMENSIONS}
    data = post_json(url, {"api-key": key}, payload)
    return data["data"][0]["embedding"]


def retrieve(question: str, top: int = 5) -> list[dict[str, Any]]:
    endpoint = env("AZURE_SEARCH_ENDPOINT").rstrip("/")
    key = env("AZURE_SEARCH_ADMIN_KEY")
    vector = embed_query(question)
    url = f"{endpoint}/indexes/{SEARCH_INDEX}/docs/search?api-version={SEARCH_API_VERSION}"
    payload = {
        "search": question,
        "top": top,
        "select": "title,content,source_path,raw_data_lake_path,document_type,department,sensitivity_label",
        "vectorQueries": [
            {
                "kind": "vector",
                "vector": vector,
                "fields": "content_vector",
                "k": top,
                "exhaustive": False,
            }
        ],
    }
    data = post_json(url, {"api-key": key}, payload)
    return data.get("value", [])


def build_context(results: list[dict[str, Any]]) -> str:
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


def answer(question: str, results: list[dict[str, Any]]) -> str:
    endpoint = env("AZURE_OPENAI_ENDPOINT").rstrip("/")
    key = env("AZURE_OPENAI_API_KEY")
    deployment = env("AZURE_OPENAI_CHAT_DEPLOYMENT", "gpt-5-mini")
    url = f"{endpoint}/openai/deployments/{deployment}/chat/completions?api-version={OPENAI_API_VERSION}"
    payload = {
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a credit-risk AI assistant for a synthetic portfolio demo. "
                    "Answer only from the provided context. If the context is insufficient, say so. "
                    "Cite source paths exactly. Keep answers concise."
                ),
            },
            {
                "role": "user",
                "content": f"Question:\n{question}\n\nContext:\n{build_context(results)}",
            },
        ],
        "max_completion_tokens": 1000,
    }
    data = post_json(url, {"api-key": key}, payload)
    return data["choices"][0]["message"]["content"].strip()


def rank_of_citation(results: list[dict[str, Any]], expected_citation: str) -> int | None:
    for idx, result in enumerate(results, start=1):
        citation = result.get("raw_data_lake_path") or result.get("source_path")
        if citation == expected_citation:
            return idx
    return None


def terms_present(answer_text: str, terms: list[str]) -> bool:
    lowered = answer_text.lower()
    return all(term.lower() in lowered for term in terms)


def evaluate_case(case: dict[str, Any]) -> dict[str, Any]:
    results = retrieve(case["question"])
    answer_text = answer(case["question"], results)
    expected_rank = rank_of_citation(results, case["expected_citation"])
    citations = [result.get("raw_data_lake_path") or result.get("source_path") for result in results]
    return {
        "id": case["id"],
        "question": case["question"],
        "expected_citation": case["expected_citation"],
        "expected_citation_rank": expected_rank,
        "retrieval_hit_at_5": expected_rank is not None,
        "answer_non_empty": bool(answer_text.strip()),
        "answer_term_pass": terms_present(answer_text, case["required_answer_terms"]),
        "required_answer_terms": case["required_answer_terms"],
        "answer": answer_text,
        "retrieved_citations": citations,
    }


def summarize(results: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(results)
    hits = sum(1 for result in results if result["retrieval_hit_at_5"])
    answer_passes = sum(1 for result in results if result["answer_term_pass"])
    non_empty_answers = sum(1 for result in results if result["answer_non_empty"])
    reciprocal_ranks = [
        1 / result["expected_citation_rank"] for result in results if result["expected_citation_rank"]
    ]
    return {
        "case_count": total,
        "retrieval_hit_rate_at_5": hits / total if total else 0,
        "answer_non_empty_rate": non_empty_answers / total if total else 0,
        "answer_term_pass_rate": answer_passes / total if total else 0,
        "mean_reciprocal_rank": sum(reciprocal_ranks) / total if total else 0,
        "all_cases_passed": hits == total and answer_passes == total,
    }


def write_markdown(summary: dict[str, Any], results: list[dict[str, Any]]) -> None:
    lines = [
        "# RAG Evaluation Results",
        "",
        "## Summary",
        "",
        f"- Cases: {summary['case_count']}",
        f"- Retrieval hit rate @5: {summary['retrieval_hit_rate_at_5']:.2f}",
        f"- Answer non-empty rate: {summary['answer_non_empty_rate']:.2f}",
        f"- Answer term pass rate: {summary['answer_term_pass_rate']:.2f}",
        f"- Mean reciprocal rank: {summary['mean_reciprocal_rank']:.2f}",
        f"- All cases passed: {summary['all_cases_passed']}",
        "",
        "## Cases",
        "",
    ]
    for result in results:
        lines.extend(
            [
                f"### {result['id']}",
                "",
                f"Question: {result['question']}",
                "",
                f"Expected citation rank: {result['expected_citation_rank']}",
                f"Retrieval hit @5: {result['retrieval_hit_at_5']}",
                f"Answer non-empty: {result['answer_non_empty']}",
                f"Answer term pass: {result['answer_term_pass']}",
                "",
                "Retrieved citations:",
                "",
            ]
        )
        lines.extend(f"- {citation}" for citation in result["retrieved_citations"])
        lines.extend(["", "Answer:", "", "```text", result["answer"], "```", ""])
    (OUT_DIR / "rag_evaluation_results.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    cases = json.loads(CASES.read_text(encoding="utf-8"))
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    results = []
    for case in cases:
        print(f"Evaluating {case['id']}")
        results.append(evaluate_case(case))
        time.sleep(0.2)

    summary = summarize(results)
    payload = {
        "summary": summary,
        "results": results,
        "contains_real_data": False,
    }
    (OUT_DIR / "rag_evaluation_results.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    write_markdown(summary, results)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
