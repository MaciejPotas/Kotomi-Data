# C2.2: kategorie podmiotów i zakończenie kategorii A

## Zakres i zgodność

Content 62 bazuje na C2.1, commit `83c36863ee56f606a00a1f02f38d8d75d0595193`.
Wdrożono 26 kolejnych czasowników, 252 tłumaczenia uzgodnione i 26 ról podmiotowych.
Łącznie C2.1 i C2.2 obejmują 33 czasowniki A, 308 dodanych tłumaczeń i 32 dodane role.
Wszystkie wartości, klasy i cztery formy pochodzą bez zmian z zatwierdzonego C1.
Bazowe tłumaczenia, kana, kanji, pozostałe formy, role object/target/location i rekcja
pozostały bez zmian. Dokumenty C1 oraz C2.1 i historyczne wyniki zachowano.

Nowe czasowniki: `aruku`, `asobu`, `ayamaru`, `deru`, `hairu`, `harau`, `hashiru`,
`iku`, `isogu`, `kaeru`, `kau`, `kikokusuru`, `kotaeru`, `kuru`, `matsu`, `nomu`,
`okoru`, `omou`, `oyogu`, `renshuusuru`, `taberu`, `undousuru`, `usowotsuku`,
`utau`, `warau`, `shinjiru`.

## Role oparte na kategoriach

Zamiast list osób stosujemy `<role ref="subject" accepts="person" />`.
Nowy rzeczownik `brother` z kategorią `person` jest zgodny z rolą bez edycji
czasownika. Dotyczy to też sześciu czasowników C2.1 i wcześniejszego `hataraku`.

Spośród migrowanych czasowników `accepts="person animal"` mają: `asobu`, `deru`, `hairu`, `hashiru`, `iku`,
`kaeru`, `kuru`, `matsu`, `nomu`, `oyogu`, `taberu` oraz wcześniejszy `neru`.
Dopuszczają całą kategorię zwierząt, w tym nowe `cat`. Historyczne ograniczenia
C1 do `inu` świadomie poszerzono również o `tori`. Nie dodano wyjątków `nouns`.
Pozostałe migrowane role dopuszczają tylko `person`.

To świadoma ogólna polityka kategorii: nie modeluje umiejętności pojedynczych
gatunków, np. pływania. Nowy rzeczownik nadal wymaga poprawnych przypadków i klasy
uzgodnienia obsługiwanej przez formę czasownika. C2.2 nie dodaje klas uzgodnienia
ani odmiany mnogiej; np. przyszły podmiot rodzaju nijakiego wymaga osobnego
zatwierdzenia jego tłumaczeń. Listy `bag box` dla `aku` i `shimaru` nie zmieniły się.

## Hitori i lekcja

`hitori` oznacza realizację liczebności jednej osoby. Usunięto ten wpis ze wspólnego
słownika rzeczowników, pozostawiając bez zmian cały `counters.xml`, w tym
`nin` + `number="1"` → `ひとり / 一人 / hitori`.

Jedyną referencję `nouns:hitori`, w `ola_l24_dokkai_nouns`, zastąpiono istniejącym
formatem `local_word`: zachowano ID `ola_l24_dokkai_nouns_005`, znaczenie
„jedna osoba”, kana i kanji. Lekcja słownictwa zachowuje wyrażenie; lokalne słowo
nie rozszerza globalnej kategorii `person` ani ról gramatycznych.

## Walidacja i CI

Obecny walidator rozszerzono o `validate_category_a_deployment`. Porównuje dokładne
mapy tłumaczeń C1, pełne `depends_on`, docelowe atrybuty ról i liczbę operacji.
Odrzuca listy `nouns`, dodatkowe kategorie/atrybuty, brakujące lub nadmiarowe
zależności i duplikaty. Kontrola `hitori` sprawdza XML rzeczowników i realizację
jednej osoby. Referencje lekcji sprawdza istniejący walidator ogólny.

