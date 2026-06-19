"""Virtual environment helpers."""

from __future__ import annotations

import logging
import platform
import shutil
import sys
from pathlib import Path

from project_setup_helper.commands import run_command
from project_setup_helper.config import ProjectConfig, VENV_DIR_NAME
from project_setup_helper.prompts import ask_yes_no, exit_script


def get_target_os() -> str:
    """Return the OS style used for venv paths."""
    return "windows" if platform.system() == "Windows" else "macos_linux"


def get_base_python_path() -> Path:
    """Return the Python executable to use for creating the venv."""
    if get_target_os() == "windows":
        return Path(sys.executable)
    python3 = shutil.which("python3")
    if not python3:
        raise FileNotFoundError("Could not find python3 on PATH.")
    return Path(python3)


def get_venv_dir(config: ProjectConfig) -> Path:
    return config.project_root / VENV_DIR_NAME


def get_venv_python_path(config: ProjectConfig) -> Path:
    """Return path to the Python executable inside the venv."""
    if get_target_os() == "windows":
        return get_venv_dir(config) / "Scripts" / "python.exe"
    return get_venv_dir(config) / "bin" / "python"


def get_activation_command(config: ProjectConfig) -> str:
    """Return the activation command for the current OS."""
    if get_target_os() == "windows":
        return rf"{VENV_DIR_NAME}\Scripts\activate"
    return f"source {VENV_DIR_NAME}/bin/activate"


def create_virtual_environment(config: ProjectConfig) -> None:
    """Create the virtual environment if requested and missing."""
    if not config.create_venv:
        print("\nSkipping virtual environment creation.")
        return

    venv_dir = get_venv_dir(config)
    if venv_dir.exists():
        logging.info("Virtual environment already exists: %s", venv_dir)
        print(f"\nVirtual environment already exists at: {venv_dir}")
        return

    base_python = get_base_python_path()

    print("\nAbout to create a virtual environment.")
    print("A virtual environment is a private Python environment for this project.")
    print("It keeps this project's packages separate from your system Python.")
    print("\nThis venv will be created using:")
    print(f"  {base_python}")

    version_result = run_command([str(base_python), "--version"], cwd=config.project_root)
    version_text = version_result.stdout.strip() or version_result.stderr.strip()
    if version_text:
        print(f"  {version_text}")

    print("\nThe command will be:")
    print(f"  {base_python} -m venv {venv_dir}")

    if not ask_yes_no("\nCreate the virtual environment now?", default=True):
        exit_script("Setup stopped before creating the virtual environment.")

    result = run_command([str(base_python), "-m", "venv", str(venv_dir)], cwd=config.project_root)
    if result.returncode != 0:
        raise RuntimeError("Failed to create virtual environment. See log file for details.")

    logging.info("Virtual environment created at %s", venv_dir)
    print(f"\nVirtual environment created at:\n  {venv_dir}")
