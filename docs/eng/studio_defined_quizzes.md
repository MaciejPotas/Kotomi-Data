# Create sentence quizzes in Studio

Create a quiz, enter its name and description, then select sentence patterns or
composite patterns. Optionally expose a word type, category or feature filter.
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

Upgrade in order: Application 1.1.12 or later, Content revision 72 or later, then
approve Quiz Update (catalog 1.1.14, Grammar 1.1.13). Quiz Update verifies the
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

Quick Filters are named on/off shortcuts to the existing advanced Word Filter. Choose **+ Add Quick Filter**, enter a name, choose a vocabulary role and property, check one or more values, and optionally enable the shortcut by default. Edit and Remove act on compact rows. The editor has no per-pattern selection, allowed-values column or per-value defaults.

New shortcuts are optional and off by default. Select **Require at least one option for this target and property** to make their shared group required. This applies to all shortcuts with the same target/property, and requires at least one default-enabled shortcut. No quiz ID or dictionary size determines requiredness. Rows identify required versus optional groups.

The player shows one checkbox per shortcut, using the same settings model on Windows and Mobile. The name is the learner-facing label. Existing advanced Word Filter editing remains available. The adjective profile defines two XML shortcuts, i-adjectives and na-adjectives, both initially on. Both on selects both types; either one on selects that type; both off shows a validation message because this group requires at least one selection.

Enabled shortcuts for the **same target and property use OR**, including multiple values within a shortcut. Different groups and the advanced Word Filter use **AND**. Empty optional groups add no restriction. Empty required groups are rejected before generation, feasibility, statistics and exhaustion. The existing parser and compatibility solver handle generation, feasibility, exact counts and exhaustion. Mandatory grammar/semantic restrictions always apply. No second filtering engine or grammar DSL extension is introduced.

Targets are quiz-wide conceptual roles obtained from analyzed aliases: main verb, embedded verb, noun, embedded noun, adjective or another unambiguous role. The editor does not expose generated pattern IDs or encoded exact-slot selectors. A target absent from an alternative contributes no restriction there. A present target with no compatible candidates makes that alternative unavailable. If all alternatives are unavailable, the normal no-compatible-questions message is shown; the shortcut stays enabled. Overlapping different aliases for one property are rejected; use the same target for OR alternatives.

Target choices use stable identities and unique friendly captions. A compact scrollable scope field lists affected constructions, including fixed-word elements when the engine filters them. Repeated role labels include construction context and vocabulary position. Equivalent aliases keep the existing selected identity without duplicate choices. Editing properties/values preserves the selected target and draft values; ambiguous bindings are rejected.

Values come from the relevant whole dictionaries and their declared metadata, not the candidates of a single pattern. A known value can currently have no usable questions. The dialog explicitly warns about this possibility. Category is offered for real category metadata; the compatibility fallback from `Word.categories` to features does not create a duplicate Category control. Advanced filtering keeps its previous semantics. Numeric ranges and adjective chains remain independent existing capabilities.

### XML definition

```xml
<quick_filters required="adjective.type">
  <quick_filter id="i_adjectives" label="i-adjectives"
                target="adjective" property="type" values="i_adjective"
                default_enabled="true" />
  <quick_filter id="na_adjectives" label="na-adjectives"
                target="adjective" property="type" values="na_adjective"
                default_enabled="true" />
  <quick_filter id="people_animals_food" label="People, animals and food"
                target="noun" property="category" values="person animal food"
                default_enabled="false" />
</quick_filters>
```

`required` is an optional space-separated list of `target.property` keys. Omitted means all groups are optional. In the example, adjective type requires a choice while noun category remains optional. Each required key must exist and have an enabled default.

IDs are unique within a quiz and remain unchanged when editing a name, expression or default. Names and values are nonempty. One shortcut has one target/property and one or more values. `default_enabled` is `true` or `false` (omitted means false). These elements live inside the existing quiz, alongside `patterns`. A quiz cannot mix new and legacy filter definitions.

### Saved settings and older definitions

New settings store `quick_filter_states` by stable ID. Existing states override defaults; new IDs use defaults; removed IDs are discarded with the existing correction notice. Other settings and advanced expressions are preserved. Filters use the existing vocabulary-dependent cache identity and do not clear unrelated caches. Source grammar becoming temporarily unavailable does not erase declared shortcuts or their states.

A Content update can make a previously optional group required. Saved empty choices are preserved, not reset to defaults. Start opens settings with a localized notice naming the options; the learner must select at least one before saving or generating questions. Unrelated settings and advanced expressions remain unchanged.

Old `filters` / `vocabulary_filters` XML remains readable through a compatibility adapter. It creates one shortcut per legacy value. An unrelated Studio edit preserves that XML unchanged. Editing/removing its shortcut explicitly converts the definition to optional Quick Filters; Studio displays a conversion notice. The old allowed/default columns are gone.

Old adjective i/na selections and other exactly representable selections become checkbox states. If an old restriction cannot be represented exactly, it is preserved as an advanced Word Filter condition and shortcuts for that group are disabled to avoid adding an accidental intersection. Old explicit author allowed-value bounds are also retained as advanced conditions in saved settings. They can be reviewed and changed in the existing advanced editor. An old empty selection was invalid, so it is not silently treated as unrestricted: starting is blocked until the learner reviews and saves settings. Loading does not overwrite the original file. Repeated load/save does not append duplicate restrictions.

### Theme and update order

The quiz editor and shortcut dialog use the active Studio theme for native text/list controls, scrolling containers and ttk labels/inputs. Theme changes refresh their colors without rebuilding the quiz model. Keyboard navigation, Escape and scrolling remain available.

Install Application **1.1.14+**, then approve catalog **1.1.16** (Grammar **1.1.15**), then Content **74**. This order ensures both the runtime and Grammar package understand required groups before loading their definitions. The package still accepts Content 72 through its legacy adapter. Content 74 marks the adjective type group as required in XML. Lessons remains **1.1.9**. No translation XML or unrelated learning dictionary is changed.
