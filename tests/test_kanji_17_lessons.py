"""Kanji 17 source-sheet coverage and shared-dictionary-reference contracts."""
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]

EXPECTED = {
    "ola_kanji_166_170": [
        ("adjectives", "hiroi"), ("verbs", "hirogeru"),
        ("nouns", "hiroshima"), ("nouns", "koukoku"),
        ("adjectives", "koudai"), ("adjectives", "mijikai"),
        ("nouns", "tanki_period"), ("adjectives", "tanki_short_tempered"),
        ("expressions", "tanjikan"), ("nouns", "tansho"),
        ("nouns", "tanka_poem"), ("adjectives", "hikui"),
        ("nouns", "teikiatsu"), ("verbs", "teika_suru"),
        ("adjectives", "saitei"), ("nouns", "teion"),
        ("expressions", "teireberu_no"), ("adjectives", "kurai"),
        ("expressions", "makkura"), ("verbs", "anki_suru"),
        ("nouns", "anzan"), ("nouns", "ansatsu"),
        ("nouns", "angou"), ("adjectives", "tooi"),
        ("verbs", "enryo_suru"), ("nouns", "ensoku"),
        ("nouns", "eien"), ("nouns", "enpou"),
        ("nouns", "enkyori"),
    ],
    "ola_kanji_171_175": [
        ("adjectives", "chikai"), ("adverbs", "chikaku_ni"),
        ("adverbs", "saikin"), ("nouns", "kinjo"),
        ("nouns", "fukin"), ("nouns", "kinki_region"),
        ("adjectives", "hayai_early"), ("nouns", "hayaoki"),
        ("adverbs", "souchou"), ("adverbs", "sassoku"),
        ("adjectives", "osoi_late"), ("verbs", "okureru"),
        ("nouns", "chikoku"), ("adjectives", "omoi"),
        ("verbs", "kasaneru"), ("nouns", "taijuu"),
        ("expressions", "nijuu"), ("nouns", "juuryoku"),
        ("adjectives", "kichou"), ("adjectives", "karui"),
        ("expressions", "migaru"), ("adjectives", "kigaru"),
        ("adjectives", "tegaru"), ("adjectives", "keihaku"),
        ("verbs", "keishi_suru"),
    ],
}

class Kanji17LessonsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lessons = ET.parse(ROOT / "lessons/lessons.xml").getroot()
        cls.dictionaries = {
            name: {word.get("id"): word for word in
                   ET.parse(ROOT / "dictionaries" / (name + ".xml")).findall("./words/word")}
            for name in ("nouns", "verbs", "adjectives", "adverbs", "expressions")
        }

    def test_two_lessons_use_only_valid_references_in_source_order(self):
        for lesson_id, expected in EXPECTED.items():
            with self.subTest(lesson=lesson_id):
                lesson = self.lessons.find("./lessons/lesson[@id='" + lesson_id + "']")
                self.assertIsNotNone(lesson)
                self.assertEqual(("Ola", "Kanji"), (lesson.get("group"), lesson.get("main")))
                self.assertEqual([], lesson.findall("./local_word"))
                words = lesson.findall("./word")
                self.assertEqual(len(expected), len(words))
                for index, (entry, (dictionary, word)) in enumerate(zip(words, expected), 1):
                    self.assertEqual(
                        lesson_id + "_" + format(index, "03d"), entry.get("id"))
                    ref = entry.find("dictionary_ref")
                    self.assertIsNotNone(ref)
                    self.assertEqual((dictionary, word), (ref.get("dictionary"), ref.get("word")))
                    linked = self.dictionaries[dictionary][word]
                    self.assertTrue(linked.get("kana"))
                    self.assertTrue(linked.get("kanji"))
                    self.assertTrue(linked.get("translation"))

    def test_distinct_early_and_fast_japanese_adjectives(self):
        early = self.dictionaries["adjectives"]["hayai_early"]
        fast = self.dictionaries["adjectives"]["hayai"]
        self.assertEqual(("はやい", "早い", "wczesny"),
                         (early.get("kana"), early.get("kanji"), early.get("translation")))
        self.assertEqual("速い", fast.get("kanji"))
        late = self.dictionaries["adjectives"]["osoi_late"]
        self.assertEqual(("遅い", "późny"), (late.get("kanji"), late.get("translation")))

    def test_family_words_have_explicit_plural_cases(self):
        expected = {"kazoku": ("feminine", "rodzina"),
                    "ryoushin": ("plural_masculine_personal", "rodzice"),
                    "shimai": ("plural_non_masculine_personal", "siostry")}
        cases = "nominative genitive dative accusative instrumental locative vocative".split()
        for identifier, (klass, nominative) in expected.items():
            noun = self.dictionaries["nouns"][identifier]
            self.assertEqual(klass, noun.find("agreement").get("class"))
            values = noun.find("cases")
            self.assertEqual(nominative, values.get("nominative"))
            self.assertTrue(all(values.get(name) for name in cases))

    def test_new_verbs_have_finite_plural_agreement_forms(self):
        new_verbs = "hirogeru teika_suru anki_suru enryo_suru okureru kasaneru keishi_suru".split()
        finite = "dictionary polite_nonpast plain_negative polite_negative past_plain past_polite past_negative_plain past_negative_polite".split()
        for identifier in new_verbs:
            verb = self.dictionaries["verbs"][identifier]
            for form in finite:
                with self.subTest(verb=identifier, form=form):
                    node = verb.find("./forms/form[@ref='" + form + "']")
                    self.assertIsNotNone(node)
                    agreement = {value.get("class"): value.get("value")
                                 for value in node.findall("./agreement_translations/translation")}
                    self.assertTrue(agreement.get("plural_masculine_personal"))
                    self.assertTrue(agreement.get("plural_non_masculine_personal"))

if __name__ == "__main__":
    unittest.main()
