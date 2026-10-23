# Przydawki z lekcji 26

Content 65 rozszerza istniejący quiz `relative_clauses`. Wymaga powiązanej poprawki Kotomi: wiązania podmiotu przed dopełnieniem, jawnego neutralnego kontekstu oraz katalogu form `progressive` i `desiderative`. Najpierw należy wdrożyć aplikację z tymi zmianami. Sam Content nie aktualizuje silnika.

To reprezentatywne pokrycie wszystkich rodzin A–H z zadania, **nie obsługa każdego zdania z PDF**. Poniższe ograniczenia są częścią zakresu wydania.

## Wzorce

Wszystkie nowe ID zaczynają się od `Przydawki / `. Warianty są rozdzielone tam, gdzie różnią się role, polski pytajnik lub forma orzeczenia. Żaden wzorzec nie przechowuje kompletnego przykładu jako stałej odpowiedzi.

| Końcówka ID | Zastosowanie |
|---|---|
| Osoba i dopełnienie | Identyfikacja wykonawcy; jeden czasownik, podmiot i dopełnienie |
| Pytanie o wykonawcę | `だれ`, z zachowaniem obu argumentów |
| Wybór przedmiotu | `どれ` i polski rodzaj rzeczownika |
| Wskazanie przedmiotu | Pytanie z `これですか` |
| Lokalizacja przedmiotu | `どこ` jako pytanie o położenie rzeczy |
| Miejsce czynności | Budynek, w którym lub na którym zachodzi czynność |
| Ocena miejsca | `どうでしたか`, z uzgodnionym polskim „był/była/było” |
| Miejsce zamieszkania | `すんでいるところ`; jawne „w którym” |
| Dzień czynności | Dzień opisany ruchem osoby, identyfikowany dniem tygodnia |
| Pytanie o dzień | `いつ`, niezależny podmiot i cel ruchu |
| Pragnienie spotkania | `〜たい` i rekcja „z kim” |
| Pragnienie podróży | Kraj, do którego chcę pojechać, z wyborem kraju |
| Upodobanie | `いちばんすきな`, osobna konstrukcja przymiotnikowa |
| Pożądana rzecz | `いちばんほしい`, osobna konstrukcja przymiotnikowa |
| Ocena przedmiotu | Przydawka dopełnieniowa z `どうでしたか` |
| Opis osoby | Przydawka dopełnieniowa z przymiotnikowym orzeczeniem |
| Powód czynności | `りゆうはなんですか`, polskie „dla którego” |
| Liczba osób | `なんにん` przez istniejące `interrogative` i `counter` |
| Osoba i dopełnienie 〜ている | Identyfikacja osoby wykonującej czynność lub będącej w stanie |
| Pytanie o wykonawcę 〜ている | Pytanie o tę osobę |
| Miejsce czynności 〜ている | Miejsce trwającej czynności nieprzechodniej |

Formy proste: `dictionary`, `plain_negative`, `past_plain`, `past_negative_plain`. Warianty `〜ている` i `〜たい` są stałą formą **nieprzeszłą twierdzącą**, nie nowymi osiami czasu w quizie. `progressive` przechowuje całe `よんでいる` lub `きている` wraz z właściwym tłumaczeniem, np. „ma na sobie”. `desiderative` przechowuje `あいたい` lub `いきたい`. Brak formy lub uzgodnienia wyklucza kombinację.

Istniejąca kompozycja `Czynność w toku 〜ている` nadal działa bez zmian. Jej `translation:current` zachowuje czas polskiego tekstu, ale składanie formy `te_form` z `いる` nie daje automatycznie znaczenia stanu `きている` i nie wstawia pomocniczego czasownika przed głową dowolnej przydawki. Zapis leksykalny dwóch dodatkowych form używa obecnego mechanizmu form, bez nowego solvera, placeholdera ani parametru DSL.

## Przykłady sprawdzane w całości

| Polski tekst | Japoński tekst |
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

Pełne pary, czas pomiarów i odrzucone kombinacje zawiera `docs/validation/relative_lesson26.json`. Pomiar liczenia dotyczy zablokowanych wyborów, nie całego iloczynu słownictwa. Audyt nie zmienia starych znaczeń czasowników, np. `miru` nadal korzysta z istniejącego „oglądałem”.

## Granice zakresu

