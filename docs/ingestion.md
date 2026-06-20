# Ingestion

The first ingestion step creates a document registry from the synthetic dataset.

## Build Registry

```bash
python3 src/ingestion/build_document_registry.py
```

Outputs:

```text
data/processed/document_registry/document_registry.csv
data/processed/document_registry/document_registry.json
data/processed/document_registry/document_registry_summary.json
```

## Upload Registry

```bash
python3 scripts/upload_processed_registry.py
```

Target:

```text
Storage account: stcraidev6fecno
Filesystem: processed
Path: document_registry/
```

## Registry Fields

- document ID
- file name
- source path
- raw Data Lake path
- document type
- department
- sensitivity label
- owner
- retention category
- source system
- MIME type
- file size
- SHA-256 hash
- ingestion timestamp
- real-data flag
- search readiness flag

## Purpose

This registry becomes the bridge between raw document storage, Azure SQL metadata,
AI Search indexing, governance reporting, and Power BI metrics.

## Current Demo Output

The current synthetic dataset produces:

```text
Document records: 23
Contains real data: false
```

Document type counts:

```text
dataset_note: 1
governance_document: 2
fraud_review_note: 1
loan_application: 6
operations_report: 1
policy: 3
structured_dataset: 3
underwriting_memo: 6
```

Department counts:

```text
Analytics: 4
Compliance: 5
Fraud / Risk Ops: 1
Credit Risk: 12
Operations: 1
```
