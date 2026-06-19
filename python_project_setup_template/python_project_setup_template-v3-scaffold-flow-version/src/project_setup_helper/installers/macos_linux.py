"""Shared macOS/Linux installer placeholder.

Most macOS/Linux behavior is handled by venv_tools.py. Apple Silicon gets a
separate teaching module because Homebrew Python and PATH order are important.
"""

from __future__ import annotations


def run_macos_linux_check() -> None:
    """Currently no-op for non-Apple-Silicon macOS/Linux systems."""
    return
