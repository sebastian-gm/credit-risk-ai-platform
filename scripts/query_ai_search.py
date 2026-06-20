#!/usr/bin/env python3
"""Run a test Azure AI Search query and print citation-ready results."""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

INDEX_NAME = "credit-risk-documents"
API_VERSION = "2024-07-01"


def env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise SystemExit(f"Missing required environment variable: {name}")
    return value


def main() -> None:
    query = " ".join(sys.argv[1:]) or "What policy applies when debt-to-income is above 45%?"
    endpoint = env("AZURE_SEARCH_ENDPOINT").rstrip("/")
    key = env("AZURE_SEARCH_ADMIN_KEY")

    params = urllib.parse.urlencode(
        {
            "api-version": API_VERSION,
            "search": query,
            "$top": 5,
            "$select": "title,content,source_path,document_type,department,sensitivity_label,raw_data_lake_path",
        }
    )
    url = f"{endpoint}/indexes/{INDEX_NAME}/docs?{params}"
    req = urllib.request.Request(url, headers={"api-key": key})

    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        details = exc.read().decode("utf-8")
        raise SystemExit(f"Azure AI Search query failed: {exc.code} {details}") from exc

    print(f"Query: {query}\n")
    for idx, result in enumerate(payload.get("value", []), start=1):
        content = result["content"].replace("\n", " ")
        excerpt = content[:260] + ("..." if len(content) > 260 else "")
        print(f"{idx}. {result['title']}")
        print(f"   source: {result['source_path']}")
        print(f"   type: {result['document_type']} | department: {result['department']}")
        print(f"   citation: {result['raw_data_lake_path']}")
        print(f"   excerpt: {excerpt}\n")


if __name__ == "__main__":
    main()
