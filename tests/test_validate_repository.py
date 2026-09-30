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
    validate_counting_data,
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
            self.assertNotIn(";", question)
            self.assertNotIn(";", answer)
            if connector_id == "dakara":
                self.assertIn(
                    "{verb@first[form]}。{connector[id:dakara]}、{verb@second[form]}。",
                    answer,
                )
            else:
                self.assertIn(f"、{{connector[id:{connector_id}]}}", answer)
            if connector_id == "soreka":
                self.assertIn("} {connector[id:" + connector_id + "]", question)
            else:
                self.assertIn("}, {connector[id:" + connector_id + "]", question)
            self.assertEqual(
                ["first", "second"],
                re.findall(r"\{verb@([^}\[]+)\[form\]\.translation\}", question),
            )
            self.assertEqual(
                ["first", "second"],
                re.findall(r"\{verb@([^}\[]+)\[form\]\}", answer),
            )
            for text in (question, answer):
                self.assertNotIn("{noun", text)
                self.assertNotRegex(text, r"\{verb@[^}]*\b(id|role|feature|government):")
        self.assertEqual(
            {"dakara", "soreka", "dakedo", "sorenara", "soreyori", "shikamo", "demo"},
            seen,
        )

    def test_dakara_keeps_finite_polite_verb_before_sentence_boundary(self) -> None:
        patterns = ET.parse(ROOT / "patterns" / "sentence_maps.xml").getroot()
        pattern = patterns.find(
            "./sentence_patterns/sentence_pattern[@id='Łącznik だから']"
        )
        self.assertIsNotNone(pattern)
        assert pattern is not None
        self.assertEqual(
            "{verb@first[form]}。{connector[id:dakara]}、{verb@second[form]}。",
            pattern.findtext("answer", ""),
        )

    def test_pattern_readme_uses_supported_interrogative_syntax(self) -> None:
        text = (ROOT / "patterns" / "README.md").read_text(encoding="utf-8")
        self.assertNotIn("interrogative@object[id:nani, government:", text)
        self.assertIn("interrogative@object[id:nani].translation", text)

    def test_schema2_counting_inventory_is_complete(self) -> None:
        validate_counting_data()

    def test_age_twenty_and_domain_counters_are_exact_data(self) -> None:
        counters = ET.parse(
            ROOT / "dictionaries" / "counters.xml"
        ).getroot()
        expected = {
            "ji": ("4", "よじ", "四時"),
            "fun": ("3", "さんぷん", "三分"),
            "sai": ("20", "はたち", "二十歳"),
            "kai": ("3", "さんがい", "三階"),
        }
        for counter_id, (number, kana, kanji) in expected.items():
            with self.subTest(counter=counter_id):
                node = counters.find(
                    "./words/word[@id='" + counter_id + "']/"
                    "quantity_realizations/realization[@number='" + number + "']"
                )
                self.assertIsNotNone(node)
                assert node is not None
                self.assertEqual(kana, node.get("kana"))
                self.assertEqual(kanji, node.get("kanji"))

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
