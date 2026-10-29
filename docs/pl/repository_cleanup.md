# Architektura Content i audyt porządkowy — kontynuacja PR 93

[Repozytorium](../../README.md) · [Kontrakt kategorii](semantic_category_catalog.md) ·
[Polecenia developerskie](developer_tools.md)

## Odpowiedzialność i przepływ danych

Punktem wejścia jest `quiz_project.xml`: deklaruje słowniki, dane gramatyczne,
wzorce i quizy zdań. Kotomi ładuje najpierw gramatykę aplikacji, następnie opcjonalną
hierarchię kategorii Content oraz słowa i referencje. Przynależność do lekcji stanowi
osobny katalog; nie określa znaczenia słowa ani jego dostępności dla generatora.

| Katalog / źródło | Odpowiedzialność | Konsument / rozszerzanie |
|---|---|---|
| `grammar/categories.xml` | Pełna hierarchia semantyczna z jednym opcjonalnym rodzicem | Walidator Data i loader Kotomi; nowe ID tutaj, kontrola referencji, wybieralności i cykli |
| `grammar/contexts.xml` | Warianty leksykalnych kontekstów i referencje | Loader kontekstów i selekcja DSL; poprawne ID słowników |
| `grammar/counting.xml` | Powiązania liczników i zestawy liczb | Loader danych liczenia; algorytmy kompozycji w Kotomi |
| `dictionaries/` | Jawne słownictwo, formy, tłumaczenia, kategorie i powiązania | Generator i edytory; brak użycia w lekcjach nie oznacza zbędności |
| `patterns/` | Prosty/złożony DSL pytań i odpowiedzi oraz profile quizów zdań | Parser/renderer aplikacji; zmiana ID razem z referencjami złożeń i quizów |
| `lessons/` | Organizacja lekcji Schema 4 i referencje słowników/wzorców | Loader lekcji; słowo może należeć do wielu lekcji |
| `quizzes/` | Niezależnie wersjonowane wykonywalne paczki quizów | Rejestr/aktualizator quizów; poza rewizją danych Content |
| `tools/`, `tests/` | Walidacja i audyty opt-in, ograniczone fixtures mutacyjne | `validate_repository.py`, `validate_question_patterns.py`, `run_tests.py` |

Data zawiera deklaracje, nie drugi silnik gramatyczny. `validate_semantic_categories`
sprawdza kategorie słowników, a jawne ID kategorii kanonicznych tokenów DSL przekazuje
do `validate_pattern_category_references`. Pełny parsing i zgodność pozostają w
Kotomi. Content bez deklaracji katalogu kategorii zachowuje wcześniejsze działanie.
Dokładny zakres składni i granice parsera opisuje przewodnik kategorii.

Dodając deklarację, zmień właściwy XML i referencje, uruchom oba walidatory i testy
syntetyczne, następnie walidację strukturalną aplikacji. Zmiana publikowanych danych
wymaga przebudowy hashy/rewizji narzędziem publikacji; sama dokumentacja/narzędzia
nie wymagają podniesienia rewizji. Aktualizator śledzi ścieżki manifestu, w tym
kategorie, a cache uwzględnia te same źródła. Nie usuwaj słowa tylko dlatego, że
nie używa go żadna lekcja.

## Audyt całego repozytorium

Początkowa lista obejmuje wszystkie 172 pliki: 13 w słownikach, 4 w grammar,
9 we wzorcach, 3 w lekcjach, 61 dokumentów, 20 narzędzi, 28 testów/fixtures,
21 plików paczek quizów oraz główne manifesty, konfiguracje, launchery i CI.
Sprawdzono odbiorców manifestów/ścieżek, identyczność bajtową, importy i wywołania,
dynamiczne entrypointy, wejścia walidacji/raportów, CI i udokumentowane polecenia.
Brak importu nie stanowił dowodu bezpiecznego usunięcia.

| Kandydat / obszar | Decyzja | Dowód / weryfikacja |
|---|---|---|
| Cztery przekierowania `patterns/contextual_{counted_adjectives,existentials}*.md` | MERGE | Pary językowe identyczne bajtowo, wskazują `grammar_contexts.md` / `.pl.md`; bezpośrednia nawigacja zastępuje duplikaty |
| `grammar/categories.xml`, `contexts.xml`, `counting.xml` | KEEP | Jawni odbiorcy w projekcie/manifeście; różne role semantyki, kontekstów i liczników |
| Katalog kategorii zgodności w Kotomi | KEEP | Fallback starszego Content, nie drugi aktywny katalog Data |
| Wszystkie słowa/formy/kategorie/tłumaczenia | KEEP | Generator, symulator i quizy działają niezależnie od lekcji; XML leksykalny bez zmian |
| Wzorce, złożenia, profile quizów, lekcje | KEEP | Referencje manifestu/runtime; walidatory repozytorium i pytań sprawdzają powiązania |
| Publikowane kopie `quizzes/*` | KEEP | Osobny kanał wydań; źródła w `apps/*` Kotomi; deduplikacja zepsułaby niezależne instalacje |
| `_rules_for_slot` w publikowanym quizie gramatycznym | UNCERTAIN | Brak bezpośrednich wywołań, ale usunięcie wymaga osobno wersjonowanej publikacji quizu; pozostaje ze źródłową kopią |
| JSON propozycji C1 i decyzji C3 | KEEP | Wejścia `validate_repository.py` i walidatorów integracji; kontrakty wydania, nie zbędne raporty |
| Historyczne raporty akceptacji/wydajności | UNCERTAIN | Dowody przypiętych wydań i zewnętrznego review; brak dowodu zbędności |
| `tools/*`, główne launchery BAT | KEEP | CI, opisane CLI lub audyty opt-in; runtime nie musi ich importować |
| Testy i ograniczone fixtures | KEEP | Discovery i kontrakty mutacji; bez nowych asercji rzeczywistego inwentarza |
| Manifesty Content/quizów, rewizja i CI | KEEP | Celowe wejścia publikacji; dokumentacja nie zmienia payloadu ani rewizji |
| Lokalne cache, pyc i buildy | KEEP poza Git | Ignorowane pliki tymczasowe, nie artefakty publikowane |

## Weryfikacja i ograniczenia

Uruchom `python tools/run_tests.py`, `python tools/validate_repository.py` oraz
`python tools/validate_question_patterns.py`. Testy mutują niezależne fixtures;
opcjonalne kontrakty silnika mogą być pominięte bez ścieżki do Kotomi. Nie dochodzi
zależność od Kotomi, pełnego ładowania bazy ani generowania. Ta kontynuacja nie
zmienia żadnych bajtów publikowanych danych Content ani paczek quizów. Przypięcie
submodułu aplikacji nadal wskazuje nowy commit dokumentacyjny. Nie da się wykluczyć
zewnętrznych odbiorców historycznych raportów, stąd jawne decyzje UNCERTAIN.
