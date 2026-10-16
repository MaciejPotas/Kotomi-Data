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

    def test_existing_catalog_cannot_drift_on_both_sides_of_engine_comparison(self):
        from audit_noun_roles import validate_catalog_extension
        before = {'parent': {'id':'parent'}}
        after = {**before, 'child': {'id':'child', 'parent':'parent'}}
        validate_catalog_extension(before, after)
        after['parent'] = {'id':'parent', 'parent':'child'}
        with self.assertRaisesRegex(ValueError, 'existing category'):
            validate_catalog_extension(before, after)


class DecisionTests(unittest.TestCase):
    """Independent C3 decision fixture v2; approved values are authored literals."""
    def setUp(self):
        from audit_noun_roles import validate_decisions
        self.validate_decisions = validate_decisions
        self.before = {'build': ET.fromstring('''<word id="build"><usage>
          <role ref="object" nouns="house park exception" government="direct_object"/>
          <role ref="subject" accepts="person"/>
          </usage><forms><form ref="plain"/><form ref="negative"/></forms></word>''')}
        self.after = deepcopy(self.before)
        role = self.after['build'].find('usage/role')
        role.attrib.update(accepts='building', nouns='exception')
        self.decisions = {'build/object': {
            'target': {'ref':'object', 'accepts':'building', 'nouns':'exception', 'government':'direct_object'},
            'added':['tower'], 'removed':['park'], 'status':'retained_exception',
            'reason_pl':'Budynki oraz zatwierdzony wyjątek.'}}
        self.pairs = [dict(key='build/object', before=['exception','house','park'],
                           after=['exception','house','tower'], added=['tower'], removed=['park']),
                      dict(key='build/subject', before=['exception'], after=['exception'], added=[], removed=[])]

    def validate(self):
        self.validate_decisions(self.before, self.after, self.decisions, self.pairs)

    def test_approved_migration(self):
        self.validate()

    def test_exact_role_attributes_not_just_observed_counts(self):
        role = self.after['build'].find('usage/role')
        original = dict(role.attrib)
        for name, value in [('accepts','place'), ('accepts',None),
                            ('nouns','exception park'), ('nouns',None),
                            ('government','other')]:
            with self.subTest(name=name, value=value):
                role.attrib.clear(); role.attrib.update(original)
                if value is None: role.attrib.pop(name)
                else: role.set(name, value)
                with self.assertRaises(ValueError): self.validate()

    def test_unreviewed_role_cannot_change_even_if_matches_stay_equal(self):
        self.after['build'].findall('usage/role')[1].set('accepts','living')
        with self.assertRaisesRegex(ValueError, 'approved role attributes'): self.validate()

    def test_exact_pairs_include_unreviewed_roles(self):
        for index, field, ids in [(0,'added',['other']), (0,'added',[]),
                                   (0,'removed',[]), (0,'removed',['other']),
                                   (1,'added',['park']), (1,'removed',['exception'])]:
            with self.subTest(index=index, field=field, ids=ids):
                original = self.pairs[index][field]
                self.pairs[index][field] = ids
                with self.assertRaisesRegex(ValueError, 'unapproved'): self.validate()
                self.pairs[index][field] = original

    def test_role_and_form_order_are_preserved(self):
        for section in ('usage','forms'):
            with self.subTest(section=section):
                parent = self.after['build'].find(section)
                parent[:] = list(reversed(parent))
                with self.assertRaisesRegex(ValueError, 'unrelated XML'): self.validate()
                parent[:] = list(reversed(parent))

    def test_missing_extra_and_duplicate_decisions(self):
        import json
        from audit_noun_roles import load_decisions
        self.assertEqual(load_decisions(json.dumps(self.decisions)), self.decisions)
        with self.assertRaisesRegex(ValueError, 'Duplicate'):
            load_decisions('{"build/object":{},"build/object":{}}')
        with self.assertRaisesRegex(ValueError, 'Duplicate'):
            load_decisions('{"build/object":{"target":{},"target":{}}}')
        self.decisions['extra/object'] = self.decisions['build/object']
        with self.assertRaisesRegex(ValueError, 'exactly'): self.validate()
        self.decisions.clear()
        with self.assertRaisesRegex(ValueError, 'exactly'): self.validate()

    def test_documentation_status_cannot_disagree_with_target(self):
        self.decisions['build/object']['status'] = 'category'
        with self.assertRaisesRegex(ValueError, 'documentation'): self.validate()


