# Enterprise AI Enablement Platform Plan

## Decision

Recommended domain: **fintech / credit risk operations**.

Why:

- It matches your previous fintech and credit-risk experience.
- It gives stronger AI Engineer portfolio value than a generic construction demo.
- It naturally supports documents, structured data, risk workflows, governance, auditability, Power BI, and cited AI answers.
- It avoids using confidential employer data or unrelated production product data.

Construction was a reasonable option because of your current BI/operations background, but fintech is the better portfolio story for you.

## Project Scenario

Build a fake mid-size fintech company:

**LumaCredit Financial**

LumaCredit processes personal loan and small-business loan applications. Business data is spread across PDFs, Excel files, policy documents, applicant forms, bank statement extracts, credit-risk memos, fraud notes, compliance checklists, and operational reports.

The platform ingests, organizes, classifies, searches, and analyzes this data using Azure. It supports AI assistants and workflows for Credit Risk, Compliance, Operations, Finance, and Leadership.

## Portfolio Summary

This project demonstrates a governed Azure AI platform for a fintech credit-risk operation. It ingests documents and structured data, extracts fields with Document Intelligence, creates a searchable knowledge layer with Azure AI Search, powers cited RAG assistants with Azure OpenAI / Azure AI Foundry, automates credit-risk workflows, and reports adoption, quality, and governance risk in Power BI.

## Target Skills

- AI-103 preparation
- Azure AI Foundry
- Azure OpenAI
- Azure AI Search
- Azure Document Intelligence
- Azure Functions
- Azure Data Lake Gen2
- Azure SQL
- Azure Key Vault
- Managed Identity
- Terraform
- Power BI
- responsible AI and governance

## Phase 0: Setup

Deliverables:

- project README
- architecture plan
- Terraform folder structure
- synthetic data plan
- initial backlog

## Phase 1: Azure Foundation

Build:

- resource group
- storage account / Data Lake Gen2
- Azure SQL
- Key Vault
- managed identity
- Application Insights
- Log Analytics
- Azure Functions placeholder

Deliverables:

- Terraform deployable infrastructure
- environment naming convention
- secrets stored in Key Vault
- local deployment notes

## Phase 2: Synthetic Data

Create fake fintech data:

- loan applications
- applicant profiles
- bank statement summaries
- credit-risk policies
- underwriting memos
- fraud review notes
- compliance checklists
- customer support escalations
- portfolio performance CSVs

Deliverables:

- `/data/raw`
- `/data/synthetic`
- data dictionary
- privacy note explaining all data is fake

## Phase 3: Ingestion

Build:

- upload pipeline
- document registry table
- metadata extraction
- document classification
- ingestion logs

Azure services:

- Data Lake Gen2
- Azure Functions
- Azure SQL

## Phase 4: Document Intelligence

Use Azure AI Document Intelligence to extract:

- loan application fields
- income fields
- employer fields
- invoice or bank-statement-like records
- missing document flags

Deliverables:

- extraction results table
- confidence scores
- validation rules
- failed extraction handling

## Phase 5: Knowledge Layer

Build:

- chunking pipeline
- embeddings
- Azure AI Search index
- metadata filters
- source citations
- department/security labels

Deliverables:

- searchable credit-risk knowledge base
- hybrid search
- vector search
- citation-ready chunks

## Phase 6: AI Assistant

First assistant: **Credit Risk Policy Assistant**

Capabilities:

- answer policy questions with citations
- summarize underwriting rules
- compare applicant facts to policy requirements
- refuse unsupported answers
- show source documents

Second assistant: **Loan File Review Assistant**

Capabilities:

- summarize a loan application file
- identify missing documents
- flag risk factors
- prepare a human-review checklist

## Phase 7: Workflow Automation

Build workflows:

- intake validation
- missing document detection
- risk memo draft
- compliance checklist review
- weekly portfolio summary

Use Azure Functions and SQL-backed workflow tables.

## Phase 8: Governance

Build:

- AI use-case registry
- prompt library
- risk classification
- acceptable-use checklist
- audit log
- human-review rules

Important: do not build an automated loan approval system. The assistant supports analysts; humans make decisions.

## Phase 9: Evaluation

Build:

- golden question set
- expected citations
- groundedness checks
- answer relevance checks
- extraction accuracy tracking
- prompt version tracking

Deliverables:

- evaluation report
- known limitations
- improvement log

## Phase 10: Power BI

Dashboard pages:

- adoption
- document processing
- extraction quality
- RAG answer quality
- workflow throughput
- governance risk
- estimated productivity gain

## Phase 11: Portfolio Packaging

Deliverables:

- polished README
- architecture diagram
- screenshots
- demo video
- website case study
- cost estimate
- security and governance notes
- lessons learned
