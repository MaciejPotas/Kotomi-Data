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
Japanese conjugation generator. They are not copied into Data. ERROR identifies
a structural inconsistency or missing field required by the dictionary contract.
WARNING identifies absent explicit form translations, noun cases or agreement
classes, explicit nouns exceptions, or differences from the generator. A conjugation
difference may be a valid linguistic variant. “Incomplete” means review required,
not automatically incorrect vocabulary. Findings are grouped by dictionary and ID.

Not every catalog form is productive for every word. Absent entries are listed in
`absent_catalog_forms` and verbose output without false errors. Counting-profile
generated forms do not require manual entries. `target_translation` and
`agreement_translations` are optional; pattern-specific requirements are checked
by the solver in Kotomi's coverage diagnostics. A parser failure exits with code 1
and explicitly states that remaining words were not scanned. Fix the structure
and rerun. Warnings alone retain exit code 0. An unknown dictionary filter is an error.

CI retains `tools/validate_repository.py`, unittest and
`tools/validate_question_patterns.py`. Bounded audit tests join the unit suite;
production quality and coverage results remain manual. Verb coverage, empty
patterns and unused words are checked by `tools/diagnostics/run_diagnostics.bat`
in Kotomi, without a second solver in Data.

Current complete examples: [target](target_government_c32.md),
[categories](noun_role_categories_c3.md), [relatives](relative_clauses.md).
`depends_on` belongs to operations in historical audit proposal JSON, not to word
or role XML. C1/C2 are stage-specific reports; this tool audits the current data.

Current revision results: [JSON report](../validation/developer_tools_audit.json). 380 words, 0 errors, 24 warnings: 15 explicit nouns exception declarations and 9 adjective conjugation variants. All 122 verbs have coverage; 22 words have no demonstrated lexical use in patterns. Literal kana in patterns is not a dictionary reference. The audit did not change vocabulary or translations.
