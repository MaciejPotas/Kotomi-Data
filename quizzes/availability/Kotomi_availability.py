"""Compatibility entrypoint for the Availability quiz package.

The platform-neutral implementation lives in :mod:`logic`, while the Kivy
presentation lives in :mod:`mobile`. This module preserves the public API and
entrypoint used by existing Desktop, Mobile, Pydroid, and updater installs.
"""

from __future__ import annotations

try:
    from .logic import *
    from .mobile import (
        _apply_absolute_button_scale,
        _apply_absolute_font_scale,
        create_app_class,
        create_embedded_controller,
        main,
        mobile_sentence_hint_entries,
    )
except ImportError:  # Loaded directly from its package directory.
    from logic import *
    from mobile import (
        _apply_absolute_button_scale,
        _apply_absolute_font_scale,
        create_app_class,
        create_embedded_controller,
        main,
        mobile_sentence_hint_entries,
    )


if __name__ == "__main__":
    raise SystemExit(main())
