#!/usr/bin/env python3
"""
interactive_python_project_setup.py

Interactive helper for setting up a Python project with:

- a virtual environment
- either requirements.txt or pyproject.toml
- optional src/ package layout
- .gitignore protection for virtual environments and Python cache files
- robust timestamped logging
- macOS Apple Silicon checks for Homebrew-managed Python

This script is intentionally educational. It pauses at important decision points
so the user understands what is about to happen.

Works on Windows, macOS, and Linux.

IMPORTANT:
Edit the CONFIG section below before running.
"""

from __future__ import annotations

import logging
import os
import platform
import re
import shutil
import subprocess
import sys
import textwrap
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
TARGET_OS = "macos_linux"  # change to "windows" on Windows

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

# On macOS Apple Silicon, whether to walk the user through checking Homebrew
# and Homebrew-managed Python before creating the virtual environment.
ENABLE_MACOS_HOMEBREW_PYTHON_HELPER = True

# =============================================================================
# END CONFIG
# =============================================================================


SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR
VENV_DIR = PROJECT_ROOT / VENV_DIR_NAME
LOG_DIR = PROJECT_ROOT / "setup_logs"
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / f"python_project_setup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

EXIT_WORDS = {"q", "quit", "exit", "cancel"}


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


def exit_script(message: str = "Exiting setup.") -> None:
    """Exit the script cleanly."""
    logging.info(message)
    print(f"\n{message}")
    print(f"Log file:\n  {LOG_FILE}")
    sys.exit(0)


def check_for_exit(answer: str) -> None:
    """Exit if the user typed an exit word."""
    if answer.strip().lower() in EXIT_WORDS:
        exit_script("Setup cancelled by user.")


def pause(message: str = "Press Enter to continue, or type 'exit' to quit...") -> None:
    """Pause so the user can read and consciously continue."""
    answer = input(f"\n{message} ").strip()
    check_for_exit(answer)


def ask_yes_no(prompt: str, default: bool = True) -> bool:
    """Ask a yes/no question. User can always type exit."""
    default_text = "Y/n" if default else "y/N"

    while True:
        answer = input(f"{prompt} [{default_text}, or exit]: ").strip().lower()
        check_for_exit(answer)

        if not answer:
            return default

        if answer in {"y", "yes"}:
            return True

        if answer in {"n", "no"}:
            return False

        print("Please answer yes or no, or type 'exit' to quit.")


def ask_choice(prompt: str, choices: dict[str, str], default: str | None = None) -> str:
    """
    Ask the user to choose from numbered options.

    choices example:
        {
            "1": "Continue",
            "2": "Skip",
        }
    """
    print(f"\n{prompt}")

    for key, description in choices.items():
        print(f"  {key}) {description}")

    if default is not None:
        print(f"Press Enter for default: {default}) {choices[default]}")

    while True:
        answer = input("Choose an option, or type 'exit' to quit: ").strip().lower()
        check_for_exit(answer)

        if not answer and default is not None:
            return default

        if answer in choices:
            return answer

        print("Invalid choice. Try again.")


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
    detected_machine = platform.machine()

    logging.info("Starting interactive Python project setup.")
    logging.info("Project root: %s", PROJECT_ROOT)
    logging.info("Detected system: %s", detected_os)
    logging.info("Detected machine: %s", detected_machine)
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

    print("\nDetected machine:")
    print(f"  OS:                   {detected_os}")
    print(f"  CPU/architecture:     {detected_machine}")

    print(f"\nLog file will be written to:\n  {LOG_FILE}")

    pause(
        "Review the configuration above. "
        "If it is wrong, type 'exit', edit the CONFIG section, and rerun. "
        "Otherwise press Enter to continue..."
    )


def run_command(
    command: list[str],
    cwd: Path | None = None,
    check: bool = False,
) -> subprocess.CompletedProcess[str]:
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

    if check and result.returncode != 0:
        raise RuntimeError(
            f"Command failed with exit code {result.returncode}: {' '.join(command)}"
        )

    return result


