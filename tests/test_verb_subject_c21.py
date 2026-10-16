"""C2.1 check mutations on independent versioned C1 fixture v1, never Content."""
from copy import deepcopy
import json
from pathlib import Path
import sys
import unittest
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from validate_verb_subject_c21 import validate_deployment


class DeploymentTests(unittest.TestCase):
    def setUp(self):
        fixture = json.loads((ROOT / 'tests/fixtures/c1/v1.json').read_text(encoding='utf-8'))
        self.report = fixture['report']
        self.root = ET.fromstring(fixture['verbs_xml'])
        self.selected = {c['verb_id'] for c in self.report['changes']}
        for change in self.report['changes']:
            word = self.root.find(f"words/word[@id='{change['verb_id']}']")
            if change['operation'] == 'add_role':
                ET.SubElement(word.find('usage'), 'role', change['role'])
            else:
                form = word.find(f"forms/form[@ref='{change['form']}']")
                section = form.find('agreement_translations')
                if section is None:
                    section = ET.SubElement(form, 'agreement_translations')
                ET.SubElement(section, 'translation', {'class': change['class'], 'value': change['value']})
        self.word = self.root.find("words/word[@id='fixture_new']")

    def validate(self):
        return validate_deployment(self.root, self.report, self.selected)

    def test_valid_deployment_is_read_only(self):
        before = ET.tostring(self.root), deepcopy(self.report)
        self.assertEqual(self.validate(), 9)
        self.assertEqual(before, (ET.tostring(self.root), self.report))

    def test_missing_or_duplicate_parent(self):
        for path, tag in [('words', 'word'), ('words/word', 'usage'),
                          ('words/word/forms', 'form')]:
            # Use the selected word for nested cases, not another fixture verb.
            parent = self.root.find('words') if path == 'words' else (
                self.word if tag == 'usage' else self.word.find('forms'))
            child = self.word if tag == 'word' else parent.find(tag)
            with self.subTest(tag=tag):
                parent.append(deepcopy(child))
                with self.assertRaises(ValueError): self.validate()
                parent.remove(parent[-1])
                parent.remove(child)
                with self.assertRaises(ValueError): self.validate()
                parent.append(child)

    def test_changed_or_duplicate_translation(self):
        section = self.word.find('forms/form/agreement_translations')
        entry = section[0]
        for attr, value in [('value', 'incorrect'), ('class', 'unknown')]:
            old = entry.get(attr); entry.set(attr, value)
            with self.assertRaises(ValueError): self.validate()
            entry.set(attr, old)
        section.append(deepcopy(entry))
        with self.assertRaises(ValueError): self.validate()

    def test_missing_map_and_missing_class(self):
        form = self.word.find('forms/form'); section = form.find('agreement_translations')
        form.remove(section)
        with self.assertRaises(ValueError): self.validate()
        form.append(section); section.remove(section[0])
        with self.assertRaises(ValueError): self.validate()

    def test_no_extra_class_or_duplicate_container(self):
        form = self.word.find('forms/form'); section = form.find('agreement_translations')
        ET.SubElement(section, 'translation', {'class': 'neuter', 'value': 'extra'})
        with self.assertRaises(ValueError): self.validate()
        section.remove(section[-1]); form.append(deepcopy(section))
        with self.assertRaises(ValueError): self.validate()

    def test_exact_subject_role_rejects_broadening(self):
        role = self.word.find("usage/role[@ref='subject']")
        for key, value in [('accepts', 'person'), ('nouns', 'other'), ('government', 'other')]:
            original = dict(role.attrib); role.set(key, value)
            with self.assertRaises(ValueError): self.validate()
            role.attrib.clear(); role.attrib.update(original)

    def test_missing_duplicate_or_non_a_operations(self):
        original = deepcopy(self.report)
        mutations = [lambda: self.report['changes'].pop(),
                     lambda: self.report['changes'].append(deepcopy(self.report['changes'][0])),
                     lambda: self.report['changes'][0].update(status='B'),
                     lambda: self.report['changes'][1].update(depends_on=['absent']),
                     lambda: self.report['changes'][1].update(path='/wrong')]
        for mutate in mutations:
            self.report = deepcopy(original); mutate()
            with self.assertRaises(ValueError): self.validate()

    def test_legacy_translations_roles_and_maps_are_not_modified(self):
        self.word.find('forms/form').set('translation', 'legacy gloss')
        ET.SubElement(self.word.find('usage'), 'role', {'ref': 'object', 'nouns': 'fixture_item',
                                                      'government': 'direct_object'})
        before = ET.tostring(self.root)
        self.validate()
        self.assertEqual(before, ET.tostring(self.root))
