# C1 validator fixture v1

`v1.json` is a hand-authored, bounded synthetic fixture: two invented verbs,
three nouns and nineteen forms (all existing C1 policy groups). It is independent of all production dictionaries,
lessons and quizzes. Its Japanese text is a placeholder, not linguistic evidence.
Tests mutate copies in memory. Never regenerate this fixture from Content.

Default tests exercise the standalone validator and comparison boundaries.
With `KOTOMI_PATH=/absolute/path/to/Kotomi`, four additional tests use the real
engine's `role_matches` with synthetic model objects, including OR, inherited
categories, role defaults and wildcard behavior. They load no project or dictionary.

The fixture also contains main verb properties, nested feature refs and complete
CSV columns. Empty kanji and specific findings intentionally remain valid.
