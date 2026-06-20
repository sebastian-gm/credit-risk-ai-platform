#!/usr/bin/env python3
"""Load document registry and IFRS9 analytics data into Azure SQL."""

from __future__ import annotations

import os
from pathlib import Path

import pandas as pd
import pymssql

ROOT = Path(__file__).resolve().parents[1]

DOCUMENT_REGISTRY = ROOT / "data" / "processed" / "document_registry" / "document_registry.csv"
IFRS9 = ROOT / "data" / "external" / "ifrs9" / "credit_risk_dataset_cleaned.csv"
IFRS9_BY_GRADE = ROOT / "data" / "processed" / "ifrs9" / "default_rate_by_grade.csv"
IFRS9_BY_INTENT = ROOT / "data" / "processed" / "ifrs9" / "default_rate_by_intent.csv"
IFRS9_BY_HOME = ROOT / "data" / "processed" / "ifrs9" / "default_rate_by_home_ownership.csv"


def env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise SystemExit(f"Missing required environment variable: {name}")
    return value


def connect() -> pymssql.Connection:
    return pymssql.connect(
        server=env("SQL_SERVER"),
        user=env("SQL_USER"),
        password=env("SQL_PASSWORD"),
        database=env("SQL_DATABASE"),
        login_timeout=30,
        timeout=120,
    )


def sql_literal(value: object) -> str:
    if pd.isna(value):
        return "NULL"
    if isinstance(value, bool):
        return "1" if value else "0"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        return repr(value)
    escaped = str(value).replace("'", "''")
    return f"N'{escaped}'"


def insert_chunks(cursor: pymssql.Cursor, table: str, columns: list[str], rows: list[tuple], chunk_size: int = 500) -> None:
    if not rows:
        return

    column_sql = ", ".join(columns)
    for start in range(0, len(rows), chunk_size):
        chunk = rows[start : start + chunk_size]
        values_sql = ",\n".join(
            "(" + ", ".join(sql_literal(value) for value in row) + ")"
            for row in chunk
        )
        cursor.execute(f"INSERT INTO dbo.{table} ({column_sql}) VALUES {values_sql};")


def create_schema(cursor: pymssql.Cursor) -> None:
    cursor.execute(
        """
        IF OBJECT_ID('dbo.document_registry', 'U') IS NOT NULL DROP TABLE dbo.document_registry;
        IF OBJECT_ID('dbo.ifrs9_default_rate_by_grade', 'U') IS NOT NULL DROP TABLE dbo.ifrs9_default_rate_by_grade;
        IF OBJECT_ID('dbo.ifrs9_default_rate_by_intent', 'U') IS NOT NULL DROP TABLE dbo.ifrs9_default_rate_by_intent;
        IF OBJECT_ID('dbo.ifrs9_default_rate_by_home_ownership', 'U') IS NOT NULL DROP TABLE dbo.ifrs9_default_rate_by_home_ownership;
        IF OBJECT_ID('dbo.ifrs9_credit_risk', 'U') IS NOT NULL DROP TABLE dbo.ifrs9_credit_risk;

        CREATE TABLE dbo.document_registry (
            document_id NVARCHAR(32) NOT NULL PRIMARY KEY,
            file_name NVARCHAR(260) NOT NULL,
            relative_path NVARCHAR(500) NOT NULL,
            raw_data_lake_path NVARCHAR(600) NOT NULL,
            document_type NVARCHAR(80) NOT NULL,
            department NVARCHAR(100) NOT NULL,
            sensitivity_label NVARCHAR(80) NOT NULL,
            owner NVARCHAR(100) NOT NULL,
            retention_category NVARCHAR(100) NOT NULL,
            source_system NVARCHAR(100) NOT NULL,
            mime_type NVARCHAR(120) NOT NULL,
            file_size_bytes BIGINT NOT NULL,
            sha256 CHAR(64) NOT NULL,
            ingestion_timestamp DATETIMEOFFSET NOT NULL,
            contains_real_data BIT NOT NULL,
            ready_for_search_index BIT NOT NULL
        );

        CREATE TABLE dbo.ifrs9_credit_risk (
            credit_risk_id INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
            person_age FLOAT NOT NULL,
            person_income FLOAT NOT NULL,
            person_home_ownership NVARCHAR(40) NOT NULL,
            person_emp_length FLOAT NOT NULL,
            loan_intent NVARCHAR(60) NOT NULL,
            loan_grade NVARCHAR(5) NOT NULL,
            loan_amnt FLOAT NOT NULL,
            loan_int_rate FLOAT NOT NULL,
            loan_status INT NOT NULL,
            loan_percent_income FLOAT NOT NULL,
            cb_person_default_on_file NVARCHAR(5) NOT NULL,
            cb_person_cred_hist_length INT NOT NULL,
            loan_to_income_ratio FLOAT NOT NULL
        );

        CREATE TABLE dbo.ifrs9_default_rate_by_grade (
            loan_grade NVARCHAR(5) NOT NULL PRIMARY KEY,
            loan_count INT NOT NULL,
            default_count INT NOT NULL,
            avg_income FLOAT NOT NULL,
            avg_loan_amount FLOAT NOT NULL,
            avg_interest_rate FLOAT NOT NULL,
            avg_loan_to_income FLOAT NOT NULL,
            default_rate FLOAT NOT NULL
        );

        CREATE TABLE dbo.ifrs9_default_rate_by_intent (
            loan_intent NVARCHAR(60) NOT NULL PRIMARY KEY,
            loan_count INT NOT NULL,
            default_count INT NOT NULL,
            avg_income FLOAT NOT NULL,
            avg_loan_amount FLOAT NOT NULL,
            avg_interest_rate FLOAT NOT NULL,
            avg_loan_to_income FLOAT NOT NULL,
            default_rate FLOAT NOT NULL
        );

        CREATE TABLE dbo.ifrs9_default_rate_by_home_ownership (
            person_home_ownership NVARCHAR(40) NOT NULL PRIMARY KEY,
            loan_count INT NOT NULL,
            default_count INT NOT NULL,
            avg_income FLOAT NOT NULL,
            avg_loan_amount FLOAT NOT NULL,
            avg_interest_rate FLOAT NOT NULL,
            avg_loan_to_income FLOAT NOT NULL,
            default_rate FLOAT NOT NULL
        );
        """
    )


