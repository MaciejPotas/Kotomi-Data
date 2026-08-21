"""Mobile Kivy availability quiz backed by Kotomi schema 10 XML files.

The module keeps Kivy imports inside ``create_app_class``. This lets the XML
engine and settings logic be tested on a computer where Kivy is not installed.
On a phone, run this file directly with Kivy available.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
import os
from pathlib import Path
import random
import re
import sys
import threading
from typing import Dict, Iterable, List, Mapping, Optional, Sequence, Set


SCRIPT_DIR = Path(__file__).resolve().parent
REPOSITORY_SHARED_DIR = SCRIPT_DIR.parents[1] / "shared"
INSTALL_ROOT = REPOSITORY_SHARED_DIR.parent
for import_root in (INSTALL_ROOT, REPOSITORY_SHARED_DIR):
    if str(import_root) not in sys.path:
        sys.path.insert(0, str(import_root))

from quiz_core import (
    ProjectError,
    Word,
)
from quiz_engine import SharedQuizEngine, balanced_choice, normalize_answer
from mobile_ui import (
    DEFAULT_MOBILE_BUTTON_SCALE,
    FocusRequest,
    MOBILE_BUTTON_BACKGROUND,
    MOBILE_BUTTON_TEXT,
    MOBILE_CORRECT_BACKGROUND,
    MOBILE_QUIZ_LAYOUT,
    MOBILE_WRONG_BACKGROUND,
    MobileReviewInputMixin,
    fitted_compact_text_layout,
    format_grammatical_hint_entry,
    format_mobile_hint_entries,
    format_mobile_hint_entry,
    mobile_font_path,
    scaled_button_height,
    validate_mobile_button_scale,
)
from shared.app_identity import (
    app_icon_png_path,
    apply_kivy_window_icon,
    configure_windows_app_id,
)

try:
    from shared.mobile_i18n import mobile_error_text, mobile_text
except ImportError:  # Direct execution adds ``shared`` itself to sys.path.
    from mobile_i18n import mobile_error_text, mobile_text
from settings_xml import load_settings, save_settings, settings_path
from quiz_updater import (
    QuizUpdater,
    UpdateError,
    load_update_url,
)

PROJECT_ENVIRONMENT_VARIABLE = "JAPANESE_QUIZ_PROJECT"
SETTINGS_FILENAME = "availability_quiz_settings.xml"
RECENT_MAIN_VERB_WINDOW = 4
MOBILE_APP_TITLE = "Kotomi, dostępność"
MOBILE_SUBTITLE = "どうし＋めいし＋がある"
MOBILE_SETTINGS_TITLE = "Ustawienia quizu dostępności"
MOBILE_FILTER_TITLE = "Filtr głównego czasownika"
MOBILE_FILTER_HELP = (
    "Filtruj po polach, np. ending=su,ru lub "
    "type=godan;ending=ku. Przecinek łączy wartości, "
    "średnik łączy reguły."
)
MOBILE_FILTER_HINT = "ending=su,ru;type=godan"
MOBILE_WORD_DETAIL_LABEL = "Czasownik główny"
MOBILE_HELP_SECTIONS = (
    (
        "Jak działa quiz",
        "Aplikacja ładuje quiz_project.xml. Pozostałe słowniki, "
        "konteksty, wzorce i słownictwo są pobierane ze ścieżek "
        "zapisanych w tym pliku.",
    ),
    (
        "Klawiatura telefonu",
        "Pole odpowiedzi pozostaje aktywne. Przycisk Enter na "
        "klawiaturze sprawdza odpowiedź. Po użyciu przycisków "
        "Sprawdź, Zaakceptuj / pomiń lub Hint klawiatura wraca "
        "automatycznie.",
    ),
    (
        "Hint",
        "Przycisk Hint pokazuje tylko słowa użyte do zbudowania zdania, "
        "bez ujawniania gotowej odpowiedzi.",
    ),
    (
        "Ustawienia",
        "Ustawienia są zapisywane jako XML w katalogu settings aplikacji. "
        "Po ponownym uruchomieniu możesz od razu rozpocząć quiz, "
        "bez przechodzenia przez ekran ustawień.",
    ),
    (
        "Filtry",
        "Filtr dotyczy głównego czasownika. Przykłady: "
        "ending=su,ru;type=godan albo id=yomu.",
    ),
    (
        "Pliki XML",
        "Domyślna lokalizacja manifestu to "
        "quiz_data/quiz_project.xml obok skryptu. Możesz też "
        "ustawić zmienną JAPANESE_QUIZ_PROJECT.",
    ),
)

MODE_POLISH_TO_JAPANESE = "polish_to_japanese"

MODE_LABELS = {
    MODE_POLISH_TO_JAPANESE: "Napisz zdanie po japońsku",
}

PATTERN_LABELS = {
    "verb_noun_ga_aru__simple": "Sam czasownik",
    "verb_noun_ga_aru__transitive_object": "Dopełnienie",
    "verb_noun_ga_aru__destination": "Cel ruchu",
    "verb_noun_ga_aru__companion": "Towarzysz",
    "verb_noun_ga_aru__place": "Miejsce",
}
SUPPORTED_PATTERNS = tuple(PATTERN_LABELS)

FORM_GROUPS = {
    "nonpast": {
        "label": "Nieprzeszła twierdząca",
        "plain": "dictionary",
        "polite": "polite_nonpast",
    },
    "negative": {
        "label": "Nieprzeszła przecząca",
        "plain": "plain_negative",
        "polite": "polite_negative",
    },
    "past": {
        "label": "Przeszła twierdząca",
        "plain": "past_plain",
        "polite": "past_polite",
    },
    "past_negative": {
        "label": "Przeszła przecząca",
        "plain": "past_negative_plain",
        "polite": "past_negative_polite",
    },
}

FORM_STYLE_LABELS = {
    "plain": "potoczna",
    "polite": "uprzejma",
}

FILTER_FIELDS = {
    "dictionary",
    "id",
    "translation",
    "kana",
    "kanji",
    "type",
    "ending",
    "category",
    "categories",
    "feature",
    "features",
    "role",
    "roles",
}


class MobileQuizError(ValueError):
    """Raised for invalid mobile settings or an unavailable question."""


@dataclass
class AvailabilityQuizSettings:
    """Persistent settings corresponding to the availability widget."""

    mode: str = MODE_POLISH_TO_JAPANESE
    polite_output: bool = True
    plain_output: bool = True
    enabled_forms: List[str] = field(
        default_factory=lambda: list(FORM_GROUPS)
    )
    enabled_patterns: List[str] = field(
        default_factory=lambda: list(SUPPORTED_PATTERNS)
    )
    word_filter: str = ""
    question_count: int = 25
    number_of_tries: int = 1
    random_order: bool = True
    auto_advance_seconds: float = 100.0
    font_scale: float = 1.0
    mobile_button_scale: float = DEFAULT_MOBILE_BUTTON_SCALE

    @classmethod
    def from_dict(cls, values: Mapping[str, object]) -> "AvailabilityQuizSettings":
        defaults = cls()
        settings = cls(
            mode=str(values.get("mode", defaults.mode)),
            polite_output=bool(
                values.get("polite_output", defaults.polite_output)
            ),
            plain_output=bool(
                values.get("plain_output", defaults.plain_output)
            ),
            enabled_forms=[
                str(value)
                for value in values.get(
                    "enabled_forms",
                    defaults.enabled_forms,
                )
                if str(value) in FORM_GROUPS
            ],
            enabled_patterns=[
                str(value)
                for value in values.get(
                    "enabled_patterns",
                    defaults.enabled_patterns,
                )
                if str(value) in SUPPORTED_PATTERNS
            ],
            word_filter=str(
                values.get("word_filter", defaults.word_filter)
            ),
            question_count=_safe_int(
                values.get("question_count"),
                defaults.question_count,
            ),
            number_of_tries=1,
            random_order=True,
            auto_advance_seconds=_safe_float(
                values.get("auto_advance_seconds"),
                defaults.auto_advance_seconds,
            ),
            font_scale=_safe_float(
                values.get("font_scale"),
                defaults.font_scale,
            ),
            mobile_button_scale=_safe_float(
                values.get("mobile_button_scale"),
                defaults.mobile_button_scale,
            ),
        )
        settings.validate()
        return settings

    def validate(self) -> None:
        # These controls are intentionally no longer user-configurable.
        self.number_of_tries = 1
        self.random_order = True
        if self.mode != MODE_POLISH_TO_JAPANESE:
            raise MobileQuizError(f"Nieznany tryb quizu: {self.mode}")
        if not self.enabled_forms:
            raise MobileQuizError("Wybierz co najmniej jedną formę.")
        if not self.enabled_patterns:
            raise MobileQuizError("Wybierz co najmniej jeden wzorzec zdania.")
        if not self.polite_output and not self.plain_output:
            raise MobileQuizError(
                "Wybierz co najmniej jeden styl japońskiej odpowiedzi."
            )
        if not 1 <= self.question_count <= 200:
            raise MobileQuizError(
                "Liczba pytań musi mieścić się w zakresie 1–200."
            )
        if not 0.0 <= self.auto_advance_seconds <= 600.0:
            raise MobileQuizError(
                "Automatyczne przejście musi mieścić się w zakresie 0–600 s."
            )
        if not 0.7 <= self.font_scale <= 3.0:
            raise MobileQuizError(
                "Rozmiar tekstu musi mieścić się w zakresie 70–300%."
            )
        try:
            validate_mobile_button_scale(self.mobile_button_scale)
        except (TypeError, ValueError) as exception:
            raise MobileQuizError(str(exception)) from exception
        parse_word_filter(self.word_filter)

    def summary(self) -> str:
        forms = ", ".join(
            FORM_GROUPS[name]["label"] for name in self.enabled_forms
        )
        patterns = ", ".join(
            PATTERN_LABELS[name] for name in self.enabled_patterns
        )
        return (
            f"{MODE_LABELS[self.mode]}\n"
            f"Pytania: {self.question_count}\n"
            f"Formy: {forms}\n"
            f"Wzorce: {patterns}\n"
            f"Rozmiar tekstu: {round(self.font_scale * 100)}%\n"
            f"Rozmiar przycisków: "
            f"{round(self.mobile_button_scale * 100)}%"
        )


@dataclass(frozen=True)
class WordFilterRule:
    field: str
    values: tuple[str, ...]


@dataclass(frozen=True)
class GenerationRule:
    category: str
    source_form: str
    target_form: str
    target_label: str


@dataclass(frozen=True)
class GenerationCombination:
    pattern_id: str
    rule: GenerationRule


@dataclass
class AvailabilityQuestion:
    key: str
    source_sentence: str
    expected_answer: str
    target_label: str
    context_question: str
    pattern_id: str
    target_form: str
    source_form: str
    word_id: str
    word_meaning: str
    word_kana: str
    word_kanji: str
    hint_pairs: List[tuple[str, str]]
    bindings: str
    context_translation: str = ""
    context_kana: str = ""


@dataclass
class SubmissionResult:
    state: str
    message: str
    expected_answer: str = ""


def _safe_int(value: object, default: int) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _safe_float(value: object, default: float) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def normalize_japanese(text: str) -> str:
    """Normalize harmless punctuation and spacing for answer comparison."""
    return normalize_answer(text)


def selected_context_hint(
    project: object,
    preview: object,
) -> tuple[str, str]:
    """Return Hint metadata for the exact context selected by generation."""
    pool = getattr(project, "contexts", {}).get(
        getattr(preview, "context_pool", "")
    )
    option = (
        getattr(pool, "options", {}).get(
            getattr(preview, "context_option", "")
        )
        if pool is not None
        else None
    )
    if option is None:
        return "", ""
    return (
        str(getattr(option, "translation", "") or "").strip(),
        str(getattr(option, "kana", "") or "").strip(),
    )


def mobile_sentence_hint_entries(
    question: object,
    project: object,
) -> List[str]:
    """Resolve selected base words for a mobile Hint, never the answer."""
    entries: List[str] = []
    seen: set[tuple[str, str]] = set()
    context_entry = (
        str(getattr(question, "context_translation", "") or "").strip(),
        str(getattr(question, "context_kana", "") or "")
        .strip()
        .rstrip(" 、。"),
        "",
    )
    if any(context_entry):
        formatted = format_mobile_hint_entry(context_entry)
        if formatted:
            entries.append(formatted)
        seen.add(("context", "\0".join(context_entry)))
    slots = {}
    try:
        slots = project.analyze_pattern(question.pattern_id).slots
    except (AttributeError, KeyError, ValueError, ProjectError):
        slots = {}

    binding_entries_found = False
    for binding in re.split(
        r"[,;]", str(getattr(question, "bindings", "") or "")
    ):
        slot, separator, identifiers = binding.strip().partition("=")
        if not separator:
            continue
        definition = slots.get(slot.strip())
        for identifier in identifiers.split("+"):
            identifier = identifier.strip()
            if not identifier:
                continue
            if getattr(definition, "kind", "") == "entity":
                key = ("entity", identifier)
                item = getattr(project, "entities", {}).get(identifier)
            else:
                dictionary_id = str(
                    getattr(definition, "dictionary", "") or ""
                )
                key = (dictionary_id, identifier)
                item = getattr(project, "words", {}).get(
                    dictionary_id, {}
                ).get(identifier)
            if item is not None and key not in seen:
                seen.add(key)
                formatted = format_grammatical_hint_entry(item)
                if formatted:
                    entries.append(formatted)
                binding_entries_found = True

    if binding_entries_found:
        return entries

    # Compatibility fallback for old serialized cards without bindings.
    candidates = [
        *(
            item
            for dictionary in getattr(project, "words", {}).values()
            for item in dictionary.values()
        ),
        *getattr(project, "entities", {}).values(),
    ]
    for translation, kana in getattr(question, "hint_pairs", ()):
        matching = next(
            (
                item
                for item in candidates
                if str(getattr(item, "translation", "") or "").strip()
                == str(translation or "").strip()
                and str(getattr(item, "kana", "") or "").strip()
                == str(kana or "").strip()
            ),
            None,
        )
        if matching is not None:
            formatted = format_grammatical_hint_entry(matching)
        else:
            formatted = format_grammatical_hint_entry(
                (translation, kana, ""), kind="word"
            )
        if formatted:
            entries.append(formatted)
    return entries


def _apply_absolute_font_scale(widget: object, scale: float) -> None:
    base_font_size = getattr(widget, "_quiz_base_font_size", None)
    if base_font_size is not None:
        resized = float(base_font_size) * float(scale)
        maximum = getattr(widget, "_mobile_max_font_size", None)
        widget.font_size = (
            min(resized, float(maximum))
            if maximum is not None
            else resized
        )
    for child in getattr(widget, "children", []):
        _apply_absolute_font_scale(child, scale)


def _apply_absolute_button_scale(widget: object, scale: float) -> None:
    base_height = getattr(widget, "_quiz_base_button_height", None)
    if base_height is not None:
        widget.height = scaled_button_height(base_height, scale)
    base_row_height = getattr(widget, "_quiz_base_action_height", None)
    if base_row_height is not None:
        widget.height = scaled_button_height(base_row_height, scale)
    for child in getattr(widget, "children", []):
        _apply_absolute_button_scale(child, scale)


def parse_word_filter(text: str) -> List[WordFilterRule]:
    """Parse the C++ widget's field=value;field=value filter syntax."""
    rules: List[WordFilterRule] = []
    for expression in (text or "").split(";"):
        expression = expression.strip()
        if not expression:
            continue
        if "=" not in expression:
            raise MobileQuizError(
                f"Nieprawidłowy filtr „{expression}”. Użyj pole=wartość."
            )
        field_name, values_text = (
            value.strip() for value in expression.split("=", 1)
        )
        field_name = field_name.casefold()
        values = tuple(
            value.strip().casefold()
            for value in values_text.split(",")
            if value.strip()
        )
        if field_name not in FILTER_FIELDS:
            raise MobileQuizError(
                f"Nieznane pole filtra „{field_name}”."
            )
        if not values:
            raise MobileQuizError(
                f"Filtr „{field_name}” nie zawiera wartości."
            )
        rules.append(WordFilterRule(field_name, values))
    return rules


