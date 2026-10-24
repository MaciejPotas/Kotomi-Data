# Zdania przydawkowe w Content

Nowe rodziny z lekcji 26: [zakres i ograniczenia](relative_lesson26.md).

Aktualny silnik obejmuje B3 oraz uniwersalny target C3.2. Ten dokument zachowuje opis konkretnego etapu; bieżące odwołania i kompletność sprawdzaj narzędziami opisanymi w [audycie](developer_tools.md).

Rewizja Content 59 dodaje jeden wzorzec `Zdania przydawkowe` w kategorii
`przydawki` w `patterns/sentence_maps.xml`. Definicja `relative_clauses` w
`patterns/sentence_quizzes.xml` udostępnia go jako quiz **Zdania przydawkowe**
w Windows i Mobile przez istniejący pakiet quizów gramatycznych.
Wymagana jest aplikacja zawierająca mechanizm z Kotomi PR #208 i gramatyka Polski.
Samo pobranie danych nie dodaje obsługi DSL do starszej aplikacji.

```xml
<sentence_pattern id="Zdania przydawkowe" category="przydawki"
                  forms="dictionary plain_negative past_plain past_negative_plain">
  <question>To jest {noun@item[case:nominative]}, {relative[agree:@item, government:@action].phrase} {verb@action[role:object, form].translation}.</question>
  <answer>これはわたしが{verb@action[role:object, form]}{noun@item}です。</answer>
</sentence_pattern>
```

`.phrase` zachowuje przyimek rekcji: `nad którym zastanawiam się`,
`na który czekam`, `w który wierzę`. Bez przyimka działa tak samo jak
`.translation`: `którą czytam`, `której nie czytam`. Rzeczownik i czasownik
wiąże istniejąca rola `object`; nie są potrzebne dodatkowe argumenty.

| Forma | Pytanie dla `book` i `yomu` | Odpowiedź |
|---|---|---|
| `dictionary` | To jest książka, którą czytam. | これはわたしがよむほんです。 |
| `plain_negative` | To jest książka, której nie czytam. | これはわたしがよまないほんです。 |
| `past_plain` | To jest książka, którą czytałem. | これはわたしがよんだほんです。 |
| `past_negative_plain` | To jest książka, której nie czytałem. | これはわたしがよまなかったほんです。 |

W Studio wybierz kategorię `przydawki`. Podgląd i symulator korzystają z tych
samych ograniczeń form co quiz. W quizie włącz styl potoczny; formy grzeczne
czasownika wewnątrz przydawki są wykluczone. Końcowe `です` pozostaje stałe.
Do ćwiczenia wybranego słownictwa służą istniejące filtry, np.
`verb.id=yomu;noun.id=book`. Bez filtrów obowiązują dotychczasowe kategorie
i jawne listy kompatybilności słowników, które nie gwarantują naturalności
każdego połączenia znaczeń. Rewizja 59 koryguje dwa wykazane problemy:
`sukuu` dopuszcza ludzi, zwierzęta i jawnie `inochi` (życie), a `ireru`
nie dopuszcza ogólnego `abstract`, zachowując jawnie `okane` (pieniądze).
Odrzuca to „ratować powtórkę” i „wkładać czas” we wszystkich wzorcach.
Zawężenie `sukuu` wyklucza również abstrakcyjne dopełnienia takie jak praca
i plan. Nie dodano wyjątków ani słownika dobrych zdań do silnika.

Zakres pierwszego wzorca pozostaje pojedynczy i dopełnieniowy. `okane` ma klasę liczby mnogiej,
więc jest poprawnie odrzucane; `harau`, ograniczone do `okane`, nie daje tu
wyników. Nie należy dopisywać sztucznych form w celu obejścia tego ograniczenia.

Liczniki silnika rozróżniają kombinacje słów, generowane realizacje z kontekstem
i unikalne teksty. Ten wzorzec nie wypisuje kontekstu, dlatego różne istniejące
opcje kontekstu mogą dawać identyczny tekst. Nie należy interpretować pola
`generated_sentences` jako liczby różnych zdań do wyświetlenia.

