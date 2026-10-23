# Lesson 26 relative clauses

Content 65 extends the existing `relative_clauses` quiz. Deploy the paired Kotomi changes first: subject binding before object government, explicit neutral context precedence, and the `progressive`/`desiderative` form catalog entries. Content alone does not update the engine.

This is representative coverage of task families A–H, **not support for every sentence in the PDF**. The limitations below are part of the release scope.

## Patterns

All IDs start with `Przydawki / `. Separate variants represent different roles, Polish interrogatives or predicates. None stores an entire example as a fixed answer.

| ID suffix | Purpose |
|---|---|
| Osoba i dopełnienie | Identify an agent; one verb with both subject and object |
| Pytanie o wykonawcę | Ask `だれ`, preserving both arguments |
| Wybór przedmiotu | `どれ` with a neutral Polish choice phrase |
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
| Która z tych rzeczy to zegarek, który kupiłem? | わたしがかったとけいはどれですか。 |
| Gdzie znajduje się miejsce, w którym mieszkam? | わたしがすんでいるところはどこですか。 |
| Jaki był hotel, w którym nocowałem? | わたしがとまったホテルはどうでしたか。 |
| Kiedy przypada dzień, w którym mama idzie do Japonii? | おかあさんがにほんへいくひはいつですか。 |
| Kim jest osoba, która ma na sobie ubranie? | ふくをきているひとはだれですか。 |
| Kim jest osoba, z którą najbardziej chcę się spotkać? | わたしがいちばんあいたいひとはだれですか。 |
| Która z tych rzeczy to wino, które najbardziej lubię? | わたしがいちばんすきなワインはどれですか。 |
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


## Historical implementation measurements

Three alternating fresh-process runs: median load 112.5 → 152.0 ms; full validation 5.78 → 9.28 s; first preview of the old pattern 11.7 → 19.0 ms. These are local measurements with the larger vocabulary/pattern inventory, not a phone latency guarantee. All samples are in `relative_lesson26_performance.json` in the Content report directory. The complete new-quiz Cartesian count was not measured.

## Code-review follow-up

The review changes only ten of the 21 new templates. Existing pattern definitions, quiz membership/settings, all dictionaries, grammar XML and lessons are unchanged byte for byte against the initial PR head. `relative_lesson26_regressions.json` records hashes and 76 unchanged complete legacy PL/JA pairs (18 representative families, four forms, and four forced reflexive questions). This is a release comparison, not a copied unit fixture.

| Patterns | Review outcome |
|---|---|
| Osoba i dopełnienie; Osoba i dopełnienie 〜ている | Start with “To … jest …”; identity in nominative, head in instrumental, relative subject still nominative. |
| Wybór przedmiotu; Upodobanie; Pożądana rzecz | Start with “Która z tych rzeczy to …”; neutral choice wording works across head genders. Japanese still asks `どれ`. |
| Wskazanie przedmiotu | “Czy to klucz, którego zapomniałem?” replaces “Czy klucz, którego zapomniałem, to właśnie to?”. The meaning of `wasureru` is unchanged. |
| Dzień czynności | “To piątek jest dniem, w którym mama przychodzi do Polski.” Capitalization comes from the template. |
| Pragnienie spotkania | Fixed Polish predicate “chcę się spotkać”; Japanese verb explicitly restricted with existing `id:au`. The person and relative government remain dynamic. |
| Pragnienie podróży | Paired yes/no question: “Czy kraj, do którego najbardziej chcę pojechać, to Indie?” / `わたしがいちばんいきたいくにはインドですか。`. |
| Opis osoby | Paired yes/no question and existing `id:matsu` restriction: “Czy osoba, na którą czekałem, była urocza?” / `わたしがまったひとはかわいかったですか。`. Avoids arbitrary object verbs with person heads. |
| Miejsce czynności; Miejsce czynności 〜ている | Templates unchanged. Restored pre-PR clitic behavior gives “Gdzie znajduje się dom, w którym się urodziłem?”. |
| Pytanie o wykonawcę; Pytanie o wykonawcę 〜ている; Lokalizacja przedmiotu; Ocena miejsca; Miejsce zamieszkania; Pytanie o dzień; Ocena przedmiotu; Powód czynności; Liczba osób | Reviewed without template edits. Full pairs cover government, agreement and compatible forms. |

