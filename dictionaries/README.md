# Dictionaries

This directory owns Kotomi's lexical dictionaries.

Files:

- `verbs.xml`
- `nouns.xml`
- `adjectives.xml`
- `copulas.xml`
- `interrogatives.xml`

All dictionary files use project Schema 1 and are referenced by `../quiz_project.xml`. Dictionary IDs are part of the data contract and can be referenced by lessons, grammar, patterns, and quiz code, so renaming an ID requires updating every reference and the validation tests.

Keep word data here. Grammar rules, sentence patterns, and lesson organization belong in their corresponding directories.

The `interrogatives` dictionary stores Japanese question words as form-less lexical entries. `asks_for` describes the information requested (for example `place`, `reason`, or `method`); grammar patterns still own particles and sentence structure.

Polish adjective agreement is optional lexical data. Nouns may store
`<agreement class="..." />`, while adjectives store ready-to-use values in
`<polish_forms>`. The latter contains one optional `<common>` section and
zero or more `<override classes="...">` sections. An override contains only
values that differ from `common`; classes with identical overrides are grouped
in one space-separated `classes` attribute. The writer normalizes redundant
overrides on save.

The runtime only looks up `specific -> common -> translation`. It does not
infer a class from a semantic category and does not create Polish forms from
spelling, endings, stems, or profiles. Missing agreement metadata is valid and
falls back to the adjective's normal `translation`.
