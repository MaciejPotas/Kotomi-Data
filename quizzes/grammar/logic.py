"""Platform-neutral settings and generation logic for Grammar quizzes.

This module intentionally imports no Kivy or Tkinter classes. Desktop and
Mobile presentations use the same profile, settings, engine, session, and
question models from here.
"""

from __future__ import annotations

from kotomi.application.quiz_hints import QuizVocabularyHint, selected_vocabulary_hints

from kotomi.core.generation.progress import progress_step
from kotomi.core.generation.cancellation import check_cancelled

from dataclasses import asdict, dataclass, field, replace
import os
from pathlib import Path
import random
import re
import sys
from typing import Callable, Dict, Iterable, List, Mapping, Optional, Sequence, Set
from types import SimpleNamespace


SCRIPT_DIR = Path(__file__).resolve().parent
INSTALL_ROOT = SCRIPT_DIR.parents[1]
REPOSITORY_DATA_DIR = INSTALL_ROOT / "data"
if str(INSTALL_ROOT) not in sys.path:
    sys.path.insert(0, str(INSTALL_ROOT))

from kotomi.core.project import Entity, ProjectError, Word
from kotomi.core.project.errors import SourceGrammarUnavailable
from kotomi.core.project.errors import NoCompatibleChoices
from kotomi.application.generation_engine import SharedQuizEngine
from kotomi.application.quiz_preflight import iter_quiz_previews
from kotomi.application.quiz_project import QuizProject
from kotomi.core.generation import (
    balanced_choice,
)
from kotomi.core.generation import compatibility as compatibility_solver
from kotomi.core.generation.counting import NumericRangeCandidates
from kotomi.core.generation.models import ChoiceScope, NumericRangeScope
from platforms.mobile.presentation import DEFAULT_MOBILE_BUTTON_SCALE, validate_mobile_button_scale
from kotomi.application.settings import validate_mobile_button_font_scale
from kotomi.application.settings_xml import load_settings, save_settings, settings_path, safe_int as _safe_int
from kotomi.application.sentence_session import (
    SentenceQuizSession,
    QuestionSpaceExhausted,
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
_HistoryKey = str | tuple[str, str]


def quiz_settings_path() -> Path:
    return settings_path(INSTALL_ROOT, SETTINGS_FILENAME)

MODE_TRANSFORMATION = "transformation"
MODE_POLISH_TO_JAPANESE = "polish_to_japanese"
MODE_LABELS = {
    MODE_POLISH_TO_JAPANESE: "Napisz zdanie po japońsku",
    MODE_TRANSFORMATION: "Zmień japońskie zdanie",
}

PATTERN_LABELS = {
    "Możliwość ことができる / Sam czasownik": "ことができる, sam czasownik",
    "Możliwość ことができる / Czasownik z dopełnieniem": "ことができる, dopełnienie",
    "Możliwość ことができる / Miejsce czynności": "ことができる, miejsce",
}
SUPPORTED_PATTERNS = tuple(PATTERN_LABELS)
PATTERN_EXPANSIONS = {pattern_id: (pattern_id,) for pattern_id in SUPPORTED_PATTERNS}
SUPPORTS_NUMERIC_QUANTITY_RANGE = False
FILTER_OPTIONS = {}
FILTER_DEFAULTS = {}
FILTER_TARGETS = {}
FILTER_VALUE_LABELS = {}
SUPPORTS_WORD_CHAINS = False
MOBILE_DIRECTION_TOGGLES = (("polite_to_plain", "specialized.polite_to_plain"),
                            ("plain_to_polite", "specialized.plain_to_polite"))

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

class GrammarQuizExhausted(GrammarQuizError, QuestionSpaceExhausted):
    """All renderable questions have already been used."""


@dataclass
class GrammarQuizSettings:
    mode: str = MODE_POLISH_TO_JAPANESE
    polite_output: bool = True
    plain_output: bool = True
    enabled_forms: List[str] = field(default_factory=lambda: list(FORM_GROUPS))
    enabled_patterns: List[str] | None = None
    word_filter: str = ""
    filter_selections: Dict[str, List[str]] = field(default_factory=dict)
    polite_to_plain: bool = True
    plain_to_polite: bool = False
    word_chain_length: int = 1
    quantity_range_enabled: bool = False
    quantity_range_min: int = 1
    quantity_range_max: int = 20
    question_count: int = 25
    number_of_tries: int = 1
    random_order: bool = True
    auto_advance_seconds: float = 100.0
    font_scale: float = 1.0
    mobile_button_font_scale: float = 1.0
    mobile_button_scale: float = DEFAULT_MOBILE_BUTTON_SCALE

    def __post_init__(self) -> None:
        supported = getattr(type(self), "supported_patterns", SUPPORTED_PATTERNS)
        if self.enabled_patterns is None:
            self.enabled_patterns = list(supported)
        self._pattern_labels = dict(getattr(type(self), "pattern_labels", PATTERN_LABELS))

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
                if str(value) in defaults.enabled_patterns
            ],
            word_filter=str(values.get("word_filter", defaults.word_filter)),
            filter_selections={key: list(value) for key, value in
                               values.get("filter_selections", {}).items()},
            polite_to_plain=bool(values.get("polite_to_plain", True)),
            plain_to_polite=bool(values.get("plain_to_polite", False)),
            word_chain_length=_safe_int(values.get("word_chain_length", 1), 1),
            quantity_range_enabled=bool(
                values.get(
                    "quantity_range_enabled",
                    defaults.quantity_range_enabled,
                )
            ),
            quantity_range_min=_safe_int(
                values.get("quantity_range_min"),
                defaults.quantity_range_min,
            ),
            quantity_range_max=_safe_int(
                values.get("quantity_range_max"),
                defaults.quantity_range_max,
            ),
            question_count=_safe_int(
                values.get("question_count"), defaults.question_count
            ),
            number_of_tries=1,
            random_order=True,
            auto_advance_seconds=_safe_float(
                values.get("auto_advance_seconds"), defaults.auto_advance_seconds
            ),
            font_scale=_safe_float(values.get("font_scale"), defaults.font_scale),
            mobile_button_font_scale=_safe_float(
                values.get("mobile_button_font_scale"), defaults.mobile_button_font_scale,
            ),
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
        if self.mode not in MODE_LABELS:
            raise GrammarQuizError(f"Nieznany tryb quizu: {self.mode}")
        if not self.enabled_forms:
            raise GrammarQuizError("Wybierz co najmniej jedną formę.")
        if not self.enabled_patterns:
            raise GrammarQuizError("Wybierz co najmniej jeden wzorzec zdania.")
        if self.mode == MODE_TRANSFORMATION and not (self.polite_to_plain or self.plain_to_polite):
            raise GrammarQuizError("Wybierz co najmniej jeden kierunek zmiany formy.")
        if not 1 <= self.word_chain_length <= 3:
            raise GrammarQuizError("Liczba słów w łańcuchu musi wynosić 1–3.")
        if self.mode == MODE_POLISH_TO_JAPANESE and not self.plain_output and not self.polite_output:
            raise GrammarQuizError(
                "Wybierz co najmniej jeden styl japońskiej odpowiedzi."
            )
        if (
            self.quantity_range_enabled
            and self.quantity_range_min > self.quantity_range_max
        ):
            raise GrammarQuizError(
                "Początek zakresu liczb nie może być większy od końca."
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
            validate_mobile_button_font_scale(self.mobile_button_font_scale)
        except (TypeError, ValueError) as exception:
            raise GrammarQuizError(str(exception)) from exception
        parse_slot_filter(self.effective_word_filter())

    def effective_word_filter(self) -> str:
        from kotomi.application.quiz_filters import selection_filter_text
        return ";".join(filter(None, (self.word_filter,
                                     selection_filter_text(self.filter_selections))))

    def summary(self) -> str:
        forms = ", ".join(FORM_GROUPS[name]["label"] for name in self.enabled_forms)
        patterns = ", ".join(self._pattern_labels.get(name, name) for name in self.enabled_patterns)
        summary = (
            f"{MODE_LABELS[self.mode]}\n"
            f"Pytania: {self.question_count}\n"
            f"Formy: {forms}\n"
            f"Wzorce: {patterns}\n"
            f"Rozmiar tekstu: {round(self.font_scale * 100)}%\n"
            f"Rozmiar przycisków: "
            f"{round(self.mobile_button_scale * 100)}%"
        )
        if self.quantity_range_enabled:
            summary += (
                "\nZakres liczb: "
                f"{self.quantity_range_min}–{self.quantity_range_max}"
            )
        return summary


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
    vocabulary_hints: tuple[QuizVocabularyHint, ...] | None = None
    _history_key: tuple[str, str] | None = field(default=None, repr=False, compare=False)


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

    from kotomi.core.project.quiz_filters import slot_filter_aliases
    aliases = slot_filter_aliases(analysis, slot)
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
        REPOSITORY_DATA_DIR / "quiz_project.xml",
        SCRIPT_DIR / "quiz_project.xml",
    ]
    for candidate in candidates:
        if candidate is not None and candidate.exists():
            return candidate.resolve()
    raise GrammarQuizError("Nie znaleziono quiz_project.xml.")


