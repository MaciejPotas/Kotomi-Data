# Dictionaries, context references and lexical tokens

Kotomi 1.7 reads one canonical Content project. A dictionary owns each lexical
entry; lessons and context pools refer to it. `kinou` belongs to `adverbs`.
`ashita` remains in `nouns` and can be referenced by any context. A word may be
used by any number of lessons and pools without copying its translation or kana.
The retired `time_expressions` dictionary is not a separate source of words.

## Dictionary ID, schema and placeholder kind

| Dictionary ID | Schema | Token | Selection | Realization |
|---|---|---|---|---|
| `adverbs` | `adverb` | `adverb` | `id`, alias | direct outputs |
| `demonstratives` | `demonstrative` | `demonstrative` | `id`, alias | direct outputs; `agree`, `case` for source translation |
| `expressions` | `expression` | `expression` | `id`, alias | direct outputs |

All three support `occurrence` and the outputs `id`, `translation`, `kana`,
`kanji`, `romaji`. A bare token returns kana. They do not support `form`,
`polarity`, `role`, `feature` or `category` selectors. An explicit output requesting an empty optional field fails with a diagnostic;
it does not invent text. An alias shares the selection, while `occurrence` identifies
one local grammatical use of that selection.

The manifest registers the file and schema. The file declares the same ID and
schema. Authoring capabilities come from `dictionary_config_for_language()`;
Content cannot supply an `<editor>` schema. Merely creating a custom dictionary
with a schema does not create a new public token: `PLACEHOLDER_CONTRACTS` maps
public kinds to specific dictionary IDs.

Add these registrations inside the existing `<dictionaries>` element:

```xml
<dictionary id="adverbs" file="dictionaries/adverbs.xml" schema="adverb" />
<dictionary id="demonstratives" file="dictionaries/demonstratives.xml" schema="demonstrative" />
<dictionary id="expressions" file="dictionaries/expressions.xml" schema="expression" />
```

Older projects may omit all three dictionaries. A pattern using an absent
dictionary cannot generate a sentence. Existing inline context options remain
supported. Referenced context Content declares `min_kotomi_version="1.7"` so
older applications cannot silently render an empty context.

## Complete dictionary examples

These are independent small examples, not an inventory to enforce in tests.
Add words in the Desktop dictionary editor by selecting the existing dictionary,
entering an ID, translation and kana, and optionally kanji/romaji. The three new
types also appear in New Dictionary. Demonstrative source agreement is editable
under Polish grammar. Japanese forms are not conjugated for these types.

`dictionaries/adverbs.xml`:

```xml
<dictionary schema_version="2" id="adverbs" schema="adverb"
            target_language_id="ja" instruction_language_id="pl" label="Adverbs">
  <words>
    <word id="kinou" translation="wczoraj" kana="きのう" kanji="昨日" romaji="kinou" />
  </words>
</dictionary>
```

`dictionaries/expressions.xml`:

```xml
<dictionary schema_version="2" id="expressions" schema="expression"
            target_language_id="ja" instruction_language_id="pl" label="Expressions">
  <words>
    <word id="shikata_ga_nai" translation="nic nie da się zrobić"
          kana="しかたがない" kanji="仕方がない" romaji="shikata ga nai" />
  </words>
</dictionary>
```

`dictionaries/demonstratives.xml`:

```xml
<dictionary schema_version="2" id="demonstratives" schema="demonstrative"
            target_language_id="ja" instruction_language_id="pl" label="Demonstratives">
  <words>
    <word id="kono" translation="ten" kana="この" kanji="この" romaji="kono">
      <polish_forms>
        <common cases="nominative accusative vocative" value="ten" />
        <common cases="genitive" value="tego" />
        <common cases="dative" value="temu" />
        <common cases="instrumental locative" value="tym" />
        <override classes="masculine_personal masculine_animate" cases="accusative" value="tego" />
        <override classes="feminine" cases="nominative vocative" value="ta" />
        <override classes="feminine" cases="genitive dative locative" value="tej" />
        <override classes="feminine" cases="accusative" value="tę" />
        <override classes="feminine" cases="instrumental" value="tą" />
        <override classes="neuter" cases="nominative accusative vocative" value="to" />
        <override classes="plural_non_masculine_personal" cases="nominative accusative vocative" value="te" />
        <override classes="plural_non_masculine_personal" cases="genitive locative" value="tych" />
        <override classes="plural_non_masculine_personal" cases="dative" value="tym" />
        <override classes="plural_non_masculine_personal" cases="instrumental" value="tymi" />
      </polish_forms>
    </word>
  </words>
</dictionary>
```

Polish runtime selects stored forms, first a class override, then a common case
value. It does not synthesize morphology. Redundant overrides are normalized
away on save. Standalone `kore/sore/are` use common case values; `kono/sono/ano`
also need gender overrides. The example covers the currently supported classes;
it does not claim support for a separate masculine-personal plural class.

| Token using the examples | Lexical result |
|---|---|
| `{adverb[id:kinou].translation}` | `wczoraj` |
| `{adverb[id:kinou].kana}` | `きのう` |
| `{adverb@time[id:kinou].kanji}` | `昨日` |
| `{expression[id:shikata_ga_nai]}` | `しかたがない` |
| `{expression[id:shikata_ga_nai].translation}` | `nic nie da się zrobić` |
| `{demonstrative[id:kono]}` | `この` |
| `{demonstrative[id:kono].translation}` | `ten` |
| `{demonstrative[id:kono, agree:@item, case:@item].translation}` with feminine `noun@item` in locative | `tej` |

