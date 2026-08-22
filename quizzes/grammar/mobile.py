"""Kivy presentation adapter for the Grammar quiz.

Grammar-specific settings and generation live in :mod:`logic`. This module
connects that policy to the reusable Availability mobile presentation.
"""

from __future__ import annotations

import sys

try:
    from .logic import *
    from .logic import _safe_float, _safe_int
    from . import logic as _logic
except ImportError:  # Direct execution from the quiz package directory.
    from logic import *
    from logic import _safe_float, _safe_int
    import logic as _logic

try:
    from apps.availability import mobile as availability_mobile
except ImportError:
    from availability import mobile as availability_mobile

def create_app_class():
    return create_mobile_sentence_app_class(sys.modules[__name__])


def create_embedded_controller():
    app_class = create_app_class()
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


if __name__ == "__main__":
    raise SystemExit(main())