def chain_slot(project, analysis):
    """Recognize the bounded adjective composition supported by the renderer.

    Multi-clause patterns retain their authored structure. A chain is offered
    only for a single adjective with an optional copula and noun.
    """
    slots = [s for s in analysis.word_slots
             if project.dictionary_schemas.get(analysis.slots[s].dictionary) == "adjective"]
    if len(slots) != 1 or slots[0] in analysis.fixed_words:
        return None
    if any(project.dictionary_schemas.get(analysis.slots[s].dictionary)
           not in {"adjective", "copula"} for s in analysis.word_slots):
        return None
    if len(analysis.entity_slots) > 1 or any(t.kind == "relative" for t in analysis.placeholders):
        return None
    return slots[0]


def target_form_group(project, target_form):
    """Resolve presentation labels using the same catalog as generation."""
    for catalog in project.form_definitions.values():
        definition = catalog.get(target_form)
        if definition is None or not definition.register or not definition.polarity:
            continue
        category = "past" if definition.context == "past" else "nonpast"
        if definition.polarity == "negative":
            category = "past_negative" if category == "past" else "negative"
        return category, definition.register
    return None


def configure_quiz_profile(quiz_id: str, *, project: QuizProject | None = None) -> None:
    """Configure this reusable quiz UI from one XML quiz definition."""

    # No-argument loading is retained only for standalone legacy callers.
    if project is None:
        project = QuizProject.load(resolve_project_path())
    quiz = project.sentence_quizzes.get(quiz_id)
    if quiz is None:
        raise GrammarQuizError(f"Nie znaleziono quizu zdań '{quiz_id}'.")
    expansions = project.sentence_quiz_pattern_expansions(quiz)
    selection_ids = list(expansions)
    effective_ids = list(dict.fromkeys(value for values in expansions.values() for value in values))
    from kotomi.languages.contract import source_grammar_enabled
    if not selection_ids and quiz.pattern_ids and not source_grammar_enabled(project.instruction_language):
        # Keep the profile openable so the shared preflight can explain how to
        # enable the required source grammar. No unsupported question is generated.
        expansions = {reference: () for reference in quiz.pattern_ids}
        selection_ids = list(expansions)
    if not selection_ids:
        if quiz.pattern_ids:
            details = "; ".join(project.composite_diagnostics.values())
            raise GrammarQuizError(
                f"Quiz '{quiz.label}' has pattern definitions but no supported "
                f"expansions for instruction language '{project.instruction_language.id}'. "
                + details
            )
        raise GrammarQuizError(f"Quiz '{quiz.label}' nie zawiera wzorców.")

    global ACTIVE_QUIZ_ID
    global SETTINGS_FILENAME
    global PATTERN_LABELS
    global SUPPORTED_PATTERNS
    global PATTERN_EXPANSIONS
    global SUPPORTS_NUMERIC_QUANTITY_RANGE
    global FILTER_OPTIONS, FILTER_DEFAULTS, FILTER_TARGETS, FILTER_VALUE_LABELS, SUPPORTS_WORD_CHAINS
    global MOBILE_APP_TITLE
    global MOBILE_SUBTITLE
    global MOBILE_SETTINGS_TITLE
    global MOBILE_HELP_SECTIONS

    ACTIVE_QUIZ_ID = quiz.id
    SETTINGS_FILENAME = f"sentence_quiz_{quiz.id}_settings.xml"
    PATTERN_LABELS = {}
    for pattern_id in selection_ids:
        composite = project.composite_patterns.get(pattern_id)
        pattern = project.patterns.get(pattern_id)
        PATTERN_LABELS[pattern_id] = (
            composite.label if composite is not None
            else pattern.label if pattern is not None
            else pattern_id
        )
    SUPPORTED_PATTERNS = tuple(selection_ids)
    PATTERN_EXPANSIONS = expansions
    analyses = {}
    for pattern_id in effective_ids:
        try:
            analyses[pattern_id] = project.analyze_pattern(project.patterns[pattern_id])
        except SourceGrammarUnavailable:
            continue
    SUPPORTS_NUMERIC_QUANTITY_RANGE = any(
        slot.number_range is not None and not slot.fixed_word_id and not slot.number_sets
        for analysis in analyses.values() for slot in analysis.slots.values())
    from kotomi.application.quiz_filters import profile_filter_contract, value_labels
    FILTER_OPTIONS, FILTER_DEFAULTS, FILTER_TARGETS = profile_filter_contract(project, quiz)
    FILTER_VALUE_LABELS = value_labels(project)
    SUPPORTS_WORD_CHAINS = any(
        chain_slot(project, analysis) is not None for analysis in analyses.values())
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
    settings_class = GrammarQuizSettings

    def __init__(self, path: Path) -> None:
        self.path = path

    def load(self) -> GrammarQuizSettings:
        if not self.path.exists():
            legacy = getattr(type(self), "legacy_filename", "")
            legacy_path = self.path.with_name(legacy) if legacy else None
            if legacy_path is not None and legacy_path.exists():
                try:
                    values = load_settings(legacy_path)
                except (OSError, ValueError, TypeError, AttributeError):
                    return self.settings_class()
                if legacy.startswith("adjective"):
                    values["word_chain_length"] = values.pop("adjective_count", 1)
                    values["filter_selections"] = {"adjective.type": [value for value, flag in
                        (("i_adjective", "enable_i_adjectives"), ("na_adjective", "enable_na_adjectives"))
                        if values.get(flag, True)]}
                    expressions = []
                    for expression in values.get("word_filter", "").split(";"):
                        if expression.strip():
                            key, sep, value = expression.partition("=")
                            expressions.append((key if "." in key else "adjective." + key) + sep + value)
                    values["word_filter"] = ";".join(expressions)
                try:
                    settings = self.settings_class.from_dict(values)
                except (ValueError, TypeError):
                    # An invalid legacy selection is kept intact for rollback.
                    return self.settings_class()
                self.save(settings)
                return settings
            return self.settings_class()
        try:
            return self.settings_class.from_dict(load_settings(self.path))
        except (OSError, ValueError, TypeError, AttributeError):
            return self.settings_class()

    def save(self, settings: GrammarQuizSettings) -> None:
        settings.validate()
        save_settings(self.path, asdict(settings))


