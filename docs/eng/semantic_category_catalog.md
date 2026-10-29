# Content-owned noun categories

`quiz_project.xml` declares `<semantic_categories file="grammar/categories.xml" />`.
The complete catalog uses `<noun_categories schema_version="2">` and entries such
as `<category id="body_part" parent="concrete" label="Body part" />`.

Add a unique lowercase ID, one optional existing parent, an optional label and an
optional `selectable="true|false"` flag. All parents must be declared in the same
catalog. Multiple parents are unsupported. Nouns select leaf or other selectable
categories; verbs, adjectives and noun selectors can accept broader parents.
Retain categories referenced by application role defaults and existing Content.

The new Kotomi loader must be installed once. Subsequent category additions use
Content updates only, provided they need no new grammar algorithm. Older Content
without this manifest element uses Kotomi's compatibility catalog. Existing
category IDs explicitly declared here are not rewritten by legacy migrations.

After editing, run `python tools/validate_repository.py`,
`python -m unittest discover -s tests -v`, and the companion Kotomi structural
validation. The standalone validator checks duplicate/unknown categories,
selectability, missing parents and cycles. `tests/test_noun_category_catalog.py`
uses tiny independent fixtures. Kotomi additionally checks pattern constraints and
exposes the catalog in Studio. Runtime/cache dependency checks include this file.

The Data validator also checks explicit `category:id` properties in canonical
`noun[...]` and `adverb[...]` tokens in both question and answer, including
composite templates. Noun IDs use this catalog; adverb IDs use the separate
`adverbs` dictionary catalog. Errors identify the pattern, field and unknown ID.
This is a reference check, not another DSL parser: malformed syntax, unsupported
selectors, alias rules and composite expansion remain Kotomi's responsibility.
Content without `semantic_categories` retains its previous behavior. Synthetic
coverage is in `tests/test_pattern_category_references.py`.

Increment `content_revision.json` and regenerate `content_update_manifest.json`
with Kotomi's `write_content_manifest` tooling. All category changes must be in
the same Content snapshot as the words and patterns using them. No translation,
form, counting algorithm or DSL semantics are changed by a category declaration.