def run_interactive_command(command: list[str], cwd: Path | None = None) -> int:
    """
    Run a command interactively so the user can see prompts/output.

    This is used for commands like the Homebrew installer.
    """
    logging.info("Running interactive command: %s", " ".join(command))

    result = subprocess.run(
        command,
        cwd=str(cwd or PROJECT_ROOT),
    )

    logging.info("Interactive command exited with code: %s", result.returncode)
    return result.returncode


def is_macos() -> bool:
    """Return True if running on macOS."""
    return platform.system() == "Darwin"


def is_apple_silicon() -> bool:
    """Return True if running on Apple Silicon."""
    return platform.machine().lower() in {"arm64", "aarch64"}


def get_expected_homebrew_bin_dir() -> Path:
    """
    Return the conventional Homebrew bin directory for this machine.

    Apple Silicon:
        /opt/homebrew/bin

    Intel macOS:
        /usr/local/bin
    """
    if is_macos() and is_apple_silicon():
        return Path("/opt/homebrew/bin")

    return Path("/usr/local/bin")


def find_homebrew_command() -> Path | None:
    """Find Homebrew even if it is not currently on PATH."""
    brew_from_path = shutil.which("brew")
    if brew_from_path:
        return Path(brew_from_path)

    possible_paths = [
        Path("/opt/homebrew/bin/brew"),
        Path("/usr/local/bin/brew"),
    ]

    for path in possible_paths:
        if path.exists():
            return path

    return None


def get_path_entries() -> list[str]:
    """Return PATH as a list of directory strings."""
    return os.environ.get("PATH", "").split(os.pathsep)


def path_contains_before(first: Path, second: Path) -> bool:
    """
    Return True if first appears in PATH before second.

    If second is not in PATH, first only needs to exist in PATH.
    """
    entries = get_path_entries()

    first_text = str(first)
    second_text = str(second)

    if first_text not in entries:
        return False

    if second_text not in entries:
        return True

    return entries.index(first_text) < entries.index(second_text)


def prepend_to_current_process_path(directory: Path) -> None:
    """
    Prepend a directory to PATH for the current script process.

    This does not permanently update the user's shell config. It only affects
    this running script and subprocesses launched from it.
    """
    current_entries = get_path_entries()
    directory_text = str(directory)

    new_entries = [directory_text] + [
        entry for entry in current_entries if entry != directory_text
    ]

    os.environ["PATH"] = os.pathsep.join(new_entries)
    logging.info("Prepended to current process PATH: %s", directory)


def ensure_line_in_file(path: Path, line: str) -> bool:
    """
    Add a line to a file if it is not already present.

    Returns True if the file was changed.
    """
    existing = path.read_text(encoding="utf-8") if path.exists() else ""

    if line in existing.splitlines():
        return False

    with path.open("a", encoding="utf-8") as f:
        if existing and not existing.endswith("\n"):
            f.write("\n")
        f.write(line)
        f.write("\n")

    return True


def maybe_install_homebrew() -> Path | None:
    """Offer to install Homebrew if missing."""
    brew_command = find_homebrew_command()

    if brew_command:
        print(f"\nHomebrew appears to be installed at:\n  {brew_command}")
        return brew_command

    print("\nHomebrew was not found.")
    print("Homebrew is a popular package manager for macOS.")
    print("For Apple Silicon Macs, it commonly installs tools under:")
    print("  /opt/homebrew")

    should_install = ask_yes_no(
        "\nDo you want this script to run the official Homebrew installer?",
        default=False,
    )

    if not should_install:
        print("\nSkipping Homebrew installation.")
        return None

    print("\nAbout to run the official Homebrew installer.")
    print("The installer may ask for your macOS password.")
    print("It may also print additional instructions after it finishes.")

    pause()

    install_command = [
        "/bin/bash",
        "-c",
        "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)",
    ]

    exit_code = run_interactive_command(install_command)

    if exit_code != 0:
        print("\nHomebrew installation did not complete successfully.")
        print("You can install it manually later from the official Homebrew instructions.")
        return None

    brew_command = find_homebrew_command()

    if brew_command:
        print(f"\nHomebrew is now available at:\n  {brew_command}")
        return brew_command

    print("\nThe Homebrew installer finished, but this script still cannot find brew.")
    print("You may need to open a new terminal or update your PATH.")
    return None