A complete agreement example using a noun `school` with feminine agreement and
stored locative `szkole` is:

```text
{demonstrative[id:kono, agree:@item, case:@item].translation} {noun@item[id:school, case:locative]}
```

It realizes `tej szkole`. Source sentence formatting may capitalize the first
word to `Tej`; the table describes lexical values. `case` requires `agree` on a
demonstrative, and agreement requires `.translation`. For example,
`{demonstrative[id:kono, case:locative].translation}` and
`{adverb[id:kinou, form:dictionary]}` are rejected. `agree:@item` can inherit the
effective noun case, so an explicit `case:@item` is only needed when expressing
that dependency explicitly or selecting a different case.

## Lesson references

```xml
<lesson_catalog schema_version="4" instruction_language_id="pl">
  <lessons>
    <lesson id="example_a" group="Examples" main="Time" name="First">
      <word><dictionary_ref dictionary="adverbs" word="kinou" /></word>
    </lesson>
    <lesson id="example_b" group="Examples" main="Review" name="Second">
      <word><dictionary_ref dictionary="adverbs" word="kinou" /></word>
    </lesson>
  </lessons>
</lesson_catalog>
```

Saving a dictionary-backed lesson word writes its reference, not a copied lexical
entry. Lesson loading resolves references from the current project; reload a
catalog after dictionary edits to refresh its materialized lesson values. This
is different from context resolution, which reads the current Word on each use.
Missing words are validation errors. There is no special group name or minimum
number of words. Tests must not pin the membership or size of a real lesson.

## Context references and suffixes

```xml
<contexts schema_version="2" instruction_language_id="pl">
  <context id="none" label="Neutral"><option id="neutral" translation="" kana="" /></context>
  <context id="past" label="Past">
    <option id="yesterday" dictionary="adverbs" word="kinou" weight="2"
            translation_suffix=" " kana_suffix="、" />
  </context>
  <context id="future" label="Future">
    <option id="tomorrow" dictionary="nouns" word="ashita" weight="1"
            translation_suffix=" " kana_suffix="、" />
  </context>
</contexts>
```

The final option requires an existing `nouns/ashita`. `ContextOption.resolved()`
reads the current lexical translation through the active instruction language
and appends `translation_suffix`; it appends `kana_suffix` to lexical kana.
Suffixes are literal separators, preserve intentional spaces and are not
placeholder templates. A word can serve several pools. Editing it changes all
subsequent context resolutions without rewriting the context definitions.

`{context[pool:past].translation}` yields `wczoraj `, and
`{context[pool:past].kana}` yields `きのう、`. Weighted selection chooses the same
option for the paired source and target outputs. In Studio's Contexts tab enter
the dictionary and word IDs, leave inline texts empty, and enter separators in
After translation / After kana. Inline neutral or custom options remain valid.

Both `dictionary` and `word` must be supplied together. A reference cannot be
mixed with inline `translation` or `kana`; suffixes require a reference. The
loader, project validator and context writer reject dangling or mixed references.
Full project save validates all model data before its first write, without
running sentence renderability enumeration. Errors leave every project file
unchanged. Each successful file replacement is atomic; a multi-file save does
not promise rollback after an unrelated disk I/O failure.

## Retired dictionaries

The project manifest, and only that manifest, stores retirement:

```xml
<retired_dictionaries>
  <dictionary id="time_expressions" />
</retired_dictionaries>
```

Remove the old dictionary registration and migrate every lesson/context reference
before publishing the retirement. `DictionaryService` will not rediscover an
unregistered file declaring that ID after an update. It leaves user files on
disk. Explicit registration takes precedence and reactivates the dictionary.
Project save/reload preserves retirement. `counting.xml` contains only number
sets and counter bindings, never `retired_dictionaries`.

## Adding a kind and testing it

A new public kind needs a `PLACEHOLDER_CONTRACTS` entry, a dictionary authoring
schema where capabilities differ, and compatible parser, analysis, generation,
XML and Studio support. IntelliSense uses contracts to offer kinds, IDs, aliases,
selectors and outputs. It suppresses used properties and unsupported combinations;
for demonstratives it offers `case` after `agree` and only `.translation` for
agreement. Check actual completion edits with the parser, including negative
examples and missing dictionary/ID errors. Do not add per-word branches.

Use `tests/data/engine` and the bounded `data/tests/fixtures/lexical` supplement.
Neither may be copied or generated from the production database during tests.
Mutate temporary copies to test deletion, shared references and invalid input.
Engine tests exercise arbitrary lessons, round trips, agreement and rendering.
Release checks separately validate every shipped reference, form and manifest.

Every production exception in `tests/conftest.py` names one test and supplies
`invariant`, `fixture_gap`, `file_scope`, `growth_cost`. The guard enforces the
file scope. A marker or an empty/generic rationale grants no access. Metadata
checks use a separate registry and cannot read lexical XML. Removing a specific
lesson assertion does not justify removing general Content quality checks.

Dictionary editing blocks deletion or ID changes when a context or a Schema 4
lesson references the word. A malformed lesson file prevents this safety check
and blocks the destructive edit until it can be read. Editing lexical values
under the same ID remains allowed and updates subsequent context resolutions.
