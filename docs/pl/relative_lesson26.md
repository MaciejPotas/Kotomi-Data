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


## Optymalizacja dokładnego licznika

Pomiary z wcześniejszego review powyżej są historyczne. Profilowanie 5000 podglądów dużego wzorca identyfikacji zajęło 11,61 s pod cProfile: około 6,27 s w enumeracji solvera i 4,80 s w pełnym renderowaniu podglądu (czasy zagnieżdżone nakładają się). Statystyki quizu przechodziły cały iloczyn wyborów rzeczowników i realizowały oba języki dla każdej kombinacji. `has_possible_question()` potrzebuje jedynie pierwszej poprawnej kombinacji. Zwiększenie limitu czasu nie usuwa tego kosztu.

`iter_counted_possibilities()` ustala wybory słów i grupuje tylko niezależne domeny rzeczowników, korzystając z istniejącego planu realizacji oraz przechodnich zależności aliasów. Każdy wymiar jest enumerowany przez dotychczasowy solver i renderer przy ustalonych pozostałych wyborach. Powiązane rzeczowniki pozostają enumerowane; reprezentant otrzymuje dokładną krotność oraz komplet identyfikatorów niezależnych rzeczowników dla metryki dostępnych słów. Konteksty nadal liczą się osobno, nawet przy identycznym tekście. Wyniki wzorców/form sumują się tak jak wcześniej. Nie ma cache zdań ani wyników, wymagającego unieważniania, ani estymacji liczby możliwości.

Dotychczasowa pętla solvera i renderera dla jednej formy została wydzielona do `_iter_form_possibilities()` i jest współdzielona. Zapobiega to ponownemu globalnemu ustalaniu form dla każdej już zweryfikowanej próby. `SharedQuizEngine.iter_counted_previews()` udostępnia tę ścieżkę `GrammarQuizEngine.statistics()` na obu platformach. Starszy host i filtry nakładane po renderowaniu zachowują dotychczasową ścieżkę. Countery/ilości, zależności między rzeczownikami, nieustalone formy dynamiczne, pojedynczy rzeczownik i iloczyn domen słów ponad 256 nadal korzystają z dokładnej enumeracji tam, gdzie grupowanie nie ma zastosowania. Próg 256 wybiera algorytm, nigdy nie obcina wyniku. Nie zmieniono reguł gramatyki, DSL, wyboru ani XML słowników i wzorców.

`count_possibilities()` w Symulatorze nadal enumeruje: unikalnych tekstów pytań/odpowiedzi, zestawów słów i połączeń nie można zastąpić mnożeniem liczby wyborów. Kosztowne przypadki zapasowej ścieżki pozostają możliwe. Windows i Mobile już wykonują jawne obliczanie statystyk przez mechanizmy postępu i obliczeń; otwieranie i uruchamianie quizu nadal korzysta z wczesnego zakończenia sprawdzania dostępności. Zmiana wyboru lub ustawień uruchamia nowe liczenie.

| Scenariusz | Dokładny licznik przed = po | Przed | Po |
|---|---:|---:|---:|
| Mały wzorzec podróży | 3 | 4,9 ms | 13,6 ms |
| Duży wzorzec identyfikacji | 71 936 | 50,584 s | 7,644 s |
| Wszystkie 21 nowych wzorców | 142 591 | 98,521 s | 43,582 s |
| Pełny quiz przydawek | 182 651 | 89,495 s | 34,842 s |
| Istniejące „Trzy lubiane rzeczy” | 729 000 | 158,210 s | 68,5 ms |
| Istniejący prosty wzorzec czasownikowy | 2480 | 233,8 ms | 258,8 ms |
| Stara przydawka podmiotowa (mediana trzech prób) | 6480 | 1,125 s | 1,280 s |
| Cały istniejący quiz Gramatyka | nie uzyskano | >180 s | >180 s |

Długie pełne pomiary są osobną diagnostyką, nie zaliczeniem limitu 12 s. Wzorzec identyfikacji i stary wzorzec trzech rzeczowników kończą się teraz w tym limicie; wszystkie nowe/cały quiz przydawek nadal nie. Cały stary quiz Gramatyka pozostaje nierozwiązanym kosztownym przypadkiem enumeracji, bez publikowania częściowej sumy. Jest to ogólna optymalizacja, sprawdzona na istniejącym wzorcu bez przydawek, bez wyjątków zależnych od ID lekcji.

