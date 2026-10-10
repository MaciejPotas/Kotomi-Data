# Kategorie semantyczne przysłówków

Funkcja jest dostępna od Kotomi 1.8.0. Manifest Content wymaga tej wersji, żeby
starszy edytor nie zgubił kategorii przy zapisie. Nadal używamy Schema 2.

## Dane i znaczenie

Rzeczownik zachowuje pojedynczą, hierarchiczną `category`. Jej przodkowie biorą
udział w dopasowaniu czasowników, przymiotników i liczenia. Przysłówek może mieć
zero, jedną lub kilka płaskich kategorii. Nie ma między nimi dziedziczenia.
Wykorzystujemy istniejące `DictionaryConfig.categories`, sloty wyboru słów i
solver zgodności. Tagi lekcji nie zastępują klasyfikacji znaczeniowej.

Jedyny zapis przynależności to atrybut `categories` słowa, z wartościami
rozdzielonymi spacją. Katalog należy do słownika i może zawierać również
kategorie, których jeszcze nie przypisano żadnemu słowu:

```xml
<dictionary schema_version="2" id="adverbs" schema="adverb"
            instruction_language_id="pl">
  <categories>
    <category id="frequency" />
    <category id="time" />
    <category id="manner" />
    <category id="degree" />
    <category id="focus" />
  </categories>
  <words>
    <word id="mainichi" kana="まいにち" kanji="毎日"
          translation="codziennie" categories="frequency" />
    <word id="saikin" kana="さいきん" kanji="最近"
          translation="ostatnio" categories="time" />
  </words>
</dictionary>
```

| Kategoria | Znaczenie | Przykładowa kana |
| --- | --- | --- |
| `frequency` | Jak często | まいにち, ときどき, よく |
| `time` | Kiedy | さいきん, きのう, きょう |
| `manner` | Jak wykonywana jest czynność | ゆっくり |
| `degree` | Stopień lub intensywność | とても |
| `focus` | Wyróżnienie | とくに |

To deklaracje Content, a nie lista zaszyta w GUI. Własne ID kategorii mają format
`[a-z][a-z0-9_]*`. Puste i błędne ID, powtórzone deklaracje, powtórzone przypisania
oraz przypisania spoza katalogu są odrzucane. Wpis katalogu zawiera tylko `id`.
Przysłówek nie może użyć atrybutu `category`, bo stworzyłoby to drugi zapis tej
samej informacji. Starszy słownik bez katalogu i słowa bez `categories` nadal
się wczytują, ale takie słowa nie pasują do ograniczenia `category:...`.

Kilka kategorii, np. `categories="frequency time"`, przypisujemy tylko wtedy,
gdy jedno zapisane znaczenie pasuje do obu zastosowań. To nie jest alternatywa
różnych tłumaczeń. Produkcyjne `yoku` znaczy „często”, więc otrzymuje tylko
`frequency`. Dodanie `manner` dla osobnego znaczenia „dobrze” powodowałoby błędne
polskie tłumaczenia. Kategorie nie są zgadywane z tłumaczenia. „Wczoraj” określa
czas, a nie częstotliwość. `time_expressions` pozostaje wycofany.

## Pattern language i solver

`category:<id>` ogranicza wybór słowa. Dozwolone wartości pochodzą z katalogu
aktywnego słownika przysłówków. `categories:` nie jest właściwością placeholdera.

```text
{adverb[category:frequency].translation}
{adverb[category:frequency]}

{adverb@when[category:time].translation}
{adverb@when[category:time]}

{adverb@frequency[category:frequency].translation} {verb[form].translation}.
{adverb@frequency[category:frequency]} {verb[form]}。

{adverb[id:saikin, category:time]}
```

Alias oznacza ten sam wybrany wpis po obu stronach i we wszystkich wystąpieniach.
Ograniczenia aliasu przecinają się, również gdy zapisano je tylko po drugiej
stronie. Jeśli jedno wystąpienie wymaga częstotliwości, a drugie czasu, wybrane
słowo musi mieć obie kategorie. `id` i `category` również działają łącznie.

Przykłady niepoprawnego użycia:

| Przykład | Wynik |
| --- | --- |
| `{adverb[category:missing]}` | Błąd analizy, jeśli katalog nie zawiera `missing` |
| `{adverb[id:saikin, category:frequency]}` | Brak kandydatów dla powyższych danych |
| `{adverb[category:time, category:frequency]}` | Parser odrzuca powtórzoną właściwość |
| `{adverb[categories:time]}` | Parser odrzuca nieznaną właściwość |
| `{adverb[category:time, form:dictionary]}` | Parser odrzuca odmianę przysłówka |

