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

Deploy the Kotomi category-catalog PR before Content 63. Old applications do not
recognize these categories. Merging the application PR does not update user
installations. The historical `min_kotomi_version` is not raised: the current
Content header does not enforce it as a version gate, and application versioning
is independent. Coordinate Content publication with application distribution.
Neither PR enables automatic merge.

[Content audit](../validation/noun_role_audit_c3.md).
