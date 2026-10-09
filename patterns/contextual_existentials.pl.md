# Migracja konstrukcji egzystencjalnej z liczebnikiem

English: [Migration notes](contextual_existentials.md).

Content w rewizji 50 wymaga Kotomi 1.3. Tylko pattern
`Istnienie policzonych rzeczowników` włącza `semantics_version="2"`: forma
orzeczenia jest dynamiczna, rzeczownik korzysta z jego rekcji, a liczebnik
uzgadnia się z rzeczownikiem i przypadkiem konstrukcji. Nie zapisujemy gotowych
orzeczeń jako stałego tekstu. Pattern `Ile jest policzonych rzeczowników`
pozostaje bez zmian.

Uzupełnienia danych to żeński dopełniacz „jednej”, dopełniacze liczebników 3–10
oraz źródłowa rekcja `existential_subject` dla `iru`. Obecne formy „dwa”, formy
liczonych rzeczowników, japońskie liczniki i formy czasownika pozostają bez
zmian. Reguły gramatyczne nadal należą do warstwy językowej Kotomi.

Obsługiwany zestaw liczb to 1–10. Testy integracyjne Kotomi obejmują rzeczowniki
żeńskie, nijakie, męskie nieżywotne i męskie żywotne, m.in. book, car, inu
i ringo. Nie oznacza to obsługi liczebników zbiorowych, męskoosobowości,
pluralia tantum ani polskich form dowolnej liczby generowanej.

Ćwiczenia przeczące opisują brak wskazanej grupy N przedmiotów. Nie utożsamiają
różnych zakresów negacji ani nie stwierdzają automatycznie, że łączna liczba
wynosi zero. Zakres ćwiczenia i przepływ realizacji opisuje dokument Kotomi
`docs/contextual_existentials.pl.md`.

Najpierw można zmergować PR danych, potem zgodny PR Kotomi wskazujący sprawdzony
commit. Stare Kotomi przypina stare dane, a jego updater odrzuci wymóg 1.3 przed
instalacją rewizji 50. Nie należy omijać tej kontroli ani ręcznie instalować
nowej rewizji w Kotomi 1.2.
