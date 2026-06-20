# RAG Assistant

The first assistant connects Azure AI Search retrieval with an Azure OpenAI chat
deployment. It answers only from retrieved context and prints the citations that
were provided to the model.

## Azure Resources

```text
Model: gpt-5-mini
Model version: 2025-08-07
Deployment: gpt-5-mini
Deployment SKU: GlobalStandard
Capacity: 10K TPM
Region: East US 2
Embedding model: text-embedding-3-small
Embedding dimensions: 1536
```

East US 2 is used for the model deployment because the lab subscription has
available GlobalStandard quota there for this small demo model.

## Run

Set these environment variables locally:

```bash
AZURE_SEARCH_ENDPOINT="https://<search-service>.search.windows.net"
AZURE_SEARCH_ADMIN_KEY="<search-admin-key>"
AZURE_OPENAI_ENDPOINT="https://<openai-resource>.openai.azure.com/"
AZURE_OPENAI_API_KEY="<openai-key>"
AZURE_OPENAI_CHAT_DEPLOYMENT="gpt-5-mini"
AZURE_OPENAI_EMBEDDING_DEPLOYMENT="text-embedding-3-small"
```

Ask a question:

```bash
python3 scripts/ask_credit_risk_assistant.py "What policy applies when debt-to-income is above 45%?"
```

Expected behavior:

- answer is grounded in retrieved source chunks;
- source paths are printed as citations;
- if the answer is not in context, the assistant should say so;
- no real customer data is used.

## Smoke Test

Question:

```text
What policy applies when debt-to-income is above 45%?
```

Observed answer:

```text
Applications with debt-to-income ratio above 45% require exception review.
```

Primary citation:

```text
raw/synthetic/policies/credit_policy_2026.md
```

Current limitation:

```text
The demo uses a small synthetic corpus. Retrieval quality should be measured
again after adding larger policy, application, and exception-review datasets.
```
