# IFRS 9 Structured Credit-Risk Dataset

The platform uses the Kaggle `Credit Risk Dataset` by Lao Tse as an external
structured analytics source.

## License

Kaggle metadata lists the dataset license as:

```text
CC0: Public Domain
```

Source:

```text
https://www.kaggle.com/datasets/laotse/credit-risk-dataset
```

License URL:

```text
https://creativecommons.org/publicdomain/zero/1.0/
```

## Role In This Project

This dataset is used for:

- structured credit-risk analytics;
- Azure SQL fact tables;
- portfolio default-rate summaries;
- Power BI dashboard metrics;
- model-monitoring examples.

It is not used as the only project data source because it does not provide
business documents for RAG, citations, policy lookup, or document governance.

## Profile Outputs

Generate profile outputs with:

```bash
python3 src/ingestion/profile_ifrs9_dataset.py
```

Outputs:

```text
data/processed/ifrs9/ifrs9_profile.json
data/processed/ifrs9/default_rate_by_grade.csv
data/processed/ifrs9/default_rate_by_intent.csv
data/processed/ifrs9/default_rate_by_home_ownership.csv
```

Upload raw and processed IFRS9 assets:

```bash
python3 scripts/upload_ifrs9_data.py
```

Data Lake targets:

```text
raw/external/credit_risk_ifrs9/
processed/ifrs9/
```