Pełny kontrakt DSL i ograniczeń `forms` opisuje dokumentacja
[Kotomi](https://github.com/MaciejPotas/Kotomi/blob/main/docs/pl/relative_clauses.md).
Publikacja zwiększa wyłącznie rewizję Content i odświeża jego manifest.
Pakiety wykonywalne Quiz oraz numer wersji aplikacji pozostają bez zmian.


## B3: przydawki podmiotowe

Rewizja Content 60 dodaje drugi wzorzec do tego samego quizu. Wymaga B1/B2
oraz poprawki granicy katalogu egzystencjalnego opisanej poniżej. B4 dopiero
przypnie tę rewizję w aplikacji; sam ten PR nie zmienia gitlinka ani dystrybucji.

```xml
<sentence_pattern id="Zdania przydawkowe podmiotowe" category="przydawki"
                  forms="dictionary plain_negative past_plain past_negative_plain">
  <question>To jest {noun@item[case:nominative]}, {relative[agree:@item, case:nominative].translation} {verb@action[role:subject, form, agree:@item].translation}.</question>
  <answer>これは{verb@action[role:subject, form]}{noun@item}です。</answer>
</sentence_pattern>
```

Przydawka dopełnieniowa opisuje rzecz, wobec której ktoś wykonuje czynność:
„książka, którą czytam”. Przydawka podmiotowa opisuje wykonawcę lub przedmiot
zmiany: „osoba, która pracuje”, „pudełko, które się otworzyło”. W drugim wzorcu
nie ma `わたしが`. `relative[case:nominative]` wybiera mianownik, natomiast
`relative[government:@action]` w pierwszym wzorcu realizuje przypadek i przyimek
rekcji. `role:subject` sprawdza zgodność podmiotu; nie dodajemy `government`.
Reguły polskiej odmiany pozostają w
[dokumentacji języka](https://github.com/MaciejPotas/Kotomi/blob/main/kotomi/languages/polish/docs/polish_grammar.md#b2-uzgodnienie-form-czasownika).

| Czasownik | Podmioty | Klasy zapisanych tłumaczeń |
|---|---|---|
| `hataraku` | `friend mother sister teacher roujin hito programmer madogiwazoku` | masculine_personal, feminine |
| `neru` | te same osoby oraz `inu tori` | masculine_personal, masculine_animate, feminine |
| `aku` | istniejące `bag box` | feminine, neuter |

To świadomie mały zestaw: praca człowieka, sen osoby/zwierzęcia i otwieranie
przedmiotu. Zachowano wszystkie dotychczasowe role, formy japońskie oraz zwykłe
`Form.translation`. Nowe role `hataraku` i `neru` używają `nouns="..."`.
Nie wystarczy ogólne `person`: obejmuje `hitori` („jedna osoba”), które nie jest
zwykłym rzeczownikiem do bezpośredniego doklejenia po czasowniku. Nie zmieniono
tej kategorii ani istniejących ról innych czasowników. `aku` zachowuje swoją
listę `bag box`. Nie dopisano nieużywanych klas, np. masculine_inanimate.
Wszystkie pięć klas mechanizmu nadal sprawdzają izolowane testy B2.

Przykład przechowywanej formy:

```xml
<form ref="past_plain" kana="はたらいた" translation="pracowałem" kanji="働いた">
  <agreement_translations>
    <translation class="masculine_personal" value="pracował" />
    <translation class="feminine" value="pracowała" />
  </agreement_translations>
</form>
```

`agree:@item` odczytuje dokładnie formę i klasę wybranego rzeczownika.
Brak przypisania wyklucza realizację; nie ma powrotu do pierwszej osoby,
automatycznej koniugacji ani losowania rodzaju. `hito` nadal oznacza „osoba”
i zachowuje klasę feminine. Liczba mnoga pozostaje poza zakresem B3.

| Forma | Pytanie | Odpowiedź |
|---|---|---|
| dictionary | To jest osoba, która pracuje. | これははたらくひとです。 |
| plain_negative | To jest osoba, która nie pracuje. | これははたらかないひとです。 |
| past_plain | To jest osoba, która pracowała. | これははたらいたひとです。 |
| past_negative_plain | To jest osoba, która nie pracowała. | これははたらかなかったひとです。 |

Pozostałe przykłady: „To jest pies, który spał.” (`これはねたいぬです。`),
„To jest torba, która nie otworzyła się.” (`これはあかなかったかばんです。`),
„To jest pudełko, które otworzyło się.” (`これはあいたはこです。`).
Są to formy proste; wzorzec nie dodaje znaczenia trwającej właśnie czynności
z konstrukcji `ている`.

### Studio i quiz

W Studio wybierz kategorię `przydawki` i nowy wzorzec. Wybór dozwolonych form
zawiera cztery wskazane formy; inne wpisy katalogu pozostają dostępne w edytorze,
ale nie należą do tego wzorca. W słowniku czasowników zaznacz formę i wybierz
„Tłumaczenia według rodzaju”. Puste wiersze oznaczają brak obsługi klasy.
Szczegóły zapisu i tabeli:
[B2](https://github.com/MaciejPotas/Kotomi/blob/main/docs/pl/verb_form_agreement.md).

Quiz `relative_clauses` zawiera obie referencje. W Windows i Mobile zaznacz tylko
„Zdania przydawkowe”, tylko „Zdania przydawkowe podmiotowe” lub oba wzorce.
Włącz styl potoczny i odpowiednie czasy/polaryzacje. Hint pokazuje wyłącznie
wybrany czasownik i rzeczownik, bez niewidocznego kontekstu i gotowej odpowiedzi.
Interfejs oraz pakiet quizu pozostają wspólne i nie wymagają zmian.

### Walidacja i warunek integracji

Na niepoprawionym B2 katalog `existential` dopuszczał również `iru` i
`aru_existential`, np. „osoba, która nie ma”. To błąd granicy między zwykłym
uzgodnieniem podmiotu a katalogiem konstrukcji egzystencjalnej. [Kotomi #213](https://github.com/MaciejPotas/Kotomi/pull/213)
odrzuca niepowiązany rekcją podmiot rzeczownikowy dla tego katalogu. Zachowuje
konstrukcje z `government`, uzgodnienie z ilością i stare liczenie. Nie należy
usuwać cech tych czasowników ani dopisywać sztucznych tłumaczeń w Content.
**Najpierw należy zintegrować poprawkę Kotomi, potem wdrażać Content 60.**

Odrzucone połączenia obejmują `hataraku + book/inu/hitori`, `neru + car/hitori`,
`aku + hito/book` oraz niejawne `iru/aru_existential`. Rzeczowniki i stare
przydawki dopełnieniowe pozostają bez zmian.

Wynik: 20 par słów (8 + 10 + 2), 20 unikalnych pytań i odpowiedzi na formę,
80 unikalnych par tekstów łącznie. 100 realizacji na formę i 400 łącznie
uwzględnia pięć niewypisywanych kontekstów. Nie są to 400 różne zdania.

[Raport walidacji i wszystkie 80 par](../validation/subject_relatives_b3.json)
oraz [surowe pomiary](../validation/subject_relatives_b3_performance.json).
Uruchomienie walidacji wydania opisuje [tools/README.md](../../tools/README.md).
To jawna walidacja produkcyjnego Content, poza testami jednostkowymi.
Automatyczne testy używają niezależnych fixture'ów. Sprawdzono wspólne ścieżki
oraz kontrolki bez ekranu; nie wykonano manualnego testu fizycznego Windows/Androida.

Dodatkowy [test UI bez ekranu](../validation/subject_relatives_b3_ui.json)
sprawdza dwa cykle kontrolera Mobile, trzy wybory wzorców, 48 pytań oraz
12 przykładów przez rzeczywisty callback symulatora, bez ponownego ładowania projektu.