def word_matches_filter(
    word: Word,
    rules: Iterable[WordFilterRule],
) -> bool:
    for rule in rules:
        if rule.field in {"category", "categories"}:
            values = {value.casefold() for value in word.categories}
            if not values.intersection(rule.values):
                return False
            continue
        if rule.field in {"feature", "features"}:
            if not {value.casefold() for value in word.features}.intersection(rule.values):
                return False
            continue
        if rule.field in {"role", "roles"}:
            if not {value.casefold() for value in word.usage}.intersection(rule.values):
                return False
            continue
        field_name = (
            "dictionary_id"
            if rule.field == "dictionary"
            else rule.field
        )
        value = str(getattr(word, field_name, "") or "").casefold()
        if value not in rule.values:
            return False
    return True


def resolve_project_path() -> Path:
    """Find the manifest without hardcoding any referenced XML filename."""
    environment_path = os.environ.get(PROJECT_ENVIRONMENT_VARIABLE, "").strip()
    candidates = [
        Path(environment_path).expanduser() if environment_path else None,
        SCRIPT_DIR / "quiz_data" / "quiz_project.xml",
        REPOSITORY_SHARED_DIR / "quiz_data" / "quiz_project.xml",
        SCRIPT_DIR / "quiz_project.xml",
        SCRIPT_DIR / "examples" / "quiz_project.xml",
    ]
    for candidate in candidates:
        if candidate is not None and candidate.exists():
            return candidate.resolve()
    searched = "\n".join(
        str(candidate) for candidate in candidates if candidate is not None
    )
    raise MobileQuizError(
        "Nie znaleziono quiz_project.xml. Sprawdzone lokalizacje:\n"
        + searched
    )


class SettingsStore:
    def __init__(self, path: Path) -> None:
        self.path = path

    def load(self) -> AvailabilityQuizSettings:
        if not self.path.exists():
            return AvailabilityQuizSettings()
        try:
            return AvailabilityQuizSettings.from_dict(load_settings(self.path))
        except (OSError, ValueError):
            return AvailabilityQuizSettings()

    def save(self, settings: AvailabilityQuizSettings) -> None:
        settings.validate()
        save_settings(self.path, asdict(settings))


