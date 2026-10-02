# Grammar

This directory contains reusable grammar data used by the Schema 2 project.

- `grammar_rules.xml` owns grammar-wide roles, features, noun categories, form catalogs, agreement catalogs, noun relation profiles, and noun-case rules.
- `counting.xml` owns counting classes, class-to-counter compatibility, class defaults, compositional number and counter profiles, terminal digit/unit rewrites, the source language, source count profiles and their authoring strategies, exact, periodic or ranged quantity mappings, and named number sets.
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

Retired form attributes such as `style`, `polarity_group`, and `quiz` are not part of Schema 2 and must not be added back.

Dictionary XML files store only word-specific realizations through `<form ref="...">`.
They must not duplicate grammar metadata such as context, polarity, register, labels, or lesson aliases.

`noun_case_by_form` maps grammar polarity directly to a noun case. It does not maintain a second list of form names or form sets.

All grammar files are loaded through `../quiz_project.xml`. Keep grammar-wide definitions here rather than placing them beside dictionaries or sentence patterns.

## Counting grammar

Each counting class lists its compatible counter references and one default
counter. Nouns store only selected class IDs and an optional exceptional
`preferred_counter` override. Counter dictionaries store lexical values,
exact quantity realizations and a reference to a grammar-owned composition
profile, but not noun compatibility. Exact output fields override composition
independently, while symbolic quantities always require exact data. This makes
`counting.xml` the single source of truth for class-to-counter matching and
reusable composition rules.

The `one` source profile uses `fallback="noun_case"`; nouns therefore store
only explicit `few` and `many` forms that differ from their ordinary cases.
The file-level `source_language` identifies those editable source forms.
Non-fallback profiles declare `source_form_strategy`; Studio executes that
strategy without inferring a profile's meaning from its mapped quantities.
Every profile also declares `source_agreement`. This metadata can feed the
ordinary `agree:@alias` resolver, so source predicates such as Polish
`jest`/`są` are selected by grammar data rather than number heuristics.

## Polish agreement catalogs

`agreement_catalogs` define how a stored lexical agreement value is realized
for one dictionary schema and optional form. Dictionary `<polish_forms>` own
the actual declension of a word. A catalog owns only reusable grammar behavior:

- `schema` and optional `form` select the dependent-word realization;
- optional `features` restricts a catalog to words declaring all listed
  grammar features;
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

The verb catalogs for `jest`, `są`, `była`, `było`, and `były` require the
generic `existential` feature. Consequently ordinary verbs cannot acquire an
existential Polish realization merely by declaring `[agree:...]`.


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

A frame defines only the noun case, an optional preposition, and whether
realization changes with the selected form's polarity. Question intent stays
on the interrogative through `asks_for`, and the interrogative's
`polish_forms` owns case forms such as `co/czego/czym`.

`polish_clitics` is a grammar-owned catalog of movable Polish tokens such as
`się`. Their lexical presence remains only in verb/form translations, for
example `zastanawiam się` or `nie zastanawiam się`. Question rendering may
reposition a declared token, but government never stores or duplicates it.

The pattern engine never derives a Polish case or question word directly from
a Japanese particle. In particular, `role:object` does not mean accusative and
does not mean `co`.

## Question form rules

`question_form_rules` constrain finite forms for an interrogative `asks_for`
intent when the Polish prompt contains a fixed tense or polarity. For example,
price, people-count, and age prompts are present affirmative, while the manner
question permits past forms but not negative forms. Compatibility reads these
contexts and polarities from XML instead of maintaining a pattern-name list in
Python.


## Counting metadata

Schema 2 grammar defines reusable `counting_classes`, `count_source_profiles`, exact, periodic or inclusive range quantity-to-profile mappings, compositional number/counter profiles, and named `number_sets`. A number's semantic identity stays language-neutral. Periodic mappings classify suffix-dependent source forms without embedding language rules in Python. Counter variants match the terminal numeric component, not the full value modulo ten. Ranges create lazy numeric candidates without adding dictionary words and must stay inside the declared number-composition domain. Generated ranges expose numeric/Japanese outputs only; lexical `id` and `set` selections own source-language translation and agreement. Source-form language and authoring strategy are explicit `counting.xml` data. Polish counted noun selection is resolved from the grammar mapping and effective case.

## Named number sets

Schema 2 publishes the canonical counting domains `one_to_ten`,
`two_to_four`, and `two_or_more`. Sets contain only existing number
dictionary entries. Exact exceptional values, such as age 20, remain ordinary
number entries selected by `id` or another pattern constraint.
