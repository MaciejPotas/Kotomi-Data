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

Upgrade in order: Application 1.1.11 or later, Content revision 72 or later, then
approve Quiz Update (catalog 1.1.13, Grammar 1.1.12). Quiz Update verifies the
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
