"""Protect stored inflections that cannot be generated at runtime."""
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET


class PolishNumberCasesTests(unittest.TestCase):
    def test_one_dative_locative_and_feminine_oblique_forms(self):
        root = ET.parse(Path(__file__).resolve().parents[1] / 'dictionaries/numbers.xml').getroot()
        one = root.find("./words/word[@id='one']/polish_forms")
        def value(case, agreement=None):
            nodes = one.findall('override') if agreement else one.findall('common')
            return [node.get('value') for node in nodes
                    if case in node.get('cases', '').split()
                    and (not agreement or agreement in node.get('classes', '').split())]
        for case, expected in [('genitive', 'jednego'), ('dative', 'jednemu'),
                               ('locative', 'jednym'), ('instrumental', 'jednym')]:
            self.assertEqual(value(case), [expected])
        for case in ('genitive', 'dative', 'locative'):
            self.assertEqual(value(case, 'feminine'), ['jednej'])
        self.assertEqual(value('instrumental', 'feminine'), ['jedną'])

    def test_existing_numbers_supply_oblique_common_cases(self):
        root = ET.parse(Path(__file__).resolve().parents[1] / 'dictionaries/numbers.xml').getroot()
        for word in root.findall('./words/word'):
            for case in ('nominative', 'genitive', 'dative', 'accusative', 'instrumental', 'locative'):
                with self.subTest(word=word.get('id'), case=case):
                    values = [node.get('value') for node in word.findall('./polish_forms/common')
                              if case in node.get('cases', '').split()]
                    self.assertEqual(len(values), 1)
                    self.assertTrue(values[0])
