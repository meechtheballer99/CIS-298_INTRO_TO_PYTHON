"""Main command-line flow for the educational project setup helper."""

from __future__ import annotations

import logging
import platform
import sys

from project_setup_helper.config import DEV_DEPENDENCIES, PROJECT_STYLE, TARGET_OS, VENV_DIR_NAME, validate_config
from project_setup_helper.dependencies import install_dependencies
from project_setup_helper.installers.macos_apple_silicon import macos_homebrew_python_assistant
from project_setup_helper.installers.macos_linux import run_macos_linux_check
from project_setup_helper.installers.windows import run_windows_check
from project_setup_helper.logging_setup import configure_logging
from project_setup_helper.notes import print_final_summary, write_local_notes
from project_setup_helper.os_detect import get_platform_key
from project_setup_helper.paths import LOG_FILE, PROJECT_ROOT, VENV_DIR
from project_setup_helper.project_files.gitignore import ensure_gitignore
from project_setup_helper.project_files.pyproject import create_pyproject_toml
from project_setup_helper.project_files.requirements import create_requirements_txt
from project_setup_helper.prompts import ask_yes_no, pause
from project_setup_helper.venv_tools import create_virtual_environment


def print_intro() -> None:
    """Explain what the helper is configured to do."""
    detected_os = platform.system()
    detected_machine = platform.machine()

    logging.info("Starting interactive Python project setup.")
    logging.info("Project root: %s", PROJECT_ROOT)
    logging.info("Detected system: %s", detected_os)
    logging.info("Detected machine: %s", detected_machine)
    logging.info("Configured TARGET_OS: %s", TARGET_OS)
    logging.info("Configured PROJECT_STYLE: %s", PROJECT_STYLE)
    logging.info("Configured venv folder: %s", VENV_DIR)

    print("\nThis package will help set up a Python project.")
    print("\nCurrent configuration:")
    print(f"  TARGET_OS:            {TARGET_OS}")
    print(f"  PROJECT_STYLE:        {PROJECT_STYLE}")
    print(f"  VENV_DIR_NAME:        {VENV_DIR_NAME}")

    print("\nDetected machine:")
    print(f"  OS:                   {detected_os}")
    print(f"  CPU/architecture:     {detected_machine}")

    print(f"\nProject root that will be modified:\n  {PROJECT_ROOT}")
    print(f"\nLog file will be written to:\n  {LOG_FILE}")

    pause(
        "Review the configuration above. "
        "If it is wrong, type 'exit', edit project_setup_helper/config.py, and rerun. "
        "Otherwise press Enter to continue..."
    )


def run_platform_check() -> None:
    """Dispatch to platform-specific preflight checks."""
    platform_key = get_platform_key()

    if platform_key == "macos_apple_silicon":
        macos_homebrew_python_assistant()
    elif platform_key == "windows":
        run_windows_check()
    else:
        run_macos_linux_check()


def main() -> None:
    """Main interactive setup flow."""
    configure_logging()

    try:
        validate_config()
        print_intro()
        run_platform_check()

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
