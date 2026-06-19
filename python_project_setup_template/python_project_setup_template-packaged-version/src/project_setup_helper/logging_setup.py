"""Logging setup for the educational project setup helper."""

from __future__ import annotations

import logging
import sys

from project_setup_helper.paths import LOG_FILE


class SafeStreamHandler(logging.StreamHandler):
    """Logging handler that avoids crashing on console Unicode encoding issues."""

    def emit(self, record: logging.LogRecord) -> None:
        try:
            msg = self.format(record)
            self.stream.write(msg + self.terminator)
            self.flush()
        except UnicodeEncodeError:
            encoding = self.stream.encoding or "utf-8"
            msg = self.format(record).encode(encoding, errors="replace").decode(encoding)
            self.stream.write(msg + self.terminator)
            self.flush()


def configure_logging() -> None:
    """Configure timestamped file logging and console logging."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(LOG_FILE, mode="w", encoding="utf-8"),
            SafeStreamHandler(sys.stdout),
        ],
        force=True,
    )
