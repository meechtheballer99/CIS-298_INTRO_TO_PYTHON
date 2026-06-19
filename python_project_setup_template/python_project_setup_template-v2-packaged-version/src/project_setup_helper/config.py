"""Editable configuration for the educational project setup helper.

This module intentionally keeps beginner-facing settings in one place.
Edit these values before running the helper, or later replace this module with
argument parsing / config-file loading as a teaching extension.
"""

from __future__ import annotations

import re

# Choose the operating system behavior the helper should use.
# Valid values: "windows", "macos_linux"
TARGET_OS = "macos_linux"

# Name of the virtual environment folder. Common convention is ".venv".
VENV_DIR_NAME = ".venv"

# Dependency/project style. Valid values: "requirements", "pyproject".
PROJECT_STYLE = "requirements"

# Used only when PROJECT_STYLE = "pyproject".
PROJECT_NAME = "my-python-project"
PACKAGE_IMPORT_NAME = "my_python_project"
USE_SRC_LAYOUT = True

# Basic dependencies to install/write into requirements.txt or pyproject.toml.
DEPENDENCIES = [
    "requests",
    "beautifulsoup4",
]

# Optional development tools.
DEV_DEPENDENCIES = [
    "pytest",
    "ruff",
]

ASK_TO_UPGRADE_PIP = True
INSTALL_DEPENDENCIES = True
ENABLE_MACOS_HOMEBREW_PYTHON_HELPER = True

# User can type any of these at prompts to exit safely.
EXIT_WORDS = {"q", "quit", "exit", "cancel"}


def validate_config() -> None:
    """Validate user-editable config values."""
    if TARGET_OS not in {"windows", "macos_linux"}:
        raise ValueError('TARGET_OS must be "windows" or "macos_linux".')

    if PROJECT_STYLE not in {"requirements", "pyproject"}:
        raise ValueError('PROJECT_STYLE must be "requirements" or "pyproject".')

    if not VENV_DIR_NAME:
        raise ValueError("VENV_DIR_NAME cannot be empty.")

    if PROJECT_STYLE == "pyproject":
        if not PROJECT_NAME:
            raise ValueError("PROJECT_NAME cannot be empty.")

        if not re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", PACKAGE_IMPORT_NAME):
            raise ValueError(
                "PACKAGE_IMPORT_NAME must be a valid Python package name, "
                "for example: my_python_project"
            )
