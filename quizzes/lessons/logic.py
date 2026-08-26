"""Platform-neutral Lesson quiz facade and hint policies.

The reusable written, choice, conjugation, sentence, catalog, settings, and
session implementations live in :mod:`kotomi.core`. This module exposes those
shared capabilities together with the small presentation-neutral adapters used
by the Lesson package. It intentionally imports neither Kivy nor Tkinter.
"""

from __future__ import annotations

from pathlib import Path
import sys
from typing import List


APP_ROOT = Path(__file__).resolve().parent
INSTALL_ROOT = APP_ROOT.parents[1]
for search_path in (INSTALL_ROOT, APP_ROOT):
    if str(search_path) not in sys.path:
        sys.path.insert(0, str(search_path))

from kotomi.core.quiz import (
    build_choice_questions,
    build_written_questions,
    eligible_count,
)
from kotomi.core.quiz import (
    available_forms,
    build_conjugation_questions,
    conjugation_base_hint,
)
from kotomi.application.lesson_catalog_sync import synchronize_catalog
from kotomi.core.lessons import (
    FIELD_LABELS,
    FORM_LABELS,
    FORM_ORDER,
    Lesson,
    LessonCatalog,
    LessonWord,
    is_available,
)
from kotomi.core.quiz import Question, QuizSession
from kotomi.application.lesson_sentence_quiz import LessonSentenceQuiz
from kotomi.application.settings import AppSettings
from kotomi.application.storage import CatalogStore, SettingsStore
from platforms.mobile.presentation import (
    fitted_compact_text_layout,
    fitted_single_line_font_size,
    format_grammatical_hint_entry,
    format_mobile_hint_entries,
)


QUIZ_DATA_DIR = INSTALL_ROOT / "data"
QUIZ_PROJECT = QUIZ_DATA_DIR / "quiz_project.xml"

def fitted_choice_text_layout(
    natural_line_widths: List[float],
    available_width: float,
    *,
    preferred_sp: float,
    minimum_sp: float,
) -> tuple[int, float]:
    """Fit a choice while preserving an explicit option/hint line break."""
    widths = [max(0.0, float(value)) for value in natural_line_widths] or [0.0]
    if len(widths) > 1:
        return min(2, len(widths)), fitted_single_line_font_size(
            max(widths),
            available_width,
            preferred_sp=preferred_sp,
            minimum_sp=minimum_sp,
        )
    return fitted_compact_text_layout(
        widths[0],
        available_width,
        preferred_sp=preferred_sp,
        minimum_sp=minimum_sp,
        maximum_lines=2,
    )


def sentence_lexical_items(question: Question, project: object) -> List[str]:
    """Return readable lexical items selected for a mobile sentence card.

    Sentence questions already carry the completed engine bindings in their
    metadata.  Resolve those IDs against the loaded project here so the mobile
    Hint can show useful vocabulary without revealing the generated answer.
    This adapter is deliberately local to the mobile lessons application and
    therefore does not change the desktop question or hint policy.
    """

    bindings: List[tuple[str, str]] = []
    for binding in question.metadata.get("bindings", "").split(","):
        slot, separator, identifiers = binding.strip().partition("=")
        if not separator:
            continue
        for identifier in identifiers.split("+"):
            identifier = identifier.strip()
            selected_binding = (slot.strip(), identifier)
            if identifier and selected_binding not in bindings:
                bindings.append(selected_binding)
    if question.focus_word_id and all(
        identifier != question.focus_word_id for _slot, identifier in bindings
    ):
        bindings.append(("", question.focus_word_id))

    entities = getattr(project, "entities", {})
    dictionaries = getattr(project, "words", {})
    slots = {}
    pattern_id = question.metadata.get("pattern", "")
    try:
        slots = project.analyze_pattern(pattern_id).slots if pattern_id else {}
    except (AttributeError, KeyError, ValueError):
        slots = {}
    entries: List[dict[str, str]] = []
    context_kana = str(question.metadata.get("context_kana", "") or "").strip()
    context_translation = str(
        question.metadata.get("context_translation", "") or ""
    ).strip()
    if context_kana.casefold() != "n/a":
        context_kana = context_kana.rstrip(" 、。")
        if context_kana:
            entries.append(
                {
                    "translation": context_translation.rstrip(" ,."),
                    "kana": context_kana,
                    "hint_kind": "context",
                }
            )
    seen_items: set[tuple[str, str]] = set()
    for slot, identifier in bindings:
        slot_definition = slots.get(slot)
        item = None
        resolved_dictionary = ""
        if getattr(slot_definition, "kind", "") == "entity":
            item = entities.get(identifier)
            resolved_dictionary = str(
                (getattr(item, "dictionary", "") or "entity")
                if item is not None
                else ""
            )
        else:
            dictionary_id = getattr(slot_definition, "dictionary", "")
            item = dictionaries.get(dictionary_id, {}).get(identifier)
            if item is not None:
                resolved_dictionary = str(dictionary_id)
        # Older cards may not identify their slot. Keep a collision-safe
        # fallback for those cards, but prefer the analyzed slot above.
        if item is None:
            for dictionary_id, dictionary in dictionaries.items():
                if identifier in dictionary:
                    item = dictionary[identifier]
                    resolved_dictionary = str(dictionary_id)
                    break
        if item is None:
            item = entities.get(identifier)
            if item is not None:
                resolved_dictionary = str(
                    getattr(item, "dictionary", "") or "entity"
                )
        if item is None:
            continue
        resolved_key = (resolved_dictionary, identifier)
        if resolved_key in seen_items:
            continue
        seen_items.add(resolved_key)

        kana = str(getattr(item, "kana", "") or "").strip()
        kanji = str(getattr(item, "kanji", "") or "").strip()
        translation = str(getattr(item, "translation", "") or "").strip()
        romaji = str(getattr(item, "romaji", "") or "").strip()
        entries.append(
            {
                "translation": translation,
                "kana": kana,
                "kanji": kanji,
                "romaji": romaji,
                "type": str(getattr(item, "type", "") or ""),
                "dictionary_id": resolved_dictionary,
            }
        )
    result: List[str] = []
    for entry in entries:
        kind = str(entry.pop("hint_kind", "") or "")
        if kind == "context":
            value = format_mobile_hint_entries((entry,))
        else:
            value = format_grammatical_hint_entry(entry)
        if value:
            result.append(value)
    return result


