"""Regression checks for Szymon's reference-only first lesson."""
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
CASES = set("nominative genitive dative accusative instrumental locative vocative".split())
NOUN_IDS = ["getsuyoubi","kayoubi","suiyoubi","mokuyoubi","kinyoubi","doyoubi","nichiyoubi","tatemono","yuubinkyoku","byouin","biru","jimusitsu","eigakan","ginkou","aji","programmer","kikitori","shuumatsu","fukushuu","madogiwazoku"]
COUNTED_NOUNS = set(["tatemono","yuubinkyoku","byouin","biru","jimusitsu","eigakan","ginkou","aji","programmer","shuumatsu","fukushuu","madogiwazoku"])

class SzymonFirstLessonTests(unittest.TestCase):
    def test_seven_groups_use_58_unique_dictionary_references(self):
        root = ET.parse(ROOT / "lessons/lessons.xml").getroot()
        lessons = [lesson for lesson in root.findall("./lessons/lesson") if lesson.get("group") == "Szymon" and lesson.get("main") == "pierwsza"]
        self.assertEqual(7, len(lessons))
        refs = [(word.get("dictionary"), word.get("word")) for lesson in lessons for word in lesson.findall("./word/dictionary_ref")]
        self.assertEqual(58, len(refs))
        self.assertEqual(58, len(set(refs)))
        self.assertTrue(all(not lesson.findall(".//local_word") for lesson in lessons))
        for dictionary, word in refs:
            with self.subTest(dictionary=dictionary, word=word):
                dictionary_root = ET.parse(ROOT / "dictionaries" / (dictionary + ".xml")).getroot()
                self.assertIsNotNone(dictionary_root.find("./words/word[@id='" + word + "']"))

    def test_new_nouns_have_complete_cases_and_counting_where_appropriate(self):
        root = ET.parse(ROOT / "dictionaries/nouns.xml").getroot()
        for identifier in NOUN_IDS:
            with self.subTest(noun=identifier):
                noun = root.find("./words/word[@id='" + identifier + "']")
                self.assertIsNotNone(noun)
                self.assertEqual(CASES, {case for case in CASES if noun.find("cases").get(case)})
                counting = noun.find("counting")
                if identifier not in COUNTED_NOUNS:
                    self.assertIsNone(counting)
                    continue
                self.assertIsNotNone(counting)
                for profile in ("few", "many"):
                    actual = {case for form in counting.findall("./source_forms/form") if form.get("profile") == profile for case in form.get("cases").split()}
                    self.assertEqual(CASES, actual)

    def test_new_adjectives_and_sumu_have_fifteen_filled_forms(self):
        for dictionary, ids in (("adjectives", ("shoppai", "saikou", "saitei")), ("verbs", ("sumu",))):
            root = ET.parse(ROOT / "dictionaries" / (dictionary + ".xml")).getroot()
            for identifier in ids:
                with self.subTest(dictionary=dictionary, word=identifier):
                    word = root.find("./words/word[@id='" + identifier + "']")
                    self.assertIsNotNone(word)
                    forms = word.findall("./forms/form")
                    self.assertEqual(15, len(forms))
                    self.assertTrue(all(form.get("kana") and form.get("kanji") and form.get("translation") for form in forms))
        verbs = ET.parse(ROOT / "dictionaries/verbs.xml").getroot()
        self.assertEqual("住んで", verbs.find("./words/word[@id='sumu']/forms/form[@ref='te_form']").get("kanji"))

    def test_sumu_uses_ni_target_for_places_not_de_location(self):
        verbs = ET.parse(ROOT / "dictionaries/verbs.xml").getroot()
        usage = verbs.find("./words/word[@id='sumu']/usage")
        self.assertIsNotNone(usage)
        self.assertEqual([{"ref": "target", "accepts": "place"}],
                         [role.attrib for role in usage.findall("role")])

    def test_sundeimasu_is_not_a_separate_vocabulary_entry(self):
        roots = [ET.parse(ROOT / "dictionaries" / (name + ".xml")).getroot() for name in ("verbs", "expressions")]
        self.assertFalse(any(word.get("id") == "sundeimasu" or word.get("kana") == "すんでいます" for root in roots for word in root.findall("./words/word")))

    def test_demonstrative_polish_forms_are_explicit(self):
        words = ET.parse(ROOT / "dictionaries/demonstratives.xml").getroot()
        for identifier in ("kore", "sore", "are"):
            node = words.find("./words/word[@id='" + identifier + "']/cases")
            self.assertEqual(CASES, {case for case in CASES if node.get(case)})
        for identifier in ("kono", "sono", "ano"):
            node = words.find("./words/word[@id='" + identifier + "']/polish_forms")
            self.assertIsNotNone(node)
            self.assertTrue(node.findall("override"))

if __name__ == "__main__":
    unittest.main()
