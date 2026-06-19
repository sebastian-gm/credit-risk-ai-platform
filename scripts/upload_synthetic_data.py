#!/usr/bin/env python3
"""Upload committed synthetic data to the raw Data Lake filesystem using Azure CLI."""

from __future__ import annotations

import subprocess
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "synthetic"
STORAGE_ACCOUNT = "stcraidev6fecno"
FILESYSTEM = "raw"
AUTH_MODE = os.environ.get("AZURE_STORAGE_AUTH_MODE", "key")


def main() -> None:
    if not SOURCE.exists():
        raise SystemExit("Synthetic data folder does not exist. Run scripts/generate_synthetic_data.py first.")

    cmd = [
        "az",
        "storage",
        "fs",
        "directory",
        "upload",
        "--account-name",
        STORAGE_ACCOUNT,
        "--file-system",
        FILESYSTEM,
        "--source",
        str(SOURCE / "*"),
        "--destination-path",
        "synthetic",
        "--recursive",
        "--auth-mode",
        AUTH_MODE,
    ]
    subprocess.run(cmd, check=True)


if __name__ == "__main__":
    main()
