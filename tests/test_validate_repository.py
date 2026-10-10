from __future__ import annotations

from pathlib import Path
import sys
import unittest
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))


from validate_repository import (  # noqa: E402
    unexpected_word_form_attributes,
    validate_counting_data,
)


class GrammarValidationContractTests(unittest.TestCase):


    def test_pattern_readme_uses_supported_interrogative_syntax(self) -> None:
        text = (ROOT / "patterns" / "README.md").read_text(encoding="utf-8")
        self.assertNotIn("interrogative@object[id:nani, government:", text)
        self.assertIn("interrogative@object[id:nani].translation", text)

    def test_schema2_counting_inventory_is_complete(self) -> None:
        validate_counting_data()


    def test_canonical_number_sets_are_declared(self) -> None:
        grammar = ET.parse(
            ROOT / "grammar" / "counting.xml"
        ).getroot()
        sets = {
            node.get("id"): {
                number.get("ref")
                for number in node.findall("./number")
            }
            for node in grammar.findall("./number_sets/set")
        }
        self.assertEqual(
            {
                "one", "two", "three", "four", "five",
                "six", "seven", "eight", "nine", "ten",
            },
            sets["one_to_ten"],
        )
        self.assertEqual({"two", "three", "four"}, sets["two_to_four"])
        self.assertEqual(
            {
                "two", "three", "four", "five", "six",
                "seven", "eight", "nine", "ten", "twenty",
            },
            sets["two_or_more"],
        )

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

    def test_twenty_oclock_is_exact_data(self) -> None:
        counters = ET.parse(
            ROOT / "dictionaries" / "counters.xml"
        ).getroot()
        realization = counters.find(
            "./words/word[@id='ji']/"
            "quantity_realizations/realization[@number='20']"
        )
        self.assertIsNotNone(realization)
        assert realization is not None
        self.assertEqual("にじゅうじ", realization.get("kana"))
        self.assertEqual("二十時", realization.get("kanji"))
        self.assertEqual("nijuuji", realization.get("romaji"))


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
