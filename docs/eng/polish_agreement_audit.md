# Full Polish agreement audit, Content 69

The audit covers all **394 entries in 11 dictionaries**, every stored verb form, seven agreement classes, noun cases and counting profiles. Baseline: Content `e604502180113b47235a7724a09fe37f7dc9ca3b` (revision 68). Per-word/form decisions: [polish_agreement_review.json](../validation/polish_agreement_review.json). This is an audit record, not engine configuration or a test fixture.

## Findings and changes

| Scope | Result |
|---|---|
| Verbs | 124 reviewed, 118 extended, **7388 added cells**, 9612 total |
| Core finite forms | 115 verbs with seven classes; three process verbs with four role-compatible classes; six exceptions below |
| Other verb forms | Extended stored potential, conditional, causative, progressive, desiderative and 58 straightforward passive forms |
| Nouns | 90/90 have seven cases; all 68 counted entries have complete existing few/many profiles |
| Adjectives | 92/92 have complete seven-class, seven-case matrices |
| Interrogatives | Five adjective-like entries have complete matrices; the other 17 require their own constructions rather than 49 adjective cells |
| Demonstratives | Three attributive modifiers have complete matrices; three standalone pronouns retain their own declension |
| Numerals | 11/11 reviewed, **90 added cells**; explicit masculine-personal plural, correct dwaj/trzej/czterej and dwóch/trzech/czterech; jeden also receives adjectival vocative |
| Other dictionaries | 16 adverbs, seven connectors, one copula, 23 counters, two expressions; copula and numerical constructions use catalogs, without invented verb paradigms |

Existing base translations, Japanese forms and role categories are preserved. Added 28 missing Japanese forms (21 progressive and seven desiderative), their Polish glosses and agreement cells, and marked seven movement verbs as intransitive. Verb additions preserve the aspect and reflexivity of each stored form: podniosłem yields podniósł/podniosła/podnieśli rather than forms derived from the base imperfective podnosić. Inflection was checked with SGJP/Morfeusz 2; the otworzył and śmiali się alternatives and descriptive constructions were resolved explicitly. New kureru cells agree with the giver (daje mi / dają mi), retaining the receiver mi.

## Example: hataraku

| Form | Masculine singular | Feminine singular | Masculine-personal plural | Other plural |
|---|---|---|---|---|
| polite_nonpast | pracuje | pracuje | pracują | pracują |
| past_polite | pracował | pracowała | pracowali | pracowały |
| past_negative_polite | nie pracował | nie pracowała | nie pracowali | nie pracowały |
| potential | może pracować | może pracować | mogą pracować | mogą pracować |
| tara | jeśli pracuje | jeśli pracuje | jeśli pracują | jeśli pracują |
| causative | każe komuś pracować | każe komuś pracować | każą komuś pracować | każą komuś pracować |

Neuter and both other masculine classes, plain forms and progressive also have separate cells. A normal quiz without agree still uses the original pracuję.

## Deliberately empty cells

- aru_existential and iru: finite forms use the existential catalog with government, including nie ma rodziców. Other constructions need separate participant analysis.
- fuku, furu, hareru and kumoru: the current model represents weather predicates without a lexical subject role. Causative/passive constructions change participant roles and cannot be completed by mechanically inflecting weather for personal gender.
- aku, shimaru and owaru: core, conditional and potential forms (when stored) cover masculine inanimate, feminine, neuter and non-masculine-personal plural. Personal variants are not added against role restrictions.
- te_form uses a nonfinite adverbial gloss without person/number; volitional expresses speaker intention or first-person plural; imperative addresses a second person. Third-person agreement cells are not automatically appropriate.
- 58 stored passive forms remain without maps: affected-person and descriptive clauses involving ktoś, mi and mnie need case, perspective and participant binding. They are not classified as fully agreed.
- Cardinal numerals 2+ have no separate vocative paradigm in SGJP. No artificial values were inserted. Noun few/many profiles do not change the noun's inherent agreement class.

## Additional pattern-audit findings

- mieru: concrete includes person and animal. All seven classes are now present, including jest widoczny / są widoczni. The previous inanimate-only justification was incorrect.
- donata: added six appropriate kto cases, including kim required by companion questions. The original polite base gloss is preserved.
- The residence pattern now explicitly selects id:sumu. Travel without an object requires feature:intransitive; the previously available iku remains supported. Seven corresponding movement verbs now carry that feature. Patterns must not depend on incidental missing forms in other candidates.
- hataraku also receives desiderative: chcę pracować / chce pracować / chcą pracować.
- sugosu/companion now has the appropriate z_instrumental frame, checked through the renderer. Its complete spend-time meaning still requires a duration argument or context.
- Eleven government frames remain unresolved: ten target roles have explicit decisions in [C3.2](target_government_c32.md), while hanashiau/companion contains the ze sobą perspective. They need construction and meaning decisions; no single frame was assigned to heterogeneous complements merely to silence the audit.

[Japanese ている semantics, Japan Foundation](https://www.irodori.jpf.go.jp/assets/data/elementary02/pdf/Z_L02.pdf) distinguishes ongoing actions from result states. New glosses are explicit data, not runtime-generated translations.

## Verification and architecture

The 114-pattern sweep checked 423,567 relationships and verified 415,903. It left 4,086 unverified units (limits and unsupported scopes); **coverage is incomplete**. Of 16 reported errors, four missing forms and the sugosu government frame were fixed; scoped rechecks of those five words reported zero errors. The remaining 11 government limitations are documented above. This bounded check is not exhaustive sentence enumeration.

Full QuizProject.validate() after the changes: **zero issues**. The renderer checked **9612/9612 verb cells**, using synthetic nominal class representatives and comparing Japanese output with the stored form. This diagnostic verifies individual cells, not every role/sentence combination.

Application review found an autofill bug: SGJP returns every degree of a lexeme, and selecting only pos changed najlepszy to dobrzy. The fix preserves the input degree with independent tests. Validation now reads the language-owned explicit-class catalog instead of a hardcoded Polish class name.

Both audit tools expose missing classes for every stored form. Passing XML validation or completing eight masculine-personal forms does not imply a full agreement matrix. The historical C2 gate preserves all approved values and roles while permitting explicitly allowed additions in other classes.

New unit tests use only small independent fixtures. Production Content auditing remains opt-in. Exhaustive sentence enumeration, linguistic review of every historical translation and Android integration are outside the verified results of this audit.
