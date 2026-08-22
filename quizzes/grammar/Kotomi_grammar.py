"""Backwards-compatible entrypoint for the Grammar quiz package."""

from __future__ import annotations

try:
    from .logic import *
    from .mobile import create_app_class, create_embedded_controller, main
except ImportError:  # Direct execution from the quiz package directory.
    from logic import *
    from mobile import create_app_class, create_embedded_controller, main


if __name__ == "__main__":
    raise SystemExit(main())
