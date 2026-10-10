"""Published lexical quality checks, independent of quiz membership."""
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]


class ContextualCountingDataTests(unittest.TestCase):


    def test_one_to_ten_has_required_genitives(self):
        root = ET.parse(ROOT / 'dictionaries/numbers.xml').getroot()
        expected = {'one': 'jednego', 'two': 'dwóch', 'three': 'trzech', 'four': 'czterech',
                    'five': 'pięciu', 'six': 'sześciu', 'seven': 'siedmiu',
                    'eight': 'ośmiu', 'nine': 'dziewięciu', 'ten': 'dziesięciu'}
        for ident, value in expected.items():
            with self.subTest(number=ident):
                word = root.find(f"./words/word[@id='{ident}']")
                matches = [node.get('value') for node in word.findall('./polish_forms/common')
                           if 'genitive' in node.get('cases', '').split()]
                self.assertEqual(matches, [value])
        one = root.find("./words/word[@id='one']")
        self.assertTrue(any(node.get('value') == 'jednej'
            and 'feminine' in node.get('classes', '').split()
            and 'genitive' in node.get('cases', '').split()
            for node in one.findall('./polish_forms/override')))

    def test_animate_predicate_gains_only_source_government(self):
        root = ET.parse(ROOT / 'dictionaries/verbs.xml').getroot()
        word = root.find("./words/word[@id='iru']")
        subject = word.find("./usage/role[@ref='subject']")
        self.assertEqual(subject.get('accepts'), 'person animal')
        self.assertEqual(subject.get('government'), 'existential_subject')
        for name, kana in [('dictionary', 'いる'), ('past_plain', 'いた'),
                           ('plain_negative', 'いない'), ('past_negative_plain', 'いなかった')]:
            self.assertEqual(word.find(f"./forms/form[@ref='{name}']").get('kana'), kana)
