# Słowniki, referencje kontekstów i tokeny leksykalne

Kotomi 1.7 wczytuje jeden projekt Content. Słownik przechowuje słowo, a lekcje
i pule kontekstów wskazują ten wpis. `kinou` należy do `adverbs`. `ashita` zostaje
w `nouns` i może być używane przez dowolny kontekst. Jedno słowo może należeć do
wielu lekcji i pul bez kopiowania tłumaczenia lub kany. Wycofany słownik
`time_expressions` nie stanowi osobnego źródła słów.

## ID słownika, schemat i rodzaj tokena

| ID słownika | Schemat | Token | Wybór | Realizacja |
|---|---|---|---|---|
| `adverbs` | `adverb` | `adverb` | `id`, `category`, alias | wyjścia bezpośrednie |
| `demonstratives` | `demonstrative` | `demonstrative` | `id`, alias | wyjścia bezpośrednie; `agree`, `case` dla tłumaczenia |
| `expressions` | `expression` | `expression` | `id`, alias | wyjścia bezpośrednie |

Wszystkie trzy obsługują `occurrence` oraz wyjścia `id`, `translation`, `kana`,
`kanji`, `romaji`. Token bez końcówki zwraca kanę. Nie obsługują selektorów
`form`, `polarity`, `role` ani `feature`. Przysłówki dodatkowo obsługują `category`. Jawne żądanie pustego pola opcjonalnego kończy się komunikatem błędu;
silnik nie wymyśla brakującego tekstu. Alias współdzieli wybór słowa, a `occurrence` wskazuje
jedno lokalne użycie gramatyczne tego wyboru.

Manifest rejestruje plik i schemat. Plik deklaruje takie samo ID i schemat.
Możliwości edytora określa `dictionary_config_for_language()`. Content nie może
definiować schematu `<editor>`. Samo utworzenie własnego słownika z wybranym
schematem nie dodaje publicznego tokena. `PLACEHOLDER_CONTRACTS` wiąże rodzaje
tokenów z konkretnymi ID słowników.

Do istniejącej sekcji `<dictionaries>` dodaj rejestracje:

```xml
<dictionary id="adverbs" file="dictionaries/adverbs.xml" schema="adverb" />
<dictionary id="demonstratives" file="dictionaries/demonstratives.xml" schema="demonstrative" />
<dictionary id="expressions" file="dictionaries/expressions.xml" schema="expression" />
```

Starszy projekt może nie mieć tych trzech słowników. Pattern używający brakującego
słownika nie wygeneruje zdania. Konteksty z tekstem wpisanym bezpośrednio nadal
działają. Content z referencjami kontekstów deklaruje `min_kotomi_version="1.7"`,
żeby starsza aplikacja nie potraktowała referencji jako pustego kontekstu.

## Kompletne przykłady słowników

To małe, niezależne przykłady, a nie lista słów, której testy mają pilnować.
W desktopowym edytorze wybierz istniejący słownik, wpisz ID, tłumaczenie i kanę,
a w razie potrzeby także kanji i romaji. Trzy nowe typy są dostępne również przy
tworzeniu słownika. Dla demonstratywów z aktywną gramatyką Polski można edytować
uzgodnienie. Te typy nie mają japońskiej odmiany czasownikowej.

`dictionaries/adverbs.xml`:

```xml
<dictionary schema_version="2" id="adverbs" schema="adverb"
            target_language_id="ja" instruction_language_id="pl" label="Adverbs">
  <words>
    <word id="kinou" translation="wczoraj" kana="きのう" kanji="昨日" romaji="kinou" />
  </words>
</dictionary>
```

`dictionaries/expressions.xml`:

```xml
<dictionary schema_version="2" id="expressions" schema="expression"
            target_language_id="ja" instruction_language_id="pl" label="Expressions">
  <words>
    <word id="shikata_ga_nai" translation="nic nie da się zrobić"
          kana="しかたがない" kanji="仕方がない" romaji="shikata ga nai" />
  </words>
</dictionary>
```

`dictionaries/demonstratives.xml`:

