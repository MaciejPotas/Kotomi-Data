# Repository Tools

`validate_repository.py` is the repository integrity gate.

It checks:

- the canonical learning-data directory layout;
- XML syntax and expected schema versions;
- references from `quiz_project.xml`;
- all lesson and context dictionary references, plus every sentence-quiz pattern reference, without rules tied to a lesson or group name;
- Content revision and manifest coverage, hashes, and URLs;
- published quiz package descriptors and file inventories;
- Python syntax in published quiz packages.

Run it from any working directory with:

```text
python tools/validate_repository.py
```

The validator is also executed by GitHub Actions. Keep repository-layout and cross-reference rules in this validator so accidental flat files, broken lesson references, or missing documentation are caught before merge.

`validate_repository.py` validates dictionary semantic catalogs and memberships independently of lesson membership and vocabulary size. `tests/test_semantic_categories.py` uses temporary XML mutation fixtures.

## Opt-in B3 release acceptance

Production Content validation is separate from unit tests. It checks the actual
published references and lexical realizations, which independent fixtures cannot
verify. The audit reads the declared project XML graph, enumerates only the two
relative patterns, and edits only a temporary copy. Cost grows linearly with
these patterns' realizations, plus full project validation and one save/reload.
No new production-dependent unit test or exception registration is introduced.

```sh
python tools/validate_subject_relatives.py --kotomi ../Kotomi \
  --baseline-data ../data-before \
  --output docs/validation/subject_relatives_b3.json
```

