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

Kolejność aktualizacji: aplikacja 1.1.12 lub nowsza, Content w rewizji 72 lub nowszej,
a następnie zatwierdzona Quiz Update (katalog 1.1.14, Grammar 1.1.13). Quiz Update
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

## Filtry słownictwa

Edytor Studio pokazuje tylko skonfigurowane filtry. Wybierz **+ Dodaj filtr**, a następnie:

1. Wybierz element słownictwa. Okno pokazuje wzorce objęte filtrem, aby odróżnić role główne, zagnieżdżone i dopełnienia.
2. Wybierz typ słowa, kategorię semantyczną lub cechy gramatyczne. Właściwości bez wartości nie są proponowane.
3. Zaznacz wartości, z których może korzystać uczeń.
4. Wybierz niepusty zestaw domyślny i zapisz. Edycja i usuwanie zmieniają definicję, a nie bieżące ustawienia ćwiczenia ucznia.

W odtwarzaczu każdy skonfigurowany filtr korzysta ze wspólnych ustawień Windows/Mobile. Małe grupy mają checkboxy. W istniejących profilach typów przymiotników początkowo zaznaczone są i-adjective i na-adjective. Poprawny zapisany wybór ma pierwszeństwo. Odznaczenie obu jest błędem, nigdy domyślnym wyborem wszystkich słów.

Wartości jednej grupy łączy **OR**. Oddzielne grupy i dodatkowy filtr tekstowy łączy **AND**. Ograniczenia wzorca, zgodność semantyczna i zgodność form pozostają obowiązkowe. Powtórzone lub nakładające się kontrolki tej samej właściwości danego elementu są odrzucane, zamiast tworzyć ukryty dodatkowy warunek.

Elementy słownictwa i ich nazwy pochodzą z rozwiniętych alternatyw konstrukcji. Opcjonalny filtr dotyczy wyłącznie alternatyw zawierających jego element; inna poprawna alternatywa pozostaje dostępna. Obowiązkowe ograniczenia konstrukcji pozostają we wzorcu i uczeń nie może ich wyłączyć. Okno pokazuje objęte filtrem alternatywy. Niejednoznaczny element, usuniętą referencję lub niedostępną wartość trzeba poprawić przed zapisem. Zakresy liczb i łańcuchy przymiotników pozostają osobnymi ustawieniami zależnymi od możliwości wzorca.

Ustawienia należą do identyfikatora profilu. Po zmianie konfiguracji poprawne wartości pozostają zaznaczone, nieobsługiwane są usuwane, a domyślne wracają tylko wtedy, gdy wcześniejszy niepusty wybór utracił wszystkie wartości. Usunięcie filtra nie zeruje pozostałych ustawień. Istotna korekta jest wyjaśniana w istniejącym komunikacie ustawień. Jawnie pusty wybór pozostaje niepoprawny.

### Format definicji

Dotychczasowe `filters="adjective.type"` nadal udostępnia wszystkie dostępne wartości i domyślnie zaznacza wszystkie. Studio może dodatkowo zapisać:

```xml
<vocabulary_filters>
  <filter key="adjective.type"
          allowed="i_adjective na_adjective"
          defaults="i_adjective na_adjective" />
</vocabulary_filters>
```

Klucz należy do listy `filters` quizu; loader obsługuje też klucz zadeklarowany bezpośrednio w `vocabulary_filters`. Zestawy dozwolony i domyślny są niepuste, a wartości domyślne muszą należeć do dozwolonych. Autor korzysta z okna edycji, a nie XML ani DSL. Rozszerzony kontrakt wymaga Application 1.1.12+ i Grammar 1.1.13+. W tym wydaniu Content pozostaje w rewizji 72, a istniejące definicje profili nie zmieniają się.

Jeśli gramatyka języka źródłowego jest czasowo niedostępna, definicje filtrów i zapisane wybory pozostają zachowane. Sprawdzanie elementów wraca po udostępnieniu tej gramatyki.
