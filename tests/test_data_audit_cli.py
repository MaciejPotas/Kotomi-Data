"""Audit report fixture v1, independent of production Content and engine files."""
from types import SimpleNamespace as NS
from pathlib import Path
import unittest
import importlib.util
_spec = importlib.util.spec_from_file_location('kotomi_data_audit', Path(__file__).resolve().parents[1]/'tools/diagnostics/data_audit.py')
_module = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_module)
audit_project, render_report = _module.audit_project, _module.render_report


def fixture():
    word = NS(id='fixture', translation=' ', kana='かな', forms={}, usage={},
              agreement_class='', cases={}, usage_nouns={})
    return NS(words={'sample': {'fixture': word}}, dictionary_paths={'sample': Path('sample.xml')},
              manifest_path=None, dictionary_schemas={'sample': 'generic'}, form_definitions={},
              dictionary_configs={'sample': NS(required_fields=['translation','kana'])},
              validate=lambda **kw: [], instruction_language=NS(capabilities=NS(cases=())))


class AuditTests(unittest.TestCase):
    def test_missing_required_translation_is_located(self):
        report = audit_project(fixture())
        self.assertEqual(report['words_scanned'], 1)
        self.assertEqual(report['errors'], 1)
        self.assertEqual(report['findings'][0]['file'], 'sample.xml')
        self.assertIn('sample/fixture', render_report(report))

    def test_optional_catalog_form_is_inventory_not_error(self):
        project = fixture(); project.words['sample']['fixture'].translation = 'fixture'
        project.form_definitions = {'generic': {'optional': object()}}
        report = audit_project(project)
        self.assertEqual(report['errors'], 0)
        self.assertEqual(report['inventory']['sample/fixture']['absent_catalog_forms'], ['optional'])

    def test_zero_numeric_value_is_present(self):
        project = fixture(); project.dictionary_configs['sample'].required_fields = ['value']
        project.words['sample']['fixture'].number_value = 0
        self.assertEqual(audit_project(project)['errors'], 0)

    def test_unknown_dictionary_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'Unknown dictionary'):
            audit_project(fixture(), 'missing')

    def test_repeated_audit_is_deterministic_and_read_only(self):
        project = fixture(); before = repr(project.words)
        self.assertEqual(audit_project(project), audit_project(project))
        self.assertEqual(repr(project.words), before)

    def test_engine_reference_errors_are_preserved(self):
        project = fixture()
        project.validate = lambda **kw: ["ERROR: Word 'sample/fixture' uses unknown category 'missing'."]
        report = audit_project(project)
        self.assertEqual(report['errors'], 2)
        self.assertTrue(all(item['word'] == 'fixture' for item in report['findings']))


