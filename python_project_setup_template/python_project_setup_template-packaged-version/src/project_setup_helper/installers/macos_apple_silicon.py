"""macOS Apple Silicon-specific setup logic.

Why separate this?
Windows, macOS, and Linux use different shell commands, activation paths, and
Python installation conventions. Separating OS logic keeps the main CLI easier
to read and teaches the idea of modules with focused responsibilities.
"""

from __future__ import annotations

import logging
import os
import shutil
from pathlib import Path

from project_setup_helper.commands import run_command, run_interactive_command
from project_setup_helper.config import ENABLE_MACOS_HOMEBREW_PYTHON_HELPER, TARGET_OS
from project_setup_helper.os_detect import is_apple_silicon, is_macos
from project_setup_helper.prompts import ask_choice, ask_yes_no, exit_script, pause


def get_expected_homebrew_bin_dir() -> Path:
    """Return the conventional Homebrew bin directory for this machine."""
    if is_macos() and is_apple_silicon():
        return Path("/opt/homebrew/bin")
    return Path("/usr/local/bin")


def find_homebrew_command() -> Path | None:
    """Find the Homebrew executable from PATH or standard locations."""
    brew_from_path = shutil.which("brew")
    if brew_from_path:
        return Path(brew_from_path)

    for path in [Path("/opt/homebrew/bin/brew"), Path("/usr/local/bin/brew")]:
        if path.exists():
            return path
    return None


def get_path_entries() -> list[str]:
    """Return PATH as a list of directory strings."""
    return os.environ.get("PATH", "").split(os.pathsep)


def path_contains_before(first: Path, second: Path) -> bool:
    """Return True if first appears in PATH before second."""
    entries = get_path_entries()
    first_text = str(first)
    second_text = str(second)

    if first_text not in entries:
        return False
    if second_text not in entries:
        return True
    return entries.index(first_text) < entries.index(second_text)


def prepend_to_current_process_path(directory: Path) -> None:
    """Prepend a directory to PATH for this running script process only."""
    current_entries = get_path_entries()
    directory_text = str(directory)
    new_entries = [directory_text] + [entry for entry in current_entries if entry != directory_text]
    os.environ["PATH"] = os.pathsep.join(new_entries)
    logging.info("Prepended to current process PATH: %s", directory)


def ensure_line_in_file(path: Path, line: str) -> bool:
    """Add a line to a file if it is not already present."""
    existing = path.read_text(encoding="utf-8") if path.exists() else ""
    if line in existing.splitlines():
        return False

    with path.open("a", encoding="utf-8") as f:
        if existing and not existing.endswith("\n"):
            f.write("\n")
        f.write(line)
        f.write("\n")
    return True


def shell_profile_has_homebrew_path(homebrew_bin: Path) -> bool:
    """Return True if ~/.zprofile contains the expected Homebrew PATH line."""
    zprofile = Path.home() / ".zprofile"
    line = f'export PATH="{homebrew_bin}:$PATH"'
    if not zprofile.exists():
        return False
    return line in zprofile.read_text(encoding="utf-8").splitlines()


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

    should_install = ask_yes_no("\nDo you want this script to run the official Homebrew installer?", default=False)
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
    """Offer to add Homebrew's bin directory to ~/.zprofile."""
    print("\nChecking whether Homebrew's bin directory is early on PATH.")
    print(f"Homebrew bin directory expected for this machine:\n  {homebrew_bin}")

    current_python = shutil.which("python3")
    current_brew = shutil.which("brew")

    print("\nCurrently resolved commands for this script run:")
    print(f"  brew:    {current_brew or 'not found on PATH'}")
    print(f"  python3: {current_python or 'not found on PATH'}")

    homebrew_before_usr_bin = path_contains_before(homebrew_bin, Path("/usr/bin"))

    if homebrew_before_usr_bin:
        print("\nHomebrew appears before /usr/bin on PATH for this running script.")
        print("Next, this script will verify which python3 is actually active.")

        if not shell_profile_has_homebrew_path(homebrew_bin):
            print("\nHowever, ~/.zprofile does not appear to contain the Homebrew PATH line.")
            print("That means future terminal sessions may still use /usr/bin/python3 first.")
            print("\nRecommended line:")
            print(f'  export PATH="{homebrew_bin}:$PATH"')

            should_add = ask_yes_no("Add the Homebrew PATH line to ~/.zprofile for future terminal sessions?", default=True)
            if should_add:
                zprofile = Path.home() / ".zprofile"
                line = f'export PATH="{homebrew_bin}:$PATH"'
                changed = ensure_line_in_file(zprofile, line)
                print(f"\n{'Added PATH line to' if changed else 'PATH line was already present in'}:\n  {zprofile}")
                print("\nTo apply it in your current terminal after this script exits, run:")
                print(f"  source {zprofile}")
            else:
                print("\nSkipping ~/.zprofile update.")
        else:
            print("\n~/.zprofile already contains the Homebrew PATH line.")
            print("Future terminal sessions should also prefer Homebrew commands.")
        return

    print("\nHomebrew does not appear before /usr/bin on PATH for this running script.")
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
        print(f"\n{'Added PATH line to' if changed else 'PATH line was already present in'}:\n  {zprofile}")
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

    should_install = ask_yes_no("\nDo you want to install Python using Homebrew now?", default=True)
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
    """Interactive helper for macOS Apple Silicon users."""
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

    if brew_command.parent.exists() and str(brew_command.parent) not in get_path_entries():
        print("\nHomebrew was found, but it is not currently on PATH for this script.")
        print(f"Temporarily adding it for this script run:\n  {brew_command.parent}")
        prepend_to_current_process_path(brew_command.parent)

    maybe_add_homebrew_to_shell_path(homebrew_bin)
    maybe_install_homebrew_python(brew_command, homebrew_bin)

    if homebrew_python_exists(homebrew_bin) and str(homebrew_bin) not in get_path_entries():
        print("\nHomebrew Python exists, but Homebrew bin is still not on PATH.")
        should_update_now = ask_yes_no("Update PATH for this running script so it can use Homebrew Python?", default=True)
        if should_update_now:
            prepend_to_current_process_path(homebrew_bin)

    print_python_resolution()

    selected_python = shutil.which("python3")
    expected_homebrew_python = str(homebrew_bin / "python3")

    if selected_python == expected_homebrew_python:
        print("\nGood: python3 resolves to Homebrew-managed Python:")
        print(f"  {selected_python}")
    elif selected_python and selected_python.startswith("/usr/bin/"):
        print("\nWARNING:")
        print("  python3 still resolves to Apple's system Python:")
        print(f"  {selected_python}")
        print("\nYou can continue, but the venv may be created using system Python.")
        if not ask_yes_no("Do you want to continue anyway?", default=False):
            exit_script("Setup stopped before creating the virtual environment.")
    elif selected_python:
        print("\nNote:")
        print("  python3 does not resolve to Apple's system Python.")
        print("  It also does not resolve to the expected Homebrew Python path.")
        print("  This may be fine if you use pyenv, asdf, conda, or another Python manager.")
        print("\nCurrent python3:")
        print(f"  {selected_python}")
        if not ask_yes_no("Do you want to continue using this python3?", default=True):
            exit_script("Setup stopped before creating the virtual environment.")
    else:
        print("\nNo python3 could be found on PATH.")
        if not ask_yes_no("Do you want to continue anyway?", default=False):
            exit_script("Setup stopped before creating the virtual environment.")

    pause("macOS Python check complete. Press Enter to continue, or type 'exit' to quit...")
