#!/usr/bin/env python3
"""
interactive_python_project_setup.py

Interactive helper for setting up a Python project with:

- a virtual environment
- either requirements.txt or pyproject.toml
- optional src/ package layout
- .gitignore protection for virtual environments and Python cache files
- robust timestamped logging

This script is intentionally educational. It pauses at important decision points
so the user understands what is about to happen.

Works on Windows, macOS, and Linux.

IMPORTANT:
Edit the CONFIG section below before running.
"""

from __future__ import annotations

import logging
import platform
import re
import subprocess
import sys
import textwrap
import venv
from datetime import datetime
from pathlib import Path


# =============================================================================
# CONFIG: EDIT THESE VALUES FIRST
# =============================================================================

# Choose the operating system you want the script to assume.
# Valid values:
#   "windows"
#   "macos_linux"
#
# This is intentionally explicit so beginners can see which activation command
# and executable paths are being used.
TARGET_OS = "windows"  # change to "macos_linux" on macOS/Linux

# Name of the virtual environment folder.
# Common convention is ".venv".
VENV_DIR_NAME = ".venv"

# Choose the dependency/project style.
# Valid values:
#   "requirements"  -> creates requirements.txt
#   "pyproject"     -> creates pyproject.toml
PROJECT_STYLE = "requirements"

# Used only when PROJECT_STYLE = "pyproject".
# Distribution/project name can contain hyphens.
PROJECT_NAME = "my-python-project"

# Used only when PROJECT_STYLE = "pyproject".
# Import package name should use underscores, not hyphens.
PACKAGE_IMPORT_NAME = "my_python_project"

# Used only when PROJECT_STYLE = "pyproject".
# If True, creates:
#   src/package_name/
# If False, creates:
#   package_name/
USE_SRC_LAYOUT = True

# Basic dependencies to install/write into requirements.txt or pyproject.toml.
# Use PyPI names here.
DEPENDENCIES = [
    "requests",
    "beautifulsoup4",
]

# Development tools. These are optional and only installed if the user confirms.
DEV_DEPENDENCIES = [
    "pytest",
    "ruff",
]

# Whether to ask before upgrading pip inside the venv.
ASK_TO_UPGRADE_PIP = True

# Whether to actually install dependencies immediately.
# If False, the script only writes files and tells the user what command to run.
INSTALL_DEPENDENCIES = True

# =============================================================================
# END CONFIG
# =============================================================================


SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR
VENV_DIR = PROJECT_ROOT / VENV_DIR_NAME
LOG_DIR = PROJECT_ROOT / "setup_logs"
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / f"python_project_setup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"


class SafeStreamHandler(logging.StreamHandler):
    """Logging handler that avoids crashing on console Unicode encoding issues."""

    def emit(self, record: logging.LogRecord) -> None:
        try:
            msg = self.format(record)
            self.stream.write(msg + self.terminator)
            self.flush()
        except UnicodeEncodeError:
            encoding = self.stream.encoding or "utf-8"
            msg = self.format(record).encode(encoding, errors="replace").decode(encoding)
            self.stream.write(msg + self.terminator)
            self.flush()


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, mode="w", encoding="utf-8"),
        SafeStreamHandler(sys.stdout),
    ],
)


def pause(message: str = "Press Enter to continue...") -> None:
    """Pause so the user can read and consciously continue."""
    input(f"\n{message}")


def ask_yes_no(prompt: str, default: bool = True) -> bool:
    """Ask a yes/no question."""
    default_text = "Y/n" if default else "y/N"

    while True:
        answer = input(f"{prompt} [{default_text}]: ").strip().lower()

        if not answer:
            return default

        if answer in {"y", "yes"}:
            return True

        if answer in {"n", "no"}:
            return False

        print("Please answer yes or no.")


def validate_config() -> None:
    """Validate user-edited config values."""
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


def print_intro() -> None:
    """Explain what the script is configured to do."""
    detected_os = platform.system()

    logging.info("Starting interactive Python project setup.")
    logging.info("Project root: %s", PROJECT_ROOT)
    logging.info("Detected system: %s", detected_os)
    logging.info("Configured TARGET_OS: %s", TARGET_OS)
    logging.info("Configured PROJECT_STYLE: %s", PROJECT_STYLE)
    logging.info("Configured venv folder: %s", VENV_DIR)

    print("\nThis script will help set up a Python project.")
    print("\nCurrent configuration:")
    print(f"  TARGET_OS:            {TARGET_OS}")
    print(f"  PROJECT_STYLE:        {PROJECT_STYLE}")
    print(f"  VENV_DIR_NAME:        {VENV_DIR_NAME}")
    print(f"  INSTALL_DEPENDENCIES: {INSTALL_DEPENDENCIES}")

    if PROJECT_STYLE == "pyproject":
        print(f"  PROJECT_NAME:         {PROJECT_NAME}")
        print(f"  PACKAGE_IMPORT_NAME:  {PACKAGE_IMPORT_NAME}")
        print(f"  USE_SRC_LAYOUT:       {USE_SRC_LAYOUT}")

    print(f"\nLog file will be written to:\n  {LOG_FILE}")

    pause(
        "Review the configuration above. "
        "If it is wrong, press Ctrl+C, edit the CONFIG section, and rerun. "
        "Otherwise press Enter to continue..."
    )


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


