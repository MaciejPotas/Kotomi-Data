"""Read-only, opt-in C1 completeness check, separate from unit-test discovery.

Standalone checks read verbs.xml, nouns.xml and the JSON/CSV audit artifacts.
--kotomi additionally loads the declared project XML graph through QuizProject
and checks real role matching, inherited categories, language capabilities,
role defaults and observed pattern availability. No translations are generated,
proposals applied, projects saved or files written. See tools/README.md for cost.
"""
from __future__ import annotations

import argparse
from collections import Counter
import csv
from dataclasses import asdict
import json
from pathlib import Path
import sys
from xml.etree import ElementTree as ET

PRIORITY_FORMS = ('dictionary', 'plain_negative', 'past_plain', 'past_negative_plain')
FORM_POLICIES = {
    **dict.fromkeys(PRIORITY_FORMS, 'priority'),
    **dict.fromkeys(('polite_nonpast', 'polite_negative', 'past_polite',
                     'past_negative_polite'), 'polite'),
    'te_form': 'te', 'potential': 'potential', 'passive': 'passive',
    'causative': 'causative', 'tara': 'tara', 'volitional': 'volitional',
    'imperative': 'imperative',
}
FORM_COLUMNS = frozenset(('verb_id', 'form', 'kana', 'kanji', 'translation',
                          'morphology', 'policy', 'specific_finding'))
MORPHOLOGY_STATUSES = frozenset((
    'regular_or_known_exception', 'confirmed_kure_exception',
    'lexical_duplicate_not_inflection_error',
    'mechanical_pattern_only_not_confirmed_lexical_form',
))
# Versioned C1 contract; --kotomi compares this with the live language capability.
C1_CLASSES = frozenset(('masculine_personal', 'masculine_animate',
                        'masculine_inanimate', 'feminine', 'neuter'))
ROLE_METADATA = {'matched_nouns', 'review'}
OP_METADATA = {'reason', 'reason_ref', 'impact'}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def unique(values, label):
    values = list(values)
    require(len(values) == len(set(values)), f'Duplicate {label}')
    return set(values)


def read_form_audit(stream):
    reader = csv.DictReader(stream)
    columns = unique(reader.fieldnames or [], 'CSV column')
    require(FORM_COLUMNS <= columns,
            f'Missing required CSV columns: {sorted(FORM_COLUMNS - columns)}')
    return list(reader)


def agreement_values(word):
    result = {}
    for form in word.findall('forms/form'):
        entries = form.findall('agreement_translations/translation')
        unique((e.get('class') for e in entries), 'existing agreement class')
        if entries:
            result[form.get('ref')] = {e.get('class'): e.get('value') for e in entries}
    return result


def expected_operations(record):
    """Derive the complete additive set from reviewed A values, never changes/stats."""
    if record['category'] != 'A':
        return []
    key = record['id']
    prefix = f"/dictionary/words/word[@id='{key}']"
    role_id = None
    result = []
    if not any(r['ref'] == 'subject' for r in record['current_roles']):
        role_id = f'{key}:subject'
        result.append(dict(id=role_id, verb_id=key, status='A', operation='add_role',
                           path=prefix + '/usage', expected_absent=True, depends_on=[],
                           role={'ref': 'subject', 'nouns': ' '.join(record['subject_candidate_nouns'])}))
    for form in PRIORITY_FORMS:
        for cls, value in record['proposed_priority_values'][form].items():
            old = record['existing_agreement'].get(form, {})
            if cls in old:
                require(old[cls] == value, f'Would overwrite reviewed translation: {key}/{form}/{cls}')
                continue
            result.append(dict(id=f'{key}:{form}:{cls}', verb_id=key, status='A',
                               operation='add_agreement_translation',
                               path=prefix + f"/forms/form[@ref='{form}']/agreement_translations",
                               form=form, **{'class': cls}, value=value, expected_absent=True,
                               depends_on=[role_id] if role_id else []))
    return result


