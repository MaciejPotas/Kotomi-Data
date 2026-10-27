# Kanji 151–160: inwentaryzacja i niepełny import (WIP)

## Zakres i ograniczenia

Źródła: *新漢字15-2（151-155）* i *新漢字16-1（156-160）*, po jednej stronie każdy. 39 pozycji w 10 grupach kanji.
Porównanie z Kotomi-Data main (Content 69) znalazło 8 wpisów istniejących.
Przygotowano 26 nowych rzeczowników, 2 przymiotniki i 1 czasownik oraz zamianę 13 `local_word` na 27 `dictionary_ref` w lekcji 151–155.
**Status: WIP, NIE GOTOWE DO MERGE.** Nie utworzono lekcji 156–160, ponieważ nie znaleziono bezpiecznej reprezentacji dwóch pozycji (私, 私立).

## Pełna inwentaryzacja

| Kanji | Japoński | Kana | Znaczenie źródłowe | ID | Status | Semantyka i uzasadnienie |
|---|---|---|---|---|---|---|
| 151 | 教える | おしえる | uczyć, instruować | `verbs/oshieru` | existing | person/target/object. Existing verb; distinguish teaching a subject vs teaching someone. |
| 151 | 教室 | きょうしつ | sala lekcyjna | `nouns/kyoushitsu` | new | place. Classroom, not entire building; w/do relation. |
| 151 | 教科書 | きょうかしょ | podręcznik | `nouns/kyoukasho` | new | text. Bound-volume counting. |
| 151 | 教育 | きょういく | edukacja | `nouns/kyouiku` | new | abstract. Process, not a person. |
| 151 | 教授 | きょうじゅ | profesor | `nouns/kyouju` | new | person. Professor rank meaning, not 教授する teaching sense; male-generic PL gloss. |
| 151 | 教師 | きょうし | nauczyciel | `nouns/kyoushi` | new | person. Occupation, distinct from 先生. |
| 152 | 作る | つくる | robić, wytwarzać | `verbs/tsukuru` | existing | subject/object. Existing sense and forms retained. |
| 152 | 作業 | さぎょう | praca, czynność | `nouns/sagyou` | new | abstract. Activity, not employee or workplace. |
| 152 | 手作り | てづくり | wykonany ręcznie | `nouns/tezukuri` | partial | abstract. Imported nominal sense 'ręczne wykonanie'; 手作りの attributive not supported here. |
| 152 | 作家 | さっか | autor, pisarz, artysta | `nouns/sakka` | new | person. Broad 'twórca', not only book authors. |
| 152 | 作品 | さくひん | dzieło, utwór | `nouns/sakuhin` | new | media. Creative work, not generic physical object. |
| 152 | 名作 | めいさく | arcydzieło | `nouns/meisaku` | new | media. Creative masterpiece. |
| 153 | 通る | とおる | przechodzić | `verbs/tooru` | existing | route. Existing motion verb retained. |
| 153 | 通学 | つうがく | uczęszczanie do szkoły | `nouns/tsuugaku` | new | abstract. School attendance, not route/place. |
| 153 | 通う | かよう | uczęszczać | `verbs/kayou` | existing | target. Existing attendance verb retained. |
| 153 | 共通 | きょうつう | wspólny | `adjectives/kyoutsuu` | partial | concrete/abstract. Explicit 共通の; shared-between relationship not expressible semantically. |
| 153 | 交通 | こうつう | ruch uliczny | `nouns/koutsuu` | new | abstract. Traffic, not street/location. |
| 153 | 普通 | ふつう | zwykły | `adjectives/futsuu` | new | concrete/abstract. Explicit 普通の and 普通に with adverbial gloss. |
| 154 | 歩く | あるく | chodzić pieszo | `verbs/aruku` | existing | subject/destination. Existing motion verb retained. |
| 154 | 歩道 | ほどう | chodnik | `nouns/hodou` | new | place. Walking path, not any building. |
| 154 | 散歩 | さんぽ | spacer | `nouns/sanpo` | new | abstract. Activity, counted in Japanese with 回, not general_item. |
| 154 | 横断歩道 | おうだんほどう | przejście dla pieszych | `nouns/oudanhodou` | new | place. Na/na location/destination; counting location. |
| 154 | 進歩する | しんぽする | robić postępy | `verbs/shinposuru` | partial | subject: person/abstract. 13 forms, explicit seven-class maps; passive/causative participant changes deferred. |
| 155 | 取る | とる | brać | `verbs/toru` | existing | object. Existing broad take meaning. |
| 155 | 取材 | しゅざい | zbieranie materiałów | `nouns/shuzai` | new | abstract. Journalistic research; no fictitious physical object. |
| 155 | 取り外す | とりはずす | zdejmować, demontować | `verbs/torihazusu` | existing | object. Existing removal verb. |
| 155 | 取り引き | とりひき | transakcja | `nouns/torihiki` | new | abstract. 交易 may appear 取引, source spelling 取り引き preserved. |
| 156 | 私 | わたし/わたくし | ja | `PENDING` | decision | pronoun. First-person pronoun cannot bind a fixed Polish gender and vocative; do not fake noun agreement. |
| 156 | 私立 | しりつ | prywatny (o instytucji) | `PENDING` | decision | no-adjective/noun. 私立の, not 私立な. Current adjective type cannot represent no-adjective faithfully. |
| 156 | 私用 | しよう | prywatna sprawa | `nouns/shiyou` | new | abstract. Private business, not adjective 'private'. |
| 157 | 兄 | あに | własny starszy brat | `nouns/ani` | new | person. Kinship term, distinguish honorific お兄さん. |
| 157 | お兄さん | おにいさん | czyjś starszy brat | `nouns/oniisan` | new | person. Honorific separate entry; Polish cases explicit. |
| 157 | 父兄 | ふけい | rodzice, opiekunowie | `nouns/fukei` | partial | person/plural_masculine_personal. School guardians collective, Polish plural 'opiekunowie'; modern gender nuance noted. |
| 158 | 弟 | おとうと | młodszy brat | `nouns/otouto` | new | person. Male younger sibling. |
| 158 | 兄弟 | きょうだい | rodzeństwo, bracia | `nouns/kyoudai` | partial | person/neuter. Neutral collective 'rodzeństwo', sense 'bracia' not a separate gloss here. |
| 159 | 姉 | あね | własna starsza siostra | `nouns/sister` | existing | person. Exact existing Japanese entry, not modified. |
| 159 | お姉さん | おねえさん | czyjaś starsza siostra | `nouns/oneesan` | new | person. Honorific usage distinct from 姉. |
| 160 | 妹 | いもうと | młodsza siostra | `nouns/imouto` | new | person. Female younger sibling. |
| 160 | 姉妹 | しまい | siostry | `nouns/shimai` | partial | person/plural_non_masculine_personal. Already-plural Polish lexical realization; not counted as two individual women. |

