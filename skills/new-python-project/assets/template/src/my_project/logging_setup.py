"""Logging configuration.

Library modules only call `logging.getLogger(__name__)`. Only the entry point (`cli.main`)
calls `configure_logging`, one time.
"""

from __future__ import annotations

import logging

LOG_FORMAT = "%(asctime)s %(levelname)-8s %(name)s: %(message)s"


def configure_logging(level: str = "INFO") -> None:
    """Configure the root logger. A second call replaces the first configuration."""
    logging.basicConfig(level=level.upper(), format=LOG_FORMAT, force=True)
