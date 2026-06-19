"""Small input/prompt helpers.

Teaching note: these functions are in their own module because many other
parts of the package need to ask the user questions. Shared behavior belongs in
one reusable place.
"""

from __future__ import annotations

import logging
import sys

from project_setup_helper.config import EXIT_WORDS
from project_setup_helper.paths import LOG_FILE


def exit_script(message: str = "Exiting setup.") -> None:
    """Exit the helper cleanly."""
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
    """Ask the user to choose from numbered options."""
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
