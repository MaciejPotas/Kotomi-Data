"""Opt-in C1 report completeness check, separate from unit-test discovery.

Reads only verbs.xml, nouns.xml and the audit artifacts. This verifies the
actual published dictionary inventory, which a synthetic fixture cannot do.
Cost is linear in dictionary forms, audited forms and proposals. With --kotomi,
checks supported classes against the actual language contract as well.
Does not generate translations, apply proposals, save projects or write files.
"""
from __future__ import annotations

import argparse
from collections import Counter
import csv
import json
from pathlib import Path
import sys
from xml.etree import ElementTree as ET


def require(condition, message):
    if not condition:
        raise ValueError(message)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--kotomi', type=Path)
    args = parser.parse_args()
    root = args.data.resolve()
    folder = root / 'docs/validation'
    report = json.loads((folder / 'verb_dictionary_proposals_c1.json').read_text(encoding='utf-8'))
    words = ET.parse(root / 'dictionaries/verbs.xml').findall('words/word')
    nouns = {n.get('id'): n for n in ET.parse(root / 'dictionaries/nouns.xml').findall('words/word')}
    actual = {w.get('id'): w for w in words}
    require(len(actual) == len(words), 'Duplicate dictionary IDs')
    records = report['verbs']
    require(Counter(r['id'] for r in records) == Counter(actual.keys()), 'Missing or duplicated verb records')
    classes = set(report['allowed_classes'])
    if args.kotomi:
        sys.path.insert(0, str(args.kotomi.resolve()))
        from kotomi.languages.polish import PolishLanguage
        require(classes == set(PolishLanguage.capabilities.verb_agreement_classes), 'Language class contract drift')
    expected_forms = {(key, form.get('ref')): form for key, word in actual.items() for form in word.findall('forms/form')}
    with (folder / 'verb_dictionary_forms_c1.csv').open(encoding='utf-8', newline='') as stream:
        audited = list(csv.DictReader(stream))
    require(Counter((r['verb_id'], r['form']) for r in audited) == Counter(expected_forms.keys()), 'Missing/duplicate form audits')
    for row in audited:
        form = expected_forms[row['verb_id'], row['form']]
        for field in ('kana', 'kanji', 'translation'):
            require(row[field] == form.get(field, ''), f'Stale {field}: {row["verb_id"]}/{row["form"]}')
        require(row['policy'] in report['form_policies'], 'Unknown form review policy')
    for row in records:
        word = actual[row['id']]
        require(Counter(row['forms']) == Counter(f.get('ref') for f in word.findall('forms/form')), 'Record form inventory drift')
        for key in ('current_subject_nouns', 'subject_candidate_nouns'):
            require(set(row[key]) <= set(nouns), f'Unknown noun in {row["id"]}/{key}')
        for role in row['current_roles']:
            require(set(role['matched_nouns']) <= set(nouns), 'Unknown matched noun')
        for values in row['proposed_priority_values'].values():
            require(set(values) <= classes and all(v.strip() for v in values.values()), 'Invalid proposed class/value')
    changes = report['changes']
    require(len({c['id'] for c in changes}) == len(changes), 'Duplicate proposal ID')
    ids = {c['id'] for c in changes}
    touched = set()
    by_id = {r['id']: r for r in records}
    categories = {r['id']: r['category'] for r in records}
    for change in changes:
        key = change['verb_id']
        require(key in actual and categories[key] == 'A' and change['status'] == 'A', 'Unsafe/unknown proposed verb')
        require(set(change.get('depends_on', [])) <= ids, 'Missing proposal dependency')
        require(change['expected_absent'] is True, 'Proposals must be additive')
        word = actual[key]
        prefix = f"/dictionary/words/word[@id='{key}']"
        if change['operation'] == 'add_role':
            require(change['path'] == prefix + '/usage', 'Incorrect role XPath')
            require(change['role']['ref'] == 'subject', 'Unexpected role mutation')
            require(set(change['role']) == {'ref', 'nouns'}, 'Unexpected role attributes')
            require(word.find("usage/role[@ref='subject']") is None, 'Role already exists')
            noun_ids = change['role']['nouns'].split()
            require(bool(noun_ids) and len(noun_ids) == len(set(noun_ids)) and set(noun_ids) <= set(nouns), 'Invalid role nouns')
            require(set(noun_ids) == set(by_id[key]['subject_candidate_nouns']), 'Role disagrees with reviewed subjects')
            identity = (key, 'subject')
        else:
            require(change['operation'] == 'add_agreement_translation', 'Unsupported operation')
            form_id, cls = change['form'], change['class']
            require(change['path'] == prefix + f"/forms/form[@ref='{form_id}']/agreement_translations", 'Incorrect form XPath')
            require((key, form_id) in expected_forms and cls in classes, 'Unknown form/class')
            form = expected_forms[key, form_id]
            require(form.find(f"agreement_translations/translation[@class='{cls}']") is None, 'Would overwrite existing translation')
            require(bool(change['value'].strip()), 'Empty proposed translation')
            require(change['value'] == by_id[key]['proposed_priority_values'][form_id][cls], 'Proposal disagrees with reviewed value')
            identity = (key, form_id, cls)
        require(identity not in touched, f'Conflicting proposal: {identity}')
        touched.add(identity)
    stats = report['stats']
    require(stats['verbs'] == len(actual) and stats['forms'] == len(expected_forms), 'Inventory statistics mismatch')
    require(stats['by_category'] == dict(Counter(r['category'] for r in records)), 'Category statistics mismatch')
    require(stats['A_role_additions'] == sum(c['operation'] == 'add_role' for c in changes), 'Role count mismatch')
    require(stats['A_agreement_entries'] == sum(c['operation'] == 'add_agreement_translation' for c in changes), 'Translation count mismatch')
    print(f"C1 completeness OK: {len(actual)} verbs, {len(expected_forms)} forms, {len(changes)} proposals; no files modified.")


if __name__ == '__main__':
    main()
