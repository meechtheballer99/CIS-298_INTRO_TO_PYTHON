"""Python and pip version selection helpers."""

from __future__ import annotations

import os
import re
import shutil
import sys
from pathlib import Path

from project_setup_helper.commands import run_command
from project_setup_helper.prompts import ask_choice, ask_text, ask_yes_no


def choose_minimum_python_version(supported_versions: list[str], default: str) -> str:
    """Ask which minimum Python version the generated project should declare."""
    choices = {
        str(index): version
        for index, version in enumerate(supported_versions, start=1)
    }
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

    answer = ask_text(
        "Enter pip version, for example 24.3.1, or press Enter for latest",
        default=default or "latest",
    )

    normalized = answer.strip().lower()
    normalized = normalized.removeprefix("pip==")

    if normalized == "latest":
        return ""

    return normalized


def choose_python_interpreter() -> Path:
    """Ask which Python executable should be used to create the virtual environment."""
    choice = ask_choice(
        "Python interpreter for creating the virtual environment",
        choices={
            "1": "Use the current Python interpreter",
            "2": "Use python3 from PATH",
            "3": "Enter a specific Python executable path",
            "4": "Use Homebrew python@3.x path on Apple Silicon macOS",
            "5": "Use pyenv-managed Python",
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
        return ask_for_specific_interpreter_path()

    if choice == "4":
        return ask_for_homebrew_interpreter()

    return choose_pyenv_interpreter()


def ask_for_specific_interpreter_path() -> Path:
    """Ask the user for a full Python executable path."""
    raw_path = ask_text("Enter full Python executable path")
    path = Path(raw_path).expanduser()

    if not path.exists():
        raise FileNotFoundError(f"Python executable not found: {path}")

    return path


def ask_for_homebrew_interpreter() -> Path:
    """Ask for a Homebrew Python version and return its expected executable path."""
    version = ask_text(
        "Enter Homebrew Python version, for example 3.12",
        default="3.12",
    ).strip()

    path = Path(f"/opt/homebrew/bin/python{version}")

    if path.exists():
        return path

    print(f"\nHomebrew Python was not found at:\n  {path}")
    print("\nYou may need to run:")
    print(f"  brew install python@{version}")

    if ask_yes_no("Continue anyway with this path?", default=False):
        return path

    raise FileNotFoundError(f"Homebrew Python not found: {path}")


def get_pyenv_root() -> Path:
    """Return the likely pyenv root directory."""
    env_root = os.environ.get("PYENV_ROOT")

    if env_root:
        return Path(env_root).expanduser()

    return Path.home() / ".pyenv"


def find_pyenv_interpreters() -> list[Path]:
    """
    Find Python interpreters installed by pyenv.

    Common layout:
      ~/.pyenv/versions/3.8.13/bin/python
      ~/.pyenv/versions/3.12.11/bin/python
    """
    versions_dir = get_pyenv_root() / "versions"

    if not versions_dir.exists():
        return []

    interpreters: list[Path] = []

    for version_dir in sorted(versions_dir.iterdir()):
        python_path = version_dir / "bin" / "python"

        if python_path.exists():
            interpreters.append(python_path)

    return interpreters


def choose_pyenv_interpreter() -> Path:
    """Let the user choose from pyenv-managed Python interpreters."""
    interpreters = find_pyenv_interpreters()

    if not interpreters:
        print("\nNo pyenv-managed Python versions were found.")
        print("\nExpected location:")
        print(f"  {get_pyenv_root() / 'versions'}")
        print("\nYou may need to install one first:")
        print("  brew install pyenv")
        print("  pyenv install 3.12.11")

        if ask_yes_no(
            "\nDo you want to enter a specific Python executable path instead?",
            default=True,
        ):
            return ask_for_specific_interpreter_path()

        raise FileNotFoundError("No pyenv-managed Python interpreters found.")

    choices: dict[str, str] = {}

    for index, interpreter in enumerate(interpreters, start=1):
        version_name = interpreter.parent.parent.name
        choices[str(index)] = f"{version_name}  ({interpreter})"

    selected_key = ask_choice(
        "Choose pyenv Python interpreter",
        choices=choices,
        default="1",
    )

    return interpreters[int(selected_key) - 1]


def parse_major_minor(version_text: str) -> tuple[int, int] | None:
    """
    Extract major/minor version from text like:
      Python 3.12.4
      3.12.4
    """
    match = re.search(r"(\d+)\.(\d+)", version_text)

    if not match:
        return None

    return int(match.group(1)), int(match.group(2))


def get_interpreter_version(interpreter: Path) -> tuple[int, int] | None:
    """Return the selected interpreter's major/minor Python version."""
    result = run_command([str(interpreter), "--version"])
    version_text = result.stdout.strip() or result.stderr.strip()
    return parse_major_minor(version_text)


def print_python_version(interpreter: Path) -> None:
    """Print the version reported by the selected interpreter."""
    result = run_command([str(interpreter), "--version"])
    version = result.stdout.strip() or result.stderr.strip() or "unknown"

    print("\nSelected Python interpreter:")
    print(f"  {interpreter}")
    print(f"Version:\n  {version}")


def warn_if_interpreter_too_old(
    minimum_python_version: str,
    interpreter: Path,
) -> None:
    """Warn if selected interpreter is lower than the project requirement."""
    required = parse_major_minor(minimum_python_version)
    actual = get_interpreter_version(interpreter)

    if required is None or actual is None:
        return

    if actual >= required:
        return

    print("\nWARNING:")
    print("The selected interpreter does not satisfy the project requirement.")
    print("\nProject requires:")
    print(f"  Python >= {minimum_python_version}")
    print("\nSelected interpreter:")
    print(f"  Python {actual[0]}.{actual[1]}")
    print(f"  {interpreter}")
    print("\nThe virtual environment could still be created,")
    print("but package installation may fail because of requires-python.")

    should_continue = ask_yes_no(
        "\nContinue anyway?",
        default=False,
    )

    if not should_continue:
        raise SystemExit("Setup stopped because Python version requirement was not met.")