#!/usr/bin/env python3
"""Profile the external IFRS9 credit-risk dataset for analytics outputs."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "data" / "external" / "ifrs9" / "credit_risk_dataset_cleaned.csv"
OUT = ROOT / "data" / "processed" / "ifrs9"


def rate_table(df: pd.DataFrame, group_cols: list[str]) -> pd.DataFrame:
    grouped = (
        df.groupby(group_cols, dropna=False)
        .agg(
            loan_count=("loan_status", "size"),
            default_count=("loan_status", "sum"),
            avg_income=("person_income", "mean"),
            avg_loan_amount=("loan_amnt", "mean"),
            avg_interest_rate=("loan_int_rate", "mean"),
            avg_loan_to_income=("loan_to_income_ratio", "mean"),
        )
        .reset_index()
    )
    grouped["default_rate"] = grouped["default_count"] / grouped["loan_count"]
    return grouped


def main() -> None:
    if not SOURCE.exists():
        raise SystemExit(f"Missing source dataset: {SOURCE}")

    OUT.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(SOURCE)

    profile = {
        "generated_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
        "source_file": str(SOURCE.relative_to(ROOT)),
        "license": "CC0: Public Domain",
        "source_url": "https://www.kaggle.com/datasets/laotse/credit-risk-dataset",
        "row_count": int(len(df)),
        "column_count": int(len(df.columns)),
        "columns": list(df.columns),
        "contains_direct_identifiers": False,
        "target": "loan_status",
        "default_count": int(df["loan_status"].sum()),
        "non_default_count": int((df["loan_status"] == 0).sum()),
        "default_rate": float(df["loan_status"].mean()),
        "loan_amount": {
            "min": float(df["loan_amnt"].min()),
            "max": float(df["loan_amnt"].max()),
            "mean": float(df["loan_amnt"].mean()),
        },
        "income": {
            "min": float(df["person_income"].min()),
            "max": float(df["person_income"].max()),
            "mean": float(df["person_income"].mean()),
        },
    }

    (OUT / "ifrs9_profile.json").write_text(json.dumps(profile, indent=2) + "\n", encoding="utf-8")
    rate_table(df, ["loan_grade"]).to_csv(OUT / "default_rate_by_grade.csv", index=False)
    rate_table(df, ["loan_intent"]).to_csv(OUT / "default_rate_by_intent.csv", index=False)
    rate_table(df, ["person_home_ownership"]).to_csv(OUT / "default_rate_by_home_ownership.csv", index=False)

    print(f"Wrote IFRS9 profile outputs to {OUT}")


if __name__ == "__main__":
    main()
