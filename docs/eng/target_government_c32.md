# C3.2: universal target and Polish government

`target` denotes a verb-specific relational argument, usually marked with に. It is distinct from `object` (e.g. a borrowed book marked with を) and `destination` (movement destination). A target can be a lender, recipient, anger target or attendance facility. The pattern still writes に literally; role metadata does not insert particles.

`government` on an individual verb role selects a shared Polish frame. The existing binder and `role_matches` remain responsible for selection, including multiple roles of one verb. A missing target frame excludes a candidate from this pattern. There are no word IDs in the pattern and no verb–noun lookup table.

## Production pattern

```xml
<sentence_pattern id="Czasownik z target" category="basic"
    forms="dictionary polite_nonpast plain_negative polite_negative past_plain past_polite past_negative_plain past_negative_polite">
  <question>{verb@action[role:target, form].translation} {noun@target[government:@action].phrase}.</question>
  <answer>{noun@target}に{verb@action[form]}。</answer>
</sentence_pattern>
```

The only addition to the requested XML is the existing `forms` attribute. Eight basic finite forms preserve participant roles; passive, causative and standalone linking forms are outside this construction. This restricts the pattern, not the dictionary.

## Audit of all 21 declarations

11 verbs receive government; 10 retain no target frame. Decisions concern the current lexical sense and accepted arguments.

| Verb | Frame / readiness | Meaning, government and boundary |
|---|---|---|
| `ayamaru` | `direct_object` | apology recipient; accusative, genitive under negation |
| `hairu` | `do_genitive` | interior; do + genitive; enclosed_space only |
| `ireru` | `poza / excluded` | container; do + genitive, but requires an appropriate inserted object |
| `kariru` | `od_genitive` | lender; od + genitive; contextual gloss |
| `kayou` | `do_genitive` | regular attendance facility; do + genitive |
| `kotaeru` | `poza / excluded` | person: dative; message: na + accusative; requires argument-dependent realization |
| `nareru` | `poza / excluded` | habituation target; do + genitive, but wildcard includes inappropriate concepts and quantities |
| `naru` | `poza / excluded` | result of change; instrumental; wildcard does not constrain plausible results |
| `okoru` | `na_accusative` | anger target; na + accusative including negative forms |
| `oshieru` | `poza / excluded` | teach a person (accusative/genitive) or tell something to a person (dative); construction/sense dependent |
| `sawaru` | `poza / excluded` | touched object; genitive, but concrete also contains music, voice and email |
| `teishutsusuru` | `poza / excluded` | submission recipient; dative person / w + locative institution; needs an object |
| `tomaru` | `poza / excluded` | stopping place; w/na/przy; also distinguish 止まる from 泊まる |
| `usowotsuku` | `dative` | person lied to; dative |
| `ageru_give` | `dative` | recipient away from speaker; dative; contextual gloss; object omitted in context |
| `kaesu` | `dative` | recipient of returned item; dative; object omitted in context |
| `kasu` | `dative` | borrower; dative; contextual gloss |
| `kureru` | `poza / excluded` | recipient in speaker perspective; dative; arbitrary person does not preserve me/us deixis |
| `morau` | `od_genitive` | giver; od + genitive; object omitted in context |
| `watasu` | `dative` | recipient of handed item; dative; object omitted in context |
| `sumu` | `poza / excluded` | residence; w/na + locative; place also contains nonresidential locations |

## Frames and categories

Added `do_genitive`, `od_genitive`, `dative` to the application's Polish catalog. Reused `direct_object` and `na_accusative`. All five frames are shared. Negation preserves do/od genitive and dative; direct_object switches accusative to genitive.

`kayou` retains `education_facility sports_facility`. New schools and suitable sports facilities work without editing the verb. An ordinary building is not an attendance facility. `kariru` and `kasu` retain `person`, excluding animals as lenders/borrowers.

`hairu` now selects `enclosed_space`, a reusable child of `place`. `building` inherits from it; daidokoro (kitchen), room and jimusitsu (office) use it directly. Existing place/concrete matching remains valid. Five hairu pairs are removed: kaigan, park, bazaaru, naka, oku. Parks and bazaars can occur with hairu in other senses, but Polish na and boundary-crossing context need separate treatment. Naka/oku are relational concepts needing complements. New rooms inherit matching without ID lists.

All other accepts/nouns declarations remain unchanged. Existing ireru, kotaeru and teishutsusuru noun exceptions are retained and excluded from the new pattern. No global categories were broadened to force their inclusion.

## Translation with an explicit argument

An optional `target_translation` attribute belongs to a specific form:

```xml
<form ref="dictionary" kana="かりる" translation="pożyczam od kogoś"
      target_translation="pożyczam" />
```

Selection uses `analysis.driver_for_entity` and `role_for_entity`: a noun bound to this verb's target activates the variant. Explicit `government:@action` and automatic `government` behave identically. Another verb's target cannot activate it. A target alongside an explicit object also works. No sentence search or new DSL selector is needed.

Absent variants preserve the ordinary translation. Standalone verb quizzes retain “pożyczam od kogoś”. Only eight forms each of kariru, kasu and ageru_give receive variants. Studio exposes **Translation with explicit target (optional)** in the verb forms table. Clearing the cell removes the variant; Japanese form regeneration preserves it. Inactive source-language loading retains the XML extension losslessly.

The variant applies to ordinary form `.translation`. It does not replace explicit `translation:base` or the separate subject `agree` paradigm. Combining both in future subject-aware constructions needs a separate design, never automatic text stripping.

## Examples and limitations

| Polish | Japanese |
|---|---|
| uczęszczam do szkoły. | がっこうにかよう。 |
| uczęszczam do sali gimnastycznej. | たいいくかんにかよう。 |
| wchodzę do szkoły. | がっこうにはいる。 |
| pożyczam od siostry. | あねにかりる。 |
| pożyczam siostrze. | あねにかす。 |
| nie pożyczam od siostry. | あねにかりない。 |

A noun destination relation can produce “na salę gimnastyczną”, while kayou's frame produces “do sali gimnastycznej”. Combined verb/noun-dependent government remains deliberately outside this version. Transfer examples omit a contextually known object. Past translations retain the existing first-person masculine wording.

## Publication and verification

Content 64 requires manifest format 3. Format 2 remains the revision-63 boundary; format 1 remains for older data. New clients accept all three; C3 clients reject format 3 before payload downloads. Full snapshot validation, hashes and rollback remain unchanged. Release the compatible application first. The new form attribute, category and pattern require the revision increment.

Application tests use independent v1 fixtures in `test_universal_target.py`, `test_target_translation_persistence.py` and existing C3/C3.1 tests. Production examples and counts are verified separately by opt-in `tools/validate_target_c32.py --kotomi ../Kotomi`, outside unit tests. Reports under `docs/validation` record scope and measurements. Historical C3 reports remain evidence of that stage, not the current C3.2 snapshot.

Measurements: 15 cold/warm rounds, 21 rounds at scales 1/10/50/200. One outlier was rechecked in 7 alternating fresh processes with 301 samples: +2.34%. No confirmed regression above 10%. Commands: `tools/benchmark_lesson_focus.py --rounds 15` and `tools/benchmark_target_c32.py --kotomi CHECKOUT --output report.json`. Protocol: `tools/updates/validate_content_compatibility_c32.py --kotomi CHECKOUT` (add `--legacy-c3` for previous main). Acceptance and performance reports are in Kotomi-Data: `docs/validation/target_c32_acceptance.json`, `target_c32_performance.json`.
