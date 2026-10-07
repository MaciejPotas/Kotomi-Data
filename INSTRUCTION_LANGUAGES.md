# One Content database, optional source grammar

`quiz_project.xml` is the single canonical production project. Grammar selection
never selects a different Content database. Switching grammar is non-destructive
and does not mutate Content, word IDs, paths, patterns, lessons or Content revision.

Kotomi offers Default and Polski. Default always retains Japanese/common grammar,
counting and authoring, while treating translation as opaque text. Polish activates
optional source cases, agreement, government, relations and counted forms on the
same Word. It neither verifies existing translations nor enriches them automatically.
Autofill is an explicit authoring action, committed only with the accepted edit.

The manifest's `instruction_language_id="pl"` remains default/compatibility metadata.
An explicitly selected grammar context may load the same Content as Default.
Nested source declarations are validated when that source grammar is active.
Default ignores source extensions for generation and preserves them during edits.
No multi-source Word or translation overlay is introduced.

Words without source morphology remain valid. A pattern requiring a missing
realization cannot select that word; a simple translation pattern can. Unknown
class/profile/frame references remain structural errors under the active provider.

Japanese grammar and source grammar definitions belong to Kotomi. Content owns
complete lexical entries and learning material. New Content rejects `<editor>`,
`<grammar file>` and grammar-owned counting sections. `grammar/counting.xml` owns
only counter bindings/defaults and number sets; it declares no source language.

TestLanguage and its diagnostic Content are test-only fixtures in Kotomi. They are
not production registry options or Content update files. Production English and
multi-source storage remain outside this PR.
