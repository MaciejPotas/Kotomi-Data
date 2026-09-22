# Patterns

This directory contains sentence-generation and sentence-quiz definitions.

- `sentence_maps.xml` owns sentence patterns and constructions used by the generator.
- `sentence_quizzes.xml` owns sentence-quiz definitions that select or combine those patterns.

Both files use Schema 1 and are referenced by `../quiz_project.xml`.

## Pattern identifiers

A sentence pattern has one user-facing identifier. The `id` is the readable pattern name shown in Quiz Studio and is also the value used by composite-pattern and sentence-quiz references. Do not add a separate `label` attribute to `<sentence_pattern>`.

For example:

```xml
<sentence_pattern id="Reakcja na przyczynę">
  <question>...</question>
  <answer>...</answer>
</sentence_pattern>
```

References use the same value:

```xml
<pattern ref="Reakcja na przyczynę" />
```

Pattern IDs must be non-empty and unique. Renaming a pattern therefore means renaming its references as one atomic content change. Quiz Studio performs this propagation when the pattern is renamed there.

Pattern syntax is interpreted by Kotomi's shared engine. When changing the pattern language or selectors, update Kotomi engine tests together with the data that depends on the new behavior.

Pattern categories are persisted directly on `<sentence_pattern category="...">`. Question patterns use category `questions`. Adverbial question families such as when, reason and method are composites over existing clause shapes; argument-replacement questions remain direct patterns.

The `questions` sentence quiz uses `selection="references"`, so users select question families while the engine expands composites internally and keeps form selection independent.



Noun-owned source-language relations use `[relation:...]`. The selector reads
the selected noun's relation profile and renders the full phrase by default:

```text
{noun[category:place][relation:location]}     -> w szkole / na plaży
{noun[category:place][relation:destination]}  -> do szkoły / na plażę
```

Use `.preposition` and `.case` when a construction needs the two pieces
separately. Do not combine `[relation:...]` with `[case:...]` or
`[government:...]` on the same noun occurrence.

Use government when the Polish realization is controlled by the selected verb.
Use relation when the Polish realization is lexical to the selected noun. The
Japanese role/particle remains independent from both source-language mechanisms.

Object questions keep the interrogative explicit, for example `{interrogative@object[id:nani][asks_for:thing].translation}` together with `{verb@object[role:object][form].translation}`. The shared alias binds the question intent to the verb. `asks_for` selects what is being asked, the interrogative `polish_forms` owns `co/czego/czym`, and the verb government contributes only case plus preposition. A reflexive `się` is lexical verb data, not part of the government frame.


Governed Polish noun phrases use [government:phrase]. The engine links the noun to the role-bearing verb. Use the same @name only when a pattern needs to disambiguate more than one possible pair. [government:preposition] and [government:case] expose the two parts
separately for constructions that place an adjective between them.

Use `[agree].translation` on a dependent word when its Polish translation must
agree with a noun. A shared alias declares the relationship, for example
`adjective@object` and `noun@object`, or `interrogative@item` and `noun@item`.
With one noun the binding can be inferred. With several nouns the common alias
is required; token order is never a fallback. Agreement uses the exact case
already resolved for the noun by `[government:...]`, `[case:form]`, or an
explicit case.

`[agree:neuter]` declares a fixed agreement class for a construction without a
noun, for example `To {adjective[form][agree:neuter].translation}`. Lexical
variants live in dictionary `<polish_forms>`, while grammar
`<agreement_catalogs>` define form-specific templates, default fixed cases,
and the explicit translation fallback. Grammar-only dependents such as the
Polish copula use `lexical="false"`, so forms such as `była`, `było`, and
`były` also come from grammar data rather than Python. Agreement does not
change Japanese forms, roles, government, or embedded `case_scope` behavior.

The price question selects the non-selectable grouping category
`purchasable`, whose descendants are the buyable leaf categories. The
possessor question selects `concrete`. These are taxonomy constraints, not
runtime lists of exceptional nouns.
