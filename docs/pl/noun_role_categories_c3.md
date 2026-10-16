# Kategorie rzeczowników i role czasowników (C3)

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
Dokładnie 9 dodanych i 3 usunięte kombinacje pozostają bez zmian. Definicje
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
