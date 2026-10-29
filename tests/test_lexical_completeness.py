"""Validate defined lexical forms without enforcing artificial completeness inventories."""
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
CASES = set('nominative genitive dative accusative instrumental locative vocative'.split())


def words(name):
    return {w.get('id'): w for w in ET.parse(ROOT / 'dictionaries' / f'{name}.xml').findall('./words/word')}

class LexicalCompletenessTests(unittest.TestCase):
    def assert_valid_noun_forms(self, noun, bindings, counters):
        # Noun cases are used by the generator and must remain complete.
        cases = noun.find('cases')
        self.assertIsNotNone(cases)
        self.assertTrue(all(cases.get(case, '').strip() for case in CASES))

        # A Japanese counter is not meaningful for every lexical sense.
        # In particular, Polish few/many inflections can exist without one.
        counting = noun.find('counting')
        if counting is None:
            return
        for cls in counting.get('classes', '').split():
            self.assertIn(cls, bindings)
            counter_id = bindings[cls].get('default_counter')
            self.assertIn(counter_id, counters)
            self.assertIsNotNone(
                counters[counter_id].find(
                    "./quantity_realizations/realization[@symbol='how_many']"
                )
            )

        values = {}
        for form in counting.findall('./source_forms/form'):
            profile = form.get('profile')
            self.assertIn(profile, ('few', 'many'))
            cases_for_form = form.get('cases', '').split()
            self.assertTrue(cases_for_form)
            self.assertTrue(form.get('value', '').strip())
            for case in cases_for_form:
                self.assertIn(case, CASES)
                self.assertNotIn((profile, case), values)
                values[profile, case] = form.get('value').strip()

        # Validate every declared Polish plural profile, but do not invent
        # missing profiles or Japanese counters solely to pass a coverage test.
        for profile in {profile for profile, _ in values}:
            self.assertEqual(
                {case for current_profile, case in values if current_profile == profile},
                CASES,
            )

    def test_nouns_have_cases_and_valid_declared_counting(self):
        bindings = {
            cls.get('ref'): cls
            for cls in ET.parse(ROOT / 'grammar/counting.xml').findall('./counter_bindings/class')
        }
        counters = words('counters')
        for identifier, noun in words('nouns').items():
            with self.subTest(noun=identifier):
                self.assert_valid_noun_forms(noun, bindings, counters)

    def assert_valid_declared_word_forms(self, word):
        seen = set()
        for form in word.findall('./forms/form'):
            name = form.get('ref', '').strip()
            self.assertTrue(name)
            self.assertNotIn(name, seen)
            seen.add(name)
            # Written kanji is optional for kana-only vocabulary. If given,
            # it must not be an empty placeholder.
            for field in ('kana', 'translation'):
                self.assertTrue(form.get(field, '').strip(), (name, field))
            if 'kanji' in form.attrib:
                self.assertTrue(form.get('kanji', '').strip(), (name, 'kanji'))

    def test_declared_verb_and_adjective_forms_are_valid(self):
        for dictionary in ('verbs', 'adjectives'):
            for identifier, word in words(dictionary).items():
                with self.subTest(dictionary=dictionary, word=identifier):
                    self.assert_valid_declared_word_forms(word)

    def test_counterless_noun_needs_no_inventory_exception(self):
        noun = ET.Element('word', id='synthetic_removed_word')
        ET.SubElement(noun, 'cases', {case: 'sample' for case in CASES})
        self.assert_valid_noun_forms(noun, {}, {})

    def test_polish_plurals_can_exist_without_japanese_counter(self):
        noun = ET.Element('word', id='synthetic_collective')
        ET.SubElement(noun, 'cases', {case: 'sample' for case in CASES})
        counting = ET.SubElement(noun, 'counting')
        forms = ET.SubElement(counting, 'source_forms')
        ET.SubElement(
            forms, 'form',
            profile='few', cases=' '.join(sorted(CASES)), value='examples',
        )
        self.assert_valid_noun_forms(noun, {}, {})

    def test_declared_counter_must_resolve(self):
        noun = ET.Element('word', id='synthetic_invalid_counter')
        ET.SubElement(noun, 'cases', {case: 'sample' for case in CASES})
        ET.SubElement(noun, 'counting', classes='nonexistent_counter')
        with self.assertRaises(AssertionError):
            self.assert_valid_noun_forms(noun, {}, {})

    def test_declared_plural_profile_must_cover_all_cases(self):
        noun = ET.Element('word', id='synthetic_partial_plural')
        ET.SubElement(noun, 'cases', {case: 'sample' for case in CASES})
        forms = ET.SubElement(ET.SubElement(noun, 'counting'), 'source_forms')
        ET.SubElement(forms, 'form', profile='few', cases='nominative', value='examples')
        with self.assertRaises(AssertionError):
            self.assert_valid_noun_forms(noun, {}, {})

    def test_partial_word_paradigm_is_valid_but_blank_declared_form_is_not(self):
        word = ET.Element('word', id='synthetic_verb')
        forms = ET.SubElement(word, 'forms')
        form = ET.SubElement(forms, 'form', ref='dictionary', kana='てすと', translation='test')
        self.assert_valid_declared_word_forms(word)
        form.set('translation', '')
        with self.assertRaises(AssertionError):
            self.assert_valid_declared_word_forms(word)

    def test_adjective_overrides_are_complete_and_nonredundant(self):
        classes = 'masculine_personal masculine_animate masculine_inanimate feminine neuter plural_non_masculine_personal'.split()
        explicit_plural_class = 'plural_masculine_personal'
        for identifier, word in words('adjectives').items():
            with self.subTest(word=identifier):
                common = {c: n.get('value') for n in word.findall('./polish_forms/common') for c in n.get('cases').split()}
                specific = {}
                for n in word.findall('./polish_forms/override'):
                    for cls in n.get('classes').split():
                        for case in n.get('cases').split():
                            # Plural masculine-personal cells are explicit even
                            # when a surface form happens to equal common:
                            # another class must not erase this paradigm.
                            if cls != explicit_plural_class:
                                self.assertNotEqual(n.get('value'), common.get(case))
                            self.assertNotIn((cls, case), specific)
                            specific[cls, case] = n.get('value')
                self.assertTrue(all(specific.get((cls, c), common.get(c)) for cls in classes for c in CASES))
                self.assertTrue(all(specific.get((explicit_plural_class, c)) for c in CASES))

    def test_reviewed_irregulars_and_japanese_variants(self):
        for identifier, form, expected in [('shinu','te_form','umarłszy'),('ageru_give','te_form','dając komuś'),('tomaru','te_form','zatrzymując się')]:
            self.assertEqual(words('verbs')[identifier].find(f"./forms/form[@ref='{form}']").get('translation'), expected)
        for identifier, form, kana, kanji in [('kuru','past_plain','きた','来た'),('iku','te_form','いって','行って')]:
            node = words('verbs')[identifier].find(f"./forms/form[@ref='{form}']")
            self.assertEqual((node.get('kana'),node.get('kanji')), (kana,kanji))
        node = words('adjectives')['kirei'].find("./forms/form[@ref='predicate_polite_negative']")
        self.assertEqual((node.get('kana'),node.get('kanji')), ('きれいじゃありません','綺麗じゃありません'))
