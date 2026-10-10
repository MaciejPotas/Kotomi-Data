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

Content references those IDs, and its `min_kotomi_version` declares which Kotomi
contract is required. It cannot redefine the grammar or the Studio schema.

Number sets such as `one_to_ten`, `two_to_four` and `two_or_more` select vocabulary
for study. Pattern numeric ranges retain their existing semantics and bounds.
No lexical translations are synthesized for generated numeric candidates.

Quiz selectability is derived from the form context and pattern compatibility in
Kotomi. Content forms contain lexical values and a `ref`, not grammar metadata.
