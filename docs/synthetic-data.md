# Synthetic Data

The project includes a synthetic lending dataset under:

```text
data/synthetic
```

The dataset is safe for portfolio use because it contains no real applicants,
customers, lenders, bank records, employers, or credit-bureau data.

## Contents

- structured loan applications;
- portfolio performance metrics;
- credit policy documents;
- fair lending and responsible AI policy;
- loan-file checklist policy;
- underwriting memos;
- fraud review notes;
- compliance and governance checklists;
- operations report.

Current generated size:

```text
23 files
6 synthetic loan applications
6 underwriting memos
3 policy documents
3 structured datasets
```

## Generation

The dataset is generated with:

```bash
python3 scripts/generate_synthetic_data.py
```

## Upload

The dataset can be uploaded to the raw Data Lake filesystem with:

```bash
python3 scripts/upload_synthetic_data.py
```

The upload script defaults to Azure CLI key-based storage auth for demo speed.
Set `AZURE_STORAGE_AUTH_MODE=login` if Azure AD data-plane RBAC is configured.

Target:

```text
Storage account: stcraidev6fecno
Filesystem: raw
Path: synthetic/
```

## Public Use Rule

Any screenshot, README section, demo, or portfolio page should describe this as:

```text
Synthetic demo data for a fake lending company.
```
