"""C1 validator mutations on a versioned synthetic fixture, never Content."""
from copy import deepcopy
from dataclasses import asdict
import importlib.util
import json
import os
from pathlib import Path
import sys
from types import SimpleNamespace
import unittest
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('c1_validator', ROOT / 'tools/validate_verb_dictionary_audit.py')
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class AuditTests(unittest.TestCase):
    def setUp(self):
        fixture = json.loads((ROOT / 'tests/fixtures/c1/v1.json').read_text(encoding='utf-8'))
        self.report = fixture['report']
        self.words = ET.fromstring(fixture['verbs_xml']).findall('words/word')
        self.nouns = ET.fromstring(fixture['nouns_xml']).findall('words/word')
        self.forms = fixture['forms']

    def validate(self):
        return validator.validate_static(self.report, self.words, self.nouns, self.forms)

    def test_valid_A_operations_and_no_mutation(self):
        before = deepcopy(self.report)
        source = [ET.tostring(w) for w in self.words + self.nouns]
        self.assertEqual(self.validate(), 9)
        self.assertEqual(before, self.report)
        self.assertEqual(source, [ET.tostring(w) for w in self.words + self.nouns])

    def test_missing_translation_even_with_adjusted_stats(self):
        self.report['changes'].pop()
        self.report['stats']['A_agreement_entries'] -= 1
        self.report['stats']['A_agreement_forms'] -= 1
        with self.assertRaisesRegex(ValueError, 'Operation set mismatch.*missing='):
            self.validate()

    def test_missing_role_even_with_adjusted_stats(self):
        self.report['changes'].pop(0)
        self.report['stats']['A_role_additions'] = 0
        with self.assertRaisesRegex(ValueError, 'Operation set mismatch'):
            self.validate()

    def test_extra_operation(self):
        extra = deepcopy(self.report['changes'][1]); extra['id'] = 'unreviewed'
        self.report['changes'].append(extra)
        with self.assertRaisesRegex(ValueError, 'Operation set mismatch.*extra='):
            self.validate()

    def test_duplicate_operation(self):
        self.report['changes'].append(deepcopy(self.report['changes'][1]))
        with self.assertRaisesRegex(ValueError, 'Duplicate proposal'):
            self.validate()

    def test_role_definition_changes(self):
        role = self.words[0].find('usage/role')
        before = dict(role.attrib)
        for field,value in [('ref','elsewhere'),('accepts','object'),('nouns','actor'),('government','other'),('future_attribute','new')]:
            with self.subTest(field=field):
                role.attrib.clear();role.attrib.update(before);role.set(field,value)
                with self.assertRaisesRegex(ValueError, 'Role definition drift'):
                    self.validate()

    def test_removed_role(self):
        usage = self.words[0].find('usage');usage.remove(usage[0])
        with self.assertRaisesRegex(ValueError, 'Role definition drift'):
            self.validate()

    def test_unknown_agreement_class_even_if_allowed_list_changed(self):
        self.report['allowed_classes'].append('invented')
        with self.assertRaisesRegex(ValueError, 'Unknown agreement class'):
            self.validate()

    def test_unknown_proposed_class(self):
        self.report['verbs'][0]['proposed_priority_values']['dictionary']['invented'] = 'test'
        with self.assertRaisesRegex(ValueError, 'Unknown agreement class'):
            self.validate()

    def test_noun_class_changes_with_unchanged_required_class_set(self):
        # A swap keeps the union of available classes unchanged.
        self.nouns[0].find('agreement').set('class', 'masculine_personal')
        self.nouns[1].find('agreement').set('class', 'feminine')
        with self.assertRaisesRegex(ValueError, 'Noun agreement class drift'):
            self.validate()

    def test_overwrite_existing_translation(self):
        section = ET.SubElement(self.words[0].find('forms/form'), 'agreement_translations')
        ET.SubElement(section, 'translation', {'class':'feminine','value':'already stored'})
        with self.assertRaisesRegex(ValueError, 'Existing agreement drift / overwrite'):
            self.validate()

    def test_reviewed_value_cannot_overwrite_existing_value(self):
        self.report['verbs'][0]['existing_agreement'] = {'dictionary':{'feminine':'already stored'}}
        section = ET.SubElement(self.words[0].find('forms/form'), 'agreement_translations')
        ET.SubElement(section, 'translation', {'class':'feminine','value':'already stored'})
        with self.assertRaisesRegex(ValueError, 'Would overwrite reviewed translation'):
            self.validate()

    def test_invalid_dependencies(self):
        change = self.report['changes'][1]
        for deps in ([], ['missing'], [self.report['changes'][2]['id']], [change['id']], ['fixture_new:subject'] * 2):
            with self.subTest(deps=deps):
                change['depends_on'] = deps
                with self.assertRaisesRegex(ValueError, 'dependency|Duplicate dependency'):
                    self.validate()

    def test_role_dependency_cycle(self):
        self.report['changes'][0]['depends_on'] = [self.report['changes'][1]['id']]
        with self.assertRaisesRegex(ValueError, 'dependency'):
            self.validate()

    def test_existing_subject_needs_no_role_dependency(self):
        self.report['changes'][-1]['depends_on'] = ['fixture_new:subject']
        with self.assertRaisesRegex(ValueError, 'dependency'):
            self.validate()

    def test_each_static_statistic_is_checked(self):
        stats = self.report['stats']
        for key,value in list(stats.items()):
            if key == 'patterns':continue  # real expanded pattern count requires engine
            with self.subTest(statistic=key):
                stats[key] = {'A':999} if isinstance(value,dict) else value + 1
                with self.assertRaisesRegex(ValueError, 'Statistics mismatch'):
                    self.validate()
                stats[key] = value

    def engine_view(self):
        # Stub boundary outputs, not a second implementation of role semantics.
        entities = {n.get('id'):SimpleNamespace(id=n.get('id'), agreement_class=n.find('agreement').get('class')) for n in self.nouns}
        return SimpleNamespace(roles={},patterns={},entities=entities,
            words={'verbs':{r['id']:r for r in self.report['verbs']}},
            instruction_language=SimpleNamespace(capabilities=SimpleNamespace(verb_agreement_classes=validator.C1_CLASSES)))

    def test_changed_actual_matches_are_rejected(self):
        with self.assertRaisesRegex(ValueError, 'Role matches drift'):
            validator.validate_engine(self.report, self.engine_view(), lambda p,w,r,n:False, lambda *args:False)

    def test_engine_pattern_statistic(self):
        self.report['stats']['patterns'] = 1
        with self.assertRaisesRegex(ValueError, 'Statistics mismatch: patterns'):
            validator.validate_engine(self.report, self.engine_view(), lambda *args:False, lambda *args:False)

    def test_engine_role_default_definition(self):
        self.report['engine_role_definitions'] = {'subject':{'default_categories':['living']}}
        with self.assertRaisesRegex(ValueError, 'Engine role definition drift'):
            validator.validate_engine(self.report, self.engine_view(), lambda *args:False, lambda *args:False)


