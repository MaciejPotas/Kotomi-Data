# Kategorie rzeczowników i role czasowników (C3)

> Raport historyczny C3/C3.1. Content 64 używa formatu 3; aktualne zasady i zmiany kategorii opisuje [C3.2](target_government_c32.md).

Dodanie zwykłego rzeczownika polega na wybraniu najwęższej poprawnej kategorii.
Wszystkie czasowniki akceptujące tę kategorię lub jej przodka zaczynają go obsługiwać
bez edycji `verbs.xml`. Nie oznacza to, że każdy czasownik przyjmie każdy nowy rzeczownik.
Zgodność znaczenia i tłumaczenia nadal jest warunkiem przypisania kategorii.

## Kontrakt i architektura

Rzeczownik ma jedną kategorię `category`. Wbudowany katalog już obsługuje `parent`:
`closable_container → container → thing → purchasable → concrete` oraz
`education_facility → building → place → concrete`.
Nowe kategorie rozszerzają ten istniejący mechanizm. Nie zmieniamy DSL, modelu,
algorytmu dopasowania, form ani sposobu wiązania argumentów. Noun `categories`
nie jest obsługiwane; ta płaska lista służy obecnie przysłówkom, nie rzeczownikom.

`accepts="container"` przyjmuje kategorię i jej potomków. `nouns="room"` dopuszcza
konkretne ID. Razem oznaczają OR, nie AND. Samo `nouns` nie dołącza domyślnej kategorii
roli. Pusta rola dziedziczy swój zakres z definicji roli; `accepts="*"` przyjmuje wszystko.

```xml
<word id="new_chest" category="closable_container" ... />
<role ref="object" accepts="closable_container" government="direct_object" />
<role ref="target" accepts="container" nouns="room" />
```

W pierwszej roli nowa skrzynia działa bez zmiany czasownika. W drugiej dopuszczone są
pojemniki i dodatkowo pokój. Miska z kategorią `container` nie jest automatycznie
zamykana/otwierana. W przykładzie pominięto wymagane pola rzeczownika i jego formy.

## Nowe kategorie

| Kategoria | Rodzic | Zakres i granica |
|---|---|---|
| `container` | `thing` | Pojemnik, także bez zamknięcia. Nie dowolne miejsce. |
| `closable_container` | `container` | Pojemnik z zamknięciem, np. torba, skrzynia. Nie otwarta miska. |
| `clothing` | `thing` | Odzież, w tym przyszłe spodnie. Nie torba, biżuteria ani dowolne akcesoria. |
| `money` | `availability_reason` | Pieniądze, nie dowolne plany, czas lub zobowiązania finansowe. |
| `duration` | `availability_reason` | Czas jako trwanie, nie data, dzień tygodnia lub plan. |
| `music` | `media` | Muzyka i utwory muzyczne, nie głos ani fizyczne instrumenty. |
| `building` | `place` | Budynki i placówki w fizycznym znaczeniu, nie pomieszczenia, parki i plaże. |
| `education_facility` | `building` | Placówki regularnej nauki, np. szkoła. Nie każdy obiekt kulturalny. |
| `sports_facility` | `building` | Budynki sportowe, np. sala gimnastyczna. Nie każdy teren rekreacyjny. |

Każda kategoria opisuje cechę rzeczownika, a nie pojedynczy czasownik. Osiem kategorii
ma obecnych przedstawicieli; szersze `container` jest potrzebne do rozróżnienia pojemnika
od pojemnika zamykanego. Jednoczłonowe dziś `clothing`, `money` i `duration` mają otwarte,
niezależne od ID znaczenie. Nie tworzymy oddzielnych kategorii dla każdej listy.
Rodzic `availability_reason` jest zastanym zakresem zgodności, nie idealną ontologią:
jego zachowanie chroni istniejące reguły dostępności. Nie przenosimy dat do tej gałęzi.

## Autorstwo i Studio

W edytorze rzeczownika wybierz jedną kategorię z listy. Edytor czasownika pokazuje
te same nowe kategorie przy `accepts`. Dodanie słowa, zapis, ponowne otwarcie oraz
zachowanie `government` i OR sprawdzają niezależne testy usługi Studio.
W projekcie z własnym plikiem gramatyki obowiązuje jego własny katalog. Nie jest on
automatycznie nadpisywany nowymi kategoriami wbudowanymi.

