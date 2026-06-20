# External Dataset Assessment

## Reviewed Repositories

Two existing credit-risk repositories were reviewed as candidate data sources:

```text
credit_risk_IFRS9_ECL_model
pd_predictive_modeling
```

## Summary

The `credit_risk_IFRS9_ECL_model` repository is a good fit for the structured
credit-risk analytics layer. It contains CSV data with loan-level borrower and
loan attributes that can support portfolio analytics, risk segmentation, model
monitoring examples, and Power BI reporting.

The `pd_predictive_modeling` repository is useful as prior modeling work, but
its data is stored as train/test pickle artifacts. That makes it less suitable
as a transparent public data source for this platform.

## Candidate Dataset: IFRS 9 Credit Risk CSV

Source files reviewed:

```text
data/credit_risk_dataset.csv
data/credit_risk_dataset_cleaned.csv
```

Observed structure:

```text
Raw rows: 32,581
Cleaned rows: 29,465
Columns: 13 in cleaned file
Target: loan_status
Default rows: 6,464
Non-default rows: 23,001
```

Key fields:

- person age
- person income
- home ownership
- employment length
- loan intent
- loan grade
- loan amount
- interest rate
- loan status
- loan percent income
- prior default flag
- credit history length
- loan-to-income ratio

## Candidate Dataset: PD Predictive Modeling Artifacts

Files reviewed:

```text
data/X_train.pkl
data/X_test.pkl
data/y_train.pkl
data/y_test.pkl
```

Observed structure:

```text
Training rows: 800
Test rows: 200
Feature count: 48
Format: joblib/pandas binary artifacts
```

This data appears to be based on the German Credit dataset and includes
encoded features such as checking account status, credit history, employment
duration, housing, job, telephone, and foreign worker indicators.

## Recommendation

Use the IFRS 9 credit-risk CSV as an **external structured analytics source**,
not as a replacement for the synthetic document dataset.

Keep the current synthetic dataset because it provides:

- policy documents;
- underwriting memos;
- compliance checklists;
- fraud notes;
- operations reports;
- files for ingestion and metadata classification;
- source documents for RAG citations.

Use the IFRS 9 CSV for:

- portfolio analytics;
- Power BI dashboard metrics;
- Azure SQL fact tables;
- risk-band and default-rate examples;
- model monitoring examples;
- future responsible-AI evaluation examples.

## License Confirmation

The Kaggle page for `laotse/credit-risk-dataset` exposes structured dataset
metadata that lists:

```text
License: CC0: Public Domain
License URL: https://creativecommons.org/publicdomain/zero/1.0/
```

Because the license is CC0, the cleaned CSV can be included with attribution
and source documentation.

## Decision

Current direction:

```text
Synthetic documents: keep
IFRS 9 CSV: include as structured portfolio/risk analytics source
PD pickle artifacts: do not use as primary platform data source
```
