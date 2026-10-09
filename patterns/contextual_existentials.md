# Counted existential migration

Polish: [Opis migracji](contextual_existentials.pl.md).

Content revision 51 requires Kotomi 1.4. Two patterns use `semantics_version="2"`:

- `Istnienie policzonych rzeczowników`, introduced in revision 50 for Kotomi 1.3;
- `Istnienie policzonych opisanych rzeczowników`, added in revision 51 for Kotomi 1.4.

Both are available in the `counting` quiz. Their predicate form is dynamic, the
noun is governed by that predicate, and number agreement follows the noun's
construction case. The second pattern adds an adjective with `agree:@item` alone;
its effective class and case come from the shared construction. See the
[stage 4A contract and limitations](contextual_counted_adjectives.md).
No forms are embedded as literal text. `Ile jest policzonych rzeczowników`
keeps its previous definition and semantics 1.

Revision 50 added the feminine genitive of `one`, genitive forms of 3–10,
and `existential_subject` source government for `iru`. Revision 51 retains those
data and adds the described-noun pattern and its quiz reference. Existing counted
noun forms, adjective forms, Japanese counters and verb forms are unchanged.
Grammar rules remain in Kotomi's language layer, not in Content.

The supported canonical number set is 1–10. Integration in Kotomi checks feminine,
neuter, masculine inanimate and masculine animate nouns, including book, car,
inu and ringo. This does not claim collective numerals, masculine personal
agreement, pluralia tantum, or source forms for arbitrary generated numbers.

Negative exercises describe an indicated group of N objects missing, not a
universal equivalence between negation scopes or a zero total. Kotomi's technical
`docs/contextual_existentials.md` defines this exercise scope and realization flow.

Merge this Data PR before the matching Kotomi PR and update the gitlink to its
reviewed commit. Kotomi 1.3 and earlier reject revision 51's 1.4 requirement before
installation. Version 1.3 understands the original semantics-2 construction but
cannot realize its contextual adjective extension. Do not bypass that requirement
or install this revision manually into an unsupported application.
