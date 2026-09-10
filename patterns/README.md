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
