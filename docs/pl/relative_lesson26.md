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
| Która z tych rzeczy to zegarek, który kupiłem? | わたしがかったとけいはどれですか。 |
| Gdzie znajduje się miejsce, w którym mieszkam? | わたしがすんでいるところはどこですか。 |
| Jaki był hotel, w którym nocowałem? | わたしがとまったホテルはどうでしたか。 |
| Kiedy przypada dzień, w którym mama idzie do Japonii? | おかあさんがにほんへいくひはいつですか。 |
| Kim jest osoba, która ma na sobie ubranie? | ふくをきているひとはだれですか。 |
| Kim jest osoba, z którą najbardziej chcę się spotkać? | わたしがいちばんあいたいひとはだれですか。 |
| Która z tych rzeczy to wino, które najbardziej lubię? | わたしがいちばんすきなワインはどれですか。 |
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


## Historyczne pomiary implementacji

Trzy naprzemienne uruchomienia w świeżych procesach: mediana ładowania 112,5 → 152,0 ms; pełnej walidacji 5,78 → 9,28 s; pierwszego podglądu starego wzorca 11,7 → 19,0 ms. To pomiar na tej maszynie, przy większym zasobie słów i wzorców, nie gwarancja czasu na telefonie. Pełne próbki: `relative_lesson26_performance.json` w katalogu raportów Content. Nie zmierzono pełnej liczby kombinacji nowego quizu.

## Poprawki po code review

Poprawki obejmują dziesięć z 21 nowych szablonów. Definicje wcześniejszych wzorców, skład quizu i ustawienia, wszystkie słowniki, XML gramatyki i lekcje pozostały identyczne bajtowo względem początkowego heada PR. `relative_lesson26_regressions.json` zawiera hashe i 76 niezmienionych pełnych par PL/JA (18 reprezentatywnych rodzin, cztery formy oraz cztery wymuszone pytania zwrotne). To porównanie wydania, nie skopiowana fixtura testu jednostkowego.

| Wzorce | Wynik przeglądu |
|---|---|
| Osoba i dopełnienie; Osoba i dopełnienie 〜ている | Początek „To … jest …”; identyfikowana osoba w mianowniku, człon nadrzędny w narzędniku, podmiot przydawki nadal w mianowniku. |
| Wybór przedmiotu; Upodobanie; Pożądana rzecz | Początek „Która z tych rzeczy to …”, wspólny dla różnych rodzajów rzeczownika. Po japońsku nadal pytanie `どれ`. |
| Wskazanie przedmiotu | „Czy to klucz, którego zapomniałem?” zamiast „Czy klucz, którego zapomniałem, to właśnie to?”. Znaczenie `wasureru` bez zmian. |
| Dzień czynności | „To piątek jest dniem, w którym mama przychodzi do Polski.” Wielka litera wynika z szablonu. |
| Pragnienie spotkania | Stała polska fraza „chcę się spotkać”; japoński czasownik ograniczony istniejącym `id:au`. Osoba i rekcja zaimka pozostają zmienne. |
| Pragnienie podróży | Spójne pytanie tak/nie: „Czy kraj, do którego najbardziej chcę pojechać, to Indie?” / `わたしがいちばんいきたいくにはインドですか。`. |
| Opis osoby | Pytanie tak/nie i istniejące ograniczenie `id:matsu`: „Czy osoba, na którą czekałem, była urocza?” / `わたしがまったひとはかわいかったですか。`. Eliminuje przypadkowe czasowniki przechodnie z osobą jako dopełnieniem. |
| Miejsce czynności; Miejsce czynności 〜ている | Szablony bez zmian. Przywrócony szyk sprzed PR daje „Gdzie znajduje się dom, w którym się urodziłem?”. |
| Pytanie o wykonawcę; Pytanie o wykonawcę 〜ている; Lokalizacja przedmiotu; Ocena miejsca; Miejsce zamieszkania; Pytanie o dzień; Ocena przedmiotu; Powód czynności; Liczba osób | Przejrzane bez zmian szablonu. Pełne pary sprawdzają rekcję, uzgodnienia i kompatybilne formy. |

Jedyna zmiana silnika w tej poprawce usuwa dwuwierszowy wyjątek „dowolny wcześniejszy relative” dodany przez #226. Nie dodano nowego warunku renderera. Oznajmujące „urodziłem się” i „chcę się spotkać” zachowują szyk słownikowy. Pytania odzyskują „w którym się urodziłem”; inne pytania i dalsze frazy czasownikowe zachowują poprzednie działanie. Wzorzec spotkania zapisuje stałą frazę modalną, podobnie jak istniejące wzorce upodobania zapisują stałe orzeczenia. Nie przepisuje tłumaczenia czasownika. Ogólny szyk pytań modalnych nie został przebudowany.

