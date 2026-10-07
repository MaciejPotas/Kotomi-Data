"""The no-source-grammar probe still ships the complete Japanese authoring data."""
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
PROBE = ROOT / 'instruction_languages/test'


def attributes_without_labels(node):
    if node is None:
        return None
    return (node.tag, {key: value for key, value in node.attrib.items() if key != 'label'},
            [attributes_without_labels(child) for child in node])


class JapaneseTargetAuthoringTests(unittest.TestCase):
    def test_target_catalogs_do_not_depend_on_instruction_language(self):
        reference = ET.parse(ROOT / 'grammar/grammar_rules.xml').getroot()
        probe = ET.parse(PROBE / 'grammar.xml').getroot()
        for tag in ('noun_categories', 'form_catalogs'):
            with self.subTest(tag=tag):
                self.assertEqual(attributes_without_labels(reference.find(tag)),
                                 attributes_without_labels(probe.find(tag)))
        self.assertIsNone(probe.find('agreement_catalogs'))
        self.assertIsNone(probe.find('polish_government'))

    def test_target_counting_is_complete_without_polish_source_profiles(self):
        reference = ET.parse(ROOT / 'grammar/counting.xml').getroot()
        probe = ET.parse(PROBE / 'counting.xml').getroot()
        for tag in ('number_composition', 'counter_composition_profiles', 'counting_classes'):
            with self.subTest(tag=tag):
                self.assertEqual(attributes_without_labels(reference.find(tag)),
                                 attributes_without_labels(probe.find(tag)))
        for profile in probe.findall('./count_source_profiles/profiles/profile'):
            self.assertNotIn('source_agreement', profile.attrib)
            self.assertNotIn('source_form_strategy', profile.attrib)
            self.assertNotIn('fallback', profile.attrib)

    def test_counter_surfaces_and_exact_quantities_are_target_data(self):
        reference = ET.parse(ROOT / 'dictionaries/counters.xml').getroot()
        probe = {node.get('id'): node for node in ET.parse(PROBE / 'counters.xml').findall('./words/word')}
        for word in reference.findall('./words/word'):
            with self.subTest(counter=word.get('id')):
                counterpart = probe[word.get('id')]
                for field in ('kana', 'kanji', 'romaji'):
                    self.assertEqual(word.get(field), counterpart.get(field))
                for tag in ('composition', 'quantity_realizations'):
                    self.assertEqual(attributes_without_labels(word.find(tag)),
                                     attributes_without_labels(counterpart.find(tag)))