```xml
<dictionary schema_version="2" id="demonstratives" schema="demonstrative"
            target_language_id="ja" instruction_language_id="pl" label="Demonstratives">
  <words>
    <word id="kono" translation="ten" kana="この" kanji="この" romaji="kono">
      <polish_forms>
        <common cases="nominative accusative vocative" value="ten" />
        <common cases="genitive" value="tego" />
        <common cases="dative" value="temu" />
        <common cases="instrumental locative" value="tym" />
        <override classes="masculine_personal masculine_animate" cases="accusative" value="tego" />
        <override classes="feminine" cases="nominative vocative" value="ta" />
        <override classes="feminine" cases="genitive dative locative" value="tej" />
        <override classes="feminine" cases="accusative" value="tę" />
        <override classes="feminine" cases="instrumental" value="tą" />
        <override classes="neuter" cases="nominative accusative vocative" value="to" />
        <override classes="plural_non_masculine_personal" cases="nominative accusative vocative" value="te" />
        <override classes="plural_non_masculine_personal" cases="genitive locative" value="tych" />
        <override classes="plural_non_masculine_personal" cases="dative" value="tym" />
        <override classes="plural_non_masculine_personal" cases="instrumental" value="tymi" />
      </polish_forms>
    </word>
  </words>
</dictionary>
```

Polska gramatyka wybiera zapisaną formę: najpierw nadpisanie dla klasy, potem
wspólną wartość przypadka. Runtime nie tworzy odmiany. Zapis usuwa nadpisania
identyczne z wartością wspólną. Samodzielne `kore/sore/are` mają wspólne wartości
przypadków; `kono/sono/ano` wymagają też odmiany według rodzaju. Przykład obejmuje
aktualnie obsługiwane klasy, bez deklarowania osobnej klasy męskoosobowej liczby
mnogiej, której obecny model nie udostępnia.

| Token dla powyższych przykładów | Wartość leksykalna |
|---|---|
| `{adverb[id:kinou].translation}` | `wczoraj` |
| `{adverb[id:kinou].kana}` | `きのう` |
| `{adverb@time[id:kinou].kanji}` | `昨日` |
| `{expression[id:shikata_ga_nai]}` | `しかたがない` |
| `{expression[id:shikata_ga_nai].translation}` | `nic nie da się zrobić` |
| `{demonstrative[id:kono]}` | `この` |
| `{demonstrative[id:kono].translation}` | `ten` |
| `{demonstrative[id:kono, agree:@item, case:@item].translation}` przy żeńskim `noun@item` w miejscowniku | `tej` |

Pełny przykład uzgodnienia z rzeczownikiem `school`, który ma klasę żeńską
i zapisany miejscownik `szkole`:

```text
{demonstrative[id:kono, agree:@item, case:@item].translation} {noun@item[id:school, case:locative]}
```

Wynik to `tej szkole`. Formatowanie początku zdania może zmienić pierwszą literę
na `Tej`; tabela opisuje same wartości leksykalne. Dla demonstratywu `case`
wymaga `agree`, a uzgodnienie wymaga wyjścia `.translation`. Na przykład
`{demonstrative[id:kono, case:locative].translation}` oraz
`{adverb[id:kinou, form:dictionary]}` są błędne. `agree:@item` potrafi przejąć
wynikowy przypadek rzeczownika. Jawne `case:@item` przydaje się, gdy chcesz
zapisać tę zależność wprost albo wskazać inny przypadek.

## Referencje w lekcjach

```xml
<lesson_catalog schema_version="4" instruction_language_id="pl">
  <lessons>
    <lesson id="example_a" group="Examples" main="Time" name="First">
      <word><dictionary_ref dictionary="adverbs" word="kinou" /></word>
    </lesson>
    <lesson id="example_b" group="Examples" main="Review" name="Second">
      <word><dictionary_ref dictionary="adverbs" word="kinou" /></word>
    </lesson>
  </lessons>
</lesson_catalog>
```

Zapis słowa pochodzącego ze słownika zachowuje referencję, bez kopiowania wpisu.
Loader lekcji rozwiązuje referencje z aktualnego projektu. Po edycji słownika
wczytaj katalog ponownie, żeby odświeżyć utworzone wcześniej wartości lekcji.
Kontekst działa inaczej: przy każdym użyciu odczytuje bieżący obiekt Word.
Brak słowa jest błędem walidacji. Żadna nazwa grupy nie ma specjalnych uprawnień
ani minimalnej liczby słów. Testy nie mogą utrwalać składu lub wielkości prawdziwej lekcji.

## Referencje kontekstów i sufiksy

```xml
<contexts schema_version="2" instruction_language_id="pl">
  <context id="none" label="Neutral"><option id="neutral" translation="" kana="" /></context>
  <context id="past" label="Past">
    <option id="yesterday" dictionary="adverbs" word="kinou" weight="2"
            translation_suffix=" " kana_suffix="、" />
  </context>
  <context id="future" label="Future">
    <option id="tomorrow" dictionary="nouns" word="ashita" weight="1"
            translation_suffix=" " kana_suffix="、" />
  </context>
</contexts>
```

