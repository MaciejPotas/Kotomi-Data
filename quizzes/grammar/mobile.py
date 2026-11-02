"""Mobile adapter for data-defined Grammar quizzes.

Grammar owns only its platform-neutral policy. The complete Kivy presentation
receives the live Grammar logic module, so an
XML profile change immediately affects the rendered settings and questions.
"""

from __future__ import annotations

from pathlib import Path
import sys


SCRIPT_DIR = Path(__file__).resolve().parent
INSTALL_ROOT = SCRIPT_DIR.parents[1]
if str(INSTALL_ROOT) not in sys.path:
    sys.path.insert(0, str(INSTALL_ROOT))

from apps.grammar import logic as _logic
from platforms.mobile.sentence_quiz import (
    create_app_class as _create_mobile_sentence_app_class,
)


def create_app_class(policy=None):
    """Return the shared mobile sentence UI configured by Grammar logic."""
    return _create_mobile_sentence_app_class(policy or _logic)


def create_embedded_controller(policy=None):
    """Create a Grammar controller for the main Kotomi mobile launcher."""
    app_class = create_app_class(policy)
    controller = app_class()
    controller.embedded_mode = True
    return controller


def main() -> int:
    try:
        app_class = create_app_class()
    except ModuleNotFoundError as exception:
        if exception.name == "kivy":
            print(
                "Kivy nie jest zainstalowane. Uruchom skrypt w środowisku "
                "telefonu z obsługą Kivy, na przykład w Pydroid 3."
            )
            return 1
        raise
    app_class().run()
    return 0


__all__ = [
    "create_app_class",
    "create_embedded_controller",
    "main",
]


if __name__ == "__main__":
    raise SystemExit(main())
