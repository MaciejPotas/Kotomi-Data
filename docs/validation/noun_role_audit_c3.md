# Audyt ograniczeń rzeczowników C3

Baza danych: `ef338045ed383763db2cbf04aceea5b1b7ad1d69`. Baza Kotomi: `9d6d662228301dfb9d94524736e09dcc763b28cc`. Stan po: powiązane branche C3, Content 63.

Zbadano cały słownik: 122 czasowniki, 253 role i wszystkie 80 rzeczowników. Wystąpienia `nouns` obejmują także OR z `accepts`. Nie przywrócono `hitori`; Kategorie person i animal pozostają bez zmian; C3.1 zawęża cztery role target do person.

## Metryki

| Metryka | Przed | Po |
|---|---:|---:|
| Czasowniki | 122 | 122 |
| Wszystkie role | 253 | 253 |
| Role z nouns | 36 | 15 |
| Role z accepts | 108 | 122 |
| Kategorie zadeklarowane | 14 | 23 |
| Kategorie wybieralne | 12 | 21 |
| Kategorie użyte w rzeczownikach | 11 | 19 |
| Nowe kategorie | 0 | 9 |
| Zmienione rzeczowniki | 0 | 18 |
| Jawne listy pozostawione | 36 | 15 |
| Udokumentowane wyjątki w pozostawionych listach | nieklasyfikowane | 10 |
| Listy wymagające decyzji o sensach | nieklasyfikowane | 5 |
| Nowe kombinacje verb/role/noun | 0 | 19 |
| Usunięte kombinacje verb/role/noun | 0 | 35 |

Kategoria oznacza w metrykach osobno katalog, elementy wybieralne i rzeczywiście użyte. Kombinacja nie oznacza pytania: konteksty i formy mnożą realizacje. 22 z 36 pierwotnych list znika całkowicie; C3.1 dodaje ograniczony wyjątek kotaeru/target. Łącznie 30 ról jest zmodyfikowanych. Żadnego `government`, tekstu tłumaczenia, formy, identyfikatora/kolejności ról ani wzorca nie zmieniono.

## Końcowy przegląd target (C3.1)

