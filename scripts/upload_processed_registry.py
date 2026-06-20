#!/usr/bin/env python3
"""Upload processed document registry outputs to the processed Data Lake filesystem."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "processed" / "document_registry"
STORAGE_ACCOUNT = "stcraidev6fecno"
FILESYSTEM = "processed"
AUTH_MODE = os.environ.get("AZURE_STORAGE_AUTH_MODE", "key")


def main() -> None:
    if not SOURCE.exists():
        raise SystemExit("Document registry does not exist. Run src/ingestion/build_document_registry.py first.")

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
        "document_registry",
        "--recursive",
        "--auth-mode",
        AUTH_MODE,
    ]
    subprocess.run(cmd, check=True)


if __name__ == "__main__":
    main()
