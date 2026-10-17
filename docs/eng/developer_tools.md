# Manual audits and tests

The test runner prefers the active virtualenv, then `.venv`, then `python` on
PATH. It uses installed pytest, falling back to the existing unittest suite.
It preserves the exit code and prints the framework summary plus total time.
Test file selection and `--verbose` also work with unittest. Advanced pytest
flags require pytest. Double-click execution keeps the window open for reading.

```bat
run_tests.bat
run_tests.bat tests/test_semantic_categories.py --verbose
run_data_audit.bat --kotomi ..\Kotomi
run_data_audit.bat --dictionary verbs --verbose
run_data_audit.bat --output audit.txt --json audit.json
```

The audit requires a Kotomi checkout, automatically finding the submodule parent
or a sibling Kotomi directory. Use `--kotomi` for another checkout and `--project`
for another manifest. It opens no GUI, writes no XML and generates no translations.
The default report is `audit-results/data-audit.txt`; JSON is optional.

Rules come from Kotomi's parser, `QuizProject.validate`,
`DictionaryService.validate_word`, active-language catalogs and the existing
Japanese conjugation generator. They are not copied into Data. ERROR identifies a contract violation or a missing required field. WARNING
identifies a probable data gap or an item requiring verification. INFO covers
explicit `nouns` exceptions, recognized conjugation variants and optional data.
An unrecognized generator difference remains WARNING without automatically
becoming a data gap. `affects_completeness` records each finding's impact;
`review_notes` counts findings without that impact, not incomplete words. JSON
separates `errors`, `warnings`, `info` and dictionary completeness. Completeness
covers checked contracts, not every possible grammatical use.

Inventory separates stored forms, `generated_forms` (authoring suggestions),
`optional_forms_not_explicit` (no established storage obligation),
`unsupported_by_generator` and `missing_required_forms`. Generator limitations
do not prove linguistic impossibility. Universal per-word obligation and
productivity metadata is unavailable; `requirements_status` states that
uncertainty. `absent_catalog_forms` retains the raw backward-compatible list.
`selectable_catalog_forms` comes from the current registry.

A known obligation comes from a fixed word and fixed form selector analyzed by
the engine. The generator does not supply runtime forms or verify translations.
A missing required stored form therefore remains WARNING even if its kana is
generatable. Open slots, dynamic quiz forms, inherited forms and full contextual
validity belong to solver diagnostics. Studio lists fixed forms too;
`eligible_form_names` restricts dynamic quiz forms, not a mandatory inventory
for every verb.

When `target_translation` or `agreement_translations` exists without a general
gloss, INFO states that other contexts remain unverified. A form with no
translation gets a completeness-affecting WARNING. The auditor never generates
translations. Parser failure exits 1 and explicitly reports an interrupted scan.
Warnings and information alone retain exit code 0.

CI retains `tools/validate_repository.py`, unittest and
`tools/validate_question_patterns.py`. Bounded audit tests join the unit suite;
production quality and coverage results remain manual. Verb coverage, empty
patterns and unused words are checked by `tools/diagnostics/run_diagnostics.bat`
in Kotomi, without a second solver in Data.

Current complete examples: [target](target_government_c32.md),
[categories](noun_role_categories_c3.md), [relatives](relative_clauses.md).
`depends_on` belongs to operations in historical audit proposal JSON, not to word
or role XML. C1/C2 are stage-specific reports; this tool audits the current data.

Current revision results: [JSON report](../validation/developer_tools_audit.json). 380 words, 0 errors, 0 warnings, 24 informational findings: 15 explicit nouns exception declarations and 9 adjective conjugation variants. All 122 verbs have coverage; 22 words have no demonstrated lexical use in patterns. Literal kana in patterns is not a dictionary reference. The audit did not change vocabulary or translations.

## Full local validation and realization coverage

Kotomi now owns `tools/diagnostics/pattern_realization_audit.py`, since actual
word-pattern-form requirements need the engine. From the parent Kotomi checkout:

```bat
tools\diagnostics\run_pattern_audit.bat --output audit.txt --json audit.json --strict
tools\run_full_validation.bat
tools\run_full_validation.bat --quick
tools\run_full_validation.bat --diagnostics-only
```

`--full` is the default. The full runner sequentially includes Data tests,
repository/pattern validators and this Data audit, followed by Kotomi tests and
Content diagnostics. It reads the `data` submodule, stores per-step logs and
structured summaries in `validation-results/<UTC>`, and never generates manifests
or edits vocabulary. A code-0 audit with data errors still fails the runner;
INFO does not. Missing dependencies are skipped explicitly. Benchmarks stay separate.

The realization audit distinguishes semantic rejection, confirmed missing data,
renderable relationships and UNVERIFIED coverage. It checks reachable forms,
required cases, government, agreement, contextual translations and related word
IDs without imposing every noun case or catalog form universally. TXT groups
issues by word; JSON retains all contexts and indexed positive relationships.
ERROR is a confirmed missing field, WARNING requests review, INFO is informational,
and UNVERIFIED is neither correct nor erroneous. Generated numeric domains,
provider limitations and bounded dependency enumeration remain explicit gaps.
The PL/ENG Kotomi developer-tools guide documents budgets, table decoding and
all CLI options. These production diagnostics remain outside mandatory CI.

JSON also records `execution_success`: false means parsing/loading or audit execution was interrupted, independently of the number of data errors.
