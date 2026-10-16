# Noun categories and verb roles (C3)

Add an ordinary noun by choosing its narrowest correct category. Verbs accepting
that category or an ancestor then accept the noun without changes to `verbs.xml`.
This is not a promise that every verb accepts every future noun: meaning and the
source translation still determine whether a category is appropriate.

## Contract and architecture

A noun has one `category`. The existing catalog already supports `parent`, e.g.
`closable_container → container → thing → purchasable → concrete` and
`education_facility → building → place → concrete`. C3 extends this mechanism,
not the DSL, model, matcher, forms or argument binding. The plural `categories`
attribute currently belongs to adverbs and is not supported for nouns.

`accepts="container"` accepts the category and its descendants. `nouns="room"`
adds an exact ID. Together they mean OR, never AND. An exact-ID-only role does not
also accept its role default. An empty role uses its default; `accepts="*"` accepts all.

```xml
<word id="new_chest" category="closable_container" ... />
<role ref="object" accepts="closable_container" government="direct_object" />
<role ref="target" accepts="container" nouns="room" />
```

The new chest works without editing either verb. The second role accepts containers
and additionally a room. An open bowl classified as `container` does not gain closing
or opening behavior. Required noun fields and forms are omitted in this example.

## New categories

| Category | Parent | Meaning and boundary |
|---|---|---|
| `container` | `thing` | A container, including open ones; not an arbitrary place. |
| `closable_container` | `container` | A container with a closure, e.g. a bag/chest; not an open bowl. |
| `clothing` | `thing` | Garments, including future trousers; not bags, jewelry or arbitrary accessories. |
| `money` | `availability_reason` | Money, not plans, time or arbitrary financial obligations. |
| `duration` | `availability_reason` | Time as duration, not a date, weekday or plan. |
| `music` | `media` | Music and musical pieces, not a voice or physical instruments. |
| `building` | `place` | Physical buildings/facilities, not rooms, parks or beaches. |
| `education_facility` | `building` | Buildings for regular education, e.g. schools, not every cultural venue. |
| `sports_facility` | `building` | Sports buildings, e.g. gymnasiums, not every recreation area. |

Each category describes a noun property, not one verb's arbitrary list. Eight
categories have current members; the broader `container` distinguishes open from
closable containers. Currently singleton clothing/money/duration have reusable
meanings independent of IDs. The inherited `availability_reason` parent is a legacy
compatibility scope, not an ideal ontology; retaining it protects availability rules.
Calendar dates are not moved into that branch.

## Authoring and Studio

Select one noun category. The verb editor exposes the same new categories in
`accepts`. Independent Studio service tests cover insertion, saving, reloading,
unchanged verb XML after adding a noun, government and OR exceptions. Projects
with explicit standalone grammar retain their own catalog, without an automatic overwrite.

Before adding a category inspect all potential members, ancestors, current roles
and source translations. Reuse an existing category if appropriate. Trousers need
`haku`, not `kiru`; `kiru` therefore retains its exact generic `clothes` exception,
while `nugu` and `sentakusuru` use clothing. Do not classify a physical instrument
as music merely to allow practice: an instrument and a musical piece are different things.

## Exceptions and architectural boundary

Keep exact IDs for lexical readings or restricted contexts, such as saving `inochi`
outside person/animal. Document the reason. Do not broaden to all abstract things,
places or media just to eliminate the last lists.

Five retained lists (`hajimeru`, `owaru`, `suru`, `tsuzukeru`, `ukeru`) remain a
scalability limitation pending sense/translation decisions. They are explicitly
marked `deferred_sense_review`, not presented as a finished category solution.
The Polish gloss of `keikosuru` also needs a separate sense review; C3 preserves it.

A single tree cannot describe independent facets such as object, material and
purpose without artificial combinations. If needed, the simplest recommendation
is to retain base `category` and add optional semantic memberships on the noun.
Matching would use their union and ancestors, keeping OR and avoiding per-verb
mapping tables. This is a separate decision requiring coordinated validation,
serialization, indexes, editor and completion changes. C3 neither implements it
nor simulates multiple facets through an artificial tree.

## Patterns, quizzes and deployment

Patterns and agreement maps are unchanged. Existing ancestor matches are retained.
The audit checks every verb role, including roles without nouns, and all adjective
pairs. Integration compares relative outputs in four forms, automatic argument
binding, government, questions, counts and availability of other patterns. Engine
unit tests use independent fixtures only.

## Approved decisions and review audit

`noun_role_decisions_c3.json` owns the approved expectations: `target` stores the
complete exact role attributes, while `added` and `removed` list the noun IDs of
approved changed combinations. There is no second match matrix. Other roles must
retain their baseline attributes and every match. The audit independently compares
these decisions, XML and observations from the existing `role_matches`. Regenerating
the report does not approve changes. Duplicate JSON keys fail; decision status must
agree with retained exceptions. Government, role/form order and unrelated XML remain
protected. The exact nine additions and three removals are unchanged. Existing category
definitions are also compared against the baseline catalog, so loading both projects
with the current engine cannot hide the same category drift on both sides.

## Content 63 compatibility and publication

