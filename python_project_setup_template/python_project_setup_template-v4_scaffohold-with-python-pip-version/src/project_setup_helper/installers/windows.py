"""Windows-specific setup placeholder.

The current helper uses sys.executable on Windows and the Scripts/ folder inside
.venv. This module is intentionally small for now, but gives the repo a clear
place to teach Windows-specific setup later.
"""

from __future__ import annotations


def run_windows_check() -> None:
    """Currently no-op for Windows-specific preflight checks."""
    return
