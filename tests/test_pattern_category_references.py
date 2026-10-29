"""Bounded DSL category-reference fixtures; no Kotomi engine or shipped Content."""
from pathlib import Path
import tempfile
import unittest
import xml.etree.ElementTree as ET

from tools.validate_repository import validate_semantic_categories


class PatternCategoryReferencesTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        (self.root/'quiz_project.xml').write_text('''<quiz_project><dictionaries>
          <dictionary id="adverbs" schema="adverb" file="adverbs.xml"/>
          </dictionaries><semantic_categories file="categories.xml"/>
          <sentence_maps file="maps.xml"/></quiz_project>''')
        (self.root/'categories.xml').write_text('''<noun_categories schema_version="2">
          <category id="concrete" selectable="false"/><category id="person" parent="concrete"/>
          </noun_categories>''')
        (self.root/'adverbs.xml').write_text('''<dictionary schema="adverb"><categories>
          <category id="frequency"/></categories><words/></dictionary>''')

    def pattern(self, question, answer='', *, composite=False):
        root = ET.Element('sentence_maps')
        node = ET.SubElement(ET.SubElement(root, 'sentence_patterns'), 'sentence_pattern', id='Synthetic pattern')
        if composite:
            ET.SubElement(ET.SubElement(node, 'patterns'), 'pattern', ref='Other pattern')
        ET.SubElement(node, 'question').text = question
        ET.SubElement(node, 'answer').text = answer
        ET.ElementTree(root).write(self.root/'maps.xml', encoding='utf-8')

    def test_existing_category(self):
        self.pattern('{noun@person[category:person].translation}')
        validate_semantic_categories(self.root)

    def test_new_category_needs_only_catalog_declaration(self):
        self.pattern('{noun[category:new_material]}')
        tree = ET.parse(self.root/'categories.xml')
        ET.SubElement(tree.getroot(), 'category', id='new_material', parent='concrete')
        tree.write(self.root/'categories.xml')
        validate_semantic_categories(self.root)

    def test_unknown_and_misspelled_categories_include_pattern_location(self):
        for category in ('unknown', 'persno'):
            with self.subTest(category=category):
                self.pattern('{noun@person[category:'+category+'].translation}')
                with self.assertRaisesRegex(AssertionError, "Synthetic pattern question: unknown noun category '"+category+"'"):
                    validate_semantic_categories(self.root)

    def test_no_selector_and_plain_text_are_not_category_references(self):
        self.pattern('category:persno {noun@person.translation} {verb[form].translation}')
        validate_semantic_categories(self.root)

    def test_every_token_in_both_fields_is_checked(self):
        for field in ('question', 'answer'):
            with self.subTest(field=field):
                values = {'question': '{noun[category:person]}', 'answer': '{noun[category:concrete]}'}
                values[field] += ' {noun@second[case:nominative, category:persno].translation}'
                self.pattern(**values)
                with self.assertRaisesRegex(AssertionError, field+": unknown noun category 'persno'"):
                    validate_semantic_categories(self.root)

    def test_composite_template_tokens_are_checked_without_expansion(self):
        self.pattern('{noun[category:person]} {pattern[form:dictionary]}', composite=True)
        validate_semantic_categories(self.root)
        self.pattern('{noun[category:persno]} {pattern[form:dictionary]}', composite=True)
        with self.assertRaisesRegex(AssertionError, 'Synthetic pattern.*persno'):
            validate_semantic_categories(self.root)

    def test_older_content_without_category_catalog_keeps_legacy_behavior(self):
        self.pattern('{noun[category:legacy_category]}')
        tree = ET.parse(self.root/'quiz_project.xml')
        tree.getroot().remove(tree.getroot().find('semantic_categories'))
        tree.write(self.root/'quiz_project.xml')
        (self.root/'categories.xml').unlink()
        validate_semantic_categories(self.root)

    def test_adverb_catalog_is_separate(self):
        self.pattern('{adverb@frequency[category:frequency].translation} {noun[category:person]}')
        validate_semantic_categories(self.root)
        self.pattern('{adverb[category:person]}')
        with self.assertRaisesRegex(AssertionError, "unknown adverb category 'person'"):
            validate_semantic_categories(self.root)

    def test_malformed_or_unsupported_selectors_remain_application_checks(self):
        for token in ('{noun[category:@alias]}', '{noun[category:bad value]}',
                      '{noun[category:person][id:sample]}', '{verb[category:persno]}'):
            with self.subTest(token=token):
                self.pattern(token)
                validate_semantic_categories(self.root)
