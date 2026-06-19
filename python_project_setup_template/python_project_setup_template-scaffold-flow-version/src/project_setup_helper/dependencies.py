"""Dependency installation helpers."""

from __future__ import annotations

import logging

from project_setup_helper.commands import run_command
from project_setup_helper.config import ASK_TO_UPGRADE_PIP, INSTALL_DEPENDENCIES, ProjectConfig
from project_setup_helper.prompts import ask_yes_no
from project_setup_helper.venv_tools import get_venv_python_path


def install_dependencies(config: ProjectConfig) -> None:
    """Install dependencies into the generated project's venv."""
    if not INSTALL_DEPENDENCIES or not config.install_dependencies:
        logging.info("Dependency installation disabled; skipping install.")
        print("\nSkipping dependency installation.")
        return

    venv_python = get_venv_python_path(config)
    if not venv_python.exists():
        raise FileNotFoundError(f"Could not find venv Python at {venv_python}")

    print("\nAbout to install dependencies into the virtual environment.")
    print("This does NOT install packages globally if the venv Python path is correct.")
    print(f"Using Python executable:\n  {venv_python}")

    if not ask_yes_no("Install dependencies now?", default=True):
        print("\nSkipping dependency installation.")
        return

    if ASK_TO_UPGRADE_PIP and ask_yes_no("Upgrade pip inside the virtual environment first?", default=True):
        result = run_command([str(venv_python), "-m", "pip", "install", "--upgrade", "pip"], cwd=config.project_root)
        if result.returncode != 0:
            raise RuntimeError("Failed to upgrade pip. See log file for details.")

    if config.uses_requirements:
        req = config.project_root / ("requirements-dev.txt" if config.include_dev_tools else "requirements.txt")
        if not req.exists():
            print(f"\nDependency file does not exist, skipping install:\n  {req}")
            return
        result = run_command([str(venv_python), "-m", "pip", "install", "-r", str(req)], cwd=config.project_root)
    else:
        target = ".[dev]" if config.include_dev_tools else "."
        result = run_command([str(venv_python), "-m", "pip", "install", "-e", target], cwd=config.project_root)

    if result.returncode != 0:
        raise RuntimeError("Dependency installation failed. See log file for details.")

    logging.info("Dependency installation complete.")
    print("\nDependency installation complete.")
