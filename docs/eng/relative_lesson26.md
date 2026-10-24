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


## Exact-count performance follow-up

The earlier review measurements above are historical. Profiling 5,000 previews of the large identity pattern took 11.61 s under cProfile: about 6.27 s in solver enumeration and 4.80 s in complete preview rendering (nested costs overlap). Grammar statistics enumerated the full product of noun choices and rendered both languages for every binding. `has_possible_question()` needs only a first witness. Increasing the deadline would not remove this work.

`iter_counted_possibilities()` fixes word selections and factors only noun domains proven independent by the existing realization plan and transitive alias dependencies. Each dimension is enumerated with the original solver and renderer while other choices are fixed. Coupled noun choices remain enumerated; each representative carries an exact multiplicity and the complete factored entity IDs for the eligible-word metric. Contexts still count separately, even when text is identical. Quiz totals are additive by pattern/form, as before. There is no sentence cache, result cache or approximate count to invalidate.

The canonical per-form solver/rendering loop is extracted into `_iter_form_possibilities()` and reused, avoiding repeated global form discovery for already validated forms. `SharedQuizEngine.iter_counted_previews()` exposes this path to `GrammarQuizEngine.statistics()` on both hosts. Older hosts and post-render word filters keep the original path. Counters/quantity constructions, cross-noun dependencies, unbound dynamic forms, single-noun patterns and word products above 256 retain exact enumeration where factoring is inapplicable. The 256 guard chooses the algorithm, never limits the answer. No grammar/DSL/selection rule or lexical/pattern XML changes.

`count_possibilities()` in the Simulator still enumerates: its distinct question/answer/vocabulary and connection metrics cannot be replaced by binding multiplication. Expensive fallbacks therefore remain possible. Windows and Mobile already run explicit statistics through their calculation/progress facilities; opening or starting a quiz continues to use the early-exit feasibility path. Selection/settings changes invoke a fresh count.

| Scenario | Exact count before = after | Before | After |
|---|---:|---:|---:|
| Small travel pattern | 3 | 4.9 ms | 13.6 ms |
| Large identity pattern | 71,936 | 50.584 s | 7.644 s |
| All 21 new patterns | 142,591 | 98.521 s | 43.582 s |
| Complete relative quiz | 182,651 | 89.495 s | 34.842 s |
| Existing “Trzy lubiane rzeczy” | 729,000 | 158.210 s | 68.5 ms |
| Existing simple verb pattern | 2,480 | 233.8 ms | 258.8 ms |
| Existing subject-relative pattern (three-sample median) | 6,480 | 1.125 s | 1.280 s |
| Existing full Grammar quiz | not obtained | >180 s | >180 s |

Long before/after totals are separate diagnostic runs, not passes of the 12-second gate. The identity and old three-noun patterns now complete within that gate; all-new/full-relative selections still do not. The old full Grammar quiz remains an unresolved enumeration bottleneck, with no partial total published. This is a general optimization, demonstrated on a pre-existing non-relative pattern, not a lesson-ID exception.

Initial cold medians: load 200.7 → 169.1 ms; validation 7.362 → 7.969 s. These paths were not optimized. Startup measurements were variable, so nine further fresh-process AB/BA pairs were recorded: first-question medians one/all-new/full-relative **30.3 → 34.3 / 53.5 → 63.0 / 59.6 → 65.0 ms**. The ranges overlap (for full-relative: 50.8–82.5 / 58.1–79.8 ms), but the higher medians are reported, not hidden as a speedup or proof of zero latency regression. First-generation code is unchanged; seeded complete questions and RNG state match. The slower old-pattern single samples prompted a same-process, alternating five-pair comparison: canonical 1.386 s, weighted fallback 1.400 s, identical 6,480 counts, about 1% dispatch overhead. All raw measurements remain in the existing JSON report; these local observations are not a device latency guarantee.

Local verification: 1,179 application tests plus 356 subtests passed; 16 native Tk tests skipped without a display. Data validation and question-pattern validation passed; 133 Data tests ran, seven skipped. The release comparison preserved 76 legacy full pairs; every XML file remains unchanged against the pre-optimization heads. Full Windows CI is linked from the PR; OS DPI/physical-device validation remains manual.

