# C1: audyt czasowników

[Raport i komplet materiałów](../validation/verb_dictionary_audit_c1.md) obejmują
122 czasowniki, 1817 form oraz wszystkie ich deklaracje ról na przypiętych
rewizjach obu repozytoriów. Wynik: A 33, B 79, C 7, D 3.

Do późniejszego C2 przygotowano 308 jawnych tłumaczeń w 132 formach i 32 nowe
role `subject`. Wszystkie propozycje A sprawdzono na tymczasowej kopii danych.
Kategorie dotyczą czterech form priorytetowych i zwykłych przydawek podmiotowych;
pozostałe formy mają odrębne oceny. A nie jest certyfikacją całego czasownika.

C1 nie zmienia słowników, wzorców, quizów ani manifestów. C2 wymaga zatwierdzenia.
Pełne wartości i decyzje B/C są w raportach, ale tylko operacje `changes` w JSON
stanowią propozycje A do późniejszego wdrożenia.

Kontrola kompletności, uruchamiana osobno od testów jednostkowych:

```sh
python tools/validate_verb_dictionary_audit.py --kotomi ../Kotomi
```

Raport zawiera wyniki regresji, pomiary wydajności, ograniczenia językowe i plan
wdrożenia. Dokumentacja kontraktów silnika nie została zmieniona.

Po review `nonbiri_suru` zmieniono z A na B, a `tori` wyłączono z propozycji
`iku`, `kuru`, `deru`, `hairu`. Tłumaczeń produkcyjnych nie zmieniono.
`chigau/potential` i `wakaru/potential` nie są zatwierdzone jako zadania odmiany.

Bez `--kotomi` walidator sprawdza kompletność operacji, dokładne zależności,
statystyki, lokalne definicje ról i klasy podmiotów. Kontrole dopasowań OR,
dziedziczenia, wartości domyślnych ról i dostępności wykonuje oryginalny silnik
przy `--kotomi`; pominięte kontrole są jawnie wypisane.

Po review ponowiono eksperyment A i testy: 295 par, 1180 widocznych przykładów,
30940 niezmienionych realizacji dopełnieniowych, 57 testów Kotomi-Data
(z `KOTOMI_PATH`, w tym 23 nowe) oraz 162 testy Kotomi. Pomiary wydajności
zachowano jako historyczne; nie uruchomiono ich ponownie dla zmienionej propozycji.