Testy jednostkowe używają wyłącznie niezależnych fixture'ów. Testy Kotomi obejmują
nowe osoby i zwierzęta, odrzucanie zwierząt przez `person`, cztery formy, jawne
oraz niejawne `agree`, renderowanie związanych wyborów, pytania i zapis XML.
Obowiązkowe CI kontroluje produkcyjne dane strukturalnie, bez renderowania wzorców.
Pełna integracja i poniższe pomiary są narzędziami opt-in, poza obowiązkowym CI.
Job benchmarku lekcji Kotomi wymaga ręcznego `workflow_dispatch` i
`run_lesson_performance=true`. Pakiety Quiz i ich wersje pozostały bez zmian.
Manifest Content wygenerowano istniejącym narzędziem; zmieniły się tylko rewizja
oraz hashe `verbs.xml`, `nouns.xml` i `lessons.xml`.

## Integracja na rzeczywistych danych

Silnik: `2656c5a270489141661561701d0a064c8a1dcbd4`. Pełna walidacja obu projektów
i katalogu lekcji: zero błędów. Wszystkie 368 sond dostępności (92 wzorce × 4 formy)
zachowały wynik. Automatycznie sprawdzono pełne polskie zdania względem
zatwierdzonych tłumaczeń C1, przypadków i zaimków oraz pełne japońskie odpowiedzi
względem niezmienionych form kana. Sprawdzono też 104 generowane pytania
(26 nowych czasowników × 4 formy), każde jawne związanie i równoważność `agree`.

| Forma | Pary podmiotowe przed | Pary podmiotowe po | Realizacje dopełnieniowe przed | Po |
| --- | ---: | ---: | ---: | ---: |
| dictionary | 70 | 300 | 7735 | 7645 |
| plain_negative | 70 | 300 | 7735 | 7645 |
| past_plain | 70 | 300 | 7735 | 7645 |
| past_negative_plain | 70 | 300 | 7735 | 7645 |

Każda forma ma 230 nowych par. Silnik uwzględnia pięć opcji kontekstu,
więc liczba realizacji wynosi 350 → 1500 na formę; liczba unikalnych pytań
i odpowiedzi wynosi 70 → 300. Pięć dodatkowych par względem historycznej
prognozy 295 wynika z dopuszczenia `tori` tam, gdzie C1 wskazywało jedynie `inu`.
Ubytek 90 realizacji dopełnieniowych na formę obejmuje wyłącznie `hitori`.
Po ich odjęciu pozostałe realizacje są dokładnie identyczne, łącznie z wiązaniami,
kontekstami i formami. Usunięcie `hitori` ogranicza też inne selekcje osób lub
wildcard do pozostałych rzeczowników; dostępność żadnego wzorca nie znika.

Liczenie przed i po daje m.in. „Jest jedna osoba.” → `ひとがひとりいる。` oraz
„Ile jest osób?” → `ひとがなんにんいるの？`. Cztery formy liczbowego stwierdzenia
są niezmienione. Pytania o liczbę zachowują wcześniejsze ograniczenie do form
twierdzących; ich formy przeczące nadal są odrzucane.

Pełne dane: [integracja](../validation/verb_subject_c22_validation.json),
[pomiary](../validation/verb_subject_c22_performance.json) i
[raport akceptacji](../validation/verb_subject_c22_acceptance.md).
Polecenia odtworzenia opisano w `tools/README.md`.

## Dodatkowy audyt bez rozszerzania zmian

- Potwierdzona redundancja: `hitori` jako rzeczownik i realizacja `nin`; poprawiono.
  Nie znaleziono drugiej identycznej redundancji w przeglądzie słowników.
- `ほん` (klasyfikator `hon` i książka `book`) oraz `ふく` (ubranie i czasownik)
  to różne jednostki o tej samej kana, nie wpisy do automatycznego usunięcia.
- Kategoria `availability_reason` miesza czas, pieniądze i plany. `okane` wymaga
  wielu jawnych wyjątków w rolach przedmiotowych; to kandydat do osobnego audytu
  kategorii, nie zmiana C2.2.
- `aku/shimaru: bag box`, `owaru: shigoto meal yotei`, cele `ireru` i `kayou`
  oraz listy rzeczy otwieranych/zamykanych są semantycznie węższe niż istniejące
  kategorie. Pozostają potrzebne w obecnym modelu.
- Listy `music song`, `clothes`, miejsc budowanych przez `tateru` i dokumentów
  dla `teishutsusuru` mogą nie objąć przyszłych haseł. Nie zastąpiono ich szerszymi
  kategoriami bez osobnej decyzji semantycznej.
