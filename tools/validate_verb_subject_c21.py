"""Small, read-only C2 deployment checks. C1 remains a historical baseline.

Called with the already parsed verbs XML by the repository integrity gate.
No engine import, project loading or possibility enumeration is permitted here.
"""
from collections import Counter

VERBS = frozenset({'shimaru', 'yomu', 'kaku', 'hanasu', 'kangaeru',
                   'sentakusuru', 'soujisuru'})
FORMS = frozenset({'dictionary', 'plain_negative', 'past_plain', 'past_negative_plain'})
C22_VERBS = frozenset('aruku asobu ayamaru deru hairu harau hashiru iku isogu kaeru '
    'kau kikokusuru kotaeru kuru matsu nomu okoru omou oyogu renshuusuru taberu '
    'undousuru usowotsuku utau warau shinjiru'.split())


def require(condition, message):
    if not condition:
        raise ValueError(f'C2: {message}')


def one(parent, path):
    nodes = parent.findall(path)
    require(len(nodes) == 1, f'expected exactly one {path}, found {len(nodes)}')
    return nodes[0]


def category_subject_role(row, report):
    """Translate the reviewed C1 noun groups to the C2.2 category decision."""
    nouns = set(row['subject_candidate_nouns'])
    groups = report['noun_groups']
    for group, accepts in (('people', 'person'), ('people_animals', 'person animal'),
                           ('people_dog', 'person animal')):
        if nouns and nouns == set(groups[group]):
            return {'ref': 'subject', 'accepts': accepts}
    require(False, f'{row["id"]}: unreviewed category migration')


def validate_hitori_retirement(nouns, counters):
    """C2.2 structural invariant; no engine or lesson inventory is needed."""
    require(not nouns.findall("words/word[@id='hitori']"), 'hitori must not be an ordinary noun')
    value = one(counters, "words/word[@id='nin']/quantity_realizations/realization[@number='1']")
    require(value.attrib == {'number': '1', 'kana': 'ひとり', 'kanji': '一人', 'romaji': 'hitori'},
            'nin: changed realization for one person')


def validate_category_a_deployment(root, report):
    """Current release gate: all A translations and the reviewed role migration."""
    selected = VERBS | C22_VERBS
    require({r['id'] for r in report['verbs'] if r['category'] == 'A'} == selected,
            'incorrect category A selection')
    changes = [c for c in report['changes'] if c['verb_id'] in selected]
    require(Counter(c['operation'] for c in changes) ==
            {'add_role': 32, 'add_agreement_translation': 308}, 'incorrect category A totals')
    role_overrides = {row['id']: category_subject_role(row, report)
        for row in report['verbs'] if row['id'] in selected - {'shimaru'}}
    # C3 replaces the exact bag/box subject list with the inherited container category.
    role_overrides['shimaru'] = {'ref': 'subject', 'accepts': 'closable_container'}
    # Reviewed impersonal quantity predicates: ile osób przyszło / poszło.
    extensions = {(verb, form): {'neuter': value}
        for verb, values in (
            ('kuru', ('przychodzi', 'nie przychodzi', 'przyszło', 'nie przyszło')),
            ('iku', ('idzie', 'nie idzie', 'poszło', 'nie poszło')))
        for form, value in zip(('dictionary', 'plain_negative', 'past_plain', 'past_negative_plain'), values)}
    count = validate_deployment(root, report, selected, role_overrides=role_overrides,
                                agreement_extensions=extensions,
                                allowed_extension_classes=set(report['allowed_classes']) |
                                    {'plural_masculine_personal', 'plural_non_masculine_personal'})
    for vid, accepts in (('hataraku', 'person'), ('neru', 'person animal')):
        role = one(root, f"words/word[@id='{vid}']/usage/role[@ref='subject']")
        require(role.attrib == {'ref': 'subject', 'accepts': accepts},
                f'{vid}: incorrect migrated subject role')
    return count


def validate_deployment(root, report, selected=VERBS, *, role_overrides=None, agreement_extensions=None,
                        allowed_extension_classes=()):
    """Check selected approved operations and their complete target XML maps.

    The selection argument supports bounded synthetic fixtures. Only the default
    production selection requires the release totals of 56 translations / 6 roles.
    Explicit role_overrides apply the reviewed C2.2 policy while keeping the
    historical C2.1 acceptance tool usable on its original snapshots.
    """
    role_overrides = {} if role_overrides is None else role_overrides
    require(set(role_overrides) <= set(selected), 'unselected role override')
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
            require(role.attrib == role_overrides.get(vid, change['role']),
                    f'{vid}: changed subject role')
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
    for key, values in (agreement_extensions or {}).items():
        require(key in expected_maps, 'unselected agreement extension')
        require(not set(values) & set(expected_maps[key]), 'agreement extension replaces baseline')
        require(set(values) <= set(report['allowed_classes']), 'unknown extension class')
        require(all(isinstance(value, str) and value.strip() for value in values.values()),
                'empty agreement extension')
        expected_maps[key].update(values)
    for vid, row in records.items():
        word = one(root, f"words/word[@id='{vid}']")
        role = one(one(word, 'usage'), "role[@ref='subject']")
        if vid in role_overrides:
            require(role.attrib == role_overrides[vid], f'{vid}: incorrect category subject role')
        else:
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
            expected = expected_maps[vid, form]
            if allowed_extension_classes:
                # Preserve every reviewed historical value while allowing
                # explicitly authorized missing singular and plural cells.
                extras = set(actual) - set(expected)
                require(
                    all(actual.get(cls) == value for cls, value in expected.items())
                    and extras <= set(allowed_extension_classes)
                    and all(isinstance(actual[cls], str) and actual[cls].strip()
                            for cls in extras),
                    f'{vid}/{form}: changed agreement map',
                )
            else:
                require(actual == expected, f'{vid}/{form}: changed agreement map')
    return len(changes)