Run from the Content repository using the existing `tools/benchmark_relative_lesson26_review.py --optimization --before-kotomi BEFORE --kotomi AFTER --data CONTENT --diagnostic-timeout 180 --output docs/validation/relative_lesson26_review_performance.json`. All paths must name separate matching checkouts. The optional 180-second diagnostic is separate from the unchanged 12-second process deadline. Three alternating fresh-process project/first-question samples and one count per scenario use identical Content/interpreter; no concurrent benchmarks. Loading, validation, analysis, statistics and generation are reported separately. No performance threshold is added to CI.

Independent bounded fixtures compare expanded weighted bindings against full canonical enumeration, complete representative PL/JA pairs, duplicated text/contexts, four forms, fixed progressive/desiderative forms, multiple arguments, government/agreement, counters, compositions, filters, settings changes, entity/form mutations, old-host fallback and a non-relative noun quiz. A deterministic assertion verifies fewer renderer calls, without timing hardware. Existing engine, quiz, progress and Mobile regression tests remain authoritative. The existing release comparison also checks legacy pairs and unchanged XML; production latency is measured only by the optional release tool, never copied into unit fixtures.

## Windows quiz setup layout

`SpecializedQuizSetupDialog` serves Grammar (including all relative patterns), verbs, adjectives and availability. Its existing notebook now has bounded `VerticalScrolledFrame` pages for settings, forms and patterns, with local mouse-wheel bindings and wrapping checkbox labels. An independent footer row keeps action buttons outside scrolling content. The lesson launcher, conjugation and sentence setup use the same 720×650 initial size, resizable weighted body and fixed footer; the existing monitor-work-area clamp remains in use. Conjugation reuses the same viewport; sentence setup retains its existing scrolling PatternPicker and form Listboxes. Settings serialization and selection rules are unchanged; Mobile layout is untouched.

`test_quiz_setup_scrolling.py` uses synthetic v1 settings and real Tk widgets: 23 patterns, 35 forms, one-pattern case, wheel/end-of-list selection, resize, footer bounds and settings round-trip. It also covers lesson setup dialogs. Font scales 100/125/150% are tested when a display is available. Headless environments skip these native tests, rather than claiming visual coverage from fake controls. Manual Windows checks at 1366×768 and Full HD, 125/150% OS scaling and monitor/taskbar combinations remain necessary: Tk font scaling is not a substitute for per-monitor DPI testing.


## Final review and actual menu opening (2026-10-24)

This continuation compares Kotomi `b12de81` and Content `ab18c0a`; the complete PRs were also reviewed against their `main` branches. The user clarified that the affected application is **KotomiMobile running on Windows (Kivy)**. Native Tk `QuizLauncherFrame` does not calculate statistics or validate the project when opening configuration. Its profiled import/profile/settings path took 94 ms initially and 29 ms on reopening, excluding Tk drawing.

The Kivy bottleneck was full project validation while building verbs/adjectives/availability controllers. Start reads and validates the project again, so that initial validation was unnecessary for displaying settings. The launcher now supplies one freshly loaded project to these quizzes, following the existing Grammar profile path. Verb/adjective `reload_engine` consumes it once; subsequent Start/reload still reads and validates current data. Errors requiring full validation can consequently appear on Start instead of menu entry. There is no project cache across openings or change to validation rules. Module refresh remains intact for updated packages. `open_quiz` also removes two 160 ms pauses and the completion-animation wait, closing the popup when the screen is ready. Loading remains during actual work, without new artificial percentages.

Measurements use real Kivy 2.3.1 widgets, SDL offscreen and Mesa on Linux, without widget doubles. Three fresh-process AB/BA pairs, two openings per process, no concurrent tests. Timing starts at the menu callback; physical Windows click delivery is not measured. Import/profile, project load, analysis, settings, engine, widget construction, longest UI frame and settings navigation are separate. Nested stage times are inclusive and must not be summed.

| Quiz | First opening before → after | Reopening before → after |
|---|---:|---:|
| Verbs | 4485 → 235 ms | 4600 → 218 ms |
| Adjectives | 4435 → 215 ms | 4856 → 226 ms |
| Availability | 4406 → 218 ms | 4705 → 232 ms |
| Relative clauses | 718 → 277 ms | 782 → 259 ms |
| Grammar | 703 → 232 ms | 738 → 253 ms |

One initial verb opening spent 3539 ms in validation, 3612 ms in the engine, and 3712 ms in its longest UI frame. Afterwards this path performs no validation, engine construction takes 0.18 ms and the longest frame takes 122 ms. These are environment measurements, not Windows latency guarantees.

