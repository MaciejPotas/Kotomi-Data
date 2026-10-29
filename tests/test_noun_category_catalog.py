"""Synthetic declaration and membership checks for extensible noun categories."""
import tempfile
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET
from tools.validate_repository import validate_semantic_categories


class NounCategoryCatalogTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root/'quiz_project.xml').write_text('''<quiz_project><dictionaries>
          <dictionary id="nouns" file="nouns.xml" schema="noun"/>
          <dictionary id="adjectives" file="adjectives.xml" schema="adjective"/>
          </dictionaries><semantic_categories file="categories.xml"/></quiz_project>''')
        (self.root/'nouns.xml').write_text('<dictionary schema="noun"><words><word id="sample" category="new_leaf"/></words></dictionary>')
        (self.root/'adjectives.xml').write_text('<dictionary schema="adjective"><words><word id="quality"><describes categories="new_leaf"/></word></words></dictionary>')
        self.catalog('<category id="base" selectable="false"/><category id="new_leaf" parent="base"/>')

    def catalog(self, value):
        (self.root/'categories.xml').write_text('<noun_categories schema_version="2">'+value+'</noun_categories>')

    def test_new_data_category_and_parent_are_accepted(self):
        validate_semantic_categories(self.root)

    def test_unknown_membership_is_rejected(self):
        self.catalog('<category id="base"/>')
        with self.assertRaisesRegex(AssertionError, 'Unknown noun category'):
            validate_semantic_categories(self.root)

    def test_invalid_graphs_are_rejected(self):
        for nodes, message in [
            ('<category id="new_leaf"/><category id="new_leaf"/>', 'Duplicate'),
            ('<category id="new_leaf" parent="missing"/>', 'Unknown'),
            ('<category id="new_leaf" parent="other"/><category id="other" parent="new_leaf"/>', 'Cyclic'),
            ('<category id="new_leaf" selectable="invalid"/>', 'selectable'),
            ('<category id="new_leaf" parent="one two"/>', 'Unknown'),
        ]:
            with self.subTest(nodes=nodes):
                self.catalog(nodes)
                with self.assertRaisesRegex(AssertionError, message):
                    validate_semantic_categories(self.root)

    def test_nonselectable_parent_cannot_be_assigned_to_noun(self):
        root = ET.parse(self.root/'nouns.xml').getroot()
        root.find('./words/word').set('category','base')
        ET.ElementTree(root).write(self.root/'nouns.xml')
        with self.assertRaisesRegex(AssertionError, 'nonselectable'):
            validate_semantic_categories(self.root)
