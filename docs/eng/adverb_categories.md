# Semantic categories for adverbs

Available from Kotomi 1.8.0. The Content manifest requires this version so an older
editor cannot silently discard category metadata. Schema 2 is unchanged.

## Data and meaning

Nouns keep their single, hierarchical `category`: its ancestors participate in
verb government, adjective compatibility and counting. Adverbs instead carry
zero or more flat semantic memberships. There is no inheritance between them.
They use the existing `DictionaryConfig.categories`, word-selection slots and
compatibility solver. Lesson tags are not semantic restrictions.

The only persisted membership is the space-separated `categories` word attribute.
The dictionary owns its catalog, which may include values not yet used by words:

```xml
<dictionary schema_version="2" id="adverbs" schema="adverb"
            instruction_language_id="pl">
  <categories>
    <category id="frequency" />
    <category id="time" />
    <category id="manner" />
    <category id="degree" />
    <category id="focus" />
  </categories>
  <words>
    <word id="mainichi" kana="まいにち" kanji="毎日"
          translation="codziennie" categories="frequency" />
    <word id="saikin" kana="さいきん" kanji="最近"
          translation="ostatnio" categories="time" />
  </words>
</dictionary>
```

| Category | Meaning | Example reading |
| --- | --- | --- |
| `frequency` | How often | まいにち, ときどき, よく |
| `time` | When | さいきん, きのう, きょう |
| `manner` | How an action is performed | ゆっくり |
| `degree` | Intensity | とても |
| `focus` | Emphasis or focus | とくに |

These are Content declarations, not a GUI enum. Custom catalog IDs match
`[a-z][a-z0-9_]*`. Empty/malformed IDs, duplicate declarations, duplicate
memberships, and undeclared memberships are rejected. Catalog entries contain
only `id`. The singular `category` attribute on an adverb is rejected to avoid two
sources of truth. A dictionary without a catalog and words without `categories`
remain valid, but unclassified words cannot satisfy `category:...`.

Multiple memberships, for example `categories="frequency time"`, are appropriate
only when the stored lexical meaning genuinely supports both uses. They are not
an OR of different translations. The shipped `yoku` means “często”, so it is only
`frequency`; adding `manner` for the separate meaning “well” would generate the
wrong Polish translation. No category is inferred from translation. Relative time
such as yesterday is not frequency. `time_expressions` remains retired.

## Pattern language and solver

`category:<id>` is a selection constraint. Its values are the active adverb
dictionary's catalog. `categories:` is not a placeholder property.

```text
{adverb[category:frequency].translation}
{adverb[category:frequency]}

{adverb@when[category:time].translation}
{adverb@when[category:time]}

{adverb@frequency[category:frequency].translation} {verb[form].translation}.
{adverb@frequency[category:frequency]} {verb[form]}。

{adverb[id:saikin, category:time]}
```

An alias shares one word across both languages and all occurrences. Constraints
on the alias are intersected, including constraints written only on the other
side. If one occurrence asks for frequency and another for time, the selected
word must carry both memberships. `id` and `category` are also an intersection.

Invalid examples and their outcomes:

| Example | Outcome |
| --- | --- |
| `{adverb[category:missing]}` | Analysis error when `missing` is not declared |
| `{adverb[id:saikin, category:frequency]}` | No candidates with the example data |
| `{adverb[category:time, category:frequency]}` | Parser rejects repeated property |
| `{adverb[categories:time]}` | Parser rejects unknown property |
| `{adverb[occurrence:left]}` | Parser rejects unsupported grammar context |
| `{adverb[category:time, form:dictionary]}` | Parser rejects inflection on a formless word |

Enumeration returns an empty set for contradictory or unsatisfied constraints;
preview generation raises `NoCompatibleChoices`. Bound rendering also checks
`id` and the combined category constraints, and rejects stale/incompatible
bindings with `ProjectError`. Words are selected once, without another solver or
special handling for particular IDs.

Explicit `occurrence:...` is not supported by adverb tokens: the parser rejects
it and IntelliSense does not offer it. That property addresses grammatical
contexts in other supported constructions. Repeated adverb tokens share their
selection through the `@name` alias; compiled token occurrences do not require
an explicit `occurrence` property.

Categories do not enforce tense compatibility, verb valency, negation, natural
word order or the suitability of every adverb/verb pairing. Use an appropriate
pattern and other existing constraints. No Polish grammar rules or adverb
inflection were added.

## IntelliSense and Studio

All text surfaces using `placeholder_completions` share the capability contract:
pattern questions and answers, composite authoring and the existing inline
assistant. `{adverb[` offers `id` and `category`, but not `occurrence`, forms,
roles or features. `{adverb[category:` reads the active dictionary catalog,
including unused custom categories. Typing a prefix filters the list. Used
properties are not offered again; both `id, category` and `category, id` work.
Completions insert parser-compatible text. The placeholder insertion dialog also
switches its category choices between nouns and adverbs.

Open an adverb in the existing word editor, expand its advanced fields and use
**Semantic categories**. Select each membership from the list. Remove selected
memberships with Delete; an empty list clears the classification. Save and reload
preserve the catalog and every membership. This reuses `ValuePicker`, not a
separate adverb editor. New catalog values are declared in dictionary XML; the
word editor assigns the values already declared by the project.

## Validation and tests

`tests/data/adverb_categories/adverbs.xml` has four independent words, one with
multiple memberships and one legacy entry, plus an unused custom category.
Engine tests cover parsing, selection, alias intersections, bilingual output,
exact IDs, empty domains, unknown values, XML and complete project round trips,
completion insertion, bound rendering, local grammar contexts, real editor class
construction with a recording Tk backend, and unchanged noun behavior.

The separate Kotomi-Data validator checks catalogs and references for every
manifest dictionary without asserting lesson membership, word count, order or
specific IDs. Its mutation tests build a tiny temporary XML fixture. No new test
needs production Content permission. Run the production validator separately to
check the actual released files.

## Verified generation example

With production Content, the generic frequency pattern above, form
`polite_nonpast`, and the verb choice `taberu` (no adverb ID), enumeration produced:

| Source output | Target output |
| --- | --- |
| `codziennie jem.` | `まいにち たべます。` |
| `czasami jem.` | `ときどき たべます。` |
| `często jem.` | `よく たべます。` |

These are exact outputs, including their lower-case source initial. A plain
adverb output does not introduce a new sentence-capitalization rule. Identical
pairs can recur across existing context options when the pattern omits context.
