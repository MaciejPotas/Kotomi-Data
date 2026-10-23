# Lesson 26 relative clauses

Content 65 extends the existing `relative_clauses` quiz. Deploy the paired Kotomi changes first: subject binding before object government, explicit neutral context precedence, and the `progressive`/`desiderative` form catalog entries. Content alone does not update the engine.

This is representative coverage of task families A–H, **not support for every sentence in the PDF**. The limitations below are part of the release scope.

## Patterns

All IDs start with `Przydawki / `. Separate variants represent different roles, Polish interrogatives or predicates. None stores an entire example as a fixed answer.

| ID suffix | Purpose |
|---|---|
| Osoba i dopełnienie | Identify an agent; one verb with both subject and object |
| Pytanie o wykonawcę | Ask `だれ`, preserving both arguments |
| Wybór przedmiotu | `どれ` with Polish noun gender |
| Wskazanie przedmiotu | Identification with `これですか` |
| Lokalizacja przedmiotu | Ask `どこ` about an object's location |
| Miejsce czynności | A building where an activity occurs |
| Ocena miejsca | `どうでしたか` with agreed Polish past copula |
| Miejsce zamieszkania | `すんでいるところ`, explicit Polish “w którym” |
| Dzień czynności | Identify a day by a person's movement and a weekday |
| Pytanie o dzień | `いつ`, independent subject and destination |
| Pragnienie spotkania | `〜たい`, Polish “z kim” government |
| Pragnienie podróży | The country I want to visit, with a selected country |
| Upodobanie | Separate adjectival `いちばんすきな` construction |
| Pożądana rzecz | Separate adjectival `いちばんほしい` construction |
| Ocena przedmiotu | Object relative with `どうでしたか` |
| Opis osoby | Object relative with an adjective predicate |
| Powód czynności | `りゆうはなんですか`, Polish “dla którego” |
| Liczba osób | `なんにん` using existing interrogative/counter realization |
| Osoba i dopełnienie 〜ている | Identify an agent performing an activity or in a state |
| Pytanie o wykonawcę 〜ている | Ask about that agent |
| Miejsce czynności 〜ている | Location of an ongoing intransitive activity |

Simple forms are `dictionary`, `plain_negative`, `past_plain`, `past_negative_plain`. The `〜ている` and `〜たい` variants use a fixed **affirmative nonpast** form, not new quiz tense axes. `progressive` stores complete `よんでいる` or `きている` with its lexical meaning, including “ma na sobie”. `desiderative` stores `あいたい` or `いきたい`. Missing forms/agreement exclude a binding.

The existing `Czynność w toku 〜ている` composition is unchanged. Its `translation:current` preserves Polish tense, but combining `te_form` and `いる` does not automatically supply the result-state meaning of `きている` or insert the auxiliary before an arbitrary relative head. Two additional lexical forms reuse existing form selection without a new solver, placeholder or DSL parameter.

## Complete checked examples

| Polish | Japanese |
|---|---|
| Kim jest osoba, która zrobiła ciasto? | ケーキをつくったひとはだれですか。 |
| Kim jest osoba, która nie czytała książki? | ほんをよまなかったひとはだれですか。 |
| Który to zegarek, który kupiłem? | わたしがかったとけいはどれですか。 |
| Gdzie znajduje się miejsce, w którym mieszkam? | わたしがすんでいるところはどこですか。 |
| Jaki był hotel, w którym nocowałem? | わたしがとまったホテルはどうでしたか。 |
| Kiedy przypada dzień, w którym mama idzie do Japonii? | おかあさんがにほんへいくひはいつですか。 |
| Kim jest osoba, która ma na sobie ubranie? | ふくをきているひとはだれですか。 |
| Kim jest osoba, z którą najbardziej chcę się spotkać? | わたしがいちばんあいたいひとはだれですか。 |
| Które to wino, które najbardziej lubię? | わたしがいちばんすきなワインはどれですか。 |
| Ile osób przyszło do szkoły? | がっこうへきたひとはなんにんですか。 |

All pairs, rejected bindings and timings are in `docs/validation/relative_lesson26.json`. Count timings use locked selections, not the entire vocabulary product. Existing meanings are preserved: for example, `miru` still uses the existing Polish “oglądałem”.

## Scope boundaries

- There is no grammatical-person conjugation. First-person patterns explicitly contain `わたしが`; nominal subjects use `agree`. A first-person gloss never pretends to mean “you bought”. Literal `あなた`, plural parents and arbitrary possessors are not covered.
- There is no arbitrary composition of three or more arguments/modifiers, such as a watch you bought in Japan, keys forgotten yesterday at work or meeting a husband for the first time. Two arguments of one verb are verified.
- `じゅぎょうがないひ`, `ここにあったざっし` and `日曜日だけ` are unsupported. Existential negation requires its own government; ordinary B3 agreement is not substituted. Future/negative `〜たい` and past/negative `〜ている` variants are not exposed.
- The day question uses “Kiedy przypada dzień, w którym…?”, without a separate “Którego dnia…?” variant. Identification answers use `です`, without a negative final copula.
- Activity locations are limited to buildings and `intransitive` verbs, preventing incomplete phrases such as “the hotel where I am wearing”. Noun relations supply `w/na` and the relative has explicit locative case. Residence uses generic `ところ`, not every place-category head.
- Relative heads remain singular. Counting uses existing quantity forms and an impersonal predicate, without a plural `relative` implementation.
- Not all proper names, party, examination, picture or the idiom `せがたかい` were added. Personal description is checked using existing grammatical `かわいい`. Vocabulary omissions are not engine limitations.

## Quiz and validation

Windows and Mobile share the quiz definition. All or selected patterns can be practiced. Old IDs/settings remain valid; manually saved selections are not silently expanded. Enable plain output for the four simple forms. Fixed `progressive/desiderative` forms follow existing fixed-construction selection behavior.

New answers contain `{context[pool:none].kana}`. Its single empty context prevents invisible “today/yesterday” options multiplying identical text. Hints do not receive invisible time expressions. Counting and preview still share the engine.

From Kotomi-Data:

```sh
python tools/validate_repository.py
python -m unittest discover -s tests -v
python tools/validate_relative_lesson26.py --kotomi ../Kotomi --output docs/validation/relative_lesson26.json
python tools/validate_relative_lesson26_ui.py --kotomi ../Kotomi --output docs/validation/relative_lesson26_ui.json
```

The last two commands are explicit release audits, outside unit-test discovery. They read actual published data because independent fixtures cannot certify its sentences. Cost: one project load/validation, a bounded reference list and one question per selected configuration, without complete enumeration. Engine tests use an independent v1 fixture. UI checks run real callbacks with fake controls/font; they do not operate native Windows/Android devices or build an APK.


## Local measurements

Three alternating fresh-process runs: median load 112.5 → 152.0 ms; full validation 5.78 → 9.28 s; first preview of the old pattern 11.7 → 19.0 ms. These are local measurements with the larger vocabulary/pattern inventory, not a phone latency guarantee. All samples are in `relative_lesson26_performance.json` in the Content report directory. The complete new-quiz Cartesian count was not measured.
