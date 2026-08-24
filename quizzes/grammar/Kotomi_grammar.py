"""Compatibility entrypoint for the Grammar quiz package.

The platform-neutral profile and engine live in :mod:`logic`. Mobile rendering
is delegated through :mod:`mobile`. This wrapper preserves the public API used
by Desktop, Mobile, Pydroid, the registry, and existing quiz packages.
"""

from __future__ import annotations

from pathlib import Path
import sys


SCRIPT_DIR = Path(__file__).resolve().parent
INSTALL_ROOT = SCRIPT_DIR.parents[1]
AVAILABILITY_DIR = INSTALL_ROOT / "apps" / "availability"
for import_root in (INSTALL_ROOT, AVAILABILITY_DIR):
    if str(import_root) not in sys.path:
        sys.path.insert(0, str(import_root))

from apps.grammar import logic as _logic
from apps.grammar import mobile as _mobile
from apps.grammar.logic import *


_PROFILE_EXPORTS = (
    "ACTIVE_QUIZ_ID",
    "SETTINGS_FILENAME",
    "PATTERN_LABELS",
    "SUPPORTED_PATTERNS",
    "MOBILE_APP_TITLE",
    "MOBILE_SUBTITLE",
    "MOBILE_SETTINGS_TITLE",
    "MOBILE_HELP_SECTIONS",
)


def _sync_profile_exports() -> None:
    """Mirror mutable profile metadata for legacy module consumers."""
    for name in _PROFILE_EXPORTS:
        globals()[name] = getattr(_logic, name)


def configure_quiz_profile(quiz_id: str) -> None:
    """Configure the live Grammar policy and refresh compatibility exports."""
    _logic.configure_quiz_profile(quiz_id)
    _sync_profile_exports()


def create_app_class():
    return _mobile.create_app_class()


def create_embedded_controller():
    return _mobile.create_embedded_controller()


def main() -> int:
    return _mobile.main()


def __getattr__(name: str):
    if hasattr(_logic, name):
        return getattr(_logic, name)
    if hasattr(_mobile, name):
        return getattr(_mobile, name)
    raise AttributeError(name)


_sync_profile_exports()

__all__ = [
    *getattr(_logic, "__all__", ()),
    "create_app_class",
    "create_embedded_controller",
    "main",
]


if __name__ == "__main__":
    raise SystemExit(main())