Przed dodaniem kolejnej kategorii sprawdź wszystkich jej potencjalnych członków,
przodków, obecne role i polskie tłumaczenia. Wybierz istniejącą kategorię, jeśli pasuje.
Nie umieszczaj spodni w kategorii tylko po to, by dopuścić `kiru`: spodnie wymagają
`haku`. Dlatego `kiru` zachowuje jawne `clothes`, mimo że `nugu` i `sentakusuru`
korzystają z `clothing`. Dla przyszłego instrumentu nie używaj `music`, ponieważ
instrument jest przedmiotem, a nie utworem.

## Wyjątki i granica rozwiązania

`nouns` pozostaje dla konkretnego odczytania leksykalnego lub kontekstu, np. ratowania
`inochi` poza kategoriami person/animal. Uzasadnienie wpisz w raporcie. Nie traktuj
ogólnego `abstract`, `thing`, `place` lub `media` jako sposobu usunięcia ostatnich ID.

Pięć zachowanych list (`hajimeru`, `owaru`, `suru`, `tsuzukeru`, `ukeru`) nie jest
ostatecznym rozwiązaniem skalowania: wymaga doprecyzowania sensów czynności, planów
lub tłumaczeń. Audyt jawnie oznacza je jako `deferred_sense_review`. Także ogólne
polskie „trenować” przy `keikosuru` wymaga osobnego przeglądu; nie zmieniono tłumaczeń.

Jedna hierarchia nie opisze niezależnych osi, np. obiektu, materiału i przeznaczenia,
bez sztucznych kombinacji. Jeśli te osie okażą się konieczne, najprostsza rekomendacja
to zachowanie bazowego `category` i dodanie opcjonalnych dodatkowych kategorii
semantycznych na samym rzeczowniku. Dopasowanie używałoby sumy kategorii i przodków,
bez tabel per czasownik i bez zmiany OR. To osobna decyzja wymagająca wspólnej zmiany
walidacji, serializacji, indeksów, edytora i podpowiedzi. C3 tego nie implementuje
ani nie symuluje przez nadużywanie drzewa.

## Wzorce, quizy i wdrożenie

Nie zmieniono wzorców ani map uzgodnienia. Wszystkie odziedziczone stare kategorie
pozostają skuteczne. Macierz audytu obejmuje wszystkie role, również bez `nouns`,
oraz wszystkie pary przymiotnik/rzeczownik. Integracja porównuje realizacje przydawek
we wszystkich czterech formach, sprawdza automatyczne wiązanie, government, quizy,
statystyki i dostępność pozostałych wzorców. Testy silnika czytają wyłącznie fixture.

## Zatwierdzone decyzje i audyt po review

`noun_role_decisions_c3.json` jest źródłem zatwierdzonych oczekiwań: `target`
zawiera pełne, dokładne atrybuty roli, a `added` i `removed` jawne ID zmienionych
kombinacji. Nie przechowujemy drugiej macierzy dopasowań. Pozostałe role muszą
zachować atrybuty i wszystkie dopasowania z bazowej rewizji. Audyt porównuje osobno
te decyzje, XML i wyniki istniejącego `role_matches`. Ponowne wygenerowanie raportu
nie zatwierdza zmian. Duplikaty kluczy JSON są błędem; status decyzji musi zgadzać się
z obecnością wyjątków. `government`, kolejność ról i form oraz pozostałe XML są chronione.
Pierwotne 9 dodatków i 3 usunięcia zachowano; C3.1 dodaje jawne korekty target opisane poniżej. Definicje
istniejących kategorii są porównywane z bazowym katalogiem, aby obecny silnik
nie ukrył takiego samego błędu po obu stronach porównania.

## Kompatybilność i publikacja Content 63

Samo wdrożenie aplikacji przed Content nie zabezpiecza starszych instalacji.
`content_header.check_content_manifest` sprawdza nagłówek i schemat XML, lecz ignoruje
historyczne `min_kotomi_version="1.8.0"`. Aplikacja ma niezależną wersję `1.1.2`;
włączenie prostego porównania tych liczb odrzuciłoby także zgodny Content 62.

Desktop i Mobile używają wspólnego `QuizUpdater` z `expected_channel="content"`
i wybranym katalogiem danych. Kanał aplikacji ma osobne manifesty `version`,
Content używa `revision`, a quizy własnego kontraktu API. Sprawdzanie aplikacji opiera
się na hashach plików; rewizja Content ma istniejącą obsługę równości i potwierdzania
obniżenia wersji. Nie łączymy tych kanałów ani ich numerów. Natywna aplikacja Android kieruje
aktualizację samej aplikacji do niezależnego wydania APK; nie instaluje jej kanałem Content.