def maybe_add_homebrew_to_shell_path(homebrew_bin: Path) -> None:
    """
    Offer to add Homebrew's bin directory to ~/.zprofile.

    Also updates the current Python process PATH so this script can keep going.
    """
    print("\nChecking whether Homebrew's bin directory is early on PATH.")
    print(f"Homebrew bin directory expected for this machine:\n  {homebrew_bin}")

    current_python = shutil.which("python3")
    current_brew = shutil.which("brew")

    print("\nCurrently resolved commands:")
    print(f"  brew:    {current_brew or 'not found on PATH'}")
    print(f"  python3: {current_python or 'not found on PATH'}")

    homebrew_before_usr_bin = path_contains_before(homebrew_bin, Path("/usr/bin"))

    if homebrew_before_usr_bin:
        print("\nHomebrew already appears before /usr/bin on PATH.")
        return

    print("\nHomebrew does not appear before /usr/bin on PATH.")
    print("That means macOS may find Apple's system Python before Homebrew Python.")
    print("\nRecommended PATH line for Apple Silicon macOS:")
    print(f'  export PATH="{homebrew_bin}:$PATH"')

    choice = ask_choice(
        "What do you want to do?",
        choices={
            "1": "Add this PATH line to ~/.zprofile and update PATH for this script",
            "2": "Only update PATH for this script right now",
            "3": "Skip PATH changes",
        },
        default="1",
    )

    if choice == "1":
        zprofile = Path.home() / ".zprofile"
        line = f'export PATH="{homebrew_bin}:$PATH"'

        changed = ensure_line_in_file(zprofile, line)

        if changed:
            print(f"\nAdded PATH line to:\n  {zprofile}")
        else:
            print(f"\nPATH line was already present in:\n  {zprofile}")

        prepend_to_current_process_path(homebrew_bin)

        print("\nUpdated PATH for this running script.")
        print("\nFor future terminal windows, ~/.zprofile should be loaded automatically.")
        print("To apply it immediately in your current terminal after this script exits, run:")
        print(f"  source {zprofile}")

    elif choice == "2":
        prepend_to_current_process_path(homebrew_bin)
        print("\nUpdated PATH for this running script only.")
        print("This change will not persist after the script exits.")

    else:
        print("\nSkipping PATH changes.")


def homebrew_python_exists(homebrew_bin: Path) -> bool:
    """Return True if Homebrew-managed python3 appears to exist."""
    return (homebrew_bin / "python3").exists()


def maybe_install_homebrew_python(brew_command: Path, homebrew_bin: Path) -> None:
    """Offer to install Python using Homebrew if Homebrew Python is missing."""
    if homebrew_python_exists(homebrew_bin):
        print(f"\nHomebrew-managed Python appears to exist at:\n  {homebrew_bin / 'python3'}")
        return

    print("\nHomebrew-managed Python was not found at:")
    print(f"  {homebrew_bin / 'python3'}")

    should_install = ask_yes_no(
        "\nDo you want to install Python using Homebrew now?",
        default=True,
    )

    if not should_install:
        print("\nSkipping Homebrew Python installation.")
        return

    print("\nAbout to run:")
    print("  brew install python")

    pause()

    exit_code = run_interactive_command([str(brew_command), "install", "python"])

    if exit_code != 0:
        raise RuntimeError("Homebrew Python installation failed.")

    print("\nHomebrew Python installation command finished.")