Początkowe mediany: ładowanie 200,7 → 169,1 ms; walidacja 7,362 → 7,969 s. Tych ścieżek nie optymalizowano. Ze względu na zmienność czasu startu wykonano dodatkowo dziewięć par świeżych procesów w kolejności AB/BA: mediany pierwszego pytania dla jednego/wszystkich nowych/pełnego quizu przydawek to **30,3 → 34,3 / 53,5 → 63,0 / 59,6 → 65,0 ms**. Zakresy nakładają się (dla pełnego quizu: 50,8–82,5 / 58,1–79,8 ms), ale wyższych median nie ukryto jako przyspieszenia ani dowodu zerowej regresji opóźnienia. Kod pierwszego generowania pozostaje bez zmian; kompletne pytania dla ustalonego ziarna i stan RNG są zgodne. Wolniejsze pojedyncze pomiary starego wzorca sprawdzono dodatkowo w jednym procesie w pięciu naprzemiennych parach: ścieżka kanoniczna 1,386 s, zapasowa ścieżka nowego licznika 1,400 s, identyczne 6480 możliwości, około 1% narzutu wyboru ścieżki. Surowe wyniki pozostały w istniejącym JSON; nie są gwarancją opóźnień urządzenia.

Lokalnie przeszło 1179 testów aplikacji i 356 subtestów; 16 natywnych testów Tk pominięto z powodu braku wyświetlacza. Walidacja Data i pytań przeszła; uruchomiono 133 testy Data, siedem pominięto. Porównanie wydania zachowało 76 kompletnych starych par; każdy XML pozostał identyczny względem headów sprzed optymalizacji. Pełne CI Windows jest podlinkowane w PR; sprawdzenie systemowego DPI i fizycznego urządzenia pozostaje manualne.

Odtworzenie z katalogu repozytorium Content: istniejący `tools/benchmark_relative_lesson26_review.py --optimization --before-kotomi BEFORE --kotomi AFTER --data CONTENT --diagnostic-timeout 180 --output docs/validation/relative_lesson26_review_performance.json`. Ścieżki wskazują osobne, zgodne checkouty. Opcjonalny limit diagnostyczny 180 s jest oddzielony od niezmienionego limitu procesu 12 s. Trzy naprzemienne pomiary projektu/pierwszego pytania w świeżych procesach i jeden pomiar licznika na scenariusz używają identycznego Content/interpretera, bez równoległych benchmarków. Ładowanie, walidacja, analiza, statystyki i generowanie są raportowane osobno. Nie dodano progu wydajności do CI.

Niezależne ograniczone fixtury porównują rozwinięte grupy wyborów z pełną enumeracją, kompletne reprezentatywne pary PL/JA, duplikaty tekstu/kontekstów, cztery formy, stałe progressive/desiderative, wiele argumentów, rekcję/uzgodnienie, countery, kompozycje, filtry, zmiany ustawień, danych rzeczowników/form i starszego hosta oraz quiz rzeczownikowy bez przydawek. Deterministyczna asercja sprawdza mniejszą liczbę wywołań renderera, bez zależności od szybkości sprzętu. Nadal obowiązują istniejące testy silnika, quizów, postępu i Mobile. Dotychczasowe narzędzie porównawcze sprawdza też stare pary i niezmienione XML; opóźnienia produkcyjne mierzy wyłącznie opcjonalny skrypt wydania, bez kopiowania Content do fixtur.

## Układ konfiguracji quizów Windows

`SpecializedQuizSetupDialog` obsługuje Grammar (w tym wszystkie przydawki), czasowniki, przymiotniki i dostępność. Istniejący notebook zawiera teraz ograniczone przestrzenią strony `VerticalScrolledFrame` dla ustawień, form i wzorców, z lokalną obsługą kółka oraz zawijaniem etykiet checkboxów. Osobny dolny wiersz utrzymuje przyciski poza przewijaną zawartością. Launcher lekcji, konfiguracja koniugacji i zdań mają ten sam początkowy rozmiar 720×650, elastyczną część środkową i stałą stopkę; zachowano istniejące ograniczenie do obszaru roboczego monitora. Koniugacja używa tego samego kontenera; zdania zachowują przewijany PatternPicker i Listboxy form. Nie zmieniono zapisu ustawień ani reguł zaznaczania. Układ Mobile pozostaje bez zmian.

