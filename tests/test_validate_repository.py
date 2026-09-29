from __future__ import annotations

from pathlib import Path
import re
import sys
import unittest
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from validate_repository import (  # noqa: E402
    unexpected_word_form_attributes,
    validate_polarity_pair,
)


class GrammarValidationContractTests(unittest.TestCase):
    def test_connector_dictionary_and_quiz_cover_requested_inventory(self) -> None:
        dictionary = ET.parse(
            ROOT / "dictionaries" / "connectors.xml"
        ).getroot()
        self.assertEqual("connector", dictionary.get("schema"))
        self.assertEqual(
            {
                "dakara", "soreka", "dakedo", "sorenara", "soreyori",
                "shikamo", "demo",
            },
            {
                word.get("id", "")
                for word in dictionary.findall("./words/word")
            },
        )
        quizzes = ET.parse(
            ROOT / "patterns" / "sentence_quizzes.xml"
        ).getroot()
        quiz = quizzes.find("./quiz[@id='connectors']")
        self.assertIsNotNone(quiz)
        self.assertEqual("references", quiz.get("selection"))
        self.assertEqual(
            {
                "Łącznik だから",
                "Łącznik それか",
                "Łącznik だけど",
                "Łącznik それなら",
                "Łącznik それより",
                "Łącznik しかも",
                "Łącznik でも",
            },
            {
                pattern.get("ref", "")
                for pattern in quiz.findall("./patterns/pattern")
            },
        )

    def test_connector_patterns_use_two_unconstrained_verbs(self) -> None:
        patterns = ET.parse(ROOT / "patterns" / "sentence_maps.xml").getroot()
        grammar = ET.parse(ROOT / "grammar" / "grammar_rules.xml").getroot()
        self.assertFalse(any(
            (feature.get("id") or "").startswith("connector_")
            for feature in grammar.findall("./features/feature")
        ))
        seen = set()
        for pattern in patterns.findall("./sentence_patterns/sentence_pattern"):
            if pattern.get("category") != "connectors":
                continue
            question = pattern.findtext("question", "")
            answer = pattern.findtext("answer", "")
            connector = re.search(r"\{connector\[id:([a-z]+)\]", question)
            self.assertIsNotNone(connector, pattern.get("id"))
            connector_id = connector.group(1)
            seen.add(connector_id)
            self.assertIn(f"{{connector[id:{connector_id}]}}", answer)
            self.assertEqual(
                ["first", "second"],
                re.findall(r"\{verb@([^}\[]+)\[form:dictionary\]\.translation\}", question),
            )
            self.assertEqual(
                ["first", "second"],
                re.findall(r"\{verb@([^}\[]+)\[form:dictionary\]\}", answer),
            )
            for text in (question, answer):
                self.assertNotIn("{noun", text)
                self.assertNotRegex(text, r"\{verb@[^}]*\b(id|role|feature|government):")
        self.assertEqual(
            {"dakara", "soreka", "dakedo", "sorenara", "soreyori", "shikamo", "demo"},
            seen,
        )

    def test_pattern_readme_uses_supported_interrogative_syntax(self) -> None:
        text = (ROOT / "patterns" / "README.md").read_text(encoding="utf-8")
        self.assertNotIn("interrogative@object[id:nani, government:", text)
        self.assertIn("interrogative@object[id:nani].translation", text)

    def test_polarity_pair_requires_complete_pair(self) -> None:
        with self.assertRaisesRegex(
            AssertionError,
            "exactly one affirmative and one negative",
        ):
            validate_polarity_pair(
                "verb",
                "present",
                "plain",
                {"affirmative"},
            )

    def test_polarity_pair_accepts_matching_pair(self) -> None:
        validate_polarity_pair(
            "verb",
            "present",
            "plain",
            {"affirmative", "negative"},
        )

    def test_word_form_attribute_allowlist_matches_loader_contract(self) -> None:
        self.assertEqual(
            set(),
            unexpected_word_form_attributes(
                {
                    "ref": "dictionary",
                    "translation": "biorę",
                    "kana": "とる",
                    "kanji": "取る",
                    "romaji": "toru",
                }
            ),
        )
        self.assertEqual(
            {"context", "custom"},
            unexpected_word_form_attributes(
                {
                    "ref": "dictionary",
                    "kana": "とる",
                    "context": "present",
                    "custom": "unexpected",
                }
            ),
        )


if __name__ == "__main__":
    unittest.main()