Najmniejsza skuteczna blokada wykorzystuje istniejące odrzucanie nieznanego formatu:
manifest aktualizacji Content 63 i nowszego ma `format: 2`. Dotychczasowe klienty
formatu 1 odrzucają go w `_parse_manifest`, przed pobraniem pierwszego pliku.
Nowy klient obsługuje formaty 1 i 2 wyłącznie na kanale Content; kanał aplikacji
pozostaje przy formacie 1. Generator oraz walidator wydania wymagają formatu 2 od
rewizji 63. `content_revision.json` i schematy XML nie zmieniają formatu.
Bazowy klient ma już dodatkową ochronę: walidacja snapshotu odrzuca nieznane
kategorie bez zmiany zainstalowanych danych, także przy manifeście formatu 1.
Format 2 przesuwa blokadę przed pobranie i chroni klientów obsługujących tylko format 1
bez polegania na obecności i szczegółach ich walidacji semantycznej.
To rzeczywista bariera dla już zainstalowanego klienta, nie ignorowane nowe pole. Po aktualizacji
aplikacji trzeba ją uruchomić ponownie, aby proces używał nowego aktualizatora.

Po pobraniu i sprawdzeniu hashy aktualizator buduje izolowany kompletny snapshot,
ładuje projekt i lekcje, sprawdza kategorie oraz referencje, dopiero potem rozpoczyna
istniejącą transakcję z kopiami zapasowymi. Błąd pobrania lub walidacji nie zapisuje
pliku na żywo. Błąd instalacji uruchamia istniejący rollback; znacznik rewizji jest
zapisywany ostatni. Obsługa błędów systemu plików nadal zachowuje kopie odzyskiwania,
jeśli sam rollback zawiedzie. Pliki spoza manifestu nie są nadpisywane; istniejąca
reguła usuwania dotyczy wyłącznie zarejestrowanych, wycofanych słowników, nie plików użytkownika.

| Aplikacja | Content 62, format 1 | Content 63, format 2 |
|---|---|---|
| Bazowa `9d6d662` | Instaluje | Odrzuca przed pobraniem danych |
| C3 po review | Instaluje | Instaluje po walidacji snapshotu |

Macierz sprawdzono rzeczywistym aktualizatorem obu checkoutów na niezależnym fixture,
nie na produkcyjnym słowniku. Testy nowej aplikacji obejmują nieznaną kategorię,
uszkodzone pobranie i zgodność wszystkich niepowiązanych plików. Istniejące testy
rollback, potwierdzania downgrade i anulowania pozostają w użyciu.

**Status: Content 63 można publikować przez manifest formatu 2 po przejściu CI obu PR-ów i bramek C3.**
Nie wolno publikować go jako format 1, także przez lustro lub starszy generator.
Dystrybucja nowego Kotomi umożliwia instalację; starszy klient pozostaje bezpiecznie
przy swoim Content i może nadal zaktualizować aplikację niezależnym kanałem.
Nie gwarantujemy zgodności ręcznego kopiowania XML z pominięciem aktualizatora.
Nie wykonano publikacji ani merge. W razie pozostawienia formatu 1 publikacja jest zablokowana.

## Korekta wydajności bez zmiany semantyki

Pomiar po review wykazał przekroczenie progu 10% przy pierwszym pytaniu po rozgrzaniu.
Profil wskazał częste tworzenie zbiorów w przecięciu kategorii. `role_matches`
używa teraz `accepted.isdisjoint(...)` zamiast kopiowania gotowego zbioru i tworzenia
zbioru przecięcia. Pozostaje ten sam matcher, OR, pełne obliczenie przodków i kontrola
cykli; nie dodano cache ani nowego modelu. Raport zachowuje także pomiary przed korektą.

## Niewielki zakres C4

Jedno drzewo wystarcza dla relacji typu budynek/placówka oraz pojemnik/pojemnik
zamykany, lecz nie dla niezależnych cech funkcjonalnych. `doa` i `mado` nie są
pojemnikami. Fixture pokazuje, że jako `thing` nie pasują do czterech ról
`closable_container`. To zamierzona obecna granica, nie uszkodzony test.
Podobnie `clothing` obejmuje koszulę i spodnie, lecz nie określa sposobu zakładania;
fixture zachowuje zakres `kiru` ograniczony do jawnego ID.

