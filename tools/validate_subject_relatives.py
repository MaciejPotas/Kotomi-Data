"""Opt-in B3 release audit against an explicitly supplied Kotomi checkout.

This reads production Content for release acceptance, never during unit tests.
Scope: the declared project XML graph, both relative patterns and three verbs.
Cost: linear in the enumerated realizations of those two patterns, plus one full
project validation and temporary authoring round trip. No checkout is modified.
"""
from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import random
import shutil
import sys
import tempfile

FORMS = ('dictionary', 'plain_negative', 'past_plain', 'past_negative_plain')
SUBJECT = 'Zdania przydawkowe podmiotowe'
OBJECT = 'Zdania przydawkowe'
PEOPLE = {'friend', 'mother', 'sister', 'teacher', 'roujin', 'hito', 'programmer', 'madogiwazoku'}
EXPECTED = {'hataraku': PEOPLE, 'neru': PEOPLE | {'inu', 'tori'}, 'aku': {'bag', 'box'}}
PRONOUNS = {'masculine_personal': 'który', 'masculine_animate': 'który',
            'masculine_inanimate': 'który', 'feminine': 'która', 'neuter': 'które'}


def signature(value):
    return (value.source, value.answer, tuple(sorted(value.words.items())),
            tuple(sorted(value.entities.items())), tuple(sorted(value.forms.items())),
            value.context_pool, value.context_option)