Deploying the application before Content alone does not protect older installations.
`content_header.check_content_manifest` checks the header and XML schema but ignores
the historical `min_kotomi_version="1.8.0"`. The application independently uses
version `1.1.2`; simply enforcing that comparison would reject compatible Content 62.

Desktop and Mobile share `QuizUpdater` with `expected_channel="content"` and the
selected data directory. Application manifests use `version`, Content uses `revision`,
and quizzes have their own API contract. Application checks compare file hashes;
Content retains revision equality and downgrade-confirmation behavior. These channels
and their numbering remain independent. Native Android routes application
updates to its separate APK release; Content never installs the application.

The smallest effective gate uses existing rejection of unknown formats: Content
revision 63 and later require update manifest `format: 2`. Existing format-1 clients
reject it in `_parse_manifest`, before downloading any payload. The new client accepts
formats 1 and 2 only on the Content channel; application updates retain format 1.
The builder and release validator require format 2 from revision 63. The revision
metadata file and XML schemas keep their existing formats. The baseline has another existing defense: snapshot validation rejects unknown
categories without changing installed data even with a format-1 manifest.
Format 2 moves rejection ahead of downloads and protects format-1-only clients
without relying on the presence or details of their semantic snapshot validation.
This is an enforced
boundary in already installed clients, not an ignored additional version field. Restart after
updating the application so the running process uses the new updater.

After downloading and verifying hashes, the updater constructs a complete isolated
snapshot, loads the project and lessons, and validates categories and references
before starting the existing backup transaction. Download/validation failures never
write live files. Installation failures use the existing rollback, with the revision
marker written last. Existing filesystem-error handling retains recovery backups if
rollback itself fails. Files outside the manifest are not overwritten; existing
removal rules cover only registered retired dictionaries, not unrelated user files.

| Application | Content 62, format 1 | Content 63, format 2 |
|---|---|---|
| Baseline `9d6d662` | Installs | Rejects before payload download |
| C3 after review | Installs | Installs after snapshot validation |

This matrix ran the actual updater from both checkouts with independent fixtures,
not production vocabulary. New application tests cover an unknown category, corrupt
downloads and byte equality of all unrelated files. Existing rollback, downgrade
confirmation and cancellation tests remain in place.

**Status: Content 63 can be published through format 2 after both PRs pass CI and the C3 acceptance gates.**
Never distribute it through format 1, including mirrors or an older builder.
Distributing updated Kotomi enables installation; older clients safely retain their
Content and can still upgrade the application through its independent channel.
Manual XML copying outside the updater is not a compatibility guarantee.
No publication or merge was performed. Publication remains blocked if format 1 is retained.

## Performance correction without semantic changes

Review measurements exceeded the 10% limit for warm first-question generation.
Profiling identified repeated temporary sets in category intersections. `role_matches`
now uses `accepted.isdisjoint(...)` instead of copying an existing set and building
an intersection set. The matcher, OR, full ancestor evaluation and cycle checks are
unchanged; no cache or new model was added. The report retains pre-correction samples.

## Small proposed C4 scope

One tree fits building/facility and container/closable-container relationships, but
cannot express independent functional properties. `doa` and `mado` are not containers.
Characterization fixtures show that as `thing` they do not match the four
`closable_container` roles. This is an intentional current boundary, not a failing
test. Likewise, `clothing` includes shirts and trousers without specifying how they
are worn; the fixture retains the exact-ID scope of `kiru`.

Existing OR in `accepts` could add a suitable category, such as architectural closures,
to the four verbs once. Later nouns in that category would require no verb changes.
This is the smallest option without model or DSL changes if actual new vocabulary
fits such disjoint groups. C3 does not introduce it based on two examples. Classifying
doors as containers would be incorrect.

If actual vocabulary demonstrates repeated overlapping groups, C4 should first define
a small set of functional properties (opening, wearing method) and verb scopes.
Then evaluate optional additional noun memberships, keeping pattern and `accepts`
syntax, with an empty default preserving existing data. This requires coordinated
model, loader/writer, validation, indexes, Studio, IntelliSense and distribution-gate
changes. Existing `semantic_categories` are restricted to adverbs and cannot simply
be assigned to nouns today. C4 should exclude solver rewrites, multiple-parent trees
and a wholesale vocabulary migration.


## Test coverage after review

| Scope | Existing Kotomi tests and additions |
|---|---|
| Inheritance, OR, future nouns | `test_noun_role_categories.py`, with no duplicate matcher |
| Government, explicit/implicit agree, four forms | `test_noun_role_categories.py`, `test_verb_form_agreement.py`, `test_subject_relative_catalog_boundary.py` |
| Subject/object relatives | `test_relative_realization.py`, `test_relative_explicit_case.py`, opt-in C3 integration |
| XML and Studio | `test_xml_fragment_save.py`, `test_studio_change_aware_save.py`; extended C3 test checks every unrelated file after noun and verb saves |
| IntelliSense | `test_intellisense_capability_matrix.py`, existing pattern editor and relative tests |
| Updates and rollback | `test_content_c3_compatibility.py`, existing `test_data_downgrade.py`, `test_update_progress.py` |
| C3 decisions | Data: `test_noun_role_audit.py`, explicit fixture mutations and optional real-engine contracts |


[Content audit](../validation/noun_role_audit_c3.md).
