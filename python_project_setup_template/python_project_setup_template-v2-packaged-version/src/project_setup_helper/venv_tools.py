"""Virtual environment helpers."""

from __future__ import annotations

import logging
import shutil
import sys
from pathlib import Path

from project_setup_helper.commands import run_command
from project_setup_helper.config import TARGET_OS, VENV_DIR_NAME
from project_setup_helper.paths import VENV_DIR
from project_setup_helper.prompts import ask_yes_no, exit_script


def get_base_python_path() -> Path:
    """Return the Python executable to use for creating the venv."""
    if TARGET_OS == "windows":
        return Path(sys.executable)

    python3 = shutil.which("python3")
    if not python3:
        raise FileNotFoundError("Could not find python3 on PATH.")
    return Path(python3)


def get_venv_python_path() -> Path:
    """Return path to the Python executable inside the venv."""
    if TARGET_OS == "windows":
        return VENV_DIR / "Scripts" / "python.exe"
    return VENV_DIR / "bin" / "python"


def get_activation_command() -> str:
    """Return the activation command for the configured OS."""
    if TARGET_OS == "windows":
        return rf"{VENV_DIR_NAME}\Scripts\activate"
    return f"source {VENV_DIR_NAME}/bin/activate"


def create_virtual_environment() -> None:
    """Create the virtual environment if it does not already exist."""
    if VENV_DIR.exists():
        logging.info("Virtual environment already exists: %s", VENV_DIR)
        print(f"\nVirtual environment already exists at: {VENV_DIR}")
        return

    base_python = get_base_python_path()

    print("\nAbout to create a virtual environment.")
    print("A virtual environment is a private Python environment for this project.")
    print("It keeps this project's packages separate from your system Python.")
    print("\nThis venv will be created using:")
    print(f"  {base_python}")

    version_result = run_command([str(base_python), "--version"])
    version_text = version_result.stdout.strip() or version_result.stderr.strip()
    if version_text:
        print(f"  {version_text}")

    print("\nThe command will be:")
    print(f"  {base_python} -m venv {VENV_DIR}")

    if not ask_yes_no("\nCreate the virtual environment now?", default=True):
        exit_script("Setup stopped before creating the virtual environment.")

    logging.info("Creating virtual environment at %s", VENV_DIR)
    result = run_command([str(base_python), "-m", "venv", str(VENV_DIR)])
    if result.returncode != 0:
        raise RuntimeError("Failed to create virtual environment. See log file for details.")

    logging.info("Virtual environment created.")
    print(f"\nVirtual environment created at:\n  {VENV_DIR}")
