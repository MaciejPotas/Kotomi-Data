# Tworzenie quizów zdań w Studio

Utwórz quiz, wpisz nazwę i opis, a następnie wybierz wzorce zdań lub wzorce złożone.
Opcjonalnie dodaj nazwane filtry obsługiwanych metadanych słownika. Zapisz projekt po
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

Bieżąca kolejność aktualizacji znajduje się na końcu tego przewodnika. Quiz Update
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

Szybkie filtry to nazwane skróty on/off do istniejącego zaawansowanego filtra słów. Wybierz **+ Dodaj szybki filtr**, wpisz nazwę, zaznacz jedną lub więcej pozycji słownictwa w **Dotyczy**, wybierz właściwość i odznacz niechciane wartości. Nowy filtr jest domyślnie włączony i początkowo obejmuje wszystkie dostępne zgodne wartości. Zapis wymaga nazwy, pozycji i co najmniej jednej wartości. Edycja zachowuje dotychczasowy identyfikator, ustawienie domyślne i wybrane wartości. Okno nie zawiera przełączników domyślnego włączenia ani wymaganej grupy.

Kompaktowe okno można skalować; Zapisz/Anuluj pozostają w stałej stopce. Przewijają się tylko wartości. Menu zakresu jawnie pokazuje zaznaczone pozycje i udostępnia **Wszystkie rzeczowniki**, **Wszystkie czasowniki** lub **Wszystkie przymiotniki**, gdy ma to zastosowanie. **Pokaż objęte wzorce** wyświetla cały zakres. Jedyna dostępna pozycja jest wybierana automatycznie. Escape anuluje; dostępne są aktywny jasny/ciemny motyw i nawigacja klawiaturą.

Studio centralnie rozpoznaje alternatywne wybory **typu**: co najmniej dwa filtry o identycznym pełnym zakresie pozycji i parami rozłącznych wartościach typu tworzą wymaganą grupę, jeżeli co najmniej jeden jest domyślnie włączony. Pojedynczy nowy filtr pozostaje opcjonalny. Ograniczenia kategorii, końcówki, cech i roli użycia pozostają opcjonalne także przy kilku filtrach. Istniejące jawne wymagane grupy są zachowywane, dopóki mają filtry. Jeśli edycja/usunięcie pozostawi taką grupę bez włączonego domyślnego filtra, jej pierwszy pozostały filtr staje się domyślny dla nowych użytkowników; zapisane stany uczącego się nie zmieniają się. Starsze definicje z wszystkimi domyślnymi stanami wyłączonymi pozostają opcjonalne, jeśli wcześniej nie były jawnie wymagane. Silnik odczytuje zapisaną politykę grup; nie wyznacza jej z ID quizu, liczby wartości słownika ani zmieniającego się słownictwa.

Uczący się widzi dokładnie jeden checkbox na nazwany filtr w Windows, Androidzie i Mobile Preview, również przy kilku pozycjach. Alternatywy i/na w profilu przymiotników początkowo włączają oba typy. Jedna alternatywa wybiera dany typ; wyłączenie obu pokazuje komunikat wskazujący wymagane opcje. Puste opcjonalne grupy nie dodają ograniczeń. Puste wymagane grupy są odrzucane przed generowaniem, oceną wykonalności, dokładnymi statystykami i wyszukiwaniem pozostałych pytań.

Wartości i włączone alternatywy dla **tej samej pozycji/właściwości używają OR**. Różne wybrane pozycje, właściwości, zaawansowany filtr słów oraz obowiązkowe warunki gramatyczne i semantyczne używają **AND**. Dla **Trzy lubiane rzeczy** wybierz Pierwszy, Drugi i Trzeci rzeczownik oraz Kategoria = Jedzenie. Wszystkie trzy pozycje muszą wtedy używać słownictwa z kategorii Jedzenie. Wybór tylko Pierwszego rzeczownika ogranicza wyłącznie tę pozycję. Wyłączenie pojedynczego checkboxa usuwa to dodatkowe ograniczenie.

Cele są stabilnymi tożsamościami pojęciowych ról z analizy wzorców. Przyjazne nazwy rozróżniają czasownik główny, czasownik wewnątrz konstrukcji, rzeczownik jako podmiot/dopełnienie i kolejne rzeczowniki. Powtarzające się etykiety zawierają kontekst konstrukcji/pozycji. Równoważne aliasy nie są dublowane; zapisany identyfikator zostaje zachowany. Stałe elementy gramatyczne nie są oferowane dla nowych filtrów; istniejące poprawne wybory nadal można edytować. Cel nieobecny w alternatywie konstrukcji złożonej nie dodaje tam warunku. Obecny cel bez zgodnego słownictwa wyklucza tę alternatywę. Niejednoznaczne powiązania lub nakładające się różne aliasy tej samej właściwości są odrzucane z wyjaśnieniem. Filtr nigdy nie wiąże się przez wyświetlaną etykietę.

