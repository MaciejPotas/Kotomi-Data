"""Small, read-only C2.1 deployment check. C1 remains a historical baseline.

Called with the already parsed verbs XML by the repository integrity gate.
No engine import, project loading or possibility enumeration is permitted here.
"""
from collections import Counter

VERBS = frozenset({'shimaru', 'yomu', 'kaku', 'hanasu', 'kangaeru',
                   'sentakusuru', 'soujisuru'})
FORMS = frozenset({'dictionary', 'plain_negative', 'past_plain', 'past_negative_plain'})


def require(condition, message):
    if not condition:
        raise ValueError(f'C2.1: {message}')


def one(parent, path):
    nodes = parent.findall(path)
    require(len(nodes) == 1, f'expected exactly one {path}, found {len(nodes)}')
    return nodes[0]


def validate_deployment(root, report, selected=VERBS):
    """Check selected approved operations and their complete target XML maps.

    The selection argument supports bounded synthetic fixtures. Only the default
    production selection requires the release totals of 56 translations / 6 roles.
    """
    records = {}
    for row in report['verbs']:
        if row['id'] in selected:
            require(row['id'] not in records, f'duplicate record {row["id"]}')
            records[row['id']] = row
    require(set(records) == set(selected), 'missing selected audit records')
    require(all(row['category'] == 'A' for row in records.values()), 'non-A record')
    changes = [c for c in report['changes'] if c['verb_id'] in selected]
    ids = [c['id'] for c in changes]
    require(len(ids) == len(set(ids)), 'duplicate operation')
    if selected == VERBS:
        require(Counter(c['operation'] for c in changes) ==
                {'add_role': 6, 'add_agreement_translation': 56}, 'incorrect release totals')
    subject_roles = {}
    for change in changes:
        if change['operation'] == 'add_role':
            vid = change['verb_id']
            require(vid not in subject_roles and change['role'].get('ref') == 'subject',
                    f'{vid}: invalid subject role operation')
            subject_roles[vid] = change['id']
    for vid, row in records.items():
        require(row['subject_role_change'] == subject_roles.get(vid),
                f'{vid}: subject_role_change does not match approved role operation')
    expected_maps = {}
    roles = {}
    for change in changes:
        vid = change['verb_id']
        require(change['status'] == 'A' and change['expected_absent'] is True,
                f'{vid}: operation is not an approved addition')
        dependencies = change.get('depends_on', [])
        require(isinstance(dependencies, list) and
                all(isinstance(dependency, str) for dependency in dependencies),
                f'{change["id"]}: invalid dependencies')
        require(len(dependencies) == len(set(dependencies)),
                f'{change["id"]}: duplicate dependencies')
        expected_dependencies = ({subject_roles[vid]}
            if change['operation'] == 'add_agreement_translation' and vid in subject_roles else set())
        require(set(dependencies) == expected_dependencies,
                f'{change["id"]}: incorrect dependencies; expected {sorted(expected_dependencies)}')
        word = one(root, f"words/word[@id='{vid}']")
        base = f"/dictionary/words/word[@id='{vid}']"
        if change['operation'] == 'add_role':
            require(change['path'] == base + '/usage', f'{vid}: incorrect role path')
            require(vid not in roles, f'{vid}: duplicate role operation')
            roles[vid] = change['role']
            role = one(one(word, 'usage'), "role[@ref='subject']")
            require(role.attrib == change['role'], f'{vid}: changed subject role')
        else:
            require(change['operation'] == 'add_agreement_translation', 'unknown operation')
            form, cls = change['form'], change['class']
            require(form in FORMS and cls in report['allowed_classes'], f'{vid}: unknown form/class')
            require(change['path'] == base + f"/forms/form[@ref='{form}']/agreement_translations",
                    f'{vid}: incorrect translation path')
            expected = expected_maps.setdefault((vid, form), {})
            require(cls not in expected, f'{vid}/{form}: duplicate class operation')
            expected[cls] = change['value']
    require(set(expected_maps) == {(v, f) for v in selected for f in FORMS},
            'missing priority form operations')
    for vid, row in records.items():
        word = one(root, f"words/word[@id='{vid}']")
        role = one(one(word, 'usage'), "role[@ref='subject']")
        require(set(role.get('nouns', '').split()) == set(row['subject_candidate_nouns']),
                f'{vid}: changed exact subject list')
        require(set(role.attrib) == {'ref', 'nouns'}, f'{vid}: broad or changed subject role')
        for form in FORMS:
            node = one(one(word, 'forms'), f"form[@ref='{form}']")
            section = one(node, 'agreement_translations')
            entries = list(section)
            require(not section.attrib and all(e.tag == 'translation' and
                    set(e.attrib) == {'class', 'value'} and not len(e) for e in entries),
                    f'{vid}/{form}: invalid translation structure')
            actual = {e.get('class'): e.get('value') for e in entries}
            require(len(actual) == len(entries), f'{vid}/{form}: duplicate class')
            require(actual == expected_maps[vid, form], f'{vid}/{form}: changed agreement map')
    return len(changes)
