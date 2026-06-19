"""Dependency installation helpers."""

from __future__ import annotations

import logging

from project_setup_helper.commands import run_command
from project_setup_helper.config import ASK_TO_UPGRADE_PIP, INSTALL_DEPENDENCIES, PROJECT_STYLE
from project_setup_helper.paths import PROJECT_ROOT
from project_setup_helper.prompts import ask_yes_no
from project_setup_helper.venv_tools import get_venv_python_path


def install_dependencies(include_dev: bool) -> None:
    """Install dependencies into the venv."""
    if not INSTALL_DEPENDENCIES:
        logging.info("INSTALL_DEPENDENCIES is False; skipping install.")
        print("\nINSTALL_DEPENDENCIES is False; skipping dependency installation.")
        return

    venv_python = get_venv_python_path()
    if not venv_python.exists():
        raise FileNotFoundError(f"Could not find venv Python at {venv_python}")

    print("\nAbout to install dependencies into the virtual environment.")
    print("This does NOT install packages globally if the venv Python path is correct.")
    print(f"Using Python executable:\n  {venv_python}")

    if not ask_yes_no("Install dependencies now?", default=True):
        print("\nSkipping dependency installation.")
        return

    if ASK_TO_UPGRADE_PIP and ask_yes_no("Upgrade pip inside the virtual environment first?", default=True):
        result = run_command([str(venv_python), "-m", "pip", "install", "--upgrade", "pip"])
        if result.returncode != 0:
            raise RuntimeError("Failed to upgrade pip. See log file for details.")

    if PROJECT_STYLE == "requirements":
        req = PROJECT_ROOT / ("requirements-dev.txt" if include_dev else "requirements.txt")
        if not req.exists():
            print(f"\nDependency file does not exist, skipping install:\n  {req}")
            return
        result = run_command([str(venv_python), "-m", "pip", "install", "-r", str(req)])
    else:
        target = ".[dev]" if include_dev else "."
        result = run_command([str(venv_python), "-m", "pip", "install", "-e", target])

    if result.returncode != 0:
        raise RuntimeError("Dependency installation failed. See log file for details.")

    logging.info("Dependency installation complete.")
    print("\nDependency installation complete.")
