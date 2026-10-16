"""Opt-in C3 integration; real Content is deliberately outside unit-test CI.

Reads the declared project graph and the C3 matrix report. Enumerates only two
relative patterns, checks other patterns with exists(), and saves only a temp copy.
Cost is linear in relative realizations plus bounded pattern/form probes.
"""
import argparse
from collections import Counter
from dataclasses import asdict
import json
from pathlib import Path
import random
import shutil
import sys
import tempfile

from validate_subject_relatives import FORMS, SUBJECT, OBJECT, signature, fingerprint


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--kotomi', type=Path, required=True)
    parser.add_argument('--data', type=Path, required=True)
    parser.add_argument('--baseline-data', type=Path, required=True)
    parser.add_argument('--audit', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    sys.path.insert(0, str(args.kotomi.resolve()))
    from kotomi.application.quiz_project import QuizProject
    from kotomi.application.generation_engine import SharedQuizEngine
    from kotomi.core.project.xml_writer import save_dictionary
    from kotomi.application.storage import CatalogStore
    from kotomi.core.generation.compatibility import CompatibilityProbe
    from kotomi.core.generation.models import EngineRequest
    from audit_noun_roles import compare_roles, words, load_decisions, validate_decisions
    from kotomi.core.generation.compatibility import role_matches
    before = QuizProject.load(args.baseline_data.resolve() / 'quiz_project.xml')
    after = QuizProject.load(args.data.resolve() / 'quiz_project.xml')
    assert before.validate() == after.validate() == []
    assert before.patterns == after.patterns
    assert CatalogStore(args.data.resolve()).load(language_context=after.language_context).validate() == []
    audit = json.loads(args.audit.read_text(encoding='utf-8'))
    actual_matrix = compare_roles(before, after, role_matches)
    validate_decisions(words(args.baseline_data / 'dictionaries/verbs.xml'),
                       words(args.data / 'dictionaries/verbs.xml'),
                       load_decisions((args.data / 'docs/validation/noun_role_decisions_c3.json').read_text(encoding='utf-8')),
                       actual_matrix)
    assert actual_matrix == audit['all_role_pairs'], 'stale audit matrix'
    deltas = {direction: {(r['key'].split('/')[0], r['key'].split('/')[1], noun)
              for r in actual_matrix for noun in r[direction]} for direction in ('added', 'removed')}
    evidence = {'scope': 'Opt-in production acceptance, not unit tests',
                'project_errors': [], 'lesson_errors': [], 'relatives': {}, 'examples': [], 'availability': []}
    engine = SharedQuizEngine(after, random.Random(173))
    for pattern, role in ((SUBJECT, 'subject'), (OBJECT, 'object')):
        for form in FORMS:
            old = list(before.iter_possibilities(pattern, form_name=form))
            new = list(after.iter_possibilities(pattern, form_name=form))
            def pair(v):
                return v.words['verb@action'], role, v.entities['noun@item']
            retained_old = [v for v in old if pair(v) not in deltas['removed']]
            retained_new = [v for v in new if pair(v) not in deltas['added']]
            assert Counter(map(signature, retained_old)) == Counter(map(signature, retained_new))
            assert {pair(v) for v in new} - {pair(v) for v in old} == {x for x in deltas['added'] if x[1] == role}
            assert {pair(v) for v in old} - {pair(v) for v in new} == {x for x in deltas['removed'] if x[1] == role}
            stats = after.count_possibilities(pattern, form_name=form)
            assert stats.generated_sentences == len(new)
            assert stats.unique_questions == len({v.source for v in new})
            assert stats.unique_answers == len({v.answer for v in new})
            for value in new:
                assert after.render_bound_pattern(pattern, word_choices=value.words,
                    entity_choices=value.entities, form_overrides=value.forms,
                    context_pool=value.context_pool, context_option=value.context_option) == (value.source, value.answer)
            outputs = {(v.source, v.answer) for v in new}
            q = engine.build_question(EngineRequest(pattern, form_name=form))
            assert (q.prompt, q.expected_answer) in outputs and q.matches_answer(q.expected_answer)
            for vid, _, nid in sorted(x for x in deltas['added'] if x[1] == role):
                q = engine.build_question(EngineRequest(pattern, form_name=form,
                    word_choices={'verb@action': vid}, entity_choices={'noun@item': nid}))
                assert (q.prompt, q.expected_answer) in outputs
                evidence['examples'].append({'verb': vid, 'noun': nid, 'form': form,
                    'source': q.prompt, 'answer': q.expected_answer})
            for vid, _, nid in sorted(x for x in deltas['removed'] if x[1] == role):
                assert not CompatibilityProbe(after, after.analyze_pattern(pattern), form).exists(
                    word_choices={'verb@action': vid}, entity_choices={'noun@item': nid})
            evidence['relatives'][pattern + '/' + form] = {'before': len(old), 'after': len(new),
                'retained': len(retained_new), 'unchanged_retained_sha256': fingerprint(list(map(signature, retained_new))),
                'after_statistics': asdict(stats)}
            print(pattern, form, len(old), '->', len(new), flush=True)
    for pattern in before.patterns:
        for form in FORMS:
            old = CompatibilityProbe(before, before.analyze_pattern(pattern), form).exists()
            new = CompatibilityProbe(after, after.analyze_pattern(pattern), form).exists()
            assert old == new, (pattern, form, old, new)
            evidence['availability'].append([pattern, form, old, new])
    with tempfile.TemporaryDirectory(prefix='kotomi-c3-roundtrip-') as tmp:
        target = Path(tmp) / 'data'
        shutil.copytree(args.data, target, ignore=shutil.ignore_patterns('.git', '__pycache__'))
        p = QuizProject.load(target / 'quiz_project.xml')
        assert p.validate() == []
        for dictionary in ('nouns', 'verbs'):
            save_dictionary(p, dictionary, p.dictionary_paths[dictionary])
        reloaded = QuizProject.load(target / 'quiz_project.xml')
        assert reloaded.validate() == []
        assert compare_roles(after, reloaded, role_matches) == compare_roles(after, after, role_matches)
        assert {i: n.category for i, n in after.entities.items()} == {i: n.category for i, n in reloaded.entities.items()}
    evidence['temporary_save_reload'] = 'Categories, role matches and full validation preserved'
    args.output.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
