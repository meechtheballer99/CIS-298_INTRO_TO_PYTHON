"""Operating-system and architecture detection helpers."""

from __future__ import annotations

import platform


def is_macos() -> bool:
    """Return True if running on macOS."""
    return platform.system() == "Darwin"


def is_apple_silicon() -> bool:
    """Return True if running on Apple Silicon."""
    return platform.machine().lower() in {"arm64", "aarch64"}


def get_platform_key() -> str:
    """Return a simple platform key used by the CLI dispatcher."""
    system = platform.system()
    machine = platform.machine().lower()

    if system == "Darwin" and machine in {"arm64", "aarch64"}:
        return "macos_apple_silicon"
    if system == "Darwin":
        return "macos_other"
    if system == "Windows":
        return "windows"
    return "linux"
