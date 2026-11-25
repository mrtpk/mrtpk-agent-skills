"""Command-line interface. Keep it thin: parse arguments, then call `core`."""

from __future__ import annotations

import argparse
import logging
from collections.abc import Sequence

from my_project import __version__
from my_project.config import Settings
from my_project.core.greeting import make_greeting
from my_project.logging_setup import configure_logging

logger = logging.getLogger(__name__)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="my-project", description="my-project command line.")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("--log-level", help="Override the log level (for example DEBUG).")
    sub = parser.add_subparsers(dest="command", required=True)

    greet = sub.add_parser("greet", help="Print a greeting.")
    greet.add_argument("name", help="Name to greet.")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the CLI. Return the process exit code."""
    args = build_parser().parse_args(argv)
    settings = Settings.load()
    configure_logging(args.log_level or settings.log_level)

    if args.command == "greet":
        try:
            print(make_greeting(args.name, settings.greeting))
        except ValueError as exc:
            logger.error("%s", exc)
            return 2
        return 0

    raise AssertionError(f"unhandled command: {args.command}")  # pragma: no cover
