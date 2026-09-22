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
`<polish_forms>`. The latter contains zero or more `<common>` entries and
zero or more `<override classes="...">` entries. Each entry uses a
space-separated `cases` attribute and one `value`, so a form shared by several
cases is stored only once. There may be several common and override entries.
An override contains only values that differ from `common`; identical class
and case groupings are combined. The writer groups values in canonical case
and class order and removes redundant overrides on save.

The runtime only looks up `specific -> common -> translation`. It does not
infer a class from a semantic category and does not create Polish forms from
spelling, endings, stems, or profiles. Missing agreement metadata is valid and
falls back to the adjective's normal `translation`.


## Noun relation profiles

A noun may reference a reusable source-language relation profile:

```xml
<relations language="pl" profile="place_w_do" />
```

The profile itself is owned by `grammar/grammar_rules.xml`; the dictionary does
not duplicate prepositions or case rules. This lets multiple nouns share the
same realization while still allowing lexical differences such as
`w szkole / do szkoły`, `na plaży / na plażę`, or
`we wnętrzu / do wnętrza`.

Relation profiles are authoring data. Runtime does not infer a profile from the
noun category or Polish spelling.