The full-relative count profile showed 83,809 renders and repeated checks of identical role/word/noun pairs. `_SearchCandidates.role_pairs` memoizes up to 4096 exact results of the existing predicate within one search, with fixed project, analysis and form. Keys include both slots and IDs; the solver still checks full-sentence dependencies. It stores no sentences, survives neither operations nor edits, and never merges forms. Single-noun searches do not use this pair memo. `iter_counted_possibilities` rejects ineligible cases before independence analysis. Previous independent-domain factoring and all fallbacks remain, including exhaustive Simulator metrics.

| Count | Identical result | Before → after this continuation |
|---|---:|---:|
| Identity, median of 3 pairs | 71,936 | 2.511 → 2.342 s |
| All 21 new patterns, one pair | 142,591 | 10.127 → 9.470 s |
| Full relative quiz, median of 3 pairs | 182,651 | 13.312 → 12.723 s |
| Legacy subject relative, median of 3 pairs | 6480 | 524 → 463 ms |
| Simple verb, median of 3 pairs | 2480 | 85.4 → 87.3 ms |
| Three liked things, one pair | 729,000 | 34.8 → 33.4 ms |

The counting improvement is modest. The simple verb retains a +1.9 ms difference, not claimed as speedup or proof of zero overhead. These timings must not be directly compared with the historical 34.8 s from another environment execution. Full Grammar still exceeds the 12 s process deadline, without returning partial totals. Coupled domains, counters and large word products remain expensive; further factoring would require a broader independence proof. Separate Start measurements remain approximately 4.2–4.6 s, mostly preserved full validation on the UI thread. Removing menu latency does not remove that cost.

A separate first-question sample measured 29.7 → 35.4 ms for the full quiz, 19.6 → 18.3 ms for one pattern, and 1.10 → 1.10 ms for the simple verb. One sample does not prove zero overhead; complete outputs and RNG remain identical.

Additional review/tests cover a transitive three-noun dependency chain with a fourth independent dimension, full pairs/bindings with memo enabled/disabled, four forms, fresh results after edits, complete eligible sets, contexts and identical text. Existing progressive/desiderative, multi-argument, government/agreement, counter, composition, filter and RNG tests remain. The release comparison preserved 76 complete legacy PL/JA pairs. **No XML or lexical translation changed during this continuation.** The original lesson implementation in the complete PR adds vocabulary/forms and patterns; that scope is separate from optimization.

New bounded Kivy controller tests verify one-time project handoff, no validation before Start, both instruction languages and subsequent reload. The launcher queue test now checks immediate popup dismissal once the screen is ready instead of deliberate animation waiting. This is an intentional presentation change, not a grammar expectation change. Verb/adjective packages are version 1.1.3 with identical sources in both repositories; older hosts retain their previous path without preloaded_project. Current complete CI results are linked in the PR.

### Windows GUI and remaining limitations

The previous shared scrollable Tk dialogs, fixed footers and test scaling restoration remain. Real Kivy offscreen checks cover scrolling to controls, reversible selection, resizing and settings-button bounds for verbs and all 23 relative patterns at 1366×768, 1093×614, 911×512 and 1920×1080. These logical sizes **do not test system DPI at 125/150%**. Native Tk tests run in Windows CI; the local environment has no Tk display. Physical mouse clicks/wheel and an Android device were not tested.

- P1, release verification: exercise the user's KotomiMobile on Windows after updating both application and packages, at 1366×768/Full HD and 125/150% DPI. Code and real Kivy timings support the menu fix, but green CI does not verify the display driver or system DPI. This remains the gate before unconditional merge approval.
- P2, existing Start cost: approximately 4 s of full validation on the UI thread. A separate fix can be deferred if that delay is accepted; no new regression or weaker validation was introduced.
- P2, exact statistics: the large relative quiz remains approximately 13 s, and full Grammar remains expensive. Counting stays off the UI thread and exact; further optimization can be deferred without changing available sentences.

Reproduce with `tools/benchmark_relative_lesson26_review.py --worker menu --selection verbs --kotomi KOTOMI --data CONTENT`. Optional `--menu-start` and `--menu-layout` separately measure Start and check layout. Linux used `KIVY_NO_ARGS=1 SDL_VIDEODRIVER=offscreen`; use the actual backend on Windows. This continuation's results are in `final_review` in the existing JSON report. No benchmark or timing threshold was added to CI.
