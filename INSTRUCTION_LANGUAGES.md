# Source-language scope

The canonical production bundle declares `instruction_language_id="pl"`; the
project target is `target_language_id="ja"`. Translation, case, agreement,
government, context and source-pattern data belong to that instruction-language
scope. Japanese lexical IDs and exact Japanese forms keep their existing meaning.

The additive metadata is compatible with Project Schema 2. New readers reject a
file whose declared instruction language conflicts with the active project.
Legacy Polish element names are preserved by the Polish language implementation.

`instruction_languages/test/` is an intentionally small no-grammar probe bundle.
It exists to exercise the same runtime language-selection path as a future real
instruction language, while declaring no cases, agreement classes or morphology.
Its source strings are simple English-like test values, not production English
content. The bundle is deliberately separate from the canonical Polish Content
snapshot and is not listed in `content_update_manifest.json`.

A future production language should use its own project manifest and source file
paths. Source patterns can differ structurally and do not require one-to-one slot
mapping to Polish. A real English implementation and dataset remain out of scope.
