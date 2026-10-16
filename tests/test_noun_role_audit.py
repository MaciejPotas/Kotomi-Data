"""C3 independent XML fixture v1. No shipped vocabulary is read."""
from copy import deepcopy
from pathlib import Path
import sys
import unittest
from xml.etree import ElementTree as ET

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from audit_noun_roles import check_local_scope, inventory


class AuditTests(unittest.TestCase):
    def setUp(self):
        self.nouns = {'sample': ET.fromstring('<word id="sample" category="parent" translation="test"/>')}
        self.verbs = {'action': ET.fromstring('<word id="action" translation="test"><usage>'
            '<role ref="object" accepts="parent" nouns="sample" government="frame"/>'
            '<role ref="target" nouns="sample"/></usage><forms><form ref="plain"/></forms></word>')}

    def test_inventory_includes_or_and_repeated_lists(self):
        rows, repeated = inventory(self.verbs, self.nouns)
        self.assertEqual([r['key'] for r in rows], ['action/object', 'action/target'])
        self.assertEqual(rows[0]['before']['accepts'], 'parent')
        self.assertEqual(rows[0]['noun_categories_before'], {'sample': 'parent'})
        self.assertEqual(repeated[0]['roles'], ['action/object', 'action/target'])

    def test_dangling_or_duplicate_reference_fails(self):
        role = self.verbs['action'].find('usage/role')
        for ids in ('missing', 'sample sample'):
            with self.subTest(ids=ids):
                role.set('nouns', ids)
                with self.assertRaises(ValueError): inventory(self.verbs, self.nouns)

    def test_local_changes_preserve_government_forms_and_role_order(self):
        candidate = deepcopy(self.verbs)
        role = candidate['action'].find('usage/role')
        role.attrib.pop('nouns')
        role.set('accepts', 'child')
        check_local_scope(self.verbs, candidate)
        for node, name in ((role, 'government'), (candidate['action'], 'translation'),
                           (candidate['action'].find('forms/form'), 'ref')):
            old = node.get(name)
            node.set(name, 'changed')
            with self.assertRaises(ValueError): check_local_scope(self.verbs, candidate)
            node.set(name, old)
        candidate['action'].find('usage').remove(role)
        with self.assertRaises(ValueError): check_local_scope(self.verbs, candidate)

    def test_noun_reclassification_preserves_all_other_fields(self):
        candidate = deepcopy(self.nouns)
        candidate['sample'].set('category', 'child')
        check_local_scope(self.nouns, candidate, noun=True)
        candidate['sample'].set('translation', 'changed')
        with self.assertRaises(ValueError): check_local_scope(self.nouns, candidate, noun=True)