class AvailabilityQuizEngine:
    """Mobile policy for ``verb + availability noun + が + ある``."""

    def __init__(
        self,
        project_path: Path | str,
        rng: Optional[random.Random] = None,
    ) -> None:
        self.project_path = Path(project_path).resolve()
        self.rng = rng or random.Random()
        self.shared_engine = SharedQuizEngine(self.project_path, self.rng)
        self.project = self.shared_engine.project
        issues = self.project.validate()
        if issues:
            raise MobileQuizError("\n".join(issues))

    def reload(self) -> None:
        self.shared_engine.reload()
        self.project = self.shared_engine.project
        issues = self.project.validate()
        if issues:
            raise MobileQuizError("\n".join(issues))

    def build_generation_rules(
        self,
        settings: AvailabilityQuizSettings,
    ) -> List[GenerationRule]:
        settings.validate()
        rules: List[GenerationRule] = []
        for category in settings.enabled_forms:
            form_group = FORM_GROUPS[category]
            category_label = str(form_group["label"]).lower()
            for style_name, enabled in (
                ("plain", settings.plain_output),
                ("polite", settings.polite_output),
            ):
                if enabled:
                    rules.append(
                        GenerationRule(
                            category=category,
                            source_form="",
                            target_form=str(form_group[style_name]),
                            target_label=(
                                f"{category_label}, styl "
                                f"{FORM_STYLE_LABELS[style_name]}"
                            ),
                        )
                    )
        return rules

    def build_combinations(
        self,
        settings: AvailabilityQuizSettings,
    ) -> List[GenerationCombination]:
        rules = self.build_generation_rules(settings)
        combinations: List[GenerationCombination] = []
        for pattern_id in settings.enabled_patterns:
            pattern = self.project.patterns.get(pattern_id)
            if pattern is None:
                continue
            try:
                analysis = self.shared_engine.analyze_pattern(pattern)
                if pattern.composite_id != "verb_noun_ga_aru":
                    continue
                if (
                    "aru" not in analysis.fixed_words.values()
                    or not analysis.focus_slot
                    or analysis.slots[analysis.focus_slot].dictionary != "verbs"
                ):
                    continue
            except ProjectError:
                continue
            combinations.extend(
                GenerationCombination(pattern_id, rule) for rule in rules
            )
        if not combinations:
            raise MobileQuizError(
                "Bieżące ustawienia nie tworzą żadnej reguły quizu."
            )
        return combinations

    def generate_question(
        self,
        settings: AvailabilityQuizSettings,
        seen_keys: Optional[Set[str]] = None,
        preferred: Optional[GenerationCombination] = None,
        word_usage: Optional[Mapping[str, int]] = None,
        recent_word_ids: Optional[Sequence[str]] = None,
    ) -> AvailabilityQuestion:
        rules = parse_word_filter(settings.word_filter)
        combinations = self.build_combinations(settings)
        if preferred is not None:
            combinations = [
                preferred,
                *[
                    combination
                    for combination in combinations
                    if combination != preferred
                ],
            ]
        if settings.random_order:
            first = combinations[:1] if preferred is not None else []
            remaining = combinations[len(first):]
            self.rng.shuffle(remaining)
            combinations = first + remaining

        seen_keys = seen_keys or set()
        for _attempt in range(96):
            combination = (
                combinations[0]
                if preferred is not None and _attempt == 0
                else self.rng.choice(combinations)
            )
            question = self._question_for_combination(
                combination,
                settings,
                rules,
                word_usage=word_usage,
                recent_word_ids=recent_word_ids,
            )
            if question is not None and question.key not in seen_keys:
                return question
        raise MobileQuizError(
            "Nie udało się znaleźć kolejnego unikalnego pytania dla "
            "bieżących ustawień i filtra."
        )

    def _question_for_combination(
        self,
        combination: GenerationCombination,
        settings: AvailabilityQuizSettings,
        filter_rules: Sequence[WordFilterRule],
        word_usage: Optional[Mapping[str, int]] = None,
        recent_word_ids: Optional[Sequence[str]] = None,
    ) -> Optional[AvailabilityQuestion]:
        analysis = self.shared_engine.analyze_pattern(combination.pattern_id)
        try:
            compatible = self.shared_engine.compatible(
                combination.pattern_id,
                form_name=combination.rule.target_form,
            )
        except ProjectError:
            return None
        candidates = [
            word
            for word in compatible.words.get(analysis.focus_slot, [])
            if word.dictionary_id == "verbs"
            and word_matches_filter(word, filter_rules)
        ]
        if not candidates:
            return None

        selected_word = balanced_choice(
            candidates,
            word_usage or {},
            recent_word_ids or (),
            self.rng,
        )
        try:
            completed = self.shared_engine.complete(
                combination.pattern_id,
                form_name=combination.rule.target_form,
                word_choices={analysis.focus_slot: selected_word.id},
                rng=self.rng,
            )
            preview = self.shared_engine.preview(
                combination.pattern_id,
                form_name=completed.form_name,
                word_choices=completed.words,
                entity_choices=completed.entities,
                rng=self.rng,
            )
        except ProjectError:
            return None

        source_sentence = preview.source
        context_question = ""

        binding_parts = [
            *(
                f"{slot_id}={word_id}"
                for slot_id, word_id in preview.words.items()
            ),
            *(
                f"{slot_id}={entity_id}"
                for slot_id, entity_id in preview.entities.items()
            ),
        ]
        context_translation, context_kana = selected_context_hint(
            self.project,
            preview,
        )
        key = "|".join(
            (
                combination.pattern_id,
                combination.rule.source_form,
                combination.rule.target_form,
                source_sentence,
                preview.answer,
            )
        )
        return AvailabilityQuestion(
            key=key,
            source_sentence=source_sentence,
            expected_answer=preview.answer,
            target_label=combination.rule.target_label,
            context_question=context_question,
            pattern_id=combination.pattern_id,
            target_form=combination.rule.target_form,
            source_form=combination.rule.source_form,
            word_id=selected_word.id,
            word_meaning=selected_word.translation,
            word_kana=selected_word.kana,
            word_kanji=selected_word.kanji,
            hint_pairs=self._build_hint_pairs(preview),
            bindings=", ".join(binding_parts),
            context_translation=context_translation,
            context_kana=context_kana,
        )

    def _build_hint_pairs(self, preview: object) -> List[tuple[str, str]]:
        """Return every selected base word without exposing the answer form."""
        analysis = self.shared_engine.analyze_pattern(preview.pattern_id)
        result: List[tuple[str, str]] = []
        for slot in analysis.word_slots:
            dictionary_id = analysis.slots[slot].dictionary
            word = self.project.words[dictionary_id][preview.words[slot]]
            result.append((word.translation, word.kana))
        for slot in analysis.entity_slots:
            entity = self.project.entities[preview.entities[slot]]
            result.append((entity.translation, entity.kana))
        return result

    def statistics(self, settings: AvailabilityQuizSettings) -> Dict[str, int]:
        """Calculate exact statistics. The GUI calls this on a worker thread."""
        filter_rules = parse_word_filter(settings.word_filter)
        combinations = self.build_combinations(settings)
        possible = 0
        enabled_patterns: Set[str] = set()
        for combination in combinations:
            enabled_patterns.add(combination.pattern_id)
            for preview in self.shared_engine.iter_previews(
                combination.pattern_id,
                form_name=combination.rule.target_form,
            ):
                analysis = self.shared_engine.analyze_pattern(
                    combination.pattern_id
                )
                word = self.project.words["verbs"][
                    preview.words[analysis.focus_slot]
                ]
                if word_matches_filter(word, filter_rules):
                    possible += 1
        return {
            "words": sum(
                len(dictionary)
                for dictionary in self.project.words.values()
            ),
            "patterns": len(enabled_patterns),
            "entities": len(self.project.entities),
            "categories": len(self.project.noun_categories),
            "possible": possible,
        }


class AvailabilityQuizSession:
    """Quiz progress and retry behavior, independent from Kivy."""

    def __init__(
        self,
        engine: AvailabilityQuizEngine,
        settings: AvailabilityQuizSettings,
    ) -> None:
        settings.validate()
        self.engine = engine
        self.settings = settings
        self.combinations = engine.build_combinations(settings)
        if settings.random_order:
            engine.rng.shuffle(self.combinations)
        self.seen_keys: Set[str] = set()
        self.word_usage: Dict[str, int] = {}
        self.recent_word_ids: List[str] = []
        self.current_question: Optional[AvailabilityQuestion] = None
        self.current_index = -1
        self.current_try = 0
        self.correct_answers = 0
        self.wrong_answers = 0
        self.accepted_answers = 0
        self.waiting_for_next = False
        self.current_outcome = ""

    @property
    def complete(self) -> bool:
        return self.current_index >= self.settings.question_count

    def next_question(self) -> Optional[AvailabilityQuestion]:
        next_index = self.current_index + 1
        if next_index >= self.settings.question_count:
            self.current_index = self.settings.question_count
            self.current_question = None
            self.waiting_for_next = False
            return None
        preferred = self.combinations[
            next_index % len(self.combinations)
        ]
        question = self.engine.generate_question(
            self.settings,
            seen_keys=self.seen_keys,
            preferred=preferred,
            word_usage=self.word_usage,
            recent_word_ids=self.recent_word_ids,
        )
        self.seen_keys.add(question.key)
        self.word_usage[question.word_id] = (
            self.word_usage.get(question.word_id, 0) + 1
        )
        self.recent_word_ids.append(question.word_id)
        if len(self.recent_word_ids) > RECENT_MAIN_VERB_WINDOW:
            self.recent_word_ids = self.recent_word_ids[-RECENT_MAIN_VERB_WINDOW:]
        self.current_question = question
        self.current_index = next_index
        self.current_try = 0
        self.waiting_for_next = False
        self.current_outcome = ""
        return question

    def submit(self, answer: str) -> SubmissionResult:
        if self.current_question is None or self.waiting_for_next:
            return SubmissionResult("ignored", "")
        expected = self.current_question.expected_answer
        if normalize_japanese(answer) == normalize_japanese(expected):
            self.correct_answers += 1
            self.waiting_for_next = True
            self.current_outcome = "correct"
            return SubmissionResult(
                "correct",
                "Dobrze!",
                expected,
            )
        self.current_try += 1
        if self.current_try >= self.settings.number_of_tries:
            self.wrong_answers += 1
            self.waiting_for_next = True
            self.current_outcome = "wrong"
            return SubmissionResult(
                "wrong",
                "Niepoprawnie. Poniżej jest oczekiwana odpowiedź.",
                expected,
            )
        return SubmissionResult(
            "retry",
            (
                "Jeszcze nie. Spróbuj ponownie "
                f"({self.current_try}/{self.settings.number_of_tries})."
            ),
        )

    def accept_or_skip(self) -> None:
        if self.current_question is None:
            return
        if not self.waiting_for_next:
            self.correct_answers += 1
            self.accepted_answers += 1
            self.current_outcome = "accepted"
        elif self.current_outcome == "wrong":
            if self.wrong_answers > 0:
                self.wrong_answers -= 1
            self.correct_answers += 1
            self.accepted_answers += 1
            self.current_outcome = "accepted"
        self.waiting_for_next = True


