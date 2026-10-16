"""Opt-in C3 release audit using the real engine, never a second role matcher.

Production reads are intentional: certify the shipped XML migration against a
pinned baseline. Cost is O(roles * nouns + adjectives * nouns), plus optional
bounded relative-pattern enumeration in the companion integration command.
Unit tests exercise pure functions with independently authored XML only.
"""
import argparse
from collections import defaultdict
from copy import deepcopy
import json
from pathlib import Path
import sys
from xml.etree import ElementTree as ET


def words(path):
    return {w.get('id'): w for w in ET.parse(path).findall('words/word')}


def shape(node):
    return node.tag, tuple(sorted(node.attrib.items())), (node.text or '').strip(), tuple(map(shape, node))


def check_local_scope(before, after, *, noun=False):
    """Only category or role accepts/nouns can change, not any other XML value."""
    if set(before) != set(after):
        raise ValueError('Word IDs changed')
    for wid, original in before.items():
        old, new = deepcopy(original), deepcopy(after[wid])
        if noun:
            old.attrib.pop('category', None)
            new.attrib.pop('category', None)
        else:
            for w in (old, new):
                for role in w.findall('usage/role'):
                    role.attrib.pop('accepts', None)
                    role.attrib.pop('nouns', None)
        if shape(old) != shape(new):
            raise ValueError(f'{wid}: unrelated XML changed')


def inventory(verbs, nouns):
    rows = []
    repeated = defaultdict(list)
    for vid, verb in verbs.items():
        for role in verb.findall('usage/role'):
            if not role.get('nouns'):
                continue
            ids = role.get('nouns').split()
            if len(ids) != len(set(ids)):
                raise ValueError(f'{vid}: duplicate noun reference')
            missing = set(ids) - nouns.keys()
            if missing:
                raise ValueError(f'{vid}: missing nouns {sorted(missing)}')
            key = f'{vid}/{role.get("ref")}'
            rows.append({'key': key, 'translation': verb.get('translation'),
                'before': dict(role.attrib),
                'noun_categories_before': {i: nouns[i].get('category') for i in ids}})
            repeated[tuple(sorted(ids))].append(key)
    return rows, [{'nouns': list(ids), 'roles': keys} for ids, keys in repeated.items() if len(keys) > 1]


def compare_roles(before, after, matcher):
    """Inspect every role, including those with no explicit noun list."""
    rows = []
    for vid, verb in before.words['verbs'].items():
        for role in verb.usage:
            old = {n.id for n in before.entities.values() if matcher(before, verb, role, n)}
            new = {n.id for n in after.entities.values()
                   if matcher(after, after.words['verbs'][vid], role, n)}
            rows.append({'key': f'{vid}/{role}', 'before': sorted(old), 'after': sorted(new),
                         'added': sorted(new - old), 'removed': sorted(old - new)})
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--kotomi', type=Path, required=True)
    parser.add_argument('--data', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--baseline-data', type=Path, required=True)
    parser.add_argument('--baseline-grammar', type=Path, required=True)
    parser.add_argument('--decisions', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    sys.path.insert(0, str(args.kotomi.resolve()))
    from kotomi.application.quiz_project import QuizProject
    from kotomi.core.generation.compatibility import role_matches, adjective_matches, effective_entity_categories
    b, a = (QuizProject.load(root / 'quiz_project.xml') for root in (args.baseline_data, args.data))
    old_v, new_v = (words(root / 'dictionaries/verbs.xml') for root in (args.baseline_data, args.data))
    old_n, new_n = (words(root / 'dictionaries/nouns.xml') for root in (args.baseline_data, args.data))
    check_local_scope(old_v, new_v)
    check_local_scope(old_n, new_n, noun=True)
    rows, repeated = inventory(old_v, old_n)
    decisions = json.loads(args.decisions.read_text(encoding='utf-8'))
    if set(decisions) != {r['key'] for r in rows}:
        raise ValueError('Decisions must cover exactly every original nouns role')
    pairs = compare_roles(b, a, role_matches)
    pair_by_key = {r['key']: r for r in pairs}
    for row in rows:
        vid, role = row['key'].split('/')
        row['after'] = dict(new_v[vid].find(f"usage/role[@ref='{role}']").attrib)
        row.update(decisions[row['key']])
        row['pairs'] = pair_by_key[row['key']]
    old_catalog = {x.get('id'): dict(x.attrib) for x in ET.parse(args.baseline_grammar).findall('noun_categories/category')}
    new_catalog = {x.get('id'): dict(x.attrib) for x in ET.parse(args.kotomi / 'kotomi/core/grammar/japanese/grammar.xml').findall('noun_categories/category')}
    reclassified = {i: {'before': old_n[i].get('category'), 'after': n.get('category')}
                    for i, n in new_n.items() if n.get('category') != old_n[i].get('category')}
    for i in new_n:
        if not set(effective_entity_categories(b, b.entities[i])) <= set(effective_entity_categories(a, a.entities[i])):
            raise ValueError(f'{i}: lost ancestor category')
    adjective_changes = []
    for vid, verb in b.words['adjectives'].items():
        for nid, noun in b.entities.items():
            if adjective_matches(b, verb, noun) != adjective_matches(a, a.words['adjectives'][vid], a.entities[nid]):
                adjective_changes.append([vid, nid])
    errors = [issue for issue in a.validate(include_pattern_renderability=False) if issue.startswith('ERROR:')]
    if errors or adjective_changes:
        raise ValueError(errors or adjective_changes)
    def metrics(vs, ns, catalog):
        roles = [r for v in vs.values() for r in v.findall('usage/role')]
        return {'verbs': len(vs), 'nouns': len(ns), 'roles': len(roles),
                'roles_with_nouns': sum(bool(r.get('nouns')) for r in roles),
                'roles_with_accepts': sum(bool(r.get('accepts')) for r in roles),
                'declared_categories': len(catalog),
                'selectable_categories': sum(x.get('selectable', 'true') == 'true' for x in catalog.values()),
                'used_categories': len({n.get('category') for n in ns.values()})}
    report = {'baseline_data': 'ef338045ed383763db2cbf04aceea5b1b7ad1d69',
        'baseline_engine': '9d6d662228301dfb9d94524736e09dcc763b28cc',
        'metrics': {'before': metrics(old_v, old_n, old_catalog), 'after': metrics(new_v, new_n, new_catalog)},
        'new_categories': {i: c for i, c in new_catalog.items() if i not in old_catalog},
        'all_nouns': {i: {'translation': old_n[i].get('translation'), 'before': old_n[i].get('category'),
                        'after': new_n[i].get('category')} for i in old_n},
        'reclassified_nouns': reclassified, 'original_nouns_roles': rows, 'repeated_lists': repeated,
        'all_role_pairs': pairs, 'adjective_changes': adjective_changes,
        'added_combinations': sum(len(r['added']) for r in pairs),
        'removed_combinations': sum(len(r['removed']) for r in pairs), 'structural_errors': errors}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: report[k] for k in ('metrics', 'added_combinations', 'removed_combinations')}, indent=2))


if __name__ == '__main__':
    main()
