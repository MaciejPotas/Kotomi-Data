# Dictionaries

This directory owns Kotomi's lexical dictionaries.

Files:

- `verbs.xml`
- `nouns.xml`
- `adjectives.xml`
- `copulas.xml`

All dictionary files use project Schema 1 and are referenced by `../quiz_project.xml`. Dictionary IDs are part of the data contract and can be referenced by lessons, grammar, patterns, and quiz code, so renaming an ID requires updating every reference and the validation tests.

Keep word data here. Grammar rules, sentence patterns, and lesson organization belong in their corresponding directories.

The `interrogatives` dictionary stores Japanese question words as form-less lexical entries. `asks_for` describes the information requested (for example `place`, `reason`, or `method`); grammar patterns still own particles and sentence structure.