Ostatnia opcja wymaga istniejącego `nouns/ashita`. `ContextOption.resolved()`
odczytuje tłumaczenie przez aktywny język instrukcji i dopisuje
`translation_suffix`. Do kany słowa dopisuje `kana_suffix`. Sufiksy to dosłowne
separatory, zachowują celowe spacje i nie są szablonami placeholderów.
Jedno słowo może obsługiwać kilka pul. Jego edycja zmienia wszystkie kolejne
rozwiązania referencji bez przepisywania definicji kontekstów.

`{context[pool:past].translation}` daje `wczoraj `, a
`{context[pool:past].kana}` daje `きのう、`. Losowanie według wag wybiera tę samą
opcję dla obu języków. W zakładce Konteksty w Studio wpisz ID słownika i słowa,
zostaw puste teksty inline, a separatory wpisz w polach Po tłumaczeniu i Po kanie.
Opcje neutralne lub własne teksty wpisane bezpośrednio nadal są poprawne.

`dictionary` i `word` muszą wystąpić razem. Nie łącz referencji z inline
`translation` lub `kana`; sufiksy wymagają referencji. Loader, walidator projektu
i zapis kontekstów odrzucają brakujące słowa oraz mieszane definicje.
Pełny zapis projektu sprawdza cały model przed pierwszą zmianą pliku, bez
wyliczania możliwości zdań. Błąd walidacji pozostawia wszystkie pliki bez zmian.
Podmiana pojedynczego pliku jest atomowa, ale zapis wielu plików nie zapewnia
wycofania wcześniejszych zapisów po niezależnym błędzie dysku.

## Wycofywanie słowników

Informację o wycofaniu zapisuje wyłącznie manifest projektu:

```xml
<retired_dictionaries>
  <dictionary id="time_expressions" />
</retired_dictionaries>
```

Przed publikacją usuń starą rejestrację słownika i popraw wszystkie referencje
lekcji oraz kontekstów. `DictionaryService` nie wykryje ponownie niezarejestrowanego
pliku z takim ID po aktualizacji. Plik użytkownika pozostaje na dysku.
Jawna rejestracja ma pierwszeństwo i ponownie aktywuje słownik. Zapis i wczytanie
projektu zachowują listę wycofanych ID. `counting.xml` zawiera wyłącznie zestawy
liczb i powiązania counterów, nigdy `retired_dictionaries`.

## Nowy typ i jego testy

Nowy publiczny typ potrzebuje wpisu w `PLACEHOLDER_CONTRACTS`, schematu edytora,
jeśli różnią się możliwości, oraz zgodnej obsługi w parserze, analizie,
generowaniu, XML i Studio. IntelliSense korzysta z kontraktów, podpowiadając
typy, ID, aliasy, selektory i wyjścia. Pomija użyte argumenty i niedozwolone
kombinacje. Dla demonstratywów podpowiada `case` po `agree`, a dla uzgodnienia
wyłącznie `.translation`. Sprawdź rzeczywisty tekst po zastosowaniu podpowiedzi
parserem, także błędne kombinacje oraz brak słownika lub ID. Nie dodawaj wyjątków
dla konkretnych słów.

Korzystaj z `tests/data/engine` i niewielkiego uzupełnienia
`data/tests/fixtures/lexical`. Nie kopiuj ani nie generuj ich z aktualnej bazy
produkcyjnej podczas testów. Modyfikuj kopie w katalogu tymczasowym, żeby sprawdzać
usuwanie słów, współdzielenie referencji i nieprawidłowe dane. Testy silnika
obejmują dowolne lekcje, zapis i odczyt, uzgodnienie oraz renderowanie. Oddzielne
kontrole wydania sprawdzają wszystkie publikowane referencje, formy i manifesty.

Każdy wyjątek produkcyjny w `tests/conftest.py` wskazuje jeden test i zawiera
`invariant`, `fixture_gap`, `file_scope`, `growth_cost`. Guard egzekwuje zakres
plików. Sam marker, puste uzasadnienie lub ogólnik nie przyznają dostępu.
Kontrole metadanych mają osobny rejestr i nie czytają leksykalnych XML-i.
Usunięcie asercji o konkretnej lekcji nie uzasadnia usuwania ogólnych kontroli
jakości Content.

Edytor słowników blokuje usunięcie lub zmianę ID słowa używanego przez kontekst
albo lekcję w Schema 4. Jeśli plik lekcji jest uszkodzony i nie można sprawdzić
referencji, operacja również jest blokowana. Zmiana wartości słowa pod tym samym
ID pozostaje dozwolona i zmienia kolejne rozwiązania referencji kontekstów.

[Kategorie semantyczne: XML, wybór, IntelliSense i Studio](adverb_categories.md).
