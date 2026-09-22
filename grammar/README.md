# Grammar

This directory contains reusable grammar data used by the Schema 1 project.

- `grammar_rules.xml` owns grammar-wide roles, features, noun categories, form catalogs, agreement catalogs, noun relation profiles, and noun-case rules.
- `contexts.xml` contains reusable context pools used by sentence generation.

## Form catalogs

`grammar_rules.xml` is the single source of truth for grammatical form metadata.
Each `<form_catalog schema="...">` defines the forms available to one dictionary schema.
A form definition may contain:

- `name`: canonical engine identifier.
- `label`: human-readable form label used by lesson and quiz UIs.
- `lesson_name`: optional persisted lesson alias when the lesson-facing name differs from the engine name.
- `context`: context pool family, for example `present`, `past`, or `none`.
- `polarity`: `affirmative` or `negative` for finite forms.
- `register`: `plain` or `polite` for finite forms.

Quiz selectability is derived rather than stored. A form is a standard selectable finite form when it has a real context plus both polarity and register. Derived and non-finite forms use `context="none"` and omit polarity/register.

Polarity counterparts are also derived. For every finite `(context, register)` pair the catalog must contain exactly one affirmative and one negative form, so no separate `polarity_group` is stored.

Retired form attributes such as `style`, `polarity_group`, and `quiz` are not part of Schema 1 and must not be added back.

Dictionary XML files store only word-specific realizations through `<form ref="...">`.
They must not duplicate grammar metadata such as context, polarity, register, labels, or lesson aliases.

`noun_case_by_form` maps grammar polarity directly to a noun case. It does not maintain a second list of form names or form sets.

Both grammar files are loaded through `../quiz_project.xml`. Keep grammar-wide definitions here rather than placing them beside dictionaries or sentence patterns.

## Polish agreement catalogs

`agreement_catalogs` define how a stored lexical agreement value is realized
for one dictionary schema and optional form. Dictionary `<polish_forms>` own
the actual declension of a word. A catalog owns only reusable grammar behavior:

- `schema` and optional `form` select the dependent-word realization;
- `default_case_ref` supplies a case only for fixed agreement such as
  `[agree:neuter]`; noun-bound agreement always reuses the noun's resolved case;
- `fallback="translation"` explicitly preserves generation when a lexical
  agreement value is absent;
- lexical catalogs use a common `<template value="...{value}...">` and
  exactly one `{value}` marker; class-specific templates may override it;
- `lexical="false"` declares a grammar-only realization whose templates do
  not contain `{value}`, for example an inflected Polish copula.

For example, predicate adjective catalogs can store `jest {value}`, plural
`są {value}`, feminine past `była {value}`, and neuter past `było {value}`.
Copula catalogs can instead store complete realizations such as `był`,
`była`, `było`, and `były` with `lexical="false"`. The engine resolves
the relation, agreement class, and case, then applies this data. It does not
contain Polish gender tables or pattern-specific exceptions.


## Polish noun relation profiles

Some Polish preposition and case choices belong to the noun, not to the verb.
Place nouns are the clearest example:

- `school`: `w szkole`, `do szkoły`;
- `kaigan`: `na plaży`, `na plażę`;
- `station`: `na stacji`, `na stację`.

These choices live in reusable `polish_noun_relations` profiles. A noun only
stores a profile reference:

```xml
<relations language="pl" profile="place_na_na" />
```

The profile defines each supported semantic relation:

```xml
<profile id="place_na_na">
  <realization relation="location" case_ref="locative" preposition="na" />
  <realization relation="destination" case_ref="accusative" preposition="na" />
</profile>
```

The engine does not infer the Polish preposition from spelling, category, or
Japanese particle. It resolves the selected noun's profile and reads the
declared `preposition` and `case_ref`.

This is intentionally separate from Polish verb government. Government answers
"how does this verb realize its argument?", while a noun relation profile
answers "how is this noun realized as a location/destination/etc.?".


## Polish verb government

Japanese roles and Polish argument realization are independent:

- role:object selects the Japanese object relation and particle を;
- accepts and nouns constrain compatible vocabulary;
- government on a verb usage entry references a Polish frame from polish_government.

A frame defines the noun case, an optional preposition, and whether realization
changes with the selected form's polarity. The pattern engine never derives a
Polish case directly from a Japanese particle.
