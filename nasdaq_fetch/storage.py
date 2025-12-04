"""
Storage utilities for saving stock data to CSV or JSON.
"""

from __future__ import annotations

import csv
import json
import logging
import pathlib
from typing import Dict, Iterable, List

logger = logging.getLogger(__name__)


def ensure_parent_dir(path: pathlib.Path) -> None:
    """
    Ensure the parent directory of the given path exists.
    """
    path.parent.mkdir(parents=True, exist_ok=True)


def save_csv(path: str, rows: List[Dict]) -> None:
    """
    Save a list of dictionaries as a CSV file.

    Args:
        path: Path to the output CSV file.
        rows: List of dictionaries, all with the same keys.
    """
    path_obj = pathlib.Path(path)
    ensure_parent_dir(path_obj)

    if not rows:
        logger.warning("No rows to save to CSV at %s.", path_obj)
        return

    columns = list(rows[0].keys())
    logger.debug("CSV columns: %s", columns)

    with path_obj.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)

    logger.info("Saved %d rows to CSV: %s", len(rows), path_obj)


def save_json(path: str, rows: Iterable[Dict]) -> None:
    """
    Save a list (or iterable) of dictionaries as a pretty-printed JSON file.

    Args:
        path: Path to the output JSON file.
        rows: Iterable of dictionaries.
    """
    path_obj = pathlib.Path(path)
    ensure_parent_dir(path_obj)
    rows_list = list(rows)

    with path_obj.open("w", encoding="utf-8") as f:
        json.dump(rows_list, f, ensure_ascii=False, indent=2)

    logger.info("Saved %d objects to JSON: %s", len(rows_list), path_obj)
