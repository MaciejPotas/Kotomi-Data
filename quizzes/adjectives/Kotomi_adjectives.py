"""Compatibility entrypoint for the Adjectives quiz package.

The platform-neutral implementation lives in :mod:`logic`, while the Kivy
presentation lives in :mod:`mobile`. This module preserves the public API and
entrypoint used by existing Desktop, Mobile, Pydroid, and updater installs.
"""

from __future__ import annotations

from pathlib import Path
import sys


SCRIPT_DIR = Path(__file__).resolve().parent
INSTALL_ROOT = SCRIPT_DIR.parents[1]
if str(INSTALL_ROOT) not in sys.path:
    sys.path.insert(0, str(INSTALL_ROOT))

from apps.adjectives import logic as _logic
from apps.adjectives import mobile as _mobile
from apps.adjectives.logic import *
from apps.adjectives.mobile import (
    create_app_class,
    create_embedded_controller,
    main,
    mobile_sentence_hint_items,
)


def __getattr__(name: str):
    if hasattr(_logic, name):
        return getattr(_logic, name)
    if hasattr(_mobile, name):
        return getattr(_mobile, name)
    raise AttributeError(name)


if __name__ == "__main__":
    raise SystemExit(main())