def conjugation_lexical_hint(question: Question, project: object) -> str:
    """Format a conjugation base word like the other mobile quiz Hints."""
    dictionary_id = str(question.metadata.get("dictionary_id", "") or "").strip()
    dictionary_word_id = str(
        question.metadata.get("dictionary_word_id", "") or ""
    ).strip()
    dictionaries = getattr(project, "words", {})
    selected = dictionaries.get(dictionary_id, {}).get(dictionary_word_id)
    if selected is None:
        focus_word_id = str(getattr(question, "focus_word_id", "") or "").strip()
        for candidate_dictionary_id, dictionary in dictionaries.items():
            if focus_word_id and focus_word_id in dictionary:
                selected = dictionary[focus_word_id]
                dictionary_id = str(candidate_dictionary_id)
                break
    if selected is not None:
        return format_grammatical_hint_entry(
            {
                "translation": str(getattr(selected, "translation", "") or ""),
                "kana": str(getattr(selected, "kana", "") or ""),
                "kanji": str(getattr(selected, "kanji", "") or ""),
                "romaji": str(getattr(selected, "romaji", "") or ""),
                "type": str(getattr(selected, "type", "") or ""),
                "dictionary_id": dictionary_id,
            }
        )

    # Compatibility fallback for older/custom lesson catalogs whose grammar
    # dictionary reference cannot be resolved. Keep the same compact shape,
    # even if the exact conjugation class is unavailable.
    translation = str(question.metadata.get("base_translation", "") or "").strip()
    kana = str(question.metadata.get("base_kana", "") or "").strip()
    lexical_kind = {
        "verbs": "verb",
        "adjectives": "adjective",
        "nouns": "noun",
    }.get(dictionary_id, "word")
    return format_grammatical_hint_entry(
        {
            "translation": translation,
            "kana": kana,
            "dictionary_id": dictionary_id,
        },
        kind=lexical_kind,
    )


def lexical_hint_items(question: Question) -> List[str]:
    """Return card vocabulary without reproducing an accepted answer.

    Non-sentence lesson cards already carry the source word's lexical values
    in ``Question.hint``. Keep those values useful on mobile, but remove any
    value that is itself one of the accepted answers.
    """

    values = [part.strip() for part in question.hint.split("|") if part.strip()]
    if not values:
        values = [
            str(question.metadata.get(name, "") or "").strip()
            for name in ("translation", "kana", "kanji", "romaji")
        ]
    forbidden = {
        answer.strip().casefold()
        for answer in question.answers
        if answer.strip()
    }
    if question.answer_field == "japanese_form":
        # Conjugation metadata may carry the target in Kana, Kanji, or Romaji.
        # Hide every stored target representation, not only the representation
        # used by ``answers``, while retaining safe base-word vocabulary.
        forbidden.update(
            value.casefold()
            for value in (
                str(question.metadata.get(name, "") or "").strip()
                for name in ("kana", "kanji", "romaji")
            )
            if value and value.casefold() != "n/a"
        )
    result: List[str] = []
    for value in values:
        normalized = value.casefold()
        if not value or normalized == "n/a" or normalized in forbidden:
            continue
        if value not in result:
            result.append(value)
    return result


def safe_option_hint(
    question: Question,
    option: str,
    project: object | None = None,
) -> str:
    """Return translation / Kana / Kanji for one four-answer choice."""

    values: List[str] = []
    for part in question.option_hints.get(option, "").split("|"):
        value = part.strip()
        normalized = value.casefold()
        if not value or normalized == "n/a":
            continue
        if value not in values:
            values.append(value)
    if not values and option and option.casefold() != "n/a":
        values.append(option)
    return " / ".join(values[:3])


def conjugation_translation_hint(question: Question) -> str:
    """Compatibility alias for callers of the previous helper."""

    return conjugation_base_hint(question)


__all__ = [
    "APP_ROOT",
    "INSTALL_ROOT",
    "QUIZ_DATA_DIR",
    "QUIZ_PROJECT",
    "FIELD_LABELS",
    "FORM_LABELS",
    "FORM_ORDER",
    "Lesson",
    "LessonCatalog",
    "LessonWord",
    "Question",
    "QuizSession",
    "LessonSentenceQuiz",
    "AppSettings",
    "CatalogStore",
    "SettingsStore",
    "available_forms",
    "build_choice_questions",
    "build_conjugation_questions",
    "build_written_questions",
    "conjugation_base_hint",
    "eligible_count",
    "is_available",
    "synchronize_catalog",
    "fitted_choice_text_layout",
    "sentence_lexical_items",
    "conjugation_lexical_hint",
    "lexical_hint_items",
    "safe_option_hint",
    "conjugation_translation_hint",
]