Enumeracja zwraca pusty zbiór przy sprzecznych lub niespełnionych ograniczeniach.
Podgląd zgłasza `NoCompatibleChoices`. Renderer bound sprawdza `id` i wspólne
ograniczenia kategorii, więc niezgodne lub nieaktualne przypisanie kończy się
`ProjectError`. Wybór słowa odbywa się raz, we wspólnym solverze, bez wyjątków
dla konkretnych ID.

`occurrence` zachowuje dotychczasowe znaczenie kontekstu gramatycznego: jawne
adresy należą do realizacji źródłowych i muszą wskazywać kompletny zadeklarowany
kontekst i być częścią obsługiwanej konstrukcji gramatycznej. Przysłówki nie pełnią
w niej takiej roli, więc jawne `occurrence` nadal kończy się błędem analizy, choć
wspólny parser rozpoznaje tę właściwość. W zwykłych parach zdań wystarczy
alias. Skompilowane wystąpienia tokenów i powtórzone wyjścia nadal współdzielą
wybór słowa.

Kategorie nie sprawdzają zgodności z czasem zdania, rekcji, przeczenia,
naturalnego szyku ani sensowności każdej pary przysłówek/czasownik. Pattern trzeba
dobrać do zastosowania i wykorzystać pozostałe dostępne ograniczenia. Zmiana nie
dodaje polskiej odmiany przysłówków ani nowych reguł polskiej gramatyki.

## IntelliSense i Studio

Pola korzystające z `placeholder_completions` współdzielą kontrakt możliwości:
pytania i odpowiedzi patternów, edycja konstrukcji oraz istniejący asystent przy
polu tekstowym. `{adverb[` proponuje `id`, `category` i `occurrence`, bez form,
ról i cech. `{adverb[category:` czyta aktywny katalog, także własne i jeszcze
nieużywane kategorie. Wpisany fragment zawęża podpowiedzi. Użyta właściwość nie
pojawia się ponownie; działają kolejności `id, category` oraz `category, id`.
Wstawiony tekst jest zgodny z parserem. Okno wstawiania placeholdera również
przełącza listę kategorii między rzeczownikami a przysłówkami.

Otwórz przysłówek w obecnym edytorze słów, rozwiń pola zaawansowane i znajdź
**Kategorie semantyczne**. Wybierz z listy kolejne kategorie. Przyciskiem Usuń
usuń wybrane przypisania; pusta lista usuwa klasyfikację. Zapis i ponowne
wczytanie zachowują katalog i wszystkie przypisania. To istniejący `ValuePicker`,
a nie osobny edytor. Nową kategorię deklarujesz w XML słownika, a edytor słowa
pozwala przypisać wartości już zadeklarowane w projekcie.

## Walidacja i testy

`tests/data/adverb_categories/adverbs.xml` zawiera cztery niezależne słowa:
jedno wielokategorialne, jedno starsze bez kategorii i nieużywaną kategorię własną.
Testy silnika sprawdzają parser, filtrowanie, przecięcie aliasów, pary językowe,
ID, puste zbiory, nieznane wartości, zapis XML i całego projektu, zastosowanie
podpowiedzi, bound, lokalne konteksty gramatyczne oraz rzeczywistą klasę edytora
z rejestrującym backendem Tk. Sprawdzają też zachowanie rzeczowników.

Osobny walidator Kotomi-Data sprawdza katalogi i referencje wszystkich słowników
z manifestu, bez założeń o składzie lekcji, liczbie słów, ich kolejności lub
konkretnych ID. Jego testy mutacji budują mały, tymczasowy XML. Żaden nowy test
nie potrzebuje wyjątku pozwalającego czytać produkcyjny Content. Walidację
rzeczywistych plików wydania uruchamia się osobno.

## Sprawdzony przykład generowania

Dla produkcyjnego Content, powyższego ogólnego patternu częstotliwości, formy
`polite_nonpast` i wyboru czasownika `taberu`, bez ID przysłówka, enumeracja zwróciła:

| Wynik źródłowy | Wynik docelowy |
| --- | --- |
| `codziennie jem.` | `まいにち たべます。` |
| `czasami jem.` | `ときどき たべます。` |
| `często jem.` | `よく たべます。` |

To dokładne wyniki, także z małą literą na początku. Zwykłe wyjście przysłówka
nie dodaje reguły wielkiej litery. Identyczne pary mogą powtarzać się dla różnych
istniejących opcji kontekstu, gdy pattern nie zawiera tokenu kontekstu.