@unittest.skipUnless(os.environ.get('KOTOMI_PATH'), 'Set KOTOMI_PATH for actual engine contract tests on synthetic objects')
class EngineRoleContractTests(unittest.TestCase):
    def setUp(self):
        sys.path.insert(0, os.environ['KOTOMI_PATH'])
        from kotomi.core.project.models import Word, Entity, NounCategory, RoleDefinition
        from kotomi.core.generation.compatibility import role_matches
        self.matches = role_matches
        self.word = Word('verbs','synthetic','test','てすと',usage={'subject':['living']},usage_nouns={'subject':['prop']})
        self.actor = Entity('actor','てすと',category='child',agreement_class='feminine')
        self.prop = Entity('prop','てすと',category='object',agreement_class='neuter')
        self.project = SimpleNamespace(noun_categories={'living':NounCategory('living','Living'), 'child':NounCategory('child','Child',parent='living'), 'object':NounCategory('object','Object')}, roles={})

    def test_actual_OR_and_inherited_categories(self):
        self.assertTrue(self.matches(self.project,self.word,'subject',self.actor))
        self.assertTrue(self.matches(self.project,self.word,'subject',self.prop))
        self.assertFalse(self.matches(self.project,self.word,'missing',self.actor))

    def test_actual_inheritance_drift_is_caught_by_validator(self):
        from kotomi.core.project.models import NounCategory
        from kotomi.languages.polish import PolishLanguage
        fixture=json.loads((ROOT/'tests/fixtures/c1/v1.json').read_text())
        report=fixture['report'];report['verbs']=report['verbs'][:1]
        row=report['verbs'][0];row['current_roles']=[{'ref':'subject','matched_nouns':['actor','prop']}]
        self.project.entities={'actor':self.actor,'prop':self.prop}
        self.project.words={'verbs':{row['id']:self.word}}
        self.project.patterns={};self.project.instruction_language=PolishLanguage
        validator.validate_engine(report,self.project,self.matches,lambda *args:False)
        self.project.noun_categories['child']=NounCategory('child','Child',parent='object')
        with self.assertRaisesRegex(ValueError,'Role matches drift'):
            validator.validate_engine(report,self.project,self.matches,lambda *args:False)

    def test_actual_defaults_and_exact_nouns(self):
        from kotomi.core.project.models import RoleDefinition
        self.word.usage={'subject':[]};self.word.usage_nouns={}
        self.project.roles={'subject':RoleDefinition('subject','Subject','が',default_categories=['living'])}
        self.assertTrue(self.matches(self.project,self.word,'subject',self.actor))
        self.assertFalse(self.matches(self.project,self.word,'subject',self.prop))
        self.word.usage_nouns={'subject':['prop']}
        self.assertFalse(self.matches(self.project,self.word,'subject',self.actor))
        self.assertTrue(self.matches(self.project,self.word,'subject',self.prop))

    def test_actual_wildcard(self):
        self.word.usage={'subject':['*']}
        self.assertTrue(self.matches(self.project,self.word,'subject',self.actor))
        self.assertTrue(self.matches(self.project,self.word,'subject',self.prop))


if __name__ == '__main__':
    unittest.main()
