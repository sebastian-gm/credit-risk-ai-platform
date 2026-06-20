#!/usr/bin/env python3
"""Query Azure SQL row counts for demo verification."""

from __future__ import annotations

import os

import pymssql

TABLES = [
    "document_registry",
    "ifrs9_credit_risk",
    "ifrs9_default_rate_by_grade",
    "ifrs9_default_rate_by_intent",
    "ifrs9_default_rate_by_home_ownership",
]


def env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise SystemExit(f"Missing required environment variable: {name}")
    return value


def main() -> None:
    with pymssql.connect(
        server=env("SQL_SERVER"),
        user=env("SQL_USER"),
        password=env("SQL_PASSWORD"),
        database=env("SQL_DATABASE"),
        login_timeout=30,
        timeout=60,
    ) as conn:
        cursor = conn.cursor()
        for table in TABLES:
            cursor.execute(f"SELECT COUNT(*) FROM dbo.{table};")
            count = cursor.fetchone()[0]
            print(f"{table}: {count}")


if __name__ == "__main__":
    main()
