"""Command-running helpers."""

from __future__ import annotations

import logging
import subprocess
from pathlib import Path

from project_setup_helper.paths import PROJECT_ROOT


def run_command(command: list[str], cwd: Path | None = None, check: bool = False) -> subprocess.CompletedProcess[str]:
    """Run a command and log stdout/stderr."""
    logging.info("Running command: %s", " ".join(command))

    result = subprocess.run(command, cwd=str(cwd or PROJECT_ROOT), capture_output=True, text=True)

    if result.stdout.strip():
        logging.info("stdout:\n%s", result.stdout.strip())
    if result.stderr.strip():
        if result.returncode == 0:
            logging.info("stderr:\n%s", result.stderr.strip())
        else:
            logging.error("stderr:\n%s", result.stderr.strip())

    if check and result.returncode != 0:
        raise RuntimeError(f"Command failed with exit code {result.returncode}: {' '.join(command)}")
    return result


def run_interactive_command(command: list[str], cwd: Path | None = None) -> int:
    """Run a command interactively so the user can see prompts/output."""
    logging.info("Running interactive command: %s", " ".join(command))
    result = subprocess.run(command, cwd=str(cwd or PROJECT_ROOT))
    logging.info("Interactive command exited with code: %s", result.returncode)
    return result.returncode
