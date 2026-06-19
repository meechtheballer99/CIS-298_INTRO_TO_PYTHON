"""Filesystem path helpers.

Teaching note:
A project generator should work with the project root selected by the user, not
only with the directory where the generator itself lives.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path


def timestamp() -> str:
    """Return a compact timestamp for log/note filenames."""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def setup_log_file(project_root: Path) -> Path:
    """Return the timestamped log file path for a generated project."""
    log_dir = project_root / "setup_logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    return log_dir / f"python_project_setup_{timestamp()}.log"
