# Demo Walkthrough

This walkthrough shows the current end-to-end demo evidence for the Credit Risk AI Platform. All data is synthetic.

## Demo Goal

Show that the platform can:

- store governed credit-risk data in Azure SQL
- retrieve trusted policy sources from Azure AI Search
- answer a credit-risk question with citations using Azure OpenAI
- extract invoice fields with Azure AI Document Intelligence
- evaluate retrieval and answer quality
- track governance decisions and blocked use cases

## 1. Data and Governance Load

Evidence file:

- [sql-row-counts.txt](evidence/sql-row-counts.txt)

Current SQL evidence:

```text
document_registry: 23
ifrs9_credit_risk: 29465
ai_use_case_registry: 6
ai_tool_review_checklist: 6
ai_prompt_library: 4
ai_audit_log: 4
```

This proves the demo has document metadata, structured credit-risk data, and governance tables loaded into Azure SQL.

## 2. Hybrid Retrieval

Evidence file:

- [search-query-results.txt](evidence/search-query-results.txt)

Demo question:

```text
What policy applies when debt-to-income is above 45%?
```

The search layer returns the policy source first:

```text
1. Credit Policy 2026
citation: raw/synthetic/policies/credit_policy_2026.md
```

The query runs in hybrid mode when embeddings are available:

```text
Mode: hybrid vector + keyword
```

## 3. Grounded Assistant Answer

Evidence file:

- [rag-assistant-answer.txt](evidence/rag-assistant-answer.txt)

Assistant answer:

```text
Applications with a debt-to-income ratio above 45% require an exception review.
```

Returned citations include:

```text
raw/synthetic/policies/credit_policy_2026.md
raw/synthetic/underwriting_memos/APP-2026-0001_memo.md
raw/synthetic/underwriting_memos/APP-2026-0006_memo.md
raw/synthetic/underwriting_memos/APP-2026-0004_memo.md
```

This proves the assistant is using retrieved context and showing source paths instead of giving an unsupported answer.

## 4. Document Intelligence Extraction

Evidence files:

- [invoice-extraction-output.txt](evidence/invoice-extraction-output.txt)
- [invoice-extraction-summary.json](evidence/invoice-extraction-summary.json)

Extracted fields:

```text
VendorName: Northstar Office Supplies
CustomerName: LumaCredit Finance Operations
InvoiceId: INV-2026-1042
InvoiceDate: 2026-06-15
DueDate: 2026-07-15
SubTotal: USD 1,525.00
TotalTax: USD 106.75
InvoiceTotal: USD 1,631.75
```

The evidence is from a generated synthetic invoice. No real vendor, customer, or payment data is used.

## 5. RAG Evaluation

Evidence files:

- [rag-evaluation-console.txt](evidence/rag-evaluation-console.txt)
- [rag-evaluation-results.md](evidence/rag-evaluation-results.md)
- [rag-evaluation-results.json](evidence/rag-evaluation-results.json)

Current evaluation summary:

```text
case_count: 4
retrieval_hit_rate_at_5: 1.00
answer_non_empty_rate: 1.00
answer_term_pass_rate: 1.00
mean_reciprocal_rank: 0.875
all_cases_passed: true
```

The evaluation covers:

- DTI exception policy
- small-business required documents
- missing-document routing
- prohibited automated loan approval

## 6. Governance Review

Governance source files:

- [../src/governance/ai_use_case_registry.csv](../src/governance/ai_use_case_registry.csv)
- [../src/governance/ai_tool_review_checklist.csv](../src/governance/ai_tool_review_checklist.csv)
- [../src/governance/prompt_library.csv](../src/governance/prompt_library.csv)
- [../src/governance/ai_audit_log_seed.csv](../src/governance/ai_audit_log_seed.csv)

Key governance evidence:

```text
UC-001 Credit Policy Assistant: Demo, citations required
UC-004 Invoice Field Extraction: Demo, finance reviewer validates totals
UC-006 Fully Automated Loan Approval: Blocked, not approved for demo
```

The tool review checklist intentionally fails the automated-loan-approval use case:

```text
CHK-006, UC-006, Acceptable Use, Failed, Fully automated loan approval is prohibited
```

This proves the demo includes an AI governance layer, not only retrieval and extraction scripts.

## 7. Azure AI Foundry Check

Evidence file:

- [foundry-project-summary.md](evidence/foundry/foundry-project-summary.md)

Foundry resource group:

```text
rg-crai-foundry-dev-eastus2
```

Foundry project endpoint:

```text
https://ai-account-dosuleocw4nxo.services.ai.azure.com/api/projects/crai-foundry-project
```

The `gpt-5-mini` deployment is running on the Foundry account and supports both
Responses and Agents v2. A hosted `credit-policy-assistant` agent is deployed,
uses Azure AI Search for grounding, and returns source-path citations.

Remote agent evidence:

- [hosted-agent-invoke-output.txt](evidence/foundry/hosted-agent-invoke-output.txt)
- [hosted-agent-playground.png](evidence/foundry/hosted-agent-playground.png)

## Demo Script

Use this sequence when showing the project:

1. Open the architecture diagram and explain the workflow from documents to governed answers.
2. Show `sql-row-counts.txt` to prove the data and governance tables are loaded.
3. Show `search-query-results.txt` for the DTI policy question.
4. Show `rag-assistant-answer.txt` to show the cited assistant answer.
5. Show `invoice-extraction-summary.json` for Document Intelligence extraction.
6. Show `rag-evaluation-results.md` to prove the assistant behavior is measured.
7. Show the blocked `UC-006` use case in the governance registry.
8. Show `hosted-agent-invoke-output.txt` to prove the Foundry hosted agent is working with Search grounding.

## Evidence Snapshot

A portfolio-friendly screenshot summary is saved here:

- [evidence-summary.png](evidence/evidence-summary.png)

Azure Portal screenshots are saved here:

- [azure-portal/](evidence/azure-portal/)

## Notes

- This is a portfolio demo using synthetic data.
- It does not approve, deny, or price loans.
- Final credit decisions require human review.
- Secrets and local environment files are not committed.
