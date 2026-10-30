"""Availability adapter for the application-owned shared mobile quiz UI."""
from apps.availability.logic import (
    AvailabilityQuizSettings, AvailabilityQuizEngine, AvailabilityQuizSession,
    AvailabilityQuestion, SubmissionResult, SettingsStore,
)
from platforms.mobile.sentence_quiz import (
    create_app_class, create_embedded_controller, main, mobile_sentence_hint_entries,
    _apply_absolute_font_scale, _apply_absolute_button_scale,
)

if __name__ == "__main__":
    raise SystemExit(main())
