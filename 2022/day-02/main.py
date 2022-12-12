from __future__ import annotations

import argparse as ap
import logging
import sys

from pathlib import Path
from typing import Sequence
from logging.handlers import RotatingFileHandler

from solution import _DAY_NUMBER, run_solution

logger = logging.getLogger(__name__)


def _parse_args(argv: Sequence[str] | None = None) -> ap.Namespace:
    parser = ap.ArgumentParser(
        prog=f"aoc-2022-{_DAY_NUMBER:02}",
        description=f"Advent of Code Day {_DAY_NUMBER:02} Solution",
        formatter_class=ap.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "--debug",
        default=False,
        required=False,
        action="store_true",
        help="Enable verbose debug logging",
    )

    return parser.parse_args(argv)


def _configure_logging(debug: bool) -> None:
    log_path = Path("./logs")
    log_path.mkdir(parents=True, exist_ok=True)
    log_file_path = log_path.joinpath(f"log_day_{_DAY_NUMBER:02}.log").resolve()

    log_message_fmt = "{asctime}.{msecs:03.0f} - {levelname:<8} - {name}.{funcName}.{lineno:04d} - {message}"
    log_datetime_fmt = "%Y-%m-%dT%H:%M:%S"
    msg_formatter = logging.Formatter(fmt=log_message_fmt, datefmt=log_datetime_fmt, style="{")
    rotating_log_handler = RotatingFileHandler(
        filename=log_file_path,
        mode="a",
        maxBytes=268435456,
        backupCount=8,
        encoding="utf-8",
    )
    stdout_handler = logging.StreamHandler(stream=sys.stdout)

    rotating_log_handler.setFormatter(msg_formatter)
    stdout_handler.setFormatter(msg_formatter)

    root_logger = logging.getLogger()

    if debug:
        root_logger.setLevel(logging.DEBUG)
    else:
        root_logger.setLevel(logging.INFO)

    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    root_logger.addHandler(stdout_handler)
    root_logger.addHandler(rotating_log_handler)

    return None


def main(argv: Sequence[str] | None = None) -> int:
    args = _parse_args(argv)
    _configure_logging(args.debug)
    return run_solution()


if __name__ == "__main__":
    exit(main())
