# Dictionaries

This directory owns Kotomi's lexical dictionaries.

Files:

- `verbs.xml`
- `nouns.xml`
- `adjectives.xml`
- `connectors.xml`
- `copulas.xml`
- `interrogatives.xml`
- `numbers.xml`
- `counters.xml`

All dictionary files use project Schema 2 and are referenced by `../quiz_project.xml`. Dictionary IDs are part of the data contract and can be referenced by lessons, grammar, patterns, and quiz code, so renaming an ID requires updating every reference and the validation tests.

Keep word data here. Grammar rules, sentence patterns, and lesson organization belong in their corresponding directories.

The `interrogatives` dictionary stores Japanese question words as form-less lexical entries. `asks_for` describes the information requested (for example `place`, `reason`, or `method`); grammar patterns still own particles and sentence structure.

Japanese homographs with different source-language syntax remain separate
lexical entries. In particular, `aru_possessive` owns Polish `mieć` and
direct-object government, while `aru_existential` owns `być / istnieć`, the
`existential` feature, and nominative/genitive existential government. Both
entries realize Japanese `ある`; patterns never switch an entry's meaning.

The `connectors` dictionary stores form-less discourse connectors. Connector
entries own only their lexical Japanese value and Polish meaning. Sentence
patterns own clause order, punctuation, register and example context, so
near-synonyms such as `だけど` and `でも` are not selected interchangeably in
an unsuitable random sentence.

Polish adjective agreement is optional lexical data. Nouns may store
`<agreement class="..." />`, while adjectives store ready-to-use values in
`<polish_forms>`. The latter contains zero or more `<common>` entries and
zero or more `<override classes="...">` entries. Each entry uses a
space-separated `cases` attribute and one `value`, so a form shared by several
cases is stored only once. There may be several common and override entries.
An override contains only values that differ from `common`; identical class
and case groupings are combined. The writer groups values in canonical case
and class order and removes redundant overrides on save.

For required Polish agreement the runtime looks up a specific override and then
the common form. It never invents morphology or falls back to base translation
when a required realization is missing. Optional enrichment may be absent on a
valid word, but such a word cannot satisfy a pattern requiring that realization.


## Noun relation profiles

A noun may reference a reusable source-language relation profile:

```xml
<relations language="pl" profile="place_w_do" />
```

The profile itself is owned by the selected Kotomi grammar; the dictionary does
not duplicate prepositions or case rules. This lets multiple nouns share the
same realization while still allowing lexical differences such as
`w szkole / do szkoły`, `na plaży / na plażę`, or
`we wnętrzu / do wnętrza`.

Relation profiles are authoring data. Runtime does not infer a profile from the
noun category or Polish spelling.


## Schema 2 counting dictionaries

- `numbers.xml` stores semantic integer values and standalone Japanese and Polish forms.
- `counters.xml` stores lexical values, exact per-output realizations keyed by numeric or symbolic quantity, and references to grammar-owned composition profiles.
- `grammar/counting.xml` is the single source of class-to-counter compatibility and class defaults.
- noun `<counting>` metadata stores counting classes, an optional exceptional preferred-counter override, and explicit Polish profile-by-case forms.
- the `how_many` interrogative exposes `quantity_symbol="how_many"`.

Exact counter realization fields are authoritative and override composition. Numeric gaps may use the composition profile defined by Kotomi Japanese grammar; symbolic quantities remain exact-only.
The `one` profile falls back to ordinary noun cases and must not duplicate them.
Studio builds its counted-form table from the profiles supplied by the active Kotomi language and
all cases supported by the project model. Authoring-time autofill may propose
only conservative forms supported by the noun translation, agreement class,
ordinary cases and quantity mappings. The proposal is saved as editable XML;
unknown forms stay empty and runtime never performs Polish morphology.

## Lesson Szymon / pierwsza

Słówka nieodmienne i gotowe zwroty z lekcji otrzymały oddzielne słowniki z `schema="generic"`: `demonstratives`, `time_expressions`, `adverbs`, `expressions`. Nie udajemy, że przysłówki czy zaimki wskazujące są rzeczownikami, a odmianę polską demonstratywów zapisujemy pomocniczo we właściwościach `cases` lub `polish_forms`.

Forma `住んでいます` nie jest odrębnym słowem: `verbs/sumu` zawiera słownikowe `住む` i `te_form=住んで`. Konstrukcje z `～ています` pozostają po stronie patternów. Nieodmienne określenia czasu nie dostają sztucznego liczenia, a dni tygodnia oraz `聞き取り` mają polskie przypadki bez counterów. Policzalne hasła otrzymują istniejące klasy counterów i komplet przypadków w profilach few/many.

Pełny audyt: `lessons/szymon_pierwsza_audit.pl.md`.
