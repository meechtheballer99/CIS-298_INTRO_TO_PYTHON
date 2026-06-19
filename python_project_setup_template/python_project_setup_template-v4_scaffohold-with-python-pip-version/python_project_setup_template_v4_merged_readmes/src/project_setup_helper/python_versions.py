"""Python and pip version selection helpers."""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

from project_setup_helper.commands import run_command
from project_setup_helper.prompts import ask_choice, ask_text, ask_yes_no


def choose_minimum_python_version(supported_versions: list[str], default: str) -> str:
    """Ask which minimum Python version the generated project should declare."""
    choices = {str(index): version for index, version in enumerate(supported_versions, start=1)}
    default_key = next((key for key, value in choices.items() if value == default), "1")

    selected_key = ask_choice(
        "Minimum Python version for this project",
        choices=choices,
        default=default_key,
    )
    return choices[selected_key]


def ask_pip_version(default: str = "") -> str:
    """Optionally ask for a pip version to install inside the virtual environment."""
    should_pin = ask_yes_no(
        "\nPin a specific pip version inside the virtual environment?",
        default=False,
    )
    if not should_pin:
        return default

    return ask_text(
        "Enter pip version, for example 24.3.1, or press Enter for latest",
        default=default or "latest",
    ).strip().lower().removeprefix("pip==").replace("latest", "")


def choose_python_interpreter() -> Path:
    """Ask which Python executable should be used to create the virtual environment."""
    choice = ask_choice(
        "Python interpreter for creating the virtual environment",
        choices={
            "1": "Use the current Python interpreter",
            "2": "Use python3 from PATH",
            "3": "Enter a specific Python executable path",
            "4": "Use Homebrew python@3.x path on Apple Silicon macOS",
        },
        default="1",
    )

    if choice == "1":
        return Path(sys.executable)

    if choice == "2":
        python3 = shutil.which("python3")
        if not python3:
            raise FileNotFoundError("Could not find python3 on PATH.")
        return Path(python3)

    if choice == "3":
        raw_path = ask_text("Enter full Python executable path")
        path = Path(raw_path).expanduser()
        if not path.exists():
            raise FileNotFoundError(f"Python executable not found: {path}")
        return path

    version = ask_text("Enter Homebrew Python version, for example 3.12", default="3.12")
    path = Path(f"/opt/homebrew/bin/python{version}")

    if path.exists():
        return path

    print(f"\nHomebrew Python was not found at:\n  {path}")
    print("\nYou may need to run:")
    print(f"  brew install python@{version}")

    if ask_yes_no("Continue anyway with this path?", default=False):
        return path

    raise FileNotFoundError(f"Homebrew Python not found: {path}")


def print_python_version(interpreter: Path) -> None:
    """Print the version reported by the selected interpreter."""
    result = run_command([str(interpreter), "--version"])
    version = result.stdout.strip() or result.stderr.strip() or "unknown"
    print("\nSelected Python interpreter:")
    print(f"  {interpreter}")
    print(f"Version:\n  {version}")
