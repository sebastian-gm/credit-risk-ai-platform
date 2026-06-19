# Synthetic Data Plan

All data in this project must be fake.

## Data Domains

- loan applications
- applicant profiles
- bank-statement summaries
- income verification documents
- underwriting memos
- credit-risk policy documents
- fraud review notes
- compliance checklists
- customer support escalations
- portfolio performance files

## Example Files

```text
data/raw/loan_applications/
data/raw/policies/
data/raw/underwriting_memos/
data/raw/fraud_notes/
data/raw/compliance/
data/raw/portfolio/
```

## Required Metadata

- document_id
- file_name
- document_type
- department
- sensitivity_label
- source_system
- ingestion_timestamp
- owner
- retention_category

## Sensitivity Labels

- public_demo
- internal
- confidential_synthetic
- pii_synthetic

## Rule

Never use real applicant, customer, bank, employer, credit-bureau, or company-confidential data.

