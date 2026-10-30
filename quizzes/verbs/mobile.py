"""Verb generation policy using the shared mobile quiz presentation."""
from __future__ import annotations
import re
from types import SimpleNamespace
from typing import List
from apps.verbs import logic
from apps.verbs.logic import *
from kotomi.core.project import ProjectError
from platforms.mobile.presentation import format_grammatical_hint_entry, format_mobile_hint_entry

def mobile_sentence_hint_items(
    question: VerbQuestion,
    project: object,
) -> List[str]:
    """Resolve the vocabulary used by a mobile question without revealing it.

    The specialized desktop quiz keeps its existing hint presentation.  This
    small adapter is consumed only by the Kivy screen and turns the engine's
    completed bindings into compact dictionary-form Japanese vocabulary.
    """

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

    # Context is selected during generation and carried explicitly. Never
    # infer it by scanning prompt or answer text.
    context_entry = (
        str(question.context_translation or "").strip(),
        str(question.context_kana or "").strip().rstrip(" 、。"),
        "",
    )
    if any(context_entry):
        formatted_context = format_mobile_hint_entry(context_entry)
        if formatted_context and formatted_context not in result:
            result.append(formatted_context)

    for slot, identifier in bindings:
        slot_definition = slots.get(slot)
        item = None
        dictionary_id = ""
        if getattr(slot_definition, "kind", "") == "entity":
            item = entities.get(identifier)
            dictionary_id = "entity"
        else:
            dictionary_id = str(
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
        append_item(fallback, ("verbs", question.word_id))
    return result


def quiz_policy():
    values = {key: getattr(logic, key) for key in dir(logic) if not key.startswith("__")}
    values.update(
        QUIZ_SETTINGS_CLASS=logic.VerbQuizSettings,
        QUIZ_ENGINE_CLASS=logic.VerbQuizEngine,
        QUIZ_SESSION_CLASS=VerbQuizSession,
        SETTINGS_STORE_CLASS=logic.SettingsStore,
        QUIZ_ERROR_CLASS=logic.MobileQuizError,
        MOBILE_TITLE_KEY="specialized.verbs_title",
        MOBILE_SUBTITLE='どうしのクイズ',
        MOBILE_FILTER_HINT='ending=su,ru;type=godan',
        MOBILE_HINT_ITEMS=mobile_sentence_hint_items,
        MOBILE_HELP_ID='verbs',
        MOBILE_DIRECTION_TOGGLES=(("polite_to_plain", "specialized.polite_to_plain"),
                                 ("plain_to_polite", "specialized.plain_to_polite")),
        MOBILE_EXTRA_TOGGLES=(),
        MOBILE_EXTRA_NUMBERS=(),
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
