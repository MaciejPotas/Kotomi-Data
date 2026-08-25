"""Platform-neutral settings and generation logic for the Adjectives quiz.

This module intentionally imports no Kivy or Tkinter classes. Desktop and
Mobile presentations use the same settings, engine, session, question, and
result models from here.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
import os
from pathlib import Path
import random
import re
import sys
from typing import Dict, Iterable, List, Mapping, Optional, Sequence


SCRIPT_DIR = Path(__file__).resolve().parent
INSTALL_ROOT = SCRIPT_DIR.parents[1]
REPOSITORY_DATA_DIR = INSTALL_ROOT / "data"
if str(INSTALL_ROOT) not in sys.path:
    sys.path.insert(0, str(INSTALL_ROOT))

from kotomi_core.project import (
    ContextOption,
    ContextPool,
    Entity,
    Form,
    ProjectError,
    SentencePattern,
    Word,
)
from kotomi_core.generation import SharedQuizEngine, normalize_answer
from kotomi_core.settings_xml import load_settings, save_settings
from kotomi_ui.mobile import (
    DEFAULT_MOBILE_BUTTON_SCALE,
    validate_mobile_button_scale,
)


PROJECT_ENVIRONMENT_VARIABLE = "JAPANESE_QUIZ_PROJECT"
SETTINGS_FILENAME = "adjective_quiz_settings.xml"

MODE_TRANSFORMATION = "transformation"
MODE_POLISH_TO_JAPANESE = "polish_to_japanese"

MODE_LABELS = {
    MODE_POLISH_TO_JAPANESE: "Napisz zdanie po japońsku",
    MODE_TRANSFORMATION: "Zmień japońskie zdanie",
}
LABEL_TO_MODE = {label: mode for mode, label in MODE_LABELS.items()}

PATTERN_LABELS = {
    "adjective_predicate": "Po rzeczowniku z partykułą wa",
    "adjective_simple": "Proste zdanie wskazujące",
    "adjective_attributive": "Przymiotnik przed rzeczownikiem",
}
SUPPORTED_PATTERNS = tuple(PATTERN_LABELS)

FORM_GROUPS = {
    "nonpast": {
        "label": "Nieprzeszła twierdząca",
        "plain": "predicate_plain_nonpast",
        "polite": "predicate_polite_nonpast",
    },
    "negative": {
        "label": "Nieprzeszła przecząca",
        "plain": "predicate_plain_negative",
        "polite": "predicate_polite_negative",
    },
    "past": {
        "label": "Przeszła twierdząca",
        "plain": "predicate_plain_past",
        "polite": "predicate_polite_past",
    },
    "past_negative": {
        "label": "Przeszła przecząca",
        "plain": "predicate_plain_past_negative",
        "polite": "predicate_polite_past_negative",
    },
}

COPULA_FORM_GROUPS = {
    "nonpast": {"plain": "dictionary", "polite": "polite_nonpast"},
    "negative": {"plain": "plain_negative", "polite": "polite_negative"},
    "past": {"plain": "past_plain", "polite": "past_polite"},
    "past_negative": {
        "plain": "past_negative_plain",
        "polite": "past_negative_polite",
    },
}

STYLE_LABELS = {"plain": "potoczny", "polite": "uprzejmy"}

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
    """Raised for invalid settings or an unavailable adjective question."""


@dataclass
class AdjectiveQuizSettings:
    """Persistent settings corresponding to the C++ adjective widget."""

    mode: str = MODE_POLISH_TO_JAPANESE
    polite_to_plain: bool = True
    plain_to_polite: bool = False
    polite_output: bool = True
    plain_output: bool = True
    enabled_forms: List[str] = field(default_factory=lambda: list(FORM_GROUPS))
    enabled_patterns: List[str] = field(
        default_factory=lambda: list(SUPPORTED_PATTERNS)
    )
    enable_i_adjectives: bool = True
    enable_na_adjectives: bool = True
    adjective_count: int = 1
    word_filter: str = ""
    question_count: int = 25
    number_of_tries: int = 1
    random_order: bool = True
    auto_advance_seconds: float = 100.0
    font_scale: float = 1.0
    mobile_button_scale: float = DEFAULT_MOBILE_BUTTON_SCALE

    @classmethod
    def from_dict(cls, values: Mapping[str, object]) -> "AdjectiveQuizSettings":
        defaults = cls()
        settings = cls(
            mode=str(values.get("mode", defaults.mode)),
            polite_to_plain=bool(values.get("polite_to_plain", defaults.polite_to_plain)),
            plain_to_polite=bool(values.get("plain_to_polite", defaults.plain_to_polite)),
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
            enable_i_adjectives=bool(
                values.get("enable_i_adjectives", defaults.enable_i_adjectives)
            ),
            enable_na_adjectives=bool(
                values.get("enable_na_adjectives", defaults.enable_na_adjectives)
            ),
            adjective_count=_safe_int(values.get("adjective_count"), defaults.adjective_count),
            word_filter=str(values.get("word_filter", defaults.word_filter)),
            question_count=_safe_int(values.get("question_count"), defaults.question_count),
            number_of_tries=1,
            random_order=True,
            auto_advance_seconds=_safe_float(
                values.get("auto_advance_seconds"), defaults.auto_advance_seconds
            ),
            font_scale=_safe_float(values.get("font_scale"), defaults.font_scale),
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
        if self.mode not in MODE_LABELS:
            raise MobileQuizError(f"Nieznany tryb quizu: {self.mode}")
        if not self.enabled_forms:
            raise MobileQuizError("Wybierz co najmniej jedną formę.")
        if not self.enabled_patterns:
            raise MobileQuizError("Wybierz co najmniej jeden wzorzec zdania.")
        if not self.enable_i_adjectives and not self.enable_na_adjectives:
            raise MobileQuizError("Wybierz przymiotniki typu i i/lub na.")
        if self.mode == MODE_TRANSFORMATION:
            if not self.polite_to_plain and not self.plain_to_polite:
                raise MobileQuizError("Wybierz co najmniej jeden kierunek transformacji.")
        elif not self.polite_output and not self.plain_output:
            raise MobileQuizError("Wybierz co najmniej jeden styl odpowiedzi.")
        if not 1 <= self.adjective_count <= 3:
            raise MobileQuizError("Liczba przymiotników musi mieścić się w zakresie 1–3.")
        if not 1 <= self.question_count <= 200:
            raise MobileQuizError("Liczba pytań musi mieścić się w zakresie 1–200.")
        if not 0.0 <= self.auto_advance_seconds <= 600.0:
            raise MobileQuizError("Automatyczne przejście musi mieścić się w zakresie 0–600 s.")
        if not 0.7 <= self.font_scale <= 1.6:
            raise MobileQuizError("Rozmiar tekstu musi mieścić się w zakresie 70–160%.")
        try:
            validate_mobile_button_scale(self.mobile_button_scale)
        except (TypeError, ValueError) as exception:
            raise MobileQuizError(str(exception)) from exception
        parse_word_filter(self.word_filter)

    def summary(self) -> str:
        forms = ", ".join(FORM_GROUPS[name]["label"] for name in self.enabled_forms)
        adjective_types = []
        if self.enable_i_adjectives:
            adjective_types.append("i")
        if self.enable_na_adjectives:
            adjective_types.append("na")
        return (
            f"{MODE_LABELS[self.mode]}\n"
            f"Pytania: {self.question_count}, przymiotniki w zdaniu: {self.adjective_count}\n"
            f"Typy: {' + '.join(adjective_types)}, formy: {forms}\n"
            f"Rozmiar tekstu: {round(self.font_scale * 100)}%, "
            f"przyciski: {round(self.mobile_button_scale * 100)}%"
        )


@dataclass(frozen=True)
class WordFilterRule:
    field: str
    values: tuple[str, ...]


@dataclass(frozen=True)
class GenerationRule:
    category: str
    source_polite: bool
    target_polite: bool
    has_source_form: bool
    target_label: str


@dataclass
class QuestionSpace:
    pattern: SentencePattern
    rule: GenerationRule
    final_adjective: Word
    prefix_candidates: List[Word]
    source_form: str
    target_form: str
    context_pool: ContextPool
    subject: Optional[Entity] = None
    copula: Optional[Word] = None
    source_copula_form: str = ""
    target_copula_form: str = ""
    permutation_count: int = 0
    question_count: int = 0


@dataclass
class AdjectiveQuestion:
    key: str
    source_sentence: str
    expected_answer: str
    target_label: str
    context_question: str
    pattern_id: str
    target_form: str
    source_form: str
    adjective_ids: str
    word_meaning: str
    word_kana: str
    word_kanji: str
    adjective_count: int
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
    return normalize_answer(text)



def parse_word_filter(text: str) -> List[WordFilterRule]:
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
            value.strip().strip("\"'").casefold()
            for value in values_text.split(",")
            if value.strip().strip("\"'")
        )
        if field_name not in FILTER_FIELDS:
            raise MobileQuizError(f"Nieznane pole filtra „{field_name}”.")
        if not values:
            raise MobileQuizError(f"Filtr „{field_name}” nie zawiera wartości.")
        rules.append(WordFilterRule(field_name, values))
    return rules


def word_matches_filter(word: Word, rules: Iterable[WordFilterRule]) -> bool:
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
        field_name = "dictionary_id" if rule.field == "dictionary" else rule.field
        value = str(getattr(word, field_name, "") or "").casefold()
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
    searched = "\n".join(str(candidate) for candidate in candidates if candidate is not None)
    raise MobileQuizError("Nie znaleziono quiz_project.xml. Sprawdzone lokalizacje:\n" + searched)


class SettingsStore:
    def __init__(self, path: Path) -> None:
        self.path = path

    def load(self) -> AdjectiveQuizSettings:
        if not self.path.exists():
            return AdjectiveQuizSettings()
        try:
            return AdjectiveQuizSettings.from_dict(load_settings(self.path))
        except (OSError, ValueError):
            return AdjectiveQuizSettings()

    def save(self, settings: AdjectiveQuizSettings) -> None:
        settings.validate()
        save_settings(self.path, asdict(settings))


class AdjectiveQuizEngine:
    """Mobile policy layer that mirrors AdjectiveSentenceQuizWidget."""

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

    def reload(self) -> None:
        self.shared_engine.reload()
        self.project = self.shared_engine.project
        self._validate_project()

    def _validate_project(self) -> None:
        issues = self.project.validate()
        if issues:
            raise MobileQuizError("\n".join(issues))
        for dictionary_id in ("adjectives", "copulas"):
            if dictionary_id not in self.project.words:
                raise MobileQuizError(f"Brak słownika XML: {dictionary_id}")
        for pattern_id in SUPPORTED_PATTERNS:
            if pattern_id not in self.project.patterns:
                raise MobileQuizError(f"Brak wzorca zdania: {pattern_id}")

    def build_generation_rules(
        self,
        settings: AdjectiveQuizSettings,
    ) -> List[GenerationRule]:
        settings.validate()
        rules: List[GenerationRule] = []
        if settings.mode == MODE_TRANSFORMATION:
            directions = (
                (settings.polite_to_plain, True, False),
                (settings.plain_to_polite, False, True),
            )
            for enabled, source_polite, target_polite in directions:
                if not enabled:
                    continue
                for category in settings.enabled_forms:
                    rules.append(
                        GenerationRule(
                            category=category,
                            source_polite=source_polite,
                            target_polite=target_polite,
                            has_source_form=True,
                            target_label=self._target_label(category, target_polite),
                        )
                    )
        else:
            styles = (
                (settings.plain_output, False),
                (settings.polite_output, True),
            )
            for enabled, target_polite in styles:
                if not enabled:
                    continue
                for category in settings.enabled_forms:
                    rules.append(
                        GenerationRule(
                            category=category,
                            source_polite=target_polite,
                            target_polite=target_polite,
                            has_source_form=False,
                            target_label=self._target_label(category, target_polite),
                        )
                    )
        return rules

    @staticmethod
    def _target_label(category: str, polite: bool) -> str:
        return (
            f"{str(FORM_GROUPS[category]['label']).lower()}, "
            f"styl {STYLE_LABELS['polite' if polite else 'plain']}"
        )

    def build_spaces(self, settings: AdjectiveQuizSettings) -> List[QuestionSpace]:
        settings.validate()
        rules = self.build_generation_rules(settings)
        filters = parse_word_filter(settings.word_filter)
        adjectives = list(self.project.words["adjectives"].values())
        spaces: List[QuestionSpace] = []
        prefix_count = settings.adjective_count - 1

        if "adjective_predicate" in settings.enabled_patterns:
            pattern = self.project.patterns["adjective_predicate"]
            for rule in rules:
                source_form, target_form = self._finite_forms(rule)
                for subject in self.project.entities.values():
                    prefix_base = self._prefix_candidates(settings, filters, subject)
                    for final in adjectives:
                        if not self._adjective_eligible(final, settings, filters):
                            continue
                        if not self._entity_matches_adjective(subject, final):
                            continue
                        if source_form not in final.forms or target_form not in final.forms:
                            continue
                        pool = self._context_pool(
                            final.forms[source_form], final.forms[target_form]
                        )
                        if pool is None:
                            continue
                        self._append_space(
                            spaces,
                            QuestionSpace(
                                pattern=pattern,
                                rule=rule,
                                final_adjective=final,
                                prefix_candidates=[word for word in prefix_base if word.id != final.id],
                                source_form=source_form,
                                target_form=target_form,
                                context_pool=pool,
                                subject=subject,
                            ),
                            prefix_count,
                        )

        if "adjective_simple" in settings.enabled_patterns:
            pattern = self.project.patterns["adjective_simple"]
            prefix_base = self._prefix_candidates(settings, filters, None)
            for rule in rules:
                source_form, target_form = self._finite_forms(rule)
                for final in adjectives:
                    if not self._adjective_eligible(final, settings, filters):
                        continue
                    if source_form not in final.forms or target_form not in final.forms:
                        continue
                    pool = self._context_pool(
                        final.forms[source_form], final.forms[target_form]
                    )
                    if pool is None:
                        continue
                    self._append_space(
                        spaces,
                        QuestionSpace(
                            pattern=pattern,
                            rule=rule,
                            final_adjective=final,
                            prefix_candidates=[word for word in prefix_base if word.id != final.id],
                            source_form=source_form,
                            target_form=target_form,
                            context_pool=pool,
                        ),
                        prefix_count,
                    )

        if "adjective_attributive" in settings.enabled_patterns:
            pattern = self.project.patterns["adjective_attributive"]
            for rule in rules:
                source_copula, target_copula = self._copula_forms(rule)
                for copula in self.project.words["copulas"].values():
                    if source_copula not in copula.forms or target_copula not in copula.forms:
                        continue
                    for subject in self.project.entities.values():
                        prefix_base = self._prefix_candidates(settings, filters, subject)
                        for final in adjectives:
                            if not self._adjective_eligible(final, settings, filters):
                                continue
                            if not self._entity_matches_adjective(subject, final):
                                continue
                            if "attributive_nonpast" not in final.forms:
                                continue
                            pool = self._context_pool(
                                final.forms["attributive_nonpast"],
                                final.forms["attributive_nonpast"],
                                copula.forms[source_copula],
                                copula.forms[target_copula],
                            )
                            if pool is None:
                                continue
                            before_noun_rule = GenerationRule(
                                category=rule.category,
                                source_polite=rule.source_polite,
                                target_polite=rule.target_polite,
                                has_source_form=rule.has_source_form,
                                target_label=rule.target_label + ", przymiotnik przed rzeczownikiem",
                            )
                            self._append_space(
                                spaces,
                                QuestionSpace(
                                    pattern=pattern,
                                    rule=before_noun_rule,
                                    final_adjective=final,
                                    prefix_candidates=[word for word in prefix_base if word.id != final.id],
                                    source_form="attributive_nonpast",
                                    target_form="attributive_nonpast",
                                    context_pool=pool,
                                    subject=subject,
                                    copula=copula,
                                    source_copula_form=source_copula,
                                    target_copula_form=target_copula,
                                ),
                                prefix_count,
                            )
        return spaces

    @staticmethod
    def _append_space(
        spaces: List[QuestionSpace],
        space: QuestionSpace,
        prefix_count: int,
    ) -> None:
        permutations = AdjectiveQuizEngine.permutation_count(
            len(space.prefix_candidates), prefix_count
        )
        context_count = len(space.context_pool.options)
        if permutations <= 0 or context_count <= 0:
            return
        space.permutation_count = permutations
        space.question_count = permutations * context_count
        spaces.append(space)

    def _adjective_eligible(
        self,
        adjective: Word,
        settings: AdjectiveQuizSettings,
        filters: Iterable[WordFilterRule],
    ) -> bool:
        type_enabled = (
            adjective.type == "i_adjective" and settings.enable_i_adjectives
        ) or (
            adjective.type == "na_adjective" and settings.enable_na_adjectives
        )
        return type_enabled and word_matches_filter(adjective, filters)

    def _prefix_candidates(
        self,
        settings: AdjectiveQuizSettings,
        filters: Iterable[WordFilterRule],
        subject: Optional[Entity],
    ) -> List[Word]:
        result: List[Word] = []
        for adjective in self.project.words["adjectives"].values():
            if not self._adjective_eligible(adjective, settings, filters):
                continue
            if "connective" not in adjective.forms:
                continue
            if subject is not None and not self._entity_matches_adjective(subject, adjective):
                continue
            result.append(adjective)
        return sorted(result, key=lambda word: (word.kana, word.id))

    def _entity_matches_adjective(self, entity: Entity, adjective: Word) -> bool:
        return self.shared_engine.adjective_matches(entity, adjective)

    @staticmethod
    def _finite_forms(rule: GenerationRule) -> tuple[str, str]:
        group = FORM_GROUPS[rule.category]
        target = str(group["polite" if rule.target_polite else "plain"])
        source = (
            str(group["polite" if rule.source_polite else "plain"])
            if rule.has_source_form
            else target
        )
        return source, target

    @staticmethod
    def _copula_forms(rule: GenerationRule) -> tuple[str, str]:
        group = COPULA_FORM_GROUPS[rule.category]
        target = str(group["polite" if rule.target_polite else "plain"])
        source = (
            str(group["polite" if rule.source_polite else "plain"])
            if rule.has_source_form
            else target
        )
        return source, target

    def _context_pool(self, *forms: Form) -> Optional[ContextPool]:
        context = "none"
        for form in forms:
            form_context = form.context or "none"
            if context == "none":
                context = form_context
            elif form_context != "none" and form_context != context:
                return None
        return self.project.contexts.get(context)

    @staticmethod
    def permutation_count(candidate_count: int, selected_count: int) -> int:
        if selected_count > candidate_count:
            return 0
        result = 1
        for index in range(selected_count):
            result *= candidate_count - index
        return result

    def statistics(self, settings: AdjectiveQuizSettings) -> Dict[str, int]:
        spaces = self.build_spaces(settings)
        return {
            "words": len(self.project.words["adjectives"]),
            "patterns": len(SUPPORTED_PATTERNS),
            "active_patterns": len(settings.enabled_patterns),
            "entities": len(self.project.entities),
            "categories": len(self.project.noun_categories),
            "eligible": len({space.final_adjective.id for space in spaces}),
            "spaces": len(spaces),
            "possible": sum(space.question_count for space in spaces),
        }

    def generate_question(self, settings: AdjectiveQuizSettings) -> AdjectiveQuestion:
        spaces = self.build_spaces(settings)
        total = sum(space.question_count for space in spaces)
        if total <= 0:
            raise MobileQuizError("Brak pytań dla bieżących ustawień i filtra.")
        for _attempt in range(20):
            question = self._question_from_index(spaces, self.rng.randrange(total), settings)
            if question is not None:
                return question
        raise MobileQuizError("Nie udało się wygenerować różniącej się pary zdań.")

    def build_questions(self, settings: AdjectiveQuizSettings) -> List[AdjectiveQuestion]:
        spaces = self.build_spaces(settings)
        total = sum(space.question_count for space in spaces)
        if total <= 0:
            raise MobileQuizError("Brak pytań dla bieżących ustawień i filtra.")
        requested = min(total, settings.question_count)
        indices = (
            self.rng.sample(range(total), requested)
            if settings.random_order
            else list(range(requested))
        )
        questions: List[AdjectiveQuestion] = []
        for index in indices:
            question = self._question_from_index(spaces, index, settings)
            if question is not None:
                questions.append(question)
        if not questions:
            raise MobileQuizError("Nie udało się wygenerować pytań dla bieżących ustawień.")
        return questions

    def _question_from_index(
        self,
        spaces: Sequence[QuestionSpace],
        global_index: int,
        settings: AdjectiveQuizSettings,
    ) -> Optional[AdjectiveQuestion]:
        selected: Optional[QuestionSpace] = None
        local_index = global_index
        for space in spaces:
            if local_index < space.question_count:
                selected = space
                break
            local_index -= space.question_count
        if selected is None:
            return None
        options = list(selected.context_pool.options.values())
        context_count = len(options)
        permutation_rank = local_index // context_count
        context_option = options[local_index % context_count]
        prefixes = self._unrank_prefix(
            selected.prefix_candidates,
            settings.adjective_count - 1,
            permutation_rank,
        )
        chain = prefixes + [selected.final_adjective]
        target_question, target_answer = self._render_pattern(
            selected,
            chain,
            selected.target_form,
            selected.target_copula_form,
            context_option,
        )
        source_answer = ""
        if settings.mode == MODE_TRANSFORMATION:
            _source_question, source_answer = self._render_pattern(
                selected,
                chain,
                selected.source_form,
                selected.source_copula_form,
                context_option,
            )
            if normalize_japanese(source_answer) == normalize_japanese(target_answer):
                return None
        source_sentence = (
            source_answer if settings.mode == MODE_TRANSFORMATION else target_question
        )
        ids = " + ".join(word.id for word in chain)
        source_name = (
            (
                "attributive_nonpast + " + selected.source_copula_form
                if selected.source_copula_form
                else selected.source_form
            )
            if settings.mode == MODE_TRANSFORMATION
            else "source_language"
        )
        target_name = (
            "attributive_nonpast + " + selected.target_copula_form
            if selected.target_copula_form
            else selected.target_form
        )
        bindings = []
        if selected.subject is not None:
            bindings.append("subject=" + selected.subject.id)
        bindings.append("adjectives=" + ids)
        if selected.copula is not None:
            bindings.append("copula=" + selected.copula.id)
        key = (
            f"{selected.pattern.id}:{selected.subject.id if selected.subject else 'no_subject'}:"
            f"{ids}:{context_option.id}:{source_name}->{target_name}:"
            f"{selected.copula.id if selected.copula else 'no_copula'}"
        )
        return AdjectiveQuestion(
            key=key,
            source_sentence=source_sentence,
            expected_answer=target_answer,
            target_label=selected.rule.target_label,
            context_question=(
                target_question if settings.mode == MODE_TRANSFORMATION else ""
            ),
            pattern_id=selected.pattern.id,
            target_form=target_name,
            source_form=source_name,
            adjective_ids=ids,
            word_meaning=" + ".join(word.translation for word in chain),
            word_kana=" + ".join(word.kana for word in chain),
            word_kanji=" + ".join(word.kanji for word in chain),
            adjective_count=len(chain),
            bindings="; ".join(bindings),
            context_translation=str(
                context_option.translation or ""
            ).strip(),
            context_kana=str(context_option.kana or "").strip(),
        )

    @classmethod
    def _unrank_prefix(
        cls,
        candidates: Sequence[Word],
        prefix_count: int,
        rank: int,
    ) -> List[Word]:
        result: List[Word] = []
        remaining = list(candidates)
        for position in range(prefix_count):
            positions_after = prefix_count - position - 1
            block_size = cls.permutation_count(len(remaining) - 1, positions_after)
            selected_index = rank // block_size if block_size else 0
            if selected_index >= len(remaining):
                return []
            result.append(remaining.pop(selected_index))
            if block_size:
                rank %= block_size
        return result

    def _render_pattern(
        self,
        space: QuestionSpace,
        chain: Sequence[Word],
        final_form: str,
        copula_form: str,
        context_option: ContextOption,
    ) -> tuple[str, str]:
        analysis = self.shared_engine.analyze_pattern(space.pattern)
        adjective_slot = next(
            slot for slot in analysis.word_slots
            if analysis.slots[slot].dictionary == "adjectives"
        )
        word_choices: Dict[str, str] = {}
        form_overrides = {adjective_slot: final_form}
        if space.copula is not None:
            copula_slot = next(
                slot for slot in analysis.word_slots
                if analysis.slots[slot].dictionary == "copulas"
            )
            word_choices[copula_slot] = space.copula.id
            form_overrides[copula_slot] = copula_form
        entity_choices: Dict[str, str] = {}
        if space.subject is not None:
            noun_slot = analysis.entity_slots[0]
            entity_choices[noun_slot] = space.subject.id
        return self.shared_engine.render_bound_pattern(
            space.pattern.id,
            word_choices=word_choices,
            entity_choices=entity_choices,
            word_chains={adjective_slot: [word.id for word in chain]},
            form_overrides=form_overrides,
            context_pool=space.context_pool.id,
            context_option=context_option.id,
        )

class AdjectiveQuizSession:
    def __init__(
        self,
        engine: AdjectiveQuizEngine,
        settings: AdjectiveQuizSettings,
    ) -> None:
        settings.validate()
        self.engine = engine
        self.settings = settings
        self.questions = engine.build_questions(settings)
        self.current_index = -1
        self.current_question: Optional[AdjectiveQuestion] = None
        self.current_try = 0
        self.correct_answers = 0
        self.wrong_answers = 0
        self.accepted_answers = 0
        self.waiting_for_next = False
        self.current_outcome = ""

    @property
    def complete(self) -> bool:
        return self.current_index + 1 >= len(self.questions)

    def next_question(self) -> Optional[AdjectiveQuestion]:
        if self.current_question is not None and not self.waiting_for_next:
            return self.current_question
        next_index = self.current_index + 1
        if next_index >= len(self.questions):
            self.current_index = len(self.questions)
            self.current_question = None
            return None
        self.current_index = next_index
        self.current_question = self.questions[next_index]
        self.current_try = 0
        self.waiting_for_next = False
        self.current_outcome = ""
        return self.current_question

    def submit(self, answer: str) -> SubmissionResult:
        question = self.current_question
        if question is None:
            return SubmissionResult("idle", "Brak aktywnego pytania.")
        if self.waiting_for_next:
            return SubmissionResult("waiting", "To pytanie jest już zakończone.", question.expected_answer)
        if normalize_japanese(answer) == normalize_japanese(question.expected_answer):
            self.correct_answers += 1
            self.waiting_for_next = True
            self.current_outcome = "correct"
            return SubmissionResult("correct", "Dobrze!", question.expected_answer)
        self.current_try += 1
        if self.current_try >= self.settings.number_of_tries:
            self.wrong_answers += 1
            self.waiting_for_next = True
            self.current_outcome = "wrong"
            return SubmissionResult("wrong", "Niepoprawnie.", question.expected_answer)
        return SubmissionResult(
            "retry",
            f"Niepoprawnie. Spróbuj ponownie. Próba {self.current_try}/{self.settings.number_of_tries}.",
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
