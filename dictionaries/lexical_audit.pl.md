# Audyt kompletności słowników, 9 października 2026

Sprawdzono 61 rzeczowników, 121 czasowników i 87 przymiotników. Countery rozszerzono z 12 do 23.

## Rzeczowniki

Każdy rzeczownik ma siedem zwykłych przypadków. Profil `one` korzysta z nich przez
`fallback="noun_case"`, więc nie zapisujemy drugiej kopii. 50 haseł policzalnych
ma komplet siedmiu przypadków zarówno w `few`, jak i `many`, oraz powiązanie
z counterem. Formy `many` w mianowniku, bierniku i wołaczu używają dopełniacza
liczby mnogiej zgodnie z istniejącą strategią Kotomi. W pozostałych przypadkach
zachowujemy właściwą odmianę, np. `książkom`, `książkami`, `książkach`.

`clothes` ma teraz polską podstawę `ubranie`, rodzaj nijaki i odpowiednią odmianę
liczby pojedynczej. Dzięki temu jedna sztuka nie daje błędnego `jedno ubrania`.
`coffee`, `tea` i `water` są liczone jako zamówione porcje napoju w naczyniu,
np. dwie kawy. `sushi` oznacza w liczeniu pojedyncze kawałki.

Jedenaście wpisów pozostaje bez countera. Nie dokładamy fikcyjnych form typu
„dwie muzyki” ani nie zmieniamy znaczenia „telewizja” na „telewizor”. Ich powody
są wymienione w tabeli. Gdy potrzebujemy jednostki, należy dodać osobne hasło,
np. miska ryżu, godzina, utwór muzyczny lub moneta. Ich zwykłe przypadki są kompletne.

| ID | Klasa liczenia lub wyjątek | Znaczenie / uzasadnienie |
|---|---|---|
| `bag` | `small_object` | torba |
| `book` | `bound_volume` | książka |
| `box` | `small_object` | pudełko |
| `car` | `machine` | samochód |
| `clothes` | `garment` | ubranie |
| `coffee` | `cupful` | kawa |
| `daidokoro` | `general_item` | kuchnia |
| `email` | `correspondence` | mail |
| `friend` | `person` | przyjaciel |
| `fune` | `boat` | łódź |
| `gohan` | `wyjątek` | ryż jako substancja; wymaga osobnego hasła porcji/miski |
| `home` | `building` | dom |
| `inu` | `small_animal` | pies |
| `jikan` | `wyjątek` | czas, nie jednostka godziny |
| `keikaku` | `general_item` | plan działania |
| `kaigan` | `location` | plaża |
| `letter` | `correspondence` | list |
| `manga` | `bound_volume` | manga |
| `meal` | `meal` | posiłek |
| `mother` | `person` | mama |
| `motorcycle` | `machine` | motocykl |
| `music` | `wyjątek` | muzyka, nie utwór muzyczny |
| `newspaper` | `publication` | gazeta |
| `note` | `flat_object` | notatka |
| `okane` | `wyjątek` | pieniądze, nie monety ani jednostki waluty |
| `pan` | `general_item` | chleb |
| `park` | `location` | park |
| `ringo` | `small_object` | jabłko |
| `room` | `general_item` | pokój |
| `school` | `building` | szkoła |
| `shigoto` | `general_item` | praca |
| `sister` | `person` | siostra |
| `song` | `song` | piosenka |
| `station` | `location` | stacja |
| `sushi` | `small_object` | sushi |
| `taiikukan` | `building` | sala gimnastyczna |
| `tea` | `cupful` | herbata |
| `teacher` | `person` | nauczyciel |
| `television` | `wyjątek` | telewizja, nie telewizor |
| `tori` | `bird` | ptak |
| `water` | `cupful` | woda |
| `yakusoku` | `general_item` | obietnica |
| `yotei` | `general_item` | plan |
| `youji` | `general_item` | sprawa do załatwienia |
| `bazaaru` | `location` | bazar |
| `roujin` | `person` | starzec |
| `mise` | `building` | sklep |
| `naka` | `wyjątek` | relacyjne wnętrze, nie samodzielny policzalny przedmiot |
| `hitori` | `wyjątek` | gotowe wyrażenie jedna osoba |
| `koe` | `general_item` | głos |
| `hito` | `person` | osoba |
| `oku` | `wyjątek` | relacyjna głębia |
| `ashita` | `wyjątek` | jutro jako określenie czasu |
| `kagi` | `small_object` | klucz |
| `inochi` | `general_item` | życie |
| `riyuu` | `general_item` | powód |
| `hanashi` | `general_item` | opowieść |
| `saisho` | `wyjątek` | pierwszy moment/początek w znaczeniu relacyjnym |
| `detarame` | `wyjątek` | nonsens jako niepoliczalna treść |
| `pencil` | `long_object` | ołówek |
| `paper_sheet` | `flat_object` | kartka papieru |

## Nowe countery

