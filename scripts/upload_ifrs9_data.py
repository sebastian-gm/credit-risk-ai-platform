#!/usr/bin/env python3
"""Upload IFRS9 external raw data and processed profile outputs to Data Lake."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STORAGE_ACCOUNT = "stcraidev6fecno"
AUTH_MODE = os.environ.get("AZURE_STORAGE_AUTH_MODE", "key")


def upload(source: Path, filesystem: str, destination: str) -> None:
    if not source.exists():
        raise SystemExit(f"Missing upload source: {source}")

    cmd = [
        "az",
        "storage",
        "fs",
        "directory",
        "upload",
        "--account-name",
        STORAGE_ACCOUNT,
        "--file-system",
        filesystem,
        "--source",
        str(source / "*"),
        "--destination-path",
        destination,
        "--recursive",
        "--auth-mode",
        AUTH_MODE,
    ]
    subprocess.run(cmd, check=True)


def main() -> None:
    upload(ROOT / "data" / "external" / "ifrs9", "raw", "external/credit_risk_ifrs9")
    upload(ROOT / "data" / "processed" / "ifrs9", "processed", "ifrs9")


if __name__ == "__main__":
    main()