Obecne OR w `accepts` pozwala jednorazowo dodać do czterech czasowników nową poprawną
kategorię, np. elementów architektonicznych z zamknięciem. Kolejne rzeczowniki tej
kategorii działają bez edycji czasowników. To najmniejsza opcja bez zmian modelu i DSL,
jeśli rzeczywisty nowy słownik mieści się w takich rozłącznych grupach. Nie dodajemy
jej teraz na podstawie dwóch przykładów. Przypisanie drzwi do pojemników byłoby błędne.

Jeśli rzeczywisty słownik wykaże powtarzające się przecinanie grup, C4 powinno najpierw
ustalić mały katalog cech funkcjonalnych (otwieralność, sposób noszenia) i zakresy
czasowników. Następnie można ocenić opcjonalne dodatkowe członkostwa rzeczownika,
bez zmiany składni wzorców i `accepts`, z domyślną pustą listą zachowującą stare dane.
Wymaga to świadomej zmiany modelu, loadera/writera, walidacji, indeksów, Studio,
IntelliSense i bramki dystrybucji. Obecne `semantic_categories` są tylko dla przysłówków;
nie można ich dziś po prostu wpisać do rzeczownika. C4 nie obejmuje przebudowy
solverów, wielodziedziczenia drzewa ani masowej migracji słownika.


## Pokrycie testów po review

| Zakres | Istniejące testy Kotomi i uzupełnienia |
|---|---|
| Dziedziczenie, OR, nowe rzeczowniki | `test_noun_role_categories.py`, bez dublowania matcherów |
| Government, jawne/niejawne agree, cztery formy | `test_noun_role_categories.py`, `test_verb_form_agreement.py`, `test_subject_relative_catalog_boundary.py` |
| Przydawki podmiotowe/dopełnieniowe | `test_relative_realization.py`, `test_relative_explicit_case.py`, opt-in integracja C3 |
| XML i Studio | `test_xml_fragment_save.py`, `test_studio_change_aware_save.py`; rozszerzony test C3 sprawdza wszystkie niezwiązane pliki po zapisie rzeczownika i czasownika |
| IntelliSense | `test_intellisense_capability_matrix.py`, istniejące testy edytora wzorców i przydawek |
| Aktualizacja i rollback | `test_content_c3_compatibility.py`, istniejące `test_data_downgrade.py`, `test_update_progress.py` |
| Decyzje C3 | Data: `test_noun_role_audit.py`, jawne mutacje fixture oraz opcjonalne kontrakty rzeczywistego silnika |


[Raport zawartości](../validation/noun_role_audit_c3.md).

## C3.1: rola `target` i kierunek relacji

`target` to argument czasownika oznaczany tutaj partykułą **に**, nie synonim
odbiorcy. `object` oznacza dopełnienie z **を**, a `destination` kierunek ruchu
z **へ**. W japońskim に i へ czasem są wymienne, ale deklaracje DSL pozostają
odrębne. `target` zachowuje identyfikator i zgodność wcześniejszego Content.

Sam wpis w `<usage>` nie dodaje argumentu do zdania. Wzorzec wybiera rolę przez
`verb[role:target]`, a autor zapisuje に w odpowiedzi. `particle` jest metadanymi
katalogu i pomocą autora, nie automatycznym wstawianiem tekstu. Żaden z obecnych
92 wzorców produkcyjnych nie wybiera `target`; `reaction_target` jest inną rolą.
Żaden nowy wzorzec produkcyjny nie został dodany.

`accepts` filtruje kategorię wraz z przodkami; `nouns` dodaje dokładne ID przez OR.
`government` opisuje polski przypadek/przyimek **dla konkretnej roli czasownika**,
nie kategorię rzeczownika ani japońską partykułę. `target` nie oznacza automatycznie
celownika. Obecne deklaracje produkcyjne `target` nie mają `government`.
Wzorzec z `[government]` wymaga odpowiedniej ramki; przy jej braku nie powstaną
zgodne możliwości. Przed dodaniem takiego wzorca trzeba uzupełnić ramki i teksty
polskich form, a nie domyślnie używać rekcji `object`.

### Przegląd wszystkich 21 deklaracji

