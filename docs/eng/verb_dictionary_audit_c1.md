# C1: verb dictionary audit

[The report and complete evidence](../validation/verb_dictionary_audit_c1.md)
cover 122 verbs, 1817 forms and every usage declaration at pinned revisions of
both repositories. Classification: A 33, B 79, C 7, D 3.

The proposed later C2 scope contains 308 explicit translations across 132 forms
and 32 new `subject` roles. All A proposals were checked on temporary Content.
Categories describe the four priority forms and ordinary subject relatives;
other forms have separate assessments. A does not certify the entire verb.

C1 changes no dictionaries, patterns, quizzes or manifests. C2 requires approval.
The reports include exact values and B/C decisions, but only the JSON `changes`
operations are A proposals for later implementation. The detailed linguistic
report is in Polish; IDs, paths and structured operation fields are language-neutral.

Run the completeness check separately from unit tests:

```sh
python tools/validate_verb_dictionary_audit.py --kotomi ../Kotomi
```

The report records regression results, performance samples, linguistic limits
and an implementation plan. Engine contract guides remain unchanged.

After review, `nonbiri_suru` moved from A to B and `tori` was removed from the
`iku`, `kuru`, `deru`, `hairu` proposals. Production translations are unchanged.
`chigau/potential` and `wakaru/potential` are not approved as conjugation tasks.

Without `--kotomi`, the validator checks operation completeness, exact dependencies,
statistics, local role definitions and subject classes. With `--kotomi`, the original
engine checks OR matching, inheritance, role defaults and availability. Skipped
engine checks are explicitly reported in standalone mode.

The A experiment and tests were rerun after review: 295 pairs, 1180 visible examples,
30940 unchanged object-relative realizations, 57 Kotomi-Data tests
(with `KOTOMI_PATH`, including 23 new tests) and 162 Kotomi tests. Performance
measurements are retained as historical; they were not rerun for the revised proposal.
