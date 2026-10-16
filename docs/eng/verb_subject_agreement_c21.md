# C2.1: verb subject agreement

The current engine includes B3 and universal target C3.2. This document preserves a historical stage; check current references and completeness with the [audit tools](developer_tools.md).

Content 61 applies exactly 62 `changes` from the
[approved C1 proposals](../validation/verb_dictionary_proposals_c1.json):
56 agreed translations across 28 forms and six new `subject` roles.

The scope is `shimaru`, `yomu`, `kaku`, `hanasu`, `kangaeru`, `sentakusuru`
and `soujisuru`. The other 26 category-A verbs remain for C2.2.
No B/C proposals were applied. The engine, DSL, patterns, nouns, quiz packages
and their manifest are unchanged.

The four forms are `dictionary`, `plain_negative`, `past_plain` and
`past_negative_plain`. Human activities support `masculine_personal` and
`feminine`; `shimaru` supports `feminine` and `neuter`. No extra classes,
plurals or forms were added. Values come exclusively from C1.

The six new roles allow exactly `friend mother sister teacher roujin hito
programmer madogiwazoku`. The existing `shimaru` subject still allows only
`bag box`. There is no `accepts="person"`: the engine combines `accepts`
and `nouns` with OR, which would widen the list to include e.g. `hitori`.
Base `translation`, kana, kanji, form order, existing maps, roles and government
are unchanged. XML was edited locally without whole-file serialization.

## Fast checks and CI

```sh
python tools/validate_repository.py
python tools/validate_question_patterns.py
python -m unittest discover -s tests -v
```

The existing repository validator passes the already parsed `verbs.xml` to the
small C2.1 check. Its only additional input is the C1 proposal JSON. It checks
seven entries, exact roles, maps, classes, forms, values, dependencies and
duplicates. It never loads `QuizProject`, runs quizzes or invokes the solver.
Additional cost is linear in proposals with a bounded number of XML searches.
A fixture cannot prove deployment in the published file, so this is a release
check in the existing integrity gate, separate from unit tests.

Fifteen mutation tests use only independent, versioned
`tests/fixtures/c1/v1.json`. Map loading, class selection, negation, past tense,
missing-class rejection, legacy translations and persistence are already tested
in Kotomi (`test_verb_form_agreement.py`, `test_verb_agreement_persistence.py`,
`test_subject_relative_catalog_boundary.py`); Data does not duplicate the engine.

Dependency validation derives the complete expected set from role-addition
operations and `subject_role_change`. Missing, extra, duplicate and malformed
`depends_on` entries fail, including references to existing but incorrect operations.

## Integration acceptance outside CI

Baseline: Kotomi-Data `9227fd02c3c315c3d49ea9357a652a0a4d9c36bc`
(main before C2.1) and Kotomi `9c01404465837f55d32ce1b4056fbb6e99817440`.

```sh
git worktree add --detach ../data-before 9227fd02c3c315c3d49ea9357a652a0a4d9c36bc
python tools/validate_verb_subject_c21_integration.py --kotomi ../Kotomi \
  --baseline-data ../data-before \
  --engine-revision 9c01404465837f55d32ce1b4056fbb6e99817440 \
  --baseline-revision 9227fd02c3c315c3d49ea9357a652a0a4d9c36bc \
  --output docs/validation/verb_subject_c21_validation.json
```

The tool reads both declared project XML graphs and checks loading/validation,
minimal changes, every realization of both relative patterns, exact roles,
rejections, explicit/implicit `agree`, Polish agreement and 100 seeded questions.
Other patterns receive availability probes only. Cost grows with both relative
patterns' realizations and the number of patterns/nouns; this tool is outside CI.
Revision arguments label the report; verify the checkouts before running it.

The [report](../validation/verb_subject_c21_validation.json) records
20 → 70 verb/noun pairs per form, or 100 → 350 realizations including five
contexts. This is specific to the baseline/configuration, not a guarantee for
arbitrary quiz filters. All 30,940 object-relative realizations are identical.
Availability across 92 patterns × 4 forms is preserved. All 2,068 out-of-role noun
rejections, both agreement variants and bound rendering, and 100 generated
questions passed. Both projects report zero validation errors.

## Performance and historical C1

[Raw C2.1 measurements](../validation/verb_subject_c21_performance.json) follow
B3: alternating fresh before/after processes, one CPU, separate cold/warm trials,
seven paired rounds, all samples retained, median of paired-round ratios.
Cold means a newly loaded project, not an OS cold cache. Measurements cover load,
compatibility, availability, counting and first question. One process invocation,
repeated alternately for both data directories:

```sh
python tools/benchmark_subject_relatives.py --kotomi ../Kotomi \
  --data ../data-before --samples 7 \
  --operations load compatibility exists count first_question \
  --output before.json
```

For subject relatives add `--pattern 'Zdania przydawkowe podmiotowe'` and use
`--samples 21`. The default complete B3 benchmark is unchanged; `--operations`
only narrows the measurement set. No benchmark was added to CI.
See the [acceptance summary](../validation/verb_subject_c21_acceptance.md) for interpretation.

C1 remains an untouched historical audit. Before implementation, its static and
engine checks passed against the baseline whose dictionaries are identical to
pinned `236bf6af22e897d103099a1166fb9a941d3ee1fd`. Its validator deliberately
requires proposed entries to be absent, so run it on `../data-before`, not Content 61:

```sh
python ../data-before/tools/validate_verb_dictionary_audit.py --kotomi ../Kotomi
```

Content revision advances from 60 to 61. Kotomi's official builder generated the
manifest; only hashes/URLs for `verbs.xml` and `content_revision.json` changed.
Quiz package versions and manifest are unchanged. No physical-device testing was
performed; acceptance covers the shared engine and data.
