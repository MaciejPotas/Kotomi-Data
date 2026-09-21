# Grammar

This directory contains reusable grammar data used by the Schema 1 project.

- `grammar_rules.xml` owns grammar-wide roles, features, noun categories, form catalogs, and noun-case rules.
- `contexts.xml` contains reusable context pools used by sentence generation.

## Form catalogs

`grammar_rules.xml` is the single source of truth for grammatical form metadata.
Each `<form_catalog schema="...">` defines the forms available to one dictionary schema.
A form definition may contain:

- `name`: canonical engine identifier.
- `label`: human-readable form label used by lesson and quiz UIs.
- `lesson_name`: optional persisted lesson alias when the lesson-facing name differs from the engine name.
- `context`: context pool family, for example `present` or `past`.
- `style`: human-readable grammatical style.
- `polarity`: `affirmative` or `negative` when applicable.
- `register`: `plain` or `polite` when applicable.
- `polarity_group`: pair used by local `[polarity:...]` transformations.
- `quiz`: whether the form is selectable as a quiz form.

Every polarity group must contain exactly one affirmative and one negative form.
Both members must preserve the same `context` and `register`; only polarity may change.

Dictionary XML files store only word-specific realizations through `<form ref="...">`.
They must not duplicate grammar metadata such as context, polarity, register, labels, or lesson aliases.

`noun_case_by_form` maps grammar polarity directly to a noun case. It does not maintain a second list of form names or form sets.

Both grammar files are loaded through `../quiz_project.xml`. Keep grammar-wide definitions here rather than placing them beside dictionaries or sentence patterns.