Poniższe zakresy są decyzjami dla znaczeń dydaktycznych Content, nie twierdzeniem,
że w metaforze, bajce lub szczególnym kontekście inne argumenty są niemożliwe.
Każda rola jest zgodna z に. Kategorie nie sprawdzają prawdopodobieństwa całej
sytuacji ani relacji między dwoma wybranymi rzeczownikami.

| Czasownik | Znaczenie `target` i ocena ograniczenia |
|---|---|
| `ayamaru` | Adresat przeprosin; `person animal` pozostaje: można przeprosić zwierzę. |
| `hairu` | Miejsce, do którego się wchodzi; `place` pozostaje. Nie każdy kontekst wejścia jest instytucjonalny. |
| `ireru` | Miejsce umieszczenia; `container` OR dokładne `room` pozostaje. Ograniczenie nie sprawdza rozmiarów przedmiotu i pojemnika. |
| `kariru` | Osoba, **od której** pożyczamy; `person animal → person`. Zwykłe zwierzę nie jest pożyczkodawcą. |
| `kayou` | Placówka regularnego uczęszczania; pozostaje `education_facility sports_facility`. |
| `kotaeru` | Osoba, której odpowiadamy, lub wiadomość; `abstract → person` OR `nouns="email letter"`. Usunięto m.in. dni tygodnia, czas i pieniądze. Nie rozszerzamy na każdą książkę/tekst. Nowe „pytanie” wymaga świadomego rozszerzenia zakresu. |
| `nareru` | Obiekt/osoba/sytuacja, do której się przyzwyczajamy; `*` pozostaje jako celowo szerokie znaczenie. |
| `naru` | Wynik zmiany/stawania się; `*` pozostaje dla ról, stanów i przekształceń. Dowolne pary podmiot–wynik nie są gwarantowane; przyszły wzorzec musi ograniczyć kontekst (nie generator codziennych zdań o dowolnej przemianie). |
| `okoru` | Osoba/zwierzę, na które się gniewamy; `person animal` pozostaje. |
| `oshieru` | Uczeń/odbiorca nauki; `person animal` pozostaje, bo można uczyć psa komend. Przedmiot nauki i uczeń wymagają spójnego kontekstu. |
| `sawaru` | Dotykany obiekt; `concrete` pozostaje, bez ograniczenia do odbiorców/osób. |
| `teishutsusuru` | Osoba/instytucja przyjmująca dokument; dokładne `teacher school` pozostaje. |
| `tomaru` | Punkt zatrzymania; `place` pozostaje. Obecne 止まる nie jest nocowaniem 泊まる. |
| `usowotsuku` | Rozmówca, którego okłamujemy; `person animal → person` dla podstawowej komunikacji językowej. Zwodzenie zwierzęcia zachowaniem nie uzasadnia całej kategorii. |
| `ageru_give` | Odbiorca daru; `person animal` pozostaje (np. jedzenie dla psa). `ageru` z kanji 上げる oznacza tu osobne „podnosić”. |
| `kaesu` | Odbiorca zwracanego przedmiotu; `person animal` pozostaje (np. zwrot zabawki psu). |
| `kasu` | Osoba, **której** pożyczamy; `person animal → person`: udostępnienie z oczekiwaniem zwrotu, nie samo danie zwierzęciu. |
| `kureru` | Odbiorca po stronie mówiącego; `person` pozostaje, ale sama kategoria nie koduje perspektywy. Przyszły wzorzec musi określić mówiącego/jego bliskich. |
| `morau` | Osoba, **od której** otrzymujemy; `person animal → person` w zwykłym interpersonalnym znaczeniu. Zwierzę jako dawca wymaga osobnego kontekstu. |
| `watasu` | Odbiorca przekazywanego przedmiotu; `person` pozostaje. |
| `sumu` | Miejsce zamieszkania; `place` pozostaje. Kontekst określa możliwość zamieszkania, nie sama hierarchia. |

### Dwa argumenty i tłumaczenia

Istniejący DSL obsługuje obie role jednego slotu. Deklaracje powtarzane dla tego
samego aliasu łączą role, np. w pytaniu `verb@action[role:target, form].translation`,
a w odpowiedzi `{noun@partner}に{noun@item}を{verb@action[role:object, form]}`.
Rzeczowniki można ograniczyć przez `category:person` i `category:text`; automatyczne
wiązanie używa rzeczywistego `role_matches`. Przy nakładających się domenach ról
samo `government:@action` nie rozstrzyga, **którą rolą** jest rzeczownik: wskazuje
czasownik, a nie rolę. Wtedy potrzebne są rozłączne domeny istniejącymi filtrami;
gdy nie da się ich uzyskać, przyszły wzorzec wymaga osobnego zadania. Nie dodajemy
obejścia ani składni selektora roli rzeczownika w C3.1.

