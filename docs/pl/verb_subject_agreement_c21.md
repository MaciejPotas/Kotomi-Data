# C2.1: uzgodnienie czasowników z podmiotem

Content 61 wdraża dokładnie 62 operacje `changes` z
[zatwierdzonych propozycji C1](../validation/verb_dictionary_proposals_c1.json):
56 tłumaczeń uzgodnionych w 28 formach i sześć nowych ról `subject`.

Zakres to `shimaru`, `yomu`, `kaku`, `hanasu`, `kangaeru`, `sentakusuru`
i `soujisuru`. Pozostałe 26 czasowników kategorii A pozostaje do C2.2.
Propozycje B/C nie zostały zastosowane. Nie zmieniono silnika, DSL, wzorców,
rzeczowników, danych quizów ani ich manifestu.

Cztery formy to `dictionary`, `plain_negative`, `past_plain` i
`past_negative_plain`. Czynności ludzi mają klasy `masculine_personal` i
`feminine`; `shimaru` ma `feminine` i `neuter`. Nie ma dodatkowych klas,
liczby mnogiej ani nowych form. Wartości pochodzą wyłącznie z C1.

Sześć nowych ról dopuszcza dokładnie `friend mother sister teacher roujin hito
programmer madogiwazoku`. Istniejący podmiot `shimaru` nadal dopuszcza tylko
`bag box`. Nie dodajemy `accepts="person"`, ponieważ silnik łączy `accepts`
i `nouns` przez OR, co rozszerzyłoby listę m.in. o `hitori`.
Bazowe `translation`, kana, kanji, kolejność form, istniejące mapy, role
oraz rekcja pozostają niezmienione. XML zmieniono miejscowo, bez pełnej serializacji.

## Szybka kontrola i CI

```sh
python tools/validate_repository.py
python tools/validate_question_patterns.py
python -m unittest discover -s tests -v
```

Istniejący walidator repozytorium przekazuje już odczytane `verbs.xml` do małej
kontroli C2.1. Jedynym dodatkowym źródłem jest JSON propozycji C1. Kontrola
sprawdza siedem wpisów, dokładne role, mapy, klasy, formy, wartości, zależności
oraz duplikaty. Nie ładuje `QuizProject`, nie uruchamia quizu ani solvera.
Koszt dodatkowy to liniowe przejście po propozycjach oraz stała liczba wyszukań
w XML. Fixture nie potwierdzi wdrożenia danych w publikowanym pliku, dlatego
jest to kontrola wydania w istniejącym gate, poza testami jednostkowymi.

Piętnaście testów mutacyjnych korzysta wyłącznie z niezależnego,
wersjonowanego `tests/fixtures/c1/v1.json`. Testy odczytu map, wyboru klas,
negacji, przeszłości, braku fallbacku, zachowania tłumaczeń i zapisu już istnieją
w Kotomi (`test_verb_form_agreement.py`, `test_verb_agreement_persistence.py`,
`test_subject_relative_catalog_boundary.py`); nie duplikujemy silnika w Data.

Kontrola zależności wyznacza pełny oczekiwany zestaw z operacji dodania roli i
`subject_role_change`. Odrzuca brakujące, nadmiarowe, zduplikowane i nieprawidłowe
`depends_on`, także odwołanie do istniejącej, ale niewłaściwej operacji.

## Akceptacja integracyjna poza CI

Punkt odniesienia: Kotomi-Data `9227fd02c3c315c3d49ea9357a652a0a4d9c36bc`
(main przed C2.1) i Kotomi `9c01404465837f55d32ce1b4056fbb6e99817440`.

```sh
git worktree add --detach ../data-before 9227fd02c3c315c3d49ea9357a652a0a4d9c36bc
python tools/validate_verb_subject_c21_integration.py --kotomi ../Kotomi \
  --baseline-data ../data-before \
  --engine-revision 9c01404465837f55d32ce1b4056fbb6e99817440 \
  --baseline-revision 9227fd02c3c315c3d49ea9357a652a0a4d9c36bc \
  --output docs/validation/verb_subject_c21_validation.json
```

Skrypt odczytuje graf XML obu projektów, sprawdza pełne ładowanie i walidację,
minimalny diff, wszystkie realizacje obu przydawek, dokładne role, odrzucenia,
jawne i niejawne `agree`, polskie uzgodnienie i 100 pytań ze stałym ziarnem.
Pozostałe wzorce sprawdza tylko przez dostępność. Koszt rośnie z realizacjami
obu przydawek oraz liczbą wzorców i rzeczowników; narzędzie nie należy do CI.
Parametry rewizji są etykietami raportu; przed uruchomieniem zweryfikuj checkouty.

Wynik zapisano w [raporcie](../validation/verb_subject_c21_validation.json):
20 → 70 par czasownik/rzeczownik na każdą z czterech form, czyli 100 → 350
realizacji po uwzględnieniu pięciu kontekstów. To wynik tej bazy i konfiguracji,
nie gwarancja dla dowolnych filtrów quizu. Wszystkie 30 940 realizacji przydawek
dopełnieniowych są identyczne. Dostępność 92 wzorców × 4 form jest zachowana.
Przeszło 2068 kontroli odrzucenia niedozwolonego rzeczownika, kontrola renderowania
obu wariantów `agree` oraz 100 pytań. Oba projekty zgłaszają zero błędów.

## Wydajność i historia C1

[Surowe pomiary C2.1](../validation/verb_subject_c21_performance.json) używają
metody B3: naprzemienne świeże procesy przed/po, jeden CPU, osobne zimne i ciepłe
próby, siedem par rund, wszystkie próbki zachowane, mediana ilorazów sparowanych
rund. Zimna próba oznacza nowy projekt, nie zimny cache systemu operacyjnego.
Zakres to wczytanie, kompatybilność, dostępność, liczenie i pierwsze pytanie.
Przykład pojedynczego procesu, powtarzany naprzemiennie dla obu katalogów:

```sh
python tools/benchmark_subject_relatives.py --kotomi ../Kotomi \
  --data ../data-before --samples 7 \
  --operations load compatibility exists count first_question \
  --output before.json
```

Dla przydawek podmiotowych dodaj `--pattern 'Zdania przydawkowe podmiotowe'`
i użyj `--samples 21`. Domyślny pełny benchmark B3 pozostał bez zmian;
`--operations` jedynie ogranicza zakres pomiaru. Nie dodano benchmarków do CI.
Interpretację wyników zawiera [podsumowanie akceptacji](../validation/verb_subject_c21_acceptance.md).

C1 pozostaje nienaruszonym audytem historycznym. Przed zmianami przeszedł kontrolę
statyczną i silnikową na bazie, której słowniki są identyczne z przypiętym
`236bf6af22e897d103099a1166fb9a941d3ee1fd`. Jego walidator celowo wymaga braku
proponowanych wpisów, więc uruchamiaj go na `../data-before`, nie na Content 61:

```sh
python ../data-before/tools/validate_verb_dictionary_audit.py --kotomi ../Kotomi
```

Rewizja Content wzrosła z 60 do 61. Oficjalny builder Kotomi wygenerował manifest;
zmieniły się tylko hashe i URL-e `verbs.xml` oraz `content_revision.json`.
Nie zmienił się manifest ani wersja pakietów Quiz. Nie wykonano testów na fizycznych
urządzeniach; akceptacja dotyczy wspólnego silnika i danych.