The sole engine edit in this follow-up deletes the two-line “any earlier relative” exception introduced by #226. No new renderer condition is added. Declarative “urodziłem się” and “chcę się spotkać” retain lexical order. Questions again use “w którym się urodziłem”; unrelated and later verb clauses retain their previous behavior. The meeting template supplies its fixed modal phrase, as existing preference templates already supply their fixed predicates. It does not rewrite verb translations. General modal-question clitic placement is not redesigned.

`tests/test_polish_clitic_regressions.py` adds 13 independent v2 full-pair cases for reflexives, negation, past/nonpast, relative/nonrelative questions and two verbs. The earlier meeting test keeps its expected output and now exercises the actual fixed template. The release audit checks 43 reviewed PL/JA pairs and seven rejected bindings; all checked new sentences start with capitals. The residence template has one currently supported lexical combination; it is not padded with fake vocabulary. Headless UI checks cover 21 individual selections plus all-new/mixed selections, settings persistence, rejection of unsupported polite relative forms and 43 simulator pairs. Native device interaction and APK builds remain untested.

### Review performance

See `relative_lesson26_review_performance.json`. Three fresh-process runs per scenario on one machine/interpreter; medians are local observations, not a device guarantee. First legacy preview is measured before validation, avoiding its caches.

| Operation | Initial PR | After review |
|---|---:|---:|
| Load Content | 71.2 ms | 74.6 ms |
| Full project validation | 3904 ms | 3957 ms |
| First legacy preview | 11.2 ms | 10.3 ms |
| First question, one new pattern | 20.0 ms | 19.4 ms |
| First question, all 21 new patterns | 42.7 ms | 35.3 ms |
| First question, full relative quiz | 35.0 ms | 32.9 ms |

Quiz rows use a preloaded project, an availability check, then first generation. After-review availability takes 19.8/44.3/41.8 ms respectively; engine construction itself is about 0.1 ms. Cold loading/validation is separate. With the same current engine, main Content validates in 3693 ms; expanded Content with the 21 new templates removed takes 3881 ms; all templates take 3957 ms. This controlled comparison attributes most additional validation work to the expanded Content graph and a smaller part to the new templates. It does not prove that the earlier, differently timed 5.78/9.28-second measurements were caused solely by those factors. Three samples do not establish a statistical performance guarantee.

`statistics()` visits complete previews through `iter_quiz_previews`; `has_possible_question()` stops at a renderable assignment. They have very different costs. Counting the small travel pattern completes (three possibilities). Counting the multi-argument identity pattern, all new patterns or the full quiz exceeds the 12-second process deadline both before and after review. No total is invented or extrapolated. This is a confirmed limitation of exhaustive statistics, not evidence of a new review regression. No counting/solver optimization or heavy CI performance test was added.

Reproduce optional probes with `tools/benchmark_relative_lesson26_review.py` and `tools/compare_relative_review.py`; pass separate checked-out before/current code and Content paths, plus main Content for the benchmark. Both read only the declared production project graph. Their bounded work is documented in the scripts; they are outside test discovery. Independent fixtures cannot certify release vocabulary, complete shipped sentences or real inventory latency.

### Remaining limitations

Negative forms of “Liczba osób” currently have no compatible binding and are filtered out; affirmative nonpast/past are checked. This was already present at the initial PR head. Existing lexical choices such as `iku` “idzie” and `kuru` “przychodzi” can sound literal with country destinations. They were not silently changed to other travel verbs. General modal placement, grammatical person, existential relatives and arbitrary three-argument compositions remain outside scope. These cosmetic changes do not claim exhaustive linguistic validation of every Cartesian combination.
