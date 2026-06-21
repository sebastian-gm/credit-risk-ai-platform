# Portfolio Demo Package

This package is the short version of the project for interviews, portfolio reviews, and internal demos.

All data is synthetic.

## One-Minute Explanation

This project is a credit-risk AI platform for a lending team. It brings policies, loan documents, invoices, governance records, and credit-risk data into Azure. Analysts can ask policy questions, get cited answers, extract invoice fields, and see evidence that the assistant behavior was tested.

The important part is the workflow: data foundation, trusted retrieval, document extraction, hosted Foundry agent, evaluation, and governance controls.

## What To Show

| Step | Evidence | What It Shows |
| --- | --- | --- |
| 1 | [architecture.md](architecture.md) | End-to-end Azure workflow from documents to governed answers |
| 2 | [sql-row-counts.txt](evidence/sql-row-counts.txt) | Azure SQL contains document, analytics, and governance tables |
| 3 | [search-query-results.txt](evidence/search-query-results.txt) | Azure AI Search retrieves the right policy source |
| 4 | [rag-assistant-answer.txt](evidence/rag-assistant-answer.txt) | The assistant answers with source-path citations |
| 5 | [invoice-extraction-summary.json](evidence/invoice-extraction-summary.json) | Document Intelligence extracts structured invoice fields |
| 6 | [rag-evaluation-results.md](evidence/rag-evaluation-results.md) | Retrieval and answer checks passed on the curated test set |
| 7 | [hosted-agent-playground.png](evidence/foundry/hosted-agent-playground.png) | The assistant is deployed as a Foundry hosted agent |
| 8 | [hosted-agent-evaluation-report.png](evidence/foundry/hosted-agent-evaluation-report.png) | Foundry evaluated the hosted agent and passed 2 of 2 smoke cases |
| 9 | [foundry-project-summary.md](evidence/foundry/foundry-project-summary.md) | Foundry resources, model deployment, and hosted agent evidence |

## Screenshots To Use

Use these screenshots in the portfolio page, LinkedIn post, or interview deck:

- [evidence-summary.png](evidence/evidence-summary.png)
- [azure-portal/resource-group-overview.png](evidence/azure-portal/resource-group-overview.png)
- [azure-portal/storage-account-overview.png](evidence/azure-portal/storage-account-overview.png)
- [azure-portal/azure-sql-database-overview.png](evidence/azure-portal/azure-sql-database-overview.png)
- [azure-portal/ai-search-overview.png](evidence/azure-portal/ai-search-overview.png)
- [azure-portal/azure-openai-overview.png](evidence/azure-portal/azure-openai-overview.png)
- [azure-portal/document-intelligence-overview.png](evidence/azure-portal/document-intelligence-overview.png)
- [azure-portal/key-vault-overview.png](evidence/azure-portal/key-vault-overview.png)
- [foundry/hosted-agent-playground.png](evidence/foundry/hosted-agent-playground.png)
- [foundry/hosted-agent-evaluation-report.png](evidence/foundry/hosted-agent-evaluation-report.png)

## Five-Minute Demo Script

### 1. Start With The Business Problem

Lending teams have policies, applications, invoices, reports, and governance records spread across different places. This project shows how that information can be organized in Azure so analysts can find trusted answers faster.

### 2. Show The Data Foundation

Open [sql-row-counts.txt](evidence/sql-row-counts.txt).

Say:

```text
The platform has synthetic credit-risk records, document metadata, and governance tables loaded into Azure SQL. The data layer is separate from the AI layer, so reporting and controls are not dependent on a single prompt.
```

### 3. Show Search And Cited Answers

Open [search-query-results.txt](evidence/search-query-results.txt), then [rag-assistant-answer.txt](evidence/rag-assistant-answer.txt).

Say:

```text
For a DTI question, Azure AI Search retrieves the credit policy first. The assistant uses that context and returns source paths, so the analyst can check where the answer came from.
```

### 4. Show Document Extraction

Open [invoice-extraction-summary.json](evidence/invoice-extraction-summary.json).

Say:

```text
The platform also handles document automation. This example uses Document Intelligence to extract invoice fields for review. It is a simple finance workflow, but the same pattern applies to loan files, forms, and compliance documents.
```

### 5. Show Foundry And Evaluation

Open [hosted-agent-playground.png](evidence/foundry/hosted-agent-playground.png), then [hosted-agent-evaluation-report.png](evidence/foundry/hosted-agent-evaluation-report.png).

Say:

```text
The assistant is deployed as a hosted agent in Azure AI Foundry. I also ran a Foundry smoke evaluation. Both cases passed: one checks policy behavior and one checks that the assistant refuses automated loan approval.
```

### 6. End With Governance

Open [governance.md](governance.md).

Say:

```text
The project includes use-case registration, prompt metadata, review checks, audit logs, and blocked use cases. The automated loan approval use case is blocked because final lending decisions require human review.
```

## What This Proves

This project proves the ability to:

- design an Azure data and AI workflow for a real business process;
- provision cloud resources with Terraform;
- organize synthetic business documents and structured credit-risk data;
- load governed tables into Azure SQL;
- build hybrid retrieval with Azure AI Search;
- generate grounded answers with citations;
- use Document Intelligence for field extraction;
- deploy and test a hosted agent in Azure AI Foundry;
- run a Foundry evaluation and preserve the result;
- define governance records for use cases, prompts, reviews, and audit events;
- explain the business value in simple terms.

## Current Results

| Area | Result |
| --- | --- |
| Azure SQL load | 29,465 credit-risk rows and governance tables loaded |
| Search index | 20 embedded chunks indexed |
| RAG evaluation | 4 of 4 curated cases passed |
| Foundry evaluation | 2 of 2 hosted-agent smoke cases passed |
| Document extraction | Invoice vendor, customer, dates, subtotal, tax, and total extracted |
| Governance | Automated loan approval marked blocked |

## Business Value

The business value is practical:

- analysts spend less time searching for policy details;
- answers include citations, so review is faster;
- invoice and document fields can be extracted for workflow review;
- risky use cases can be blocked before release;
- evaluation results give leadership a measurable quality signal;
- the same data foundation can later support Power BI reporting.

## Demo Boundaries

- The data is synthetic.
- The project does not approve, deny, or price loans.
- The assistant supports review and research.
- Final credit decisions require authorized human review.
- Power BI is the next reporting layer, not part of the current evidence package.
- Production orchestration with Azure Functions is planned after the current demo evidence.

## Next Build Phase

1. Build the Power BI report for adoption, quality, governance risk, and credit-risk metrics.
2. Add more document templates for loan files, invoices, and compliance reviews.
3. Add a larger Foundry evaluation set with more policy, safety, and citation cases.
4. Record a short demo video or create a small slide deck from this package.
