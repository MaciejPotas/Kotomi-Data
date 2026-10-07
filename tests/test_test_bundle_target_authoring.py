"""Both source bundles reference one Japanese target; no target copies."""
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
PROBE = ROOT / 'instruction_languages/test'


class JapaneseTargetAuthoringTests(unittest.TestCase):
    def test_both_languages_reference_one_target_source(self):
        pairs = [('grammar/grammar_rules.xml', 'grammar.xml'),
                 ('grammar/counting.xml', 'counting.xml')]
        pairs.extend((f'dictionaries/{name}.xml', f'{name}.xml') for name in (
            'nouns', 'verbs', 'adjectives', 'counters', 'numbers', 'copulas',
            'interrogatives', 'connectors'))
        for left, right in pairs:
            paths = [ROOT / left, PROBE / right]
            references = []
            for path in paths:
                source = ET.parse(path).getroot()
                references.append((path.parent / source.attrib['shared_target']).resolve())
                self.assertTrue(references[-1].is_file())
                for node in source.iter():
                    self.assertFalse({'kana', 'kanji', 'romaji', 'category', 'particle'} & node.attrib.keys())
            self.assertEqual(*references)

    def test_public_probe_has_no_source_grammar(self):
        tags = {'source_government', 'source_noun_relations', 'count_source_profiles',
                'cases', 'agreement', 'relations', 'source_forms'}
        for path in PROBE.glob('*.xml'):
            self.assertFalse(tags & {node.tag for node in ET.parse(path).iter()}, path)

    def test_shared_target_has_no_source_translations_or_grammar(self):
        for path in (ROOT / 'shared/ja').rglob('*.xml'):
            root = ET.parse(path).getroot()
            self.assertEqual('ja', root.get('target_language_id'))
            for node in root.iter():
                self.assertNotIn('translation', node.attrib)
                self.assertNotIn('government', node.attrib)
                self.assertNotIn(node.tag, {'cases', 'agreement', 'relations', 'polish_forms',
                    'polish_government', 'polish_noun_relations', 'count_source_profiles'})