- せんせいにほんをかりる — „Pożyczam książkę **od nauczyciela**”: target wymaga `od` + dopełniacz.
- ともだちにほんをかす — „Pożyczam książkę **przyjacielowi**”: target wymaga celownika.
- ともだちにほんをあげる — „Daję książkę **przyjacielowi**”: `ageru_give`, celownik.
- がっこうにはいる — „Wchodzę **do szkoły**”: target, `do` + dopełniacz.
- がっこうにかよう — „Uczęszczam **do szkoły**”: target, `do` + dopełniacz.

Fixture sprawdza trzy pierwsze zdania, dodatnie i przeczące formy, liczenie,
wiązanie, OR, odmienne ramki obu argumentów, partykułę i zapis/odczyt XML.
Jest napisane niezależnie od Content. Nie twierdzi, że produkcyjne tłumaczenia
są już gotowe do nowego uniwersalnego wzorca: `kariru` ma „pożyczam od kogoś”,
`kasu` „pożyczam komuś”, `ageru_give` „daję komuś”. Mechaniczne dopisanie argumentu
dublowałoby „od kogoś/komuś”; potrzebny jest wariant tłumaczenia dla takiego wzorca.
`kureru` dodatkowo wymaga perspektywy i osoby podmiotu; `kotaeru` różnej polskiej
rekcji osoby („komuś”) i wiadomości („na list”). To małe osobne zadanie autorskie
przed publikacją wzorców, nie powód do przebudowy solvera.

### Placówki a `building`

Szkoła i uczelnia należą do `education_facility`; sala gimnastyczna/treningowa
rozumiana jako obiekt zajęć do `sports_facility`. Zwykły pokój treningowy nie staje
się przez to budynkiem: potrzebna jest osobna decyzja leksykalna. Nowe poprawnie
sklasyfikowane placówki działają z `kayou` bez edycji czasownika. Bank, biurowiec
lub szpital nie są placówkami edukacyjnymi/sportowymi tylko dlatego, że są budynkami.
Japońskie 病院に通う jest poprawne („regularnie chodzić do szpitala”), podobnie
regularne wizyty/dojazdy mogą dotyczyć banku/biura. Obecne polskie „uczęszczać”
nie pokrywa automatycznie tych znaczeń. Zachowujemy oba podtypy i wąski zakres;
`building` byłoby nieuzasadnionym poszerzeniem. Nie dodajemy kategorii ani cech.

### Dowody i zakres akceptacji C3.1

Zmieniono pięć ról `target`; pozostałe 248 ról zachowują wyniki zatwierdzonego C3.
Łączna macierz względem bazy C3 ma **19 dodanych i 35 usuniętych** kombinacji
(wcześniej 9/3); jawne `nouns` pozostają w **15** rolach (wcześniej 14).
Nowy wyjątek `kotaeru` jest celowy, nie ukryty za szeroką kategorią.
Istniejący JSON decyzji zawiera pięć wpisów `scope: C3.1_target`, dokładny `before`,
`target`, uzasadnienie i zbiory `added/removed`. Brak wpisu, dryf XML albo wyników
nadal blokuje audyt. Regeneracja raportu nie zatwierdza nowych decyzji.
Content pozostaje nieopublikowaną rewizją 63 z manifestem formatu **2**.

Źródła językowe (odczyt 2026-10-16; polityka zakresu Content jest naszą decyzją):
[TUFS: に i kierunek przekazywania](https://www.coelang.tufs.ac.jp/mt/ja/gmod/courses/c01/lesson08/step3/explanation/028.html),
[TUFS: あげる/くれる/もらう, także zwierzęta](https://www.coelang.tufs.ac.jp/mt/ja/gmod/courses/c01/lesson22/step1/explanation/085.html),
[Daijisen: 通う](https://kotobank.jp/word/通う-467110),
[Daijisen: 答える](https://kotobank.jp/word/答える-502121),
[Daijisen: 嘘](https://kotobank.jp/word/嘘-440021).
