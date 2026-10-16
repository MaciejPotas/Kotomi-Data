"""C2.2 mutation fixture v1, derived only from independent C1 fixture v1."""
from copy import deepcopy
import json
from pathlib import Path
import sys
import unittest
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from validate_verb_subject_c21 import category_subject_role, validate_deployment, validate_hitori_retirement


class CategoryDeploymentTests(unittest.TestCase):
    def setUp(self):
        fixture = json.loads((ROOT / 'tests/fixtures/c1/v1.json').read_text(encoding='utf-8'))
        self.report = fixture['report']
        self.report['noun_groups'] = {'people': ['actor'],
            'people_animals': ['actor', 'pet', 'bird'], 'people_dog': ['actor', 'pet']}
        self.root = ET.fromstring(fixture['verbs_xml'])
        self.word = self.root.find("words/word[@id='fixture_new']")
        self.row = next(r for r in self.report['verbs'] if r['id'] == 'fixture_new')
        self.role = ET.SubElement(self.word.find('usage'), 'role',
                                 {'ref': 'subject', 'accepts': 'person'})
        for change in self.report['changes']:
            if change['verb_id'] == 'fixture_new' and change['operation'] == 'add_agreement_translation':
                form = self.word.find(f"forms/form[@ref='{change['form']}']")
                section = form.find('agreement_translations')
                if section is None:
                    section = ET.SubElement(form, 'agreement_translations')
                ET.SubElement(section, 'translation', {'class': change['class'], 'value': change['value']})

    def validate(self):
        return validate_deployment(self.root, self.report, {'fixture_new'},
            role_overrides={'fixture_new': category_subject_role(self.row, self.report)})

    def test_category_policy_preserves_historical_report_and_other_roles(self):
        before = deepcopy(self.report), ET.tostring(self.word.find('usage/role'))
        self.assertEqual(5, self.validate())
        self.assertEqual(before, (self.report, ET.tostring(self.word.find('usage/role'))))

    def test_both_reviewed_animal_groups_use_the_complete_category(self):
        for group in ('people_animals', 'people_dog'):
            self.row['subject_candidate_nouns'] = self.report['noun_groups'][group]
            self.role.set('accepts', 'person animal')
            self.assertEqual(5, self.validate())

    def test_unknown_historical_noun_group_requires_review(self):
        self.row['subject_candidate_nouns'] = ['unreviewed']
        with self.assertRaisesRegex(ValueError, 'unreviewed category migration'):
            self.validate()

    def test_noun_exceptions_and_wrong_or_broadened_categories_fail(self):
        for attrs in ({'ref': 'subject', 'nouns': 'actor'},
                      {'ref': 'subject', 'accepts': 'person', 'nouns': 'pet'},
                      {'ref': 'subject', 'accepts': 'animal'},
                      {'ref': 'subject', 'accepts': 'person animal'},
                      {'ref': 'subject', 'accepts': 'person', 'government': 'extra'}):
            with self.subTest(attrs=attrs):
                self.role.attrib.clear(); self.role.attrib.update(attrs)
                with self.assertRaisesRegex(ValueError, 'subject role'):
                    self.validate()

    def test_category_mode_keeps_exact_dependency_checks(self):
        change = next(c for c in self.report['changes'] if c['operation'] == 'add_agreement_translation')
        required = change['depends_on'][0]
        for deps in ([], ['absent'], [change['id']], [required, required], None):
            with self.subTest(dependencies=deps):
                change['depends_on'] = deps
                with self.assertRaisesRegex(ValueError, 'dependencies'):
                    self.validate()

    def test_category_mode_keeps_exact_translations_and_classes(self):
        entry = self.word.find('forms/form/agreement_translations/translation')
        original = dict(entry.attrib)
        for attrs in ({**original, 'value': 'incorrect'}, {**original, 'class': 'neuter'}):
            entry.attrib.clear(); entry.attrib.update(attrs)
            with self.assertRaisesRegex(ValueError, 'agreement map'):
                self.validate()
        entry.attrib.clear(); entry.attrib.update(original)
        self.word.find('forms/form/agreement_translations').remove(entry)
        with self.assertRaisesRegex(ValueError, 'agreement map'):
            self.validate()


class CountingIdentityTests(unittest.TestCase):
    def test_counting_identity_is_independent_of_a_noun_entry(self):
        nouns = ET.fromstring('<dictionary><words><word id="fixture_person" /></words></dictionary>')
        counters = ET.fromstring('<dictionary><words><word id="nin"><quantity_realizations>'
            '<realization number="1" kana="ひとり" kanji="一人" romaji="hitori" />'
            '</quantity_realizations></word></words></dictionary>')
        validate_hitori_retirement(nouns, counters)
        duplicate = ET.SubElement(nouns.find('words'), 'word', {'id': 'hitori'})
        with self.assertRaisesRegex(ValueError, 'ordinary noun'):
            validate_hitori_retirement(nouns, counters)
        nouns.find('words').remove(duplicate)
        counters.find('words/word/quantity_realizations/realization').set('kana', 'いちにん')
        with self.assertRaisesRegex(ValueError, 'one person'):
            validate_hitori_retirement(nouns, counters)
