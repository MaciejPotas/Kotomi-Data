# Patterns

This directory contains sentence-generation and sentence-quiz definitions.

- `sentence_maps.xml` owns sentence patterns and constructions used by the generator.
- `sentence_quizzes.xml` owns sentence-quiz definitions that select or combine those patterns.

Both files use Schema 1 and are referenced by `../quiz_project.xml`.

Pattern syntax is interpreted by Kotomi's shared engine. When changing the pattern language or selectors, update Kotomi engine tests together with the data that depends on the new behavior.
