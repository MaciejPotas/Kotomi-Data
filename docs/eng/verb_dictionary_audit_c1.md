# C1: verb dictionary audit

[The report and complete evidence](../validation/verb_dictionary_audit_c1.md)
cover 122 verbs, 1817 forms and every usage declaration at pinned revisions of
both repositories. Classification: A 34, B 78, C 7, D 3.

The proposed later C2 scope contains 316 explicit translations across 136 forms
and 33 new `subject` roles. All A proposals were checked on temporary Content.
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
