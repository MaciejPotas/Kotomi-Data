# Dictionaries

This directory owns Kotomi's reusable lexical dictionaries:

- `verbs.xml`
- `adjectives.xml`
- `nouns.xml`
- `copulas.xml`

The dictionary IDs and filenames are declared by the repository-level `quiz_project.xml`. Sentence patterns refer to dictionary-backed slots through that project model, not through filesystem lookups of their own.

Keep word identifiers stable when editing existing entries because lessons and grammar data may reference them. Dictionary XML currently uses project Schema 1.

Dictionary content belongs here even when a word is mainly used by one lesson or one sentence pattern. Lesson-only words remain a lesson-catalog concern and should not be introduced into these shared dictionaries unless they are intended to be reusable learning data.