def canonical_operation(operation):
    result = {k: v for k, v in operation.items() if k not in OP_METADATA}
    deps = operation.get('depends_on', [])
    unique(deps, 'dependency')
    result['depends_on'] = sorted(deps)
    require(operation.get('expected_absent') is True, 'Proposals must be additive')
    return result


def validate_static(report, words, nouns, audited):
    """Validate supplied inputs without importing Kotomi or reading other files."""
    actual = {w.get('id'): w for w in words}
    require(len(actual) == len(words), 'Duplicate dictionary IDs')
    require(len({n.get('id') for n in nouns}) == len(nouns), 'Duplicate noun IDs')
    noun_map = {n.get('id'): n for n in nouns}
    records = report['verbs']
    require(Counter(r['id'] for r in records) == Counter(actual.keys()), 'Missing or duplicated verb records')
    require(unique(report['allowed_classes'], 'allowed class') == C1_CLASSES, 'Unknown agreement class contract')
    form_items = [((key, f.get('ref')), f) for key, w in actual.items() for f in w.findall('forms/form')]
    unique((key for key, _ in form_items), 'dictionary form')
    forms = dict(form_items)
    for index, row in enumerate(audited, 2):
        require(FORM_COLUMNS <= set(row), f'Missing required CSV columns at row {index}')
        require(all(isinstance(k, str) and isinstance(v, str) for k, v in row.items()),
                f'Invalid CSV structure or non-text value at row {index}')
    require(Counter((r['verb_id'], r['form']) for r in audited) == Counter(forms.keys()), 'Missing/duplicate form audits')
    for row in audited:
        form = forms[row['verb_id'], row['form']]
        for field in ('kana', 'kanji', 'translation'):
            require(row[field] == form.get(field, ''), f'Stale {field}: {row["verb_id"]}/{row["form"]}')
        require(row['policy'] in report['form_policies'], 'Unknown form review policy')
        require(row['form'] in FORM_POLICIES and row['policy'] == FORM_POLICIES[row['form']],
                f'Incorrect form policy: {row["verb_id"]}/{row["form"]}')
        require(row['morphology'] in MORPHOLOGY_STATUSES,
                f'Unknown morphology: {row["verb_id"]}/{row["form"]}')
    expected = []
    for row in records:
        key, word = row['id'], actual[row['id']]
        # C1 records the main translation, not the loader's noun-case fallback.
        # The other verb attributes normalize absent/empty values to '' and
        # strip whitespace in xml_loader.
        for field, attribute in (('meaning', 'translation'), ('kana', 'kana'),
                                 ('kanji', 'kanji'), ('type', 'type'), ('ending', 'ending')):
            require(field in row and row[field] == (word.get(attribute) or '').strip(),
                    f'Verb property drift: {key}/{field} (XML {attribute})')
        # Features are child elements, not a space-separated word attribute.
        # The loader ignores blank refs; the audit sorts the remaining list.
        features = sorted((f.get('ref') or '').strip()
                          for f in word.findall('features/feature')
                          if (f.get('ref') or '').strip())
        require(isinstance(row.get('features'), list)
                and all(isinstance(f, str) for f in row['features'])
                and sorted(row['features']) == features,
                f'Verb property drift: {key}/features')
        require(row['category'] in ('A', 'B', 'C', 'D'), f'Unknown category: {key}')
        require(row['candidate_status'] == ('A' if row['category'] == 'A' else 'existing' if row['category'] == 'D' else 'discussion_only'), 'Candidate status mismatch')
        require(Counter(row['forms']) == Counter(f.get('ref') for f in word.findall('forms/form')), 'Record form inventory drift')
        require(set(row['missing_priority_forms']) == set(PRIORITY_FORMS) - set(row['forms']), 'Missing form list drift')
        for field in ('current_subject_nouns', 'subject_candidate_nouns'):
            require(unique(row[field], field) <= set(noun_map), f'Unknown noun: {key}/{field}')
        roles = word.findall('usage/role')
        unique((r.get('ref') for r in roles), 'dictionary role')
        unique((r['ref'] for r in row['current_roles']), 'audited role')
        raw_roles = {r.get('ref'): dict(r.attrib) for r in roles}
        reviewed_roles = {r['ref']: {k: v for k, v in r.items() if k not in ROLE_METADATA} for r in row['current_roles']}
        require(raw_roles == reviewed_roles and all(not list(r) and not (r.text or '').strip() for r in roles), f'Role definition drift: {key}')
        for role in row['current_roles']:
            require(unique(role['matched_nouns'], 'matched noun') <= set(noun_map), 'Unknown matched noun')
        subject = next((r['matched_nouns'] for r in row['current_roles'] if r['ref'] == 'subject'), [])
        require(set(subject) == set(row['current_subject_nouns']), f'Subject match snapshot mismatch: {key}')
        require(agreement_values(word) == row['existing_agreement'], f'Existing agreement drift / overwrite: {key}')
        require(all(set(v) <= C1_CLASSES for v in row['existing_agreement'].values()), 'Unknown existing agreement class')
        for values in row['proposed_priority_values'].values():
            require(set(values) <= C1_CLASSES and all(isinstance(v, str) and v.strip() for v in values.values()), 'Unknown agreement class or empty value')
        require(unique(row['required_classes'], 'required class') <= C1_CLASSES, 'Unknown required class')
        if row['category'] in ('A', 'D'):
            snapshot = row['subject_candidate_agreement_classes']
            require(set(snapshot) == set(row['subject_candidate_nouns']), f'Incomplete noun class snapshot: {key}')
            current = {n: noun_map[n].find('agreement').get('class', '') if noun_map[n].find('agreement') is not None else '' for n in snapshot}
            require(current == snapshot, f'Noun agreement class drift: {key}')
            require(set(snapshot.values()) == set(row['required_classes']) <= C1_CLASSES, 'Unknown or inconsistent noun agreement class')
            require(set(row['proposed_priority_values']) == set(PRIORITY_FORMS), f'Incomplete reviewed priority forms: {key}')
            require(bool(snapshot) and all(set(v) == set(row['required_classes']) for v in row['proposed_priority_values'].values()), f'Incomplete reviewed class coverage: {key}')
            if row['category'] == 'A' and 'subject' in raw_roles:
                require(set(row['subject_candidate_nouns']) == set(subject), 'Existing subject differs from approved subjects')
        operations = expected_operations(row)
        role_ops = [c['id'] for c in operations if c['operation'] == 'add_role']
        lexical_ops = [c['id'] for c in operations if c['operation'] == 'add_agreement_translation']
        require(row['subject_role_change'] == (role_ops[0] if role_ops else None), f'Role operation reference mismatch: {key}')
        require(Counter(row['lexical_change_ids']) == Counter(lexical_ops), f'Translation operation references mismatch: {key}')
        expected.extend(operations)
    changes = report['changes']
    unique((c['id'] for c in changes), 'proposal ID')
    expected_by_id = {c['id']: c for c in expected}
    actual_by_id = {c['id']: canonical_operation(c) for c in changes}
    missing = sorted(set(expected_by_id) - set(actual_by_id))
    extra = sorted(set(actual_by_id) - set(expected_by_id))
    require(not missing and not extra, f'Operation set mismatch: missing={missing}, extra={extra}')
    for key, operation in expected_by_id.items():
        require(actual_by_id[key] == canonical_operation(operation), f'Operation/dependency mismatch: {key}')
    # All counts derive from source/reviewed inputs, not from the submitted changes.
    translations = [c for c in expected if c['operation'] == 'add_agreement_translation']
    roles = {c['verb_id'] for c in expected if c['operation'] == 'add_role'}
    translated = {c['verb_id'] for c in translations}
    stats = dict(verbs=len(actual), nouns=len(nouns), forms=len(forms),
                 usage_declarations=sum(len(r['current_roles']) for r in records),
                 by_category=dict(Counter(r['category'] for r in records)),
                 existing_agreement_verbs=sum(bool(r['existing_agreement']) for r in records),
                 existing_agreement_forms=sum(len(r['existing_agreement']) for r in records),
                 existing_agreement_entries=sum(len(v) for r in records for v in r['existing_agreement'].values()),
                 ready_current_subject_verbs=sum(all(r['observed_subject_availability'].values()) for r in records),
                 A_verbs=sum(r['category'] == 'A' for r in records), A_role_additions=len(roles),
                 A_agreement_entries=len(translations),
                 A_agreement_forms=len({(c['verb_id'], c['form']) for c in translations}),
                 A_translation_only=len(translated - roles), A_role_only=len(roles - translated),
                 A_both=len(roles & translated),
                 missing_priority_forms=sum(len(r['missing_priority_forms']) for r in records))
    require(set(report['stats']) == set(stats) | {'patterns'}, 'Unknown/missing statistics')
    for key, value in stats.items():
        require(report['stats'][key] == value, f'Statistics mismatch: {key}')
    for row in records:
        for field in ('observed_subject_availability', 'observed_object_relative_availability'):
            require(set(row[field]) == set(PRIORITY_FORMS) and all(type(v) is bool for v in row[field].values()), 'Invalid availability snapshot')
    return len(expected)