- Nie ma odmiany czasowników przez osobę gramatyczną. Wzorce pierwszoosobowe jawnie zawierają `わたしが`; podmioty rzeczownikowe używają `agree`. Nie generujemy pozornego „kupiłeś” z pierwszoosobowego tłumaczenia. Przykłady z `あなた`, rodzicami w liczbie mnogiej i swobodnym posiadaczem nie są pokryte dosłownie.
- Nie ma dowolnego składania trzech lub więcej argumentów i modyfikatorów, np. „zegarek kupiony przez ciebie w Japonii”, „klucz zostawiony wczoraj w firmie”, „pierwsze spotkanie z mężem”. Obsługa dwóch argumentów jednego czasownika jest sprawdzona.
- Brak `じゅぎょうがないひ`, `ここにあったざっし` i `日曜日だけ`. Egzystencjalne przeczenie wymaga odrębnej rekcji; nie udajemy go zwykłym uzgodnieniem B3. Warianty przyszłe i negatywne `〜たい` oraz przeszłe/negatywne `〜ている` nie są wystawione w tym wydaniu.
- Pytanie o dzień ma formę „Kiedy przypada dzień, w którym…?”, nie dodatkowy wariant „Którego dnia…?”. Odpowiedzi identyfikacyjne używają `です`, bez negatywnej końcowej kopuły.
- Miejsce czynności jest ograniczone do budynków i czasowników oznaczonych `intransitive`; zapobiega to urwanym frazom „hotel, w którym mam na sobie”. Rzeczownikowe relacje dostarczają `w/na`; zaimek ma jawny miejscownik. „Miejsce zamieszkania” używa ogólnego `ところ`, nie dowolnego rzeczownika z kategorii place.
- Cały zakres polskich form głowy przydawki nadal jest pojedynczy. Pytanie o liczbę korzysta z istniejących form ilościowych rzeczownika i bezosobowego orzeczenia, bez pluralnego `relative`.
- Nie dodano wszystkich nazw własnych, party, egzaminu, obrazu ani idiomu `せがたかい`. Opis cechy sprawdzono na istniejącym poprawnym `かわいい`. Sam brak tych słów nie jest ograniczeniem silnika.

## Quiz i walidacja

Windows i Mobile korzystają z tej samej definicji quizu. Można wybrać wszystkie wzorce lub pojedyncze. Stare ID i ustawienia są zachowane; nowe wzorce nie są automatycznie dodawane do zapisanej przez użytkownika ręcznej listy. W wariantach z formami prostymi należy włączyć styl potoczny. Stałe formy `progressive/desiderative` są rozpoznawane jako warianty stałe, tak jak inne stałe konstrukcje.

Nowe odpowiedzi zawierają `{context[pool:none].kana}`. Pusta opcja kontekstu jest jedna; nie mnoży identycznego tekstu przez „dzisiaj/wczoraj”. Hinty nie otrzymują niewidocznych wyrażeń czasowych. Liczenie i podgląd nadal korzystają ze wspólnego silnika.

Uruchomienia z katalogu Kotomi-Data:

```sh
python tools/validate_repository.py
python -m unittest discover -s tests -v
python tools/validate_relative_lesson26.py --kotomi ../Kotomi --output docs/validation/relative_lesson26.json
python tools/validate_relative_lesson26_ui.py --kotomi ../Kotomi --output docs/validation/relative_lesson26_ui.json
```

Dwa ostatnie polecenia to jawne audyty wydania, poza testami jednostkowymi. Czytają faktyczne dane, ponieważ fixture nie potwierdzi poprawności opublikowanych zdań. Koszt: jedno ładowanie projektu, walidacja, ograniczona lista przykładów i pojedyncze pytania w wybranych konfiguracjach. Nie enumerują wszystkich kombinacji. Testy silnika używają niezależnego fixture v1. Test UI uruchamia rzeczywiste callbacki z atrapami kontrolek i fontu, nie fizyczny Windows/Android ani budowę APK.


## Pomiary lokalne

Trzy naprzemienne uruchomienia w świeżych procesach: mediana ładowania 112,5 → 152,0 ms; pełnej walidacji 5,78 → 9,28 s; pierwszego podglądu starego wzorca 11,7 → 19,0 ms. To pomiar na tej maszynie, przy większym zasobie słów i wzorców, nie gwarancja czasu na telefonie. Pełne próbki: `relative_lesson26_performance.json` w katalogu raportów Content. Nie zmierzono pełnej liczby kombinacji nowego quizu.
