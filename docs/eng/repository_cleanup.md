# Content architecture and cleanup audit — PR 93 follow-up

[Repository](../../README.md) · [Category contract](semantic_category_catalog.md) ·
[Developer commands](developer_tools.md)

## Ownership and data flow

`quiz_project.xml` is the entrypoint: it declares dictionaries, grammar Content,
patterns and sentence quizzes. Kotomi loads application grammar first, then the
optional Content category hierarchy, then words and references. Lesson membership
is a separate catalog; it does not own a word's meaning or limit generator use.

| Directory / source | Responsibility | Consumer / extension point |
|---|---|---|
| `grammar/categories.xml` | Complete semantic hierarchy, one optional parent per category | Data validator and Kotomi loader; add IDs here and validate references, selectability and cycles |
| `grammar/contexts.xml` | Lexical context choices and references | Context loader and DSL selection; keep referenced dictionary IDs valid |
| `grammar/counting.xml` | Counter bindings and study number sets | Counting Content loader; composition algorithms stay in Kotomi |
| `dictionaries/` | Explicit vocabulary, forms, translations, categories and lexical links | Shared generator and word editors; unused-in-lessons does not mean unused |
| `patterns/` | Simple/composite question/answer DSL and sentence-quiz profiles | Application parser/renderer; rename IDs together with composite/quiz references |
| `lessons/` | Schema-4 lesson organization and inline dictionary/pattern references | Lesson catalog loader; one word may belong to multiple lessons |
| `quizzes/` | Independently versioned executable quiz releases | Quiz registry/updater; not part of the lexical Content revision |
| `tools/`, `tests/` | Standalone validation and opt-in audits; bounded mutation fixtures | `validate_repository.py`, `validate_question_patterns.py`, `run_tests.py` |

Data owns declarations, not a second grammar engine. `validate_semantic_categories`
checks dictionary categories and delegates explicit canonical DSL category IDs to
`validate_pattern_category_references`. Full DSL parsing and compatibility remain
in Kotomi. Content without a declared category catalog retains legacy behavior.
See the category guide for exact syntax and parser-boundary examples.

For a new data declaration, update the owning XML and its references, run both
validators and synthetic tests, then application structural validation. If the
shipped payload changes, regenerate Content hashes/revision through the application
publisher; documentation/tool-only changes do not need a revision increase. The
updater follows manifest paths, including categories; cache dependency stamps
include those same sources. Do not remove a word merely because no lesson uses it.

## Complete repository audit

The starting inventory covered all 172 tracked files: 13 dictionary-area files,
4 grammar files, 9 pattern files, 3 lesson files, 61 documents, 20 tools, 28 test/
fixture files, 21 quiz-package files, plus root manifests/configuration/launchers/CI.
Checks combined manifest/path readers, byte-identical grouping, Python imports and
call sites, dynamic package entrypoints, validation/report inputs, CI and documented
manual commands. No absence-of-import heuristic was used as deletion proof.

| Candidate / area | Decision | Evidence / validation |
|---|---|---|
| Four `patterns/contextual_{counted_adjectives,existentials}*.md` stubs | MERGE | Each language pair is byte-identical and redirects to `grammar_contexts.md` / `.pl.md`; direct navigation replaces duplicates |
| `grammar/categories.xml`, `contexts.xml`, `counting.xml` | KEEP | Explicit project/Content manifest consumers; distinct semantic, lexical-context and counter responsibilities |
| Category compatibility catalog inside Kotomi | KEEP | Fallback for older Content, not a second active Data catalog |
| All dictionary words/forms/categories/translations | KEEP | Generator, simulator and quizzes use them independently of lesson membership; no lexical XML changes |
| Patterns, composites, quiz profiles, lesson catalog | KEEP | Manifest or runtime references; repository/question validators check published relationships |
| Published `quizzes/*` copies | KEEP | Separate package release channel. Source lives in Kotomi `apps/*`; deduplication would break independent installs |
| `_rules_for_slot` in shipped grammar quiz | UNCERTAIN | No direct call found, but cleanup would require a separately versioned quiz publication; retained with its source copy |
| C1 proposal JSON and C3 decisions | KEEP | `validate_repository.py` / integration validators read them as release contracts; they are not disposable generated reports |
| Historical acceptance/performance reports | UNCERTAIN | Evidence for pinned releases and external review, not reliably proven dead; retained |
| `tools/*`, root batch launchers | KEEP | CI, documented CLI or opt-in acceptance entrypoints; not expected to be imported by runtime |
| Tests and bounded fixtures | KEEP | Discovery and mutation contracts; no production inventory assertions added |
| Content/quiz manifests, revision and CI configuration | KEEP | Intentional publication inputs. Documentation-only cleanup leaves payload hashes and revision unchanged |
| Local caches, pyc and build output | KEEP outside Git | Ignored transient files, not published artifacts |

## Verification and limitations

Run `python tools/run_tests.py`, `python tools/validate_repository.py` and
`python tools/validate_question_patterns.py`. Unit tests mutate independent fixtures;
optional engine checks may be skipped when the companion Kotomi path is unavailable.
No new dependency on Kotomi, full database loading or generation is introduced.
The published Content and quiz payload files are unchanged byte-for-byte by this
follow-up. Application submodule pinning still advances to this documentation commit.
The audit cannot prove external consumers of historical reports do not exist, hence
the explicit UNCERTAIN decisions instead of speculative deletions.
