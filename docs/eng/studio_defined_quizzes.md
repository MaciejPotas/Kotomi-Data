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

## Vocabulary filters

The Studio editor lists only configured filters. Choose **+ Add filter**, then:

1. Select a vocabulary target. The dialog lists the affected patterns so that main, embedded and object roles can be distinguished.
2. Select word type, semantic category or grammar features. Properties without values are not offered.
3. Select the values learners may use.
4. Select a nonempty default subset and save. Edit and Remove change this definition, not the learner's current practice settings.

In the player, every configured filter uses the shared Windows/Mobile settings controls. Small groups use checkboxes. For adjective type, both i-adjective and na-adjective are selected initially in existing profiles. A valid saved choice takes precedence. Neither checked is an error, never an implicit request for all words.

Values within one group use **OR**. Separate groups and any advanced text filters use **AND**. Grammar constraints, semantic compatibility and form compatibility always remain mandatory. Repeated or overlapping controls for the same target/property are rejected rather than creating a hidden extra intersection.

Effective composite alternatives supply the targets and labels. An optional filter applies only to alternatives containing its target; an unrelated alternative remains usable. Mandatory construction restrictions remain in the pattern and cannot be disabled by the learner. The dialog names the affected alternatives. An ambiguous target, removed reference or unavailable value must be repaired before saving. Numeric ranges and adjective chains remain separate capability-based settings.

Settings belong to each profile ID. After a configuration change, retained values remain selected, unsupported values are removed, and defaults are used only when a previously nonempty selection has lost all its values. Removed filters do not reset other settings. A meaningful correction appears in the existing settings notice. An explicitly empty selection remains invalid.

### Definition format

Existing `filters="adjective.type"` still exposes all available values and defaults to all. Studio can additionally store:

```xml
<vocabulary_filters>
  <filter key="adjective.type"
          allowed="i_adjective na_adjective"
          defaults="i_adjective na_adjective" />
</vocabulary_filters>
```

The key belongs to the quiz's `filters` list; the loader also accepts a key declared directly in `vocabulary_filters`. Allowed values and defaults are nonempty and defaults must be allowed. Normal authoring uses the dialog, not XML or DSL. Use Application 1.1.12+ and Grammar 1.1.13+ for this extended contract. Content revision 72 and the existing profile definitions remain unchanged in this release.

If source grammar is temporarily unavailable, its filter definitions and saved selections are retained. Target checks resume when that grammar becomes available.
