"""Runtime helpers for local runs and packaged builds."""

from pathlib import Path
import sys


def get_runtime_root() -> Path:
    """Return the root directory that contains packaged app resources."""

    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS)

    return Path(__file__).resolve().parents[1]


def get_distribution_root() -> Path:
    """Return the directory where the executable or launcher lives."""

    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent

    return get_runtime_root()
