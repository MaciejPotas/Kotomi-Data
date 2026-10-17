# Relative clauses in Content

The current engine includes B3 and universal target C3.2. This document preserves a historical stage; check current references and completeness with the [audit tools](developer_tools.md).

Content revision 59 adds one `Zdania przydawkowe` pattern in category
`przydawki` in `patterns/sentence_maps.xml`. The `relative_clauses` definition
in `patterns/sentence_quizzes.xml` exposes a **Zdania przydawkowe** quiz
on Windows and Mobile through the existing grammar quiz package.
It requires an application containing Kotomi PR #208 and Polish grammar.
Downloading Content alone cannot add DSL support to an older application.

```xml
<sentence_pattern id="Zdania przydawkowe" category="przydawki"
                  forms="dictionary plain_negative past_plain past_negative_plain">
  <question>To jest {noun@item[case:nominative]}, {relative[agree:@item, government:@action].phrase} {verb@action[role:object, form].translation}.</question>
  <answer>これはわたしが{verb@action[role:object, form]}{noun@item}です。</answer>
</sentence_pattern>
```

`.phrase` preserves government prepositions: `nad którym zastanawiam się`,
`na który czekam`, `w który wierzę`. Without a preposition it behaves like
`.translation`: `którą czytam`, `której nie czytam`. The existing `object` role
binds the noun and verb; no additional argument declarations are needed.

| Form | Question for `book` and `yomu` | Answer |
|---|---|---|
| `dictionary` | To jest książka, którą czytam. | これはわたしがよむほんです。 |
| `plain_negative` | To jest książka, której nie czytam. | これはわたしがよまないほんです。 |
| `past_plain` | To jest książka, którą czytałem. | これはわたしがよんだほんです。 |
| `past_negative_plain` | To jest książka, której nie czytałem. | これはわたしがよまなかったほんです。 |

Select category `przydawki` in Studio. Preview and Simulator use the same
form restrictions as the quiz. Enable plain output in the quiz; polite verb
forms inside the relative clause are excluded. The final `です` stays fixed.
Use existing filters to practice selected vocabulary, for example
`verb.id=yomu;noun.id=book`. Without filters the existing dictionary categories
and explicit compatibility lists apply. They do not guarantee naturalness of
every semantic combination. Revision 59 corrects two demonstrated problems:
`sukuu` accepts people, animals and explicit `inochi` (life); `ireru` no longer
accepts all `abstract` nouns but explicitly retains `okane` (money).
This rejects rescuing a revision exercise and inserting time in every pattern.
The narrower `sukuu` scope also excludes abstract objects such as work and plans.
No exceptions or curated sentence dictionary were added to the engine.

The first pattern remains limited to singular object relatives. `okane` has a plural agreement
class and is correctly rejected; `harau`, restricted to `okane`, therefore
has no results here. Do not invent forms to bypass this limitation.

Engine statistics distinguish vocabulary combinations, generated realizations
including context, and unique text. This pattern does not display context,
so different existing context options can produce identical text.
`generated_sentences` must not be read as the number of distinct visible sentences.

