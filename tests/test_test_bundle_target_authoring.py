"""Content owns complete words and references the application grammar."""
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET
ROOT = Path(__file__).resolve().parents[1]

class ContentOwnershipTests(unittest.TestCase):
    def test_words_have_one_complete_entry(self):
        self.assertFalse((ROOT / "shared").exists())
        for path in ROOT.rglob("*.xml"):
            root = ET.parse(path).getroot()
            for node in root.iter():
                self.assertNotIn("shared_target", node.attrib)
            if root.tag == "dictionary":
                self.assertIsNone(root.find("editor"))
                for word in root.findall("./words/word"):
                    self.assertTrue(word.get("translation"), path)
                    self.assertTrue(word.get("kana"), path)

    def test_public_probe_has_no_source_grammar(self):
        tags = {"source_government", "source_noun_relations", "count_source_profiles",
                "cases", "agreement", "relations", "source_forms"}
        for path in (ROOT / 'instruction_languages/test').glob('*.xml'):
            self.assertFalse(tags & {node.tag for node in ET.parse(path).iter()}, path)
