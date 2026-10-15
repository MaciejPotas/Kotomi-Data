# C1: audyt czasowników

[Raport i komplet materiałów](../validation/verb_dictionary_audit_c1.md) obejmują
122 czasowniki, 1817 form oraz wszystkie ich deklaracje ról na przypiętych
rewizjach obu repozytoriów. Wynik: A 34, B 78, C 7, D 3.

Do późniejszego C2 przygotowano 316 jawnych tłumaczeń w 136 formach i 33 nowe
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
