# Zdania przydawkowe w Content

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
każdego połączenia znaczeń. Przykładowo szeroka kategoria `abstract` dopuszcza
`sukuu` z `fukushuu` (ratować powtórkę). Nie dodano wyjątków ani słownika
dobrych zdań do silnika.

Zakres pozostaje pojedynczy i dopełnieniowy. `okane` ma klasę liczby mnogiej,
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
