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
generator japońskiej odmiany. Reguły nie są kopiowane do Data.

ERROR oznacza naruszenie kontraktu lub brak wymaganego pola. WARNING oznacza
prawdopodobny brak danych albo potrzebę weryfikacji. INFO obejmuje jawne wyjątki
`nouns`, rozpoznane warianty odmiany i opcjonalne dane. Nieznana różnica względem
generatora pozostaje WARNING, ale nie jest automatycznie brakiem danych.
`affects_completeness` określa wpływ każdej uwagi na kompletność. `review_notes`
liczy uwagi bez takiego wpływu, a nie niekompletne słowa. JSON oddziela `errors`,
`warnings`, `info` i kompletność słowników. Kompletność dotyczy sprawdzonych
kontraktów, nie wszystkich możliwych zastosowań gramatycznych.

Inwentarz rozdziela formy zapisane, `generated_forms` (możliwe do wygenerowania
przy edycji), `optional_forms_not_explicit` (bez wykazanego obowiązku zapisu),
`unsupported_by_generator` i `missing_required_forms`. Brak obsługi generatora
nie dowodzi, że forma jest językowo niemożliwa. Nie ma uniwersalnych metadanych
obowiązkowości ani produktywności form dla każdego słowa; `requirements_status`
raportuje tę niepewność. `absent_catalog_forms` pozostaje surową listą zgodną
ze starszym formatem. `selectable_catalog_forms` pochodzi z aktualnego rejestru.

Znany obowiązek wynika z konkretnego słowa i stałego selektora formy we wzorcu,
przeanalizowanych przez engine. Generator nie uzupełnia form w runtime i nie
potwierdza tłumaczeń. Dlatego brak wymaganej zapisanej formy pozostaje WARNING,
nawet jeśli można wygenerować jej kana. Otwarte sloty, dynamiczne formy quizu,
dziedziczenie form i pełną poprawność kontekstu sprawdza diagnostyka solvera.
Lista Studio pokazuje także formy stałe; `eligible_form_names` ogranicza dynamiczne
formy quizu, nie definiuje obowiązkowej listy form każdego czasownika.

Brak ogólnej translacji przy dostępnych `target_translation` lub
`agreement_translations` daje INFO o niezweryfikowanym pokryciu innych kontekstów.
Bez żadnego tłumaczenia formy audyt zgłasza WARNING wpływające na kompletność.
Audyt nie generuje tłumaczeń. Błąd parsera daje kod 1 i informację o przerwanym
skanowaniu. Ostrzeżenia i informacje same nie zmieniają kodu 0.

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

Wyniki audytu bieżącej rewizji: [raport JSON](../validation/developer_tools_audit.json). 380 słów, 0 błędów, 0 ostrzeżeń, 24 informacje: 15 deklaracji wyjątków nouns oraz 9 wariantów odmiany przymiotników. 122/122 czasowników ma pokrycie; 22 słowa pozostają bez potwierdzonego użycia leksykalnego w patternach. Literały kana we wzorcach nie są referencjami do słownika. Audyt nie zmienił słów ani ich tłumaczeń.
