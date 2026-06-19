"""Default settings and runtime project configuration.

Teaching note:
The helper used to require beginners to edit global CONFIG variables. In this
version, most values come from interactive prompts. The small constants below
are defaults the helper uses when generating projects.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

VENV_DIR_NAME = ".venv"

DEPENDENCIES = [
    "requests",
    "beautifulsoup4",
]

DEV_DEPENDENCIES = [
    "pytest",
    "ruff",
]

SUPPORTED_PYTHON_VERSIONS = ["3.10", "3.11", "3.12", "3.13"]
DEFAULT_MINIMUM_PYTHON_VERSION = "3.11"
DEFAULT_PIP_VERSION = ""

ASK_TO_UPGRADE_PIP = True
INSTALL_DEPENDENCIES = True
ENABLE_MACOS_HOMEBREW_PYTHON_HELPER = True
EXIT_WORDS = {"q", "quit", "exit", "cancel"}


@dataclass(frozen=True)
class ProjectConfig:
    """Runtime choices for one generated project."""

    project_type: str
    project_name: str
    package_name: str
    project_root: Path
    include_dev_tools: bool
    minimum_python_version: str
    python_interpreter: Path
    pip_version: str = ""
    create_venv: bool = True
    install_dependencies: bool = True

    @property
    def uses_pyproject(self) -> bool:
        return self.project_type == "pyproject"

    @property
    def uses_requirements(self) -> bool:
        return self.project_type == "requirements"


def normalize_project_name(name: str) -> str:
    """Convert free text into a simple distribution/folder name."""
    cleaned = name.strip().lower().replace("_", "-")
    cleaned = re.sub(r"[^a-z0-9-]+", "-", cleaned)
    cleaned = re.sub(r"-+", "-", cleaned).strip("-")
    if not cleaned:
        raise ValueError("Project name cannot be empty.")
    return cleaned


def package_name_from_project_name(project_name: str) -> str:
    """Convert a distribution name like weather-cli to an import name."""
    package_name = project_name.replace("-", "_")
    if not re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", package_name):
        package_name = f"project_{package_name}"
    return package_name
