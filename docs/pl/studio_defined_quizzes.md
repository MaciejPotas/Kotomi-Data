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

## Szybkie filtry

Szybkie filtry to nazwane skróty on/off do istniejącego zaawansowanego filtra słów. Wybierz **+ Dodaj szybki filtr**, wpisz nazwę, wybierz rolę słownictwa i właściwość, zaznacz jedną lub więcej wartości oraz opcjonalnie włącz skrót domyślnie. Edycja i usuwanie działają na kompaktowych wierszach. Edytor nie zawiera wyboru osobnych wzorców, kolumny dozwolonych wartości ani ustawień domyślnych dla każdej wartości.

Uczeń widzi jeden checkbox na skrót, oparty na wspólnym modelu ustawień Windows i Mobile. Etykietą jest nazwa filtra. Zaawansowany filtr słów pozostaje dostępny. Profil przymiotników definiuje w XML dwa skróty, i-adjectives i na-adjectives, domyślnie włączone. Oba włączone wybierają oba typy, jeden wybiera swój typ, a oba wyłączone nie dodają ograniczenia typu.

Włączone skróty dla **tej samej roli i właściwości łączy OR**, również dla wielu wartości jednego skrótu. Różne grupy i zaawansowany filtr słów łączy **AND**. Puste grupy nie dodają ograniczenia. Istniejący parser i solver zgodności obsługują generowanie, wykonalność, dokładne statystyki i wyczerpanie pytań. Obowiązkowe ograniczenia gramatyczne i semantyczne zawsze obowiązują. Nie powstaje drugi silnik filtrów ani rozszerzenie DSL gramatyki.

Cele filtrów to role w całym quizie, odczytywane z przeanalizowanych aliasów: czasownik główny, czasownik zagnieżdżony, rzeczownik, rzeczownik zagnieżdżony, przymiotnik lub inna jednoznaczna rola. Edytor nie pokazuje identyfikatorów wygenerowanych wzorców ani zakodowanych selektorów pojedynczych slotów. Brak danej roli w alternatywie oznacza brak ograniczenia dla tej roli. Obecna rola bez zgodnych kandydatów wyklucza daną alternatywę. Jeśli nie pozostaje żadna zgodna alternatywa, pojawia się zwykły komunikat o braku pytań, a skrót pozostaje włączony. Nakładające się różne aliasy tej samej właściwości są odrzucane; alternatywy OR powinny używać tego samego celu.

Wartości pochodzą z całych właściwych słowników i ich zadeklarowanych metadanych, a nie z kandydatów jednego wzorca. Znana wartość może obecnie nie dawać żadnych zgodnych pytań. Dialog wyraźnie informuje o tej możliwości. Kategoria jest dostępna dla rzeczywistych metadanych kategorii; zgodnościowy fallback `Word.categories` do cech nie tworzy zdublowanej kontrolki kategorii. Zaawansowany filtr zachowuje dotychczasową semantykę. Zakresy liczb i łańcuchy przymiotników pozostają osobnymi istniejącymi ustawieniami.

### Definicja XML

```xml
<quick_filters>
  <quick_filter id="i_adjectives" label="i-adjectives"
                target="adjective" property="type" values="i_adjective"
                default_enabled="true" />
  <quick_filter id="na_adjectives" label="na-adjectives"
                target="adjective" property="type" values="na_adjective"
                default_enabled="true" />
  <quick_filter id="people_animals_food" label="Ludzie, zwierzęta i jedzenie"
                target="noun" property="category" values="person animal food"
                default_enabled="false" />
</quick_filters>
```

ID jest unikalne w quizie i nie zmienia się po edycji nazwy, warunku ani stanu domyślnego. Nazwa i wartości są niepuste. Jeden skrót ma jeden cel, jedną właściwość i jedną lub więcej wartości. `default_enabled` ma wartość `true` albo `false` (pominięcie oznacza false). Elementy znajdują się w istniejącej definicji quizu, obok `patterns`. Quiz nie może mieszać nowych i starszych definicji filtrów.

### Zapisane ustawienia i starsze definicje

Nowe ustawienia zapisują `quick_filter_states` według stabilnego ID. Zapisany stan ma pierwszeństwo przed domyślnym; nowe ID korzysta z wartości domyślnej; usunięte ID jest odrzucane z istniejącym komunikatem korekty. Pozostałe ustawienia i zaawansowane warunki pozostają zachowane. Filtry korzystają z istniejącej tożsamości cache zależnej od słownictwa i nie czyszczą innych cache. Czasowa niedostępność gramatyki języka źródłowego nie usuwa zadeklarowanych skrótów ani ich stanów.

Starszy XML `filters` / `vocabulary_filters` jest nadal odczytywany przez adapter zgodności, który tworzy jeden skrót na dawną wartość. Niezwiązana edycja w Studio zachowuje ten XML. Edycja/usunięcie jego skrótu jawnie konwertuje definicję na opcjonalne szybkie filtry; Studio pokazuje informację o konwersji. Dawnych kolumn wartości dozwolonych i domyślnych już nie ma.

Starsze wybory i/na i inne wybory, które można dokładnie odwzorować, stają się stanami checkboxów. Jeśli ograniczenia nie można odwzorować dokładnie, pozostaje ono warunkiem zaawansowanego filtra słów, a skróty tej grupy są wyłączane, aby nie dodać przypadkowego przecięcia. Dawne jawne ograniczenia wartości dozwolonych przez autora również pozostają zaawansowanymi warunkami w zapisanych ustawieniach. Można je sprawdzić i zmienić w istniejącym edytorze zaawansowanym. Dawny pusty wybór był błędny, więc nie staje się po cichu brakiem ograniczeń: uruchomienie wymaga sprawdzenia i zapisania ustawień. Odczyt nie nadpisuje oryginalnego pliku. Powtarzany odczyt/zapis nie dopisuje powtórzonych warunków.

### Motyw i kolejność aktualizacji

Edytor quizów i dialog skrótu używają aktywnego motywu Studio dla natywnych pól tekstowych/list, kontenerów przewijania i etykiet/pól ttk. Zmiana motywu odświeża kolory bez przebudowy modelu quizu. Nawigacja klawiaturą, Escape i przewijanie pozostają dostępne.

Zainstaluj Application **1.1.13+**, następnie Content **73**, a potem zatwierdź katalog **1.1.15** (Grammar **1.1.14**). Pakiet nadal obsługuje Content 72 przez adapter zgodności. Content 73 deklaruje dwa skróty przymiotników w XML. Lessons pozostaje **1.1.9**. XML tłumaczeń i niezwiązane słowniki nie są zmieniane.
