# Credit Risk AI Platform

Demo Azure AI platform for a fintech lending operation, built with synthetic data.

This project shows how a company could ingest loan documents, extract fields, create a governed search layer, answer credit-risk questions with citations, automate review workflows, and report quality/adoption metrics in Power BI.

## Status

Early scaffold. No production data. No real lending decisions.

## Business Scenario

The fake company, **LumaCredit Financial**, processes personal and small-business loan applications. Its teams work across PDFs, application forms, bank-statement summaries, underwriting memos, policy documents, fraud notes, compliance checklists, and operational reports.

The platform supports:

- Credit Risk
- Compliance
- Operations
- Fraud / Risk Ops
- Finance
- Leadership

## What This Demonstrates

- Azure infrastructure with Terraform
- Azure Data Lake Gen2 document storage
- Azure SQL metadata and workflow tables
- Azure Document Intelligence extraction
- Azure AI Search indexing
- Azure OpenAI / Azure AI Foundry RAG assistants
- cited answers and source tracking
- evaluation sets and quality metrics
- governance, audit logging, and human review
- Power BI dashboard design

## Repository Structure

```text
.
├── data/                  # synthetic raw/processed/curated data placeholders
├── docs/                  # architecture, data, governance, and Azure notes
├── infra/terraform/       # Azure infrastructure as code
├── scripts/               # local generation and upload helpers
├── src/                   # Python ingestion, extraction, RAG, and evaluation code
└── PROJECT_PLAN.md
```

## Important Limitations

- This is a portfolio demo built with synthetic data.
- It is not a credit approval system.
- AI output supports human analysts; it does not make final lending decisions.
- No real applicant, customer, employer, bank, or credit-bureau data should be committed.

## First Milestone

Build the Azure foundation:

- Resource group
- Data Lake Gen2
- Azure SQL
- Key Vault
- Application Insights
- Log Analytics
- Terraform environment structure

Then add synthetic data and ingestion.

## Synthetic Data

The project includes generated synthetic lending data under `data/synthetic`.
It is safe for public portfolio use and does not contain real applicant data.

Generate or refresh it with:

```bash
python3 scripts/generate_synthetic_data.py
```

Upload it to the raw Data Lake filesystem with:

```bash
python3 scripts/upload_synthetic_data.py
```