## Dobór i kompletność form

- 26 nowych rzeczowników ma siedem jawnych przypadków polskich oraz kategorię i klasę zgodności. Liczba mnoga `few/many` powstaje **wyłącznie** w nowych policzalnych hasłach z rzeczywiście dopasowaną klasą licznika (np. `bound_volume` dla podręcznika i `person` dla zawodu/krewnego). Nie wymuszano `general_item` dla transakcji, spaceru, nauki, ruchu drogowego ani prac dziennikarskich.
- Dla `fukei` i `shimai` bazowy przekład jest liczby mnogiej. Nie dopisano fikcyjnego polskiego mianownika pojedynczego ani automatycznego licznika.
- `kyoudai` zachowuje sens zbiorowego, inkluzywnego `rodzeństwo`. Przekład "bracia" nie jest całkowicie ekwiwalentny w każdym kontekście, dlatego nie podmieniano nim podstawowego znaczenia.
- `kyoutsuu` i `futsuu` mają jawne japońskie formy; przydawkowe zapisano jako `共通の` i `普通の`, a nie niezweryfikowane `~な`. Polskie `polish_forms` obejmują siedem przypadków i siedem klas zgodności. Nie generowano nienaturalnych nominalizacji i końcówek bez uzasadnienia.
- `shinposuru` ma jawne formy podstawowe, przeczące, przeszłe, potencjalną, ciągłą, desideratywną, warunkową i `te_form` (13 w sumie). Dwanaście form osobowych zawiera siedem map `agreement_translations` (84 komórki); nie dodano stron biernej/sprawczej wymagających innych uczestników.
- Siedem istniejących czasowników oraz `sister` pozostawiono bez modyfikacji. Ich wcześniejszych danych nie należy uważać za ponownie zaudytowane tylko dlatego, że zostały użyte przez lekcję.

