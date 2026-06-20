# Azure AI Search

Azure AI Search provides the retrieval layer for the RAG workflow.

## Demo Configuration

```text
SKU: Free
Region: Canada Central
Index: credit-risk-documents
Source data: synthetic business documents
```

The index supports metadata-rich keyword search and vector search. Hybrid
queries combine BM25 keyword retrieval with Azure OpenAI embeddings.

The core resource group is in East US 2, but Search is configured separately
because capacity can vary by region.

## Indexed Content

The index includes chunks from:

- credit policies;
- fair lending and responsible AI policy;
- document checklist policy;
- underwriting memos;
- compliance checklists;
- fraud review notes;
- operations report;
- synthetic loan application JSON files.

## Citation Fields

Each chunk keeps:

- source path;
- raw Data Lake path;
- document type;
- department;
- sensitivity label;
- owner;
- chunk index.

These fields allow retrieval results to be shown with source citations.

## Run Pipeline

Generate chunks:

```bash
python3 src/search/build_search_chunks.py
```

Load the index:

```bash
AZURE_SEARCH_ENDPOINT="https://<search-service>.search.windows.net" \
AZURE_SEARCH_ADMIN_KEY="<admin-key>" \
python3 scripts/load_ai_search_index.py
```

Generate embeddings before loading the vector-enabled index:

```bash
AZURE_OPENAI_ENDPOINT="https://<openai-resource>.openai.azure.com/" \
AZURE_OPENAI_API_KEY="<openai-key>" \
AZURE_OPENAI_EMBEDDING_DEPLOYMENT="text-embedding-3-small" \
python3 src/search/build_search_embeddings.py
```

Run a test query:

```bash
AZURE_SEARCH_ENDPOINT="https://<search-service>.search.windows.net" \
AZURE_SEARCH_ADMIN_KEY="<admin-key>" \
AZURE_OPENAI_ENDPOINT="https://<openai-resource>.openai.azure.com/" \
AZURE_OPENAI_API_KEY="<openai-key>" \
AZURE_OPENAI_EMBEDDING_DEPLOYMENT="text-embedding-3-small" \
python3 scripts/query_ai_search.py "debt-to-income above 45 exception review policy"
```

Expected first result should cite:

```text
raw/synthetic/policies/credit_policy_2026.md
```

See [retrieval-results.md](retrieval-results.md) for current query evidence.

## Current Output

The current pipeline creates:

```text
Index: credit-risk-documents
Chunks: 20
Embedded chunks: 20
Embedding model: text-embedding-3-small
Vector dimensions: 1536
Contains real data: false
```