See the [Kotomi documentation](https://github.com/MaciejPotas/Kotomi/blob/main/docs/eng/relative_clauses.md)
for the complete DSL and `forms` contract. Publication advances only the Content
revision and rebuilds its manifest. Executable Quiz packages and the application
version remain unchanged.


## B3: subject-relative clauses

Content revision 60 adds a second pattern to the same quiz. It requires B1/B2
and the existential-catalog boundary fix described below. B4 will pin this
revision in the application; this PR does not change that gitlink or deployment.

```xml
<sentence_pattern id="Zdania przydawkowe podmiotowe" category="przydawki"
                  forms="dictionary plain_negative past_plain past_negative_plain">
  <question>To jest {noun@item[case:nominative]}, {relative[agree:@item, case:nominative].translation} {verb@action[role:subject, form, agree:@item].translation}.</question>
  <answer>これは{verb@action[role:subject, form]}{noun@item}です。</answer>
</sentence_pattern>
```

Object relatives describe the object of an action: “the book that I read”.
Subject relatives describe its actor or the object undergoing a change:
“the person who works”, “the box that opened”. The second pattern has no
`わたしが`. `relative[case:nominative]` selects the nominative; the first
pattern's `relative[government:@action]` obtains its case and preposition from
government. `role:subject` checks compatibility, without adding `government`.
Polish inflection rules remain in the
[language documentation](https://github.com/MaciejPotas/Kotomi/blob/main/kotomi/languages/polish/docs/polish_grammar.md#b2-uzgodnienie-form-czasownika).

| Verb | Subjects | Stored translation classes |
|---|---|---|
| `hataraku` | `friend mother sister teacher roujin hito programmer madogiwazoku` | masculine_personal, feminine |
| `neru` | the same people plus `inu tori` | masculine_personal, masculine_animate, feminine |
| `aku` | existing `bag box` | feminine, neuter |

This deliberately small set covers human work, human/animal sleep and opening
objects. All previous roles, Japanese forms and ordinary `Form.translation`
values remain unchanged. The new `hataraku` and `neru` roles use `nouns="..."`.
The broad `person` category also contains `hitori` (“one person”), which cannot
simply follow the verb as an ordinary noun. Its category and other verbs' roles
remain unchanged. `aku` keeps its existing `bag box` list. Unused classes such as
masculine_inanimate are not filled artificially. Isolated B2 tests still cover
all five supported singular classes.

Example stored form:

```xml
<form ref="past_plain" kana="はたらいた" translation="pracowałem" kanji="働いた">
  <agreement_translations>
    <translation class="masculine_personal" value="pracował" />
    <translation class="feminine" value="pracowała" />
  </agreement_translations>
</form>
```

`agree:@item` reads the selected form and noun class deterministically. Missing
assignments exclude the realization, without first-person fallback, automatic
conjugation or random gender selection. `hito` remains “osoba”, class feminine.
Plural subject relatives remain outside B3.

| Form | Polish question | Japanese answer |
|---|---|---|
| dictionary | To jest osoba, która pracuje. | これははたらくひとです。 |
| plain_negative | To jest osoba, która nie pracuje. | これははたらかないひとです。 |
| past_plain | To jest osoba, która pracowała. | これははたらいたひとです。 |
| past_negative_plain | To jest osoba, która nie pracowała. | これははたらかなかったひとです。 |

Other examples: “To jest pies, który spał.” (`これはねたいぬです。`),
“To jest torba, która nie otworzyła się.” (`これはあかなかったかばんです。`),
and “To jest pudełko, które otworzyło się.” (`これはあいたはこです。`).
These are plain forms; the pattern does not add the ongoing-action meaning
of `ている`.

### Studio and quiz

In Studio select category `przydawki` and the new pattern. Its allowed-form
selection contains the four listed forms; the editor still exposes other catalog
entries, which are not part of this pattern. Select a verb form and open
“Translations by gender”. Empty rows mean an unsupported class. See the
[B2 editor/save guide](https://github.com/MaciejPotas/Kotomi/blob/main/docs/eng/verb_form_agreement.md).

The `relative_clauses` quiz references both patterns. On Windows and Mobile,
select the object pattern, the subject pattern, or both. Enable plain style and
the desired tenses/polarities. Hint contains only the chosen verb and noun,
without hidden context or the completed answer. The shared interface and quiz
package need no changes.

### Validation and integration prerequisite

Unpatched B2 also admits `iru` and `aru_existential` through its existential
catalog, producing e.g. “osoba, która nie ma”. This is a boundary error between
ordinary subject agreement and existential construction templates. [Kotomi #213](https://github.com/MaciejPotas/Kotomi/pull/213) rejects noun-subject agreement without government for that catalog.
It preserves governed constructions, quantity agreement and legacy counting.
Do not remove those verbs' features or add artificial Content translations.
**Integrate the Kotomi fix before deploying Content 60.**

Rejected pairs include `hataraku + book/inu/hitori`, `neru + car/hitori`,
`aku + hito/book`, and implicit `iru/aru_existential`. Nouns and existing object
relatives remain unchanged.

Result: 20 word pairs (8 + 10 + 2), 20 unique questions/answers per form,
80 unique text pairs overall. The 100 realizations per form, 400 overall,
include five invisible context choices. They are not 400 different sentences.

[Validation report and all 80 pairs](../validation/subject_relatives_b3.json),
[raw timings](../validation/subject_relatives_b3_performance.json), and
[release-audit instructions](../../tools/README.md). Production Content is read
only by the explicit release audit, outside unit tests. Automated tests use
independent fixtures. Shared paths and headless controls were exercised; no
physical Windows/Android GUI was manually operated.

The additional [headless UI smoke](../validation/subject_relatives_b3_ui.json)
checks two Mobile controller lifecycles, three pattern selections, 48 questions
and 12 examples through the actual simulator callback without reloading the project.
