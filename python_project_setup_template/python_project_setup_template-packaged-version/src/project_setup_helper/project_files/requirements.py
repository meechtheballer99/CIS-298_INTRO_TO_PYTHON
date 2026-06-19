"""Write requirements.txt files."""

from __future__ import annotations

import logging

from project_setup_helper.config import DEPENDENCIES, DEV_DEPENDENCIES
from project_setup_helper.paths import PROJECT_ROOT
from project_setup_helper.prompts import ask_yes_no


def create_requirements_txt(include_dev: bool) -> None:
    """Create requirements.txt and optional requirements-dev.txt."""
    requirements = PROJECT_ROOT / "requirements.txt"

    if requirements.exists():
        print("\nrequirements.txt already exists.")
        if not ask_yes_no("Overwrite it?", default=False):
            logging.info("Keeping existing requirements.txt.")
            return

    print("\nAbout to write requirements.txt with:")
    for dependency in DEPENDENCIES:
        print(f"  - {dependency}")

    if not ask_yes_no("Write requirements.txt now?", default=True):
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

        if ask_yes_no("Write requirements-dev.txt now?", default=True):
            dev_file.write_text("\n".join(dev_content) + "\n", encoding="utf-8")
            logging.info("Wrote requirements-dev.txt.")
            print(f"Wrote:\n  {dev_file}")
        else:
            print("Skipping requirements-dev.txt.")
