# Tworzenie quizów zdań w Studio

Utwórz quiz, wpisz nazwę i opis, a następnie wybierz wzorce zdań lub wzorce złożone.
Opcjonalnie udostępnij filtr typu słowa, kategorii albo cechy. Zapisz projekt po
walidacji. Quiz pojawi się w menu bez nowego pakietu Pythona. Quizy lekcji zachowują
dotychczasowe działanie.

Gracz korzysta ze wspólnych ustawień i prezentacji pytań dla wszystkich profili
zdań. Wartości jednego filtra są alternatywami, a niezależne filtry muszą być
spełnione jednocześnie. Trzeba zaznaczyć przynajmniej jedną wartość. Profil z filtrem
typu przymiotnika pozwala wybrać i, na albo oba typy. Prosta struktura przymiotnikowa
udostępnia również 1-3 słowa w zdaniu. Transformacja plain/polite zachowuje słowa
i kontekst, zmieniając formy.

Wzorce liczenia zachowują wspólny opcjonalny zakres liczb. Ograniczenia wzorca nadal
obowiązują; stałe wartości i nazwane zbiory liczb pozostają zachowane. Rozłączne
zakresy nie tworzą żadnego pytania. Profile zdań przydawkowych nie dostają dodatkowych
filtrów słownikowych, dopóki autor ich nie wybierze.

Czasowniki, Przymiotniki i Dostępność zachowują identyfikatory profili, wybrane
wzorce i ustawienia. Oryginalne pliki ustawień są zachowane; migracja następuje tylko,
gdy nie istnieje jeszcze plik ustawień profilu. Pozostają dwa pakiety wykonawcze:
`grammar` i `lessons`. Usunięcie lub zmiana nazwy profilu nie przywraca starego silnika.

Kolejność aktualizacji: aplikacja 1.1.11 lub nowsza, Content w rewizji 72 lub nowszej,
a następnie zatwierdzona Quiz Update (katalog 1.1.13, Grammar 1.1.12). Quiz Update
weryfikuje pliki zastępcze przed atomowym wycofaniem trzech starych pakietów pierwszej
strony. Starszy Content blokuje usuwanie. Ustawienia, postęp i niezależne pakiety
użytkownika pozostają zachowane. Po aktualizacji pakietów uruchom aplikację ponownie.
Cofnięcie Content poniżej 72 lub ponowna instalacja wycofanego katalogu nie jest
obsługiwana; należy odtworzyć kompletną zgodną kopię instalacji. Ustawienia i generowanie
quizów lekcji nie zmieniają się.

Zmiana nazwy profilu zachowuje identyfikator i ustawienia. Po wyczerpaniu puli pytań
sesja kończy się normalnie.

Tryby, kierunki i formy wynikają z wybranych wzorców. Przy mieszanym wyborze używane
są tylko wzorce obsługujące wybrany tryb; nie trzeba odznaczać pozostałych. Stałe
wzorce liczbowe udostępniają zwykłe generowanie i zakres, bez opcji transformacji.
Forma występująca tylko w polskim poleceniu nie oznacza możliwości transformacji
japońskiej odpowiedzi. Zmiana wzorców lub form odświeża dostępne opcje. Jeśli zapisany
tryb przestał być obsługiwany, ustawienia wyjaśniają zmianę i wybierają dostępny tryb,
zachowując pozostałe wybory.

Next przygotowuje pytania w wątku roboczym i w razie potrzeby używa istniejącego
wskaźnika ładowania. Ponowne żądanie Next jest ignorowane podczas przygotowania.
Wyjście z quizu anuluje oczekujące przygotowanie; spóźniony wynik nie aktualizuje
opuszczonego ekranu. Wyszukiwanie pozostałych pytań jest leniwe i wznawia się od
poprzedniej pozycji. Start nie wylicza całej puli pytań.