def validate_engine(report, project, role_matches, availability):
    """Compare live engine results; callbacks are actual Kotomi contracts in CLI."""
    require(set(report['allowed_classes']) == set(project.instruction_language.capabilities.verb_agreement_classes), 'Language class contract drift')
    require(report['engine_role_definitions'] == json.loads(json.dumps({k: asdict(v) for k, v in project.roles.items()})), 'Engine role definition drift')
    require(report['stats']['patterns'] == len(project.patterns), 'Statistics mismatch: patterns')
    for row in report['verbs']:
        word = project.words['verbs'][row['id']]
        for role in row['current_roles']:
            matched = {n.id for n in project.entities.values() if role_matches(project, word, role['ref'], n)}
            require(matched == set(role['matched_nouns']), f'Role matches drift: {row["id"]}/{role["ref"]}')
        if row['category'] in ('A', 'D'):
            require({n: project.entities[n].agreement_class for n in row['subject_candidate_nouns']} == row['subject_candidate_agreement_classes'], f'Engine noun agreement drift: {row["id"]}')
        for kind, field in (('subject', 'observed_subject_availability'), ('object', 'observed_object_relative_availability')):
            require({f: availability(row['id'], kind, f) for f in PRIORITY_FORMS} == row[field], f'Availability drift: {row["id"]}/{kind}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--kotomi', type=Path)
    args = parser.parse_args()
    root = args.data.resolve()
    folder = root / 'docs/validation'
    report = json.loads((folder / 'verb_dictionary_proposals_c1.json').read_text(encoding='utf-8'))
    words = ET.parse(root / 'dictionaries/verbs.xml').findall('words/word')
    nouns = ET.parse(root / 'dictionaries/nouns.xml').findall('words/word')
    with (folder / 'verb_dictionary_forms_c1.csv').open(encoding='utf-8', newline='') as stream:
        audited = read_form_audit(stream)
    count = validate_static(report, words, nouns, audited)
    print(f'C1 static completeness OK: {len(words)} verbs, {len(audited)} forms, {count} proposals; no files modified.')
    if not args.kotomi:
        print('SKIPPED (requires --kotomi): actual role matches including OR/inheritance/defaults, engine role definitions, language contract, pattern count and observed availability.')
        return
    sys.path.insert(0, str(args.kotomi.resolve()))
    from kotomi.application.quiz_project import QuizProject
    from kotomi.core.generation.compatibility import CompatibilityProbe, role_matches
    project = QuizProject.load(root / 'quiz_project.xml')
    require(not project.validate(), 'Kotomi project validation failed')
    patterns = {'subject': project.analyze_pattern('Zdania przydawkowe podmiotowe'),
                'object': project.analyze_pattern('Zdania przydawkowe')}
    def availability(key, kind, form):
        return CompatibilityProbe(project, patterns[kind], form).exists(word_choices={'verb@action': key})
    validate_engine(report, project, role_matches, availability)
    print('C1 engine checks OK: full project validation, role definitions/matches, noun classes, language contract, patterns and availability; no files modified.')


if __name__ == '__main__':
    main()
