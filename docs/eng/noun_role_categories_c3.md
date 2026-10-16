# Noun categories and verb roles (C3)

> Historical C3/C3.1 report. Content 64 uses format 3; see [C3.2](target_government_c32.md) for current compatibility and category changes.

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
protected. The original nine additions and three removals are retained; C3.1 adds the explicit target corrections below. Existing category
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

## C3.1: `target` and relationship direction

`target` is the verb argument marked here with **に**, not a synonym for recipient.
`object` takes **を**; `destination` expresses movement direction with **へ**.
Japanese に/へ can sometimes alternate, but the DSL roles remain distinct.
The `target` identifier and compatibility with earlier Content are preserved.

A `<usage>` declaration does not insert an argument into a sentence. A pattern
selects it with `verb[role:target]` and writes に in its answer. Catalog `particle`
is authoring metadata, not automatic text insertion. None of the current 92
production patterns selects `target`; `reaction_target` is a different role.
No production pattern is added by C3.1.

`accepts` matches categories and ancestors; exact `nouns` IDs are alternatives (OR).
`government` specifies the Polish case/preposition **for that verb role**, not a
noun category or Japanese particle. `target` does not imply dative. Production
`target` declarations currently have no `government`. A pattern using `[government]`
needs a suitable frame; without it there are no compatible possibilities. Add the
frames and appropriate Polish form translations before publishing such a pattern;
never implicitly reuse the `object` frame.

### All 21 declarations

These are Content's teaching-sense decisions, not claims that other arguments
are impossible in metaphor, fiction or special contexts. Every role is compatible
with に. Categories do not validate whole-situation plausibility or relationships
between two selected nouns.

| Verb | Meaning of `target` and restriction review |
|---|---|
| `ayamaru` | Addressee of an apology; retain `person animal`: apologizing to a pet is possible. |
| `hairu` | Place entered; retain `place`. Entry need not mean joining an institution. |
| `ireru` | Place of insertion; retain `container` OR exact `room`. This does not check object/container dimensions. |
| `kariru` | Person borrowed **from**; `person animal → person`. An ordinary animal is not a lender. |
| `kayou` | Facility attended regularly; retain `education_facility sports_facility`. |
| `kotaeru` | Person answered or message replied to; `abstract → person` OR `nouns="email letter"`. Remove weekdays, duration, money, etc.; do not accept every book/text. A future “question” noun needs an explicit scope extension. |
| `nareru` | Object/person/situation one gets used to; retain intentionally broad `*`. |
| `naru` | Result of becoming/change; retain `*` for roles, states and transformations. Arbitrary subject/result pairs are not guaranteed: a future pattern must constrain context rather than produce everyday sentences about any transformation. |
| `okoru` | Person/animal one gets angry with; retain `person animal`. |
| `oshieru` | Learner; retain `person animal`, including teaching commands to a dog. The subject taught and learner still need a coherent context. |
| `sawaru` | Touched object; retain `concrete`, not just people/recipients. |
| `teishutsusuru` | Person/institution receiving a submission; retain exact `teacher school`. |
| `tomaru` | Stopping point; retain `place`. Current 止まる is not staying overnight 泊まる. |
| `usowotsuku` | Interlocutor being lied to; `person animal → person` for the ordinary verbal communication sense. Deceiving an animal through behavior does not justify the whole category. |
| `ageru_give` | Gift recipient; retain `person animal`, e.g. feeding a dog. The separate `ageru` with 上げる means “raise”. |
| `kaesu` | Recipient of a returned object; retain `person animal`, e.g. returning a toy to a dog. |
| `kasu` | Person lent **to**; `person animal → person`, temporary transfer with an expectation of return, not simply giving something to an animal. |
| `kureru` | Recipient on the speaker's side; retain `person`, but the category does not encode viewpoint. A future pattern must identify the speaker/in-group. |
| `morau` | Person received **from**; `person animal → person` for ordinary interpersonal giving. An animal donor needs a separate context. |
| `watasu` | Recipient of a handover; retain `person`. |
| `sumu` | Residence; retain `place`. Habitability depends on context, not just hierarchy. |

