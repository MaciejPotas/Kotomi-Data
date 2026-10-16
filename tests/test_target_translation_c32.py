"""C3.2 validator fixture v1: synthetic XML only."""
from pathlib import Path
import sys
import unittest
import xml.etree.ElementTree as ET
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from validate_repository import validate_target_translation,unexpected_word_form_attributes


class TargetTranslationTests(unittest.TestCase):
    def test_legacy_and_optional_gloss(self):
        for schema,xml in [('verb','<form ref="dictionary"/>'),
                           ('adjective','<form ref="dictionary"/>'),
                           ('verb','<form ref="dictionary" translation="pożyczam od kogoś" target_translation="pożyczam"/>')]:
            form=ET.fromstring(xml)
            self.assertEqual(unexpected_word_form_attributes(form.attrib),set())
            validate_target_translation(schema,form)

    def test_bad_schema_or_empty_gloss(self):
        for schema,value in [('verb',''),('verb','  '),('adjective','pożyczam'),('noun','pożyczam')]:
            with self.subTest(schema=schema,value=value):
                with self.assertRaisesRegex(AssertionError,'target_translation'):
                    validate_target_translation(schema,ET.Element('form',target_translation=value))