Use Kotomi main `7e72245a3e4636c53109ffb58c00176f648f6ce2` plus the fix in
[Kotomi #213](https://github.com/MaciejPotas/Kotomi/pull/213). The baseline Content
is `817cdef693ee004b20fd032dcc4a95b5c214e576`. The unpatched engine deliberately
fails the exact supported-pairs invariant because its existential catalog leaks
into ordinary subject-relative agreement.

The report covers all four forms, exact word pairs, contexts, reconstruction,
rejection, fixed-seed canonical questions and answer matching, both quiz
selections, hints, allowed-form UI data, alias completion and temporary Save All
round trips. Existing isolated application tests cover simulator callbacks,
Mobile controllers and the actual verb-editor callbacks; native device operation
remains manual acceptance.

For performance, invoke `benchmark_subject_relatives.py` in alternating fresh
before/after processes with explicit `--kotomi`, `--data`, `--samples 7` and
`--output`. Run seven pairs without discarding samples; compare the median of
paired round ratios. The process pins itself to one available CPU on Linux.
Use the default object-relative pattern on both revisions; use
`--pattern 'Zdania przydawkowe podmiotowe' --samples 21` for the new path.
Cold means a newly loaded project, with loading timed separately. All retained
samples are in `docs/validation/subject_relatives_b3_performance.json`.


The optional production UI smoke uses real Mobile and simulator callbacks with
Kotomi's test controls and development dependencies (including pytest). It checks
two controller lifecycles, three pattern selections, 48 questions and 12 locked
simulator examples without reloading the preloaded project:

```sh
python tools/validate_subject_relative_ui.py --kotomi ../Kotomi \
  --output docs/validation/subject_relatives_b3_ui.json
```

This is not native device testing and is not part of unit-test discovery.

## Opt-in C1 audit completeness

```sh
python tools/validate_verb_dictionary_audit.py
python tools/validate_verb_dictionary_audit.py --kotomi ../Kotomi
```

The standalone check reads `dictionaries/verbs.xml`, `dictionaries/nouns.xml`
and the JSON/CSV audit artifacts. It derives every expected operation from reviewed
A records independently of `changes` and statistics, then requires exact equality.
It checks missing/extra/duplicate operations, dependencies (including required
subject-role additions), paths, values, existing maps, all local role attributes,
per-noun A/D agreement-class snapshots, and all static statistics including touched
forms. Pattern count and actual availability require the engine; standalone mode
prints these and other deferred checks explicitly as `SKIPPED`.

Standalone checks also compare each verb's main translation (`meaning`), kana,
kanji, type, ending and nested feature refs with its audit record. Verb attributes
use the loader's whitespace normalization and empty values for missing optional
attributes; feature order is immaterial and blank refs are ignored by the loader.
Errors identify the verb and mismatched property.

The CSV reader requires all eight existing columns and rejects duplicate headers,
short/overlong rows and non-text cells. Each form must use its designated policy;
being present in the policy catalog is insufficient. Morphology is restricted to
the four existing audit statuses. Empty kanji and `specific_finding` are allowed;
findings remain free text and are not assessed by linguistic heuristics.

With `--kotomi`, it loads the declared project XML graph via `QuizProject`, validates
the project and compares all role matches through the engine's `role_matches`.
This preserves OR between `accepts` and `nouns`, inherited noun categories,
wildcards and role defaults without a second matcher implementation. It also checks
the role-definition catalog, language class contract, noun classes, expanded pattern
count and both relative patterns' observed availability for every priority form.

Production access establishes completeness and freshness of this particular audit,
which a synthetic fixture cannot establish. The standalone cost is linear in forms,
records and proposals. Engine mode additionally incurs project loading/validation,
role-by-noun comparisons (R × N) and eight availability probes per verb. It applies
no proposals and writes no files. No production-dependent unit test is introduced.

Validator tests import its pure functions with the bounded, independent fixture
`tests/fixtures/c1/v1.json`. Run:

```sh
python -m unittest discover -s tests -p test_verb_dictionary_audit.py -v
KOTOMI_PATH=/absolute/path/to/Kotomi python -m unittest discover -s tests -v
```

Without `KOTOMI_PATH`, 31 validator tests run and four real-engine contract tests
are explicitly skipped. With it, all 35 run; the four extra tests construct only
synthetic model objects and never load Content. Existing repository tests are unchanged.
See the [C1 report](../docs/validation/verb_dictionary_audit_c1.md) and equivalent
[Polish](../docs/pl/verb_dictionary_audit_c1.md) / [English](../docs/eng/verb_dictionary_audit_c1.md)
entry points. Historical performance measurements predate the review corrections
and are labelled accordingly.

## C2.1 deployment and historical C1

Content 61 applies seven approved category-A verbs. `validate_repository.py`
reuses its parsed verbs XML for the small deployment check in
`validate_verb_subject_c21.py`, comparing it with the selected C1 `changes`.
This release invariant cannot be established with fixtures: it concerns the
published XML and approved JSON. Additional work is linear in proposal count
with bounded XML searches; no project loading, solver or quiz generation occurs.
New unit tests use only the existing independent C1 fixture v1.

The historical C1 audit and validator are unchanged. Its absence preconditions
apply to the pre-C2.1 snapshot, not current Content. Run C1 in a baseline worktree
at `9227fd02c3c315c3d49ea9357a652a0a4d9c36bc`.

Use `validate_verb_subject_c21_integration.py` only for opt-in acceptance, never
unit-test discovery or mandatory CI. It compares both relative constructions
against that baseline and probes other patterns without enumerating quizzes.
`benchmark_subject_relatives.py --operations load compatibility exists count
first_question` selects the C2.1 measurement scope while preserving default B3
behavior. See equivalent [PL](../docs/pl/verb_subject_agreement_c21.md) and
[ENG](../docs/eng/verb_subject_agreement_c21.md) guides for commands and results.


## C2.2 category-based release

Content 62 deploys all category-A proposals. Required CI calls
`validate_category_a_deployment` and `validate_hitori_retirement`, reusing the
existing parsed XML. This is structural validation of the released XML against
historical C1, with no engine import or generation. C2.1's original
`validate_deployment` mode remains available for historical snapshots; current
release validation explicitly applies the reviewed C2.2 role overrides.

Unit tests use only synthetic fixtures. Run `python -m unittest discover -s tests -v`
and both existing validators. Set `KOTOMI_PATH` to enable the synthetic engine contracts.

Full acceptance and paired measurements are manual, outside mandatory CI:

```sh
python tools/validate_verb_subject_c22_integration.py --kotomi ../Kotomi --data . --baseline-data ../content61 --engine-revision 2656c5a270489141661561701d0a064c8a1dcbd4 --baseline-revision 83c36863ee56f606a00a1f02f38d8d75d0595193 --output docs/validation/verb_subject_c22_validation.json
python tools/benchmark_verb_subject_c22.py --kotomi ../Kotomi --data . --baseline-data ../content61 --engine-revision 2656c5a270489141661561701d0a064c8a1dcbd4 --baseline-revision 83c36863ee56f606a00a1f02f38d8d75d0595193 --output docs/validation/verb_subject_c22_performance.json
```

Use a detached Content 61 worktree at the stated baseline. Run benchmarks without
concurrent tests. The paired driver alternates fresh before/after processes,
fixes the hash seed, pins the same CPU where available and retains all samples.
Cold means a fresh project, not an OS cold start. Four representative patterns
cover load, compatibility, exists, count and first-question latency, cold and warm.
See the equivalent [PL](../docs/pl/verb_subject_agreement_c22.md) and
[EN](../docs/eng/verb_subject_agreement_c22.md) release notes.

## C3 noun-role categories and opt-in migration audit

Read [PL](../docs/pl/noun_role_categories_c3.md),
[EN](../docs/eng/noun_role_categories_c3.md) and the
[complete grouped inventory](../docs/validation/noun_role_audit_c3.md).
Use application main `9d6d662228301dfb9d94524736e09dcc763b28cc` plus the C3
category catalog and review corrections, and a detached Data baseline at
`ef338045ed383763db2cbf04aceea5b1b7ad1d69`. Export that application's original
`kotomi/core/grammar/japanese/grammar.xml` as `baseline-grammar.xml`.

```sh
python tools/audit_noun_roles.py --kotomi ../Kotomi --baseline-data ../data-before \
  --baseline-grammar ../baseline-grammar.xml \
  --decisions docs/validation/noun_role_decisions_c3.json \
  --output docs/validation/noun_role_audit_c3.json
python tools/validate_noun_role_integration.py --kotomi ../Kotomi --data . \
  --baseline-data ../data-before --audit docs/validation/noun_role_audit_c3.json \
  --output docs/validation/noun_role_integration_c3.json
```

These are explicit production-content acceptance commands, never mandatory unit
CI. Fixtures cannot certify every actual published list, the role/noun migration
matrix or the retained rendered sentences. Reads cover the project-declared XML
and audit JSON only. The inventory cost is O(roles * nouns + adjectives * nouns);
integration enumerates two relative patterns and probes other patterns with
`exists`. XML writers operate only on a disposable copy. The audit rejects any
change to government, forms, translation, roles or other unrelated XML content.

Unit tests (`test_noun_role_audit.py` and the application's
`test_noun_role_categories.py`) use independent bounded fixtures, not audit JSON
or production dictionaries. No production access exemption is added.

The existing paired benchmark accepts optional `--baseline-kotomi` and
`--baseline-engine-revision` for a distinct old application. Omitting them retains
C2.2 behavior. For the reviewed C3 release run with both pinned checkouts, seven alternating rounds and
21 samples, without concurrent tests:

```sh
python tools/benchmark_verb_subject_c22.py --kotomi ../Kotomi \
  --baseline-kotomi ../app-before --data . --baseline-data ../data-before \
  --engine-revision 'C3 category catalog' \
  --baseline-engine-revision 9d6d662228301dfb9d94524736e09dcc763b28cc \
  --baseline-revision ef338045ed383763db2cbf04aceea5b1b7ad1d69 \
  --rounds 7 --samples 21 --output docs/validation/noun_role_performance_c3.json
```

Current release validation deliberately accepts `shimaru/subject` using
`closable_container`. The C1 proposals and historical `validate_deployment`
behavior are not rewritten. C2.2 integration evidence remains historical.


### C3 review enforcement and publication gate

The existing decision JSON owns exact `target` role attributes and approved
`added`/`removed` noun IDs. Both audit and integration commands enforce those
expectations before writing evidence. Roles without decisions retain their baseline
attributes and matches. Duplicate decision keys fail. Regenerating a report cannot
approve a broadened `accepts`, lost exception or altered pair. No matcher is duplicated.

Content 63 requires manifest **format 2**, enforced by the release validator and
Kotomi manifest builder. Legacy format-1 clients reject it before payload download.
Never publish C3 through a format-1 mirror. Revision metadata remains format 1.
See the PL/EN C3 guides for the compatibility matrix, snapshot validation, rollback
and the limited C4 recommendation.

Reproduce the protocol matrix using actual updater implementations and the bounded
engine fixture (no production vocabulary):

```sh
python ../Kotomi/tools/updates/validate_content_compatibility_c3.py --kotomi ../app-before --legacy
python ../Kotomi/tools/updates/validate_content_compatibility_c3.py --kotomi ../Kotomi
```

The legacy checkout is `9d6d662228301dfb9d94524736e09dcc763b28cc`.
Run Data unit tests with `KOTOMI_PATH` as above to enable the three additional
synthetic C3 engine contracts. The pure decision-mutation tests always run in CI.

The review performance evidence also retains the initial 5 × 5 run and its
7 × 21 precision recheck before the small set-intersection optimization. After
that correction, the 7 × 21 full run had one borderline sub-millisecond check.
One predeclared confirmation used the same driver with `--patterns 'Sam czasownik'
--operations exists --rounds 9 --samples 101`. The final 10% gate uses the median
of all 16 same-code paired round ratios for those measured operations, retaining
the original seven rounds; other operations use the seven-round full run.
The JSON separates original `median_paired_ratios`, `verified_paired_ratios`,
`same_code_confirmation` and pre-correction diagnostics. No sample is discarded.


### C3.1 target review

Five category-only roles have explicit decisions in the same C3 JSON, with
`scope: C3.1_target`, pinned `before`, full `target`, reasons and exact pair deltas.
Original nouns-role coverage is still mandatory; an additional decision must refer
to an existing target role and match its baseline. Removing such an approval does
not allow changed XML. The audit records these under `reviewed_target_roles`.
Run the same audit/integration commands above; no second matcher or audit system.

`tests/test_target_roles.py` in Kotomi adds independent transfer/attendance fixtures:
automatic and explicit governor binding, two arguments, Polish case direction and
negation, literal に, questions/counts, ambiguous overlapping roles, missing frames
and Studio XML roundtrip. Data adds four independent decision-mutation tests.

For C3.1 performance use the same paired benchmark, `--kotomi ../Kotomi`,
`--baseline-data ../data-c3-before` pinned to `e51fcbb1d7a5cd3dc5d5918e3648d9d3ac6cdf1c`,
`--rounds 7 --samples 21`; the runtime is unchanged from `baa4b1d` on both sides.
Record this follow-up in `noun_role_performance_c3.json` without replacing the
historical main-versus-C3 measurements. The threshold stays 10%.

## C3.2 target acceptance

Run `python tools/validate_target_c32.py --kotomi ../Kotomi --output docs/validation/target_c32_acceptance.json`. This opt-in production check loads the declared project once, renders only the eight finite forms of the target pattern, compares counts and bound/quiz outputs, and checks six examples and four rejections. It is not part of unit-test CI. The historical C3 matrix describes Content 63; the C3.2 guide documents the five removed hairu pairs.


## Current manual audit and Windows test runner

`../run_tests.bat` runs the test suite. `../run_data_audit.bat` runs `diagnostics/data_audit.py` against the Kotomi engine. See [Polski](../docs/pl/developer_tools.md) / [English](../docs/eng/developer_tools.md) for filters, JSON, exit codes and optional-form interpretation.

The JSON inventory also exposes `verb_agreement`: stored/missing classes for
every form, using the application's language capabilities. The text report
separates fully populated agreement matrices from checked-contract completeness.
An intentionally impersonal or contextual form must not be filled mechanically.
Content 69 review and per-form decisions: [Polski](../docs/pl/polish_agreement_audit.md)
/ [English](../docs/eng/polish_agreement_audit.md).


## Lesson 26 release acceptance

`validate_relative_lesson26.py --kotomi ../Kotomi --output docs/validation/relative_lesson26.json` checks bounded, independently reviewed full sentences, rejected bindings and old relative patterns. `validate_relative_lesson26_ui.py` with the same arguments checks per-pattern and mixed Mobile selections and exact simulator callbacks with fake widgets. These are explicit production audits, not unit tests, and never enumerate the whole vocabulary product. See `docs/eng/relative_lesson26.md` and `docs/pl/relative_lesson26.md` for scope and limitations.

Architecture, extension workflow and cleanup decisions: [English](../docs/eng/repository_cleanup.md) / [Polski](../docs/pl/repository_cleanup.md).
