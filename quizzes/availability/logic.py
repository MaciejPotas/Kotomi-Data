"""Platform-neutral settings and generation logic for the Availability quiz.

This module intentionally imports no Kivy or Tkinter classes. Desktop and
Mobile presentations use the same settings, engine, session, and question
models from here.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
import os
from pathlib import Path
import random
import re
import sys
from typing import Dict, Iterable, List, Mapping, Optional, Sequence, Set


SCRIPT_DIR = Path(__file__).resolve().parent
REPOSITORY_SHARED_DIR = SCRIPT_DIR.parents[1] / "shared"
INSTALL_ROOT = REPOSITORY_SHARED_DIR.parent
REPOSITORY_DATA_DIR = INSTALL_ROOT / "data"
for import_root in (INSTALL_ROOT, REPOSITORY_SHARED_DIR):
    if str(import_root) not in sys.path:
        sys.path.insert(0, str(import_root))

from quiz_core import ProjectError, Word
from quiz_engine import SharedQuizEngine, balanced_choice, normalize_answer
from mobile_ui import DEFAULT_MOBILE_BUTTON_SCALE, validate_mobile_button_scale
from kotomi_core.settings_xml import load_settings, save_settings


PROJECT_ENVIRONMENT_VARIABLE = "JAPANESE_QUIZ_PROJECT"
SETTINGS_FILENAME = "availability_quiz_settings.xml"
RECENT_MAIN_VERB_WINDOW = 4

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
        REPOSITORY_DATA_DIR / "quiz_project.xml",
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


__all__ = [
    "AvailabilityQuestion",
    "AvailabilityQuizEngine",
    "AvailabilityQuizSession",
    "AvailabilityQuizSettings",
    "FILTER_FIELDS",
    "FORM_GROUPS",
    "FORM_STYLE_LABELS",
    "GenerationCombination",
    "GenerationRule",
    "INSTALL_ROOT",
    "MODE_LABELS",
    "MODE_POLISH_TO_JAPANESE",
    "MobileQuizError",
    "PATTERN_LABELS",
    "PROJECT_ENVIRONMENT_VARIABLE",
    "RECENT_MAIN_VERB_WINDOW",
    "REPOSITORY_SHARED_DIR",
    "SCRIPT_DIR",
    "SETTINGS_FILENAME",
    "SUPPORTED_PATTERNS",
    "SettingsStore",
    "SubmissionResult",
    "WordFilterRule",
    "normalize_japanese",
    "parse_word_filter",
    "resolve_project_path",
    "selected_context_hint",
    "word_matches_filter",
]
