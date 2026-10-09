# Migracja konstrukcji egzystencjalnej z liczebnikiem

English: [Migration notes](contextual_existentials.md).

Content w rewizji 51 wymaga Kotomi 1.4. Z `semantics_version="2"` korzystają dwa patterny:

- `Istnienie policzonych rzeczowników`, wprowadzony w rewizji 50 dla Kotomi 1.3;
- `Istnienie policzonych opisanych rzeczowników`, dodany w rewizji 51 dla Kotomi 1.4.

Oba są dostępne w quizie `counting` (Liczenie). Forma orzeczenia jest dynamiczna,
rzeczownik korzysta z jego rekcji, a liczebnik uzgadnia się z rzeczownikiem i
przypadkiem konstrukcji. Drugi pattern dodaje przymiotnik z samym `agree:@item`.
Jego efektywną klasę i przypadek wyznacza wspólny kontekst. Szczegóły i ograniczenia
opisuje [kontrakt etapu 4A](contextual_counted_adjectives.pl.md).
Nie zapisujemy gotowych orzeczeń jako stałego tekstu. Pattern
`Ile jest policzonych rzeczowników` pozostaje bez zmian, z semantyką 1.

Rewizja 50 uzupełniła żeński dopełniacz „jednej”, dopełniacze liczebników 3–10
oraz źródłową rekcję `existential_subject` dla `iru`. Rewizja 51 zachowuje te dane
i dodaje pattern z opisanym rzeczownikiem oraz jego wpis w quizie. Obecne formy
liczonych rzeczowników, przymiotników, japońskich liczników i czasowników pozostają
bez zmian. Reguły gramatyczne nadal należą do warstwy językowej Kotomi.

Obsługiwany zestaw liczb to 1–10. Testy integracyjne Kotomi obejmują rzeczowniki
żeńskie, nijakie, męskie nieżywotne i męskie żywotne, m.in. book, car, inu
i ringo. Nie oznacza to obsługi liczebników zbiorowych, męskoosobowości,
pluralia tantum ani polskich form dowolnej liczby generowanej.

Ćwiczenia przeczące opisują brak wskazanej grupy N przedmiotów. Nie utożsamiają
różnych zakresów negacji ani nie stwierdzają automatycznie, że łączna liczba
wynosi zero. Zakres ćwiczenia i przepływ realizacji opisuje dokument Kotomi
`docs/contextual_existentials.pl.md`.

Najpierw można zmergować PR danych, potem zgodny PR Kotomi wskazujący sprawdzony
commit. Kotomi 1.3 i starsze odrzucają wymóg 1.4 przed instalacją rewizji 51.
Wersja 1.3 rozumie pierwotną konstrukcję semantyki 2, ale nie obsługuje jej
rozszerzenia o przymiotnik kontekstowy. Nie należy omijać tej kontroli ani ręcznie
instalować nowej rewizji w nieobsługiwanej wersji aplikacji.
