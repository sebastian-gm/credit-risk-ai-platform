# Evaluation

This project includes a lightweight RAG evaluation harness for the grounded
credit-risk assistant.

## What It Measures

```text
Retrieval hit rate @5
Expected citation rank
Mean reciprocal rank
Answer term pass rate
```

The current evaluation is deterministic and portfolio-oriented. It checks
whether the expected source appears in the retrieved citations and whether the
assistant answer includes required domain terms.

## Run

```bash
AZURE_SEARCH_ENDPOINT="https://<search-service>.search.windows.net" \
AZURE_SEARCH_ADMIN_KEY="<search-admin-key>" \
AZURE_OPENAI_ENDPOINT="https://<openai-resource>.openai.azure.com/" \
AZURE_OPENAI_API_KEY="<openai-key>" \
AZURE_OPENAI_CHAT_DEPLOYMENT="gpt-5-mini" \
AZURE_OPENAI_EMBEDDING_DEPLOYMENT="text-embedding-3-small" \
python3 scripts/run_rag_evaluation.py
```

Outputs:

```text
data/processed/evaluation/rag_evaluation_results.json
data/processed/evaluation/rag_evaluation_results.md
```

Generated outputs are local artifacts and are not committed.

## Current Test Set

```text
src/evaluation/rag_eval_cases.json
```

The first test set covers:

- DTI exception policy;
- small-business required documents;
- missing-document routing;
- prohibited automated loan decisions.

## Current Results

Latest run:

```text
Cases: 4
Retrieval hit rate @5: 1.00
Answer non-empty rate: 1.00
Answer term pass rate: 1.00
Mean reciprocal rank: 0.875
All cases passed: true
Contains real data: false
```

Interpretation:

```text
The current assistant retrieves the expected source within the top 5 results
for every test case. One case has the expected citation at rank 2, which is why
mean reciprocal rank is below 1.00.
```
