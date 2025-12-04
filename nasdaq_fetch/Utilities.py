# day04/fetcher.py
"""
Business logic for Day 04 assignment: fetch and save stock-market data
from the Nasdaq screener endpoint.

No UI elements here — only functions that:
- fetch stock data from Nasdaq API
- save results to CSV or JSON
"""

import requests
import pathlib
import csv
import json
import time
from typing import List, Dict, Optional

# Public Nasdaq endpoint for the stock screener
SCREENER_URL = "https://api.nasdaq.com/api/screener/stocks"


def fetch_top_stocks(
    limit: int = 100,
    throttle_s: float = 0.0,
    user_agent: Optional[str] = None
) -> List[Dict]:
    """
    Fetch top 'limit' stocks from Nasdaq's public screener endpoint.

    Args:
        limit: how many stock records to fetch
        throttle_s: seconds to sleep after each request (optional)
        user_agent: optional custom User-Agent string

    Returns:
        List of stock record dictionaries.
    """
    headers = {
    "User-Agent": user_agent or (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/119.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "en-US,en;q=0.9",
    "Origin": "https://www.nasdaq.com",
    "Referer": "https://www.nasdaq.com/market-activity/stocks",
    "Connection": "keep-alive",
    }
    params = {"tableonly": True, "limit": limit, "offset": 0}

    print(f"Fetching top {limit} stocks from Nasdaq…")
    response = requests.get(SCREENER_URL, headers=headers, params=params, timeout=30)
    response.raise_for_status()

    data = response.json()
    # The table of stock data is under data.table.rows
    rows = data.get("data", {}).get("table", {}).get("rows", [])
    if not rows:
        print("Warning: No data returned.")
        return []

    if throttle_s:
        time.sleep(throttle_s)

    return rows[:limit]


def save_csv(path: str, rows: List[Dict]) -> None:
    """
    Save a list of dictionaries as a CSV file.
    """
    path_obj = pathlib.Path(path)
    path_obj.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        print("No rows to save.")
        return

    columns = list(rows[0].keys())
    with path_obj.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)

    print(f"Saved {len(rows)} rows to {path_obj}")


def save_json(path: str, rows: List[Dict]) -> None:
    """
    Save a list of dictionaries as a JSON file.
    """
    path_obj = pathlib.Path(path)
    path_obj.parent.mkdir(parents=True, exist_ok=True)
    with path_obj.open("w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)

    print(f"Saved {len(rows)} objects to {path_obj}")


if __name__ == "__main__":
    # Example standalone usage
    stocks = fetch_top_stocks(limit=10)
    save_csv("day04/data/top10.csv", stocks)