| Counter | Zastosowanie |
|---|---|
| `tsu` (つ) | ogólne przedmioty i sprawy, dokładne formy 1–10 i いくつ |
| `chaku` (着) | odzież |
| `hai` (杯) | napoje w naczyniach |
| `tsuu` (通) | listy i wiadomości |
| `sou` (艘) | łodzie |
| `ken` (軒) | budynki i sklepy |
| `kasho` (箇所) | miejsca |
| `bu` (部) | egzemplarze gazet |
| `shoku` (食) | posiłki |
| `kyoku` (曲) | utwory muzyczne |
| `wa` (羽) | ptaki |

Każdy nowy counter ma dokładne kana, kanji i romaji dla 1–10 oraz pytania o ilość.
Wszystkie poza `tsu` mają także profil składania większych liczb w Kotomi.
`tsu` świadomie nie ma mechanicznego składania `じゅういちつ` ani `にじゅうつ`.
Przy ilościach powyżej 10 solver wymaga countera, który taką ilość obsługuje.

## Czasowniki

Każda zapisana forma ma kana, zapis pisany w polu `kanji` i polskie tłumaczenie.
Gdy hasło zwyczajowo zapisujemy kaną, pole `kanji` zachowuje ten zapis; nie
wprowadzamy sztucznego kanji. Zachowano istniejące tłumaczenia form osobowych.
Uzupełniono brakujące tłumaczenia form łączących, potencjalnych, biernych,
kauzatywnych, warunkowych, wolitywnych i rozkazujących.

Forma て nie ma jednego polskiego odpowiednika bez zdania. Używamy objaśnienia
imiesłowowego, np. `pisząc`, a dla dokonanego `umrzeć` poprawnego `umarłszy`.
Bierna japońska może być pośrednia, dlatego np. 泣かれる opisujemy jako
„ktoś płacze, co mnie martwi”, zamiast tworzyć nieistniejący polski imiesłów.
To przykładowe znaczenia form, a nie jedyne możliwe tłumaczenia w każdym kontekście.

Nie traktujemy tabelki 15 pól jako nakazu tworzenia nieproduktywnych form:

| Wpisy | Pominięte formy | Powód |
|---|---|---|
| `aru_possessive`, `aru_existential` | potential, passive, causative | nie są zwykłymi formami tych znaczeń; `あり得る` jest osobnym wyrażeniem możliwości |
| `dekiru`, `mieru` | potential, passive | znaczenia już wyrażające możliwość lub samoistną widoczność; brak regularnego podwójnego potencjału w tym materiale |
| `chigau`, `hareru`, `kumoru` | passive | nieproduktywne jako samodzielne formy uczone dla zapisanych znaczeń |

Dla obu `aru` dodano użyteczne `あって`, `あったら`, `あろう`, `あれ`.
Nieproduktywne, wcześniej mechanicznie wygenerowane wpisy usunięto z powyższych
haseł, zamiast nadawać im mylące tłumaczenia. Lista wyjątków jest sprawdzana testem.

## Przymiotniki

Wszystkie 87 haseł miało już 15 form z kana i tłumaczeniami. Uzupełniono ich zapis
pisany. Zachowano istniejące poprawne warianty z `じゃ`, bez zastępowania ich przez
`では`. Sprawdzono siedem przypadków dla wszystkich sześciu klas zgodności
obsługiwanych obecnie przez Kotomi. Nie znaleziono braków względem paradygmatów
SGJP. Nadpisania równe wartości `common` nie są zapisywane.

Istniejące tłumaczenia nieosobowych form przymiotnika pozostają glosami leksykalnymi
zgodnie z konwencją słownika i autora form w Kotomi. Ten PR nie zmienia sposobu
budowania polskich zdań z tych glos. Męskoosobowa liczba mnoga i jej uzgodnienia
nie są obecnie osobną klasą obsługiwaną przez silnik. Samo uzupełnienie danych
nie rozszerza tej możliwości.

## Weryfikacja i źródła

Polskie przypadki porównano z Morfeuszem 2 / SGJP podczas edycji. Runtime i nowe
testy nie wymagają Morfeusza. Testy pilnują pełnego pokrycia przypadków i form,
jawnych wyjątków, braku redundantnych nadpisań oraz wybranych nieregularności.
Powiązany PR Kotomi dodaje klasy i profile counterów oraz testuje rzeczywisty resolver.
Oba PR-y należy wdrożyć razem, bo starszy katalog gramatyki nie zna nowych klas.

- [SGJP](https://sgjp.pl/)
- [Morfeusz 2](http://morfeusz.sgjp.pl/)
- [Tofugu: counter つ](https://www.tofugu.com/japanese/japanese-counter-tsu/)
- [Tofugu: zestawienie counterów](https://www.tofugu.com/japanese/japanese-counters-list/)
- [Tae Kim: potencjał i あり得る](https://guidetojapanese.org/learn/complete/potential)