### Two arguments and translations

The existing DSL supports both roles of one slot. Repeated declarations for the
same alias collect roles: use `verb@action[role:target, form].translation` in the
question and `{noun@partner}に{noun@item}を{verb@action[role:object, form]}` in the
answer. Nouns can use `category:person` and `category:text`; automatic binding uses
the actual `role_matches`. If role domains overlap, `government:@action` alone
cannot choose **which role** the noun has: it identifies a verb, not a role.
Disambiguate with existing domain filters; if that is impossible, the future
pattern needs a separate task. C3.1 adds no workaround or noun-role selector DSL.

- せんせいにほんをかりる — “Pożyczam książkę **od nauczyciela**” (borrow from the teacher): target needs `od` + genitive.
- ともだちにほんをかす — “Pożyczam książkę **przyjacielowi**” (lend to a friend): target needs dative.
- ともだちにほんをあげる — “Daję książkę **przyjacielowi**” (give to a friend): `ageru_give`, dative.
- がっこうにはいる — “Wchodzę **do szkoły**” (enter school): target, `do` + genitive.
- がっこうにかよう — “Uczęszczam **do szkoły**” (attend school): target, `do` + genitive.

Independent fixtures exercise the first three sentences, affirmative/negative
forms, counting, binding, OR, separate argument frames, particle and XML roundtrip.
They do not claim production translations are ready for a new universal pattern:
`kariru` already says “pożyczam od kogoś”, `kasu` “pożyczam komuś”, `ageru_give`
“daję komuś”. Appending an argument mechanically would duplicate “od kogoś/komuś”;
a suitable translation variant is needed. `kureru` additionally needs viewpoint
and subject person; `kotaeru` needs different Polish government for a person
(“komuś”) and a message (“na list”). This is a small separate authoring task before
publishing patterns, not a reason to rewrite the solver.

### Facilities versus `building`

Schools/universities are `education_facility`; a gym/training facility is
`sports_facility`. A mere training room does not thereby become a building and
needs its own lexical decision. Correctly classified future facilities work with
`kayou` without editing the verb. Banks, office buildings and hospitals do not
become education/sports facilities just because they are buildings. Japanese
病院に通う is valid (“regularly visit hospital”), as can be regular visits/commuting
to a bank/office. The current Polish gloss “uczęszczać” does not automatically
cover these readings. Retain the two subtypes and narrow scope; `building` would
be an unjustified expansion. No categories or properties are added.

### C3.1 acceptance scope and evidence

Five `target` roles change; the other 248 roles retain the approved C3 outcomes.
Relative to the C3 baseline, the complete matrix now has **19 additions and 35
removals** (previously 9/3), and **15** roles retain explicit `nouns` (previously 14).
The new `kotaeru` exception is deliberate, not hidden behind a broad category.
The existing decision JSON holds five `scope: C3.1_target` entries, exact `before`
and `target` attributes, reasons and approved added/removed sets. Missing approval,
XML drift or changed observations still fail. Regeneration never approves decisions.
Content remains unpublished revision 63 with update manifest format **2**.

Language references (accessed 2026-10-16; Content scope policy is our decision):
[TUFS: に and transfer direction](https://www.coelang.tufs.ac.jp/mt/ja/gmod/courses/c01/lesson08/step3/explanation/028.html),
[TUFS: あげる/くれる/もらう, including animals](https://www.coelang.tufs.ac.jp/mt/ja/gmod/courses/c01/lesson22/step1/explanation/085.html),
[Daijisen: 通う](https://kotobank.jp/word/通う-467110),
[Daijisen: 答える](https://kotobank.jp/word/答える-502121),
[Daijisen: 嘘](https://kotobank.jp/word/嘘-440021).