`test_quiz_setup_scrolling.py` używa syntetycznych ustawień v1 i rzeczywistych kontrolek Tk: 23 wzorce, 35 form, pojedynczy wzorzec, kółko/zaznaczanie na końcu listy, resize, granice stopki i zapis/odczyt ustawień. Obejmuje też okna konfiguracji lekcji. Przy dostępnym ekranie sprawdzane są skale fontu 100/125/150%. Środowisko bez wyświetlacza pomija testy natywne, zamiast deklarować wizualną weryfikację na podstawie atrap. Nadal potrzebne jest manualne sprawdzenie Windows przy 1366×768 i Full HD, skalowaniu systemowym 125/150% oraz różnych monitorach/paskach zadań: skala fontu Tk nie zastępuje testu DPI systemu.


## Finalny review i rzeczywiste otwieranie menu (2026-10-24)

Punktem odniesienia tej kontynuacji są Kotomi `b12de81` i Content `ab18c0a`; całe PR-y porównano także z ich `main`. Doprecyzowanie użytkownika wskazało **KotomiMobile uruchomione na Windows (Kivy)**. Natywny `QuizLauncherFrame` Tk nie wywołuje statystyk ani walidacji podczas otwierania konfiguracji. Jego import, profil i ustawienia zajęły w profilowaniu 94 ms przy pierwszym wejściu i 29 ms przy kolejnym, bez pomiaru rysowania Tk.

W Kivy rzeczywistą przyczyną wielosekundowego loadingu była pełna walidacja projektu podczas budowy kontrolerów verbs/adjectives/availability. Start ponownie wczytuje i waliduje projekt, więc pierwsza walidacja nie była potrzebna do pokazania ustawień. Launcher przekazuje teraz jeden świeżo wczytany projekt wszystkim tym quizom, zgodnie z istniejącą ścieżką profili Grammar. `reload_engine` czasowników i przymiotników konsumuje ten projekt tylko raz; późniejszy Start/reload nadal czyta i waliduje aktualne dane. Błędy wymagające pełnej walidacji mogą więc zostać pokazane po Start zamiast przy wejściu do konfiguracji. Nie dodano cache projektu pomiędzy otwarciami ani zmiany reguł walidacji. Odświeżanie importów zachowano dla aktualizowanych pakietów. W `open_quiz` usunięto dwie pauzy po 160 ms i oczekiwanie na końcową animację: popup znika po zbudowaniu ekranu. Loading pozostaje podczas rzeczywistej pracy, bez nowych sztucznych procentów.

Pomiary używają rzeczywistego Kivy 2.3.1, SDL offscreen i Mesa na Linuksie, bez atrap widgetów. Trzy pary świeżych procesów w kolejności AB/BA, po dwa otwarcia w procesie, bez równoległych testów. Mierzone jest wywołanie callbacku menu do gotowego ekranu; fizyczne dostarczenie kliknięcia przez Windows nie jest mierzone. Osobno zapisano import/profil, odczyt projektu, analizę, ustawienia, silnik, budowę widgetów, najdłuższą klatkę UI i przejście do ustawień. Czasy etapów są zagnieżdżone, nie należy ich sumować.

| Quiz | Pierwsze wejście przed → po | Ponowne wejście przed → po |
|---|---:|---:|
| Czasowniki | 4485 → 235 ms | 4600 → 218 ms |
| Przymiotniki | 4435 → 215 ms | 4856 → 226 ms |
| Dostępność | 4406 → 218 ms | 4705 → 232 ms |
| Przydawki | 718 → 277 ms | 782 → 259 ms |
| Gramatyka | 703 → 232 ms | 738 → 253 ms |

W przykładowym pierwszym wejściu do czasowników walidacja zajmowała 3539 ms, silnik 3612 ms, a najdłuższa klatka UI 3712 ms. Po zmianie nie ma walidacji na tej ścieżce, silnik zajmuje 0,18 ms, a najdłuższa klatka 122 ms. To pomiar tego środowiska, nie gwarancja opóźnienia Windows.

