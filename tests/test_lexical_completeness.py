"""Coverage contracts for reviewed lexical data and explicit exceptions."""
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET
ROOT = Path(__file__).resolve().parents[1]
CASES = set('nominative genitive dative accusative instrumental locative vocative'.split())
NON_COUNTABLE = set('gohan jikan music okane television naka oku ashita hitori saisho detarame'.split())
VERBS = set('dictionary polite_nonpast plain_negative polite_negative past_plain past_polite past_negative_plain past_negative_polite te_form potential passive causative tara volitional imperative'.split())
ADJECTIVES = set('predicate_plain_nonpast predicate_polite_nonpast predicate_plain_negative predicate_polite_negative predicate_plain_past predicate_polite_past predicate_plain_past_negative predicate_polite_past_negative attributive_nonpast connective adverbial conditional nominalized appearance_sou excessive_sugiru'.split())
NONPRODUCTIVE = {'aru_possessive': {'potential', 'passive', 'causative'}, 'aru_existential': {'potential', 'passive', 'causative'}, 'dekiru': {'potential', 'passive'}, 'mieru': {'potential', 'passive'}, 'chigau': {'passive'}, 'hareru': {'passive'}, 'kumoru': {'passive'}}

def words(name):
    return {w.get('id'): w for w in ET.parse(ROOT / 'dictionaries' / f'{name}.xml').findall('./words/word')}

class LexicalCompletenessTests(unittest.TestCase):
    def test_nouns_have_all_cases_and_counting_or_documented_exception(self):
        nouns = words('nouns')
        self.assertTrue(NON_COUNTABLE <= nouns.keys())
        bindings = {c.get('ref'): c for c in ET.parse(ROOT / 'grammar/counting.xml').findall('./counter_bindings/class')}
        counters = words('counters')
        for identifier, noun in nouns.items():
            with self.subTest(noun=identifier):
                self.assertTrue(all(noun.find('cases').get(c, '').strip() for c in CASES))
                counting = noun.find('counting')
                if identifier in NON_COUNTABLE:
                    self.assertIsNone(counting)
                    continue
                self.assertIsNotNone(counting)
                self.assertTrue(counting.get('classes', '').split())
                for cls in counting.get('classes').split():
                    counter = counters[bindings[cls].get('default_counter')]
                    self.assertIsNotNone(counter.find("./quantity_realizations/realization[@symbol='how_many']"))
                values = {}
                for form in counting.findall('./source_forms/form'):
                    profile = form.get('profile')
                    self.assertIn(profile, ('few', 'many'))
                    for case in form.get('cases').split():
                        self.assertNotIn((profile, case), values)
                        values[profile, case] = form.get('value', '').strip()
                for profile in ('few', 'many'):
                    self.assertEqual({c for (p, c), v in values.items() if p == profile and v}, CASES)

    def test_usable_forms_have_kana_written_form_and_translation(self):
        for dictionary, required in [('verbs', VERBS), ('adjectives', ADJECTIVES)]:
            for identifier, word in words(dictionary).items():
                with self.subTest(dictionary=dictionary, word=identifier):
                    forms = {f.get('ref'): f for f in word.findall('./forms/form')}
                    excluded = NONPRODUCTIVE.get(identifier, set()) if dictionary == 'verbs' else set()
                    self.assertEqual(set(forms), required - excluded)
                    for name, form in forms.items():
                        for field in ('kana', 'kanji', 'translation'):
                            self.assertTrue(form.get(field, '').strip(), (identifier, name, field))

    def test_adjective_overrides_are_complete_and_nonredundant(self):
        classes = 'masculine_personal masculine_animate masculine_inanimate feminine neuter plural_non_masculine_personal'.split()
        for identifier, word in words('adjectives').items():
            with self.subTest(word=identifier):
                common = {c: n.get('value') for n in word.findall('./polish_forms/common') for c in n.get('cases').split()}
                specific = {}
                for n in word.findall('./polish_forms/override'):
                    for cls in n.get('classes').split():
                        for case in n.get('cases').split():
                            self.assertNotEqual(n.get('value'), common.get(case))
                            self.assertNotIn((cls, case), specific)
                            specific[cls, case] = n.get('value')
                self.assertTrue(all(specific.get((cls, c), common.get(c)) for cls in classes for c in CASES))

    def test_reviewed_irregulars_and_japanese_variants(self):
        for identifier, form, expected in [('shinu','te_form','umarłszy'),('ageru_give','te_form','dając komuś'),('tomaru','te_form','zatrzymując się')]:
            self.assertEqual(words('verbs')[identifier].find(f"./forms/form[@ref='{form}']").get('translation'), expected)
        for identifier, form, kana, kanji in [('kuru','past_plain','きた','来た'),('iku','te_form','いって','行って')]:
            node = words('verbs')[identifier].find(f"./forms/form[@ref='{form}']")
            self.assertEqual((node.get('kana'),node.get('kanji')), (kana,kanji))
        node = words('adjectives')['kirei'].find("./forms/form[@ref='predicate_polite_negative']")
        self.assertEqual((node.get('kana'),node.get('kanji')), ('きれいじゃありません','綺麗じゃありません'))
