"""Reference-validation behavior on bounded files, never shipped vocabulary."""
from pathlib import Path
import shutil
import tempfile
import unittest
import xml.etree.ElementTree as ET
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("lexical_reference_validator", ROOT / "tools/validate_repository.py")
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)

class LexicalReferenceValidationTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name) / "fixture"
        shutil.copytree(Path(__file__).parent / "fixtures/lexical", self.root)

    def change(self, file, xpath, attributes):
        path = self.root / file
        tree = ET.parse(path)
        tree.getroot().find(xpath).attrib.update(attributes)
        tree.write(path, encoding="utf-8")

    def test_quiz_filter_values_schema(self):
        valid = '<quiz filters="adjective.type"><vocabulary_filters><filter key="adjective.type" allowed="i_adjective na_adjective" defaults="na_adjective" /></vocabulary_filters></quiz>'
        validator.validate_quiz_filter_configuration(ET.fromstring(valid))
        validator.validate_quiz_filter_configuration(ET.fromstring('<quiz filters="adjective.type"/>'))
        mutations = [valid.replace('defaults="na_adjective"', 'defaults=""'),
                     valid.replace('defaults="na_adjective"', 'defaults="missing"'),
                     valid.replace('adjective.type', 'verb[role:companion].category'),
                     valid.replace('i_adjective na_adjective', 'i_adjective i_adjective'),
                     valid.replace('</vocabulary_filters>', '<filter key="adjective.type" allowed="i_adjective" defaults="i_adjective"/></vocabulary_filters>')]
        for changed in mutations:
            with self.subTest(xml=changed), self.assertRaises(AssertionError):
                validator.validate_quiz_filter_configuration(ET.fromstring(changed))

    def test_lesson_and_context_share_one_word(self):
        validator.validate_lesson_references(self.root)
        validator.validate_context_references(self.root)

    def test_missing_lesson_word_is_rejected(self):
        self.change("lessons/lessons.xml", "./lessons/lesson/word/dictionary_ref", {"word": "missing"})
        with self.assertRaisesRegex(AssertionError, "missing word"):
            validator.validate_lesson_references(self.root)

    def test_unknown_context_dictionary_is_rejected(self):
        self.change("grammar/contexts.xml", "./context/option", {"dictionary": "missing"})
        with self.assertRaisesRegex(AssertionError, "missing word"):
            validator.validate_context_references(self.root)

    def test_missing_context_word_is_rejected(self):
        self.change("grammar/contexts.xml", "./context/option", {"word": "missing"})
        with self.assertRaisesRegex(AssertionError, "missing word"):
            validator.validate_context_references(self.root)

    def test_partial_reference_is_rejected(self):
        self.change("grammar/contexts.xml", "./context/option", {"word": ""})
        with self.assertRaisesRegex(AssertionError, "together"):
            validator.validate_context_references(self.root)

    def test_mixed_reference_and_inline_text_is_rejected(self):
        self.change("grammar/contexts.xml", "./context/option", {"kana": "other"})
        with self.assertRaisesRegex(AssertionError, "mix"):
            validator.validate_context_references(self.root)

    def test_lesson_count_and_labels_do_not_change_reference_rules(self):
        from copy import deepcopy
        path = self.root / 'lessons/lessons.xml'
        tree = ET.parse(path)
        lessons = tree.getroot().find('lessons')
        template = lessons[0]
        # One shared word, arbitrary group names, no minimum vocabulary size.
        for index, group in enumerate(('Tematyczne', 'Custom', 'Another')):
            lesson = deepcopy(template)
            lesson.set('id', f'lesson_{index}')
            lesson.set('group', group)
            lessons.append(lesson)
        tree.write(path, encoding='utf-8')
        validator.validate_lesson_references(self.root)
        for lesson in list(lessons):
            lessons.remove(lesson)
        tree.write(path, encoding='utf-8')
        validator.validate_lesson_references(self.root)

    def test_deleted_shared_word_invalidates_lesson_and_context(self):
        path = self.root / 'dictionaries/adverbs.xml'
        tree = ET.parse(path)
        words = tree.getroot().find('words')
        words.remove(words.find("word[@id='kinou']"))
        tree.write(path, encoding='utf-8')
        for validate in (validator.validate_lesson_references, validator.validate_context_references):
            with self.subTest(validator=validate.__name__):
                with self.assertRaisesRegex(AssertionError, 'missing word'):
                    validate(self.root)

    def test_all_quiz_references_resolve_independently_of_quiz_inventory(self):
        manifest_path = self.root / 'quiz_project.xml'
        manifest = ET.parse(manifest_path)
        ET.SubElement(manifest.getroot(), 'sentence_maps', file='maps.xml')
        ET.SubElement(manifest.getroot(), 'sentence_quizzes', file='quizzes.xml')
        manifest.write(manifest_path, encoding='utf-8')
        (self.root / 'maps.xml').write_text('<sentence_maps><sentence_patterns><sentence_pattern id="p" /></sentence_patterns></sentence_maps>', encoding='utf-8')
        root = ET.Element('sentence_quizzes')
        for index in range(3):
            quiz = ET.SubElement(root, 'quiz', id=f'arbitrary_{index}')
            patterns = ET.SubElement(quiz, 'patterns')
            ET.SubElement(patterns, 'pattern', ref='p')
        path = self.root / 'quizzes.xml'
        ET.ElementTree(root).write(path, encoding='utf-8')
        validator.validate_sentence_quiz_references(self.root)
        root[1].find('./patterns/pattern').set('ref', 'missing')
        ET.ElementTree(root).write(path, encoding='utf-8')
        with self.assertRaisesRegex(AssertionError, 'missing pattern'):
            validator.validate_sentence_quiz_references(self.root)

    def prepare_composite_quiz(self):
        manifest_path = self.root / 'quiz_project.xml'
        manifest = ET.parse(manifest_path)
        ET.SubElement(manifest.getroot(), 'sentence_maps', file='maps.xml')
        ET.SubElement(manifest.getroot(), 'sentence_quizzes', file='quizzes.xml')
        manifest.write(manifest_path, encoding='utf-8')
        (self.root / 'maps.xml').write_text(
            '<sentence_maps><sentence_patterns>'
            '<sentence_pattern id="plain"/><sentence_pattern id="unselected"/>'
            '<sentence_pattern id="inner"><patterns><pattern ref="plain"/></patterns></sentence_pattern>'
            '<sentence_pattern id="outer"><patterns><pattern ref="inner"/></patterns></sentence_pattern>'
            '</sentence_patterns></sentence_maps>', encoding='utf-8')

    def test_quiz_references_resolve_only_declared_composite_expansions(self):
        self.prepare_composite_quiz()
        path = self.root / 'quizzes.xml'
        for reference in ('plain', 'inner', 'inner / plain', 'outer / inner / plain'):
            path.write_text(f'<sentence_quizzes><quiz id="synthetic"><patterns><pattern ref="{reference}"/>'
                            '</patterns></quiz></sentence_quizzes>', encoding='utf-8')
            validator.validate_sentence_quiz_references(self.root)
        path.write_text('<sentence_quizzes><quiz id="synthetic"><patterns><pattern ref="inner / unselected"/>'
                        '</patterns></quiz></sentence_quizzes>', encoding='utf-8')
        with self.assertRaisesRegex(AssertionError, 'missing pattern'):
            validator.validate_sentence_quiz_references(self.root)

    def test_composite_reference_cycles_are_reported(self):
        self.prepare_composite_quiz()
        (self.root / 'maps.xml').write_text('<sentence_maps><sentence_patterns>'
            '<sentence_pattern id="loop"><patterns><pattern ref="loop"/></patterns></sentence_pattern>'
            '</sentence_patterns></sentence_maps>', encoding='utf-8')
        (self.root / 'quizzes.xml').write_text('<sentence_quizzes><quiz id="synthetic"><patterns>'
            '<pattern ref="loop"/></patterns></quiz></sentence_quizzes>', encoding='utf-8')
        with self.assertRaisesRegex(AssertionError, 'Cyclic composite'):
            validator.validate_sentence_quiz_references(self.root)
