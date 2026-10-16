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
