# Copyright (c) Microsoft. All rights reserved.

"""Credit Policy Assistant hosted agent.

Uses Azure AI Search for grounding and returns cited credit-policy answers
through the Foundry Responses protocol.
"""

import asyncio
import json
import logging
import os
import urllib.error
import urllib.request

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

from azure.ai.agentserver.responses import (
    CreateResponse,
    ResponseContext,
    ResponsesAgentServerHost,
    ResponsesServerOptions,
    TextResponse,
)
from azure.ai.agentserver.responses.models import (
    MessageContentInputTextContent,
    MessageContentOutputTextContent,
)

logger = logging.getLogger(__name__)

_credential = DefaultAzureCredential()
_endpoint = os.environ["FOUNDRY_PROJECT_ENDPOINT"]
_model = os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"]
_search_endpoint = os.environ["AZURE_SEARCH_ENDPOINT"].rstrip("/")
_search_index = os.getenv("AZURE_SEARCH_INDEX_NAME", "credit-risk-documents")
_search_top = int(os.getenv("AZURE_SEARCH_TOP_K", "5"))

_responses_client = AIProjectClient(
    endpoint=_endpoint, credential=_credential
).get_openai_client().responses

app = ResponsesAgentServerHost(
    options=ResponsesServerOptions(default_fetch_history_count=20),
)

_SYSTEM_PROMPT = """You are Credit Policy Assistant for LumaCredit Financial.

Answer lending policy and credit-risk workflow questions using only the retrieved
context. Include source paths in the answer. If the context does not contain the
answer, say that the indexed policy sources do not contain enough information.
Do not approve, deny, price, or recommend final loan decisions.
"""

_ROLE_MAP = {
    MessageContentOutputTextContent: "assistant",
    MessageContentInputTextContent: "user",
}

def _build_input(current_input: str, history: list) -> list[dict]:
    """Convert platform history + current message into Responses API input."""
    items = []
    for item in history:
        for content in getattr(item, "content", None) or []:
            role = _ROLE_MAP.get(type(content))
            if role and content.text:
                items.append({"role": role, "content": content.text})
    items.append({"role": "user", "content": current_input})
    return items


def _search_documents(question: str) -> list[dict]:
    """Search Azure AI Search with Entra auth and return top policy chunks."""
    token = _credential.get_token("https://search.azure.com/.default").token
    payload = {
        "search": question,
        "top": _search_top,
        "select": "title,content,source_path,document_type,department,sensitivity_label",
    }
    request = urllib.request.Request(
        f"{_search_endpoint}/indexes/{_search_index}/docs/search?api-version=2024-07-01",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        body = json.loads(response.read().decode("utf-8"))
    return body.get("value", [])


def _format_context(results: list[dict]) -> str:
    if not results:
        return "No indexed policy sources were retrieved."

    blocks = []
    for index, result in enumerate(results, start=1):
        blocks.append(
            "\n".join(
                [
                    f"Source {index}",
                    f"title: {result.get('title', '')}",
                    f"source_path: {result.get('source_path', '')}",
                    f"department: {result.get('department', '')}",
                    f"document_type: {result.get('document_type', '')}",
                    f"sensitivity_label: {result.get('sensitivity_label', '')}",
                    f"content: {result.get('content', '')}",
                ]
            )
        )
    return "\n\n".join(blocks)


@app.response_handler
async def handler(
    request: CreateResponse,
    context: ResponseContext,
    _cancellation_signal: asyncio.Event,
):
    """Forward user input to the model with conversation history."""
    user_input = await context.get_input_text() or "Hello!"
    history = await context.get_history()
    try:
        search_results = await asyncio.get_running_loop().run_in_executor(
            None, lambda: _search_documents(user_input)
        )
        retrieved_context = _format_context(search_results)
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        logger.exception("Search grounding failed")
        retrieved_context = f"Search grounding failed: {type(exc).__name__}"

    grounded_input = f"""Question:
{user_input}

Retrieved context:
{retrieved_context}

Answer with concise reasoning and include source_path citations."""

    input_items = _build_input(grounded_input, history)

    response = await asyncio.get_running_loop().run_in_executor(
        None,
        lambda: _responses_client.create(
            model=_model,
            instructions=_SYSTEM_PROMPT,
            input=input_items,
            store=False,
        ),
    )

    return TextResponse(context, request, text=response.output_text)


app.run()
