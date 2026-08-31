# Lessons

This directory owns the user-facing lesson catalog in `lessons.xml`.

The lesson catalog has its own persistence contract and currently uses lesson catalog Schema 4. It is intentionally separated from the Schema 1 sentence project because lessons organize learning material, while `../quiz_project.xml` describes dictionaries and sentence-generation inputs.

Lesson words may reference shared dictionary entries by dictionary ID and word ID. Keep those references synchronized when shared dictionary identifiers change.

Do not add quiz implementation Python files here. Lesson quiz runtime code is maintained in the private Kotomi repository and published separately through the quiz package channel.
