"""Platform-neutral settings and generation logic for Grammar quizzes.

This module intentionally imports no Kivy or Tkinter classes. Desktop and
Mobile presentations use the same profile, settings, engine, session, and
question models from here.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
import os
from pathlib import Path
import random
import re
import sys
from typing import Callable, Dict, Iterable, List, Mapping, Optional, Sequence, Set


SCRIPT_DIR = Path(__file__).resolve().parent
REPOSITORY_SHARED_DIR = SCRIPT_DIR.parents[1] / "shared"
INSTALL_ROOT = REPOSITORY_SHARED_DIR.parent
for import_root in (INSTALL_ROOT, REPOSITORY_SHARED_DIR):
    if str(import_root) not in sys.path:
        sys.path.insert(0, str(import_root))

from quiz_core import Entity, ProjectError, Word
from quiz_engine import SharedQuizEngine, balanced_choice
from mobile_ui import DEFAULT_MOBILE_BUTTON_SCALE, validate_mobile_button_scale
from kotomi_core.settings_xml import load_settings, save_settings, settings_path
from apps.availability.logic import (
    AvailabilityQuizSession,
    FORM_GROUPS,
    FORM_STYLE_LABELS,
    SubmissionResult,
    normalize_japanese,
    selected_context_hint,
)


PROJECT_ENVIRONMENT_VARIABLE = "JAPANESE_QUIZ_PROJECT"
SETTINGS_FILENAME = "grammar_quiz_settings.xml"
ACTIVE_QUIZ_ID = "grammar"
RECENT_MAIN_VERB_WINDOW = 4


def quiz_settings_path() -> Path:
    return settings_path(INSTALL_ROOT, SETTINGS_FILENAME)

MODE_POLISH_TO_JAPANESE = "polish_to_japanese"
MODE_LABELS = {
    MODE_POLISH_TO_JAPANESE: "Napisz zdanie po japońsku",
}

PATTERN_LABELS = {
    "koto_ga_dekiru__simple": "ことができる, sam czasownik",
    "koto_ga_dekiru__transitive_object": "ことができる, dopełnienie",
    "koto_ga_dekiru__place": "ことができる, miejsce",
}
SUPPORTED_PATTERNS = tuple(PATTERN_LABELS)

MOBILE_APP_TITLE = "Kotomi, gramatyka"
MOBILE_SUBTITLE = "ことができる"
MOBILE_SETTINGS_TITLE = "Ustawienia quizu gramatycznego"
MOBILE_FILTER_TITLE = "Filtry elementów wzorca"
MOBILE_FILTER_HELP = (
    "Podaj slot.pole=wartość. Przykłady: verb.type=godan, "
    "noun.category=food lub noun.id=school,kitchen. "
    "Samo ending=ru jest skrótem dla verb.ending=ru."
)
MOBILE_FILTER_HINT = "verb.ending=ru;noun.category=food"
MOBILE_WORD_DETAIL_LABEL = "Czasownik główny"
MOBILE_HELP_SECTIONS = (
    (
        "Jak działa konstrukcja",
        "Quiz wybiera jeden ze wzorców wskazanych przez rozszerzenie, a następnie "
        "dodaje ことができる. Czasownik główny pozostaje "
        "w formie słownikowej, a できる otrzymuje wybraną formę.",
    ),
    (
        "Czas przeszły",
        "Dla przeszłości odmienia się końcowe できる: できた, "
        "できました, できなかった albo できませんでした. "
        "Kontekst czasu jest dobierany do wybranej formy.",
    ),
    (
        "Hint",
        "Hint pokazuje tylko dobrane słowa i rzeczowniki w formie "
        "podstawowej, bez ujawniania gotowej odpowiedzi.",
    ),
    (
        "Filtry",
        "Filtry mogą dotyczyć konkretnego slotu. Przykłady: "
        "verb.type=ichidan, noun.category=food, noun.id=school. "
        "Przecinek łączy wartości, średnik łączy warunki.",
    ),
)

WORD_FILTER_FIELDS = {
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
ENTITY_FILTER_FIELDS = {
    "dictionary",
    "id",
    "translation",
    "kana",
    "kanji",
    "category",
    "categories",
}


class GrammarQuizError(ValueError):
    """Raised for invalid grammar settings or unavailable questions."""


@dataclass
class GrammarQuizSettings:
    mode: str = MODE_POLISH_TO_JAPANESE
    polite_output: bool = True
    plain_output: bool = True
    enabled_forms: List[str] = field(default_factory=lambda: list(FORM_GROUPS))
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
    def from_dict(cls, values: Mapping[str, object]) -> "GrammarQuizSettings":
        defaults = cls()
        settings = cls(
            mode=str(values.get("mode", defaults.mode)),
            polite_output=bool(values.get("polite_output", defaults.polite_output)),
            plain_output=bool(values.get("plain_output", defaults.plain_output)),
            enabled_forms=[
                str(value)
                for value in values.get("enabled_forms", defaults.enabled_forms)
                if str(value) in FORM_GROUPS
            ],
            enabled_patterns=[
                str(value)
                for value in values.get("enabled_patterns", defaults.enabled_patterns)
                if str(value) in SUPPORTED_PATTERNS
            ],
            word_filter=str(values.get("word_filter", defaults.word_filter)),
            question_count=_safe_int(
                values.get("question_count"), defaults.question_count
            ),
            number_of_tries=1,
            random_order=True,
            auto_advance_seconds=_safe_float(
                values.get("auto_advance_seconds"), defaults.auto_advance_seconds
            ),
            font_scale=_safe_float(values.get("font_scale"), defaults.font_scale),
            mobile_button_scale=_safe_float(
                values.get("mobile_button_scale"), defaults.mobile_button_scale
            ),
        )
        settings.validate()
        return settings

    def validate(self) -> None:
        # These controls are intentionally no longer user-configurable.
        self.number_of_tries = 1
        self.random_order = True
        if self.mode != MODE_POLISH_TO_JAPANESE:
            raise GrammarQuizError(f"Nieznany tryb quizu: {self.mode}")
        if not self.enabled_forms:
            raise GrammarQuizError("Wybierz co najmniej jedną formę.")
        if not self.enabled_patterns:
            raise GrammarQuizError("Wybierz co najmniej jeden wzorzec zdania.")
        if not self.plain_output and not self.polite_output:
            raise GrammarQuizError(
                "Wybierz co najmniej jeden styl japońskiej odpowiedzi."
            )
        if not 1 <= self.question_count <= 200:
            raise GrammarQuizError("Liczba pytań musi mieścić się w zakresie 1–200.")
        if not 0.0 <= self.auto_advance_seconds <= 600.0:
            raise GrammarQuizError(
                "Automatyczne przejście musi mieścić się w zakresie 0–600 s."
            )
        if not 0.7 <= self.font_scale <= 3.0:
            raise GrammarQuizError("Rozmiar tekstu musi mieścić się w zakresie 70–300%.")
        try:
            validate_mobile_button_scale(self.mobile_button_scale)
        except (TypeError, ValueError) as exception:
            raise GrammarQuizError(str(exception)) from exception
        parse_slot_filter(self.word_filter)

    def summary(self) -> str:
        forms = ", ".join(FORM_GROUPS[name]["label"] for name in self.enabled_forms)
        patterns = ", ".join(PATTERN_LABELS[name] for name in self.enabled_patterns)
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
class SlotFilterRule:
    slot: str
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
class GrammarQuestion:
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


def parse_slot_filter(text: str) -> List[SlotFilterRule]:
    """Parse slot.field=value filters, defaulting an omitted slot to verb."""

    rules: List[SlotFilterRule] = []
    for expression in (text or "").split(";"):
        expression = expression.strip()
        if not expression:
            continue
        if "=" not in expression:
            raise GrammarQuizError(
                f"Nieprawidłowy filtr „{expression}”. Użyj slot.pole=wartość."
            )
        key, values_text = (value.strip() for value in expression.split("=", 1))
        if "." in key:
            slot, field_name = (value.strip().casefold() for value in key.split(".", 1))
        else:
            slot, field_name = "verb", key.casefold()
        if not re.fullmatch(r"[a-z][a-z0-9_]*", slot):
            raise GrammarQuizError(f"Nieprawidłowy slot filtra „{slot}”.")
        if field_name not in WORD_FILTER_FIELDS | ENTITY_FILTER_FIELDS:
            raise GrammarQuizError(f"Nieznane pole filtra „{field_name}”.")
        values = tuple(
            value.strip().casefold()
            for value in values_text.split(",")
            if value.strip()
        )
        if not values:
            raise GrammarQuizError(f"Filtr „{key}” nie zawiera wartości.")
        rules.append(SlotFilterRule(slot, field_name, values))
    return rules


def _rules_for_slot(
    rules: Iterable[SlotFilterRule], slot: str
) -> List[SlotFilterRule]:
    return [rule for rule in rules if rule.slot == slot]


def _rules_for_engine_slot(
    rules: Iterable[SlotFilterRule],
    analysis: object,
    slot: str,
) -> List[SlotFilterRule]:
    """Map simple quiz filter names onto engine-owned selector slots."""

    aliases = {slot}
    definition = analysis.slots[slot]
    if slot == analysis.focus_slot:
        aliases.add("verb")
    if definition.kind == "entity":
        aliases.add("noun")
    if definition.dictionary == "adjectives":
        aliases.add("adjective")
    return [rule for rule in rules if rule.slot in aliases]


def _item_matches(
    item: Word | Entity,
    rules: Iterable[SlotFilterRule],
    effective_categories: Optional[Callable[[Entity], Iterable[str]]] = None,
) -> bool:
    for rule in rules:
        if isinstance(item, Word) and rule.field in {"feature", "features"}:
            values = {value.casefold() for value in item.features}
            if not values.intersection(rule.values):
                return False
            continue
        if isinstance(item, Word) and rule.field in {"role", "roles"}:
            values = {value.casefold() for value in item.usage}
            if not values.intersection(rule.values):
                return False
            continue
        if rule.field in {"category", "categories"}:
            if isinstance(item, Word):
                values = {value.casefold() for value in item.categories}
            else:
                categories = (
                    effective_categories(item)
                    if effective_categories is not None
                    else (item.category,)
                )
                values = {value.casefold() for value in categories}
            if not values.intersection(rule.values):
                return False
            continue
        field_name = "dictionary_id" if rule.field == "dictionary" else rule.field
        value = str(getattr(item, field_name, "") or "").casefold()
        if value not in rule.values:
            return False
    return True


def resolve_project_path() -> Path:
    environment_path = os.environ.get(PROJECT_ENVIRONMENT_VARIABLE, "").strip()
    candidates = [
        Path(environment_path).expanduser() if environment_path else None,
        SCRIPT_DIR / "quiz_data" / "quiz_project.xml",
        REPOSITORY_SHARED_DIR / "quiz_data" / "quiz_project.xml",
        SCRIPT_DIR / "quiz_project.xml",
    ]
    for candidate in candidates:
        if candidate is not None and candidate.exists():
            return candidate.resolve()
    raise GrammarQuizError("Nie znaleziono quiz_project.xml.")


def configure_quiz_profile(quiz_id: str) -> None:
    """Configure this reusable quiz UI from one XML quiz definition."""

    project = SharedQuizEngine(resolve_project_path()).project
    quiz = project.sentence_quizzes.get(quiz_id)
    if quiz is None:
        raise GrammarQuizError(f"Nie znaleziono quizu zdań '{quiz_id}'.")
    effective_ids = project.sentence_quiz_pattern_ids(quiz)
    if not effective_ids:
        raise GrammarQuizError(f"Quiz '{quiz.label}' nie zawiera wzorców.")

    global ACTIVE_QUIZ_ID
    global SETTINGS_FILENAME
    global PATTERN_LABELS
    global SUPPORTED_PATTERNS
    global MOBILE_APP_TITLE
    global MOBILE_SUBTITLE
    global MOBILE_SETTINGS_TITLE
    global MOBILE_HELP_SECTIONS

    ACTIVE_QUIZ_ID = quiz.id
    SETTINGS_FILENAME = f"sentence_quiz_{quiz.id}_settings.xml"
    PATTERN_LABELS = {
        pattern_id: project.patterns[pattern_id].label
        for pattern_id in effective_ids
    }
    SUPPORTED_PATTERNS = tuple(effective_ids)
    MOBILE_APP_TITLE = f"Kotomi, {quiz.label}"
    MOBILE_SUBTITLE = quiz.description
    MOBILE_SETTINGS_TITLE = f"Ustawienia: {quiz.label}"
    MOBILE_HELP_SECTIONS = (
        (
            "Zakres quizu",
            quiz.description or "Quiz korzysta z wybranych wzorców zdań.",
        ),
        (
            "Formy",
            "Wybrana forma steruje dynamiczną formą zdania. Formy wymuszone "
            "wewnątrz wzorca, na przykład dictionary przed ことができる, "
            "pozostają bez zmian.",
        ),
        (
            "Hint",
            "Hint pokazuje tylko dobrane słowa i rzeczowniki w formie "
            "słownikowej, bez gotowej odpowiedzi.",
        ),
        (
            "Filtry",
            "Możesz użyć na przykład ending=su, verb.type=ichidan, "
            "noun.category=food lub noun.id=school. Przecinek łączy wartości, "
            "a średnik łączy warunki.",
        ),
    )


class SettingsStore:
    def __init__(self, path: Path) -> None:
        self.path = path

    def load(self) -> GrammarQuizSettings:
        if not self.path.exists():
            return GrammarQuizSettings()
        try:
            return GrammarQuizSettings.from_dict(load_settings(self.path))
        except (OSError, ValueError):
            return GrammarQuizSettings()

    def save(self, settings: GrammarQuizSettings) -> None:
        settings.validate()
        save_settings(self.path, asdict(settings))


class GrammarQuizEngine:
    """Quiz policy over patterns selected by one XML quiz definition."""

    def __init__(
        self,
        project_path: Path | str,
        rng: Optional[random.Random] = None,
    ) -> None:
        self.project_path = Path(project_path).resolve()
        self.rng = rng or random.Random()
        self.shared_engine = SharedQuizEngine(self.project_path, self.rng)
        self.project = self.shared_engine.project
        self._validate_project()

    def _validate_project(self) -> None:
        issues = self.project.validate()
        if issues:
            raise GrammarQuizError("\n".join(issues))

    def reload(self) -> None:
        self.shared_engine.reload()
        self.project = self.shared_engine.project
        self._validate_project()

    def build_generation_rules(
        self, settings: GrammarQuizSettings
    ) -> List[GenerationRule]:
        settings.validate()
        rules: List[GenerationRule] = []
        for category in settings.enabled_forms:
            group = FORM_GROUPS[category]
            for style, enabled in (
                ("plain", settings.plain_output),
                ("polite", settings.polite_output),
            ):
                if enabled:
                    rules.append(
                        GenerationRule(
                            category=category,
                            source_form="",
                            target_form=str(group[style]),
                            target_label=(
                                f"{str(group['label']).lower()}, styl "
                                f"{FORM_STYLE_LABELS[style]}"
                            ),
                        )
                    )
        return rules

    def build_combinations(
        self, settings: GrammarQuizSettings
    ) -> List[GenerationCombination]:
        combinations: List[GenerationCombination] = []
        for pattern_id in settings.enabled_patterns:
            pattern = self.project.patterns.get(pattern_id)
            if pattern is None:
                continue
            try:
                analysis = self.shared_engine.analyze_pattern(pattern)
            except ProjectError:
                continue
            if not analysis.focus_slot or not analysis.dynamic_slots:
                continue
            eligible_forms = set(
                self.shared_engine.eligible_form_names(pattern_id)
            )
            combinations.extend(
                GenerationCombination(pattern_id, rule)
                for rule in self.build_generation_rules(settings)
                if rule.target_form in eligible_forms
            )
        if not combinations:
            raise GrammarQuizError(
                "Bieżące ustawienia nie tworzą żadnej reguły quizu."
            )
        return combinations

    def _select_bindings(
        self,
        pattern_id: str,
        form_name: str,
        rules: Sequence[SlotFilterRule],
        word_usage: Mapping[str, int],
        recent_word_ids: Sequence[str],
    ) -> Optional[tuple[Dict[str, str], Dict[str, str]]]:
        analysis = self.shared_engine.analyze_pattern(pattern_id)
        word_choices: Dict[str, str] = {}
        entity_choices: Dict[str, str] = {}

        for slot in analysis.word_slots:
            slot_rules = _rules_for_engine_slot(rules, analysis, slot)
            if slot in analysis.fixed_words:
                dictionary = analysis.slots[slot].dictionary
                fixed = self.project.words[dictionary][analysis.fixed_words[slot]]
                if not _item_matches(
                    fixed,
                    slot_rules,
                    self.project.effective_entity_categories,
                ):
                    return None
                continue
            try:
                compatible = self.shared_engine.compatible(
                    pattern_id,
                    form_name=form_name,
                    word_choices=word_choices,
                    entity_choices=entity_choices,
                )
            except ProjectError:
                return None
            candidates = [
                word
                for word in compatible.words.get(slot, [])
                if _item_matches(
                    word,
                    slot_rules,
                    self.project.effective_entity_categories,
                )
            ]
            if not candidates:
                return None
            if slot == analysis.focus_slot:
                selected = balanced_choice(
                    candidates,
                    word_usage,
                    recent_word_ids,
                    self.rng,
                )
            else:
                selected = self.rng.choice(candidates)
            word_choices[slot] = selected.id

        for slot in analysis.entity_slots:
            try:
                compatible = self.shared_engine.compatible(
                    pattern_id,
                    form_name=form_name,
                    word_choices=word_choices,
                    entity_choices=entity_choices,
                )
            except ProjectError:
                return None
            candidates = [
                entity
                for entity in compatible.entities.get(slot, [])
                if _item_matches(
                    entity,
                    _rules_for_engine_slot(rules, analysis, slot),
                    self.project.effective_entity_categories,
                )
            ]
            if not candidates:
                return None
            entity_choices[slot] = self.rng.choice(candidates).id
        return word_choices, entity_choices

    def generate_question(
        self,
        settings: GrammarQuizSettings,
        seen_keys: Optional[Set[str]] = None,
        preferred: Optional[GenerationCombination] = None,
        word_usage: Optional[Mapping[str, int]] = None,
        recent_word_ids: Optional[Sequence[str]] = None,
    ) -> GrammarQuestion:
        rules = parse_slot_filter(settings.word_filter)
        combinations = self.build_combinations(settings)
        if preferred is not None:
            combinations = [preferred] + [
                value for value in combinations if value != preferred
            ]
        seen_keys = seen_keys or set()
        for attempt in range(128):
            combination = (
                preferred
                if preferred is not None and attempt == 0
                else self.rng.choice(combinations)
            )
            question = self._question_for_combination(
                combination,
                rules,
                word_usage or {},
                recent_word_ids or (),
            )
            if question is not None and question.key not in seen_keys:
                return question
        raise GrammarQuizError(
            "Nie udało się znaleźć kolejnego unikalnego pytania dla "
            "bieżących ustawień i filtrów."
        )

    def _question_for_combination(
        self,
        combination: GenerationCombination,
        rules: Sequence[SlotFilterRule],
        word_usage: Mapping[str, int],
        recent_word_ids: Sequence[str],
    ) -> Optional[GrammarQuestion]:
        selected = self._select_bindings(
            combination.pattern_id,
            combination.rule.target_form,
            rules,
            word_usage,
            recent_word_ids,
        )
        if selected is None:
            return None
        try:
            completed = self.shared_engine.complete(
                combination.pattern_id,
                form_name=combination.rule.target_form,
                word_choices=selected[0],
                entity_choices=selected[1],
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

        analysis = self.shared_engine.analyze_pattern(combination.pattern_id)
        main_slot = analysis.focus_slot
        main_dictionary = analysis.slots[main_slot].dictionary
        main_word = self.project.words[main_dictionary][preview.words[main_slot]]
        bindings = ", ".join(
            [
                *(f"{slot}={word}" for slot, word in preview.words.items()),
                *(f"{slot}={entity}" for slot, entity in preview.entities.items()),
            ]
        )
        key = "|".join(
            (
                combination.pattern_id,
                combination.rule.target_form,
                preview.source,
                preview.answer,
            )
        )
        context_translation, context_kana = selected_context_hint(
            self.project,
            preview,
        )
        return GrammarQuestion(
            key=key,
            source_sentence=preview.source,
            expected_answer=preview.answer,
            target_label=combination.rule.target_label,
            context_question="",
            pattern_id=combination.pattern_id,
            target_form=combination.rule.target_form,
            source_form="",
            word_id=main_word.id,
            word_meaning=main_word.translation,
            word_kana=main_word.kana,
            word_kanji=main_word.kanji,
            hint_pairs=self._hint_pairs(combination.pattern_id, preview),
            bindings=bindings,
            context_translation=context_translation,
            context_kana=context_kana,
        )

    def _hint_pairs(self, pattern_id: str, preview: object) -> List[tuple[str, str]]:
        analysis = self.shared_engine.analyze_pattern(pattern_id)
        result: List[tuple[str, str]] = []
        for slot in analysis.word_slots:
            dictionary = analysis.slots[slot].dictionary
            word = self.project.words[dictionary][preview.words[slot]]
            result.append((word.translation, word.kana))
        for slot in analysis.entity_slots:
            entity = self.project.entities[preview.entities[slot]]
            result.append((entity.translation, entity.kana))
        return result

    def statistics(self, settings: GrammarQuizSettings) -> Dict[str, int]:
        rules = parse_slot_filter(settings.word_filter)
        combinations = self.build_combinations(settings)
        possible = 0
        eligible_verbs: Set[str] = set()
        active_patterns: Set[str] = set()
        for combination in combinations:
            active_patterns.add(combination.pattern_id)
            analysis = self.shared_engine.analyze_pattern(combination.pattern_id)
            for preview in self.shared_engine.iter_previews(
                combination.pattern_id,
                form_name=combination.rule.target_form,
            ):
                matches = True
                for slot in analysis.word_slots:
                    dictionary = analysis.slots[slot].dictionary
                    word = self.project.words[dictionary][preview.words[slot]]
                    if not _item_matches(
                        word,
                        _rules_for_engine_slot(rules, analysis, slot),
                        self.project.effective_entity_categories,
                    ):
                        matches = False
                        break
                if not matches:
                    continue
                for slot in analysis.entity_slots:
                    entity = self.project.entities[preview.entities[slot]]
                    if not _item_matches(
                        entity,
                        _rules_for_engine_slot(rules, analysis, slot),
                        self.project.effective_entity_categories,
                    ):
                        matches = False
                        break
                if matches:
                    possible += 1
                    eligible_verbs.add(preview.words[analysis.focus_slot])
        return {
            "possible": possible,
            "active_patterns": len(active_patterns),
            "eligible": len(eligible_verbs),
            "categories": len(self.project.noun_categories),
            "patterns": len(active_patterns),
            "words": len(eligible_verbs),
            "entities": len(self.project.entities),
        }


GrammarQuizSession = AvailabilityQuizSession
QUIZ_SETTINGS_CLASS = GrammarQuizSettings
QUIZ_ENGINE_CLASS = GrammarQuizEngine
QUIZ_SESSION_CLASS = GrammarQuizSession
SETTINGS_STORE_CLASS = SettingsStore
QUIZ_ERROR_CLASS = GrammarQuizError


__all__ = [
    "ACTIVE_QUIZ_ID",
    "ENTITY_FILTER_FIELDS",
    "FORM_GROUPS",
    "FORM_STYLE_LABELS",
    "GenerationCombination",
    "GenerationRule",
    "GrammarQuestion",
    "GrammarQuizEngine",
    "GrammarQuizError",
    "GrammarQuizSession",
    "GrammarQuizSettings",
    "INSTALL_ROOT",
    "MOBILE_APP_TITLE",
    "MOBILE_FILTER_HELP",
    "MOBILE_FILTER_HINT",
    "MOBILE_FILTER_TITLE",
    "MOBILE_HELP_SECTIONS",
    "MOBILE_SETTINGS_TITLE",
    "MOBILE_SUBTITLE",
    "MOBILE_WORD_DETAIL_LABEL",
    "MODE_LABELS",
    "MODE_POLISH_TO_JAPANESE",
    "PATTERN_LABELS",
    "PROJECT_ENVIRONMENT_VARIABLE",
    "QUIZ_ENGINE_CLASS",
    "QUIZ_ERROR_CLASS",
    "QUIZ_SESSION_CLASS",
    "QUIZ_SETTINGS_CLASS",
    "RECENT_MAIN_VERB_WINDOW",
    "REPOSITORY_SHARED_DIR",
    "SCRIPT_DIR",
    "SETTINGS_FILENAME",
    "SETTINGS_STORE_CLASS",
    "SUPPORTED_PATTERNS",
    "SettingsStore",
    "SlotFilterRule",
    "SubmissionResult",
    "WORD_FILTER_FIELDS",
    "configure_quiz_profile",
    "normalize_japanese",
    "parse_slot_filter",
    "quiz_settings_path",
    "resolve_project_path",
    "selected_context_hint",
]
