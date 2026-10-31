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

Existing Verbs, Adjectives and Availability identities migrate to profiles when
both repository updates are installed. Their saved selections and relevant
settings migrate once. Original settings and legacy package entrypoints remain
available for rollback with older Content. Install the application update before
the companion Content update. No lesson settings need migration.

Content revision 72 suppresses the legacy menu entries even if a migrated profile
is deleted. Renaming changes the label while keeping the stable ID and settings.
A session ends cleanly when its available question pool is exhausted.

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
