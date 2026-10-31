"""Adjective generation policy using the shared mobile quiz presentation."""
from __future__ import annotations
import re
from types import SimpleNamespace
from typing import List
from apps.adjectives import logic
from apps.adjectives.logic import *
from kotomi.core.project import ProjectError
from platforms.mobile.presentation import format_grammatical_hint_entry, format_mobile_hint_entry

def mobile_sentence_hint_items(
    question: AdjectiveQuestion,
    project: object,
) -> List[str]:
    """Return compact vocabulary for the mobile Hint, never the answer."""

    bindings: List[tuple[str, str]] = []
    for binding in re.split(r"[,;]", question.bindings or ""):
        slot, separator, identifiers = binding.strip().partition("=")
        if not separator:
            continue
        for identifier in identifiers.split("+"):
            selected = (slot.strip(), identifier.strip())
            if selected[1] and selected not in bindings:
                bindings.append(selected)

    dictionaries = getattr(project, "words", {})
    entities = getattr(project, "entities", {})
    slots = {}
    try:
        slots = project.analyze_pattern(question.pattern_id).slots
    except (AttributeError, KeyError, ValueError, ProjectError):
        slots = {}

    result: List[tuple[str, str, str]] = []
    seen: set[tuple[str, str]] = set()

    def append_item(item: object, key: tuple[str, str]) -> None:
        if item is None or key in seen:
            return
        seen.add(key)
        kana = str(getattr(item, "kana", "") or "").strip()
        kanji = str(getattr(item, "kanji", "") or "").strip()
        translation = str(
            project.instruction_language.translation(item) or ""
        ).strip()
        if kana.casefold() == "n/a":
            kana = ""
        if kanji.casefold() == "n/a":
            kanji = ""
        if translation.casefold() == "n/a":
            translation = ""
        if translation or kana or kanji:
            formatted = format_grammatical_hint_entry(item, translation_override=translation)
            if formatted and formatted not in result:
                result.append(formatted)

    context_entry = (
        str(question.context_translation or "").strip(),
        str(question.context_kana or "").strip().rstrip(" 、。"),
        "",
    )
    if any(context_entry):
        formatted_context = format_mobile_hint_entry(context_entry)
        if formatted_context and formatted_context not in result:
            result.append(formatted_context)

    preferred_dictionaries = {
        "adjectives": "adjectives",
        "copula": "copulas",
    }
    for slot, identifier in bindings:
        slot_definition = slots.get(slot)
        item = None
        dictionary_id = preferred_dictionaries.get(slot, "")
        if getattr(slot_definition, "kind", "") == "entity" or slot == "subject":
            item = entities.get(identifier)
            dictionary_id = "entity"
        else:
            dictionary_id = dictionary_id or str(
                getattr(slot_definition, "dictionary", "") or ""
            )
            item = dictionaries.get(dictionary_id, {}).get(identifier)
        if item is None:
            for candidate_id, dictionary in dictionaries.items():
                if identifier in dictionary:
                    item = dictionary[identifier]
                    dictionary_id = str(candidate_id)
                    break
        if item is None:
            item = entities.get(identifier)
            dictionary_id = "entity"
        append_item(item, (dictionary_id, identifier))

    if not result:
        fallback = type("MobileHintWord", (), {
            "translation": question.word_meaning,
            "kana": question.word_kana,
            "kanji": question.word_kanji,
        })()
        append_item(fallback, ("adjectives", question.adjective_ids))
    return result


def quiz_policy():
    values = {key: getattr(logic, key) for key in dir(logic) if not key.startswith("__")}
    values.update(
        QUIZ_SETTINGS_CLASS=logic.AdjectiveQuizSettings,
        QUIZ_ENGINE_CLASS=logic.AdjectiveQuizEngine,
        QUIZ_SESSION_CLASS=AdjectiveQuizSession,
        SETTINGS_STORE_CLASS=logic.SettingsStore,
        QUIZ_ERROR_CLASS=logic.MobileQuizError,
        MOBILE_TITLE_KEY="specialized.adjectives_title",
        MOBILE_SUBTITLE='けいようしのクイズ',
        MOBILE_FILTER_HINT='type=i_adjective;id=oishii,hayai',
        MOBILE_HINT_ITEMS=mobile_sentence_hint_items,
        MOBILE_HELP_ID='adjectives',
        MOBILE_DIRECTION_TOGGLES=(("polite_to_plain", "specialized.polite_to_plain"),
                                 ("plain_to_polite", "specialized.plain_to_polite")),
        MOBILE_EXTRA_TOGGLES=(('enable_i_adjectives', 'specialized.i_adjectives'), ('enable_na_adjectives', 'specialized.na_adjectives')),
        MOBILE_EXTRA_NUMBERS=(('adjective_count', 'specialized.in_sentence_count'),),
    )
    return SimpleNamespace(**values)


def create_app_class():
    from platforms.mobile.sentence_quiz import create_app_class as shared_app
    return shared_app(quiz_policy())


def create_embedded_controller():
    controller = create_app_class()()
    controller.embedded_mode = True
    return controller


def main():
    create_app_class()().run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
