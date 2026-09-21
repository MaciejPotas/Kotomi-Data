from __future__ import annotations

from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from validate_repository import (  # noqa: E402
    unexpected_word_form_attributes,
    validate_polarity_group,
)


class GrammarValidationContractTests(unittest.TestCase):
    def test_polarity_group_requires_complete_pair(self) -> None:
        with self.assertRaisesRegex(
            AssertionError,
            "exactly one affirmative and one negative",
        ):
            validate_polarity_group(
                "verb",
                "plain_nonpast",
                {"affirmative": ("present", "plain")},
            )

    def test_polarity_group_preserves_context_and_register(self) -> None:
        with self.assertRaisesRegex(
            AssertionError,
            "preserve context and register",
        ):
            validate_polarity_group(
                "verb",
                "plain_nonpast",
                {
                    "affirmative": ("present", "plain"),
                    "negative": ("past", "plain"),
                },
            )

    def test_polarity_group_accepts_matching_pair(self) -> None:
        validate_polarity_group(
            "verb",
            "plain_nonpast",
            {
                "affirmative": ("present", "plain"),
                "negative": ("present", "plain"),
            },
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
