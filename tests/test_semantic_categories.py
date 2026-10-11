"""Catalog validation with a tiny independent XML fixture, no shipped words."""
from pathlib import Path
import tempfile
import unittest
import xml.etree.ElementTree as ET
from test_lexical_reference_validation import validator


class SemanticCategoryTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        (self.root / 'quiz_project.xml').write_text('<quiz_project><dictionaries><dictionary id="adverbs" file="adverbs.xml" schema="adverb"/></dictionaries></quiz_project>')
        self.dictionary = ET.fromstring('<dictionary schema="adverb"><categories><category id="frequency"/><category id="custom"/></categories><words><word id="sample" categories="frequency custom"/><word id="legacy"/></words></dictionary>')

    def validate(self):
        ET.ElementTree(self.dictionary).write(self.root / 'adverbs.xml')
        validator.validate_semantic_categories(self.root)

    def test_valid_multi_category_and_legacy(self):
        self.validate()

    def test_unknown_membership(self):
        self.dictionary.find('./words/word').set('categories', 'missing')
        with self.assertRaisesRegex(AssertionError, 'Unknown semantic'): self.validate()

    def test_duplicate_membership(self):
        self.dictionary.find('./words/word').set('categories', 'frequency frequency')
        with self.assertRaisesRegex(AssertionError, 'Duplicate semantic'): self.validate()

    def test_duplicate_declaration(self):
        ET.SubElement(self.dictionary.find('categories'), 'category', id='frequency')
        with self.assertRaisesRegex(AssertionError, 'Duplicate semantic'): self.validate()

    def test_invalid_id(self):
        self.dictionary.find('./categories/category').set('id', 'bad value')
        with self.assertRaisesRegex(AssertionError, 'Invalid semantic'): self.validate()

    def test_noun_catalog_cannot_be_reused(self):
        self.dictionary.set('schema', 'noun')
        with self.assertRaisesRegex(AssertionError, 'require adverb'): self.validate()

    def test_singular_category_rejected(self):
        self.dictionary.find('./words/word').set('category', 'frequency')
        with self.assertRaisesRegex(AssertionError, 'Adverbs use categories'): self.validate()

    def test_old_dictionary_without_catalog(self):
        self.dictionary.remove(self.dictionary.find('categories'))
        self.dictionary.find('./words/word').attrib.pop('categories')
        self.validate()