def load_document_registry(cursor: pymssql.Cursor) -> int:
    df = pd.read_csv(DOCUMENT_REGISTRY)
    df["contains_real_data"] = df["contains_real_data"].astype(bool).astype(int)
    df["ready_for_search_index"] = df["ready_for_search_index"].astype(bool).astype(int)
    rows = [tuple(row) for row in df.itertuples(index=False, name=None)]
    insert_chunks(
        cursor,
        "document_registry",
        [
            "document_id",
            "file_name",
            "relative_path",
            "raw_data_lake_path",
            "document_type",
            "department",
            "sensitivity_label",
            "owner",
            "retention_category",
            "source_system",
            "mime_type",
            "file_size_bytes",
            "sha256",
            "ingestion_timestamp",
            "contains_real_data",
            "ready_for_search_index",
        ],
        rows,
    )
    return len(rows)


def load_ifrs9(cursor: pymssql.Cursor) -> int:
    df = pd.read_csv(IFRS9)
    rows = [tuple(row) for row in df.itertuples(index=False, name=None)]
    insert_chunks(
        cursor,
        "ifrs9_credit_risk",
        [
            "person_age",
            "person_income",
            "person_home_ownership",
            "person_emp_length",
            "loan_intent",
            "loan_grade",
            "loan_amnt",
            "loan_int_rate",
            "loan_status",
            "loan_percent_income",
            "cb_person_default_on_file",
            "cb_person_cred_hist_length",
            "loan_to_income_ratio",
        ],
        rows,
    )
    return len(rows)


def load_summary(cursor: pymssql.Cursor, path: Path, table: str, key_column: str) -> int:
    df = pd.read_csv(path)
    rows = [tuple(row) for row in df.itertuples(index=False, name=None)]
    insert_chunks(
        cursor,
        table,
        [
            key_column,
            "loan_count",
            "default_count",
            "avg_income",
            "avg_loan_amount",
            "avg_interest_rate",
            "avg_loan_to_income",
            "default_rate",
        ],
        rows,
    )
    return len(rows)


def main() -> None:
    for path in [DOCUMENT_REGISTRY, IFRS9, IFRS9_BY_GRADE, IFRS9_BY_INTENT, IFRS9_BY_HOME]:
        if not path.exists():
            raise SystemExit(f"Missing required input file: {path}")

    with connect() as conn:
        cursor = conn.cursor()
        create_schema(cursor)
        counts = {
            "document_registry": load_document_registry(cursor),
            "ifrs9_credit_risk": load_ifrs9(cursor),
            "ifrs9_default_rate_by_grade": load_summary(cursor, IFRS9_BY_GRADE, "ifrs9_default_rate_by_grade", "loan_grade"),
            "ifrs9_default_rate_by_intent": load_summary(cursor, IFRS9_BY_INTENT, "ifrs9_default_rate_by_intent", "loan_intent"),
            "ifrs9_default_rate_by_home_ownership": load_summary(
                cursor,
                IFRS9_BY_HOME,
                "ifrs9_default_rate_by_home_ownership",
                "person_home_ownership",
            ),
        }
        conn.commit()

    for table, count in counts.items():
        print(f"{table}: {count} rows loaded")


if __name__ == "__main__":
    main()
