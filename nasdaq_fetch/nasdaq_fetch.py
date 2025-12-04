# day04/app.py
"""
User interface (CLI) for Day04 assignment.
Uses functions from Utilities.py to get stock data from Nasdaq and save it locally.
"""

import argparse
from Utilities import fetch_top_stocks, save_csv, save_json


def main():
    parser = argparse.ArgumentParser(
        description="Download stock data from Nasdaq and save as CSV or JSON."
    )
    parser.add_argument(
        "--top",
        type=int,
        default=100,
        help="Number of top stocks to fetch (default: 100)",
    )
    parser.add_argument(
        "--format",
        choices=["csv", "json"],
        default="csv",
        help="Output file format (csv or json)",
    )
    parser.add_argument(
        "--out",
        default="day04/data/stocks.csv",
        help="Output file path (e.g. day04/data/stocks.csv)",
    )
    parser.add_argument(
        "--throttle",
        type=float,
        default=0.0,
        help="Seconds to wait between requests (optional)",
    )
    parser.add_argument(
        "--user-agent",
        default=None,
        help="Custom User-Agent header (optional)",
    )

    args = parser.parse_args()

    # Fetch data
    stocks = fetch_top_stocks(
        limit=args.top,
        throttle_s=args.throttle,
        user_agent=args.user_agent,
    )

    # Save in chosen format
    if args.format == "csv":
        save_csv(args.out, stocks)
    else:
        save_json(args.out, stocks)


if __name__ == "__main__":
    main()