def fingerprint(values):
    return hashlib.sha256(json.dumps(sorted(values), ensure_ascii=False).encode()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--kotomi', type=Path, required=True)
    parser.add_argument('--data', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--baseline-data', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    sys.path.insert(0, str(args.kotomi.resolve()))
    from kotomi.application.quiz_project import QuizProject
    from kotomi.application.generation_engine import SharedQuizEngine
    from kotomi.application.project_save import ProjectSaveSession
    from kotomi.application.quiz_hints import selected_vocabulary_hints, selected_context_hint
    from kotomi.application.authoring.placeholders import placeholder_completions
    from kotomi.core.generation.compatibility import CompatibilityProbe
    from kotomi.core.generation.models import EngineRequest
    from kotomi.core.project.errors import NoCompatibleChoices
    from platforms.desktop.form_authoring import form_choices
    from apps.grammar import logic

    p = QuizProject.load(args.data.resolve() / 'quiz_project.xml')
    before = QuizProject.load(args.baseline_data.resolve() / 'quiz_project.xml')
    assert p.validate() == []
    assert before.validate() == []
    assert set(p.patterns[SUBJECT].allowed_forms) == set(FORMS)
    assert p.patterns[SUBJECT].category == 'przydawki'
    assert p.sentence_quizzes['relative_clauses'].pattern_ids == [OBJECT, SUBJECT]
    picker = form_choices(p, p.patterns[SUBJECT], lambda key, **kw: key)
    assert all(form in picker and form not in picker.unavailable for form in FORMS)
    completions = placeholder_completions('{relative[agree:', len('{relative[agree:'), p,
        related_source=p.patterns[SUBJECT].question + p.patterns[SUBJECT].answer).items
    assert any('@item' in item.insert_text for item in completions)
    # Existing glosses, Japanese forms, roles, and noun classifications are immutable.
    for identifier, word in before.words['verbs'].items():
        current = p.words['verbs'][identifier]
        for role, values in word.usage.items():
            assert current.usage[role] == values
            assert current.usage_nouns.get(role) == word.usage_nouns.get(role)
        assert current.government_by_role == word.government_by_role
        for name, form in word.forms.items():
            actual = current.forms[name]
            assert (form.translation, form.kana, form.kanji) == (actual.translation, actual.kana, actual.kanji)
    assert p.entities == before.entities
    report = {'forms': {}, 'object_regression': {}, 'examples': [], 'rejected': [],
              'validation': [], 'scope': 'production release audit, not a unit test'}
    all_pairs = set()
    for form in FORMS:
        analysis = p.analyze_pattern(SUBJECT)
        assert set(analysis.slots) == {'noun@item', 'verb@action'}
        assert CompatibilityProbe(p, analysis, form).exists()
        values = list(p.iter_possibilities(SUBJECT, form_name=form))
        stats = p.count_possibilities(SUBJECT, form_name=form)
        assert stats.generated_sentences == len(values)
        pairs = {(v.source, v.answer) for v in values}
        assert stats.unique_questions == len({v.source for v in values})
        assert stats.unique_answers == len({v.answer for v in values})
        actual = {(v.words['verb@action'], v.entities['noun@item']) for v in values}
        assert actual == {(verb, noun) for verb, nouns in EXPECTED.items() for noun in nouns}
        for value in values:
            verb = p.words['verbs'][value.words['verb@action']]
            noun = p.entities[value.entities['noun@item']]
            expected_source = f'To jest {noun.cases["nominative"]}, {PRONOUNS[noun.agreement_class]} {verb.forms[form].agreement_translations[noun.agreement_class]}.'
            assert value.source == expected_source
            assert value.answer == f'これは{verb.forms[form].kana}{noun.kana}です。'
            assert p.render_bound_pattern(SUBJECT, word_choices=value.words,
                entity_choices=value.entities, form_overrides=value.forms,
                context_pool=value.context_pool, context_option=value.context_option) == (value.source, value.answer)
            assert len(selected_vocabulary_hints(p, value)) == 2
            assert selected_context_hint(p, value) == ('', '')
        all_pairs.update(pairs)
        report['forms'][form] = {**asdict(stats), 'unique_pairs': len(pairs),
                                'by_verb': dict(Counter(verb for verb, _ in actual))}
        report['examples'].extend({'form': form, 'question': q, 'answer': a} for q, a in sorted(pairs))
        old = [signature(v) for v in before.iter_possibilities(OBJECT, form_name=form)]
        new = [signature(v) for v in p.iter_possibilities(OBJECT, form_name=form)]
        assert Counter(old) == Counter(new)
        assert before.count_possibilities(OBJECT, form_name=form) == p.count_possibilities(OBJECT, form_name=form)
        report['object_regression'][form] = {'realizations': len(old), 'sha256': fingerprint(old)}
        for verb, noun in [('hataraku', 'book'), ('hataraku', 'inu'), ('hataraku', 'hitori'),
                           ('neru', 'car'), ('neru', 'hitori'), ('aku', 'hito'),
                           ('aku', 'book'), ('iru', 'hito'), ('aru_existential', 'book')]:
            assert not CompatibilityProbe(p, analysis, form).exists(
                word_choices={'verb@action': verb}, entity_choices={'noun@item': noun})
            try:
                p.render_bound_pattern(SUBJECT, word_choices={'verb@action': verb},
                    entity_choices={'noun@item': noun}, form_overrides={'verb@action': form},
                    context_pool=values[0].context_pool, context_option=values[0].context_option)
            except NoCompatibleChoices:
                pass
            else:
                raise AssertionError((verb, noun, form))
            report['rejected'].append([form, verb, noun])
    def random_sequence():
        engine = SharedQuizEngine(p, random.Random(173))
        result = []
        for i in range(100):
            q = engine.build_question(EngineRequest(SUBJECT, form_name=FORMS[i % 4]))
            assert (q.prompt, q.expected_answer) in all_pairs
            assert q.matches_answer(q.expected_answer)
            result.append((q.prompt, q.expected_answer))
        return result
    sequence = random_sequence()
    assert sequence == random_sequence()
    report['random'] = {'seed': 173, 'questions': 100, 'sha256': fingerprint(sequence)}
    report['unique_pairs_all_forms'] = len(all_pairs)
    logic.configure_quiz_profile('relative_clauses', project=p)
    policy = logic.snapshot_quiz_policy()
    engine = policy.QUIZ_ENGINE_CLASS(p.manifest_path, project=p, rng=random.Random(173))
    report['quiz_selections'] = {}
    for patterns in ([OBJECT], [SUBJECT], [OBJECT, SUBJECT]):
        settings = policy.QUIZ_SETTINGS_CLASS(enabled_patterns=patterns,
            enabled_forms=list(policy.FORM_GROUPS), polite_output=False, plain_output=True)
        assert engine.has_possible_question(settings)
        stats = engine.statistics(settings)
        assert stats['active_patterns'] == len(patterns)
        for _ in range(20):
            question = engine.generate_question(settings)
            assert question.pattern_id in patterns
        report['quiz_selections'][' + '.join(patterns)] = stats
    with tempfile.TemporaryDirectory(prefix='kotomi-b3-authoring-') as temp:
        root = Path(temp) / 'data'
        shutil.copytree(args.data, root, ignore=shutil.ignore_patterns('.git', '__pycache__'))
        editing = QuizProject.load(root / 'quiz_project.xml')
        assert editing.validate() == []
        session = ProjectSaveSession(editing)
        snapshot = {f.relative_to(root): (f.read_bytes(), f.stat().st_mtime_ns)
                    for f in root.rglob('*') if f.is_file()}
        assert session.save_all() == ()
        assert snapshot == {f.relative_to(root): (f.read_bytes(), f.stat().st_mtime_ns)
                            for f in root.rglob('*') if f.is_file()}
        selected = editing.words['verbs']['hataraku'].forms['past_plain']
        selected.agreement_translations['feminine'] = 'wykonywała pracę'
        assert editing.validate() == []
        assert session.save_all() == (editing.dictionary_paths['verbs'],)
        loaded = QuizProject.load(editing.manifest_path)
        assert loaded.words['verbs']['hataraku'].forms['past_plain'].agreement_translations == selected.agreement_translations
        for verb in EXPECTED:
            for form in FORMS:
                assert loaded.words['verbs'][verb].forms[form].agreement_translations == editing.words['verbs'][verb].forms[form].agreement_translations
        assert loaded.patterns[SUBJECT] == p.patterns[SUBJECT]
        changed = {path for path, (content, mtime) in snapshot.items()
                   if (root / path).read_bytes() != content or (root / path).stat().st_mtime_ns != mtime}
        assert changed == {Path('dictionaries/verbs.xml')}
    report['authoring'] = 'picker, alias completion, preview, no-op Save All, one-file edit and reload passed'
    report['device_limit'] = 'Headless shared logic; no physical Windows/Android GUI operated.'
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'B3 release audit passed: {len(all_pairs)} unique pairs, output {args.output}')


if __name__ == '__main__':
    main()
