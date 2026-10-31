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

Dotychczasowe identyfikatory Czasowników, Przymiotników i Dostępności przechodzą na
profile po instalacji zmian z obu repozytoriów. Zapisane wybory i pasujące ustawienia
są migrowane jednokrotnie. Oryginalne pliki ustawień i stare pakiety pozostają na
potrzeby wycofania aktualizacji przy starszym Content. Aktualizację aplikacji należy
zainstalować przed aktualizacją Content. Ustawienia lekcji nie wymagają migracji.

Od rewizji Content 72 stare wpisy menu nie wracają po usunięciu migrowanego
profilu. Zmiana nazwy zachowuje identyfikator i ustawienia. Po wyczerpaniu
dostępnej puli pytań sesja kończy się wynikiem.