def print_python_resolution() -> None:
    """Print all python3 locations and the selected python3 version."""
    print("\nPython resolution check:")

    which_all = run_command(["/usr/bin/env", "which", "-a", "python3"])

    if which_all.stdout.strip():
        print(which_all.stdout.strip())
    else:
        print("No python3 found by `which -a python3`.")

    selected_python = shutil.which("python3")

    if not selected_python:
        print("\nNo python3 is currently available on PATH.")
        return

    version_result = run_command([selected_python, "--version"])

    version_text = version_result.stdout.strip() or version_result.stderr.strip()

    print("\nSelected python3:")
    print(f"  path:    {selected_python}")
    print(f"  version: {version_text or 'unknown'}")


def macos_homebrew_python_assistant() -> None:
    """
    Interactive helper for macOS Apple Silicon users.

    Goals:
    - Check whether Homebrew is installed.
    - Offer to install Homebrew if missing.
    - Check whether Homebrew Python exists.
    - Offer to install Python with Homebrew.
    - Check whether Homebrew's bin directory appears before /usr/bin on PATH.
    - Offer to update ~/.zprofile and/or current process PATH.
    """
    if not ENABLE_MACOS_HOMEBREW_PYTHON_HELPER:
        return

    if TARGET_OS != "macos_linux":
        return

    if not is_macos():
        return

    if not is_apple_silicon():
        print("\nmacOS detected, but this does not appear to be Apple Silicon.")
        print("Skipping the Apple Silicon Homebrew Python helper.")
        return

    print("\nmacOS Apple Silicon detected.")
    print("This script can help make sure your project uses Homebrew-managed Python.")
    print("\nWhy this matters:")
    print("  /usr/bin/python3 is Apple's system-managed Python.")
    print("  For development, you usually want Homebrew Python first on PATH:")
    print("  /opt/homebrew/bin/python3")

    choice = ask_choice(
        "How do you want to handle the macOS Python check?",
        choices={
            "1": "Run the interactive Homebrew/Python/PATH check",
            "2": "Show current Python info only",
            "3": "Skip this check",
        },
        default="1",
    )

    if choice == "3":
        print("\nSkipping macOS Homebrew Python checks.")
        return

    print_python_resolution()

    if choice == "2":
        return

    homebrew_bin = get_expected_homebrew_bin_dir()

    brew_command = maybe_install_homebrew()

    if not brew_command:
        print("\nContinuing without Homebrew.")
        print("The virtual environment will be created using whichever python3 is on PATH.")
        pause()
        return

    # Make sure Homebrew's bin is available to this running script if brew was
    # found in a standard Homebrew location but not on PATH.
    if brew_command.parent.exists():
        prepend_to_current_process_path(brew_command.parent)

    maybe_add_homebrew_to_shell_path(homebrew_bin)
    maybe_install_homebrew_python(brew_command, homebrew_bin)

    if homebrew_python_exists(homebrew_bin):
        if str(homebrew_bin) not in get_path_entries():
            print("\nHomebrew Python exists, but Homebrew bin is still not on PATH.")
            should_update_now = ask_yes_no(
                "Update PATH for this running script so it can use Homebrew Python?",
                default=True,
            )
            if should_update_now:
                prepend_to_current_process_path(homebrew_bin)

    print_python_resolution()

    selected_python = shutil.which("python3")

    if selected_python and selected_python.startswith("/usr/bin/"):
        print("\nWARNING:")
        print("  python3 still resolves to Apple's system Python:")
        print(f"  {selected_python}")
        print("\nYou can continue, but the venv may be created using system Python.")

        should_continue = ask_yes_no(
            "Do you want to continue anyway?",
            default=False,
        )

        if not should_continue:
            exit_script("Setup stopped before creating the virtual environment.")

    elif selected_python:
        print("\nGood: python3 resolves to:")
        print(f"  {selected_python}")

    pause("macOS Python check complete. Press Enter to continue, or type 'exit' to quit...")


