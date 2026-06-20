# Retrieval Results

Azure AI Search index:

```text
credit-risk-documents
```

Indexed chunks:

```text
20
```

Retrieval mode:

```text
Hybrid vector + keyword search
```

## Query: DTI Exception Review

Query:

```text
debt-to-income above 45 exception review policy
```

Top result:

```text
Title: Credit Policy 2026
Source: policies/credit_policy_2026.md
Citation: raw/synthetic/policies/credit_policy_2026.md
Document type: policy
Department: Compliance
```

Observed hybrid retrieval rank:

```text
1
```

## Query: Small-Business Required Documents

Query:

```text
What documents are required for small-business loans?
```

Top result:

```text
Title: Document Checklist Policy
Source: policies/document_checklist_policy.md
Citation: raw/synthetic/policies/document_checklist_policy.md
Document type: policy
Department: Compliance
```

## Query: Missing Document Detection

Query:

```text
Which files mention missing document detection?
```

Top results:

```text
1. Weekly Credit Ops Report
   Citation: raw/synthetic/operations/weekly_credit_ops_report.md

2. AI Use Case Registry
   Citation: raw/synthetic/compliance/ai_use_case_registry.md

3. Document Checklist Policy
   Citation: raw/synthetic/policies/document_checklist_policy.md
```

## Interpretation

This validates the first retrieval layer for RAG:

- source documents are chunked;
- source chunks are embedded with Azure OpenAI;
- Azure AI Search stores a vector field for semantic similarity;
- hybrid retrieval combines keyword and vector signals;
- metadata travels with each chunk;
- retrieval returns cited source paths;
- governance labels are available for filtering;
- no real data is indexed.
