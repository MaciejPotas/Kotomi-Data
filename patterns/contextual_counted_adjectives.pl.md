# Przymiotniki w konstrukcjach liczebnych, etap 4A

[English](contextual_counted_adjectives.md)

W quizie **Liczenie** jest nowy pattern: **Istnienie policzonych opisanych rzeczowników**.
Dotychczasowy wariant bez przymiotnika zostaje. Pełna definicja nowego wygląda tak:

```xml
<sentence_pattern id="Istnienie policzonych opisanych rzeczowników" category="counting" semantics_version="2">
  <question>{verb@existence[role:subject, feature:existential, form, agree:@count].translation} {number@count[set:one_to_ten, agree:@item, case:@item].translation} {adjective@quality[form:attributive_nonpast, agree:@item].translation} {noun@item[quantity:@count, government:@existence]}.</question>
  <answer>{adjective@quality[form:attributive_nonpast]}{noun@item}が{counter@unit[counts:@item, preferred, quantity:@count]}{verb@existence[role:subject, feature:existential, form]}。</answer>
</sentence_pattern>
```

## Dlaczego wystarcza `agree:@item`?

Przymiotnik wskazuje liczony rzeczownik, więc planer zna już jego rodzaj, ilość,
profil ilości i formę orzeczenia. Z tych danych wyznacza klasę i przypadek
przymiotnika. Powiązanie wynika z aliasów, nie z kolejności słów w zdaniu.

| Ilość | Zdanie twierdzące | Zdanie przeczące |
|---|---|---|
| jedna | czerwona książka | jednej czerwonej książki |
| trzy | czerwone książki | trzech czerwonych książek |
| pięć | czerwonych książek | pięciu czerwonych książek |

Profil `one` z `fallback="noun_case"` zachowuje klasę rzeczownika. Profile `few`
(`paucal`) i `many` (`genitive_plural`) dają przymiotnikowi klasę liczby mnogiej
niemęskoosobowej. `many` wymaga dopełniacza, także gdy cała konstrukcja ma mianownik.
Negacja daje dopełniacz wszystkim trzem profilom. Dlatego w zdaniu „Było pięć
czerwonych książek” orzeczenie ma uzgodnienie nijakie, a przymiotnik jest w
dopełniaczu liczby mnogiej.

W semantyce 1 nic się nie zmienia: `agree` ustala uzgodnienie, a `case` może osobno
wskazać przypadek. Poza tą konstrukcją jawny przypadek nadal działa. Przy nowym
przymiotniku kontekstowym **każde jawne `case` jest błędem**, również `case:@item`.
Nie dodajemy składni nadpisania. Dzięki temu zmiana liczby albo negacji nie zostawi
sprzecznych instrukcji w patternie.

## Jak to działa w silniku?

Istniejący `CountedConstruction` ma teraz opcjonalny przymiotnik. Cztery żądania
w `RealizationPlan` zależą od wszystkich czterech wyborów oraz efektywnej formy
orzeczenia. Brak wyboru daje `Pending`. Brak zapisanej odmiany przy kompletnych
wyborach daje `Unsupported`. Błędne powiązania i katalogi nadal zgłaszają błędy
konfiguracji. Solver MRV, podgląd, bound rendering i wyjaśnienia korzystają z tej
samej operacji `InstructionLanguage.counted_construction`.

Polskie reguły pozostają w `kotomi/languages/polish/constructions.py`. Odczytujemy
istniejące `agreement_forms` i katalog form atrybutywnych. Nie zgadujemy końcówek.
Brak wymaganej formy żeńskiej, nijakiej w mianowniku lub mnogiej nie może dać
zastępczo męskiej formy pojedynczej. Ograniczenia `describes` nadal obowiązują.
Japońskie przymiotniki i/na, countery oraz wybór `ある`/`いる` działają jak wcześniej.

Plan nie przechowuje gotowych realizacji. Cache jest ograniczony do jednego
wyszukiwania, więc kolejne generowanie widzi zmiany danych i gramatyki.
Duże zakresy liczb pozostają leniwe; dobór przymiotnika nie enumeruje miliona
wartości. Nie dokładamy losowań ani nowego solvera.

Silnik generuje m.in. „Jest jedna czerwona książka”, „Są trzy czerwone książki”,
„Było pięć czerwonych książek” i „Nie było trzech czerwonych książek”. Po japońsku:
`あかいほんがいっさつある。` oraz `あかいほんがいっさつあった。`.

## Zakres i bezpieczne wdrożenie

Obsługujemy rzeczowniki żeńskie, nijakie, męskie nieżywotne i męskie żywotne.
Jest jedna polska realizacja przymiotnika i japońska forma atrybutywna tego samego
wyboru. Dwa konteksty, niezależne odmiany powtórzonego przymiotnika, adresowanie
wystąpień i łańcuchy pozostają na 4B lub później. Nie rozszerzamy tego etapu o
męskoosobowość, pluralia tantum ani liczebniki zbiorowe.

Aplikacja ma wersję **1.4.0**, Content rewizję **51**, a minimalna wersja aplikacji
w danych to **1.4**. Semantyka pozostaje w wersji 2; rozszerzony zakres chroni
wymóg wersji aplikacji. Najpierw merge PR danych, potem PR Kotomi wskazujący
opublikowany commit danych. Jeśli sposób merge zmieni SHA, trzeba zaktualizować
pin. Stare aplikacje, także 1.3, odrzucą nowe dane przed instalacją. Nowa aplikacja
nadal odczytuje rewizję 50. Oba PR-y wymagają review i zielonego CI, bez automatycznego merge.
