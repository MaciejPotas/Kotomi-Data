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

Najpierw należy wdrożyć PR Kotomi z katalogiem, a dopiero potem Content 63.
Starsza aplikacja nie rozpoznaje nowych kategorii. Sam merge aplikacji na GitHub
nie aktualizuje instalacji użytkowników. Nie podnosimy istniejącego, historycznego
`min_kotomi_version`, ponieważ obecny nagłówek Content nie sprawdza go jako bramki
wersji, a numer wersji aplikacji jest niezależny. Publikację Content trzeba skoordynować
z dystrybucją aplikacji. Żaden PR nie wykonuje automatycznego merge.

[Raport zawartości](../validation/noun_role_audit_c3.md).
