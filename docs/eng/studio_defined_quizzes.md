# Create sentence quizzes in Studio

Create a quiz, enter its name and description, then select sentence patterns or
composite patterns. Optionally add named vocabulary filters for the supported dictionary metadata.
Save the project after validation. The quiz appears in the launcher without a new
Python package. Lesson quizzes retain their existing behavior.

Players use the same settings and question presentation for all sentence
profiles. Values within one filter are alternatives; independent filters must all
match. Select at least one value. A profile with adjective types can offer i,
na, or both. A simple adjective composition can also offer 1-3 words per sentence.
Plain/polite transformations retain vocabulary and context while changing forms.

Counting patterns keep their shared optional number range. Pattern restrictions
still apply; fixed values and named numeric sets are preserved. A disjoint range
has no available question. Relative-clause profiles do not acquire extra lexical
controls unless their author explicitly selects filters.

Existing Verbs, Adjectives and Availability keep their stable profile IDs, selected
patterns and settings. Original settings files are preserved and migrate only when
the profile settings file does not yet exist. Executable packages are now only
`grammar` and `lessons`; deleting or renaming a profile never restores an old engine.

Use the current update order at the end of this guide. Quiz Update verifies the
replacement files before atomically retiring the three old first-party packages.
Old Content blocks retirement. Settings, progress and unrelated custom packages
are preserved. Restart after the package update. Downgrading Content below 72 or
reinstalling the retired catalog is unsupported; restore a complete compatible
installation backup instead. Lesson settings and generation do not change.

Renaming a profile changes its label while keeping its ID and settings. A session
ends normally when its available question pool is exhausted.

Modes, directions and forms follow the selected patterns. A mixed selection uses
only the patterns supporting the chosen mode; it does not require deselecting
other patterns. Fixed numeric patterns offer standard generation and their range,
without transformation controls. A form used only in the source prompt does not
make the Japanese answer transformable. Changing patterns or forms refreshes the
available controls. If a saved mode is no longer supported, settings explain the
change and select an available mode, preserving unrelated choices.

Next prepares questions in a worker and uses the existing loading indicator when
needed. Repeated Next requests are ignored while preparation is pending. Leaving
the quiz cancels pending preparation; a late result cannot update the departed
screen. Exhaustion search stays lazy and continues from its previous position.
There is no startup enumeration of all questions.

## Quick filters

Quick Filters are named on/off shortcuts to the existing advanced Word Filter. Choose **+ Add Quick Filter**, enter a name, check one or more vocabulary positions in **Applies to**, choose a property, and deselect unwanted values. A new filter is enabled by default and initially includes every available compatible value. Saving requires a name, a position and at least one value. Editing preserves the existing ID, defaults and selected values. There are no default-enabled or required-group switches in the dialog.

The compact resizable dialog keeps Save/Cancel in a fixed footer. Only values scroll. The scope menu explicitly shows selected positions and offers **All nouns**, **All verbs** or **All adjectives** when useful. **Show affected patterns** lists the complete scope. A single available position is selected automatically. Escape cancels; the active light/dark theme and keyboard navigation remain available.

Studio centrally recognizes alternative **type** selections: two or more filters with the same complete target scope and pairwise disjoint type values form a required group, provided at least one is enabled by default. A single new filter remains optional. Category, ending, feature and usage-role restrictions remain optional even when there are several. Existing explicit required groups are preserved while they have filters. If an edit/removal leaves such a group without an enabled default, its first remaining filter becomes the new-user default; saved learner states are unchanged. Older definitions whose defaults are all off remain optional unless already explicitly required. Runtime reads the stored group policy; it does not infer requirements from quiz IDs, dictionary size or changing vocabulary.

The player shows exactly one checkbox per named filter on Windows, Android and Mobile Preview, even for several positions. The adjective profile's i/na alternatives initially enable both types. Either alternative selects that type; disabling both shows a message naming the required choices. Empty optional groups add no restriction. Empty required groups are rejected before generation, feasibility, exact statistics and exhaustion.

