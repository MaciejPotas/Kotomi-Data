# Lessons

This directory owns the lesson catalog.

`lessons.xml` uses lesson catalog Schema 4. Lessons may reference words from the dictionaries and patterns from the project, but lesson organization is intentionally kept separate from dictionary and grammar ownership.

When moving or adding lesson content, keep dictionary references valid and run the repository validator before publishing.

A `<word><dictionary_ref dictionary="adverbs" word="kinou" /></word>` can
appear in multiple lessons. Saving keeps the reference; loading resolves the
current dictionary entry. Reload a materialized catalog after editing words.
No lesson/group name imposes a fixed word count. Tests must check universal
reference rules, not the contents of a named lesson. Complete bilingual
examples: [English](../docs/eng/context_vocabulary.md) / [Polski](../docs/pl/context_vocabulary.md).
