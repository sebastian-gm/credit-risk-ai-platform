# Deployment Notes

## Dev Foundation

Deployment date:

```text
2026-06-19
```

Subscription:

```text
Lab subscription
```

Tenant:

```text
Project tenant
```

Region:

```text
East US 2
```

Budget:

```text
budget-crai-dev
CAD 50 monthly
Alerts: 50%, 80%, 100%
```

Created resources:

```text
Resource group: rg-crai-dev-eastus2
Storage account: stcraidev6fecno
Data Lake filesystems: raw, processed, curated
Uploaded raw dataset path: raw/synthetic/
Uploaded processed registry path: processed/document_registry/
Uploaded external IFRS9 path: raw/external/credit_risk_ifrs9/
Uploaded IFRS9 profile path: processed/ifrs9/
Key Vault: kv-crai-dev-6fecno
Log Analytics: law-crai-dev
Application Insights: appi-crai-dev
Azure SQL Server: sql-crai-dev-canadacentral-6fecno
Azure SQL Database: sqldb-crai-dev
Azure SQL region: Canada Central
Azure AI Search: srch-crai-dev-canadacentral-6fecno
Azure OpenAI: aoai-crai-dev-eastus2-6fecno
Azure OpenAI deployment: gpt-5-mini
Azure OpenAI embedding deployment: text-embedding-3-small
Document Intelligence: di-crai-dev-eastus2-6fecno
```

Current scope:

- low-cost Azure foundation;
- serverless Azure SQL metadata/analytics layer;
- AI governance registry and audit tables;
- Azure AI Search hybrid vector retrieval layer;
- Azure OpenAI grounded assistant layer;
- RAG evaluation harness;
- Azure AI Document Intelligence invoice extraction layer;
- no real data.

Azure SQL loaded tables:

```text
document_registry: 23 rows
ifrs9_credit_risk: 29,465 rows
ifrs9_default_rate_by_grade: 7 rows
ifrs9_default_rate_by_intent: 6 rows
ifrs9_default_rate_by_home_ownership: 4 rows
ai_use_case_registry: 6 rows
ai_tool_review_checklist: 6 rows
ai_prompt_library: 4 rows
ai_audit_log: 4 rows
```

Azure AI Search loaded index:

```text
credit-risk-documents: 20 chunks
```

Screenshot targets:

- resource group overview;
- storage account containers/filesystems;
- Key Vault overview;
- Log Analytics workspace overview;
- Application Insights overview;
- Azure SQL server and database overview;
- Azure SQL Query editor table counts;
- subscription budget page.
