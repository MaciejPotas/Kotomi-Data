from __future__ import annotations

from pathlib import Path
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
FORM_TRANSLATION = "{copula[form, agree:@item, case:@item].translation}"
EXPECTED_QUESTIONS = {
    "Pytanie który + rzeczownik": (
        "{interrogative[asks_for:choice_modifier, agree:@item, case:@item].translation} "
        "{noun@item[case:nominative]} to "
        "{copula[form, agree:@item, case:@item].translation}?"
    ),
    "Pytanie o rodzaj": (
        "{interrogative[asks_for:kind, agree:@item, case:@item].translation} to "
        "{copula[form, agree:@item, case:@item].translation} "
        "{noun@item[case:nominative]}?"
    ),
    "Pytanie czyj": (
        "{interrogative[asks_for:possessor, agree:@item, case:@item].translation} "
        "{noun@item[case:nominative]} to "
        "{copula[form, agree:@item, case:@item].translation}?"
    ),
    "Pytanie jak": (
        "{interrogative[asks_for:manner, agree:@item, case:@item].translation} "
        "{copula[form, agree:@item, case:@item].translation} "
        "{noun@item[case:nominative]}?"
    ),
}
EXPECTED_STRUCTURAL_QUESTIONS = {
    "Pytanie o rzecz": (
        "{interrogative[id:nani].translation} "
        "{context.translation}{verb[role:object, form].translation}?"
    ),
    "Pytanie ile osób": (
        "Ile osób jest {noun[category:place, relation:location].phrase}?"
    ),
    "Pytanie ile kosztuje": (
        "{interrogative[asks_for:price, agree:@item, case:@item].translation} "
        "{noun@item[category:purchasable, case:nominative]}?"
    ),
}
EXPECTED_COPULA_TRANSLATIONS = {
    "dictionary": "jest",
    "polite_nonpast": "jest",
    "plain_negative": "nie jest",
    "polite_negative": "nie jest",
    "past_plain": "był",
    "past_polite": "był",
    "past_negative_plain": "nie był",
    "past_negative_polite": "nie był",
}


def validate_question_prompts() -> None:
    maps_root = ET.parse(ROOT / "patterns" / "sentence_maps.xml").getroot()
    patterns = {
        str(node.get("id", "")): node
        for node in maps_root.findall("./sentence_patterns/sentence_pattern")
    }

    for pattern_id, expected_question in EXPECTED_QUESTIONS.items():
        node = patterns.get(pattern_id)
        if node is None:
            raise AssertionError(f"Missing audited question pattern: {pattern_id}")
        question = node.findtext("question", default="")
        answer = node.findtext("answer", default="")
        if question != expected_question:
            raise AssertionError(
                f"{pattern_id} source prompt changed unexpectedly: {question!r}"
            )
        if FORM_TRANSLATION not in question:
            raise AssertionError(
                f"{pattern_id} must render the selected copula form in Polish"
            )
        if "{copula[form]}" not in answer:
            raise AssertionError(
                f"{pattern_id} must render the same selected copula form in Japanese"
            )
    for pattern_id, expected_question in EXPECTED_STRUCTURAL_QUESTIONS.items():
        node = patterns.get(pattern_id)
        if node is None:
            raise AssertionError(f"Missing audited question pattern: {pattern_id}")
        question = node.findtext("question", default="")
        if question != expected_question:
            raise AssertionError(
                f"{pattern_id} source prompt changed unexpectedly: {question!r}"
            )


def validate_copula_translations() -> None:
    root = ET.parse(ROOT / "dictionaries" / "copulas.xml").getroot()
    word = root.find("./words/word[@id='da']")
    if word is None:
        raise AssertionError("Missing canonical copula 'da'")
    forms = {
        str(node.get("ref", "")): str(node.get("translation", ""))
        for node in word.findall("./forms/form")
    }
    for form_name, expected_translation in EXPECTED_COPULA_TRANSLATIONS.items():
        actual = forms.get(form_name)
        if actual != expected_translation:
            raise AssertionError(
                f"Copula {form_name} translation must be "
                f"{expected_translation!r}, found {actual!r}"
            )


def main() -> None:
    validate_question_prompts()
    validate_copula_translations()
    print("Question pattern validation passed")


if __name__ == "__main__":
    main()
