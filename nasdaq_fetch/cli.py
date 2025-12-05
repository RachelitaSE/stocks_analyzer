"""
Command-line interface for the Nasdaq stock downloader.

Usage examples:
    nasdaq-stocks
    nasdaq-stocks --top 50
    nasdaq-stocks --format json --out data/stocks.json
    nasdaq-stocks --top 10 --throttle 0.5 --verbose
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path
from typing import Literal

from nasdaq_client import fetch_top_stocks
from storage import save_csv, save_json

logger = logging.getLogger(__name__)

_DEAFAULT_DATA_PATH = f'{Path.home()}/.stocks_analyzer/data'


def _configure_logging(verbose: bool, quiet: bool) -> None:
    """
    Configure the root logger based on verbosity options.
    """
    if quiet:
        level = logging.WARNING
    elif verbose:
        level = logging.DEBUG
    else:
        level = logging.INFO

    logging.basicConfig(
        level=level,
        format="%(levelname)s: %(message)s",
    )


def _infer_format_from_path(path: Path) -> Literal["csv", "json"]:
    """
    Infer file format from file extension, defaulting to CSV if unknown.
    """
    suffix = path.suffix.lower()
    if suffix == ".json":
        return "json"
    return "csv"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download stock data from Nasdaq and save as CSV or JSON."
    )

    parser.add_argument(
        "--top",
        type=int,
        default=100,
        help="Number of top stocks to fetch (default: 100).",
    )
    parser.add_argument(
        "--format",
        choices=["csv", "json", "auto"],
        default="auto",
        help=(
            "Output file format: csv, json, or auto (infer from --out extension). "
            "Default: auto."
        ),
    )
    parser.add_argument(
        "--out",
        default=_DEAFAULT_DATA_PATH,
        help=f"Output data path (Defaults to {_DEAFAULT_DATA_PATH}).",
    )
    parser.add_argument(
        "--throttle",
        type=float,
        default=0.0,
        help="Seconds to wait after the request (for politeness).",
    )
    parser.add_argument(
        "--user-agent",
        default=None,
        help="Custom User-Agent header (optional).",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite output file if it already exists.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose (debug) logging.",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Only show warnings and errors.",
    )

    args = parser.parse_args(argv)

    # Basic validation
    if args.top <= 0:
        parser.error("--top must be a positive integer.")

    if args.throttle < 0:
        parser.error("--throttle cannot be negative.")

    if args.verbose and args.quiet:
        parser.error("Cannot use --verbose and --quiet at the same time.")

    return args


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    _configure_logging(args.verbose, args.quiet)

    out_path = Path(args.out)

    # Decide format (csv/json)
    if args.format == "auto":
        file_format: Literal["csv", "json"] = _infer_format_from_path(out_path)
        logger.debug("Inferred format '%s' from output path %s", file_format, out_path)
    else:
        file_format = args.format

    # Overwrite protection
    path = out_path.joinpath(f'top{args.top}.{file_format}')
    if path.exists() and not args.force:
        logger.error("Output file already exists: %s (use --force to overwrite)", path)
        return 1

    try:
        stocks = fetch_top_stocks(
            limit=args.top,
            throttle_s=args.throttle,
            user_agent=args.user_agent,
        )
    except Exception as exc:  # broad catch to turn into exit code
        logger.error("Failed to fetch stock data: %s", exc)
        return 1

    if not stocks:
        logger.warning("No stocks were fetched. Nothing to save.")
        return 0

    if file_format == "csv":
        save_csv(str(path), stocks)
    else:
        save_json(str(path), stocks)

    logger.info("Done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())