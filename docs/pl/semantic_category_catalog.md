# Kategorie rzeczowników definiowane w Content

`quiz_project.xml` deklaruje `<semantic_categories file="grammar/categories.xml" />`.
Pełny katalog ma korzeń `<noun_categories schema_version="2">` i wpisy, np.
`<category id="body_part" parent="concrete" label="Część ciała" />`.

Dodaj unikalne ID małymi literami, opcjonalnie jednego istniejącego rodzica,
etykietę i flagę `selectable="true|false"`. Wszyscy rodzice muszą być zadeklarowani
w tym katalogu. Wielu rodziców nie jest obsługiwanych. Rzeczowniki wybierają
kategorie oznaczone jako dostępne; czasowniki, przymiotniki i selektory mogą
ograniczać się do szerszych kategorii nadrzędnych. Zachowaj kategorie używane
przez domyślne role aplikacji i istniejące dane.

Najpierw trzeba zainstalować Kotomi z nowym loaderem. Kolejne kategorie wymagają
już tylko aktualizacji Content, jeśli nie wprowadzają nowego algorytmu gramatyki.
Starsze dane bez deklaracji korzystają z katalogu zgodności w Kotomi. Jawnie
zadeklarowanych ID nie przepisują migracje historycznych kategorii.

Po zmianie uruchom `python tools/validate_repository.py`,
`python -m unittest discover -s tests -v` oraz walidację strukturalną w Kotomi.
Samodzielny walidator sprawdza duplikaty, nieznane kategorie, dostępność wyboru,
brakujących rodziców i cykle. `tests/test_noun_category_catalog.py` ma małe,
niezależne dane testowe. Kotomi dodatkowo sprawdza ograniczenia wzorców i pokazuje
katalog w Studio. Kontrola zależności runtime/cache obejmuje ten plik.

Walidator Data sprawdza również jawne właściwości `category:id` w kanonicznych
tokenach `noun[...]` i `adverb[...]`, w pytaniu i odpowiedzi, także w szablonach
złożonych. Rzeczowniki korzystają z tego katalogu, a przysłówki z osobnego
katalogu słownika `adverbs`. Błąd wskazuje wzorzec, pole i nieznane ID.
To kontrola referencji, a nie drugi parser DSL: błędna składnia, niedozwolone
selektory, reguły aliasów i rozwijanie wzorców pozostają zadaniem Kotomi.
Dane bez `semantic_categories` zachowują dotychczasowe działanie. Testy
syntetyczne znajdują się w `tests/test_pattern_category_references.py`.

Zwiększ rewizję w `content_revision.json` i odtwórz `content_update_manifest.json`
narzędziem `write_content_manifest` z Kotomi. Kategorie, używające ich słowa i
wzorce muszą trafić do jednego kompletnego snapshotu Content. Deklaracja kategorii
nie zmienia tłumaczeń, form, algorytmu liczebników ani semantyki DSL.