def get_base_python_path() -> Path:
    """
    Return the Python executable to use for creating the venv.

    On macOS/Linux, this intentionally uses python3 from PATH, so Homebrew Python
    can be preferred when /opt/homebrew/bin appears before /usr/bin.
    """
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

    should_create = ask_yes_no(
        "\nCreate the virtual environment now?",
        default=True,
    )

    if not should_create:
        exit_script("Setup stopped before creating the virtual environment.")

    logging.info("Creating virtual environment at %s", VENV_DIR)

    result = run_command([str(base_python), "-m", "venv", str(VENV_DIR)])

    if result.returncode != 0:
        raise RuntimeError("Failed to create virtual environment. See log file for details.")

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

    should_update = ask_yes_no(
        "Create/update .gitignore now?",
        default=True,
    )

    if not should_update:
        print("Skipping .gitignore update.")
        return

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
        print(f".gitignore updated:\n  {gitignore}")
    else:
        logging.info(".gitignore already had required ignore rules.")
        print(".gitignore already had the required ignore rules.")


def create_requirements_txt(include_dev: bool) -> None:
    """Create requirements.txt and optional requirements-dev.txt."""
    requirements = PROJECT_ROOT / "requirements.txt"

    if requirements.exists():
        print("\nrequirements.txt already exists.")
        should_overwrite = ask_yes_no("Overwrite it?", default=False)
        if not should_overwrite:
            logging.info("Keeping existing requirements.txt.")
            return

    print("\nAbout to write requirements.txt with:")
    for dependency in DEPENDENCIES:
        print(f"  - {dependency}")

    should_write = ask_yes_no(
        "Write requirements.txt now?",
        default=True,
    )

    if not should_write:
        print("Skipping requirements.txt.")
        return

    requirements.write_text("\n".join(DEPENDENCIES) + "\n", encoding="utf-8")
    logging.info("Wrote requirements.txt.")
    print(f"Wrote:\n  {requirements}")

    if include_dev:
        dev_file = PROJECT_ROOT / "requirements-dev.txt"
        dev_content = ["-r requirements.txt", "", *DEV_DEPENDENCIES]

        print("\nAbout to write requirements-dev.txt with:")
        for dependency in DEV_DEPENDENCIES:
            print(f"  - {dependency}")

        should_write_dev = ask_yes_no(
            "Write requirements-dev.txt now?",
            default=True,
        )

        if should_write_dev:
            dev_file.write_text("\n".join(dev_content) + "\n", encoding="utf-8")
            logging.info("Wrote requirements-dev.txt.")
            print(f"Wrote:\n  {dev_file}")
        else:
            print("Skipping requirements-dev.txt.")