Values and enabled alternatives for the **same target/property use OR**. Different selected positions, properties, advanced Word Filter and mandatory grammar/semantic constraints use **AND**. For **Trzy lubiane rzeczy**, select First noun, Second noun and Third noun with Category = Food. All three positions must then use Food vocabulary. Selecting only First noun restricts only that position. Disabling the single learner checkbox removes this additional restriction.

Targets are stable conceptual identities from analyzed roles. Friendly names distinguish Main verb, Embedded verb, Subject noun, Object noun and numbered nouns. Repeated captions include construction/position context. Equivalent aliases are deduplicated while preserving a saved identity. Purely fixed grammatical elements are not offered for new filters; existing valid selections remain editable. A target absent from a composite alternative adds no condition there. A present target with no compatible vocabulary makes that alternative unavailable. Ambiguous bindings or overlapping different aliases for the same property are rejected with an explanation. No filter binds by its displayed caption.

Properties come from supported Word/Entity metadata and dictionary declarations: Type, Ending, Category, Features and Usage role, where applicable. Only properties with selectable values common to all selected positions are offered. Values are discovered from whole relevant dictionaries, independently of current feasibility; a known value can still produce no compatible questions. Noun entities offer Category, matching their existing runtime contract. Category does not duplicate the compatibility fallback from `Word.categories` to features. Unsupported attributes, forms and identifiers are not offered.

Ending is the dictionary attribute, not the suffix of a conjugated answer. `ending="ru"` can match both godan and ichidan verbs; an advanced `verb.type=godan` further restricts it. Missing optional attributes do not match a selected value. New dictionary values appear automatically and use the existing parser's case normalization. The existing matcher and solver perform all generation and counting; no new DSL or filtering engine is introduced.

### XML definition

```xml
<quick_filters required="adjective.type">
  <quick_filter id="i_adjectives" label="i-adjectives"
                target="adjective" property="type" values="i_adjective"
                default_enabled="true" />
  <quick_filter id="na_adjectives" label="na-adjectives"
                target="adjective" property="type" values="na_adjective"
                default_enabled="true" />
</quick_filters>
```

A multi-position filter uses the optional `targets` list instead of `target`:

```xml
<quick_filters>
  <quick_filter id="food_items" label="Food items"
                targets="first second third" property="category" values="food"
                default_enabled="true" />
</quick_filters>
```

Exactly one of `target` or `targets` is required. Targets are unique stable roles; all share one property and value set. Existing single-target XML is unchanged. `required` is an optional list of `target.property` keys; omitted means optional groups. Each required key must exist and have an enabled default. IDs are unique within the quiz. Names and values are nonempty. `default_enabled` accepts true/false and still defaults to false when omitted in older XML; Studio explicitly writes true for new filters. A quiz cannot mix new and legacy definitions.

### Saved settings and older definitions

Settings store `quick_filter_states` by stable ID. Existing states override defaults; new IDs use defaults; removed IDs produce the existing correction notice. Other settings and advanced expressions are preserved. Multi-target scope changes retain one state and one checkbox. Cached preparation still applies the current profile expression to questions and exact counts. Temporarily unavailable source grammar does not erase declared filters or states.

If a Content update makes an empty selection invalid, the saved choices remain intact. Start opens editable settings with a localized notice; the learner must select an alternative. Loading never overwrites the original file.

The legacy `filters` / `vocabulary_filters` adapter remains. Unrelated Studio edits preserve that XML. Editing a legacy shortcut converts the definition explicitly, with a notice; the central type-alternative policy then applies. Lossless old selections become boolean states. Other restrictions and old allowed-value bounds remain advanced Word Filter conditions. In particular, a legacy restriction for only one position does not silently enable a new multi-position filter: that shortcut stays off and the original single-position condition is retained. An old empty selection blocks starting until reviewed and saved. Repeated load/save does not duplicate restrictions.

### Theme and update order

Install Application **1.1.15+**, then catalog **1.1.17** (Grammar **1.1.16**), before authoring multi-position filters. Content **74** remains unchanged and declares the existing adjective required group. Grammar still accepts Content 72 through its compatibility adapter. Lessons remains **1.1.9**. No translation XML or unrelated dictionary data is changed.
