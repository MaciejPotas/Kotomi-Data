# Counted existential migration

Polish: [Opis migracji](contextual_existentials.pl.md).

Content revision 51 requires Kotomi 1.4. Only `Istnienie policzonych rzeczowników`
opts into `semantics_version="2"`: its predicate form is dynamic, the noun is
governed by that predicate, and number agreement follows the noun's construction
case. No forms are embedded as literal text. `Ile jest policzonych rzeczowników`
keeps its previous definition.

The data additions are the feminine genitive of `one`, genitive forms of 3–10,
and `existential_subject` source government for `iru`. Existing forms of `two`,
counted nouns, Japanese counters, and Japanese verb forms are retained. Grammar
rules remain in Kotomi's language layer, not in Content.

The supported canonical number set is 1–10. Integration in Kotomi checks feminine,
neuter, masculine inanimate and masculine animate nouns, including book, car,
inu and ringo. This does not claim collective numerals, masculine personal
agreement, pluralia tantum, or source forms for arbitrary generated numbers.

Negative exercises describe an indicated group of N objects missing, not a
universal equivalence between negation scopes or a zero total. Kotomi's technical
`docs/contextual_existentials.md` defines this exercise scope and realization flow.

Merge this Data PR before the matching Kotomi PR and update the gitlink to its
reviewed commit. Old Kotomi pins old Content; its update compatibility check rejects
revision 50's 1.3 requirement before installation. Never bypass that requirement
or install this revision into Kotomi 1.2 manually.