def create_pyproject_toml(include_dev: bool) -> None:
    """Create a minimal pyproject.toml and package structure."""
    pyproject = PROJECT_ROOT / "pyproject.toml"

    if pyproject.exists():
        print("\npyproject.toml already exists.")
        should_overwrite = ask_yes_no("Overwrite it?", default=False)
        if not should_overwrite:
            logging.info("Keeping existing pyproject.toml.")
            return

    package_root = (
        PROJECT_ROOT / "src" / PACKAGE_IMPORT_NAME
        if USE_SRC_LAYOUT
        else PROJECT_ROOT / PACKAGE_IMPORT_NAME
    )

    print("\nAbout to create pyproject.toml and package structure.")
    print(f"Project name:        {PROJECT_NAME}")
    print(f"Import package name: {PACKAGE_IMPORT_NAME}")
    print(f"Package folder:      {package_root}")

    should_create = ask_yes_no(
        "Create pyproject.toml and package files now?",
        default=True,
    )

    if not should_create:
        print("Skipping pyproject.toml/package creation.")
        return

    package_root.mkdir(parents=True, exist_ok=True)

    init_file = package_root / "__init__.py"
    cli_file = package_root / "cli.py"

    init_file.write_text(
        '"""Project package."""\n\n__version__ = "0.1.0"\n',
        encoding="utf-8",
    )

    cli_file.write_text(
        textwrap.dedent(
            f'''\
            """Command-line interface for {PROJECT_NAME}."""

            import argparse


            def main() -> None:
                """Run the command-line program."""
                parser = argparse.ArgumentParser(
                    description="Example command generated by the setup helper."
                )
                parser.add_argument(
                    "name",
                    nargs="?",
                    default="World",
                    help="Name to greet.",
                )

                args = parser.parse_args()
                print(f"Hello {{args.name}}!")


            if __name__ == "__main__":
                main()
            '''
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

    print(f"Wrote:\n  {pyproject}")
    print(f"Created package folder:\n  {package_root}")


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

    should_install = ask_yes_no(
        "Install dependencies now?",
        default=True,
    )

    if not should_install:
        print("\nSkipping dependency installation.")
        return

    if ASK_TO_UPGRADE_PIP and ask_yes_no(
        "Upgrade pip inside the virtual environment first?",
        default=True,
    ):
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


def get_macos_notes_section() -> str:
    """Return macOS notes for SETUP_NOTES.md."""
    if TARGET_OS != "macos_linux":
        return ""

    return textwrap.dedent(
        """\

        ## macOS Apple Silicon: Homebrew Python

        Apple's system Python usually lives here:

        ```text
        /usr/bin/python3
        ```

        For development on Apple Silicon Macs, it is usually better to install
        Python using Homebrew:

        ```bash
        brew install python
        ```

        Homebrew's Python usually lives here:

        ```text
        /opt/homebrew/bin/python3
        ```

        Verify which Python your shell finds first:

        ```bash
        which -a python3
        python3 --version
        ```

        If `/usr/bin/python3` appears before `/opt/homebrew/bin/python3`, add
        Homebrew to the front of your PATH:

        ```bash
        echo 'export PATH="/opt/homebrew/bin:$PATH"' >> ~/.zprofile
        source ~/.zprofile
        ```

        Then verify again:

        ```bash
        which python3
        python3 --version
        ```
        """
    )


def write_local_notes() -> None:
    """Write a small local note file summarizing commands."""
    notes = PROJECT_ROOT / "SETUP_NOTES.md"

    print("\nAbout to write SETUP_NOTES.md.")
    should_write = ask_yes_no(
        "Write setup notes now?",
        default=True,
    )

    if not should_write:
        print("Skipping SETUP_NOTES.md.")
        return

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

            ## Virtual environment Python

            The virtual environment Python should be located at:

            ```text
            {get_venv_python_path()}
            ```

            Verify it with:

            ```bash
            {get_venv_python_path()} --version
            ```
            """
        )
        + get_macos_notes_section(),
        encoding="utf-8",
    )

    logging.info("Wrote SETUP_NOTES.md.")
    print(f"Wrote:\n  {notes}")


def print_final_summary() -> None:
    """Print final setup summary."""
    print("\nSetup complete.")
    print(f"Log file:\n  {LOG_FILE}")

    print("\nTo activate your environment, run:")
    print(f"  {get_activation_command()}")

    print("\nTo verify the venv Python, run:")
    print(f"  {get_venv_python_path()} --version")

    if TARGET_OS == "macos_linux" and is_macos() and is_apple_silicon():
        print("\nFor macOS Apple Silicon, also verify your shell Python:")
        print("  which -a python3")
        print("  python3 --version")

    if PROJECT_STYLE == "pyproject":
        print("\nTry the generated command after activation:")
        print(f"  {PROJECT_NAME} Demetrius")
        print("\nOr run the module directly:")
        print(f"  python -m {PACKAGE_IMPORT_NAME}.cli Demetrius")


def main() -> None:
    """Main interactive setup flow."""
    try:
        validate_config()
        print_intro()

        macos_homebrew_python_assistant()

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
        print_final_summary()

    except KeyboardInterrupt:
        logging.warning("Setup cancelled by user.")
        print("\nSetup cancelled.")
        print(f"Log file:\n  {LOG_FILE}")
        sys.exit(130)

    except Exception as exc:
        logging.exception("Setup failed.")
        print(f"\nSetup failed: {exc}")
        print(f"See log file:\n  {LOG_FILE}")
        sys.exit(1)


if __name__ == "__main__":
    main()