Sprawdzono wszystkie 21 ról target. Pięć korekt jest jawnie zatwierdzonych w
istniejącym pliku decyzji i macierzy; pozostałe 248 ról zachowuje wyniki C3.
`kariru`, `kasu`, `morau`, `usowotsuku`: target `person animal → person`.
`kotaeru`: target `abstract → person` OR dokładne `email letter`.
Szczegółowe uzasadnienie każdej decyzji oraz ograniczenia perspektywy i tłumaczeń:
[PL](../pl/noun_role_categories_c3.md#c31-rola-target-i-kierunek-relacji),
[EN](../eng/noun_role_categories_c3.md#c31-target-and-relationship-direction).

Dodatkowe zmiany C3.1 względem poprzedniego C3:

- Usunięto `inu` i `tori` dla target każdego z czterech czasowników interpersonalnych (8 par).
- `kotaeru/target`: usunięto 24 abstrakty; dodano 8 osób oraz `email`, `letter` (10 par).
- Dokładne ID wszystkich zmian są w `reviewed_target_roles` oraz `all_role_pairs` w JSON.
- Razem z zachowaną migracją C3: **19 dodatków / 35 usunięć**, nie historyczne 9/3.
- Kategorie placówek, DSL, solver, government, tłumaczenia i produkcyjne wzorce pozostają bez zmian.
- Produkcyjne wzorce nie wybierają target; fixture dowodzi obsługi dwóch argumentów,
  ale publikacja takiego wzorca wymaga polskich ramek/tekstów i określenia perspektywy.
- Manifest Content nadal ma format 2 i rewizję 63; odświeżono hash zmienionego verbs.xml.

## Poprawki po review C3 (poprzedni etap)

- P1: Content 63 wymaga manifestu aktualizacji formatu 2. Starszy klient odrzuca go
  przed pobraniem plików; nowy nadal obsługuje format 1 i Content 62. Zachowano
  istniejącą walidację izolowanego snapshotu i rollback. Macierz uruchamia rzeczywiste
  aktualizatory obu checkoutów na niezależnym fixture. Nie podniesiono historycznego,
  ignorowanego `min_kotomi_version`; poprawiono błędne zapewnienia w dokumentacji.
- P2: istniejący plik decyzji przechowuje dokładny `target` oraz jawne `added`/`removed`.
  Walidator oddziela decyzje, XML i wyniki silnika; odrzuca duplikaty, dryf atrybutów,
  zmianę government/kolejności i niezaplanowane pary także w pozostałych rolach.
  Definicje wcześniejszych kategorii muszą pozostać zgodne z bazą. Regeneracja raportu
  nie aktualizuje decyzji. Słowniki i zatwierdzona migracja pozostają niezmienione.
- P2/P3: fixture charakteryzuje obecne granice dla drzwi, okna, koszuli i spodni.
  Nie wprowadzono wielokrotnej klasyfikacji. Przewodniki PL/EN opisują możliwość
  użycia istniejącego OR oraz mały, opcjonalny etap C4 dla cech funkcjonalnych.
- P3: rozszerzono test Studio o zachowanie wszystkich niezwiązanych plików przy
  zapisie rzeczownika i czasownika; wykorzystano dotychczasowe testy uzgodnienia,
  przydawek, serializacji i IntelliSense. Nie dodano wyjątków dostępu do Content.
- Wydajność: profil wykazał koszt tymczasowych zbiorów. Jedno wyrażenie w istniejącym
  `role_matches` używa teraz `isdisjoint`, zachowując OR i kontrolę całego łańcucha
  przodków. Nie ma nowego matchera ani cache. Wszystkie pomiary, także wcześniejsze
  przekroczenia, są zachowane w JSON wydajności.

Bezpieczna publikacja wymaga formatu 2, zielonego CI obu PR-ów oraz zaliczonych
bramek C3. Publikacja Content 63 w formacie 1 jest zabroniona. Nie wykonano merge
ani publikacji wydania. Szczegóły architektury aktualizacji i zakresu C4:
[PL](../pl/noun_role_categories_c3.md), [EN](../eng/noun_role_categories_c3.md).

## Kategorie i decyzja architektoniczna

[Pełny przewodnik PL](../pl/noun_role_categories_c3.md), [English guide](../eng/noun_role_categories_c3.md). Dziedziczenie już istniało. Wprowadzono 9 semantycznych podkategorii bez zmiany algorytmu. 5 przypadków wieloznacznych pozostawiono jawnie do osobnej decyzji, bez maskowania ich jako rozwiązanych.

## Komplet wystąpień nouns według charakteru problemu

W kolumnie kategorii podano wszystkie ID z pierwotnego nouns. Pełne dopuszczane zbiory przed/po dla każdej roli, także bez nouns, znajdują się w [macierzy JSON](noun_role_audit_c3.json), sekcja `all_role_pairs`.

### Pojemniki

| Czasownik / rola | Przed: accepts; nouns i kategorie | Po | Nowa kategoria | Decyzja / uzasadnienie |
|---|---|---|---|---|
| `akeru/object` (otwierać) | accepts: ∅; bag: thing, box: thing | accepts: closable_container; nouns: ∅ | closable_container | **category**. Zamykany pojemnik jest trwałą cechą, wspólną dla otwierania i zamykania. Zwykłe container byłoby za szerokie (np. miska). |
| `aku/subject` (otwierać się) | accepts: ∅; bag: thing, box: thing | accepts: closable_container; nouns: ∅ | closable_container | **category**. Jak akeru: podmiot musi być zamykanym pojemnikiem. Zachowano bag i box oraz brak government. |
| `ireru/target` (wkładać) | accepts: ∅; bag: thing, box: thing, room: place | accepts: container; nouns: room | container | **retained_exception**. container obejmuje miejsca przechowywania rzeczy. room jest dodatkowym celem przestrzennym; place dopuściłoby także plażę/głębię, więc zachowano room jako wyjątek zakresu. |
| `shimaru/subject` (zamykać się) | accepts: ∅; bag: thing, box: thing | accepts: closable_container; nouns: ∅ | closable_container | **category**. Zamykanie się dotyczy zamykanych pojemników. Nie dopuszczamy otwartej miski; mapy uzgodnienia C1/C2 pozostają identyczne. |
| `shimeru/object` (zamykać) | accepts: ∅; bag: thing, box: thing | accepts: closable_container; nouns: ∅ | closable_container | **category**. Zamykać można pojemniki z zamknięciem. Kategoria container pozostaje szersza na potrzeby wkładania. |

### Czynności wymagające rozróżnienia sensu

| Czasownik / rola | Przed: accepts; nouns i kategorie | Po | Nowa kategoria | Decyzja / uzasadnienie |
|---|---|---|---|---|
| `hajimeru/object` (zaczynać) | accepts: ∅; shigoto: availability_reason, keikaku: availability_reason, yotei: availability_reason, meal: food | accepts: ∅; nouns: shigoto keikaku yotei meal | nie | **deferred_sense_review**. shigoto/meal to działania, keikaku/yotei to plany i ich realizacja. Nie istnieje jedna wąska kategoria w aktualnej jednoosiowej klasyfikacji. Lista pozostaje ograniczeniem zakresu sensu, nie modelem wszystkich przyszłych czynności. Wymaga dalszej decyzji przed bezpiecznym uogólnieniem. |
| `owaru/subject` (kończyć się) | accepts: ∅; shigoto: availability_reason, meal: food, yotei: availability_reason | accepts: ∅; nouns: shigoto meal yotei | nie | **deferred_sense_review**. Kończy się praca/posiłek, a yotei wymaga znaczenia zaplanowanych zajęć. food dopuściłoby jabłko, availability_reason pieniądze. Zachowano listę do rozdzielenia zdarzeń i planów. |
| `suru/object` (robić) | accepts: ∅; shigoto: availability_reason, yakusoku: abstract, keikaku: availability_reason, yotei: availability_reason, youji: abstract | accepts: ∅; nouns: shigoto yakusoku keikaku yotei youji | nie | **deferred_sense_review**. Suru z pracą, obietnicą, planem i sprawą jest zależne od konstrukcji. Wspólne abstract jest za szerokie (życie, smak, jutro), a jedna nowa kategoria wymagałaby przecięcia obecnych gałęzi. Pozostaje jawny zakres, z jawnym długiem semantycznym. |
| `tsuzukeru/object` (kontynuować) | accepts: ∅; shigoto: availability_reason, keikaku: availability_reason, yotei: availability_reason, music: media, song: media | accepts: ∅; nouns: shigoto keikaku yotei music song | nie | **deferred_sense_review**. Kontynuować pracę/realizację planu/wykonanie muzyki. To różne odczytania zdarzeniowe, nie dowolne abstrakty lub media. Wymaga doprecyzowania sensów; nie rozszerzamy automatycznie na głos ani przyszłe gatunki muzyczne. |

### Pieniądze

| Czasownik / rola | Przed: accepts; nouns i kategorie | Po | Nowa kategoria | Decyzja / uzasadnienie |
|---|---|---|---|---|
| `harau/object` (płacić) | accepts: ∅; okane: availability_reason | accepts: money; nouns: ∅ | money | **category**. Płacić pieniądze, nie dowolny powód dostępności. money zachowuje przodka availability_reason. |
| `ireru/object` (wkładać) | accepts: person animal food drink text media vehicle thing; okane: availability_reason | accepts: person animal food drink text media vehicle thing money; nouns: ∅ | money | **category**. Pieniądze można wkładać, a dopisanie money zachowuje istniejące OR. |
| `kariru/object` (pożyczać od kogoś) | accepts: text vehicle thing; okane: availability_reason | accepts: text vehicle thing money; nouns: ∅ | money | **category**. Pieniądze są regularnym przedmiotem pożyczania. money jest alternatywą wobec dotychczasowych accepts; nie ich zawężeniem. |
| `motteiku/object` (zabierać) | accepts: food drink text media vehicle thing; okane: availability_reason | accepts: food drink text media vehicle thing money; nouns: ∅ | money | **category**. Pieniądze są regularnym przedmiotem zabierania. Dotychczasowe accepts pozostają. |
| `mottekuru/object` (przynosić) | accepts: food drink text media vehicle thing; okane: availability_reason | accepts: food drink text media vehicle thing money; nouns: ∅ | money | **category**. Pieniądze są regularnym przedmiotem przynoszenia. Dotychczasowe accepts pozostają. |
| `nakusu/object` (gubić) | accepts: text vehicle thing; okane: availability_reason | accepts: text vehicle thing money; nouns: ∅ | money | **category**. Pieniądze można gubić. Nie wolno dopuścić wszystkich availability_reason (np. planu). |
| `ageru_give/object` (dawać komuś) | accepts: food drink text media vehicle thing; okane: availability_reason | accepts: food drink text media vehicle thing money; nouns: ∅ | money | **category**. Pieniądze można dawać; nie są leksykalnym wyjątkiem. Zachowano wszystkie inne kategorie. |
| `kaesu/object` (oddawać, zwracać) | accepts: text vehicle thing; okane: availability_reason | accepts: text vehicle thing money; nouns: ∅ | money | **category**. Pieniądze można zwracać, bez rozszerzania na czas/pracę. |
| `kasu/object` (pożyczać komuś) | accepts: text vehicle thing; okane: availability_reason | accepts: text vehicle thing money; nouns: ∅ | money | **category**. Pieniądze można pożyczać komuś; istniejące kategorie i government pozostają. |
| `kureru/object` (dawać mi, nam) | accepts: food drink text media vehicle thing; okane: availability_reason | accepts: food drink text media vehicle thing money; nouns: ∅ | money | **category**. Pieniądze można otrzymywać w znaczeniu dawania mi/nam; nie są wyjątkiem. |
| `morau/object` (otrzymywać) | accepts: food drink text media vehicle thing; okane: availability_reason | accepts: food drink text media vehicle thing money; nouns: ∅ | money | **category**. Pieniądze można otrzymywać; brak powodu do kodowania ich po ID. |

### Teksty i wieloznaczność

| Czasownik / rola | Przed: accepts; nouns i kategorie | Po | Nowa kategoria | Decyzja / uzasadnienie |
|---|---|---|---|---|
| `hiraku/object` (otwierać) | accepts: ∅; book: text, manga: text, newspaper: text, email: text, note: text, box: thing, school: place | accepts: text; nouns: box school | nie | **retained_exception**. Wszystkie 6 tekstów pasuje do otwierania/rozkładania tekstu lub dokumentu, w tym nowy letter. box jest fizycznym otwieraniem, school uruchamianiem placówki. Nie uogólniamy tych dodatkowych znaczeń na każdy pojemnik i budynek. |

### Budynki i placówki

| Czasownik / rola | Przed: accepts; nouns i kategorie | Po | Nowa kategoria | Decyzja / uzasadnienie |
|---|---|---|---|---|
| `kayou/target` (uczęszczać) | accepts: ∅; school: place, taiikukan: place | accepts: education_facility sports_facility; nouns: ∅ | education_facility, sports_facility | **category**. Uczęszczanie do placówki edukacyjnej lub sportowej jest spójne z polskim tłumaczeniem. Japońskie kayou może także oznaczać regularne wizyty w szpitalu, ale polskie uczęszczać nie uzasadnia dodania wszystkich budynków. |
| `tateru/object` (budować) | accepts: ∅; home: place, school: place, taiikukan: place | accepts: building; nouns: ∅ | building | **category**. Budowanie fizycznego budynku: dodano wszystkie pozostałe jednoznaczne budynki/placówki w obecnym słowniku. station, mise i ginkou są tutaj interpretowane jako obiekty, nie organizacje lub usługi. room, daidokoro, jimusitsu, naka i oku to pomieszczenia/relacje przestrzenne; park, kaigan, bazaaru nie są budynkami. |

### Muzyka

| Czasownik / rola | Przed: accepts; nouns i kategorie | Po | Nowa kategoria | Decyzja / uzasadnienie |
|---|---|---|---|---|
| `keikosuru/object` (trenować) | accepts: ∅; music: media, song: media | accepts: music; nouns: ∅ | music | **category**. media zawiera także koe (głos), dlatego nie wolno użyć całego media. music zachowuje obecne music i song. Polskie trenować muzykę/piosenkę jest niezręczne już w bazie; ta migracja nie dodaje takich par i nie zmienia tłumaczeń. Do osobnego przeglądu sensów. |
| `renshuusuru/object` (ćwiczyć) | accepts: ∅; music: media, song: media | accepts: music; nouns: ∅ | music | **category**. Ćwiczenie muzyki/piosenki jest węższe od wszystkich mediów; sam głos nie jest utworem ani muzyką. Instrumenty i ćwiczenia słuchowe są innymi osiami, nie dopisujemy ich do music. |

### Rozbieżne znaczenia

| Czasownik / rola | Przed: accepts; nouns i kategorie | Po | Nowa kategoria | Decyzja / uzasadnienie |
|---|---|---|---|---|
| `kesu/object` (wyłączać) | accepts: ∅; television: thing, email: text, note: text | accepts: ∅; nouns: television | nie | **retained_exception**. 消す z email/note znaczy usuwać/kasować, nie wyłączać. Usunięto obie pary zamiast zmieniać wszystkie tłumaczenia. Zostaje television w istniejącym znaczeniu telewizji/odbiornika; nie klasyfikujemy całego medium jako urządzenia. |
| `ukeru/object` (odbierać) | accepts: ∅; shigoto: availability_reason | accepts: ∅; nouns: shigoto | nie | **deferred_sense_review**. shigoto wo ukeru to przyjąć pracę/zlecenie. Obecne odbierać jest nieprecyzyjne. Nie poszerzamy na całą pracę/czynności bez uzgodnienia tłumaczeń; pozostawiono jawny zakres i wskazano dług. |

### Wyjątki leksykalne

| Czasownik / rola | Przed: accepts; nouns i kategorie | Po | Nowa kategoria | Decyzja / uzasadnienie |
|---|---|---|---|---|
| `kiru/object` (nosić) | accepts: ∅; clothes: thing | accepts: ∅; nouns: clothes | nie | **retained_exception**. clothing obejmuje także przyszłe spodnie; japońskie kiru nie zastępuje haku ani kaburu. Zachowano ogólne clothes. Docelowo potrzeba rozróżnienia sposobu noszenia lub sensów; nie przypisujemy ogólnemu clothes fałszywej cechy górnej części ciała. |
| `tojiru/object` (zamykać) | accepts: ∅; book: text, manga: text, newspaper: text, box: thing | accepts: ∅; nouns: book manga newspaper box | nie | **retained_exception**. Obecne book/manga/newspaper to zamykane/składane teksty, box to inny fizyczny obiekt. Sam text dodałby letter/email/note, a container także otwarte naczynia. Nowa kategoria tworzona tylko z tych ID nie rozwiązałaby kwestii sensów. Zachowano listę. |
| `tsukeru/object` (włączać) | accepts: ∅; television: thing | accepts: ∅; nouns: television | nie | **retained_exception**. W znaczeniu włączać obecny television jest jedynym nazwanym przypadkiem. thing byłoby błędne, a klasyfikacja telewizji jako urządzenia usunęłaby rozróżnienie medium/odbiornik. Zostaje wyjątek do audytu sensu hasła. |
| `sukuu/object` (ratować) | accepts: person animal; inochi: abstract | accepts: person animal; nouns: inochi | nie | **retained_exception**. Ratować życie to rzeczywiste połączenie leksykalne poza person/animal. abstract dodałoby nonsens, smak i jutro. Pozostawiono inochi w alternatywie OR. |

### Odzież

| Czasownik / rola | Przed: accepts; nouns i kategorie | Po | Nowa kategoria | Decyzja / uzasadnienie |
|---|---|---|---|---|
| `nugu/object` (zdejmować) | accepts: ∅; clothes: thing, bag: thing | accepts: clothing; nouns: ∅ | clothing | **category**. Odzież można zdejmować. Torba nie jest odzieżą, a bag wo nugu nie jest zwykłą konstrukcją zdejmowania torby. Usunięto bag. |
| `sentakusuru/object` (prać) | accepts: ∅; clothes: thing | accepts: clothing; nouns: ∅ | clothing | **category**. Prać odzież; kategoria jest przydatna również do zdejmowania. Nie obejmuje automatycznie toreb, urządzeń ani akcesoriów. |

### Czas

| Czasownik / rola | Przed: accepts; nouns i kategorie | Po | Nowa kategoria | Decyzja / uzasadnienie |
|---|---|---|---|---|
| `sugosu/object` (spędzać) | accepts: ∅; jikan: availability_reason | accepts: duration; nouns: ∅ | duration | **category**. duration oznacza odcinek czasu, nie datę/plan. jikan zachowuje availability_reason; ashita, dni tygodnia i shuumatsu nie zostają sztucznie przeniesione do tej gałęzi. |

### Wyjątki kontekstowe

| Czasownik / rola | Przed: accepts; nouns i kategorie | Po | Nowa kategoria | Decyzja / uzasadnienie |
|---|---|---|---|---|
| `teishutsusuru/object` (składać) | accepts: ∅; book: text, note: text, keikaku: availability_reason | accepts: ∅; nouns: book note keikaku | nie | **retained_exception**. Przedmiotem złożenia jest dokument/praca do przedłożenia, nie każdy tekst (np. gazeta). Odbiorca musi pełnić odpowiednią funkcję: nie każda osoba i nie każda placówka. Nie ma obecnie kategorii funkcjonalnej opisującej oba konteksty; zachowano listy zamiast fałszywej klasyfikacji nauczyciela lub wszystkich tekstów. |
| `teishutsusuru/target` (składać) | accepts: ∅; teacher: person, school: place | accepts: ∅; nouns: teacher school | nie | **retained_exception**. Przedmiotem złożenia jest dokument/praca do przedłożenia, nie każdy tekst (np. gazeta). Odbiorca musi pełnić odpowiednią funkcję: nie każda osoba i nie każda placówka. Nie ma obecnie kategorii funkcjonalnej opisującej oba konteksty; zachowano listy zamiast fałszywej klasyfikacji nauczyciela lub wszystkich tekstów. |

## Powtarzające się listy

| Lista | Role | Wniosek |
|---|---|---|
| bag, box | akeru/object, aku/subject, shimaru/subject, shimeru/object | closable_container, a dla celu wkładania szersze container |
| okane | harau/object, ireru/object, kariru/object, motteiku/object, mottekuru/object, nakusu/object, ageru_give/object, kaesu/object, kasu/object, kureru/object, morau/object | money zamiast 10 wyjątków OR i samodzielnego harau |
| music, song | keikosuru/object, renshuusuru/object | music zamiast media zawierającego również głos |
| clothes | kiru/object, sentakusuru/object | clothing dla prania; kiru zostaje wyjątkiem ze względu na sposób noszenia |

## Przegląd wszystkich rzeczowników

| ID | Tłumaczenie | Przed | Po |
|---|---|---|---|
| bag | torba | thing | closable_container |
| book | książka | text | text |
| box | pudełko | thing | closable_container |
| car | samochód | vehicle | vehicle |
| clothes | ubranie | thing | clothing |
| coffee | kawa | drink | drink |
| daidokoro | kuchnia | place | place |
| email | mail | text | text |
| friend | przyjaciel | person | person |
| fune | łódź | vehicle | vehicle |
| gohan | ryż | food | food |
| home | dom | place | building |
| inu | pies | animal | animal |
| jikan | czas | availability_reason | duration |
| keikaku | plan działania | availability_reason | availability_reason |
| kaigan | plaża | place | place |
| letter | list | text | text |
| manga | manga | text | text |
| meal | posiłek | food | food |
| mother | mama | person | person |
| motorcycle | motocykl | vehicle | vehicle |
| music | muzyka | media | music |
| newspaper | gazeta | text | text |
| note | notatka | text | text |
| okane | pieniądze | availability_reason | money |
| pan | chleb | food | food |
| park | park | place | place |
| ringo | jabłko | food | food |
| room | pokój | place | place |
| school | szkoła | place | education_facility |
| shigoto | praca | availability_reason | availability_reason |
| sister | siostra | person | person |
| song | piosenka | media | music |
| station | stacja | place | building |
| sushi | sushi | food | food |
| taiikukan | sala gimnastyczna | place | sports_facility |
| tea | herbata | drink | drink |
| teacher | nauczyciel | person | person |
| television | telewizja | thing | thing |
| tori | ptak | animal | animal |
| water | woda | drink | drink |
| yakusoku | obietnica | abstract | abstract |
| yotei | plan | availability_reason | availability_reason |
| youji | sprawa do załatwienia | abstract | abstract |
| bazaaru | bazar | place | place |
| roujin | starzec | person | person |
| mise | sklep | place | building |
| naka | wnętrze | place | place |
| koe | głos | media | media |
| hito | osoba | person | person |
| oku | głębia | place | place |
| ashita | jutro | abstract | abstract |
| kagi | klucz | thing | thing |
| inochi | życie | abstract | abstract |
| riyuu | powód | abstract | abstract |
| hanashi | opowieść | abstract | abstract |
| saisho | początek | abstract | abstract |
| detarame | nonsens | abstract | abstract |
| pencil | ołówek | thing | thing |
| paper_sheet | kartka papieru | thing | thing |
| getsuyoubi | poniedziałek | abstract | abstract |
| kayoubi | wtorek | abstract | abstract |
| suiyoubi | środa | abstract | abstract |
| mokuyoubi | czwartek | abstract | abstract |
| kinyoubi | piątek | abstract | abstract |
| doyoubi | sobota | abstract | abstract |
| nichiyoubi | niedziela | abstract | abstract |
| tatemono | budynek | place | building |
| yuubinkyoku | poczta | place | building |
| byouin | szpital | place | building |
| biru | biurowiec | place | building |
| jimusitsu | biuro | place | place |
| eigakan | kino | place | building |
| ginkou | bank | place | building |
| aji | smak | abstract | abstract |
| programmer | programista | person | person |
| kikitori | rozumienie ze słuchu | abstract | abstract |
| shuumatsu | weekend | abstract | abstract |
| fukushuu | powtórka | abstract | abstract |
| madogiwazoku | pracownik odsunięty na boczny tor | person | person |

Przejrzano również niezmienionych członków. Pomieszczenia (`room`, `daidokoro`, `jimusitsu`), relacje przestrzenne (`naka`, `oku`), park, plaża i bazar nie są zaliczane automatycznie do budynków. Głos pozostaje media, fizyczne teksty i dokumenty cyfrowe pozostają text. Daty, jutro i weekend pozostają abstract. Pieniądze i czas zachowują dostępność przez przodka. Żaden stary przodek żadnego rzeczownika nie został utracony.

## Ocena wszystkich zmian kombinacji

| Czasownik | Dodane | Usunięte | Ocena |
|---|---|---|---|
| hiraku/object | letter | ∅ | letter: 手紙を開く, otworzyć list. Poprawna interpretacja otwierania/rozkładania dokumentu. |
| kesu/object | ∅ | email, note | Usunięto wyłączać mail/notatkę. Japoński wymaga tu polskiego usuwać, którego obecne formy nie mają. |
| nugu/object | ∅ | bag | Usunięto bag: torbę odkłada się/zdejmuje inną konstrukcją, nie standardowym nugu dla odzieży. |
| tateru/object | biru, byouin, eigakan, ginkou, mise, station, tatemono, yuubinkyoku | ∅ | Budować biurowiec, szpital, kino, bank, sklep, stację, budynek, pocztę. Chodzi o fizyczny obiekt, nie instytucję jako organizację. |

Dla pozostałych 249 ról dopuszczane zbiory są identyczne. Porównanie wszystkich par przymiotnik/rzeczownik wykazało 0 zmian. Kategorie nie naprawiają starych problemów tłumaczeń, np. trenować muzykę lub odbierać pracę. Zostały ujawnione powyżej.

## Źródła językowe i ograniczenie oceny

Ocena migracji jest analizą słownikową i przeglądem konkretnych par, nie formalnym dowodem poprawności dowolnego przyszłego rzeczownika. Sprawdzono definicje wydawców udostępnione przez Kotobank (16.10.2026):

- [着る, Digital Daijisen](https://kotobank.jp/word/着る-480492)
- [脱ぐ, Digital Daijisen / Nihon Kokugo Daijiten](https://kotobank.jp/word/脱ぐ-594100)
- [建てる, Digital Daijisen](https://kotobank.jp/word/建てる-561735)
- [通う, Digital Daijisen](https://kotobank.jp/word/通う-467110)
- [稽古](https://kotobank.jp/word/稽古-488385)
- [消す, Digital Daijisen](https://kotobank.jp/word/消す-490067)
- [開披, Digital Daijisen](https://kotobank.jp/word/開披-458330)
- [洗濯, Digital Daijisen](https://kotobank.jp/word/洗濯-88554)

Zakres polskiego tłumaczenia jest dodatkowym ograniczeniem aplikacji: szersza poprawność japońskiego nie upoważnia do poszerzenia par przy niezmienionym polskim czasowniku.

## Weryfikacja i odtwarzanie

Patrz `tools/README.md` oraz [wyniki integracji](noun_role_integration_c3.json). Testy jednostkowe nie czytają produkcyjnego słownika. Produkcyjny audyt jest osobnym poleceniem, ponieważ fixture nie może potwierdzić kompletności rzeczywiście wydanych 36 list ani zmian bieżącej macierzy. Koszt: O(liczba ról × liczba rzeczowników), analogicznie dla przymiotników. Integracja enumeruje wyłącznie dwie przydawki i sprawdza pozostałe wzorce przez exists.

Wszystkie 368 prób dostępności (92 wzorce × 4 formy) zachowuje poprzedni wynik.
Przydawki podmiotowe mają 1500 realizacji na formę przed i po migracji.
Przydawki dopełnieniowe mają 7645 → 7675 realizacji na formę (+45 nowych, −15
niepoprawnych, po uwzględnieniu 5 kontekstów). Wszystkie pozostałe realizacje są
identyczne bajtowo jako tekst pytania/odpowiedzi i związane wybory. Każda nowa para
została wygenerowana i przejrzana we wszystkich czterech formach. Przykłady są w JSON.

Przykłady: „To jest list, którego nie otwieram.” → `これはわたしがひらかないてがみです。`;
„To jest stacja, którą budowałem.” → `これはわたしがたてたえきです。`.
Przydawki podmiotowe są także pokryte fixture z jawnym i niejawnym `agree`.
Rzeczywisty zapis noun/verb XML i ponowny odczyt w kopii tymczasowej zachowuje
kategorie, macierz ról i pełną poprawność projektu. UI urządzenia nie był klikany
ręcznie; wykonano testy usług edycji i istniejące testy kontrolerów.

Wyniki końcowe testów i pomiarów znajdują się poniżej.

### Wyniki testów po review C3 (historyczne, przed C3.1)

- Linux / Python 3.12.14: **3796 passed, 0 skipped, 6373 subtests passed**, 126.84 s.
- Osobny zestaw Data z `KOTOMI_PATH`: **106 testów, bez pominięć**.
- C3 obejmuje 42 przypadki aplikacji i 15 przypadków audytu Data na niezależnych fixture.
- Bramka 8 s: 3796 wywołań, **0 przekroczeń**; najdłuższe 1.722 s.
- Walidatory repozytorium i pytań, pełne projekty, katalog, wszystkie role,
  cztery formy obu przydawek, generowanie pytań, statystyki i zapis/odczyt: PASS.
- Dokładny zatwierdzony zbiór 9 nowych i 3 usuniętych kombinacji: PASS.
- Rzeczywisty stary aktualizator instaluje fixture Content 62, odrzuca Content 63
  przed pobraniem danych. Nowy instaluje oba. Błędy i niepowiązane pliki: PASS.
- Nie dodano testów zależnych od produkcyjnego słownika ani nowych wyjątków dostępu.

[Podsumowanie maszynowe](noun_role_tests_c3.json).

### Wydajność po review C3 (historyczna baza C3.1)

Końcowy pomiar: 7 naprzemiennych rund przed/po, 21 próbek na operację,
osobne procesy, stałe ziarno i przypięty CPU, bez równoległych testów. Baseline:
wskazane wyżej commity main. Cold to nowy projekt, warm to wywołanie po rozgrzaniu.
Próg pozostaje **10%**. W 40 porównaniach zakres wynosi
**-12.06% do +8.93%**;
liczba przekroczeń: **0**.

Pierwsze pomiary wykazały przekroczenia; dokładniejszy przebieg potwierdził +11.67%
dla rozgrzanego pierwszego pytania z dopełnieniem. Profil uzasadnił zastąpienie
alokacji zbiorów operacją `isdisjoint` w istniejącym matcherze. JSON zachowuje
pierwsze pomiary, ich kontrolę, informację o profilu i wszystkie końcowe próbki.
Nie odrzucono niewygodnych wyników ani nie podniesiono progu.

Po poprawce główna seria pozostawiła przekroczenie w krótkiej operacji dostępności.
Jedna dodatkowa seria 9 rund po 101 próbek
potwierdza operacje, które przekroczyły próg. Dla zmierzonych ponownie operacji bramka
używa mediany wszystkich parowanych ilorazów z obu serii tego samego kodu,
z zachowaniem pierwszych siedmiu rund. Pozostałe operacje używają głównej serii.
`median_paired_ratios` w JSON zachowuje pierwotne wyniki, `verified_paired_ratios`
podaje wynik łączny. Najwyższy pierwotny iloraz po korekcie: 1.105499.

| Wzorzec | Operacja | Przed [ms] | Po [ms] | Mediana ilorazu po/przed |
|---|---|---:|---:|---:|
| Sam czasownik | cold/load | 80.672 | 81.648 | 0.998 |
| Sam czasownik | cold/compatibility | 1.630 | 1.717 | 1.003 |
| Sam czasownik | cold/exists | 0.371 | 0.389 | 1.047 |
| Sam czasownik | cold/count | 21.481 | 23.886 | 1.057 |
| Sam czasownik | cold/first_question | 0.857 | 0.912 | 1.055 |
| Sam czasownik | warm/load | 77.079 | 74.598 | 0.998 |
| Sam czasownik | warm/compatibility | 0.239 | 0.203 | 1.062 |
| Sam czasownik | warm/exists | 0.166 | 0.172 | 1.018 |
| Sam czasownik | warm/count | 19.864 | 23.657 | 1.089 |
| Sam czasownik | warm/first_question | 0.511 | 0.543 | 1.081 |
| Czasownik z dopełnieniem | cold/load | 70.818 | 71.986 | 1.034 |
| Czasownik z dopełnieniem | cold/compatibility | 5.494 | 5.015 | 0.937 |
| Czasownik z dopełnieniem | cold/exists | 4.564 | 4.163 | 0.924 |
| Czasownik z dopełnieniem | cold/count | 536.010 | 514.091 | 0.965 |
| Czasownik z dopełnieniem | cold/first_question | 6.147 | 6.303 | 0.982 |
| Czasownik z dopełnieniem | warm/load | 75.291 | 78.675 | 1.019 |
| Czasownik z dopełnieniem | warm/compatibility | 4.096 | 4.013 | 0.980 |
| Czasownik z dopełnieniem | warm/exists | 4.019 | 3.798 | 0.906 |
| Czasownik z dopełnieniem | warm/count | 492.673 | 520.342 | 1.052 |
| Czasownik z dopełnieniem | warm/first_question | 6.295 | 5.909 | 0.955 |
| Zdania przydawkowe | cold/load | 78.812 | 74.982 | 0.936 |
| Zdania przydawkowe | cold/compatibility | 11.512 | 11.337 | 0.979 |
| Zdania przydawkowe | cold/exists | 8.847 | 8.221 | 0.960 |
| Zdania przydawkowe | cold/count | 509.860 | 493.615 | 0.965 |
| Zdania przydawkowe | cold/first_question | 10.882 | 10.678 | 0.999 |
| Zdania przydawkowe | warm/load | 73.354 | 76.760 | 1.071 |
| Zdania przydawkowe | warm/compatibility | 9.791 | 9.495 | 0.967 |
| Zdania przydawkowe | warm/exists | 7.851 | 7.942 | 1.019 |
| Zdania przydawkowe | warm/count | 513.391 | 496.220 | 0.989 |
| Zdania przydawkowe | warm/first_question | 11.151 | 10.589 | 0.989 |
| Zdania przydawkowe podmiotowe | cold/load | 74.015 | 72.450 | 0.961 |
| Zdania przydawkowe podmiotowe | cold/compatibility | 16.671 | 17.083 | 1.004 |
| Zdania przydawkowe podmiotowe | cold/exists | 15.566 | 15.276 | 0.982 |
| Zdania przydawkowe podmiotowe | cold/count | 114.449 | 114.310 | 1.021 |
| Zdania przydawkowe podmiotowe | cold/first_question | 20.338 | 17.677 | 0.879 |
| Zdania przydawkowe podmiotowe | warm/load | 80.838 | 74.143 | 0.983 |
| Zdania przydawkowe podmiotowe | warm/compatibility | 15.855 | 15.522 | 1.002 |
| Zdania przydawkowe podmiotowe | warm/exists | 15.679 | 15.027 | 0.900 |
| Zdania przydawkowe podmiotowe | warm/count | 111.427 | 113.571 | 1.016 |
| Zdania przydawkowe podmiotowe | warm/first_question | 17.961 | 17.833 | 0.993 |

Czasy są medianami median rund; iloraz jest medianą ilorazów parowanych.
[Surowe pomiary i diagnostyka](noun_role_performance_c3.json).


## Wyniki końcowe C3.1

- Linux / Python 3.12.14: **3824 passed, 0 skipped, 6376 subtests passed**, 125.58 s.
- Osobno Kotomi-Data: **110 testów**, bez pominięć, z niezależnymi kontraktami silnika.
- Nowe testy: 24 przypadki aplikacji i 4 audytu Data; żadnego dostępu do produkcyjnego słownika.
- Bramka 8 s: 3824 wywołania, 0 przekroczeń. Walidatory repozytorium, pytań i manifestów: PASS.
- Wszystkie 122 czasowniki / 253 role / 80 rzeczowników: dokładnie **19 dodatków i 35 usunięć** wobec bazy C3.
- Cztery formy obu przydawek, 368 prób dostępności oraz tymczasowy zapis/odczyt: PASS.
- Wobec poprzedniego C3 (Data e51fcbb): 16 pełnych porównań statystyk (4 wzorce × 4 formy) identycznych,
  wszystkie 92 definicje wzorców i definicje quizów identyczne. Żaden wzorzec nie wybiera target;
  pozostałe 248 ról zachowuje dopasowania. Nie dodano produkcyjnego wzorca.
- Macierz aktualizatorów 62/63 wykonana ponownie: stary odrzuca format 2 przed pobraniem,
  nowy przyjmuje 62 i 63; istniejące dane i niezwiązane pliki pozostają bezpieczne.
- Wydajność C3.1 wobec C3: 7 naprzemiennych rund × 21 próbek, 40 porównań, maksimum **1.067901** (+6.79%), minimum 0.900574; **0 przekroczeń 10%**. Kod runtime jest identyczny. Wszystkie próbki zapisano w `target_review_c31` istniejącego JSON; starsze pomiary zachowano.
- Dokładne statystyki i zakres ograniczeń są w `target_review_c31` pliku wyników testów. CI weryfikowane na commitach PR; nie wykonano merge ani publikacji.
