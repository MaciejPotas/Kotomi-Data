"""Compatibility entrypoint for the Lessons quiz package.

Platform-neutral Lesson behavior lives in :mod:`logic`, while the Kivy
presentation lives in :mod:`mobile`. This module preserves the public API and
entrypoint used by Desktop, Mobile, Pydroid, and quiz updates.
"""

from __future__ import annotations

from pathlib import Path
import sys


SCRIPT_DIR = Path(__file__).resolve().parent
INSTALL_ROOT = SCRIPT_DIR.parents[1]
if str(INSTALL_ROOT) not in sys.path:
    sys.path.insert(0, str(INSTALL_ROOT))

from apps.lessons import logic as _logic
from apps.lessons import mobile as _mobile
from apps.lessons.logic import *
from apps.lessons.mobile import (
    create_app_class,
    create_embedded_controller,
    main,
)


def __getattr__(name: str):
    if hasattr(_logic, name):
        return getattr(_logic, name)
    if hasattr(_mobile, name):
        return getattr(_mobile, name)
    raise AttributeError(name)


if __name__ == "__main__":
    raise SystemExit(main())
