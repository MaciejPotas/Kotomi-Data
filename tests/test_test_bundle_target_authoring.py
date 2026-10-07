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

    def test_only_canonical_production_content(self):
        self.assertFalse((ROOT / "instruction_languages").exists())
        self.assertTrue((ROOT / "quiz_project.xml").is_file())