def run_command(command: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    """Run a command and log stdout/stderr."""
    logging.info("Running command: %s", " ".join(command))

    result = subprocess.run(
        command,
        cwd=str(cwd or PROJECT_ROOT),
        capture_output=True,
        text=True,
    )

    if result.stdout.strip():
        logging.info("stdout:\n%s", result.stdout.strip())

    if result.stderr.strip():
        if result.returncode == 0:
            logging.info("stderr:\n%s", result.stderr.strip())
        else:
            logging.error("stderr:\n%s", result.stderr.strip())

    return result


def create_virtual_environment() -> None:
    """Create the virtual environment if it does not already exist."""
    if VENV_DIR.exists():
        logging.info("Virtual environment already exists: %s", VENV_DIR)
        print(f"\nVirtual environment already exists at: {VENV_DIR}")
        return

    print("\nAbout to create a virtual environment.")
    print("A virtual environment is a private Python environment for this project.")
    print("It keeps this project's packages separate from your system Python.")
    pause()

    logging.info("Creating virtual environment at %s", VENV_DIR)
    venv.create(VENV_DIR, with_pip=True)
    logging.info("Virtual environment created.")


def ensure_gitignore() -> None:
    """Create or update .gitignore with Python/venv ignore rules."""
    gitignore = PROJECT_ROOT / ".gitignore"

    rules = [
        "# Python virtual environments",
        f"{VENV_DIR_NAME}/",
        "venv/",
        "env/",
        "ENV/",
        "",
        "# Python cache/build artifacts",
        "__pycache__/",
        "*.py[cod]",
        "*.egg-info/",
        "build/",
        "dist/",
        "",
        "# Test/type/lint caches",
        ".pytest_cache/",
        ".mypy_cache/",
        ".ruff_cache/",
        "",
        "# Setup logs generated by this helper",
        "setup_logs/",
        "",
    ]

    existing = gitignore.read_text(encoding="utf-8") if gitignore.exists() else ""

    print("\nChecking .gitignore.")
    if gitignore.exists():
        print(".gitignore already exists. Missing Python/venv ignore rules will be appended.")
    else:
        print(".gitignore does not exist. It will be created.")

    pause()

    lines_to_add = []
    existing_lines = set(existing.splitlines())

    for rule in rules:
        if rule == "" or rule.startswith("#"):
            lines_to_add.append(rule)
        elif rule not in existing_lines:
            lines_to_add.append(rule)

    if lines_to_add:
        with gitignore.open("a", encoding="utf-8") as f:
            if existing and not existing.endswith("\n"):
                f.write("\n")
            f.write("\n# Added by interactive_python_project_setup.py\n")
            f.write("\n".join(lines_to_add))
            f.write("\n")

        logging.info(".gitignore updated: %s", gitignore)
    else:
        logging.info(".gitignore already had required ignore rules.")


def create_requirements_txt(include_dev: bool) -> None:
    """Create requirements.txt and optional requirements-dev.txt."""
    requirements = PROJECT_ROOT / "requirements.txt"

    if requirements.exists():
        print("\nrequirements.txt already exists.")
        should_overwrite = ask_yes_no("Overwrite it?", default=False)
        if not should_overwrite:
            logging.info("Keeping existing requirements.txt.")
            return

    requirements.write_text("\n".join(DEPENDENCIES) + "\n", encoding="utf-8")
    logging.info("Wrote requirements.txt.")

    if include_dev:
        dev_file = PROJECT_ROOT / "requirements-dev.txt"
        dev_content = ["-r requirements.txt", "", *DEV_DEPENDENCIES]
        dev_file.write_text("\n".join(dev_content) + "\n", encoding="utf-8")
        logging.info("Wrote requirements-dev.txt.")


def create_pyproject_toml(include_dev: bool) -> None:
    """Create a minimal pyproject.toml and package structure."""
    pyproject = PROJECT_ROOT / "pyproject.toml"

    if pyproject.exists():
        print("\npyproject.toml already exists.")
        should_overwrite = ask_yes_no("Overwrite it?", default=False)
        if not should_overwrite:
            logging.info("Keeping existing pyproject.toml.")
            return

    package_root = PROJECT_ROOT / "src" / PACKAGE_IMPORT_NAME if USE_SRC_LAYOUT else PROJECT_ROOT / PACKAGE_IMPORT_NAME
    package_root.mkdir(parents=True, exist_ok=True)

    init_file = package_root / "__init__.py"
    cli_file = package_root / "cli.py"

    init_file.write_text('"""Project package."""\n\n__version__ = "0.1.0"\n', encoding="utf-8")

    cli_file.write_text(
        textwrap.dedent(
            f"""\
            \"""Command-line interface for {PROJECT_NAME}.\"""

            import argparse


            def main() -> None:
                \"""Run the command-line program.\"""
                parser = argparse.ArgumentParser(
                    description="Example command generated by the setup helper."
                )
                parser.add_argument(
                    "name",
                    nargs="?",
                    default="World",
                    help="Name to greet."
                )

                args = parser.parse_args()
                print(f"Hello {{args.name}}!")


            if __name__ == "__main__":
                main()
            """
        ),
        encoding="utf-8",
    )

    dependency_lines = ",\n".join(f'    "{dep}"' for dep in DEPENDENCIES)

    optional_dev_block = ""
    if include_dev:
        dev_lines = ",\n".join(f'    "{dep}"' for dep in DEV_DEPENDENCIES)
        optional_dev_block = f"""

[project.optional-dependencies]
dev = [
{dev_lines}
]
"""

    setuptools_block = ""
    if USE_SRC_LAYOUT:
        setuptools_block = """
[tool.setuptools.packages.find]
where = ["src"]
"""

    pyproject.write_text(
        textwrap.dedent(
            f"""\
            [build-system]
            requires = ["setuptools>=68"]
            build-backend = "setuptools.build_meta"

            [project]
            name = "{PROJECT_NAME}"
            version = "0.1.0"
            description = "Example Python project configured by interactive setup script."
            requires-python = ">=3.10"
            dependencies = [
            {dependency_lines}
            ]

            [project.scripts]
            {PROJECT_NAME} = "{PACKAGE_IMPORT_NAME}.cli:main"
            """
        )
        + optional_dev_block
        + setuptools_block,
        encoding="utf-8",
    )

    logging.info("Wrote pyproject.toml.")
    logging.info("Created package folder: %s", package_root)


def install_dependencies(include_dev: bool) -> None:
    """Install dependencies into the venv."""
    if not INSTALL_DEPENDENCIES:
        logging.info("INSTALL_DEPENDENCIES is False; skipping install.")
        return

    venv_python = get_venv_python_path()

    if not venv_python.exists():
        raise FileNotFoundError(f"Could not find venv Python at {venv_python}")

    print("\nAbout to install dependencies into the virtual environment.")
    print("This does NOT install packages globally if the venv Python path is correct.")
    print(f"Using Python executable:\n  {venv_python}")
    pause()

    if ASK_TO_UPGRADE_PIP and ask_yes_no("Upgrade pip inside the virtual environment first?", default=True):
        result = run_command([str(venv_python), "-m", "pip", "install", "--upgrade", "pip"])
        if result.returncode != 0:
            raise RuntimeError("Failed to upgrade pip. See log file for details.")

    if PROJECT_STYLE == "requirements":
        req = PROJECT_ROOT / ("requirements-dev.txt" if include_dev else "requirements.txt")
        result = run_command([str(venv_python), "-m", "pip", "install", "-r", str(req)])
    else:
        target = ".[dev]" if include_dev else "."
        result = run_command([str(venv_python), "-m", "pip", "install", "-e", target])

    if result.returncode != 0:
        raise RuntimeError("Dependency installation failed. See log file for details.")

    logging.info("Dependency installation complete.")


def write_local_notes() -> None:
    """Write a small local note file summarizing commands."""
    notes = PROJECT_ROOT / "SETUP_NOTES.md"

    notes.write_text(
        textwrap.dedent(
            f"""\
            # Local Setup Notes

            Generated by `interactive_python_project_setup.py`.

            ## Activate the virtual environment

            ```bash
            {get_activation_command()}
            ```

            ## Project style

            Selected style:

            ```text
            {PROJECT_STYLE}
            ```
            """
        ),
        encoding="utf-8",
    )

    logging.info("Wrote SETUP_NOTES.md.")


def main() -> None:
    """Main interactive setup flow."""
    try:
        validate_config()
        print_intro()

        include_dev = ask_yes_no(
            "\nDo you want to include development tools "
            f"({', '.join(DEV_DEPENDENCIES)})?",
            default=True,
        )

        create_virtual_environment()
        ensure_gitignore()

        if PROJECT_STYLE == "requirements":
            print("\nYou selected requirements.txt mode.")
            print("This is best for simple scripts and small projects.")
            pause()
            create_requirements_txt(include_dev)
        else:
            print("\nYou selected pyproject.toml mode.")
            print("This is best for installable packages, reusable tools, or CLI commands.")
            pause()
            create_pyproject_toml(include_dev)

        install_dependencies(include_dev)
        write_local_notes()

        print("\nSetup complete.")
        print(f"Log file:\n  {LOG_FILE}")
        print("\nTo activate your environment, run:")
        print(f"  {get_activation_command()}")

        if PROJECT_STYLE == "pyproject":
            print("\nTry the generated command after activation:")
            print(f"  {PROJECT_NAME} Demetrius")
            print("\nOr run the module directly:")
            print(f"  python -m {PACKAGE_IMPORT_NAME}.cli Demetrius")

    except KeyboardInterrupt:
        logging.warning("Setup cancelled by user.")
        print("\nSetup cancelled.")
        sys.exit(130)
    except Exception as exc:
        logging.exception("Setup failed.")
        print(f"\nSetup failed: {exc}")
        print(f"See log file:\n  {LOG_FILE}")
        sys.exit(1)


if __name__ == "__main__":
    main()
