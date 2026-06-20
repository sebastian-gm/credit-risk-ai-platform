#!/usr/bin/env python3
"""Smoke test the Azure AI Foundry project endpoint with Entra auth."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import urllib.error
import urllib.request


PROJECT_ENDPOINT = os.getenv(
    "AZURE_AI_PROJECT_ENDPOINT",
    "https://ai-account-dosuleocw4nxo.services.ai.azure.com/api/projects/crai-foundry-project",
).rstrip("/")
DEPLOYMENT_NAME = os.getenv("AZURE_FOUNDRY_DEPLOYMENT", "gpt-5-mini")
PROMPT = (
    "In one sentence, explain what a credit policy assistant does for a lending analyst. "
    "Mention that it supports review but does not make final loan decisions."
)


def get_access_token() -> str:
    result = subprocess.run(
        [
            "az",
            "account",
            "get-access-token",
            "--resource",
            "https://ai.azure.com",
            "--query",
            "accessToken",
            "-o",
            "tsv",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def main() -> int:
    token = get_access_token()
    payload = json.dumps({"model": DEPLOYMENT_NAME, "input": PROMPT}).encode("utf-8")
    request = urllib.request.Request(
        f"{PROJECT_ENDPOINT}/openai/v1/responses",
        data=payload,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            body = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        print(exc.read().decode("utf-8"), file=sys.stderr)
        return 1

    output_text = ""
    for item in body.get("output", []):
        for content in item.get("content", []):
            if content.get("type") == "output_text":
                output_text = content.get("text", "")

    print(f"status: {body.get('status')}")
    print(f"model: {body.get('model')}")
    print(f"response: {output_text}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
