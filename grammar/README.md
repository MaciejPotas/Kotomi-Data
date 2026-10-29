# Semantic categories, contexts and counting Content

| File | Reader and load stage | Decision | Reason |
|---|---|---|---|
| `categories.xml` | `QuizProject.load` after built-in grammar, before dictionaries; Data validator | Keep | Complete declarative semantic hierarchy, editable without rebuilding Kotomi |
| `contexts.xml` | `load_contexts`, after dictionaries | Keep | Lexical context options, dictionary references, suffixes and weights used by DSL and quizzes |
| `counting.xml` | `load_counting_content`, after built-in counting contracts | Keep | Lexical counter bindings and study number sets, not duplicate composition algorithms |
| `README.md` | Developers and maintainers | Refactor | Documents the current ownership boundary and consumers |

The manifest explicitly references all three XML files. They are shipped by the
Content updater and validated before installation. None is an unused grammar
copy. Removing contexts or counting breaks context selection or counter/numeric
study choices. Removing categories loses the Content-defined semantic hierarchy.

Kotomi owns form contracts, roles, features, agreement, government, noun relations,
clitics and Japanese number/counter composition. Semantic category declarations
belong to Content; a new algorithmic behavior still requires a Kotomi change.
Adverb flat catalogs remain in their individual dictionary files.

Quiz selectability is derived from each form's context contract in Kotomi.
Forms with `context="none"`, including `progressive` and `desiderative`, remain
available to patterns that explicitly request them, but are excluded from the
ordinary tense-selection quiz. Their lexical translations belong to Content.

New categories: [English](../docs/eng/semantic_category_catalog.md) /
[Polski](../docs/pl/semantic_category_catalog.md).

Architecture, extension workflow and cleanup decisions: [English](../docs/eng/repository_cleanup.md) / [Polski](../docs/pl/repository_cleanup.md).
