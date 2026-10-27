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

    def test_reviewed_extension_preserves_baseline_and_rejects_other_additions(self):
        form = self.word.find('forms/form')
        section = form.find('agreement_translations')
        key = ('fixture_new', form.get('ref'))
        ET.SubElement(section, 'translation', {'class': 'neuter', 'value': 'fixture quantity'})
        with self.assertRaises(ValueError): self.validate()
        kwargs = {'agreement_extensions': {key: {'neuter': 'fixture quantity'}}}
        self.assertEqual(validate_deployment(self.root, self.report, self.selected, **kwargs), 9)
        section[-1].set('value', 'wrong')
        with self.assertRaises(ValueError):
            validate_deployment(self.root, self.report, self.selected, **kwargs)
        section[-1].set('value', 'fixture quantity')
        original = section[0]
        with self.assertRaises(ValueError):
            validate_deployment(self.root, self.report, self.selected,
                agreement_extensions={key: {original.get('class'): original.get('value')}})

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


    def test_required_dependency_cannot_be_removed(self):
        change = self.report['changes'][1]
        for missing in ([], None):
            with self.subTest(missing=missing):
                if missing is None:
                    change.pop('depends_on', None)
                else:
                    change['depends_on'] = missing
                with self.assertRaisesRegex(ValueError, 'incorrect dependencies'):
                    self.validate()

    def test_dependency_must_reference_the_required_role_operation(self):
        change = self.report['changes'][1]
        wrong = self.report['changes'][2]['id']
        required = self.report['changes'][0]['id']
        for dependencies in ([wrong], [required, wrong], ['absent'], [change['id']]):
            with self.subTest(dependencies=dependencies):
                change['depends_on'] = dependencies
                with self.assertRaisesRegex(ValueError, 'incorrect dependencies'):
                    self.validate()

    def test_duplicate_or_malformed_dependencies_are_rejected(self):
        change = self.report['changes'][1]
        required = self.report['changes'][0]['id']
        for dependencies in ([required, required], required, None, [None], [[]]):
            with self.subTest(dependencies=dependencies):
                change['depends_on'] = dependencies
                with self.assertRaisesRegex(ValueError, 'dependencies'):
                    self.validate()

    def test_valid_dependency_is_independent_of_operation_order(self):
        self.report['changes'].reverse()
        self.assertEqual(self.validate(), 9)

    def test_subject_role_change_must_name_the_same_verbs_role_operation(self):
        row = next(r for r in self.report['verbs'] if r['id'] == 'fixture_new')
        for role_change in (None, 'absent', self.report['changes'][1]['id']):
            with self.subTest(role_change=role_change):
                row['subject_role_change'] = role_change
                with self.assertRaisesRegex(ValueError, 'subject_role_change'):
                    self.validate()

    def test_existing_subject_requires_no_dependency(self):
        # Keep the synthetic deployed XML, but model a previously existing role.
        self.report['changes'].pop(0)
        row = next(r for r in self.report['verbs'] if r['id'] == 'fixture_new')
        row['subject_role_change'] = None
        for change in self.report['changes']:
            change.pop('depends_on', None)
        self.assertEqual(self.validate(), 8)
        self.report['changes'][0]['depends_on'] = [self.report['changes'][1]['id']]
        with self.assertRaisesRegex(ValueError, 'incorrect dependencies'):
            self.validate()

    def test_role_addition_cannot_depend_on_a_translation(self):
        self.report['changes'][0]['depends_on'] = [self.report['changes'][1]['id']]
        with self.assertRaisesRegex(ValueError, 'incorrect dependencies'):
            self.validate()

    def test_production_plural_extension_preserves_historical_translations(self):
        section = self.word.find('forms/form/agreement_translations')
        original = dict(section[0].attrib)
        added = ET.SubElement(section, 'translation', {
            'class': 'plural_masculine_personal', 'value': 'pracowali',
        })
        # Historic C2 fixture contract still rejects extra classes by default.
        with self.assertRaisesRegex(ValueError, 'changed agreement map'):
            self.validate()
        kwargs = {'allow_plural_extensions': True}
        self.assertEqual(
            validate_deployment(self.root, self.report, self.selected, **kwargs), 9)
        # Reject changing an old translation, even when plural additions are allowed.
        section[0].set('value', 'changed baseline')
        with self.assertRaisesRegex(ValueError, 'changed agreement map'):
            validate_deployment(self.root, self.report, self.selected, **kwargs)
        section[0].attrib.clear()
        section[0].attrib.update(original)
        # No arbitrary new classes or empty plural values.
        added.set('class', 'neuter')
        with self.assertRaisesRegex(ValueError, 'changed agreement map'):
            validate_deployment(self.root, self.report, self.selected, **kwargs)
        added.set('class', 'plural_non_masculine_personal')
        added.set('value', '')
        with self.assertRaisesRegex(ValueError, 'changed agreement map'):
            validate_deployment(self.root, self.report, self.selected, **kwargs)
