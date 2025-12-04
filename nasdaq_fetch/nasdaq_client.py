"""
Business logic for fetching stock-market data from the Nasdaq screener endpoint.

Responsibilities:
- Handle HTTP requests with retry logic
- Parse the response and return a list of stock dictionaries
"""

from __future__ import annotations

import logging
import time
from typing import Dict, List, Optional

import requests
from requests import Response
from requests.adapters import HTTPAdapter, Retry

logger = logging.getLogger(__name__)

SCREENER_URL = "https://api.nasdaq.com/api/screener/stocks"


def _create_session(retries: int = 3, backoff_factor: float = 1.0) -> requests.Session:
    """
    Create a requests.Session with retry behavior configured.
    """
    session = requests.Session()
    retry_config = Retry(
        total=retries,
        backoff_factor=backoff_factor,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=("GET",),
        raise_on_status=False,
    )
    adapter = HTTPAdapter(max_retries=retry_config)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


def fetch_top_stocks(
    limit: int = 100,
    throttle_s: float = 0.0,
    user_agent: Optional[str] = None,
    session: Optional[requests.Session] = None,
) -> List[Dict]:
    """
    Fetch top `limit` stocks from Nasdaq's public screener endpoint.

    Args:
        limit: How many stock records to fetch (max per request: 100 on this endpoint).
        throttle_s: Seconds to sleep after the request (optional).
        user_agent: Optional custom User-Agent string.
        session: Optional pre-configured requests.Session for testing / reuse.

    Returns:
        List of stock record dictionaries (possibly empty if nothing returned).
    """
    if session is None:
        session = _create_session()

    headers = {
        "User-Agent": user_agent
        or (
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

    logger.info("Fetching top %d stocks from Nasdaq…", limit)
    try:
        response: Response = session.get(
            SCREENER_URL,
            headers=headers,
            params=params,
            timeout=30,
        )
    except requests.RequestException as exc:
        logger.error("Network error while fetching stocks: %s", exc)
        raise

    # Raise for non-2xx, but after retries
    try:
        response.raise_for_status()
    except requests.HTTPError as exc:
        logger.error(
            "HTTP error from Nasdaq API: %s (status %s)", exc, response.status_code
        )
        raise

    try:
        data = response.json()
    except ValueError as exc:
        logger.error("Failed to parse JSON from Nasdaq response: %s", exc)
        raise

    rows = data.get("data", {}).get("table", {}).get("rows", [])
    if not rows:
        logger.warning("No stock data returned from Nasdaq.")
        return []

    if throttle_s > 0:
        logger.debug("Throttling for %s seconds…", throttle_s)
        time.sleep(throttle_s)

    logger.info("Fetched %d stock rows.", min(len(rows), limit))
    return rows[:limit]