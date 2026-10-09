# Contextual counted adjectives (stage 4A)

[Polski](contextual_counted_adjectives.pl.md)

The `counting` quiz now includes **Istnienie policzonych opisanych rzeczowników**.
Its question and answer declare one context, with an optional attributive adjective:

```xml
<sentence_pattern id="Istnienie policzonych opisanych rzeczowników" category="counting" semantics_version="2">
  <question>{verb@existence[role:subject, feature:existential, form, agree:@count].translation} {number@count[set:one_to_ten, agree:@item, case:@item].translation} {adjective@quality[form:attributive_nonpast, agree:@item].translation} {noun@item[quantity:@count, government:@existence]}.</question>
  <answer>{adjective@quality[form:attributive_nonpast]}{noun@item}が{counter@unit[counts:@item, preferred, quantity:@count]}{verb@existence[role:subject, feature:existential, form]}。</answer>
</sentence_pattern>
```

## `agree` supplies the effective noun context

In this semantics-2 construction, `agree:@item` identifies the counted noun,
its lexical class, selected quantity/profile and effective predicate form.
It therefore supplies both the adjective's effective agreement class and case.
The planner follows aliases, never token proximity. The adjective can appear
elsewhere in the question without changing its grammatical controller.

| Quantity profile | Affirmative adjective | Negative adjective |
|---|---|---|
| one (`noun_case`) | Noun class, nominative | Noun class, genitive |
| few (`paucal`) | Non-masculine-personal plural, nominative | Non-masculine-personal plural, genitive |
| many (`genitive_plural`) | Non-masculine-personal plural, genitive | Non-masculine-personal plural, genitive |

Thus `Było pięć czerwonych książek` has a nominative **construction**, a neuter
predicate, and a genitive plural adjective. Passing the noun's lexical gender
and construction case directly to the adjective would be incorrect.

In semantics 1, `agree` still supplies agreement while `case` selects a case
independently. Explicit cases outside this context retain their existing meaning.
Inside the new contextual adjective, **every explicit `case` is rejected** during
analysis, including `case:@item` and coincidentally matching literal cases.
There is no override syntax in 4A. This keeps authors from declaring competing
sources of truth as the chosen number or predicate polarity changes.

## One shared realization decision

`CountedConstruction` includes the optional adjective. All four source requests
in `RealizationPlan` depend on noun, quantity, predicate, adjective and the effective
dynamic predicate form. Incomplete bindings remain `Pending`; complete but missing
lexical realizations are `Unsupported`. Invalid bindings and catalogs remain
configuration errors. The same `InstructionLanguage.counted_construction` operation
serves MRV feasibility, preview, bound rendering and explanations. There is no
separate adjective case calculation in the renderer or another solver.

Polish rules live in `kotomi/languages/polish/constructions.py`. They resolve stored
`agreement_forms` through the existing attributive grammar catalog. No morphology
is generated at runtime. Required feminine, neuter-nominative and plural overrides
must exist; a missing override cannot silently fall back to masculine singular.
`describes` constraints remain active. Japanese i/na attributives, counters and
`ある`/`いる` forms use the existing target engine.

Plans contain syntax, not selected values. The existing cache is bounded to one
search. A fresh search observes changed Content and grammar. Numeric ranges remain
lazy and intersect the finite source numeral catalog; computing an adjective never
scans the range. No additional RNG calls are introduced.

Examples from the engine: `Jest jedna czerwona książka`, `Są trzy czerwone książki`,
`Było pięć czerwonych książek`, `Nie było trzech czerwonych książek`.
Japanese: `あかいほんがいっさつある。`, `あかいほんがいっさつあった。`.

## Indeclinable adjectives are outside stage 4A

Stage 4A does not provide a persistent declaration of indeclinability. A Polish
adjective such as `super`, represented only by identical common forms, is not
supported across the construction's agreement classes. `AgreementForms.normalized()`
removes overrides equal to the common value, including during XML persistence.
Writing duplicate overrides is therefore not a supported workaround.

Where this construction requires a feminine, neuter-nominative or plural override,
normalized common-only forms produce `Unsupported` after all dependencies are
bound, and generation reports `NoCompatibleChoices`. Incomplete assignments remain
`Pending`. Combinations already using the common masculine singular form may still
resolve; that is not full support for indeclinable adjectives. Semantics 1 keeps
its existing common-form behavior. A future extension needs an explicit declaration
that survives normalization and a save/load round trip. Inferring indeclinability
from missing overrides would also accept accidentally incomplete inflected words.

## Scope and release

Supported noun classes: feminine, neuter, masculine inanimate and masculine animate.
One source adjective realization and the same selection's Japanese attributive
form are supported. Multiple contexts, repeated source adjective realizations,
chains, masculine-personal nouns, pluralia tantum and collective numerals remain
outside 4A. Occurrence addressing and independently inflected repetitions belong
to 4B. The original pattern without an adjective remains available.

Kotomi **1.4.0**, Content revision **51**, minimum application **1.4**. Semantics
stays at 2; the application-version gate protects its expanded capabilities.
Merge the Data PR first, preserving its published commit, then the Kotomi PR that
pins that commit (or update the pin if the merge strategy changes it). Old apps
reject the new manifest before installation, including 1.3 which understood the
original semantics-2 context. The new app still accepts revision 50. Do not merge
automatically; review and green CI are required for both PRs.
