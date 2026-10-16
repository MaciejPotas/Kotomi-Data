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