class FormAuditTests(unittest.TestCase):
    """Fixture v2: bounded fake engine catalog/generator, no production Content."""

    def setUp(self):
        from unittest.mock import patch
        self.project = fixture()
        self.word = self.project.words['sample']['fixture']
        self.word.translation = 'fixture'
        self.word.type = 'godan'
        self.word.kana = 'かく'
        self.project.dictionary_schemas['sample'] = 'verb'
        self.project.form_definitions['verb'] = {
            name: NS(is_selectable=name == 'past_plain')
            for name in ('dictionary', 'past_plain', 'optional', 'unsupported')}
        self.word.forms = {'dictionary': self.form('かく', 'piszę')}
        generator = NS(generate_forms=lambda *_: {'dictionary': 'かく', 'past_plain': 'かいた'},
                       FormGenerationError=ValueError)
        self.patch = patch.dict('sys.modules', {'kotomi.core.dictionary.forms': generator})
        self.patch.start()
        self.addCleanup(self.patch.stop)

    @staticmethod
    def form(kana, translation, **kwargs):
        return NS(kana=kana, translation=translation, target_translation=kwargs.get('target_translation', ''),
                  agreement_translations=kwargs.get('agreement_translations', {}))

    def test_complete_verb_with_noun_exception_is_still_complete(self):
        self.word.usage_nouns = {'target': ['fixture_noun']}
        report = audit_project(self.project)
        self.assertEqual((report['errors'], report['warnings'], report['info']), (0, 0, 1))
        self.assertEqual(report['dictionaries']['sample']['complete'], 1)
        self.assertEqual(report['dictionaries']['sample']['review_notes'], 1)
        self.assertIn('Info: 1', render_report(report))

    def test_successful_execution_is_distinct_from_data_findings(self):
        self.word.forms['past_plain'] = self.form('かいた', '')
        report = audit_project(self.project)
        self.assertTrue(report['execution_success'])
        self.assertEqual(report['warnings'], 1)

    def test_generated_and_optional_forms_are_not_missing_obligations(self):
        report = audit_project(self.project)
        row = report['inventory']['sample/fixture']
        self.assertEqual(row['generated_forms'], ['past_plain'])
        self.assertIn('optional', row['optional_forms_not_explicit'])
        self.assertIn('unsupported', row['unsupported_by_generator'])
        self.assertEqual(row['missing_required_forms'], [])
        self.assertIn('no universal', row['requirements_status'])
        self.assertIn('runtime uses stored', row['generation_scope'])
        self.assertEqual(report['dictionaries']['sample']['incomplete'], 0)

    def test_missing_required_form_even_when_generator_can_supply_it(self):
        from unittest.mock import patch
        with patch.object(_module, 'fixed_form_requirements', return_value={('sample', 'fixture'): {'past_plain': {'fixed_pattern'}}}):
            report = audit_project(self.project)
        row = report['inventory']['sample/fixture']
        self.assertEqual(row['missing_required_forms'], ['past_plain'])
        self.assertEqual(report['warnings'], 1)
        self.assertEqual(report['dictionaries']['sample']['incomplete'], 1)

    def test_missing_translation_is_a_data_gap(self):
        self.word.forms['past_plain'] = self.form('かいた', '')
        report = audit_project(self.project)
        self.assertEqual(report['warnings'], 1)
        self.assertEqual(report['dictionaries']['sample']['incomplete'], 1)

    def test_contextual_translation_is_not_a_missing_data_error(self):
        self.word.forms['past_plain'] = self.form('かいた', '', target_translation='napisałem')
        report = audit_project(self.project)
        self.assertEqual(report['warnings'], 0)
        self.assertEqual(report['dictionaries']['sample']['complete'], 1)
        self.assertIn('past_plain', report['inventory']['sample/fixture']['contextual_translations'])
        self.assertIn('unverified', report['findings'][0]['message'])

    def test_unknown_conjugation_difference_needs_review_not_missing_data(self):
        self.word.forms['past_plain'] = self.form('ちがう', 'napisałem')
        report = audit_project(self.project)
        self.assertEqual(report['warnings'], 1)
        self.assertFalse(report['findings'][0]['affects_completeness'])
        self.assertEqual(report['dictionaries']['sample']['complete'], 1)
        self.assertIn('needs review', report['findings'][0]['message'])

    def test_only_known_na_contractions_are_recognized(self):
        self.word.type = 'na_adjective'
        self.word.kana = 'しずか'
        self.assertTrue(_module.known_conjugation_variant(self.word, 'しずかじゃなかった', 'しずかではなかった'))
        self.assertFalse(_module.known_conjugation_variant(self.word, 'べつじゃなかった', 'しずかではなかった'))
        self.word.type = 'godan'
        self.assertFalse(_module.known_conjugation_variant(self.word, 'しずかじゃなかった', 'しずかではなかった'))

    def test_supported_variant_is_info_in_report(self):
        from unittest.mock import patch
        self.word.type = 'na_adjective'
        self.word.kana = 'しずか'
        self.project.dictionary_schemas['sample'] = 'adjective'
        self.project.form_definitions['adjective'] = {'negative': NS(is_selectable=True)}
        self.word.forms = {'negative': self.form('しずかじゃなかった', 'nie był spokojny')}
        with patch.dict('sys.modules', {'kotomi.core.dictionary.forms': NS(
                generate_forms=lambda *_: {'negative': 'しずかではなかった'}, FormGenerationError=ValueError)}):
            report = audit_project(self.project)
        self.assertEqual((report['errors'], report['warnings'], report['info']), (0, 0, 1))
        self.assertEqual(report['dictionaries']['sample']['complete'], 1)

    def test_redundant_optional_override_is_info(self):
        report = audit_project(self.project, word_validator=lambda _: [NS(
            severity='WARNING', message='Redundant source-language form overrides will be removed on save.')])
        self.assertEqual(report['info'], 1)
        self.assertEqual(report['warnings'], 0)
        self.assertEqual(report['dictionaries']['sample']['complete'], 1)
