# Contexts and counting Content

This directory contains learning material and lexical relationships, not grammar definitions.

- `contexts.xml` owns concrete options such as today, yesterday and next week,
  their word references, literal separator suffixes and selection weights. Inline
  options remain supported; referenced lexical text belongs to dictionaries.
- `counting.xml` owns `number_sets` and `counter_bindings`. A binding references a
  Kotomi counting class and lists this database's compatible/default counter IDs.
- Noun counting classes and preferred counters, exact counter surfaces and
  exceptional quantity realizations remain in complete dictionary entries.

Kotomi supplies form catalogs, agreement templates, semantic categories, roles,
features, government, noun relations and clitics. Its Japanese grammar also owns
number composition and counter composition profiles. The selected source grammar
owns count profiles and quantity-to-profile mappings, including Polish one/few/many.

Content references those IDs but cannot redefine grammar or the Studio schema.
Historical `min_kotomi_version` metadata is not an enforced gate. Content 63+ uses
update manifest format 2 to reject legacy clients; new clients validate the full
snapshot before installation. See the [C3 guide](../docs/eng/noun_role_categories_c3.md).

Number sets such as `one_to_ten`, `two_to_four` and `two_or_more` select vocabulary
for study. Pattern numeric ranges retain their existing semantics and bounds.
No lexical translations are synthesized for generated numeric candidates.

Quiz selectability is derived from the form context and pattern compatibility in
Kotomi. Content forms contain lexical values and a `ref`, not grammar metadata.
