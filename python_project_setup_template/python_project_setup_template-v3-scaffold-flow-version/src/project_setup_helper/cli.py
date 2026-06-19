"""Main command-line flow for the educational project setup helper."""

from __future__ import annotations

import logging
import platform
import sys
from pathlib import Path

from project_setup_helper.config import (
    DEV_DEPENDENCIES,
    ProjectConfig,
    normalize_project_name,
    package_name_from_project_name,
)
from project_setup_helper.dependencies import install_dependencies
from project_setup_helper.installers.macos_apple_silicon import macos_homebrew_python_assistant
from project_setup_helper.installers.macos_linux import run_macos_linux_check
from project_setup_helper.installers.windows import run_windows_check
from project_setup_helper.logging_setup import configure_logging
from project_setup_helper.notes import print_final_summary, write_local_notes
from project_setup_helper.os_detect import get_platform_key
from project_setup_helper.paths import setup_log_file
from project_setup_helper.project_files.gitignore import ensure_gitignore
from project_setup_helper.project_files.pyproject import create_pyproject_package
from project_setup_helper.project_files.requirements import create_requirements_project
from project_setup_helper.prompts import ask_choice, ask_text, ask_yes_no, pause, set_log_file
from project_setup_helper.venv_tools import create_virtual_environment


def print_intro() -> None:
    """Explain the scaffold flow."""
    detected_os = platform.system()
    detected_machine = platform.machine()

    print("\nInteractive Python Project Setup Helper")
    print("\nThis tool creates a beginner-friendly Python project and explains each step.")
    print("\nFlow:")
    print("  Step 1: Choose project type")
    print("  Step 2: Choose project name")
    print("  Step 3: Choose destination")
    print("  Step 4: Generate project")
    print("\nDetected machine:")
    print(f"  OS:               {detected_os}")
    print(f"  CPU/architecture: {detected_machine}")
    pause("Press Enter to start, or type 'exit' to quit...")


def run_platform_check() -> None:
    """Dispatch to platform-specific preflight checks."""
    platform_key = get_platform_key()
    if platform_key == "macos_apple_silicon":
        macos_homebrew_python_assistant()
    elif platform_key == "windows":
        run_windows_check()
    else:
        run_macos_linux_check()


def choose_project_type() -> str:
    """Step 1: choose the kind of project to generate."""
    choice = ask_choice(
        "Step 1: Choose project type",
        choices={
            "1": "requirements.txt project",
            "2": "pyproject package",
        },
        default="1",
    )
    return "requirements" if choice == "1" else "pyproject"


def choose_project_name() -> tuple[str, str]:
    """Step 2: ask for project name and derive import package name."""
    raw_name = ask_text("\nStep 2: Project name", default="my-python-project")
    project_name = normalize_project_name(raw_name)
    package_name = package_name_from_project_name(project_name)

    print("\nName conversion:")
    print(f"  Distribution/folder name: {project_name}")
    print(f"  Import package name:      {package_name}")
    print("\nTeaching note: installs often use hyphens, but Python imports use underscores.")
    return project_name, package_name


def choose_destination(project_name: str) -> Path:
    """Step 3: choose where the generated project should live."""
    choice = ask_choice(
        "Step 3: Choose destination",
        choices={
            "1": "Current directory",
            "2": "generated_projects/",
            "3": "Custom path",
        },
        default="2",
    )

    cwd = Path.cwd().resolve()
    if choice == "1":
        return cwd
    if choice == "2":
        return cwd / "generated_projects" / project_name

    custom = ask_text("Enter custom destination path")
    custom_path = Path(custom).expanduser()
    if not custom_path.is_absolute():
        custom_path = cwd / custom_path
    return custom_path.resolve()


def build_config() -> ProjectConfig:
    """Collect all runtime choices from the user."""
    project_type = choose_project_type()
    project_name, package_name = choose_project_name()
    project_root = choose_destination(project_name)

    include_dev = ask_yes_no(
        "\nInclude development tools " f"({', '.join(DEV_DEPENDENCIES)})?",
        default=True,
    )

    return ProjectConfig(
        project_type=project_type,
        project_name=project_name,
        package_name=package_name,
        project_root=project_root,
        include_dev_tools=include_dev,
    )


def review_configuration(config: ProjectConfig) -> None:
    """Show a final summary before creating files."""
    print("\nStep 4: Review summary")
    print(f"  Project type: {config.project_type}")
    print(f"  Project name: {config.project_name}")
    print(f"  Package name: {config.package_name}")
    print(f"  Destination:  {config.project_root}")
    print(f"  Dev tools:    {'yes' if config.include_dev_tools else 'no'}")

    if config.project_root.exists() and any(config.project_root.iterdir()):
        print("\nWarning: the destination already exists and is not empty.")
        print("The helper may overwrite generated files such as README.md or pyproject.toml.")

    if not ask_yes_no("\nGenerate this project now?", default=True):
        print("\nNo files were generated.")
        sys.exit(0)


def generate_project(config: ProjectConfig) -> None:
    """Create the selected project files."""
    config.project_root.mkdir(parents=True, exist_ok=True)
    ensure_gitignore(config)

    if config.uses_requirements:
        create_requirements_project(config)
    else:
        create_pyproject_package(config)


def main() -> None:
    """Main interactive setup flow."""
    log_file: Path | None = None
    try:
        print_intro()
        run_platform_check()
        config = build_config()
        log_file = setup_log_file(config.project_root)
        set_log_file(log_file)
        configure_logging(log_file)

        logging.info("Starting interactive Python project setup.")
        logging.info("Project type: %s", config.project_type)
        logging.info("Project name: %s", config.project_name)
        logging.info("Package name: %s", config.package_name)
        logging.info("Project root: %s", config.project_root)

        review_configuration(config)
        generate_project(config)
        create_virtual_environment(config)
        install_dependencies(config)
        write_local_notes(config)
        print_final_summary(config, log_file)

    except KeyboardInterrupt:
        logging.warning("Setup cancelled by user.")
        print("\nSetup cancelled.")
        if log_file is not None:
            print(f"Log file:\n  {log_file}")
        sys.exit(130)
    except Exception as exc:
        logging.exception("Setup failed.")
        print(f"\nSetup failed: {exc}")
        if log_file is not None:
            print(f"See log file:\n  {log_file}")
        sys.exit(1)