def create_app_class(policy: object = None):
    """Import Kivy lazily and return a policy-backed mobile quiz class."""
    configure_windows_app_id()
    policy = policy or sys.modules[__name__]
    policy_settings = getattr(policy, "QUIZ_SETTINGS_CLASS", AvailabilityQuizSettings)
    policy_engine = getattr(policy, "QUIZ_ENGINE_CLASS", AvailabilityQuizEngine)
    policy_session = getattr(policy, "QUIZ_SESSION_CLASS", AvailabilityQuizSession)
    policy_store = getattr(policy, "SETTINGS_STORE_CLASS", SettingsStore)
    policy_error = getattr(policy, "QUIZ_ERROR_CLASS", MobileQuizError)
    policy_mode = getattr(policy, "MODE_POLISH_TO_JAPANESE")
    mode_labels = getattr(policy, "MODE_LABELS")
    form_groups = getattr(policy, "FORM_GROUPS")
    pattern_labels = getattr(policy, "PATTERN_LABELS")
    install_root = getattr(policy, "INSTALL_ROOT")
    settings_filename = getattr(policy, "SETTINGS_FILENAME")
    policy_settings_path = getattr(
        policy,
        "quiz_settings_path",
        lambda: settings_path(install_root, settings_filename),
    )
    resolve_policy_project = getattr(policy, "resolve_project_path")
    mobile_title = getattr(policy, "MOBILE_APP_TITLE", "Kotomi")
    mobile_subtitle = getattr(policy, "MOBILE_SUBTITLE", "")
    mobile_filter_hint = getattr(policy, "MOBILE_FILTER_HINT", "")
    is_default_availability = policy is sys.modules[__name__]
    mobile_title_key = (
        "specialized.availability_title"
        if is_default_availability
        else "specialized.grammar_title"
    )
    from kivy.app import App
    from kivy.clock import Clock
    from kivy.core.text import Label as CoreLabel
    from kivy.core.window import Window
    from kivy.metrics import dp, sp
    from kivy.uix.anchorlayout import AnchorLayout
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.button import Button
    from kivy.uix.checkbox import CheckBox
    from kivy.uix.label import Label
    from kivy.uix.progressbar import ProgressBar
    from kivy.uix.screenmanager import (
        Screen,
        ScreenManager,
        SlideTransition,
    )
    from kivy.uix.scrollview import ScrollView
    from kivy.uix.slider import Slider
    from kivy.uix.spinner import Spinner
    from kivy.uix.textinput import TextInput
    from kivy.uix.widget import Widget
    from kivy.utils import escape_markup

    def quiz_app():
        """Return the quiz controller in standalone or master mode."""
        running_app = App.get_running_app()
        controller = getattr(running_app, "active_quiz_controller", None)
        return controller or running_app

    def tr(key: str, **values: object) -> str:
        """Translate mobile chrome using the launcher-selected language."""
        return mobile_text(quiz_app(), key, **values)

    def mode_label(_mode: str) -> str:
        return tr("specialized.mode.write_japanese")

    def target_label(question: object) -> str:
        target_form = str(getattr(question, "target_form", ""))
        for group_id, group in form_groups.items():
            for style_id in ("plain", "polite"):
                if target_form == str(group[style_id]):
                    return (
                        f"{tr(f'specialized.form_group.{group_id}')}, "
                        f"{tr(f'specialized.{style_id}')}"
                    )
        return str(getattr(question, "target_label", ""))

    def settings_summary(settings: object) -> str:
        forms = ", ".join(
            tr(f"specialized.form_group.{name}")
            for name in settings.enabled_forms
        )
        patterns = ", ".join(
            tr(f"specialized.pattern.{name}")
            for name in settings.enabled_patterns
        )
        return "\n".join(
            (
                mode_label(settings.mode),
                f"{tr('specialized.question_count')}: {settings.question_count}",
                f"{tr('specialized.tab.forms')}: {forms}",
                f"{tr('specialized.tab.patterns')}: {patterns}",
                f"{tr('specialized.text_scale')}: {round(settings.font_scale * 100)}%; "
                f"{tr('specialized.button_scale')}: "
                f"{round(settings.mobile_button_scale * 100)}%",
            )
        )

    def return_to_quiz_menu() -> bool:
        """Return an embedded quiz to Kotomi's main quiz selector."""
        controller = quiz_app()
        host_callback = getattr(controller, "host_quiz_menu_callback", None)
        if callable(host_callback):
            host_callback()
            return True
        running_app = App.get_running_app()
        fallback = getattr(running_app, "return_to_launcher", None)
        if callable(fallback) and getattr(controller, "embedded_mode", False):
            fallback()
            return True
        return False

    def leave_quiz() -> None:
        """Return to the host selector, or stop only in standalone mode."""
        if not return_to_quiz_menu():
            quiz_app().stop()

    Window.clearcolor = (1, 1, 1, 1)
    try:
        Window.softinput_mode = "resize"
    except Exception:
        pass

    label_color = (0.12, 0.12, 0.12, 1)
    button_background = (0.92, 0.92, 0.92, 1)
    button_text = (0.0, 0.0, 0.0, 1)
    accent_ok = (0.10, 0.45, 0.15, 1)
    accent_bad = (0.65, 0.10, 0.10, 1)
    accent_info = (0.15, 0.20, 0.55, 1)
    input_active_background = (1.0, 1.0, 1.0, 1.0)
    input_correct_background = (0.84, 0.96, 0.87, 1.0)
    input_wrong_background = (1.0, 0.86, 0.86, 1.0)
    hint_active_background = (0.76, 0.88, 0.97, 1.0)
    font_scale_state = {"value": 1.0}
    button_scale_state = {"value": DEFAULT_MOBILE_BUTTON_SCALE}
    mixed_font = mobile_font_path(REPOSITORY_SHARED_DIR)

    def polish_font() -> str:
        return mixed_font

    def japanese_font() -> str:
        return mixed_font

    def current_font_scale() -> float:
        return float(font_scale_state["value"])

    def scaled_font_size(value: float) -> float:
        return float(value) * current_font_scale()

    def current_button_scale() -> float:
        return float(button_scale_state["value"])

    def prepare_font_size(kwargs: Dict[str, object]) -> Optional[float]:
        if "font_size" not in kwargs:
            return None
        base_font_size = float(kwargs["font_size"])
        kwargs["font_size"] = scaled_font_size(base_font_size)
        return base_font_size

    def remember_base_font_size(widget, base_font_size: Optional[float]) -> None:
        if base_font_size is not None:
            widget._quiz_base_font_size = base_font_size

    def prepare_button_height(kwargs: Dict[str, object]) -> Optional[float]:
        if kwargs.get("size_hint_y", 1) is not None or "height" not in kwargs:
            return None
        base_height = dp(float(kwargs["height"]))
        kwargs["height"] = scaled_button_height(
            base_height,
            current_button_scale(),
        )
        return base_height

    def remember_base_button_height(widget, base_height: Optional[float]) -> None:
        if base_height is not None:
            widget._quiz_base_button_height = base_height

    def action_row(base_height: float, **kwargs) -> BoxLayout:
        density_height = dp(base_height)
        row = BoxLayout(
            size_hint_y=None,
            height=scaled_button_height(
                density_height,
                current_button_scale(),
            ),
            **kwargs,
        )
        row._quiz_base_action_height = density_height
        return row

    class PolishLabel(Label):
        def __init__(self, **kwargs):
            kwargs.setdefault("font_name", polish_font())
            kwargs.setdefault("color", label_color)
            base_font_size = prepare_font_size(kwargs)
            super().__init__(**kwargs)
            remember_base_font_size(self, base_font_size)

    class JapaneseLabel(Label):
        def __init__(self, **kwargs):
            kwargs.setdefault("font_name", japanese_font())
            kwargs.setdefault("color", label_color)
            base_font_size = prepare_font_size(kwargs)
            super().__init__(**kwargs)
            remember_base_font_size(self, base_font_size)

    class AdaptiveSingleLineLabel(Label):
        """Fit complete mixed-language text inside a fixed single-line slot."""

        def __init__(self, **kwargs):
            self._base_preferred_font_sp = float(
                kwargs.pop("preferred_font_sp", 18.0)
            )
            self._base_minimum_font_sp = float(
                kwargs.pop("minimum_font_sp", 10.0)
            )
            self._maximum_fit_lines = max(
                1, int(kwargs.pop("maximum_fit_lines", 1))
            )
            self._fit_plain_text = str(
                kwargs.pop("fit_plain_text", kwargs.get("text", ""))
            )
            self._font_fit_running = False
            kwargs.setdefault("font_name", japanese_font())
            kwargs.setdefault("color", label_color)
            kwargs.setdefault("halign", "left")
            kwargs.setdefault("valign", "middle")
            # A shortened sentence can hide the part the learner must
            # translate.  Mobile quiz rows always keep the complete text and
            # reduce the font instead of rendering an ellipsis.
            kwargs["shorten"] = False
            kwargs["font_size"] = sp(
                scaled_font_size(self._base_preferred_font_sp)
            )
            super().__init__(**kwargs)
            if hasattr(self, "max_lines"):
                self.max_lines = 1
            self._quiz_base_font_size = sp(self._base_preferred_font_sp)
            self.bind(width=self._fit_font_to_width, text=self._fit_font_to_width)
            Clock.schedule_once(self._fit_font_to_width, 0)

        def set_fitted_text(self, markup_text: str, plain_text: str) -> None:
            normalized_markup = markup_text.replace("\r", " ").replace("\n", " ")
            normalized_plain = plain_text.replace("\r", " ").replace("\n", " ")
            # Clear the previous texture before changing a long prompt.  On
            # Android this prevents a wrapped tail from surviving underneath
            # the following question for one render cycle.
            self.text = ""
            self._fit_plain_text = normalized_plain
            self.text = normalized_markup
            self.shorten = False
            if hasattr(self, "max_lines"):
                self.max_lines = 1
            self._fit_font_to_width()

        def _fit_font_to_width(self, *_args) -> None:
            if self._font_fit_running:
                return
            available_width = max(0.0, self.width - dp(4))
            if available_width <= 0:
                return
            height_sp = self.height / max(sp(1.0), 0.01)
            preferred_sp = min(
                scaled_font_size(self._base_preferred_font_sp),
                height_sp * 0.80,
            )
            # Font scaling expresses preference, not permission to crop a
            # fixed mobile row. Keep the readability floor independent from
            # the user scale and constrain the final size by line height.
            minimum_sp = min(self._base_minimum_font_sp, preferred_sp)
            self._font_fit_running = True
            try:
                probe = CoreLabel(
                    text=self._fit_plain_text,
                    font_name=self.font_name,
                    font_size=sp(preferred_sp),
                )
                probe.refresh()
                fitted_lines, fitted_sp = fitted_compact_text_layout(
                    float(probe.texture.size[0]),
                    available_width,
                    preferred_sp=preferred_sp,
                    minimum_sp=minimum_sp,
                    maximum_lines=self._maximum_fit_lines,
                )
                fitted_sp = min(
                    fitted_sp,
                    height_sp * 0.80 / max(1, fitted_lines),
                )
                self.shorten = False
                if hasattr(self, "max_lines"):
                    self.max_lines = 1
                self.font_size = sp(fitted_sp)
                self.text_size = (available_width, max(0.0, self.height))
            finally:
                self._font_fit_running = False

    class PolishButton(Button):
        def __init__(self, **kwargs):
            kwargs.setdefault("font_name", polish_font())
            kwargs.setdefault("background_normal", "")
            kwargs.setdefault("background_color", button_background)
            kwargs.setdefault("color", button_text)
            base_font_size = prepare_font_size(kwargs)
            base_button_height = prepare_button_height(kwargs)
            super().__init__(**kwargs)
            remember_base_font_size(self, base_font_size)
            remember_base_button_height(self, base_button_height)

    class PolishInput(TextInput):
        def __init__(self, **kwargs):
            kwargs.setdefault("font_name", polish_font())
            base_font_size = prepare_font_size(kwargs)
            super().__init__(**kwargs)
            remember_base_font_size(self, base_font_size)

    class MobileSettingToggle(PolishButton):
        """Full-width settings toggle matching the verb/adjective mobile UI."""

        def __init__(self, setting_text: str, active: bool = True, **kwargs):
            self.setting_text = setting_text
            self._active = bool(active)
            self._setting_callback = kwargs.pop("setting_callback", None)
            kwargs.setdefault("size_hint_y", None)
            kwargs.setdefault("height", 64)
            kwargs.setdefault("font_size", 19)
            kwargs.setdefault("halign", "left")
            kwargs.setdefault("valign", "middle")
            super().__init__(**kwargs)
            self.bind(
                size=lambda instance, _value: setattr(
                    instance, "text_size", instance.size
                ),
                on_release=lambda *_: self.toggle(),
            )
            self._refresh_state()

        @property
        def active(self) -> bool:
            return self._active

        @active.setter
        def active(self, value: bool) -> None:
            self._active = bool(value)
            self._refresh_state()

        def toggle(self) -> None:
            self.active = not self.active
            if callable(self._setting_callback):
                self._setting_callback(self.active)

        def _refresh_state(self) -> None:
            self.text = (
                f"✓  {self.setting_text}"
                if self._active
                else f"     {self.setting_text}"
            )
            self.background_color = (
                hint_active_background if self._active else button_background
            )

    class PolishSpinner(Spinner):
        def __init__(self, **kwargs):
            kwargs.setdefault("font_name", polish_font())
            kwargs.setdefault("option_cls", PolishButton)
            base_font_size = prepare_font_size(kwargs)
            super().__init__(**kwargs)
            remember_base_font_size(self, base_font_size)

    class JapaneseInput(MobileReviewInputMixin, TextInput):
        def __init__(self, **kwargs):
            kwargs.setdefault("font_name", japanese_font())
            kwargs.setdefault("background_color", (1, 1, 1, 1))
            kwargs.setdefault("foreground_color", (0, 0, 0, 1))
            kwargs.setdefault("multiline", False)
            kwargs.setdefault("unfocus_on_touch", False)
            kwargs.setdefault("text_validate_unfocus", False)
            kwargs.setdefault("write_tab", False)
            base_font_size = prepare_font_size(kwargs)
            super().__init__(**kwargs)
            remember_base_font_size(self, base_font_size)

    def wrap_label(label: Label) -> None:
        label.bind(size=lambda instance, _value: setattr(
            instance,
            "text_size",
            instance.size,
        ))

    def setting_row(
        text: str,
        active: bool,
        callback,
    ) -> tuple[BoxLayout, MobileSettingToggle]:
        row = BoxLayout(
            size_hint_y=None,
            height=scaled_button_height(dp(64), current_button_scale()),
        )
        row._quiz_base_action_height = dp(64)
        toggle = MobileSettingToggle(
            setting_text=text,
            active=active,
            setting_callback=callback,
        )
        row.add_widget(toggle)
        return row, toggle

    class HomeScreen(Screen):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            embedded_mode = bool(
                getattr(quiz_app(), "embedded_mode", False)
            )
            root = BoxLayout(
                orientation="vertical",
                padding=24,
                spacing=14,
            )
            root.add_widget(
                PolishLabel(
                    text="Kotomi",
                    font_size=34,
                    size_hint_y=None,
                    height=54,
                )
            )
            root.add_widget(
                JapaneseLabel(
                    text=mobile_subtitle,
                    font_size=28,
                    size_hint_y=None,
                    height=46,
                )
            )
            self.summary = PolishLabel(
                text="",
                font_size=19,
                halign="left",
                valign="middle",
                size_hint_y=None,
                height=150,
            )
            wrap_label(self.summary)
            root.add_widget(self.summary)

            self.start_button = PolishButton(
                text=tr("specialized.start_quiz"),
                font_size=24,
                size_hint_y=None,
                height=76,
            )
            self.start_button.bind(
                on_release=lambda *_: quiz_app().start_quiz()
            )
            root.add_widget(self.start_button)
            settings_button = PolishButton(
                text=tr("action.settings"),
                font_size=22,
                size_hint_y=None,
                height=70,
            )
            settings_button.bind(
                on_release=lambda *_: quiz_app().open_settings()
            )
            root.add_widget(settings_button)
            help_button = PolishButton(
                text=tr("specialized.help"),
                font_size=22,
                size_hint_y=None,
                height=70,
            )
            help_button.bind(
                on_release=lambda *_: quiz_app().open_help()
            )
            root.add_widget(help_button)
            exit_button = PolishButton(
                text=(
                    tr("specialized.launcher_menu")
                    if embedded_mode
                    else tr("specialized.exit")
                ),
                font_size=22,
                size_hint_y=None,
                height=70,
            )
            exit_button.bind(
                on_release=lambda *_: leave_quiz()
            )
            root.add_widget(exit_button)
            root.add_widget(Widget())
            self.add_widget(root)

        def on_pre_enter(self, *_args):
            app = quiz_app()
            self.summary.text = app.home_summary()
            self.start_button.disabled = app.restart_required

        def show_update_state(self) -> None:
            app = quiz_app()
            self.summary.text = app.home_summary()
            self.start_button.disabled = app.restart_required

    class SettingsScreen(Screen):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.form_checks: Dict[str, MobileSettingToggle] = {}
            self.pattern_checks: Dict[str, MobileSettingToggle] = {}
            self.value_checks: Dict[str, MobileSettingToggle] = {}

            root = BoxLayout(
                orientation="vertical",
                padding=dp(8),
                spacing=dp(8),
            )
            scroll = ScrollView(
                do_scroll_x=False,
                do_scroll_y=True,
                bar_width=dp(12),
                scroll_type=["content", "bars"],
            )
            self.content = BoxLayout(
                orientation="vertical",
                padding=dp(4),
                spacing=dp(8),
                size_hint_y=None,
            )
            self.content.bind(
                minimum_height=self.content.setter("height")
            )
            self.content.add_widget(
                PolishLabel(
                    text=(
                        f"{tr(mobile_title_key)} "
                        f"{tr('specialized.settings_suffix')}"
                    ),
                    font_size=24,
                    size_hint_y=None,
                    height=48,
                )
            )
            self._section(tr("specialized.question_type"))
            self.mode_spinner = PolishSpinner(
                text=mode_label(policy_mode),
                values=[mode_label(policy_mode)],
                font_size=19,
                size_hint_y=None,
                height=64,
            )
            self.content.add_widget(self.mode_spinner)

            self._section(tr("specialized.answer_style"))
            self._boolean_row("plain_output", tr("specialized.plain"))
            self._boolean_row("polite_output", tr("specialized.polite"))

            self._section(tr("specialized.tab.forms"))
            for form_id, form in form_groups.items():
                row, checkbox = setting_row(
                    tr(f"specialized.form_group.{form_id}"),
                    True,
                    lambda _value: None,
                )
                self.form_checks[form_id] = checkbox
                self.content.add_widget(row)

            self._section(tr("specialized.tab.patterns"))
            for pattern_id, label_text in pattern_labels.items():
                row, checkbox = setting_row(
                    tr(f"specialized.pattern.{pattern_id}"),
                    True,
                    lambda _value: None,
                )
                self.pattern_checks[pattern_id] = checkbox
                self.content.add_widget(row)

            self._section(tr("specialized.word_filter"))
            filter_help = PolishLabel(
                text=tr(
                    "specialized.word_filter_help",
                    example=mobile_filter_hint,
                ),
                font_size=15,
                halign="left",
                valign="middle",
                size_hint_y=None,
                height=dp(70),
            )
            wrap_label(filter_help)
            self.content.add_widget(filter_help)
            self.word_filter = PolishInput(
                multiline=False,
                font_size=18,
                size_hint_y=None,
                height=64,
                hint_text=mobile_filter_hint,
            )
            self.content.add_widget(self.word_filter)

            self._section(tr("specialized.flow"))
            font_row = BoxLayout(
                orientation="vertical",
                size_hint_y=None,
                height=96,
                spacing=dp(4),
            )
            font_title = BoxLayout(size_hint_y=None, height=36)
            font_label = PolishLabel(
                text=tr("specialized.text_scale"),
                font_size=18,
                halign="left",
                valign="middle",
            )
            wrap_label(font_label)
            self.font_scale_slider = Slider(
                min=0.7,
                max=3.0,
                step=0.05,
                value=1.0,
            )
            self.font_scale_value = PolishLabel(
                text="100%",
                font_size=18,
                size_hint_x=None,
                width=72,
            )
            self.font_scale_slider.bind(value=self._font_scale_changed)
            font_title.add_widget(font_label)
            font_title.add_widget(self.font_scale_value)
            font_row.add_widget(font_title)
            font_row.add_widget(self.font_scale_slider)
            self.content.add_widget(font_row)
            button_size_row = BoxLayout(
                orientation="vertical",
                size_hint_y=None,
                height=dp(96),
                spacing=dp(4),
            )
            button_title = BoxLayout(size_hint_y=None, height=dp(36))
            button_size_label = PolishLabel(
                text=tr("specialized.button_scale"),
                font_size=18,
                halign="left",
                valign="middle",
            )
            wrap_label(button_size_label)
            self.mobile_button_scale_slider = Slider(
                min=0.8,
                max=1.6,
                step=0.05,
                value=DEFAULT_MOBILE_BUTTON_SCALE,
            )
            self.mobile_button_scale_value = PolishLabel(
                text="100%",
                font_size=18,
                size_hint_x=None,
                width=dp(72),
            )
            self.mobile_button_scale_slider.bind(
                value=self._mobile_button_scale_changed
            )
            button_title.add_widget(button_size_label)
            button_title.add_widget(self.mobile_button_scale_value)
            button_size_row.add_widget(button_title)
            button_size_row.add_widget(self.mobile_button_scale_slider)
            self.content.add_widget(button_size_row)
            self.question_count = self._number_input(
                tr("specialized.question_count"),
            )
            self.auto_advance = self._number_input(
                tr("specialized.auto_advance"),
                decimal=True,
            )

            statistics_button = PolishButton(
                text=tr("specialized.calculate_options"),
                font_size=19,
                size_hint_y=None,
                height=62,
            )
            statistics_button.bind(
                on_release=lambda *_: self.calculate_statistics()
            )
            self.content.add_widget(statistics_button)
            self.statistics = PolishLabel(
                text="",
                color=accent_info,
                font_size=17,
                halign="left",
                valign="middle",
                size_hint_y=None,
                height=120,
            )
            wrap_label(self.statistics)
            self.content.add_widget(self.statistics)

            if not getattr(quiz_app(), "embedded_mode", False):
                self._section(tr("settings.updates"))
                self.settings_check_update_button = PolishButton(
                    text=tr("action.check_updates"),
                    font_size=19,
                    size_hint_y=None,
                    height=62,
                )
                self.settings_check_update_button.bind(
                    on_release=lambda *_: quiz_app().check_for_updates()
                )
                self.content.add_widget(self.settings_check_update_button)
                self.settings_update_button = PolishButton(
                    text=tr("action.update"),
                    font_size=19,
                    size_hint_y=None,
                    height=62,
                )
                self.settings_update_button.bind(
                    on_release=lambda *_: quiz_app().update_quiz()
                )
                self.content.add_widget(self.settings_update_button)
                self.update_status = PolishLabel(
                    text=tr("settings.update_not_checked"),
                    color=accent_info,
                    font_size=16,
                    halign="left",
                    valign="middle",
                    size_hint_y=None,
                    height=64,
                )
                wrap_label(self.update_status)
                self.content.add_widget(self.update_status)
            else:
                self.settings_check_update_button = None
                self.settings_update_button = None
                self.update_status = None

            self.status = PolishLabel(
                text="",
                color=accent_bad,
                font_size=17,
                halign="left",
                valign="middle",
                size_hint_y=None,
                height=70,
            )
            wrap_label(self.status)
            self.content.add_widget(self.status)
            scroll.add_widget(self.content)
            root.add_widget(scroll)

            buttons = BoxLayout(
                orientation="vertical",
                size_hint_y=None,
                spacing=dp(8),
            )
            buttons.bind(minimum_height=buttons.setter("height"))
            save_row = action_row(68, spacing=dp(8))
            save = PolishButton(text=tr("action.save"), font_size=19)
            save.bind(on_release=lambda *_: self.save(False))
            save_start = PolishButton(
                text=tr("specialized.save_start"),
                font_size=18,
            )
            save_start.bind(on_release=lambda *_: self.save(True))
            back = PolishButton(text=tr("action.back"), font_size=19)
            back.bind(
                on_release=lambda *_: quiz_app().go_home()
            )
            save_row.add_widget(save)
            save_row.add_widget(save_start)
            buttons.add_widget(save_row)
            back_row = action_row(68)
            back_row.add_widget(back)
            buttons.add_widget(back_row)
            root.add_widget(buttons)
            self.add_widget(root)

        def _section(self, text: str) -> None:
            label = PolishLabel(
                text=text,
                color=accent_info,
                font_size=21,
                halign="left",
                valign="middle",
                size_hint_y=None,
                height=48,
            )
            wrap_label(label)
            self.content.add_widget(label)

        def _boolean_row(self, key: str, text: str) -> None:
            row, checkbox = setting_row(
                text,
                True,
                lambda _value: None,
            )
            self.value_checks[key] = checkbox
            self.content.add_widget(row)

        def _number_input(
            self,
            title: str,
            decimal: bool = False,
        ) -> TextInput:
            row = BoxLayout(
                orientation="vertical",
                size_hint_y=None,
                height=104,
                spacing=dp(4),
            )
            label = PolishLabel(
                text=title,
                font_size=18,
                halign="left",
                valign="middle",
                size_hint_y=None,
                height=36,
            )
            wrap_label(label)
            value = PolishInput(
                multiline=False,
                input_filter=None if decimal else "int",
                font_size=22,
                size_hint_y=None,
                height=64,
            )
            row.add_widget(label)
            row.add_widget(value)
            self.content.add_widget(row)
            return value

        def on_pre_enter(self, *_args):
            self.populate(quiz_app().settings)
            self.show_update_state()

        def on_leave(self, *_args):
            app = quiz_app()
            app.apply_font_scale(app.settings.font_scale)
            app.apply_mobile_button_scale(
                app.settings.mobile_button_scale
            )

        def show_update_state(self) -> None:
            if self.settings_update_button is None:
                return
            app = quiz_app()
            self.settings_update_button.text = app.update_button_text
            self.settings_update_button.disabled = (
                app.update_in_progress or app.restart_required
            )
            if self.settings_check_update_button is not None:
                self.settings_check_update_button.disabled = app.update_in_progress
            if self.update_status is not None:
                self.update_status.text = (
                    app.update_message or tr("settings.update_not_checked")
                )

        def populate(self, settings: object) -> None:
            self.mode_spinner.text = mode_label(settings.mode)
            for key in (
                "plain_output",
                "polite_output",
            ):
                self.value_checks[key].active = bool(
                    getattr(settings, key)
                )
            for name, checkbox in self.form_checks.items():
                checkbox.active = name in settings.enabled_forms
            for name, checkbox in self.pattern_checks.items():
                checkbox.active = name in settings.enabled_patterns
            self.word_filter.text = settings.word_filter
            self.question_count.text = str(settings.question_count)
            self.auto_advance.text = str(
                settings.auto_advance_seconds
            )
            self.font_scale_slider.value = settings.font_scale
            self._font_scale_changed(
                self.font_scale_slider,
                settings.font_scale,
            )
            self.mobile_button_scale_slider.value = (
                settings.mobile_button_scale
            )
            self._mobile_button_scale_changed(
                self.mobile_button_scale_slider,
                settings.mobile_button_scale,
            )
            self.status.text = ""
            self.statistics.text = ""

        def read_settings(self):
            settings = policy_settings(
                mode=policy_mode,
                plain_output=self.value_checks["plain_output"].active,
                polite_output=self.value_checks["polite_output"].active,
                enabled_forms=[
                    name
                    for name, checkbox in self.form_checks.items()
                    if checkbox.active
                ],
                enabled_patterns=[
                    name
                    for name, checkbox in self.pattern_checks.items()
                    if checkbox.active
                ],
                word_filter=self.word_filter.text.strip(),
                question_count=_safe_int(self.question_count.text, 0),
                number_of_tries=1,
                random_order=True,
                auto_advance_seconds=_safe_float(
                    self.auto_advance.text,
                    -1.0,
                ),
                font_scale=float(self.font_scale_slider.value),
                mobile_button_scale=float(
                    self.mobile_button_scale_slider.value
                ),
            )
            settings.validate()
            return settings

        def _font_scale_changed(
            self,
            _slider,
            value: float,
        ) -> None:
            self.font_scale_value.text = f"{round(value * 100)}%"
            app = quiz_app()
            if hasattr(app, "apply_font_scale"):
                app.apply_font_scale(float(value))

        def _mobile_button_scale_changed(
            self,
            _slider,
            value: float,
        ) -> None:
            self.mobile_button_scale_value.text = f"{round(value * 100)}%"
            app = quiz_app()
            if hasattr(app, "apply_mobile_button_scale"):
                app.apply_mobile_button_scale(float(value))

        def save(self, start_after_save: bool) -> None:
            try:
                settings = self.read_settings()
                app = quiz_app()
                app.save_settings(settings)
                self.status.color = accent_ok
                self.status.text = tr("settings.saved")
                if start_after_save:
                    app.start_quiz()
            except (policy_error, OSError) as exception:
                self.status.color = accent_bad
                self.status.text = mobile_error_text(self, exception)

        def calculate_statistics(self) -> None:
            try:
                settings = self.read_settings()
                self.statistics.text = tr("specialized.counting")
                quiz_app().calculate_statistics(
                    settings,
                    self._statistics_ready,
                )
            except policy_error as exception:
                self.statistics.text = mobile_error_text(self, exception)

        def _statistics_ready(
            self,
            values: Optional[Dict[str, int]],
            error: str,
        ) -> None:
            if error:
                self.statistics.text = error
                return
            if values is None:
                self.statistics.text = tr("specialized.count_failed")
                return
            self.statistics.text = "\n".join(
                (
                    tr("specialized.available_words", count=values["words"]),
                    tr("specialized.active_patterns", count=values["patterns"]),
                    tr("specialized.available_entities", count=values["entities"]),
                    tr("specialized.noun_categories", count=values["categories"]),
                    tr("specialized.possible_questions", count=values["possible"]),
                )
            )

    class HelpScreen(Screen):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            root = BoxLayout(
                orientation="vertical",
                padding=16,
                spacing=10,
            )
            scroll = ScrollView(do_scroll_x=False)
            content = BoxLayout(
                orientation="vertical",
                padding=12,
                spacing=12,
                size_hint_y=None,
            )
            content.bind(minimum_height=content.setter("height"))
            help_app_id = (
                "availability" if is_default_availability else "grammar"
            )
            sections = (
                (
                    tr("specialized.help.how"),
                    tr(f"specialized.help.{help_app_id}.how"),
                ),
                (
                    tr("specialized.help.keyboard"),
                    tr(f"specialized.help.{help_app_id}.keyboard"),
                ),
                (
                    tr("specialized.help.hint"),
                    tr(f"specialized.help.{help_app_id}.hint"),
                ),
                (
                    tr("specialized.help.settings"),
                    tr("specialized.help.settings_body"),
                ),
                (
                    tr("specialized.help.filters"),
                    tr(f"specialized.help.{help_app_id}.filters"),
                ),
                (
                    tr("specialized.help.files"),
                    tr("specialized.help.files_body"),
                ),
            )
            content.add_widget(
                PolishLabel(
                    text=tr("specialized.help"),
                    font_size=30,
                    size_hint_y=None,
                    height=54,
                )
            )
            for title, body in sections:
                title_label = PolishLabel(
                    text=title,
                    color=accent_info,
                    font_size=22,
                    halign="left",
                    valign="middle",
                    size_hint_y=None,
                    height=44,
                )
                wrap_label(title_label)
                content.add_widget(title_label)
                body_label = PolishLabel(
                    text=body,
                    font_size=19,
                    halign="left",
                    valign="middle",
                    size_hint_y=None,
                    height=120,
                )
                wrap_label(body_label)
                content.add_widget(body_label)
            scroll.add_widget(content)
            root.add_widget(scroll)
            back = PolishButton(
                text=tr("action.back"),
                font_size=21,
                size_hint_y=None,
                height=68,
            )
            back.bind(
                on_release=lambda *_: quiz_app().go_home()
            )
            root.add_widget(back)
            self.add_widget(root)

    class QuizScreen(Screen):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.session: Optional[object] = None
            self.auto_event = None
            self.focus_request = FocusRequest()
            self.screen_active = False
            self.hint_visible = False
            root = BoxLayout(
                orientation="vertical",
                padding=dp(MOBILE_QUIZ_LAYOUT.root_padding),
                spacing=dp(MOBILE_QUIZ_LAYOUT.root_spacing),
            )

            header = action_row(
                MOBILE_QUIZ_LAYOUT.header_height,
                spacing=dp(6),
            )
            self.progress = AdaptiveSingleLineLabel(
                text="",
                fit_plain_text="",
                preferred_font_sp=14,
                minimum_font_sp=8,
                halign="left",
                valign="middle",
            )
            embedded_mode = bool(getattr(quiz_app(), "embedded_mode", False))
            menu_button = PolishButton(
                text=(
                    tr("specialized.launcher_menu")
                    if embedded_mode
                    else tr("specialized.menu")
                ),
                font_size=sp(16),
                size_hint_x=None,
                width=dp(104 if embedded_mode else 92),
            )
            menu_button.bind(
                on_release=(
                    (lambda *_: leave_quiz())
                    if embedded_mode
                    else (lambda *_: quiz_app().go_home())
                )
            )
            header.add_widget(self.progress)
            header.add_widget(menu_button)
            root.add_widget(header)
            self.progress_bar = ProgressBar(
                max=1.0,
                value=0.0,
                size_hint_y=None,
                height=dp(MOBILE_QUIZ_LAYOUT.progress_height),
            )
            root.add_widget(self.progress_bar)
            self.form_line = AdaptiveSingleLineLabel(
                text="",
                fit_plain_text="",
                markup=True,
                preferred_font_sp=14,
                minimum_font_sp=1,
                size_hint_y=None,
                height=dp(MOBILE_QUIZ_LAYOUT.form_height),
            )
            root.add_widget(self.form_line)

            answer_placeholder = f"{tr('mobile.answer')}:"
            self.status = AdaptiveSingleLineLabel(
                text=answer_placeholder,
                fit_plain_text=answer_placeholder,
                markup=True,
                preferred_font_sp=MOBILE_QUIZ_LAYOUT.review_preferred_sp,
                minimum_font_sp=MOBILE_QUIZ_LAYOUT.review_minimum_sp,
                halign="left",
                valign="middle",
                size_hint_y=None,
                height=dp(MOBILE_QUIZ_LAYOUT.review_height),
            )
            root.add_widget(self.status)

            content = BoxLayout(
                orientation="vertical",
                padding=[
                    dp(MOBILE_QUIZ_LAYOUT.content_horizontal_padding),
                    0,
                    dp(MOBILE_QUIZ_LAYOUT.content_horizontal_padding),
                    0,
                ],
                spacing=dp(MOBILE_QUIZ_LAYOUT.content_spacing),
                size_hint_y=None,
            )
            content.bind(minimum_height=content.setter("height"))
            self.question_line = AdaptiveSingleLineLabel(
                text="",
                fit_plain_text="",
                markup=True,
                preferred_font_sp=MOBILE_QUIZ_LAYOUT.prompt_preferred_sp,
                minimum_font_sp=MOBILE_QUIZ_LAYOUT.prompt_minimum_sp,
                maximum_fit_lines=MOBILE_QUIZ_LAYOUT.prompt_maximum_lines,
                halign="left",
                valign="middle",
                size_hint_y=None,
                height=dp(MOBILE_QUIZ_LAYOUT.prompt_height),
            )
            content.add_widget(self.question_line)

            self.answer_input = JapaneseInput(
                font_size=sp(23),
                size_hint_y=None,
                height=dp(MOBILE_QUIZ_LAYOUT.input_height),
                padding=[dp(10), dp(5), dp(10), dp(5)],
                hint_text=tr("specialized.answer_placeholder"),
            )
            self.answer_input._mobile_max_font_size = dp(27)
            self.answer_input.font_size = min(
                float(self.answer_input.font_size),
                self.answer_input._mobile_max_font_size,
            )
            self.answer_input.bind(
                on_text_validate=lambda *_: self.input_action()
            )
            content.add_widget(self.answer_input)

            self.hint = AdaptiveSingleLineLabel(
                text="",
                fit_plain_text="",
                markup=True,
                color=accent_info,
                preferred_font_sp=MOBILE_QUIZ_LAYOUT.hint_preferred_sp,
                minimum_font_sp=MOBILE_QUIZ_LAYOUT.hint_minimum_sp,
                halign="left",
                valign="middle",
                size_hint_y=None,
                height=dp(MOBILE_QUIZ_LAYOUT.hint_height),
                opacity=0,
            )
            content.add_widget(self.hint)

            first_row = action_row(
                MOBILE_QUIZ_LAYOUT.action_height,
                spacing=dp(6),
            )
            self.primary_button = PolishButton(
                text=tr("specialized.check"),
                font_size=sp(18),
            )
            self.primary_button.bind(
                on_release=lambda *_: self._button_action(
                    self.primary_action
                )
            )
            self.secondary_button = PolishButton(
                text=tr("specialized.hint_button"),
                font_size=sp(18),
            )
            self.secondary_button.bind(
                on_release=lambda *_: self._button_action(
                    self.secondary_action
                )
            )
            first_row.add_widget(self.primary_button)
            first_row.add_widget(self.secondary_button)
            content.add_widget(first_row)
            content.add_widget(Widget())

            # Active quiz controls are deliberately not scrollable.  Hints
            # and feedback occupy reserved slots so taps never reflow them.
            # A top anchor makes any extreme small-screen overflow happen
            # below the controls instead of moving the question upward.
            content_anchor = AnchorLayout(anchor_x="left", anchor_y="top")
            content_anchor.add_widget(content)
            root.add_widget(content_anchor)
            self.add_widget(root)

        def set_session(self, session: object) -> None:
            self._cancel_auto_advance()
            self.cancel_focus()
            self.session = session
            self.next_question()

        def _button_action(self, callback) -> None:
            callback()
            self.keep_keyboard_visible()

        def keep_keyboard_visible(self) -> None:
            self.focus_request.schedule(
                Clock.schedule_once,
                self._restore_answer_focus,
                self._focus_is_active,
            )

        def _restore_answer_focus(self) -> None:
            self.answer_input.focus = True

        def _focus_is_active(self) -> bool:
            controller = quiz_app()
            manager = getattr(controller, "manager", None)
            return bool(
                self.screen_active
                and manager is not None
                and manager.current == self.name
                and self.session is not None
                and self.session.current_question is not None
            )

        def cancel_focus(self) -> None:
            self.focus_request.cancel()

        def on_enter(self, *_args):
            self.screen_active = True
            self.keep_keyboard_visible()

        def configure_actions(self) -> None:
            """Update labels and colors without replacing either button."""
            if self.session is None:
                return
            primary = self.primary_button
            secondary = self.secondary_button
            primary.opacity = 1
            primary.disabled = False
            primary.color = MOBILE_BUTTON_TEXT
            secondary.color = MOBILE_BUTTON_TEXT
            if self.session.waiting_for_next:
                if self.session.current_outcome == "wrong":
                    primary.text = tr("quiz.accept")
                    primary.background_color = MOBILE_CORRECT_BACKGROUND
                    secondary.text = tr("quiz.wrong")
                    secondary.opacity = 1
                    secondary.disabled = False
                    secondary.background_color = MOBILE_WRONG_BACKGROUND
                else:
                    primary.text = tr("quiz.next")
                    primary.background_color = MOBILE_CORRECT_BACKGROUND
                    secondary.text = ""
                    secondary.opacity = 0
                    secondary.disabled = True
                    secondary.background_color = MOBILE_BUTTON_BACKGROUND
                return
            primary.text = tr("specialized.check")
            primary.background_color = MOBILE_BUTTON_BACKGROUND
            secondary.text = tr("specialized.hint_button")
            secondary.opacity = 1
            secondary.disabled = False
            secondary.background_color = (
                hint_active_background
                if self.hint_visible
                else MOBILE_BUTTON_BACKGROUND
            )

        def update_progress(self) -> None:
            """Refresh compact progress counters and the dedicated form row."""
            if self.session is None:
                return
            total = max(1, int(self.session.settings.question_count))
            current = min(total, max(0, self.session.current_index + 1))
            question_text = tr(
                "mobile.compact_question_progress",
                current=current,
                total=total,
            )
            progress_text = (
                f"{question_text}   "
                f"✓{self.session.correct_answers}  "
                f"×{self.session.wrong_answers}  "
                f"✓+{self.session.accepted_answers}"
            )
            self.progress.set_fitted_text(progress_text, progress_text)
            self.progress_bar.value = current / total
            question = self.session.current_question
            form_text = (
                f"[{target_label(question)}]" if question is not None else ""
            )
            self.form_line.set_fitted_text(
                (
                    f"[color=#26338C]{escape_markup(form_text)}[/color]"
                    if form_text
                    else ""
                ),
                form_text,
            )

        def next_question(self) -> None:
            self._cancel_auto_advance()
            if self.session is None:
                return
            if (
                self.session.current_question is not None
                and not self.session.waiting_for_next
            ):
                self.status.color = accent_info
                message = tr("specialized.check_or_skip_first")
                self.status.set_fitted_text(message, message)
                return
            self.form_line.set_fitted_text("", "")
            self.question_line.set_fitted_text("", "")
            answer_placeholder = f"{tr('mobile.answer')}:"
            self.status.set_fitted_text(
                answer_placeholder,
                answer_placeholder,
            )
            self.hint.set_fitted_text("", "")
            self.hint.opacity = 0
            self.hint_visible = False
            try:
                question = self.session.next_question()
            except (policy_error, ProjectError) as exception:
                self.status.color = accent_bad
                message = mobile_error_text(self, exception)
                self.status.set_fitted_text(escape_markup(message), message)
                return
            if question is None:
                self.show_results()
                return
            self.update_progress()
            source_plain = question.source_sentence
            context_plain = question.context_question
            source = escape_markup(source_plain)
            context = escape_markup(context_plain)
            question_markup = (
                source
                + (
                    f"  [color=#5B6472]· {context}[/color]"
                    if context
                    else ""
                )
            )
            question_plain = source_plain + (
                f"  · {context_plain}" if context_plain else ""
            )
            self.question_line.set_fitted_text(question_markup, question_plain)
            self.answer_input.set_review_locked(False)
            self.answer_input.background_color = input_active_background
            self.answer_input.text = ""
            answer_placeholder = f"{tr('mobile.answer')}:"
            self.status.set_fitted_text(
                answer_placeholder,
                answer_placeholder,
            )
            self.status.color = label_color
            self.hint.set_fitted_text("", "")
            self.hint.opacity = 0
            self.hint_visible = False
            self.configure_actions()
            if self.screen_active:
                self.keep_keyboard_visible()

        def primary_action(self) -> None:
            if self.session is None:
                return
            if self.session.waiting_for_next:
                if self.session.current_outcome == "wrong":
                    self.accept_or_skip()
                else:
                    self.next_question()
            else:
                self.check_answer()

        def input_action(self) -> None:
            """Check before review; keep Enter inert in every terminal state."""
            if self.session is None or self.session.waiting_for_next:
                return
            self.check_answer()

        def secondary_action(self) -> None:
            if self.session is None:
                return
            if self.session.waiting_for_next:
                if self.session.current_outcome == "wrong":
                    self.next_question()
                return
            self.show_hint()

        def check_answer(self) -> None:
            if self.session is None:
                return
            if self.session.waiting_for_next:
                self.next_question()
                return
            result = self.session.submit(self.answer_input.text)
            self.update_progress()
            if result.state == "correct":
                self._show_terminal_review(
                    result.expected_answer,
                    correct=True,
                )
                delay = self.session.settings.auto_advance_seconds
                if delay > 0:
                    self.auto_event = Clock.schedule_once(
                        lambda _dt: self.next_question(),
                        delay,
                    )
            elif result.state == "wrong":
                self._show_terminal_review(
                    result.expected_answer,
                    correct=False,
                )
            elif result.state == "retry":
                message = tr(
                    "specialized.retry",
                    current=self.session.current_try,
                    total=self.session.settings.number_of_tries,
                )
                self.status.set_fitted_text(escape_markup(message), message)
                self.status.color = accent_bad
                self.keep_keyboard_visible()
            if result.state in {"correct", "wrong"}:
                self.keep_keyboard_visible()

        def _show_terminal_review(
            self,
            expected: str,
            correct: bool,
        ) -> None:
            """Fill one full-width correct-answer line without replacing input."""
            self.status.color = label_color
            answer_markup = (
                f"[color=#2F7A40]{escape_markup(expected)}[/color]"
            )
            self.status.set_fitted_text(answer_markup, expected)
            self.answer_input.set_review_locked(True)
            self.answer_input.background_color = (
                input_correct_background if correct else input_wrong_background
            )
            self.configure_actions()

        def show_hint(self) -> None:
            if (
                self.session is None
                or self.session.current_question is None
            ):
                return
            if self.hint_visible:
                self.hint_visible = False
                self.hint.set_fitted_text("", "")
                self.hint.opacity = 0
                self.configure_actions()
                self.keep_keyboard_visible()
                return
            question = self.session.current_question
            hint_text = format_mobile_hint_entries(
                mobile_sentence_hint_entries(
                    question, quiz_app().engine.project
                )
            )
            self.hint.set_fitted_text(
                escape_markup(hint_text),
                hint_text,
            )
            self.hint_visible = True
            self.hint.opacity = 1
            self.configure_actions()
            self.keep_keyboard_visible()

        def _resize_hint(self, *_args) -> None:
            if not self.hint_visible or not self.hint.text:
                self.hint.opacity = 0
                return
            self.hint._fit_font_to_width()

        def accept_or_skip(self) -> None:
            if self.session is None:
                return
            self._cancel_auto_advance()
            self.session.accept_or_skip()
            self.next_question()

        def show_results(self) -> None:
            if self.session is None:
                return
            self.screen_active = False
            self.cancel_focus()
            self.answer_input.focus = False
            app = quiz_app()
            results = app.manager.get_screen("results")
            results.set_session(self.session)
            app.manager.transition = SlideTransition(direction="left")
            app.manager.current = "results"

        def _cancel_auto_advance(self) -> None:
            if self.auto_event is not None:
                self.auto_event.cancel()
                self.auto_event = None

        def on_leave(self, *_args):
            self.screen_active = False
            self.cancel_focus()
            self._cancel_auto_advance()
            self.answer_input.focus = False

    class ResultsScreen(Screen):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            root = BoxLayout(
                orientation="vertical",
                padding=24,
                spacing=16,
            )
            root.add_widget(
                PolishLabel(
                    text=tr("specialized.finished"),
                    color=accent_info,
                    font_size=30,
                    size_hint_y=None,
                    height=58,
                )
            )
            self.results = PolishLabel(
                text="",
                font_size=23,
                halign="center",
                valign="middle",
                size_hint_y=None,
                height=220,
            )
            wrap_label(self.results)
            root.add_widget(self.results)
            again = PolishButton(
                text=tr("specialized.again"),
                font_size=22,
                size_hint_y=None,
                height=72,
            )
            again.bind(
                on_release=lambda *_: quiz_app().start_quiz()
            )
            root.add_widget(again)
            settings_button = PolishButton(
                text=tr("action.settings"),
                font_size=21,
                size_hint_y=None,
                height=70,
            )
            settings_button.bind(
                on_release=lambda *_: quiz_app().open_settings()
            )
            root.add_widget(settings_button)
            home = PolishButton(
                text=tr("specialized.main_menu"),
                font_size=21,
                size_hint_y=None,
                height=70,
            )
            home.bind(
                on_release=lambda *_: quiz_app().go_home()
            )
            root.add_widget(home)
            root.add_widget(Widget())
            self.add_widget(root)

        def set_session(self, session: object) -> None:
            self.results.text = tr(
                "specialized.results",
                correct=session.correct_answers,
                wrong=session.wrong_answers,
                accepted=session.accepted_answers,
            )

    class KotomiSentenceApp(App):
        icon = app_icon_png_path()
        def build(self):
            apply_kivy_window_icon(Window)
            self.title = tr(mobile_title_key)
            self.project_path = resolve_policy_project()
            self.settings_store = policy_store(policy_settings_path())
            self.settings = self.settings_store.load()
            font_scale_state["value"] = self.settings.font_scale
            button_scale_state["value"] = self.settings.mobile_button_scale
            self.engine: Optional[object] = None
            self.engine_error = ""
            self.update_message = ""
            self.update_button_text = tr("action.update")
            self.update_in_progress = False
            self.restart_required = False
            self.reload_engine()

            self.manager = ScreenManager()
            self.manager.add_widget(HomeScreen(name="home"))
            self.manager.add_widget(SettingsScreen(name="settings"))
            self.manager.add_widget(HelpScreen(name="help"))
            self.manager.add_widget(QuizScreen(name="quiz"))
            self.manager.add_widget(ResultsScreen(name="results"))
            self.apply_font_scale(self.settings.font_scale)
            self.apply_mobile_button_scale(
                self.settings.mobile_button_scale
            )
            if not getattr(self, "embedded_mode", False):
                Window.bind(on_keyboard=self._on_keyboard)
            return self.manager

        def prepare_for_unload(self) -> None:
            if not hasattr(self, "manager"):
                return
            quiz = self.manager.get_screen("quiz")
            quiz._cancel_auto_advance()
            quiz.cancel_focus()
            quiz.answer_input.focus = False

        def reload_engine(self) -> bool:
            try:
                if self.engine is None:
                    self.engine = policy_engine(self.project_path)
                else:
                    self.engine.reload()
                self.engine_error = ""
                return True
            except (policy_error, ProjectError, OSError) as exception:
                self.engine = None
                self.engine_error = mobile_error_text(self, exception)
                return False

        def home_summary(self) -> str:
            if self.engine_error:
                summary = tr(
                    "hub.cannot_open",
                    title=self.title,
                    detail=self.engine_error,
                )
            else:
                summary = settings_summary(self.settings)
            if self.update_message:
                summary += "\n\n" + self.update_message
            return summary

        def _refresh_home_update_state(self) -> None:
            if not hasattr(self, "manager"):
                return
            home = self.manager.get_screen("home")
            home.show_update_state()
            settings = self.manager.get_screen("settings")
            settings.show_update_state()

        def check_for_updates(self) -> None:
            if self.update_in_progress:
                return
            try:
                manifest_url = load_update_url(
                    INSTALL_ROOT / "mobile_update_config.json"
                )
                updater = QuizUpdater(INSTALL_ROOT, manifest_url)
            except UpdateError as exception:
                self.update_message = tr(
                    "settings.update_check_failed",
                    detail=mobile_error_text(
                        self, exception, key="mobile.update_failed"
                    ),
                )
                self._refresh_home_update_state()
                return

            self.update_in_progress = True
            self.update_message = tr("hub.checking_updates")
            self._refresh_home_update_state()

            def worker() -> None:
                try:
                    result = updater.check()
                    Clock.schedule_once(
                        lambda _dt: self._finish_update_check(result, ""),
                        0,
                    )
                except Exception as exception:
                    message = mobile_error_text(
                        self, exception, key="mobile.update_failed"
                    )
                    Clock.schedule_once(
                        lambda _dt: self._finish_update_check(None, message),
                        0,
                    )

            threading.Thread(target=worker, daemon=True).start()

        def _finish_update_check(self, result, error: str) -> None:
            self.update_in_progress = False
            if error:
                self.update_message = tr(
                    "settings.update_check_failed", detail=error
                )
            elif result.changed:
                self.update_message = tr(
                    "settings.update_available", version=result.version
                )
            else:
                self.update_message = tr(
                    "settings.update_current", version=result.version
                )
            self._refresh_home_update_state()

        def update_quiz(self) -> None:
            if self.update_in_progress:
                return
            try:
                manifest_url = load_update_url(
                    INSTALL_ROOT / "mobile_update_config.json"
                )
                updater = QuizUpdater(INSTALL_ROOT, manifest_url)
            except UpdateError as exception:
                self.update_message = mobile_error_text(
                    self,
                    exception,
                    key="mobile.update_failed",
                )
                self.update_button_text = tr("action.update")
                self._refresh_home_update_state()
                return

            self.update_in_progress = True
            self.update_message = tr("hub.checking_updates")
            self.update_button_text = tr("hub.checking_updates")
            self._refresh_home_update_state()

            def worker() -> None:
                try:
                    result = updater.update()
                    Clock.schedule_once(
                        lambda _dt: self._finish_update(result, ""),
                        0,
                    )
                except Exception as exception:
                    message = mobile_error_text(
                        self,
                        exception,
                        key="mobile.update_failed",
                    )
                    Clock.schedule_once(
                        lambda _dt: self._finish_update(None, message),
                        0,
                    )

            threading.Thread(target=worker, daemon=True).start()

        def _finish_update(self, result, error: str) -> None:
            self.update_in_progress = False
            self.update_button_text = tr("action.update")
            if error:
                self.update_message = tr("hub.update_failed", detail=error)
                self._refresh_home_update_state()
                return

            if not result.changed:
                self.update_message = tr(
                    "hub.version_current", version=result.version
                )
            elif result.restart_required:
                self.restart_required = True
                self.update_message = tr(
                    "hub.updated_restart", version=result.version
                )
                self.update_button_text = tr("hub.restart_required")
            else:
                self.reload_engine()
                self.update_message = tr(
                    "hub.updated_active", version=result.version
                )
            self._refresh_home_update_state()

        def save_settings(self, settings: object) -> None:
            self.settings_store.save(settings)
            self.settings = settings
            self.apply_font_scale(settings.font_scale)
            self.apply_mobile_button_scale(settings.mobile_button_scale)

        def apply_font_scale(self, scale: float) -> None:
            font_scale_state["value"] = float(scale)
            if hasattr(self, "manager"):
                _apply_absolute_font_scale(self.manager, float(scale))

        def apply_mobile_button_scale(self, scale: float) -> None:
            button_scale_state["value"] = validate_mobile_button_scale(scale)
            if hasattr(self, "manager"):
                _apply_absolute_button_scale(
                    self.manager,
                    button_scale_state["value"],
                )

        def start_quiz(self) -> None:
            if self.restart_required:
                self.update_message = tr("hub.restart_required")
                self.go_home()
                return
            if not self.reload_engine() or self.engine is None:
                self.go_home()
                return
            try:
                session = policy_session(self.engine, self.settings)
                quiz = self.manager.get_screen("quiz")
                self.manager.transition = SlideTransition(direction="left")
                self.manager.current = "quiz"
                quiz.set_session(session)
            except (policy_error, ProjectError) as exception:
                self.engine_error = mobile_error_text(self, exception)
                self.go_home()

        def open_settings(self) -> None:
            self.manager.transition = SlideTransition(direction="left")
            self.manager.current = "settings"

        def open_help(self) -> None:
            self.manager.transition = SlideTransition(direction="left")
            self.manager.current = "help"

        def go_home(self) -> None:
            self.manager.transition = SlideTransition(direction="right")
            self.manager.current = "home"

        def calculate_statistics(
            self,
            settings: object,
            callback,
        ) -> None:
            if self.engine is None:
                callback(None, self.engine_error)
                return
            engine = self.engine

            def worker() -> None:
                try:
                    result = engine.statistics(settings)
                    Clock.schedule_once(
                        lambda _dt: callback(result, ""),
                        0,
                    )
                except Exception as exception:
                    message = mobile_error_text(
                        self,
                        exception,
                        key="mobile.update_failed",
                    )
                    Clock.schedule_once(
                        lambda _dt: callback(None, message),
                        0,
                    )

            threading.Thread(target=worker, daemon=True).start()

        def _on_keyboard(self, _window, key, *_args):
            if key in (282, 290) and self.manager.current == "quiz":
                self.manager.get_screen("quiz").show_hint()
                return True
            if key not in (27, 1001):
                return False
            if self.manager.current == "home":
                self.stop()
            else:
                self.go_home()
            return True

        def on_stop(self):
            if not getattr(self, "embedded_mode", False):
                Window.unbind(on_keyboard=self._on_keyboard)

    return KotomiSentenceApp


def create_embedded_controller():
    """Create the availability UI controller for the master app."""
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
