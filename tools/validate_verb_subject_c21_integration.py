"""Opt-in C2.1 acceptance on real Content; never imported by unit tests/CI.

Reads the declared project graph in two Content snapshots. Enumerates only the
subject/object relative patterns, probes other patterns without enumeration.
"""
import argparse
from collections import Counter
from copy import deepcopy
from dataclasses import asdict
import json
from pathlib import Path
import random
import re
import sys
from xml.etree import ElementTree as ET

from validate_verb_subject_c21 import VERBS, validate_deployment
from validate_subject_relatives import FORMS, SUBJECT, OBJECT, PRONOUNS, signature, fingerprint


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--kotomi', type=Path, required=True)
    parser.add_argument('--data', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--baseline-data', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--engine-revision', default='unrecorded')
    parser.add_argument('--baseline-revision', default='unrecorded')
    args = parser.parse_args()
    sys.path.insert(0, str(args.kotomi.resolve()))
    from kotomi.application.quiz_project import QuizProject
    from kotomi.application.generation_engine import SharedQuizEngine
    from kotomi.core.generation.compatibility import CompatibilityProbe, role_matches
    from kotomi.core.generation.models import EngineRequest
    from kotomi.core.project.errors import NoCompatibleChoices

    proposals = json.loads((args.data / 'docs/validation/verb_dictionary_proposals_c1.json').read_text(encoding='utf-8'))
    changes = [c for c in proposals['changes'] if c['verb_id'] in VERBS]
    current_xml = ET.parse(args.data / 'dictionaries/verbs.xml').getroot()
    assert validate_deployment(current_xml, proposals) == 62
    # Remove exactly the additions from a temporary tree. Everything else,
    # including existing map values, roles, attributes and node order, must match.
    stripped = deepcopy(current_xml)
    for c in changes:
        word = stripped.find(f"words/word[@id='{c['verb_id']}']")
        if c['operation'] == 'add_role':
            usage = word.find('usage'); usage.remove(usage.find("role[@ref='subject']"))
        else:
            form = word.find(f"forms/form[@ref='{c['form']}']")
            section = form.find('agreement_translations')
            section.remove(section.find(f"translation[@class='{c['class']}']"))
            if not len(section): form.remove(section)
    def structure(node):
        return (node.tag, node.attrib, (node.text or '').strip(), [structure(n) for n in node])
    assert structure(stripped) == structure(ET.parse(args.baseline_data / 'dictionaries/verbs.xml').getroot())
    old_text = (args.baseline_data / 'dictionaries/verbs.xml').read_bytes()
    new_text = (args.data / 'dictionaries/verbs.xml').read_bytes()
    changed = set()
    for match in re.finditer(rb'    <word id="([^"]+)".*?</word>', old_text, re.S):
        vid = match[1].decode()
        new = re.search(rb'    <word id="' + match[1] + rb'".*?</word>', new_text, re.S)[0]
        if new != match[0]: changed.add(vid)
        new_text = new_text.replace(new, match[0], 1)
    assert changed == VERBS and new_text == old_text
    for old in (args.baseline_data / 'dictionaries').glob('*.xml'):
        if old.name != 'verbs.xml': assert old.read_bytes() == (args.data / 'dictionaries' / old.name).read_bytes()
    for old in (args.baseline_data / 'docs/validation').glob('*c1*'):
        assert old.read_bytes() == (args.data / 'docs/validation' / old.name).read_bytes()

    before = QuizProject.load(args.baseline_data.resolve() / 'quiz_project.xml')
    after = QuizProject.load(args.data.resolve() / 'quiz_project.xml')
    assert before.validate() == after.validate() == []
    assert before.entities == after.entities and before.patterns == after.patterns
    expected = {r['id']: set(r['subject_candidate_nouns']) for r in proposals['verbs'] if r['id'] in VERBS}
    for vid, nouns in expected.items():
        assert {n.id for n in after.entities.values() if role_matches(after, after.words['verbs'][vid], 'subject', n)} == nouns
    evidence = {'scope': 'Opt-in C2.1 real-Content acceptance; no unit-test production access',
                'engine_revision': args.engine_revision,
                'baseline_data_revision': args.baseline_revision,
                'xml_additions': {'verbs': 7, 'translations': 56, 'roles': 6},
                'unchanged_xml_and_c1': True, 'project_errors': [], 'subject': {},
                'object_regression': {}, 'examples': [], 'rejection_checks': 0}
    allowed = set()
    for form in FORMS:
        old = list(before.iter_possibilities(SUBJECT, form_name=form))
        new = list(after.iter_possibilities(SUBJECT, form_name=form))
        pairs = lambda values: {(v.words['verb@action'], v.entities['noun@item']) for v in values}
        old_pairs, new_pairs = pairs(old), pairs(new)
        additions = {(v, n) for v, nouns in expected.items() for n in nouns}
        assert len(old_pairs) == 20 and len(new_pairs) == 70 and new_pairs == old_pairs | additions
        assert not old_pairs & additions
        for value in new:
            noun = after.entities[value.entities['noun@item']]
            verb = after.words['verbs'][value.words['verb@action']]
            assert value.source == f'To jest {noun.cases["nominative"]}, {PRONOUNS[noun.agreement_class]} {verb.forms[form].agreement_translations[noun.agreement_class]}.'
            assert value.answer == f'これは{verb.forms[form].kana}{noun.kana}です。'
            assert after.render_bound_pattern(SUBJECT, word_choices=value.words, entity_choices=value.entities,
                form_overrides=value.forms, context_pool=value.context_pool,
                context_option=value.context_option) == (value.source, value.answer)
            allowed.add((value.source, value.answer))
        for project, values in [(before, old), (after, new)]:
            stats = project.count_possibilities(SUBJECT, form_name=form)
            assert stats.generated_sentences == len(values)
            assert stats.unique_questions == len({v.source for v in values})
            assert stats.unique_answers == len({v.answer for v in values})
        evidence['subject'][form] = {'before_pairs': len(old_pairs), 'after_pairs': len(new_pairs),
            'before': asdict(before.count_possibilities(SUBJECT, form_name=form)),
            'after': asdict(after.count_possibilities(SUBJECT, form_name=form))}
        evidence['examples'].extend({'form': form, 'verb': vid, 'question': v.source, 'answer': v.answer}
            for vid in sorted(VERBS) for v in [next(v for v in new if v.words['verb@action'] == vid)])
        a = [signature(v) for v in before.iter_possibilities(OBJECT, form_name=form)]
        b = [signature(v) for v in after.iter_possibilities(OBJECT, form_name=form)]
        assert Counter(a) == Counter(b)
        assert before.count_possibilities(OBJECT, form_name=form) == after.count_possibilities(OBJECT, form_name=form)
        evidence['object_regression'][form] = {'realizations': len(a), 'identical': True, 'sha256': fingerprint(a)}
        # Every out-of-role noun, including hitori, must fail availability.
        for vid, nouns in expected.items():
            probe = CompatibilityProbe(after, after.analyze_pattern(SUBJECT), form)
            for nid in after.entities:
                if nid in nouns: continue
                assert not probe.exists(word_choices={'verb@action': vid}, entity_choices={'noun@item': nid})
                evidence['rejection_checks'] += 1
            for nid in ('hitori', 'book'):
                if nid in nouns: continue
                try:
                    after.render_bound_pattern(SUBJECT, word_choices={'verb@action': vid},
                        entity_choices={'noun@item': nid}, form_overrides={'verb@action': form},
                        context_pool=new[0].context_pool, context_option=new[0].context_option)
                except NoCompatibleChoices: pass
                else: raise AssertionError((vid, nid, form))
        print(f'{form}: 20 -> 70 subject pairs; {len(a)} unchanged object realizations', flush=True)
    availability = []
    for pattern in before.patterns:
        for form in FORMS:
            a = CompatibilityProbe(before, before.analyze_pattern(pattern), form).exists()
            b = CompatibilityProbe(after, after.analyze_pattern(pattern), form).exists()
            assert a == b, (pattern, form, a, b)
            availability.append([pattern, form, a, b])
    evidence['pattern_availability'] = availability
    # Exercise implicit agree in memory only, with all four forms and all pairs.
    pattern = after.patterns[SUBJECT]
    original = pattern.question
    pattern.question = original.replace('form, agree:@item', 'form, agree')
    assert pattern.question != original
    assert after.analyze_pattern(SUBJECT).entity_for_agreement == {'verb@action': 'noun@item'}
    for form in FORMS:
        values = list(after.iter_possibilities(SUBJECT, form_name=form))
        assert len(pairs(values)) == 70
        assert all((v.source, v.answer) in allowed for v in values)
        for value in values:
            assert after.render_bound_pattern(SUBJECT, word_choices=value.words, entity_choices=value.entities,
                form_overrides=value.forms, context_pool=value.context_pool,
                context_option=value.context_option) == (value.source, value.answer)
    pattern.question = original
    evidence['explicit_and_implicit_agree'] = 'all four forms, every pair and bound rendering passed'
    engine = SharedQuizEngine(after, random.Random(173))
    for i in range(100):
        question = engine.build_question(EngineRequest(SUBJECT, form_name=FORMS[i % 4]))
        assert (question.prompt, question.expected_answer) in allowed
        assert question.matches_answer(question.expected_answer)
    evidence['random_questions'] = {'seed': 173, 'count': 100, 'canonical_match': True}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'C2.1 integration passed: {args.output}', flush=True)


if __name__ == '__main__':
    main()
