"""Input/output helpers used by the analysis scripts."""
from __future__ import annotations

from pathlib import Path
import pandas as pd


def ensure_parent(path: Path) -> None:
    """Create the parent directory for a file path when it does not exist."""
    path.parent.mkdir(parents=True, exist_ok=True)


def read_csv(path: Path) -> pd.DataFrame:
    """Read a UTF-8 CSV file and preserve missing values consistently."""
    return pd.read_csv(path, encoding="utf-8")


def write_csv(df: pd.DataFrame, path: Path) -> None:
    """Write a CSV file with UTF-8 BOM for compatibility with Excel."""
    ensure_parent(path)
    df.to_csv(path, index=False, encoding="utf-8-sig")