Profil licznika całego quizu wykazał 83 809 renderowań oraz powtarzane sprawdzenia tych samych par rola/słowo/rzeczownik. `_SearchCandidates.role_pairs` zapamiętuje najwyżej 4096 dokładnych wyników istniejącego predykatu w jednym wyszukiwaniu, dla ustalonego projektu, analizy i formy. Klucz zawiera oba sloty i oba ID; zależności całego zdania nadal sprawdza solver. Nie przechowuje zdań, nie przeżywa operacji ani edycji i nie łączy wyników różnych form. Dla jednego rzeczownika cache par nie jest używany. `iter_counted_possibilities` odrzuca niepasujące przypadki przed analizą niezależności. Zachowano poprzednie mnożenie niezależnych domen i wszystkie fallbacki, w tym dokładną enumerację metryk Symulatora.

| Licznik | Identyczny wynik | Przed → po tej kontynuacji |
|---|---:|---:|
| Osoba i dopełnienie, mediana 3 par | 71 936 | 2,511 → 2,342 s |
| Wszystkie 21 nowych, jedna para | 142 591 | 10,127 → 9,470 s |
| Cały quiz przydawek, mediana 3 par | 182 651 | 13,312 → 12,723 s |
| Stara przydawka podmiotowa, mediana 3 par | 6480 | 524 → 463 ms |
| Sam czasownik, mediana 3 par | 2480 | 85,4 → 87,3 ms |
| Trzy lubiane rzeczy, jedna para | 729 000 | 34,8 → 33,4 ms |

Zysk licznika jest umiarkowany. Dla prostego czasownika pozostała różnica +1,9 ms; nie przedstawiamy jej jako dowodu przyspieszenia ani zerowego narzutu. Nie porównujemy bezpośrednio tych czasów z historycznym pomiarem 34,8 s na innym wykonaniu środowiska. Pełna Gramatyka nadal przekracza limit procesu 12 s, bez zwracania częściowego wyniku. Sprzężone domeny, liczniki i duże produkty słów pozostają kosztowne; dalsze ich mnożenie wymagałoby szerszego dowodu niezależności. Osobne pomiary Start nadal wynoszą około 4,2–4,6 s, głównie przez zachowaną pełną walidację na wątku UI. Usunięcie opóźnienia menu nie jest równoznaczne z usunięciem tego kosztu.

Osobna próbka samego pierwszego pytania dała 29,7 → 35,4 ms dla całego quizu, 19,6 → 18,3 ms dla jednego wzorca i 1,10 → 1,10 ms dla prostego czasownika. Pojedyncza próbka nie dowodzi zerowego narzutu; kompletne wyniki i RNG pozostają zgodne.

Dodatkowy review i testy obejmują przechodni łańcuch zależności trzech rzeczowników z czwartą niezależną domeną, kompletne pary i wybory przy włączonym/wyłączonym memo, cztery formy, odświeżenie po edycji, pełne eligible, konteksty i identyczny tekst. Zachowano istniejące testy progressive/desiderative, wielu argumentów, rekcji, uzgodnienia, counterów, kompozycji, filtrów i RNG. Porównanie wydania potwierdziło 76 niezmienionych starych par PL/JA. **Żaden XML ani tłumaczenie leksykalne nie zmieniły się podczas tej kontynuacji.** Oryginalna implementacja lekcji w całym PR dodaje słowa/formy i wzorce; nie należy mylić tego zakresu z optymalizacją.

Kontrolery Kivy mają nowe ograniczone testy jednorazowego przekazania projektu i braku walidacji przed Start, dla obu języków instrukcji i ponownego wczytania. Istniejący test kolejki launchera sprawdza teraz natychmiastowe zamknięcie popupu po gotowym ekranie zamiast celowego oczekiwania na animację. To zamierzona zmiana prezentacji, nie zmiana oczekiwań gramatycznych. Pakiety verbs/adjectives/availability mają wersję 1.1.3 i identyczne źródła w obu repozytoriach; starszy host nadal działa przez dotychczasową ścieżkę bez preloaded_project. Aktualne wyniki pełnego CI są podlinkowane w PR.

### Windows GUI i pozostałe ograniczenia

