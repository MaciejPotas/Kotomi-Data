"""Data-side contracts for the coordinated Kotomi 1.5 migration."""
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]


class ContextualCountingDataTests(unittest.TestCase):
    def test_contextual_statements_require_the_new_loader(self):
        root = ET.parse(ROOT / 'patterns/sentence_maps.xml').getroot()
        for ident in ('Istnienie policzonych rzeczowników', 'Istnienie policzonych opisanych rzeczowników'):
            node = root.find(f"./sentence_patterns/sentence_pattern[@id='{ident}']")
            self.assertEqual(set(node.attrib), {'id', 'category'})
            self.assertIn('government:@existence', node.findtext('question'))
        project = ET.parse(ROOT / 'quiz_project.xml').getroot()
        self.assertEqual(project.get('min_kotomi_version'), '1.5')

    def test_two_contexts_share_lexemes_and_have_independent_quantities(self):
        ident = 'Dwie policzone grupy opisanych rzeczowników'
        root = ET.parse(ROOT / 'patterns/sentence_maps.xml').getroot()
        node = root.find(f"./sentence_patterns/sentence_pattern[@id='{ident}']")
        for name in ('left', 'right'):
            self.assertIn(f'occurrence:{name}', node.findtext('question'))
            self.assertIn(f'agree:@item#{name}', node.findtext('question'))
            self.assertIn(f'quantity:@{name}_count', node.findtext('answer'))
        self.assertEqual(node.findtext('answer').count('{noun@item}'), 2)
        quiz = ET.parse(ROOT / 'patterns/sentence_quizzes.xml').getroot().find("./quiz[@id='counting']")
        self.assertIsNotNone(quiz.find(f".//pattern[@ref='{ident}']"))

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

    def test_contextual_adjective_is_available_in_counting_quiz(self):
        ident = 'Istnienie policzonych opisanych rzeczowników'
        root = ET.parse(ROOT / 'patterns/sentence_maps.xml').getroot()
        node = root.find(f"./sentence_patterns/sentence_pattern[@id='{ident}']")
        self.assertEqual(node.get('category'), 'counting')
        self.assertIn('{adjective@quality[form:attributive_nonpast, agree:@item].translation}', node.findtext('question'))
        self.assertIn('{adjective@quality[form:attributive_nonpast]}{noun@item}', node.findtext('answer'))
        quiz = ET.parse(ROOT / 'patterns/sentence_quizzes.xml').getroot().find("./quiz[@id='counting']")
        self.assertIsNotNone(quiz.find(f".//pattern[@ref='{ident}']"))
