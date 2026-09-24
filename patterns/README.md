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



Every placeholder has at most one comma-separated property block. Aliases name
selection identity, while realization links are declared explicitly with
`agree:@alias`, `case:@alias`, `form:@alias`, `government:@alias`, and
`pool:@alias`. Forward references are valid across the question and answer.

Noun-owned source-language relations use `[relation:...]`. The selector reads
the selected noun's relation profile and renders the declined noun by default:

```text
{noun[category:place, relation:location].phrase}     -> w szkole / na plaży
{noun[category:place, relation:destination].phrase}  -> do szkoły / na plażę
```

Use `.phrase` for the full phrase, `.preposition` for the preposition without
trailing whitespace, and `.case` for the resolved case name. Do not combine
`[relation:...]` with `[case:...]` or `[government]` on the same noun
occurrence.

Use government when the Polish realization is controlled by the selected verb.
Use relation when the Polish realization is lexical to the selected noun. The
Japanese role/particle remains independent from both source-language mechanisms.

Object questions keep the Japanese lexical variant explicit where it matters,
for example `{interrogative@object[id:nani].translation}` together with
`{verb@action[role:object, form].translation}`. Governed interrogatives are
matched to their unique compatible role-bearing verb. The selected
interrogative still carries its own `asks_for` and
`target_categories`; its `polish_forms` owns `co/czego/czym`, while verb
government contributes only case plus preposition. For question families
where the semantic intent uniquely identifies the interrogative, prefer
`[asks_for:...]` over a concrete `[id:...]`. The lexical `się` stays in
verb/form translations; `grammar_rules.xml` only declares it as a movable
Polish clitic for question word order. It is not part of the government frame.


Governed Polish noun phrases use `[government]`. The engine infers a unique
role-bearing verb, or the pattern names it explicitly as `[government:@action]`.
The `.phrase`, `.preposition`, and `.case` outputs expose the full phrase or its
parts for constructions that place an adjective between them.

Use `[agree]` on a dependent word when its Polish translation must agree with a
noun. With one compatible noun the binding can be inferred. With several nouns
declare `[agree:@item, case:@item]`; agreement class and case are independent
links and token order is never a fallback. Agreement can also use a fixed class
such as `[agree:neuter]`. Noun aliases and adjective or interrogative aliases
must remain distinct.

`[agree:neuter]` declares a fixed agreement class for a construction without a
noun, for example `To {adjective[form, agree:neuter].translation}`. Lexical
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
