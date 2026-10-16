# Audyty ręczne i testy

Runner testów korzysta z aktywnego virtualenv, następnie `.venv`, potem `python`
z PATH. Używa zainstalowanego pytest; bez niego uruchamia istniejący unittest.
Przekazuje kod zakończenia, wypisuje podsumowanie frameworka i czas całej operacji.
Ścieżki grup testów oraz `--verbose` działają także w trybie unittest.
Zaawansowane opcje pytest wymagają pytest. Dwuklik zachowuje okno do odczytu.

```bat
run_tests.bat
run_tests.bat tests/test_semantic_categories.py --verbose
run_data_audit.bat --kotomi ..\Kotomi
run_data_audit.bat --dictionary verbs --verbose
run_data_audit.bat --output audit.txt --json audit.json
```

Audyt wymaga checkoutu Kotomi, automatycznie wykrywa rodzica podmodułu lub
sąsiedni katalog Kotomi. `--kotomi` wskazuje inną lokalizację, `--project` inny
manifest. Nie uruchamia GUI, nie zapisuje XML i nie generuje tłumaczeń.
Domyślny raport: `audit-results/data-audit.txt`. JSON jest opcjonalny.

Źródłem reguł są parser Kotomi, `QuizProject.validate`, walidacja pojedynczego
słowa `DictionaryService.validate_word`, katalog aktywnego języka i istniejący
generator japońskiej odmiany. Reguły nie są kopiowane do Data. ERROR oznacza
niespójność strukturalną lub brak pola wymaganego przez kontrakt słownika.
WARNING oznacza brak jawnego tłumaczenia formy, przypadku lub klasy agreement,
jawny wyjątek nouns albo różnicę względem generatora. Różnica odmiany może być
poprawnym wariantem językowym. „Incomplete” oznacza słowo wymagające przeglądu,
nie automatycznie błędne słowo. Błędy i ostrzeżenia są grupowane po słowniku i ID.

Nie każda forma z katalogu jest produktywna dla każdego słowa. Brakujące pozycje
trafiają do `absent_catalog_forms` w inwentarzu i trybu verbose, bez fałszywego
błędu. Formy wyliczane przez profile liczenia nie wymagają ręcznych wpisów.
`target_translation` i mapy `agreement_translations` są opcjonalne; wymagania
konkretnego wzorca weryfikuje solver w diagnostyce pokrycia Kotomi.
Błąd parsera kończy audyt z kodem 1 i jawną informacją, że pozostałych słów nie
przeskanowano. Po poprawieniu struktury uruchom audyt ponownie. Ostrzeżenia same
nie zmieniają kodu 0. Nieznany filtr słownika jest błędem.

CI pozostaje przy `tools/validate_repository.py`, unittest i
`tools/validate_question_patterns.py`. Testy audytora na małych fixture'ach są
częścią testów jednostkowych, ale rzeczywiste raporty jakości i pokrycia pozostają
manualne. Pokrycie czasowników, puste wzorce i niewykorzystane słowa sprawdza
`tools/diagnostics/run_diagnostics.bat` w Kotomi, bez drugiego solvera w Data.

Aktualne przykłady ról, rekcji i kategorii: [target](target_government_c32.md),
[kategorie](noun_role_categories_c3.md), [przydawki](relative_clauses.md).
`depends_on` jest polem operacji historycznych propozycji audytu JSON, nie
nowym atrybutem XML słowa lub roli. C1/C2 są raportami konkretnego etapu;
bieżącą kompletność sprawdza ten audyt na aktualnych danych.

Wyniki audytu bieżącej rewizji: [raport JSON](../validation/developer_tools_audit.json). 380 słów, 0 błędów, 24 ostrzeżenia: 15 deklaracji wyjątków nouns oraz 9 wariantów odmiany przymiotników. 122/122 czasowników ma pokrycie; 22 słowa pozostają bez potwierdzonego użycia leksykalnego w patternach. Literały kana we wzorcach nie są referencjami do słownika. Audyt nie zmienił słów ani ich tłumaczeń.