Zachowano wspólne przewijane okna Tk z poprzedniego commita, stopki poza listami oraz odtwarzanie skalowania w testach. W rzeczywistym Kivy offscreen sprawdzono przewijanie do kontrolek, odwracalne zaznaczenie, resize i granice przycisków ustawień dla czasowników i 23 przydawek przy 1366×768, 1093×614, 911×512 i 1920×1080. Te rozmiary logiczne **nie są testem systemowego DPI 125/150%**. Natywne testy Tk uruchamia Windows CI; lokalnie nie ma wyświetlacza Tk. Nie wykonano fizycznego kliknięcia/kółka myszy ani testu urządzenia Android.

- P1, weryfikacja wydania: sprawdzić użytkownikowy KotomiMobile na Windows po aktualizacji aplikacji i pakietów, przy 1366×768/Full HD i DPI 125/150%. Kod i pomiar Kivy potwierdzają naprawę menu, lecz zielone CI nie potwierdza zachowania sterownika ekranu i DPI. To pozostała bramka przed bezwarunkowym zatwierdzeniem merge.
- P2, istniejący koszt Start: około 4 s pełnej walidacji na UI. Można odłożyć oddzielną poprawkę po akceptacji tego opóźnienia; nie powstaje nowa regresja i nie osłabiono walidacji.
- P2, dokładne statystyki: duży quiz przydawek nadal około 13 s, pełna Gramatyka nadal kosztowna. Obliczenia pozostają poza UI i są dokładne; można odłożyć dalszą optymalizację bez zmiany dostępnych zdań.

Reprodukcja: `tools/benchmark_relative_lesson26_review.py --worker menu --selection verbs --kotomi KOTOMI --data CONTENT`. Opcjonalne `--menu-start` i `--menu-layout` mierzą osobno Start i sprawdzają układ. Na Linuksie użyto `KIVY_NO_ARGS=1 SDL_VIDEODRIVER=offscreen`; na Windows należy uruchomić z rzeczywistym backendem. Wyniki tej kontynuacji są w sekcji `final_review` istniejącego raportu JSON. W CI nie dodano benchmarków ani progów czasowych.

W końcowej kontroli ekranu Kivy wykryto też wyświetlanie kluczy `specialized.pattern...` zamiast nazw wzorców Content. Wspólna prezentacja Availability/Grammar używa teraz etykiety z profilu, gdy brak tłumaczenia interfejsu; istniejące przetłumaczone nazwy zachowują pierwszeństwo. Poprawka dotyczy listy i podsumowania, nie ID, zaznaczeń ani zdań. Dodano niezależny test tej ścieżki. Powyższe pomiary wykonano przed tą poprawką samych etykiet.


## Audyt zakresu słów i odmiany (2026-10-25)

Rozszerzono `suki` i `hoshii` z `purchasable` na `concrete abstract`: słowa nie są ograniczone do zakupów. Ograniczenia konkretnego pytania nadal należą do patternu. `tomaru_stay` dopuszcza `place`, także nocleg poza budynkiem. Nie zmieniono tłumaczeń ani form czasowników.

Sprawdzono dziesięć nowych rzeczowników, dwa przymiotniki i dwa czasowniki. `tokoro`, `hotel`, `cake`, `watch` mają komplet few/many dla siedmiu przypadków. Uzupełniono taki komplet dla `hi` (dni, dniom, dniami, dniach) i `kuni` (kraje/krajów, krajom, krajami, krajach), bez sztucznego countera. Nazwy własne Poland/Japan/India i substancja wine nie otrzymują sztucznych form liczenia egzemplarzy. Brak countera nie oznacza braku polskiej odmiany.

Oba przymiotniki mają wszystkie 15 form z katalogu i odmianę dla obsługiwanych klas zgodności. Katalog nie obsługuje jeszcze klasy męskoosobowej liczby mnogiej; nie rozszerzono silnika w tym zadaniu. `tomaru_stay` ma 15 podstawowych form; `umareru` 14, bez sztucznej strony biernej. Progressive/desiderative pozostają opcjonalne. Poszerzenie kompatybilności może zwiększyć liczniki, dlatego wcześniejsze wyniki wydajności opisują poprzedni zestaw danych.

W edytorze Tk kategorię i klasę zgodności przeniesiono do rozwijanej sekcji Więcej ustawień, bezpośrednio nad profil relacji rzeczownika. Zapis danych i mechanizm wyboru pozostają bez zmian.