import os
from types import SimpleNamespace


@unittest.skipUnless(os.environ.get('KOTOMI_PATH'), 'Set KOTOMI_PATH for synthetic engine contracts')
class DecisionEngineTests(unittest.TestCase):
    def setUp(self):
        sys.path.insert(0, os.environ['KOTOMI_PATH'])
        from kotomi.core.project.models import Word, Entity, NounCategory
        from kotomi.core.generation.compatibility import role_matches
        from audit_noun_roles import compare_roles
        self.fixture = DecisionTests(); self.fixture.setUp()
        entities = {i: Entity(i, i, category=c) for i,c in
                    [('house','building'),('tower','building'),('park','place'),('exception','person')]}
        cats = {i: NounCategory(i,i,parent=parent) for i,parent in
                [('place',''),('building','place'),('person','')]}
        old = Word('verbs','build','test','test', usage={'object':[], 'subject':['person']},
                   usage_nouns={'object':['house','park','exception']})
        self.before = SimpleNamespace(words={'verbs':{'build':old}}, entities=entities,
                                      noun_categories=cats, roles={})
        self.after = deepcopy(self.before)
        self.after.words['verbs']['build'].usage['object'] = ['building']
        self.after.words['verbs']['build'].usage_nouns['object'] = ['exception']
        self.compare = lambda: compare_roles(self.before, self.after, role_matches)

    def validate(self):
        self.fixture.pairs = self.compare()
        self.fixture.validate()

    def test_real_engine_or_and_approved_delta(self):
        self.validate()
        self.assertEqual(self.fixture.pairs[0]['after'], ['exception','house','tower'])

    def test_unapproved_pair_from_category_drift(self):
        self.after.entities['park'].category = 'building'
        with self.assertRaisesRegex(ValueError, 'unapproved'): self.validate()

    def test_lost_approved_pair_from_category_drift(self):
        self.after.entities['tower'].category = 'place'
        with self.assertRaisesRegex(ValueError, 'unapproved'): self.validate()


class TargetReviewDecisionTests(unittest.TestCase):
    """Independent explicit approval for a previously category-only role."""
    def setUp(self):
        self.before={'transfer':ET.fromstring('<word id="transfer"><usage>'
            '<role ref="target" accepts="person animal"/></usage></word>')}
        self.after=deepcopy(self.before)
        self.after['transfer'].find('usage/role').set('accepts','person')
        self.decisions={'transfer/target':{
            'scope':'C3.1_target','before':{'ref':'target','accepts':'person animal'},
            'target':{'ref':'target','accepts':'person'},'status':'semantic_review',
            'reason_pl':'Osoba w zwykłej relacji interpersonalnej.', 'added':[], 'removed':['pet']}}
        self.pairs=[{'key':'transfer/target','added':[],'removed':['pet']}]

    def validate(self):
        from audit_noun_roles import validate_decisions
        validate_decisions(self.before,self.after,self.decisions,self.pairs)

    def test_explicit_category_only_review(self):
        self.validate()

    def test_removing_review_does_not_approve_changed_xml(self):
        self.decisions.clear()
        with self.assertRaisesRegex(ValueError,'approved role attributes'): self.validate()

    def test_review_requires_pinned_baseline_and_scope(self):
        for field in ('before','scope','status'):
            with self.subTest(field=field):
                value=self.decisions['transfer/target'].pop(field)
                with self.assertRaisesRegex(ValueError,'pinned target review'): self.validate()
                self.decisions['transfer/target'][field]=value

    def test_review_still_enforces_exact_pairs(self):
        self.pairs[0]['removed']=[]
        with self.assertRaisesRegex(ValueError,'unapproved'): self.validate()
