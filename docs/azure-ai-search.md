# Azure AI Search

Azure AI Search provides the retrieval layer for the RAG workflow.

## Demo Configuration

```text
SKU: Free
Region: Canada Central
Index: credit-risk-documents
Source data: synthetic business documents
```

The first index is metadata-rich keyword search. Vector search and Azure OpenAI
embeddings are planned for the next phase.

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

Run a test query:

```bash
AZURE_SEARCH_ENDPOINT="https://<search-service>.search.windows.net" \
AZURE_SEARCH_ADMIN_KEY="<admin-key>" \
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
Contains real data: false
```
