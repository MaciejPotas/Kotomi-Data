# Grammar and Sentence Data

This directory owns the non-dictionary inputs used by Kotomi's sentence engine and sentence quizzes.

`grammar_rules.xml` defines reusable grammar relationships and roles. `contexts.xml` provides context pools. `sentence_maps.xml` contains sentence patterns and composite pattern data. `sentence_quizzes.xml` selects patterns for sentence-quiz configurations.

All four files are referenced from `../quiz_project.xml` and currently use project Schema 1.

Keep this directory declarative. Python quiz implementation code belongs in the private Kotomi source repository and generated public packages belong under the repository-level `quizzes/` directory.

Changes to the pattern language itself must be made together with the Kotomi parser, writer, tests, documentation, and migrated XML. Do not introduce a second syntax only in public data.