`tests/test_polish_clitic_regressions.py` dodaje 13 niezależnych przypadków v2 z pełnymi parami: zwrotność, negacja, przeszłość/teraźniejszość, pytania z przydawką i bez niej oraz dwa czasowniki. Wcześniejszy test spotkania zachowuje oczekiwane zdanie, a teraz sprawdza rzeczywisty stały szablon. Audyt wydania sprawdza 43 pary PL/JA i siedem odrzuconych kombinacji; wszystkie sprawdzane nowe zdania zaczynają się wielką literą. Wzorzec zamieszkania ma jedną obsługiwaną kombinację leksykalną; nie dodano sztucznych słów. Kontrola UI bez ekranu obejmuje 21 pojedynczych wyborów oraz wszystkie nowe i mieszane wzorce, zapis ustawień, odrzucenie nieobsługiwanych form grzecznych przydawki i 43 pary Symulatora. Nie przeprowadzono obsługi natywnego urządzenia ani budowy APK.

### Wydajność poprawek

Dane: `relative_lesson26_review_performance.json`. Po trzy pomiary w świeżych procesach na jednym komputerze/interpreterze; mediany są obserwacją lokalną, nie gwarancją dla telefonu. Pierwszy stary podgląd mierzono przed walidacją, bez korzystania z jej cache.

| Operacja | Początkowy PR | Po poprawkach |
|---|---:|---:|
| Ładowanie Content | 71,2 ms | 74,6 ms |
| Pełna walidacja projektu | 3904 ms | 3957 ms |
| Pierwszy podgląd starego wzorca | 11,2 ms | 10,3 ms |
| Pierwsze pytanie, jeden nowy wzorzec | 20,0 ms | 19,4 ms |
| Pierwsze pytanie, wszystkie 21 nowych | 42,7 ms | 35,3 ms |
| Pierwsze pytanie, pełny quiz przydawek | 35,0 ms | 32,9 ms |

Wiersze quizu używają już wczytanego projektu, sprawdzenia dostępności i pierwszego generowania. Dostępność po poprawkach zajmuje odpowiednio 19,8/44,3/41,8 ms, konstrukcja silnika około 0,1 ms. Zimne ładowanie/walidacja są mierzone osobno. Przy tym samym aktualnym silniku walidacja Content z main trwa 3693 ms; rozszerzonego Content bez 21 nowych szablonów 3881 ms; ze wszystkimi szablonami 3957 ms. W tym kontrolowanym porównaniu większość dodatkowej pracy walidacji wynika z większego grafu Content, mniejsza część z nowych szablonów. Nie dowodzi to, że wcześniejsze pomiary 5,78/9,28 s w innych warunkach wynikały wyłącznie z tych czynników. Trzy próbki nie stanowią statystycznej gwarancji wydajności.

`statistics()` przechodzi pełne podglądy przez `iter_quiz_previews`; `has_possible_question()` kończy po znalezieniu generowalnej kombinacji. Koszty są różne. Mały wzorzec podróży daje dokładnie trzy możliwości. Liczenie wieloargumentowego wzorca identyfikacji osoby, wszystkich nowych wzorców i całego quizu przekracza limit procesu 12 s zarówno przed poprawkami, jak i po nich. Nie podano wymyślonej ani ekstrapolowanej sumy. To potwierdzone ograniczenie pełnych statystyk, nie dowód nowej regresji. Nie dodano optymalizacji liczenia/solvera ani ciężkich testów wydajnościowych CI.

Opcjonalne pomiary odtwarzają `tools/benchmark_relative_lesson26_review.py` i `tools/compare_relative_review.py`; wymagają oddzielnych katalogów kodu i Content przed/po, a benchmark dodatkowo Content z main. Czytają wyłącznie zadeklarowany graf projektu produkcyjnego. Ograniczony koszt opisano w skryptach; nie wchodzą do test discovery. Niezależna fixtura nie potwierdzi rzeczywistego słownika, kompletnych zdań wydania ani opóźnień dla faktycznego Content.

### Pozostałe ograniczenia

Negatywne formy „Liczba osób” nie mają obecnie kompatybilnej kombinacji i są odfiltrowywane; sprawdzono twierdzącą teraźniejszość/przeszłość. Tak samo działał początkowy PR. Istniejące tłumaczenia `iku` „idzie” i `kuru` „przychodzi” mogą brzmieć dosłownie przy kraju jako celu ruchu. Nie zastąpiono ich ukradkiem innymi czasownikami podróży. Ogólny szyk modalny, osoby gramatyczne, przydawki egzystencjalne i dowolne kompozycje trzech argumentów pozostają poza zakresem. Kosmetyczne poprawki nie są deklaracją pełnej walidacji językowej każdej kombinacji kartezjańskiej.
