"""Synthetic quiz logic used by the Kotomi mobile update network self-test."""

PROBE_NAME = "kotomi-mobile-update"
PROBE_VERSION = 1


def probe_value() -> str:
    """Return the marker expected by the mobile update self-test."""
    return "quiz-logic-ok"