## Decyzje wymagające szczególnej uwagi

1. **手作り**: nominalna realizacja "ręczne wykonanie" jest zgodna z japońskim rzeczownikowym znaczeniem, ale materiał pokazuje przede wszystkim sens przydawkowy "wykonany ręcznie". Bez obsługi rzeczownikowych konstrukcji `の` w edytorze nie należy udawać `na_adjective`. Wymagany dalszy kontrakt dla drugiego sposobu użycia.
2. **共通**: oznacza wspólną cechę co najmniej dwóch rzeczy/osób; same kategorie `concrete abstract` nie wyrażają wymogu współdzielenia. Możliwe fałszywie dodatnie połączenia `wspólny X` i zbyt szeroki `describes`. To ograniczenie semantycznej reprezentacji, a nie powód do zawężenia hasła.
3. **教授**: źródło dotyczy profesora, ale `教授` może też oznaczać nauczanie. Wpis importuje tylko znaczenie osobowe. Osobny sens potrzebowałby osobnego ID.
4. **父兄 / 兄弟 / 姉妹**: osoby zbiorowe i naturalnie mnogie nie powinny dostawać takiego samego profilu liczenia jak pojedynczy brat.
5. **私**: brak stabilnej płci/rodzaju osoby mówiącej w danych statycznych, a polski zaimek pierwszej osoby ma odrębny paradygmat oraz brak zwykłego wołacza. Należy dodać obsługę zaimków osobowych albo sprawdzić bezpieczny zapis fleksji bez sztucznego `agreement class`.
6. **私立**: rzeczownikowy określnik `私立の`, nie zwykłe `~な`; brak natywnej klasy `no_adjective`. Nie dodano fałszywego wpisu.
7. **進歩する**: podmiot może być osobą, projektem lub procesem. `person abstract` to rozsądny przybliżony zakres, ale nie filtruje wszystkich dziwnych połączeń. Rekcja bierna i kauzatywna nie jest mechanicznie równa czynnej.

## Kontrola regresji, testy i aktualizacja

- Planowane zmiany: tylko słowniki, lekcja 151–155, revision/manifest i ten raport. Nie zmienia się Kotomi, DSL, wzorców, tłumaczeń XML ani testów.
- Strukturalna kontrola przed publikacją obejmuje obecność ID i referencji, brak duplikowania nowych ID oraz spójność SHA-256 manifestu. To nie zastępuje walidacji silnika.
- **Nie wykonano**: `tools/validate_repository.py`, pełnego `QuizProject.validate()`, testów generatora z syntetycznymi fixture, benchmarku startu quizów, natywnego Androida. Brak lokalnej kopii repozytorium dostępnej dla wykonania tych poleceń; nie raportować ich jako PASS.
- Wpływ na poprzednie wzorce nie został empirycznie wykluczony. Szczególnie rozszerzone `describes` i `person abstract` wymagają diagnostyki. Bieżącego brancha nie należy scalać do `main`.
- Lekcja 156–160 będzie dodana dopiero po rozstrzygnięciu `私` oraz `私立` i sprawdzeniu wszystkich referencji.

## Materiały porównawcze

Weryfikacja japońskich kategorii i alternatywnych sensów:
- https://bunpro.jp/ja/vocabs/手作り
- https://bunpro.jp/ja/vocabs/共通
- https://bunpro.jp/ja/vocabs/普通
- https://bunpro.jp/ja/vocabs/私立
- https://kotobank.jp/jeword/教授

## Kryterium dalszego zakończenia

Wykonać odpowiednią implementację obu brakujących pozycji bez fałszywej klasyfikacji, stworzyć kompletną lekcję 156–160, uruchomić oficjalny walidator i testy fixture (bez produkcyjnej bazy silnika), sprawdzić rzeczywiste użycia poprawne i odrzucane, ocenić wydajność, potwierdzić poprawność aktualizacji treści i dopiero wtedy oznaczyć branch jako gotowy do merge.