class GrammarQuizEngine:
    """Quiz policy over patterns selected by one XML quiz definition."""

    def __init__(
        self,
        project_path: Path | str,
        rng: Optional[random.Random] = None,
        *, language_context=None, project: QuizProject | None = None,
    ) -> None:
        self.language_context = language_context
        self.project_path = Path(project_path).resolve()
        self.rng = rng or random.Random()
        if project is not None:
            if project.manifest_path != self.project_path:
                raise GrammarQuizError("Quiz project belongs to a different Content manifest.")
            if language_context is not None and project.language_context is not language_context:
                raise GrammarQuizError("Quiz project belongs to a different LanguageContext.")
            self.project = project
        else:
            self.project = QuizProject.load(
                self.project_path, language_context=self.language_context,
            )
            self._validate_project()
        self.language_context = self.project.language_context
        self.shared_engine = SharedQuizEngine(self.project, self.rng)
        self.pattern_expansions = dict(getattr(type(self), "profile_expansions", PATTERN_EXPANSIONS))

    def _validate_project(self) -> None:
        issues = [issue for issue in self.project.validate()
                  if not issue.startswith("WARNING:")]
        if issues:
            raise GrammarQuizError("\n".join(issues))

    def reload(self) -> None:
        self.project = QuizProject.load(self.project_path, language_context=self.language_context)
        self.shared_engine = SharedQuizEngine(self.project, self.rng)
        self._validate_project()

    def build_generation_rules(self, settings, pattern_id=None, *, analysis=None):
        settings.validate()
        catalog = None
        if pattern_id is not None:
            analysis = analysis or self.shared_engine.analyze_pattern(pattern_id)
            if analysis.dynamic_slot:
                schema = self.project.dictionary_schemas.get(
                    analysis.slots[analysis.dynamic_slot].dictionary, "")
                catalog = self.project.form_definitions.get(schema, {})
        rules = []
        for category in settings.enabled_forms:
            group = FORM_GROUPS[category]
            context = "past" if category in {"past", "past_negative"} else "present"
            polarity = "negative" if category in {"negative", "past_negative"} else "affirmative"
            names = {style: (group[style] if catalog is None or group[style] in catalog else
                      next((f.name for f in catalog.values()
                      if (f.context in ({"present", "nonpast"} if context == "present" else {context})
                          and f.polarity == polarity and f.register == style)), ""))
                     for style in ("plain", "polite")}
            for style in ("plain", "polite"):
                transform = settings.mode == MODE_TRANSFORMATION
                enabled = (settings.polite_to_plain if style == "plain" else settings.plain_to_polite) if transform else getattr(settings, style + "_output")
                other = "polite" if style == "plain" else "plain"
                if enabled and names[style] and (not transform or names[other]):
                    rules.append(GenerationRule(category, names[other] if transform else "",
                        names[style], f"{group['label'].lower()}, styl {FORM_STYLE_LABELS[style]}"))
        return rules

    def build_combinations(
        self, settings: GrammarQuizSettings
    ) -> List[GenerationCombination]:
        settings.validate()
        cache = getattr(self, "precalculation", None)
        if cache is not None:
            return cache.combinations(self, settings, GenerationCombination, GenerationRule,
                                      self._build_combinations)
        return self._build_combinations(settings)

    def _build_combinations(self, settings: GrammarQuizSettings, *, allow_empty=False) -> List[GenerationCombination]:
        settings.validate()
        combinations: List[GenerationCombination] = []
        for selected_id in settings.enabled_patterns:
            for pattern_id in self.pattern_expansions.get(
                selected_id,
                (selected_id,),
            ):
                pattern = self.project.patterns.get(pattern_id)
                if pattern is None:
                    continue
                try:
                    analysis = self.shared_engine.analyze_pattern(pattern)
                except SourceGrammarUnavailable:
                    continue
                except ProjectError as error:
                    raise GrammarQuizError(f"Pattern '{pattern_id}': {error}") from error
                if not analysis.focus_slot and not analysis.entity_slots:
                    continue
                if settings.word_chain_length > 1 and chain_slot(self.project, analysis) is None:
                    continue
                if settings.mode == MODE_TRANSFORMATION and not self.shared_engine.transformation_slots(pattern, analysis=analysis):
                    continue
                if not analysis.dynamic_slots:
                    if settings.mode == MODE_TRANSFORMATION:
                        continue
                    combinations.append(
                        GenerationCombination(
                            pattern_id,
                            GenerationRule(
                                category="fixed",
                                source_form="",
                                target_form="",
                                target_label="",
                            ),
                        )
                    )
                    continue
                eligible_forms = set(compatibility_solver.eligible_form_names(
                    self.project, pattern_id, _analysis=analysis))
                # allowed_forms constrains the requested answer. A transformation
                # may start in the opposite register outside that target subset.
                source_forms = eligible_forms
                if settings.mode == MODE_TRANSFORMATION and pattern.allowed_forms:
                    source_pattern = replace(pattern, allowed_forms=())
                    source_analysis = self.shared_engine.analyze_pattern(source_pattern)
                    source_forms = set(compatibility_solver.eligible_form_names(
                        self.project, pattern_id, source_pattern, _analysis=source_analysis))
                combinations.extend(
                    GenerationCombination(pattern_id, rule)
                    for rule in self.build_generation_rules(settings, pattern_id, analysis=analysis)
                    if rule.target_form in eligible_forms
                    and (not rule.source_form or rule.source_form in source_forms)
                )
        if not combinations and not allow_empty:
            raise GrammarQuizError(
                "Bieżące ustawienia nie tworzą żadnej reguły quizu."
            )
        return combinations

    def capabilities(self, settings):
        """Union of selected patterns; a mode uses only its supported patterns.

        This is catalog analysis, not vocabulary generation or a persistent
        cache. The same combination builder governs UI and runtime validation.
        """
        if not settings.enabled_patterns:
            return dict(modes=(), directions=(), forms=(), styles=(), chains=False, numeric=False, dynamic=False)
        probe = replace(settings, word_chain_length=1, enabled_forms=list(FORM_GROUPS),
            plain_output=True, polite_output=True, polite_to_plain=True, plain_to_polite=True)
        all_standard = self._build_combinations(replace(probe, mode=MODE_POLISH_TO_JAPANESE), allow_empty=True)
        all_transform = self._build_combinations(replace(probe, mode=MODE_TRANSFORMATION), allow_empty=True)
        standard = [c for c in all_standard if c.rule.category == 'fixed' or c.rule.category in settings.enabled_forms]
        transform = [c for c in all_transform if c.rule.category in settings.enabled_forms]
        directions = set()
        styles = set()
        for c in transform:
            group = target_form_group(self.project, c.rule.target_form)
            if group:
                directions.add('polite_to_plain' if group[1] == 'plain' else 'plain_to_polite')
        for c in standard:
            group = target_form_group(self.project, c.rule.target_form)
            if group:
                styles.add(group[1] + '_output')
        active = transform if settings.mode == MODE_TRANSFORMATION and transform else standard
        analyses = [self.shared_engine.analyze_pattern(pid) for pid in {c.pattern_id for c in active}]
        return dict(modes=tuple(mode for mode, values in (
            (MODE_POLISH_TO_JAPANESE, standard), (MODE_TRANSFORMATION, transform)) if values),
            directions=tuple(sorted(directions)), styles=tuple(sorted(styles)),
            forms=tuple(name for name in FORM_GROUPS if any(c.rule.category == name for c in
                (all_transform if settings.mode == MODE_TRANSFORMATION and transform else all_standard))),
            chains=any(chain_slot(self.project, a) is not None for a in analyses),
            numeric=any(slot.number_range is not None and not slot.fixed_word_id and not slot.number_sets
                for a in analyses for slot in a.slots.values()),
            dynamic=any(a.dynamic_slots for a in analyses))

    def reconcile_settings(self, settings):
        """Repair only unsupported controls, retaining unrelated saved values."""
        capabilities = self.capabilities(settings)
        changed = bool(getattr(settings, '_filters_corrected', False))
        settings._filters_corrected = False
        if (not capabilities['modes'] and settings.enabled_forms and capabilities['forms']
                and not set(settings.enabled_forms).intersection(capabilities['forms'])):
            settings.enabled_forms = list(capabilities['forms'])
            capabilities = self.capabilities(settings)
            changed = True
        if capabilities['modes'] and settings.mode not in capabilities['modes']:
            settings.mode = capabilities['modes'][0]
            changed = True
            capabilities = self.capabilities(settings)
        transform = settings.mode == MODE_TRANSFORMATION
        options = ('polite_to_plain', 'plain_to_polite') if transform else ('plain_output', 'polite_output')
        available = capabilities['directions' if transform else 'styles']
        if available and not any(getattr(settings, name) for name in available):
            setattr(settings, available[0], True)
            changed = True
        for name in options:
            if available and name not in available and getattr(settings, name):
                setattr(settings, name, False)
                changed = True
        if not capabilities['chains'] and settings.word_chain_length > 1:
            settings.word_chain_length = 1
            changed = True
        notice = ''
        if changed:
            notice = ('Wybrane opcje nie są dostępne dla tych wzorców i form. Ustawiono dostępne opcje.'
                if self.language_context.ui_locale == 'pl' else
                'The selected options are unavailable for these patterns and forms. Supported options have been selected.')
        return capabilities, notice

    def choice_scope(
        self,
        settings: GrammarQuizSettings,
        pattern_id: str,
    ) -> ChoiceScope:
        """Build the shared solver scope for one effective sentence pattern."""

        if not settings.quantity_range_enabled:
            return ChoiceScope()
        analysis = self.shared_engine.analyze_pattern(pattern_id)
        numeric_range = NumericRangeScope(
            settings.quantity_range_min,
            settings.quantity_range_max,
        )
        return ChoiceScope(
            numeric_range_by_slot={
                slot_id: numeric_range
                for slot_id in analysis.word_slots
                if analysis.slots[slot_id].number_range is not None
                and slot_id not in analysis.fixed_words
                and not analysis.slots[slot_id].number_sets
            }
        )

    def _balanced_main_choice(self, candidates, dictionary, word_usage, recent_word_ids):
        """Scope session history without changing balanced_choice or public IDs.

        Bare IDs remain supported for callers supplying legacy per-pattern
        history. Sessions record dictionary-qualified keys instead.
        """
        usage = {
            item.id: word_usage.get((dictionary, item.id), word_usage.get(item.id, 0))
            for item in candidates
        } if word_usage else {}
        recent = [
            key[1] if isinstance(key, tuple) else key
            for key in recent_word_ids
            if not isinstance(key, tuple) or key[0] == dictionary
        ]
        return balanced_choice(candidates, usage, recent, self.rng)

    def _select_bindings(
        self,
        pattern_id: str,
        form_name: str,
        rules: Sequence[SlotFilterRule],
        word_usage: Mapping[_HistoryKey, int],
        recent_word_ids: Sequence[_HistoryKey],
        choice_scope: ChoiceScope,
    ) -> Optional[tuple[Dict[str, str], Dict[str, str]]]:
        analysis = self.shared_engine.analyze_pattern(pattern_id)
        main_slot = analysis.focus_slot or analysis.entity_slots[0]
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
            compatible = self.shared_engine.compatible(
                pattern_id,
                form_name=form_name,
                word_choices=word_choices,
                entity_choices=entity_choices,
                choice_scope=choice_scope,
            )
            if not compatible.form_names and not word_choices and not entity_choices:
                raise NoCompatibleChoices(f"Pattern '{pattern_id}' has no compatible words for form '{form_name}'.")
            candidate_values = compatible.words.get(slot, [])
            candidates = (
                [
                    word
                    for word in candidate_values
                    if _item_matches(
                        word,
                        slot_rules,
                        self.project.effective_entity_categories,
                    )
                ]
                if slot_rules else candidate_values
            )
            if not candidates:
                return None
            if isinstance(candidates, NumericRangeCandidates):
                selected = self.rng.choice(candidates)
            elif slot == analysis.focus_slot:
                selected = self._balanced_main_choice(
                    candidates,
                    analysis.slots[slot].dictionary,
                    word_usage,
                    recent_word_ids,
                )
            else:
                selected = self.rng.choice(candidates)
            word_choices[slot] = selected.id

        for slot in analysis.entity_slots:
            compatible = self.shared_engine.compatible(
                pattern_id,
                form_name=form_name,
                word_choices=word_choices,
                entity_choices=entity_choices,
                choice_scope=choice_scope,
            )
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
            selected = (
                self._balanced_main_choice(
                    candidates, analysis.slots[slot].dictionary,
                    word_usage, recent_word_ids,
                )
                if slot == main_slot else self.rng.choice(candidates)
            )
            entity_choices[slot] = selected.id
        return word_choices, entity_choices

    def generate_question(
        self,
        settings: GrammarQuizSettings,
        seen_keys: Optional[Set[str]] = None,
        preferred: Optional[GenerationCombination] = None,
        word_usage: Optional[Mapping[_HistoryKey, int]] = None,
        recent_word_ids: Optional[Sequence[_HistoryKey]] = None,
        remaining_questions=None,
    ) -> GrammarQuestion:
        rules = parse_slot_filter(settings.effective_word_filter())
        combinations = self.build_combinations(settings)
        if preferred is not None:
            combinations = [preferred] + [
                value for value in combinations if value != preferred
            ]
        seen_keys = seen_keys or set()
        rejected = []
        for attempt in range(16 if seen_keys else 128):
            check_cancelled()
            if not combinations:
                break
            combination = (
                preferred
                if preferred is not None and attempt == 0
                else self.rng.choice(combinations)
            )
            try:
                question = self._question_for_combination(
                    settings, combination, rules, word_usage or {}, recent_word_ids or (),
                )
            except NoCompatibleChoices as error:
                rejected.append(str(error))
                combinations = [value for value in combinations if value != combination]
                continue
            if question is not None and question.key not in seen_keys:
                return question
        remaining = remaining_questions if remaining_questions is not None else self.remaining_question_search(settings)
        for question in remaining:
            check_cancelled()
            if question.key not in seen_keys:
                return question
        if seen_keys:
            raise GrammarQuizExhausted("Wykorzystano wszystkie dostępne pytania.")
        if not combinations and rejected:
            raise GrammarQuizError("Brak zgodnych słów lub form. " + "; ".join(rejected))
        raise GrammarQuizError(
            "Nie udało się znaleźć kolejnego unikalnego pytania dla "
            "bieżących ustawień i filtrów."
        )

    def remaining_question_search(self, settings):
        """Lazy session-owned cursor: never replay already visited bindings."""
        rules = parse_slot_filter(settings.effective_word_filter())
        for combination in self.build_combinations(settings):
            yield from self._remaining_questions(settings, combination, rules)

    def _question_for_combination(
        self,
        settings: GrammarQuizSettings,
        combination: GenerationCombination,
        rules: Sequence[SlotFilterRule],
        word_usage: Mapping[_HistoryKey, int],
        recent_word_ids: Sequence[_HistoryKey],
    ) -> Optional[GrammarQuestion]:
        analysis = self.shared_engine.analyze_pattern(combination.pattern_id)
        choice_scope = self._statistics_choice_scope(settings, combination.pattern_id, analysis, rules)
        selected = self._select_bindings(
            combination.pattern_id,
            combination.rule.target_form,
            rules,
            word_usage,
            recent_word_ids,
            choice_scope,
        )
        if selected is None:
            return None
        completed = self.shared_engine.complete(
            combination.pattern_id,
            form_name=combination.rule.target_form,
            word_choices=selected[0],
            entity_choices=selected[1],
            choice_scope=choice_scope,
            rng=self.rng,
        )
        preview = self.shared_engine.preview(
            combination.pattern_id,
            form_name=completed.form_name,
            word_choices=completed.words,
            entity_choices=completed.entities,
            rng=self.rng,
        )

        return self._question_from_preview(settings, combination, preview)

    def _question_from_preview(self, settings, combination, preview, selected_chains=None):
        rendered = self._render_question(settings, combination, preview, selected_chains=selected_chains)
        if rendered is None:
            return None
        source_sentence, expected_answer, chains, context_question = rendered
        analysis = self.shared_engine.analyze_pattern(combination.pattern_id)
        main_slot = analysis.focus_slot or analysis.entity_slots[0]
        main_dictionary = analysis.slots[main_slot].dictionary
        if analysis.focus_slot:
            main_word = compatibility_solver.resolve_word_selection(
                self.project,
                main_dictionary,
                preview.words[main_slot],
            )
        else:
            main_word = self.project.entities[preview.entities[main_slot]]
        if main_word is None:
            return None
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
                combination.rule.source_form,
                source_sentence,
                expected_answer,
                preview.context_pool,
                preview.context_option,
                repr(tuple(sorted(preview.words.items()))),
                repr(tuple(sorted(preview.entities.items()))),
                repr(tuple((slot, tuple(ids)) for slot, ids in sorted(chains.items()))),
            )
        )
        context_translation, context_kana = selected_context_hint(
            self.project,
            preview,
            analysis=analysis,
        )
        vocabulary_hints = selected_vocabulary_hints(self.project, preview, analysis=analysis, word_chains=chains)
        if chains:
            bindings += ", " + ", ".join(f"{slot}=" + "+".join(ids) for slot, ids in chains.items())
        return GrammarQuestion(
            key=key,
            source_sentence=source_sentence,
            expected_answer=expected_answer,
            target_label=combination.rule.target_label,
            context_question=context_question if combination.rule.source_form else "",
            pattern_id=combination.pattern_id,
            target_form=combination.rule.target_form,
            source_form=combination.rule.source_form,
            word_id=main_word.id,
            _history_key=(main_dictionary, main_word.id),
            word_meaning=self.project.instruction_language.translation(main_word),
            word_kana=main_word.kana,
            word_kanji=main_word.kanji,
            hint_pairs=[(hint.translation, hint.kana) for hint in vocabulary_hints],
            vocabulary_hints=vocabulary_hints,
            bindings=bindings,
            context_translation=context_translation,
            context_kana=context_kana,
        )

    def _remaining_questions(self, settings, combination, rules):
        """Enumerate lazily only after repeated random collisions."""
        from itertools import permutations
        analysis = self.shared_engine.analyze_pattern(combination.pattern_id)
        scope = self._statistics_choice_scope(settings, combination.pattern_id, analysis, rules)
        for preview in iter_quiz_previews(self.shared_engine, combination.pattern_id,
                form_name=combination.rule.target_form, choice_scope=scope):
            matches = True
            for slot in (*analysis.word_slots, *analysis.entity_slots):
                item = (self.project.entities[preview.entities[slot]] if slot in analysis.entity_slots
                        else compatibility_solver.resolve_word_selection(self.project,
                            analysis.slots[slot].dictionary, preview.words[slot]))
                if item is None or not _item_matches(item, _rules_for_engine_slot(rules, analysis, slot),
                                                    self.project.effective_entity_categories):
                    matches = False
                    break
            if not matches:
                continue
            variants = ({},)
            if settings.word_chain_length > 1:
                slot, candidates = self._chain_candidates(settings, combination.pattern_id, preview, analysis=analysis)
                variants = ({slot: [word.id for word in prefix] + [preview.words[slot]]}
                            for prefix in permutations(candidates, settings.word_chain_length - 1))
            for chains in variants:
                check_cancelled()
                question = self._question_from_preview(settings, combination, preview, chains)
                if question is not None:
                    yield question

    def _hint_pairs(self, pattern_id: str, preview: object) -> List[tuple[str, str]]:
        return [(hint.translation, hint.kana)
                for hint in selected_vocabulary_hints(self.project, preview)]

    def _chain_candidates(self, settings, pattern_id, preview, candidate_cache=None, analysis=None, *, exclude_final=True):
        analysis = analysis or self.shared_engine.analyze_pattern(pattern_id)
        slot = chain_slot(self.project, analysis)
        if slot is None:
            raise GrammarQuizError("Ten wzorzec nie obsługuje łańcucha słów.")
        subject_slot = analysis.entity_for_adjective.get(slot)
        subject = self.project.entities.get(preview.entities.get(subject_slot, ""))
        cache_key = (pattern_id, subject.id if subject is not None else "")
        candidates = candidate_cache.get(cache_key) if candidate_cache is not None else None
        if candidates is None:
            rules = _rules_for_engine_slot(parse_slot_filter(settings.effective_word_filter()), analysis, slot)
            candidates = [word for word in compatibility_solver.base_word_candidates(
                self.project, slot, analysis, dynamic_form=preview.dynamic_form, check_form=False)
                if "connective" in word.forms
                and _item_matches(word, rules, self.project.effective_entity_categories)
                and (subject is None or compatibility_solver.adjective_matches(self.project, word, subject))]
            if candidate_cache is not None:
                candidate_cache[cache_key] = candidates
        return slot, ([word for word in candidates if word.id != preview.words[slot]] if exclude_final else candidates)

    def _chain_count(self, settings, pattern_id, preview, candidate_cache=None, analysis=None, *, subject_id=None):
        if settings.word_chain_length == 1:
            return 1
        import math
        analysis = analysis or self.shared_engine.analyze_pattern(pattern_id)
        slot_key = ('chain_slot', pattern_id)
        slot = candidate_cache.get(slot_key) if candidate_cache is not None else None
        if slot is None:
            slot = chain_slot(self.project, analysis)
            if candidate_cache is not None:
                candidate_cache[slot_key] = slot
        subject_slot = analysis.entity_for_adjective.get(slot)
        bound_subject = preview.entities.get(subject_slot, '')
        subject = bound_subject if subject_slot is None or subject_id is None else subject_id
        key = ('prefix_ids', pattern_id, subject)
        ids = candidate_cache.get(key) if candidate_cache is not None else None
        if ids is None:
            selected = (replace(preview, entities={**preview.entities, subject_slot: subject})
                        if subject != bound_subject else preview)
            _slot, candidates = self._chain_candidates(settings, pattern_id, selected, candidate_cache, analysis, exclude_final=False)
            ids = frozenset(word.id for word in candidates)
            if candidate_cache is not None:
                candidate_cache[key] = ids
        available = len(ids) - (preview.words[slot] in ids)
        count = settings.word_chain_length - 1
        return math.perm(available, count) if available >= count else 0

    def _render_question(self, settings, combination, preview, *, sample_chains=True, selected_chains=None, analysis=None):
        """Render both sides from identical bindings and context selections."""
        analysis = analysis or self.shared_engine.analyze_pattern(combination.pattern_id)
        chains = selected_chains or {}
        if selected_chains is None and settings.word_chain_length > 1:
            slot, candidates = self._chain_candidates(settings, combination.pattern_id, preview, analysis=analysis)
            count = settings.word_chain_length - 1
            if len(candidates) < count:
                return None
            prefix = self.rng.sample(candidates, count) if sample_chains else candidates[:count]
            chains[slot] = [w.id for w in prefix] + [preview.words[slot]]
        source, answer = preview.source, preview.answer
        if chains:
            source, answer = self.shared_engine.render_bound_pattern(
                combination.pattern_id, word_choices=preview.words, entity_choices=preview.entities,
                word_chains=chains, form_overrides=preview.forms,
                context_pool=preview.context_pool, context_option=preview.context_option)
        context_question = source
        if combination.rule.source_form:
            overrides = {}
            for slot in analysis.dynamic_slots:
                word = compatibility_solver.resolve_word_selection(self.project,
                    analysis.slots[slot].dictionary, preview.words[slot])
                source_form = word.forms.get(combination.rule.source_form)
                target_form = word.forms.get(preview.forms[slot])
                if source_form is None or target_form is None or source_form.context != target_form.context:
                    return None
                overrides[slot] = source_form.name
            if chains:
                _, source = self.shared_engine.render_bound_pattern(
                    combination.pattern_id, word_choices=preview.words, entity_choices=preview.entities,
                    word_chains=chains, form_overrides={**preview.forms, **overrides},
                    context_pool=preview.context_pool, context_option=preview.context_option)
            else:
                source = self.shared_engine.render_answer_with_forms(preview, overrides, analysis=analysis)
            if normalize_japanese(source) == normalize_japanese(answer):
                return None
        return source, answer, chains, context_question

    def _statistics_choice_scope(self, settings, pattern_id, analysis, rules):
        """Push lexical filters into the solver before rendering possibilities.

        Generated number ranges stay lazy. Fixed selections and generated
        numbers retain the final filter check in statistics().
        """
        scope = self.choice_scope(settings, pattern_id)
        allowed = dict(scope.allowed_by_slot)
        for slot in (*analysis.word_slots, *analysis.entity_slots):
            slot_rules = _rules_for_engine_slot(rules, analysis, slot)
            if not slot_rules:
                continue
            definition = analysis.slots[slot]
            if definition.number_range is not None:
                continue
            dictionary = definition.dictionary
            candidates = (
                self.project.entities.values() if slot in analysis.entity_slots
                else self.project.words.get(dictionary, {}).values()
            )
            allowed[slot] = frozenset(
                item.id for item in candidates
                if scope.allows(dictionary, slot, item.id)
                and _item_matches(item, slot_rules, self.project.effective_entity_categories)
            )
        return replace(scope, allowed_by_slot=allowed)

    def statistics(self, settings: GrammarQuizSettings) -> Dict[str, int]:
        rules = parse_slot_filter(settings.effective_word_filter())
        combinations = self.build_combinations(settings)
        possible = 0
        eligible_words: Set[tuple[str, str]] = set()
        active_patterns: Set[str] = set()
        scopes = {}
        chain_candidates = {}
        source_settings = replace(settings, word_chain_length=1)
        for combination_index, combination in enumerate(combinations):
            with progress_step(combination_index, len(combinations)):
                active_patterns.add(combination.pattern_id)
                analysis = self.shared_engine.analyze_pattern(combination.pattern_id)
                main_slot = analysis.focus_slot or analysis.entity_slots[0]
                main_dictionary = analysis.slots[main_slot].dictionary
                if combination.pattern_id not in scopes:
                    scopes[combination.pattern_id] = self._statistics_choice_scope(
                        settings, combination.pattern_id, analysis, rules,
                    )
                choice_scope = scopes[combination.pattern_id]
                counted = getattr(self.shared_engine, "iter_counted_previews", None)
                # Lexical scope is exact; generated numeric metadata filters
                # retain the post-render path instead of enumerating their range here.
                numeric_filters = any(_rules_for_engine_slot(rules, analysis, slot)
                    and analysis.slots[slot].number_range is not None for slot in analysis.word_slots)
                factor_context = chain_slot(self.project, analysis) is not None
                if counted is not None and not numeric_filters and (not rules or factor_context):
                    previews = counted(combination.pattern_id,
                        form_name=combination.rule.target_form, choice_scope=choice_scope,
                        factor_context=factor_context,
                        bindings_only=not combination.rule.source_form,
                        source_form=combination.rule.source_form)
                else:
                    # Older application hosts and post-render word filters keep
                    # the original exact path, including fixed-slot filtering.
                    previews = ((preview, 1, {}) for preview in iter_quiz_previews(
                        self.shared_engine, combination.pattern_id,
                        form_name=combination.rule.target_form, choice_scope=choice_scope))
                for preview, multiplicity, independent_entities in previews:
                    matches = True
                    for slot in analysis.word_slots:
                        dictionary = analysis.slots[slot].dictionary
                        word = compatibility_solver.resolve_word_selection(
                            self.project,
                            dictionary,
                            preview.words[slot],
                        )
                        if word is None:
                            matches = False
                            break
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
                        if combination.rule.source_form and self._render_question(source_settings, combination, preview, sample_chains=False, analysis=analysis) is None:
                            continue
                        # A factored noun domain may have different prefix
                        # vocabularies. Sum their exact chain counts, never use
                        # the representative noun's count for the whole domain.
                        noun_slot = next(iter(independent_entities), None) if factor_context else None
                        noun_ids = independent_entities.get(noun_slot, ()) if settings.word_chain_length > 1 else ()
                        chains_total = (sum(self._chain_count(settings, combination.pattern_id,
                            preview, chain_candidates, analysis, subject_id=value) for value in noun_ids)
                            if noun_ids else self._chain_count(settings, combination.pattern_id,
                                preview, chain_candidates, analysis))
                        if not chains_total:
                            continue
                        possible += (multiplicity // len(noun_ids) if noun_ids else multiplicity) * chains_total
                        selections = preview.words if analysis.focus_slot else preview.entities
                        eligible_words.update((main_dictionary, value) for value in
                            independent_entities.get(main_slot, (selections[main_slot],)))
        return {
            "possible": possible,
            "active_patterns": len(active_patterns),
            "eligible": len(eligible_words),
            "categories": len(self.project.noun_categories),
            "patterns": len(active_patterns),
            "words": len(eligible_words),
            "entities": len(self.project.entities),
        }

    def has_possible_question(self, settings: GrammarQuizSettings) -> bool:
        """Stop after the first assignment that runtime can render."""

        rules = parse_slot_filter(settings.effective_word_filter())
        combinations = self.build_combinations(settings)
        rejected = []
        for attempt in range(128):
            if not combinations:
                break
            combination = combinations[attempt % len(combinations)]
            try:
                question = self._question_for_combination(settings, combination, rules, {}, ())
            except NoCompatibleChoices:
                combinations = [value for value in combinations if value != combination]
                continue
            if question is not None:
                return True
        # The random budget selects an algorithm, never establishes emptiness.
        return next(self.remaining_question_search(settings), None) is not None


GrammarQuizSession = SentenceQuizSession
QUIZ_SETTINGS_CLASS = GrammarQuizSettings
QUIZ_ENGINE_CLASS = GrammarQuizEngine
QUIZ_SESSION_CLASS = GrammarQuizSession
SETTINGS_STORE_CLASS = SettingsStore
QUIZ_ERROR_CLASS = GrammarQuizError


def snapshot_quiz_policy():
    """Freeze this profile for one host without retaining mutable module state."""
    policy = SimpleNamespace(**{name: globals()[name] for name in __all__})
    policy.PATTERN_LABELS = dict(PATTERN_LABELS)
    policy.FILTER_OPTIONS = dict(FILTER_OPTIONS)
    policy.PATTERN_EXPANSIONS = dict(PATTERN_EXPANSIONS)

    class ProfileSettings(GrammarQuizSettings):
        supported_patterns = tuple(SUPPORTED_PATTERNS)
        pattern_labels = dict(PATTERN_LABELS)
        filter_options = dict(FILTER_OPTIONS)
        filter_defaults = dict(FILTER_DEFAULTS)
        filter_targets = dict(FILTER_TARGETS)

        def __post_init__(self):
            super().__post_init__()
            for key, values in self.filter_defaults.items():
                if values:
                    self.filter_selections.setdefault(key, list(values))

        @classmethod
        def from_dict(cls, values):
            from kotomi.application.quiz_filters import reconcile_selections
            selections, corrected = reconcile_selections(values.get('filter_selections', {}),
                                                         cls.filter_options, cls.filter_defaults)
            inactive = set(cls.filter_defaults) - set(cls.filter_options)
            original = values.get('filter_selections', {})
            selections.update({key: list(original[key]) for key in inactive if key in original})
            corrected = any(original.get(key) != selected for key, selected in selections.items() if key in original) or bool(set(original) - set(cls.filter_defaults))
            result = super().from_dict({**values, 'filter_selections': selections})
            result._filters_corrected = corrected
            return result

        def validate(self):
            from kotomi.application.quiz_filters import filter_label
            for key in self.filter_options:
                if not self.filter_selections.get(key):
                    caption = filter_label(key, lambda value: value, self.filter_targets)
                    raise GrammarQuizError(f'Choose at least one value for {caption}.')
            super().validate()
            for key, values in self.filter_selections.items():
                if key not in self.filter_defaults or (key in self.filter_options and not set(values) <= set(self.filter_options[key])):
                    raise GrammarQuizError('The vocabulary filter selection is no longer allowed. Reopen quiz settings.')

    class ProfileEngine(GrammarQuizEngine):
        profile_expansions = dict(PATTERN_EXPANSIONS)

    class ProfileStore(SettingsStore):
        settings_class = ProfileSettings
        legacy_filename = {"verbs": "verb_quiz_settings.xml", "adjectives": "adjective_quiz_settings.xml",
                           "availability": "availability_quiz_settings.xml"}.get(ACTIVE_QUIZ_ID, "")

    policy.QUIZ_SETTINGS_CLASS = ProfileSettings
    policy.QUIZ_ENGINE_CLASS = ProfileEngine
    policy.SETTINGS_STORE_CLASS = ProfileStore
    policy.SettingsStore = ProfileStore
    filename = SETTINGS_FILENAME
    policy.quiz_settings_path = lambda: settings_path(INSTALL_ROOT, filename)
    return policy


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
    "SCRIPT_DIR",
    "SETTINGS_FILENAME",
    "SETTINGS_STORE_CLASS",
    "SUPPORTED_PATTERNS",
    "PATTERN_EXPANSIONS",
    "SUPPORTS_NUMERIC_QUANTITY_RANGE",
    "FILTER_OPTIONS",
    "FILTER_DEFAULTS",
    "FILTER_TARGETS",
    "FILTER_VALUE_LABELS",
    "SUPPORTS_WORD_CHAINS",
    "MOBILE_DIRECTION_TOGGLES",
    "MODE_TRANSFORMATION",
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
    "target_form_group",
]
