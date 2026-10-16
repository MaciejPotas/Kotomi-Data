"""Opt-in C2.2 acceptance on two real Content snapshots, never mandatory CI.

Enumerates the two relative constructions only. Other patterns are checked with
existence probes. Reads no network resources and never saves a project.
"""
import argparse
from collections import Counter
from copy import deepcopy
from dataclasses import asdict
import json
from pathlib import Path
import random
import sys
from xml.etree import ElementTree as ET

from validate_verb_subject_c21 import VERBS, C22_VERBS, validate_category_a_deployment, validate_hitori_retirement
from validate_subject_relatives import FORMS, SUBJECT, OBJECT, PRONOUNS, signature, fingerprint


def structure(node):
    return node.tag, node.attrib, (node.text or '').strip(), [structure(n) for n in node]


def check_xml(before, after, proposals):
    old = ET.parse(before / 'dictionaries/verbs.xml').getroot()
    new = ET.parse(after / 'dictionaries/verbs.xml').getroot()
    assert validate_category_a_deployment(new, proposals) == 340
    restored = deepcopy(new)
    for change in proposals['changes']:
        if change['verb_id'] not in C22_VERBS:
            continue
        word = restored.find(f"words/word[@id='{change['verb_id']}']")
        if change['operation'] == 'add_role':
            word.find('usage').remove(word.find("usage/role[@ref='subject']"))
        else:
            form = word.find(f"forms/form[@ref='{change['form']}']")
            section = form.find('agreement_translations')
            section.remove(section.find(f"translation[@class='{change['class']}']"))
            if not len(section):
                form.remove(section)
    for word in restored.find('words'):
        vid = word.get('id')
        previous = old.find(f"words/word[@id='{vid}']")
        if vid in (VERBS - {'shimaru'}) | {'hataraku', 'neru'}:
            word.find("usage/role[@ref='subject']").attrib = dict(previous.find("usage/role[@ref='subject']").attrib)
        if previous.find('usage') is None and word.find('usage') is not None:
            assert not len(word.find('usage'))
            word.remove(word.find('usage'))
    assert structure(restored) == structure(old), 'Unapproved verb or non-subject role edit'
    old_nouns = ET.parse(before / 'dictionaries/nouns.xml').getroot()
    new_nouns = ET.parse(after / 'dictionaries/nouns.xml').getroot()
    old_nouns.find('words').remove(old_nouns.find("words/word[@id='hitori']"))
    assert structure(old_nouns) == structure(new_nouns)
    validate_hitori_retirement(new_nouns, ET.parse(after / 'dictionaries/counters.xml').getroot())
    old_lessons = ET.parse(before / 'lessons/lessons.xml').getroot()
    lesson = old_lessons.find("lessons/lesson[@id='ola_l24_dokkai_nouns']")
    entry = lesson.find("word[@id='ola_l24_dokkai_nouns_005']")
    position = list(lesson).index(entry)
    lesson.remove(entry)
    lesson.insert(position, ET.Element('local_word', {
        'id': 'ola_l24_dokkai_nouns_005', 'translation': 'jedna osoba', 'kana': 'ひとり',
        'kanji': '一人', 'romaji': 'hitori', 'example': ''}))
    assert structure(old_lessons) == structure(ET.parse(after / 'lessons/lessons.xml').getroot())
    for path in before.rglob('*.xml'):
        relative = path.relative_to(before)
        if str(relative) not in {'dictionaries/verbs.xml', 'dictionaries/nouns.xml', 'lessons/lessons.xml'}:
            assert path.read_bytes() == (after / relative).read_bytes(), relative
    for folder, glob in [('docs/validation', '*c1*'), ('docs/validation', '*c21*'),
                         ('docs/pl', '*c1*'), ('docs/pl', '*c21*'), ('docs/eng', '*c1*'), ('docs/eng', '*c21*')]:
        for path in (before / folder).glob(glob):
            assert path.read_bytes() == (after / path.relative_to(before)).read_bytes(), path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--kotomi', type=Path, required=True)
    parser.add_argument('--data', type=Path, required=True)
    parser.add_argument('--baseline-data', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--engine-revision', required=True)
    parser.add_argument('--baseline-revision', required=True)
    args = parser.parse_args()
    sys.path.insert(0, str(args.kotomi.resolve()))
    from kotomi.application.quiz_project import QuizProject
    from kotomi.application.generation_engine import SharedQuizEngine
    from kotomi.application.storage import CatalogStore
    from kotomi.core.generation.compatibility import CompatibilityProbe, role_matches
    from kotomi.core.generation.models import EngineRequest
    from kotomi.core.project.models import Numeric
    from kotomi.core.project.errors import NoCompatibleChoices, ProjectError

    proposals = json.loads((args.data / 'docs/validation/verb_dictionary_proposals_c1.json').read_text(encoding='utf-8'))
    check_xml(args.baseline_data, args.data, proposals)
    before = QuizProject.load(args.baseline_data.resolve() / 'quiz_project.xml')
    after = QuizProject.load(args.data.resolve() / 'quiz_project.xml')
    assert before.validate() == after.validate() == []
    assert before.patterns == after.patterns
    assert set(before.entities) - set(after.entities) == {'hitori'}
    assert 'hitori' not in after.words['nouns']
    assert all(after.entities[key] == value for key, value in before.entities.items() if key != 'hitori')
    catalog = CatalogStore(args.data).load(language_context=after.language_context)
    assert catalog.validate() == []
    evidence = {'scope': 'Opt-in real Content acceptance, outside mandatory CI',
        'engine_revision': args.engine_revision, 'baseline_data_revision': args.baseline_revision,
        'xml': {'new_verbs': 26, 'new_translations': 252, 'new_roles': 26,
                'all_a_verbs': 33, 'all_a_translations': 308, 'all_a_roles': 32,
                'existing_roles_migrated': 8, 'unrelated_xml_and_history_unchanged': True},
        'project_errors': [], 'lesson_errors': [], 'subject': {}, 'object': {}, 'examples': []}
    allowed = {}
    engine = SharedQuizEngine(after, random.Random(173))
    for form in FORMS:
        old = list(before.iter_possibilities(SUBJECT, form_name=form))
        new = list(after.iter_possibilities(SUBJECT, form_name=form))
        pairs = lambda values: {(v.words['verb@action'], v.entities['noun@item']) for v in values}
        expected = {(verb.id, noun.id) for verb in after.words['verbs'].values()
            for noun in after.entities.values() if role_matches(after, verb, 'subject', noun)
            and form in verb.forms and noun.agreement_class in verb.forms[form].agreement_translations}
        assert pairs(new) == expected
        assert pairs(old) <= pairs(new)
        allowed[form] = {(v.source, v.answer) for v in new}
        for value in new:
            noun = after.entities[value.entities['noun@item']]
            verb = after.words['verbs'][value.words['verb@action']]
            assert value.source == f'To jest {noun.cases["nominative"]}, {PRONOUNS[noun.agreement_class]} {verb.forms[form].agreement_translations[noun.agreement_class]}.'
            assert value.answer == f'これは{verb.forms[form].kana}{noun.kana}です。'
            assert after.render_bound_pattern(SUBJECT, word_choices=value.words,
                entity_choices=value.entities, form_overrides=value.forms,
                context_pool=value.context_pool, context_option=value.context_option) == (value.source, value.answer)
        for p, values in ((before, old), (after, new)):
            stats = p.count_possibilities(SUBJECT, form_name=form)
            assert stats.generated_sentences == len(values)
            assert stats.unique_questions == len({v.source for v in values})
            assert stats.unique_answers == len({v.answer for v in values})
        evidence['subject'][form] = {'before_pairs': len(pairs(old)), 'after_pairs': len(pairs(new)),
            'before': asdict(before.count_possibilities(SUBJECT, form_name=form)),
            'after': asdict(after.count_possibilities(SUBJECT, form_name=form)),
            'new_pairs': sorted(pairs(new) - pairs(old))}
        for vid in sorted(C22_VERBS):
            q = engine.build_question(EngineRequest(SUBJECT, form_name=form, word_choices={'verb@action': vid}))
            assert (q.prompt, q.expected_answer) in allowed[form]
            assert q.matches_answer(q.expected_answer)
            evidence['examples'].append({'form': form, 'verb': vid, 'question': q.prompt, 'answer': q.expected_answer})
        a = list(before.iter_possibilities(OBJECT, form_name=form))
        b = list(after.iter_possibilities(OBJECT, form_name=form))
        retained = [v for v in a if 'hitori' not in v.entities.values()]
        assert Counter(map(signature, retained)) == Counter(map(signature, b))
        evidence['object'][form] = {'before': len(a), 'after': len(b),
            'removed_hitori': len(a) - len(retained), 'other_realizations_identical': True,
            'sha256': fingerprint([signature(v) for v in b])}
        print(f'{form}: {len(pairs(old))} -> {len(pairs(new))} subject pairs; object {len(a)} -> {len(b)}', flush=True)
    evidence['pattern_availability'] = []
    for key in before.patterns:
        for form in FORMS:
            old = CompatibilityProbe(before, before.analyze_pattern(key), form).exists()
            new = CompatibilityProbe(after, after.analyze_pattern(key), form).exists()
            assert old == new, (key, form, old, new)
            evidence['pattern_availability'].append([key, form, old, new])
    pattern = after.patterns[SUBJECT]
    explicit = pattern.question
    pattern.question = explicit.replace('form, agree:@item', 'form, agree')
    assert pattern.question != explicit
    for form in FORMS:
        values = list(after.iter_possibilities(SUBJECT, form_name=form))
        assert {(v.source, v.answer) for v in values} == allowed[form]
        for value in values:
            assert after.render_bound_pattern(SUBJECT, word_choices=value.words,
                entity_choices=value.entities, form_overrides=value.forms,
                context_pool=value.context_pool, context_option=value.context_option) == (value.source, value.answer)
    pattern.question = explicit
    evidence['explicit_and_implicit_agree'] = 'Exact outputs and bound rendering match for every form and pair'
    for form in FORMS:
        with_removed = {'verb@action': 'hataraku'}
        preview = after.build_preview(SUBJECT, form_name=form, word_choices=with_removed)
        try:
            after.render_bound_pattern(SUBJECT, word_choices=with_removed,
                entity_choices={'noun@item': 'hitori'}, form_overrides={'verb@action': form},
                context_pool=preview.context_pool, context_option=preview.context_option)
        except ProjectError as error:
            assert "No noun is bound to slot 'noun@item'" in str(error), str(error)
        else:
            raise AssertionError('Removed ordinary noun remains renderable')
    evidence['counting'] = []
    for form in FORMS:
        for p in (before, after):
            assert p.words['counters']['nin'].quantity_realization(Numeric(1)).output() == 'ひとり'
        options = dict(form_name=form, word_choices={'number@count': 'one'}, entity_choices={'noun@item': 'hito'})
        a = before.build_preview('Istnienie policzonych rzeczowników', rng=random.Random(173), **options)
        b = after.build_preview('Istnienie policzonych rzeczowników', rng=random.Random(173), **options)
        assert signature(a) == signature(b) and 'ひとり' in b.answer
        row = {'form': form, 'one_person_question': b.source, 'one_person_answer': b.answer,
               'one_person_output': 'ひとり', 'unchanged': True}
        if form in ('plain_negative', 'past_negative_plain'):
            for p in (before, after):
                try:
                    p.build_preview('Ile jest policzonych rzeczowników', form_name=form,
                                    entity_choices={'noun@item': 'hito'})
                except NoCompatibleChoices:
                    pass
                else:
                    raise AssertionError('Existing count-question negative-form restriction changed')
            row['count_question'] = 'Negative form remains unsupported by the existing grammar policy'
            evidence['counting'].append(row)
            continue
        a = before.build_preview('Ile jest policzonych rzeczowników', form_name=form, entity_choices={'noun@item': 'hito'}, rng=random.Random(173))
        b = after.build_preview('Ile jest policzonych rzeczowników', form_name=form, entity_choices={'noun@item': 'hito'}, rng=random.Random(173))
        assert signature(a) == signature(b) and 'なんにん' in b.answer
        row.update(question=b.source, answer=b.answer)
        evidence['counting'].append(row)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'C2.2 integration passed: {args.output}', flush=True)


if __name__ == '__main__':
    main()
