"""Shared filesystem paths used by the setup helper."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from project_setup_helper.config import VENV_DIR_NAME

# When installed as a package, the current working directory is the project the
# user wants to set up. This is more useful than locating the package source.
PROJECT_ROOT = Path.cwd().resolve()
VENV_DIR = PROJECT_ROOT / VENV_DIR_NAME
LOG_DIR = PROJECT_ROOT / "setup_logs"
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / f"python_project_setup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
