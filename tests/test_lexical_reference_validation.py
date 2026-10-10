"""Reference-validation behavior on bounded files, never shipped vocabulary."""
from pathlib import Path
import shutil
import tempfile
import unittest
import xml.etree.ElementTree as ET
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("lexical_reference_validator", ROOT / "tools/validate_repository.py")
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)

class LexicalReferenceValidationTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name) / "fixture"
        shutil.copytree(Path(__file__).parent / "fixtures/lexical", self.root)

    def change(self, file, xpath, attributes):
        path = self.root / file
        tree = ET.parse(path)
        tree.getroot().find(xpath).attrib.update(attributes)
        tree.write(path, encoding="utf-8")

    def test_lesson_and_context_share_one_word(self):
        validator.validate_lesson_references(self.root)
        validator.validate_context_references(self.root)

    def test_missing_lesson_word_is_rejected(self):
        self.change("lessons/lessons.xml", "./lessons/lesson/word/dictionary_ref", {"word": "missing"})
        with self.assertRaisesRegex(AssertionError, "missing word"):
            validator.validate_lesson_references(self.root)

    def test_unknown_context_dictionary_is_rejected(self):
        self.change("grammar/contexts.xml", "./context/option", {"dictionary": "missing"})
        with self.assertRaisesRegex(AssertionError, "missing word"):
            validator.validate_context_references(self.root)

    def test_missing_context_word_is_rejected(self):
        self.change("grammar/contexts.xml", "./context/option", {"word": "missing"})
        with self.assertRaisesRegex(AssertionError, "missing word"):
            validator.validate_context_references(self.root)

    def test_partial_reference_is_rejected(self):
        self.change("grammar/contexts.xml", "./context/option", {"word": ""})
        with self.assertRaisesRegex(AssertionError, "together"):
            validator.validate_context_references(self.root)

    def test_mixed_reference_and_inline_text_is_rejected(self):
        self.change("grammar/contexts.xml", "./context/option", {"kana": "other"})
        with self.assertRaisesRegex(AssertionError, "mix"):
            validator.validate_context_references(self.root)
