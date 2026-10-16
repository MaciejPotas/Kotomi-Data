# C2.2: subject categories and completion of category A

## Scope and compatibility

Content 62 builds on C2.1 commit `83c36863ee56f606a00a1f02f38d8d75d0595193`.
It adds 26 verbs, 252 agreement translations and 26 subject roles. Together,
C2.1/C2.2 deploy 33 category-A verbs, 308 added translations and 32 added roles.
Every value, agreement class and priority form comes unchanged from approved C1.
Base translations, kana, kanji, other forms, object/target/location roles and
government remain unchanged. C1/C2.1 documentation and historical results remain intact.

New verbs: `aruku`, `asobu`, `ayamaru`, `deru`, `hairu`, `harau`, `hashiru`,
`iku`, `isogu`, `kaeru`, `kau`, `kikokusuru`, `kotaeru`, `kuru`, `matsu`, `nomu`,
`okoru`, `omou`, `oyogu`, `renshuusuru`, `taberu`, `undousuru`, `usowotsuku`,
`utau`, `warau`, `shinjiru`.

## Category-based roles

Person lists become `<role ref="subject" accepts="person" />`. A new `brother`
noun in category `person` matches without editing the verb. This also applies
to the six person-subject verbs from C2.1 and the earlier `hataraku`.

Among migrated verbs, `accepts="person animal"` is used by `asobu`, `deru`, `hairu`, `hashiru`, `iku`,
`kaeru`, `kuru`, `matsu`, `nomu`, `oyogu`, `taberu` and the earlier `neru`.
They accept the whole animal category, including a new `cat`. C1's dog-only
lists deliberately expand to include `tori`. There are no `nouns` exceptions.
All other migrated roles accept only `person`.

This is a deliberate broad category policy, not a species ability model (for
example, swimming). A new noun still needs valid case forms and an agreement
class supported by the verb form. C2.2 adds neither agreement classes nor plural
inflection; a future neuter subject needs separately approved translations.
The `bag box` lists for `aku` and `shimaru` are unchanged.

## Hitori and the lesson

`hitori` realizes the quantity of one person. Its ordinary noun entry is removed,
while the entire `counters.xml` stays unchanged, including
`nin` + `number="1"` → `ひとり / 一人 / hitori`.

The only `nouns:hitori` lesson reference, in `ola_l24_dokkai_nouns`, becomes an
existing-format `local_word`, preserving ID `ola_l24_dokkai_nouns_005`, the meaning
“jedna osoba”, kana and kanji. The vocabulary lesson keeps the expression; the
local word does not extend the global `person` category or grammatical roles.

## Validation and CI

The existing validator now exposes `validate_category_a_deployment`. It checks
exact C1 translation maps, complete `depends_on`, target role attributes and
operation totals. It rejects noun lists, additional categories/attributes,
missing/extra dependencies and duplicates. The hitori check inspects noun XML
and the one-person counter realization. Existing generic validation checks
lesson references.

Unit tests use independent fixtures only. Kotomi tests cover new people/animals,
rejection of animals by person-only roles, four forms, explicit/implicit `agree`,
bound rendering, questions and XML persistence. Required CI validates production
structure without pattern rendering. Full integration and measurements below
are opt-in tools outside required CI. Kotomi's lesson benchmark job requires
manual `workflow_dispatch` with `run_lesson_performance=true`. Quiz packages and
versions are unchanged. The existing generator rebuilt the Content manifest;
only the revision and hashes of `verbs.xml`, `nouns.xml` and `lessons.xml` changed.

## Real-Content integration

Engine: `2656c5a270489141661561701d0a064c8a1dcbd4`. Full validation of both projects
and the lesson catalog reports zero errors. All 368 availability probes
(92 patterns × 4 forms) retain their result. Automated checks compare complete
Polish sentences with approved C1 translations, noun cases and relative pronouns,
and complete Japanese answers with unchanged kana forms. They also cover 104
generated questions (26 new verbs × 4 forms), every explicit binding and implicit
`agree` equivalence.

| Form | Subject pairs before | Subject pairs after | Object realizations before | After |
| --- | ---: | ---: | ---: | ---: |
| dictionary | 70 | 300 | 7735 | 7645 |
| plain_negative | 70 | 300 | 7735 | 7645 |
| past_plain | 70 | 300 | 7735 | 7645 |
| past_negative_plain | 70 | 300 | 7735 | 7645 |

Each form gains 230 pairs. With five context options, generated realizations
increase from 350 to 1500 per form; unique questions and answers increase
from 70 to 300. The five pairs beyond the historical projection of
295 come from admitting `tori` where C1 listed only `inu`. The reduction of 90
object realizations per form consists entirely of hitori bindings. All other
realizations match exactly, including bindings, contexts and forms. Removing
hitori also reduces other person/wildcard selections to the remaining nouns;
no pattern loses availability.

Counting before/after includes “Jest jedna osoba.” → `ひとがひとりいる。` and
“Ile jest osób?” → `ひとがなんにんいるの？`. All four numeric statement forms stay
unchanged. Count questions retain the existing affirmative-only policy; negative
question forms remain rejected.

Full evidence: [integration](../validation/verb_subject_c22_validation.json),
[measurements](../validation/verb_subject_c22_performance.json) and
[acceptance report](../validation/verb_subject_c22_acceptance.md).
Reproduction commands are in `tools/README.md`.

## Additional audit without scope expansion

- Confirmed redundancy: the hitori noun and nin realization, now corrected.
  No second identical redundancy was found in the dictionary review.
- `ほん` (hon counter and book noun) and `ふく` (clothes noun and verb) are
  distinct entries sharing kana, not automatic deletion candidates.
- `availability_reason` groups time, money and plans. `okane` needs repeated
  explicit object exceptions; this warrants a separate category audit, not a C2.2 edit.
- `aku/shimaru: bag box`, `owaru: shigoto meal yotei`, destinations of `ireru`
  and `kayou`, and lists of things opened/closed are narrower than existing
  categories. They remain necessary in the current model.
- `music song`, `clothes`, places built by `tateru`, and documents for
  `teishutsusuru` may miss future entries. They were not widened without a
  separate semantic decision.
