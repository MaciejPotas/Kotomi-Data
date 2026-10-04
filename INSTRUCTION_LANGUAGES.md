# Source-language scope

This data bundle declares `instruction_language_id="pl"`; the project target is
`target_language_id="ja"`. Translation, case, agreement, government, context and
source-pattern data belong to that instruction-language scope. Japanese lexical
IDs and exact Japanese forms keep their existing meaning.

The additive metadata is compatible with Project Schema 2. New readers reject a
file whose declared instruction language conflicts with the active project.
Legacy Polish element names are preserved by the Polish language implementation.

A future language should use its own project manifest and source file paths.
Source patterns can differ structurally and do not require one-to-one slot
mapping to Polish. This revision contains no English implementation or data.