Właściwości pochodzą z obsługiwanych metadanych Word/Entity i deklaracji słowników: Typ, Końcówka, Kategoria, Cechy i Rola użycia, gdy mają zastosowanie. Oferowane są tylko właściwości z wybieralnymi wartościami wspólnymi dla wszystkich wybranych pozycji. Wartości pochodzą z całych odpowiednich słowników, niezależnie od aktualnej wykonalności; znana wartość może nie dawać zgodnych pytań. Encje rzeczowników oferują Kategorię zgodnie z dotychczasowym kontraktem silnika. Kategoria nie dubluje zgodnościowego odczytu cech przez `Word.categories`. Nieobsługiwane atrybuty, formy i identyfikatory nie są oferowane.

Końcówka oznacza atrybut słownika, a nie zakończenie odmienionej odpowiedzi. `ending="ru"` może pasować do czasowników godan i ichidan; zaawansowany `verb.type=godan` dodatkowo zawęża wybór. Brak opcjonalnego atrybutu nie pasuje do wybranej wartości. Nowe wartości słownika pojawiają się automatycznie z normalizacją wielkości liter dotychczasowego parsera. Generowanie i zliczanie nadal realizują istniejący matcher i solver; nie powstaje nowy DSL ani silnik filtrowania.

### Definicja XML

```xml
<quick_filters required="adjective.type">
  <quick_filter id="i_adjectives" label="i-adjectives"
                target="adjective" property="type" values="i_adjective"
                default_enabled="true" />
  <quick_filter id="na_adjectives" label="na-adjectives"
                target="adjective" property="type" values="na_adjective"
                default_enabled="true" />
</quick_filters>
```

Filtr wielu pozycji używa opcjonalnej listy `targets` zamiast `target`:

```xml
<quick_filters>
  <quick_filter id="food_items" label="Jedzenie"
                targets="first second third" property="category" values="food"
                default_enabled="true" />
</quick_filters>
```

Wymagany jest dokładnie jeden atrybut: `target` albo `targets`. Cele są unikalnymi stabilnymi rolami; wszystkie mają wspólną właściwość i zestaw wartości. Dotychczasowy XML pojedynczego celu nie zmienia się. `required` to opcjonalna lista kluczy `target.property`; brak oznacza grupy opcjonalne. Każdy wymagany klucz musi istnieć i mieć włączony domyślny filtr. Identyfikatory są unikalne w quizie. Nazwy i wartości są niepuste. `default_enabled` przyjmuje true/false, a jego brak w starszym XML nadal oznacza false; Studio jawnie zapisuje true dla nowych filtrów. Quiz nie może mieszać nowych i starszych definicji.

### Zapisane ustawienia i starsze definicje

Ustawienia przechowują `quick_filter_states` według stabilnego ID. Zapisane stany mają pierwszeństwo przed domyślnymi; nowe ID używają wartości domyślnych; usunięte ID wywołują dotychczasową informację o korekcie. Inne ustawienia i zaawansowane wyrażenia są zachowane. Zmiana zakresu wielu pozycji zachowuje jeden stan i checkbox. Przygotowanie z pamięcią podręczną nadal stosuje bieżące wyrażenie profilu do pytań i dokładnych statystyk. Tymczasowy brak gramatyki źródłowej nie usuwa definicji filtrów ani ich stanów.

Jeśli aktualizacja Content unieważni pusty wybór, zapisane stany pozostają bez zmian. Start otwiera edytowalne ustawienia z lokalizowanym komunikatem; uczący się musi wybrać alternatywę. Sam odczyt nigdy nie nadpisuje oryginalnego pliku.

Pozostaje adapter starszego `filters` / `vocabulary_filters`. Niezwiązane zmiany w Studio zachowują ten XML. Edycja starszego skrótu jawnie konwertuje definicję, z komunikatem; następnie obowiązuje centralna polityka alternatyw typu. Bezstratnie reprezentowane dawne wybory stają się stanami checkboxów. Pozostałe ograniczenia i dawne granice dozwolonych wartości pozostają warunkami zaawansowanego filtra słów. W szczególności starsze ograniczenie jednej pozycji nie włącza po cichu nowego filtra wielu pozycji: skrót pozostaje wyłączony, a oryginalny warunek jednej pozycji jest zachowany. Dawny pusty wybór blokuje Start do przeglądu i zapisania ustawień. Wielokrotny odczyt/zapis nie dubluje ograniczeń.

### Motyw i kolejność aktualizacji

Zainstaluj Application **1.1.15+**, następnie katalog **1.1.17** (Grammar **1.1.16**), zanim zaczniesz tworzyć filtry wielu pozycji. Content **74** pozostaje bez zmian i deklaruje istniejącą wymaganą grupę typu przymiotnika. Grammar nadal obsługuje Content 72 przez adapter zgodności. Lessons pozostaje **1.1.9**. Nie zmieniono XML tłumaczeń ani niezwiązanego słownictwa.
