# C1: audyt słownika czasowników i przygotowanie C2

Status: audyt i propozycje do zatwierdzenia. **C2 nie zostało rozpoczęte.**
Żaden słownik produkcyjny, wzorzec, quiz, manifest ani numer wydania nie został zmieniony.

## 1. Wynik i zakres

Przeanalizowano **122 czasowniki, wszystkie 1817 zapisanych form, wszystkie 221 deklaracji ról oraz 81 aktualnych rzeczowników**. Cztery priorytetowe formy istnieją dla każdego czasownika. Problemem jest przede wszystkim brak poprawnie ukierunkowanych tłumaczeń i ograniczeń znaczeniowych, nie brak japońskich końcówek.

| Wynik | Liczba |
|---|---:|
| A: bezpieczny, konkretny zakres uzupełnień | 33 |
| B: wymagana decyzja językowa lub doprecyzowanie argumentów | 79 |
| C: potrzebna odpowiednia konstrukcja zamiast zwykłego subject agreement | 7 |
| D: bez zmian w czterech formach priorytetowych | 3 |
| Obecnie gotowe zwykłe przydawki podmiotowe | 3 czasowniki |
| Istniejące mapy uzgodnienia | 12 form, 28 wpisów klas |
| Propozycje A do C2 | 132 form, **308 nowych wpisów klas** |
| Wymagające tylko tłumaczeń w A | 1: `shimaru` |
| Wymagające tylko nowej roli w A | 0 |
| Wymagające tłumaczeń i nowej roli w A | 32 |
| Brakujące japońskie formy priorytetowe | 0 |

**Klasyfikacja dotyczy czterech form i zwykłej przydawki podmiotowej, nie wszystkich możliwych znaczeń czasownika.** A nie oznacza, że wszystkie istniejące dopełnienia, strona bierna czy konstrukcje ciągłe danego słowa są bezbłędne. D nie oznacza certyfikacji pozostałych jedenastu form. Ich oceny są odrębne. B nie oznacza 79 błędnych czasowników: obejmuje również poprawne czasowniki wymagające dopełnienia lub kontekstu.

Liczba 308 oznacza brakujące, zatwierdzalne pozycje w wybranym zakresie A. Nie jest liczbą wszystkich hipotetycznych pustych pól w słowniku. Nie istnieje sensowny cel 122 × 4 × 5, ponieważ klasy i zastosowania zależą od podmiotów. Przydawki podmiotowe po eksperymencie A obsługują 36 czasowników, czyli 3 dotychczasowe i 33 rozszerzone.

## 2. Rewizje i źródła techniczne

Stan `main` odczytany 15 października 2026:

- Kotomi: [`9c01404465837f55d32ce1b4056fbb6e99817440`](https://github.com/MaciejPotas/Kotomi/commit/9c01404465837f55d32ce1b4056fbb6e99817440).
- Kotomi-Data: [`236bf6af22e897d103099a1166fb9a941d3ee1fd`](https://github.com/MaciejPotas/Kotomi-Data/commit/236bf6af22e897d103099a1166fb9a941d3ee1fd), Content 60.
- Drzewo Kotomi-Data: `6e6e2bb98ad6002a377e5239905b76a03686644b`. Lokalna baza audytu odtwarza to drzewo; zmiany C1 dotyczą wyłącznie dokumentacji, narzędzia i testów. Pliki obu kopii porównano z SHA blobów wskazanych przez przypięte drzewa GitHub.

Przeczytane kontrakty:

| Mechanizm | Źródło w przypiętym Kotomi |
|---|---|
| Parser map, dopuszczalne atrybuty, ochrona jawnego/niejawnego `agree` | `kotomi/core/project/form_agreement.py` |
| Pięć klas singular B2 | `kotomi/languages/polish/__init__.py`, `catalog.py` |
| Rekcja, typy i odczyt danych | `kotomi/core/project/models.py`, `xml_loader.py`, `validation.py` |
| Kategorie, dokładne ID, dopasowanie roli | `kotomi/core/generation/compatibility.py::role_matches()` |
| Rozwiązywanie form i blokowanie brakujących realizacji | `kotomi/core/generation/realization.py` |
| Odczyt tekstu dla klasy bez fallbacku | `kotomi/core/generation/rendering.py::_agreement_value()` |
| Wspólna ścieżka generowania | `kotomi/application/quiz_project.py`, `generation_engine.py` |

Porównano przewodniki PL/ENG `verb_form_agreement.md` i `relative_clauses.md` w aplikacji oraz PL/ENG `relative_clauses.md` i raport B3 w Content. Nie stwierdzono potrzeby zmiany kontraktu dokumentacji. Nowe skrócone wejścia PL/ENG do C1 przekazują ten sam zakres i liczby.

## 3. Metodologia i poziom pewności

1. Odczyt słownika i aktualnego projektu, bez stałej liczby słów w kodzie walidatora.
2. Przegląd znaczenia, odmiany kana/kanji, polskich glossów, ról i wszystkich dopasowanych rzeczowników dla każdego słowa.
3. Ręcznie dobrane polskie formy i jawne listy podmiotów. Żadnego obcinania polskich końcówek ani koniugacji w silniku.
4. Porównanie japońskich zapisów z regularnymi paradygmatami, uwzględniając `ある`, `行く`, `する`, `来る`, złożenia i wyjątek `くれる`. Kandydaty regularne były tylko narzędziem kontroli, nigdy zamiennikiem wartości XML.
5. Odrębna ocena morfologii, znaczenia, ról i przydatności konstrukcji. Poprawna końcówka nie dowodzi naturalności czasownika potencjalnego lub biernego.
6. Zastosowanie wyłącznie propozycji A w tymczasowej kopii Content. Pełna walidacja przed i po, kontrola dopasowań, pełne wyniki obu obecnych przydawek, kontrola dostępności i list kandydatów wszystkich 92 wzorców.
7. Celowo niepoprawne hipotetyczne uzupełnienia kilku B/C sprawdzono wyłącznie w pamięci. Są dowodem ryzyka, nie propozycjami C2 ani fixture'ami testów.

Wyniki parsera, liczby, dopasowania i wyrenderowane zdania są **potwierdzone eksperymentalnie**. Ocena naturalności jest konserwatywną oceną językową audytu, nie certyfikacją przez native speakera. Niejednoznaczne zastosowania pozostają B/C. Nie deklaruję kompletnego przeglądu wszystkich kombinacji wszystkich quizów ani testów na fizycznym Androidzie/Windows.

## 4. Jak czytać komplet materiałów

- [Pełne zestawienie 122 czasowników i kandydaci tłumaczeń](verb_dictionary_inventory_c1.md): jedna pozycja zbiorcza na czasownik, następnie szczegóły czterech form według klas.
- [Ustrukturyzowane rekordy i propozycje](verb_dictionary_proposals_c1.json): aktualne role i rzeczywiste dopasowania rzeczowników, znaczenia, kandydaci, decyzje, dostępność istniejących przydawek i 340 addytywnych operacji A.
- [Rejestr wszystkich 1817 form](verb_dictionary_forms_c1.csv): `verb_id`, `form`, oba zapisy, aktualne tłumaczenie, ocena morfologii, polityka konstrukcji i szczególne ustalenie. Znaczenie każdej polityki jest w JSON oraz poniżej.
- [Dokładne fragmenty XML dla wszystkich 33 czasowników A](verb_dictionary_xml_c1.md).
- [Dowody walidacji i 1180 widocznych par pytanie–odpowiedź](verb_dictionary_validation_c1.json).
- [Hipotetyczne kontrprzykłady semantyczne](verb_dictionary_semantic_examples_c1.json), zachowane z pierwotnego audytu i nieuruchomione ponownie po review.
- [Pomiary i wszystkie próbki czasu](verb_dictionary_performance_c1.json), wyłącznie historyczne, sprzed korekt review.

W JSON tylko `changes` jest zestawem operacji proponowanych do C2. `verbs[].proposed_priority_values` zawiera także **warianty dyskusyjne B/C**, wyraźnie oznaczone `candidate_status`. Nie stosować ich automatycznie. `depends_on` wiąże tłumaczenia z potrzebną nową rolą. Ścieżki wskazują istniejącego rodzica; wpisy mają `expected_absent=true` i nie nadpisują danych.

## 5. Cztery formy priorytetowe i klasy

Każdy czasownik ma `dictionary`, `plain_negative`, `past_plain`, `past_negative_plain`: łącznie 488 form. Tylko `hataraku`, `neru`, `aku` mają istniejące mapy B2. Potwierdzono wszystkie 28 wartości oraz dokładne zakresy ich podmiotów. Niczego w tych mapach nie proponuję nadpisywać.

- `hataraku`: 8 osób, klasy `masculine_personal`, `feminine`.
- `neru`: te same osoby i `inu`, `tori`, dodatkowo `masculine_animate`.
- `aku`: `bag`, `box`, klasy `feminine`, `neuter`.

Trzecia osoba zależy od klasy rzeczownika, nie od biologicznej płci osoby: `hito` ma tłumaczenie „osoba” i klasę żeńską. Dlatego poprawne jest „osoba, która czytała”. Nie trzeba dopisywać fikcyjnego dziecka lub klasy nijakiej każdemu czasownikowi.

**Semantyka i gramatyka są odrębne.** Wpis `feminine=czytała` nie dopuszcza automatycznie książki ani torby do czytania. O tym decyduje rola. W drugą stronę, obecny brak rzeczownika nijakiego będącego człowiekiem nie dowodzi, że „czytało” jest językowo niemożliwe. Warianty do przyszłych rzeczowników nie są jednak potrzebne w A.

Nie ma wspólnej/domniemanej wartości ani dziedziczenia klas w XML B2. Ten sam tekst, np. „czyta”, jest zapisany osobno dla każdej potrzebnej klasy. Czas przeszły zawiera pełne jawne formy, np. „szedł / szła”, „przyszedł / przyszła”, „wziął / wzięła”. Negacja `abiru` wymaga „prysznica”, a nie prostego dołączenia „nie” do całej frazy twierdzącej.

Liczba mnoga jest rzeczywistym ograniczeniem: `okane` ma klasę `plural_non_masculine_personal`, której B2 czasownika nie obsługuje. Również zaimek względny w obecnym zakresie jest singular. `harau` może zatem dostać poprawną przydawkę podmiotową „osoba, która płaci”, mimo że jego dopełnieniowa przydawka z pieniędzmi jest nadal niedostępna. „Drzwi, które się otwierają” nie jest przykładem liczby pojedynczej, a rzeczownika drzwi obecnie nie ma w słowniku.

## 6. Wszystkie pozostałe formy

| Forma lub grupa | Zapisanych | Ocena i dalszy kierunek |
|---|---:|---|
| Cztery grzeczne odpowiedniki | 488 | Polski może współdzielić treść z plain, ale nie wprowadzać masu wewnątrz zwykłej japońskiej przydawki. B2 może przechować tekst dla późniejszego zdania głównego. |
| `te_form` | 122 | Fragment wielu konstrukcji. Istniejące ている nie jest uniwersalną etykietą czynności ciągłej; sprawdzać stan wynikowy. Nie dodawać neutralnego trzecioosobowego B2 do samego て. |
| `potential` | 118 | Odmiana nie przesądza znaczenia zdolności, możliwości czy pozwolenia. Sprawdzić argumenty i が/を. B2 przechowa tekst, ale nie zmieni ramy argumentów. |
| `passive` | 115 | Konieczny wybór podmiotu biernego, wykonawcy oraz ewentualnej osoby dotkniętej zdarzeniem. Formy typu „ktoś…, co mi przeszkadza” to objaśnienia, nie neutralne uzgodnione orzeczenia. |
| `causative` | 120 | Rozróżnić sprawcę, wykonawcę i „każe / pozwala / sprawia”. Sama mapa rodzaju nie opisuje tych ról. |
| `tara` | 122 | „Jeśli”, „kiedy”, „po tym jak” oraz aspekt zależą od zdania głównego. Obecne glosy są wariantami, nie uniwersalną realizacją. |
| `volitional` | 122 | Zaproszenie, zamiar i przypuszczenie nie mają jednego neutralnego odpowiednika trzecioosobowego. |
| `imperative` | 122 | Potrzebny adresat i kontekst. „Niech zrobi” nie jest automatycznie zwykłym stwierdzeniem o podmiocie. |

Nie proponuję żadnych nowych map B2 dla tych form. Ich rekordy mają własne statusy, niezależnie od zbiorczego A/B/C/D.

Braki są obecnie uzasadnione lub co najmniej nie są automatyczną usterką:

- `potential` nie ma `aru_possessive`, `aru_existential`, `dekiru`, `mieru`.
- `passive` nie ma obu `aru`, `chigau`, `dekiru`, `hareru`, `kumoru`, `mieru`.
- `causative` nie ma obu `aru`.

Przegląd zapisów nie wykazał potwierdzonego błędu kana/kanji do mechanicznej poprawy. Dwa odstępstwa od regularnego oczekiwania wymagają rozróżnienia:

1. `kureru/imperative = くれ` jest poprawnym wyjątkiem. Nie zmieniać na `くれろ`.
2. `wakaru/potential = わかる / 分かる` powtarza formę podstawową, a nie osobną produktywną odmianę potencjalną. Etykieta i ekspozycja w quizie wymagają decyzji. Nie zastępować automatycznie przez `分かれる`, które może być innym leksemem.

Oceny form należy czytać rozdzielnie: `morphology` mówi o zapisie/kształcie, `specific_finding` o znaczeniu i zastrzeżeniach, a `policy` (z definicją w JSON) o zastosowaniu i potrzebnej konstrukcji. `regular_or_known_exception` nie jest deklaracją gotowości quizowej ani zatwierdzeniem każdego polskiego znaczenia.

| Pozycja | Morfologia | Znaczenie | Gotowość quizowa | Konstrukcja/decyzja |
|---|---|---|---|---|
| `chigau/potential` | `ちがえる/違える` pasuje tylko do mechanicznego wzoru u→eru; nie potwierdzono go jako neutralnej potencjalnej odmiany 違う. | „Mogę się różnić” nie jest zatwierdzone; 違える może należeć do odrębnego przechodniego leksemu. | Nie zatwierdzać jako ćwiczenia potencjalnej odmiany. | Najpierw rozstrzygnąć leksem i kontekst możliwości; sama mapa B2 lub nowy wzorzec nie naprawi etykiety. |
| `wakaru/potential` | `わかる/分かる` to poprawna forma podstawowa, lecz nie osobna produktywna odmiana potencjalna. | Rozumienie/możność zrozumienia nie uzasadnia automatycznie etykiety `potential`. | Nie zatwierdzać jako zadania odmiany. | Decyzja o ekspozycji tej pozycji oraz osobie rozumiejącej i treści; nie zastępować przez 分かれる. |

`持ってくる` prawidłowo zmienia końcowe kana na `きます`, `こない`, `きた`. Zapis mieszany nie jest niespójnością kanji. Typy `帰る`, `入る`, `走る`, `知る` pozostają godan mimo zakończenia る. `着る` pozostaje ichidan. Czasowniki pogodowe i mimowolne mogą mieć formalnie poprawne, ale pragmatycznie nacechowane rozkazy i formy potencjalne; nie oznaczyłem ich jako gotowych do dowolnego quizu.

## 7. Role, rekcja i rzeczywiste rzeczowniki

221 deklaracji: `location` 102, `object` 62, `target` 21, `subject` 18, `destination` 9, `companion` 5, `route` 2, `vehicle` 1, `reaction_target` 1. Pełna lista dopasowań każdej deklaracji znajduje się w `current_roles[].matched_nouns`.

Istotny kontrakt `role_matches()`:

- Rola musi istnieć w `word.usage`.
- `accepts` i `nouns` są połączone przez **OR**, nie przez AND.
- `accepts="*"` dopuszcza wszystkie rzeczowniki.
- Same dokładne `nouns` mogą ograniczyć rolę bez domyślnych kategorii.
- Brak lokalnych ograniczeń korzysta z kategorii domyślnych roli, a gdy ich nie ma, dopasowanie jest szerokie.
- Dziedziczone kategorie są istotne: `concrete` obejmuje także część mediów. Takie dopasowanie jest techniczne, nie dowodem widzialności.

| Rola | Co sprawdzono i czego nie zmieniać mechanicznie |
|---|---|
| `subject` | 18 obecnych deklaracji nie oznacza 18 polskich osobowych wykonawców. `wakaru` i posiadanie są kontrprzykładami. |
| `object` | Obecna rekcja jest niezmieniona. Przejrzano wildcardy i szerokie kategorie oraz przykłady różnych znaczeń; szczegóły przy każdym czasowniku. |
| `location` | Domyślne place i japońskie で nie gwarantują poprawności dla stanu/pogody lub każdego miejsca. Nowe role A nie modyfikują tych użyć. |
| `destination` | Domyślne place i へ służą kierunkowi ruchu; nie utożsamiać celu z wykonawcą. |
| `target` | Brak wspólnej polskiej rekcji wynikającej z に. Dawca, odbiorca, cel wejścia i przedmiot dotykania wymagają odrębnej oceny. |
| `companion` | Domyślnie osoby/zwierzęta. `hanashiau` wymaga partnera; brakującej polskiej frazy nie naprawia mapa rodzaju. |
| `route` | `deru`, `tooru`: zachować znaczenie punktu wyjścia/trasy i を, nie zamieniać w direct object. |
| `vehicle` | `noru`: pojazdy; problem wsiadania/jazdy pozostaje językowy. |
| `reaction_target` | `odoroku`: polski narzędnik i reakcja nie wyznaczają automatycznie jej wykonawcy. |

32 nowe role A używają wyłącznie **dokładnych istniejących ID**. Zwykła lista ludzi to `friend mother sister teacher roujin hito programmer madogiwazoku`. Tam, gdzie uzasadnione, dodano `inu/tori`, a dla `oyogu` tylko `inu`. `aruku` pozostaje przy ludziach, ponieważ polskie „pies idzie pieszo” jest nienaturalne. `utau` nie dostaje ogólnego ptaka. `shimaru` zachowuje `bag box`.

`person` zawiera `hitori` (jedna osoba, 一人). Z tego powodu nie proponuję szerokiego `accepts="person"` dla nowych ról. Stare role oparte na tej kategorii pozostają do odrębnej decyzji, aby nie zwężać po cichu istniejących quizów. Dopisanie `nouns` obok istniejącego szerokiego `accepts` nie naprawiłoby zakresu z uwagi na OR.

## 8. Najważniejsze ustalenia językowe i architektoniczne

### 8.1. Niewłaściwy argument jako źródło uzgodnienia

Potwierdzono na izolowanych hipotetycznych uzupełnieniach:

| Wpis | Wynik po naiwnym dodaniu mapy | Dlaczego nie stosować |
|---|---|---|
| `aru_possessive`, `box`, „ma” | To jest pudełko, które ma. | Bieżący subject jest rzeczą posiadaną, nie posiadaczem. |
| `wakaru`, `book`, „rozumie” | To jest książka, która rozumie. | Japoński argument treści nie jest polską osobą rozumiejącą. |
| `mieru`, `music`, „jest widoczna” | To jest muzyka, która jest widoczna. | `concrete` nie jest filtrem widzialności. |
| `naku`, `tori`, „płacze” | To jest ptak, który płacze. | Nie jest to neutralny zapis ptasiego głosu; 泣く i 鳴く mają różne znaczenia. |
| `okiru`, `hitori`, „budzi się” | これはおきるひとりです。 | Ilościowa 一人 nie jest zwykłym leksykalnym odpowiednikiem 人 w tym miejscu. |

To przykłady ryzyka aktywacji przez nowe dane, **nie regresje wprowadzone przez C1**. Nie proponuję szerszego blokowania `wakaru` lub `aru_possessive` w silniku w ramach audytu. Wskazuję semantyczną granicę istniejącej roli. Mechanizm zgodności nie wykrywa antropomorfizacji ani odwrócenia argumentów.

`aru_possessive` **nie ma** cechy `existential`; nie wolno zakładać, że chroni go katalogowa blokada PR #213. `iru` i `aru_existential` tę cechę mają. Dla nich potwierdzono zachowanie ochrony oraz konieczność `government` przy katalogowym uzgodnieniu. Nie używam nowych ról ani cech, aby ją obejść.

### 8.2. Aspekt i stan

Do decyzji pozostają przede wszystkim `suwaru` (siadać/siedzieć), `tatsu` (stanąć/stać), `noru` (wsiadać/jechać), `tsukareru` (męczyć się/być zmęczonym), `damaru` (zamilknąć/milczeć), `odoroku` (reakcja/stan zaskoczenia), `sumu` (zamieszkać/mieszkać). To nie jest polecenie automatycznej zamiany wszystkich form: znaczenie zależy od użycia i kontekstu.

`shiru` wymaga szczególnej decyzji o przeczeniu: `知らない` typowo odpowiada „nie wie/nie zna”, a nie prostemu przeczeniu „dowiaduje się”. Kandydat B rozdziela te wartości, lecz nie nadpisuje obecnego glossu.

### 8.3. Wieloznaczność i brakujące argumenty

- `kesu`: wyłączanie telewizji a usuwanie maila/notatki.
- `kiku`: słuchanie w formach podstawowych a bycie pytanym w passive.
- `suu`: base „wciągać”, podstawowe „palę”, potential „mogę wciągać”.
- `ageru` i `ageru_give`: podnoszenie a dawanie; zachować odrębne ID.
- `kariru/kasu`, `ageru_give/kureru/morau/watasu`: kierunek przekazania i osoba mówiąca. Tekst „komuś/od kogoś/mi, nam” nie jest bezpiecznym zastępstwem jawnego argumentu.
- `akeru/aku`, `shimeru/shimaru`, `hiraku/tojiru`: przechodniość i nieprzechodniość nie wynikają z samego polskiego rdzenia.
- `nugu` z `bag`, `ukeru` z `shigoto`, `suru` z `yakusoku`, `teishutsusuru` z `book`: wymagają rozstrzygnięcia konkretnej kolokacji.
- `wasureru`: dopełniacz nie jest z definicji błędny. Polszczyzna dopuszcza różne ramy zależnie od znaczenia; nie przepisywać globalnie na „o + miejscownik”.

### 8.4. Siedem C nie oznacza siedmiu nowych rozszerzeń DSL

| Czasownik | Potrzebna konstrukcja lub decyzja |
|---|---|
| `aru_existential`, `iru` | Istniejące governed existence; zwykła przydawka potrzebuje właściwej realizacji i negacji, nie katalogowego obejścia. |
| `aru_possessive` | Rozdzielenie posiadacza i rzeczy posiadanej w wybranym wzorcu. |
| `wakaru` | Rozdzielenie osoby rozumiejącej i treści albo świadomy wybór innego polskiego orzeczenia. |
| `dekiru` | Istniejące `ことができる` z dopełnieniem; samo „osoba, która może” jest niepełne w wybranym znaczeniu. |
| `hanashiau` | Partner rozmowy w liczbie pojedynczej lub odrębne mnogie uzgodnienie. Sprawdzić istniejące `companion` przed projektowaniem DSL. |
| `naru` | Jawny wynik/orzecznik. „Osoba, która staje się” nie jest skończonym zdaniem dydaktycznym. |

### 8.5. Ponowna ocena wszystkich 34 pierwotnych A

Przejrzano cztery formy, negację, aspekt przeszłości, znaczenie i pełne przydawki dla wszystkich pierwotnych A. Poniższe decyzje są oceną językową audytu, nie certyfikacją native speakera. Pozostaje ograniczenie do wybranego znaczenia i zwykłej przydawki. Nie rozszerzono zakresu na potential, bierną ani nowe konstrukcje.

Dla ruchu brak sposobu przemieszczania w japońskim zdaniu nie gwarantuje chodzenia po ziemi. Ptak może chodzić, ale taki kontekst nie jest podany. Wniosek audytu: zawęzić `iku`, `kuru`, `deru`, `hairu` do ludzi i `inu`, bez zmiany tłumaczeń. Warianty osób także reprezentują wybrane znaczenie ruchu lądowego, nie każde możliwe przybycie samolotem.

Poniższe pełne zdania to **historyczne realizacje odrzuconych teraz propozycji**, nie bieżące dopuszczenia. Pokazują również, dlaczego problem pozostaje w negacji i przeszłości.

| Pozycja | Forma | Zdanie japońskie | Zdanie polskie |
|---|---|---|---|
| `iku` | `dictionary` | これはいくとりです。 | To jest ptak, który idzie. |
| `kuru` | `dictionary` | これはくるとりです。 | To jest ptak, który przychodzi. |
| `deru` | `dictionary` | これはでるとりです。 | To jest ptak, który wychodzi. |
| `hairu` | `dictionary` | これははいるとりです。 | To jest ptak, który wchodzi. |
| `nonbiri_suru` | `dictionary` | これはのんびりするひとです。 | To jest osoba, która leniuchuje. |
| `iku` | `plain_negative` | これはいかないとりです。 | To jest ptak, który nie idzie. |
| `kuru` | `plain_negative` | これはこないとりです。 | To jest ptak, który nie przychodzi. |
| `deru` | `plain_negative` | これはでないとりです。 | To jest ptak, który nie wychodzi. |
| `hairu` | `plain_negative` | これははいらないとりです。 | To jest ptak, który nie wchodzi. |
| `nonbiri_suru` | `plain_negative` | これはのんびりしないひとです。 | To jest osoba, która nie leniuchuje. |
| `iku` | `past_plain` | これはいったとりです。 | To jest ptak, który poszedł. |
| `kuru` | `past_plain` | これはきたとりです。 | To jest ptak, który przyszedł. |
| `deru` | `past_plain` | これはでたとりです。 | To jest ptak, który wyszedł. |
| `hairu` | `past_plain` | これははいったとりです。 | To jest ptak, który wszedł. |
| `nonbiri_suru` | `past_plain` | これはのんびりしたひとです。 | To jest osoba, która leniuchowała. |
| `iku` | `past_negative_plain` | これはいかなかったとりです。 | To jest ptak, który nie poszedł. |
| `kuru` | `past_negative_plain` | これはこなかったとりです。 | To jest ptak, który nie przyszedł. |
| `deru` | `past_negative_plain` | これはでなかったとりです。 | To jest ptak, który nie wyszedł. |
| `hairu` | `past_negative_plain` | これははいらなかったとりです。 | To jest ptak, który nie wszedł. |
| `nonbiri_suru` | `past_negative_plain` | これはのんびりしなかったひとです。 | To jest osoba, która nie leniuchowała. |

`nonbiri_suru` przechodzi do B: neutralny odpoczynek/relaks nie musi oznaczać leniuchowania. NINJAL opisuje zarówno spokojne korzystanie z czasu, jak i niekiedy negatywną ocenę powolności. To uzasadnia decyzję o znaczeniu przed uzupełnieniem map, także dla „nie leniuchuje” i „leniuchował”. Obecne wartości pozostają wyłącznie dyskusyjne.

| Pierwotne A | Wynik ponownej oceny |
|---|---|
| `aruku` | A: Samodzielny ruch pieszy ma naturalnego wykonawcę; do C2 tylko ludzie, bo pies idzie pieszo jest stylistycznie nienaturalne. |
| `asobu` | A: Zabawa ludzi i zwierząt może wystąpić bez wskazania towarzysza. Zachować istniejącą rekcję towarzysza. Tori pozostaje: japońska i polska czynność nie zakładają ludzkiego wykonawcy ani konkretnego sposobu lokomocji. |
| `ayamaru` | A: Osoba może przepraszać bez jawnego adresata; target pozostaje niezależną rolą, bez poszerzania jej obecnej listy. |
| `deru` | A: Zawęzić propozycję do ludzi i inu. 出た鳥 może oznaczać ptaka, który wyleciał; polskie wyszedł zakłada ruch po ziemi. Wybrana przydawka nie podaje tego kontekstu. Zachować route i dotychczasowe tłumaczenia; bez publikacji ani pojazdów. |
| `hairu` | A: Zawęzić propozycję do ludzi i inu. 入った鳥 może oznaczać ptaka, który wleciał; polskie wszedł wymaga dodatkowego kontekstu. Zachować target=place i wszystkie tłumaczenia. Nie rozszerzać tej propozycji na inne znaczenia 入る. |
| `hanasu` | A: Rozmawia może opisywać osobę bez jawnego partnera. Nie rozszerzać na zwierzęta ani zastępować tego automatycznie znaczeniem opowiadać o czymś. |
| `harau` | A: Samodzielne płaci/zapłacił jest naturalne; zachować object=okane. Nie zmieniać znaczenia na usuwać/strzepywać. |
| `hashiru` | A: Bieg ludzi i zwierząt jest samodzielną czynnością. Pojazdy i programy pominięte, bo wymagałyby innego polskiego znaczenia. Pozostawić tori: 走る określa właśnie bieg, więc polskie biegnie/biegł nie dodaje sposobu ruchu nieobecnego w japońskim. Nie jest to twierdzenie, że każdy ptak w każdej sytuacji biegnie. |
| `iku` | A: Zawęzić propozycję do ludzi i inu. 行く określa kierunek, nie sposób ruchu; zdanie z ogólnym tori nie gwarantuje polskiego idzie/poszedł zamiast leci/poleciał. Nie zmieniać tłumaczeń ani nieregularnych いった/いかない. A obejmuje wybrane znaczenie ruchu lądowego, nie każdy sposób podróży ludzi. |
| `isogu` | A: Samodzielna czynność osoby; zachować zaakceptowaną pisownię śpieszyć, bez kosmetycznej zmiany na spieszyć. |
| `kaeru` | A: Powrót żywego wykonawcy można opisać bez jawnego celu. Nie zmieniać na ogólne zmieniać, które jest innym czasownikiem. Wraca/wrócił nie wybiera chodu ani lotu, więc tori pozostaje. |
| `kaku` | A: Pisanie jest naturalne bez jawnego tekstu, np. osoba, która pisze. Zachować object=text i direct_object. |
| `kangaeru` | A: Zastanawia się jest samodzielne; przy dopełnieniu pozostaje nad_instrumental. Pojazd jako przedmiot namysłu nie oznacza podmiotu. |
| `kau` | A: Kupuje może być użyte absolutnie dla kupującej osoby; precyzyjny zakup wymaga object. Zachować istniejące role. |
| `kikokusuru` | A: 帰国する zawiera powrót do własnego kraju; podmiot ludzki, argument celu zawarty w tłumaczeniu. Nie poszerzać na zwierzęta. |
| `kotaeru` | A: Odpowiada może wystąpić bez jawnego pytania. Existing target=abstract pozostaje osobną kwestią precyzji dopełnienia. |
| `kuru` | A: Zawęzić propozycję do ludzi i inu. 来る nie określa sposobu ruchu, więc 来た鳥 może oznaczać ptaka, który przyleciał. Przyszedł wymaga dodatkowego kontekstu ruchu po ziemi. Zachować wszystkie polskie wartości i nieregularne きた/こない; A nie certyfikuje każdego sposobu przybycia. |
| `matsu` | A: Czekanie ludzi i zwierząt jest naturalne bez jawnego obiektu; na_accusative pozostaje dla dopełnienia. Tori pozostaje: japońska i polska czynność nie zakładają ludzkiego wykonawcy ani konkretnego sposobu lokomocji. |
| `nomu` | A: Picie ma naturalnego żywego wykonawcę i może nie mieć jawnego napoju; pozostawić object=drink. Tori pozostaje: japońska i polska czynność nie zakładają ludzkiego wykonawcy ani konkretnego sposobu lokomocji. |
| `nonbiri_suru` | B: B po ponownej ocenie: のんびりする obejmuje spokojny odpoczynek i relaks, nie tylko leniuchowanie. Obecne polskie znaczenie zawęża sens i może dodawać ocenę; dotyczy też negacji i przeszłości. Najpierw zatwierdzić znaczenie lub kontekst lekcji. Zachować produkcyjne tłumaczenie; warianty leniuchuje/leniuchował pozostają dyskusyjne, bez operacji C2-A. |
| `okoru` | A: 怒る w wybranym znaczeniu emocji osoby jest samodzielne. Nie rozszerzać na homofoniczne 起こる ani bezpośrednio na karcenie kogoś. |
| `omou` | A: Myśli/pomyślał można użyć absolutnie. Zachować reporting i istniejący wybór aspektu; nie dodawać posiadania opinii o dowolnym przedmiocie. |
| `oyogu` | A: Ludzie i pies mogą pływać. Nie dopuszczać ogólnego ptaka, bo nie wszystkie ptaki pływają, ani łodzi, która wymaga innego japońskiego orzeczenia. |
| `renshuusuru` | A: Ćwiczy w znaczeniu doskonalenia umiejętności jest samodzielne. Object=music/song zostaje bez zmian i wymaga osobnej oceny idiomatyczności ćwiczyć muzykę. |
| `sentakusuru` | A: Prać można bez jawnego ubrania; object=clothes pozostaje poprawnym zakresem. Nie dopuszczać przypadkowych rzeczy jako wykonawców. |
| `shimaru` | A: Nieprzechodnie zamykanie torby/pudełka; istniejąca precyzyjna rola wystarcza. Dodać tylko feminine/neuter w czterech formach. |
| `soujisuru` | A: Sprzątanie jest samodzielną czynnością osoby; nie zmieniać object ani location. Dodatkowe dane nie naprawiają wszystkich obecnych dopełnień thing. |
| `taberu` | A: Jeść można bez jawnego jedzenia; żywy podmiot i object=food są rozdzielnymi rolami. Nie dopuszczać żywności jako wykonawcy. Tori pozostaje: japońska i polska czynność nie zakładają ludzkiego wykonawcy ani konkretnego sposobu lokomocji. |
| `undousuru` | A: Samodzielna aktywność fizyczna osoby; bez dodawania narzędzi i bez utożsamienia z ćwiczeniem utworu. |
| `usowotsuku` | A: Kłamać można bez jawnego adresata; うそをつく jest całym zapisanym leksemem. Nie tworzyć drugiego slotu dla うそ. |
| `utau` | A: Śpiew osoby jest samodzielny. Ptaki zwykle 鳴く/さえずる; nie dodawać ich do A. Object=media odrębnie wymaga wykluczenia np. głosu. |
| `warau` | A: Śmiech osoby może być samodzielny. Zachować z_genitive dla wyśmiewanej osoby/zwierzęcia; podmiot nie jest tym samym argumentem co object. |
| `yomu` | A: Czytanie ma naturalne użycie bez jawnego tekstu. Precyzyjna lista ludzi, zachować object=text; nie dodawać zwierząt ani rzeczy. |
| `shinjiru` | A: Wierzy może opisywać osobę bez jawnego obiektu wiary. Zachować w_accusative; wiara w osobę i ufanie osobie nie są automatycznie tą samą rekcją. |

Dla pozostałych A zachowano wszystkie przejrzane polskie wartości czterech form. Przeszłe pary dokonane (np. zapłacił, kupił, odpowiedział) i niedokonane (np. czytał, pływał) są wybranymi odczytaniami, nie automatycznym odwzorowaniem aspektu japońskiego. Negacja zachowuje ten wybór. Przydawki bez dopełnienia korzystają z kontekstowego pominięcia argumentu, bez twierdzenia, że wszystkie istniejące dopełnienia są poprawne. Nie dodano innych rzeczowników.

## 9. Obecne i przyszłe quizy

Dla każdego słowa w JSON znajdują się **zmierzone** booleany dostępności obu istniejących przydawek w czterech formach. To dostępność silnika, nie automatyczna aprobata językowa wszystkich zdań. `future_use` oddziela ją od przewidywanej przydatności.

- Proste zdanie bez uzgodnienia zachowuje `Form.translation`.
- Zdanie z dopełnieniem oraz przydawka dopełnieniowa nadal wymagają właściwego object i rekcji. W szczególności `harau` pozostaje bez singular object-relative z `okane`.
- Przeczenie i przeszłość nowych A wykorzystują dokładnie cztery przejrzane formy.
- Konstrukcja `ことができる` już istnieje, podobnie jak `Czynność w toku 〜ている`. Nie oznacza to automatycznej poprawności każdej formy potencjalnej, biernej lub stanowej.
- Potwierdzony przykład bazowego ている z `yomu` poprawnie realizuje polskie „czytam”; silnik nie drukuje po prostu „czytając”. Audyt fragmentów te nie jest stwierdzeniem usterki całej tej konstrukcji.
- Przyszłe ramy strony biernej, kauzatywności, rozkazu i liczby mnogiej wymagają osobnej akceptacji konstrukcji. Nie deklaruję ich pełnej kompatybilności ani nie dopisuję stanu „gotowości” do XML.

## 10. Eksperyment A, regresja i weryfikacja

Wyniki poniżej uruchomiono ponownie 15 października 2026 dla wersji audytu 2, po zmianach review. Historyczne pomiary czasu mają osobny status w sekcjach 11 i 17.

| Metryka | Przed | Po zastosowaniu A na kopii |
|---|---:|---:|
| Czasowniki w zwykłych przydawkach podmiotowych | 3 | 36 |
| Pary czasownik/rzeczownik | 20 | 295 |
| Realizacje podmiotowe na jedną formę | 100 | 1475 |
| Widoczne unikalne pary pytanie/odpowiedź na formę | 20 | 295 |
| Widoczne pary dla czterech form | 80 | 1180 |
| Realizacje dopełnieniowe na formę | 7735 | 7735 |
| Realizacje dopełnieniowe dla czterech form | 30940 | 30940 |

Pięć kontekstów może dawać ten sam widoczny tekst przydawki. Nie należy przedstawiać 5900 realizacji podmiotowych jako 5900 unikalnych pytań.

Potwierdzono:

- Pełna walidacja projektu przed i po: zero zgłoszonych problemów.
- Wszystkie nowe role dopuszczają dokładnie zatwierdzone listy rzeczowników, a klasy odpowiadają tym listom.
- Wszystkie realizacje podmiotowe w czterech formach odtworzono przez jawne `render_bound_pattern`.
- Wszystkie 30940 realizacji dopełnieniowych porównano z pełną sygnaturą: teksty, słowa, rzeczowniki, formy i konteksty są identyczne.
- Dla wszystkich 92 istniejących wzorców i czterech form: identyczna dostępność przed/po; listy ID kandydatów identyczne poza oczekiwanym rozszerzeniem przydawek podmiotowych. Sama dostępność tego wzorca też pozostaje true.
- Niezmienność wszystkich dotychczasowych ról, rekcji, bazowych tłumaczeń, zapisów japońskich, rzeczowników i wzorców.
- 564 negatywnych sprawdzeń wykluczenia niepasujących par lub niebezpiecznych katalogów.
- 100 pytań z kanonicznego generatora, seed 173, poprawne rozpoznanie oczekiwanej odpowiedzi.
- Istniejące izolowane testy Kotomi: **162 passed** (uruchomione ponownie po review) (`test_subject_relative_catalog_boundary.py`, `test_verb_form_agreement.py`, `test_relative_explicit_case.py`). Nie dodano produkcyjnych fixture'ów ani wyjątków do testów.
- Oba walidatory Kotomi-Data przechodzą; zestaw unittest z `KOTOMI_PATH`: **57 testów OK** (34 istniejące i 23 nowe, w tym 4 z rzeczywistym kontraktem silnika na obiektach syntetycznych).

Nie enumerowano wszystkich możliwych kombinacji pozostałych quizów. Dla nich dowodem jest kontrola niezmienionych danych, dostępności i list kandydatów, nie twierdzenie o pełnej równoważności dowolnej przyszłej konfiguracji. Publiczna lista pytań zależy też od aktualnych ustawień użytkownika.

## 11. Wydajność

**Pomiary historyczne, nieuruchomione ponownie po review.** Plik performance zachowuje siedem pierwotnych naprzemiennych par oraz jedną serię kontrolną 21 par. Dotyczą wcześniejszego zakresu: 34 A, 316 wpisów, 33 role i 307 par podmiotowych. Nie są pomiarem obecnych 33 A, 308 wpisów, 32 ról i 295 par. Nie wnioskujemy z nich o aktualnym czasie generowania.

Zachowano oryginalne próbki, definicje cold/warm i ograniczenia współdzielonego środowiska. Bieżąca ponowna kontrola obejmuje poprawność i regresję wyników, bez benchmarku. C2 powinno ponowić pomiary dla zatwierdzonego zakresu i docelowego urządzenia.

## 12. Przykładowy zakres XML

Dla `yomu`, dopisanie do istniejącego `usage`:

```xml
<role ref="subject" nouns="friend mother sister teacher roujin hito programmer madogiwazoku" />
```

Do istniejącego `forms/form[@ref='past_plain']`, bez zmiany `translation="czytałem"`, kana ani kanji:

```xml
<agreement_translations>
  <translation class="masculine_personal" value="czytał" />
  <translation class="feminine" value="czytała" />
</agreement_translations>
```

Pozostałe trzy formy mają odpowiednio „czyta”, „nie czyta”, „nie czytał/nie czytała”. Wszystkie fragmenty wszystkich A, nie tylko ten przykład, są w [zestawie XML](verb_dictionary_xml_c1.md). `shimaru` wymaga tylko map feminine/neuter, bez nowej roli.

## 13. Plan wdrożenia C2

Proponuję cztery niezależne zakresy, bez jednego wielkiego PR i bez PR na każde słowo:

1. **C2.1: gotowa rola i zwykłe czynności ludzi.** `shimaru` oraz proste, samodzielne czynności z listy A, w tym `yomu`, `kaku`, `hanasu`, `kangaeru`, `sentakusuru`, `soujisuru`. Dodać dokładnie proponowane mapy/listy, sprawdzić parser i próbki każdej klasy.
2. **C2.2: pozostałe A, ruch i podmioty zwierzęce.** Dokładne listy ludzi/inu/tori oraz wyjątki `aruku`, `oyogu`, `utau`. Ponownie porównać przydawki dopełnieniowe i politykę wzorców, zmierzyć liczenie oraz pierwsze pytanie.
3. **C2.3: zatwierdzone korekty leksykalne i zakresy B.** Najpierw aspekt, znaczenia i istniejące glosy, następnie precyzja ról. Oddzielić korektę istniejącego błędu od dodania nowych map. Nie zmieniać współdzielonej kategorii, aby naprawić jedno połączenie.
4. **C2.4: odpowiednie konstrukcje C i późniejsze formy.** Wykorzystać istniejące DSL, gdzie wystarcza. Nową architekturę projektować dopiero po wykazaniu brakującej reprezentacji; nie obejmować jej automatycznie PR-em danych.

Mechanicznie można sprawdzić ID, ścieżki, klasy, brak nadpisania, zgodność parsera, dopasowania i regresję wyników. Dobór znaczenia, naturalność pominięcia dopełnienia, aspekt i kierunek argumentów wymagają oceny językowej. Nie można przenieść odpowiedzialności za te decyzje na zielone testy.

## 14. Decyzje do zatwierdzenia

1. Przyjąć 33 zakresy A i 308 wartości, z dokładnymi listami podmiotów, bez automatycznego uzupełniania wszystkich pięciu klas?
2. Zachować konserwatywne wyłączenie z prostych przydawek słów wymagających jawnego dopełnienia, czy przygotować później wzorzec podmiot + dopełnienie, korzystając z istniejących ról?
3. Zatwierdzić osobny przegląd aspektu `suwaru/tatsu/noru/tsukareru/damaru/odoroku/sumu` i przeczeń `shiru` przed zmianą ich istniejących glossów?
4. Dla `kesu/kiku/suu` wybrać jedno znaczenie na obecne ID, czy zaprojektować osobne leksykalne zastosowania? Nie zmieniam ID ani nie tworzę duplikatów w C1.
5. Czy zawężenia starych ról z `hitori`, `concrete`, wildcardami i mediami mają trafić do osobnego PR C2.3, z jawnym wykazem utraconych kombinacji?
6. Priorytet dalszego rozwoju: pełne konstrukcje argumentowe czy liczba mnoga (realny przypadek `okane`)? Dla obu potrzebny odrębny zakres akceptacji.

## 15. Powtarzalna kontrola kompletności

Z katalogu repozytorium:

```sh
python tools/validate_verb_dictionary_audit.py
python tools/validate_verb_dictionary_audit.py --kotomi ../Kotomi
python tools/validate_repository.py
python tools/validate_question_patterns.py
KOTOMI_PATH=/absolute/path/to/Kotomi python -m unittest discover -s tests -q
```

Walidator C1 nie stosuje propozycji i niczego nie zapisuje. Oczekiwany zestaw operacji wyznacza z rekordów A, czterech przejrzanych map, istniejących map i istniejących ról, niezależnie od `changes` i statystyk. Wymaga dokładnej zgodności operacji, wartości, ścieżek i zależności. Brak, nadmiar, duplikat, zależność cykliczna albo od innej roli i próba nadpisania kończą się błędem. Kontroluje także liczbę zmodyfikowanych form oraz wszystkie pozostałe statystyki.

Bez `--kotomi` sprawdza kompletność JSON/CSV względem `verbs.xml` i `nouns.xml`, pełne atrybuty lokalnych deklaracji ról (w tym `government`), istniejące mapy i przypisanie klas do każdego zaakceptowanego podmiotu A/D. Nie odtwarza samodzielnie semantyki dopasowania. Wypisuje `SKIPPED` dla kontroli wymagających silnika. Statyczna liczba gotowych czasowników pochodzi ze sprawdzonych strukturalnie snapshotów dostępności; rzeczywista dostępność oraz liczba rozwiniętych wzorców wymagają silnika.

Z `--kotomi` ładuje deklarowany graf XML projektu przez `QuizProject`, wykonuje pełną walidację, porównuje katalog definicji ról (w tym wartości domyślne), klasy kontraktu języka, klasy rzeczowników, liczbę wzorców i dostępność obu przydawek dla wszystkich czasowników i czterech form. Porównuje wszystkie rzeczywiste `matched_nouns` przez oryginalne `role_matches`, zachowując OR, wildcard, domyślne role i dziedziczenie kategorii. Nie ma drugiej implementacji tych reguł.

Samodzielne sprawdzanie ma koszt liniowy względem form, rekordów i propozycji. Wariant silnikowy dodatkowo ładuje i waliduje projekt, porównuje każdą rolę z rzeczownikami (R × N) oraz wykonuje osiem zapytań o dostępność na czasownik. Czytanie produkcji jest osobną kontrolą pokrycia konkretnego audytu, której fixture nie zastąpi. Testy jednostkowe importują czyste funkcje walidatora, lecz czytają wyłącznie wersjonowany syntetyczny `tests/fixtures/c1/v1.json`. Opcjonalne cztery testy kontraktu używają `KOTOMI_PATH` i syntetycznych obiektów modeli, bez ładowania projektu lub słowników.

Eksperyment parsera/generatora można odtworzyć z `changes`: skopiować przypięty Content do katalogu tymczasowego; wykonać wyłącznie addytywne operacje w tej kopii; załadować przez `QuizProject.load`; porównać wyniki czterech form i oba wzorce wskazane w JSON. Nie używać Save All na produkcyjnym projekcie. Manifest tymczasowej kopii nie jest manifestem do wydania; C1 nie generuje nowych manifestów.

## 16. Źródła językowe i granice ich zastosowania

Ocena konkretnych par pochodzi z przeglądu danych, a nie z deklaracji, że słownik internetowy zatwierdził każdą z nich. Pomocniczo sprawdzono:

- [NINJAL, のんびり](https://www2.ninjal.ac.jp/Onomatope/50_on/nonbiri.html): spokojny odpoczynek i relaks oraz kontekstowe oceny powolności.
- [NINJAL, 来る](https://www2.ninjal.ac.jp/verbhandbook/headwords/来る.html): kierunek ruchu ludzi, zwierząt i pojazdów, w tym ptaków wędrownych; brak ograniczenia do chodu.
- [Japan Foundation, 可能形](https://www.kyozai.jpf.go.jp/kyozai/material/BTS00063/ja/render.do): nie każdy czasownik ma produktywną formę potencjalną; wymieniono m.in. わかる.
- [TUFS, 可能形](https://www.coelang.tufs.ac.jp/mt/ja/gmod/contents/explanation/074.html): reguły kształtu form potencjalnych, które nie rozstrzygają znaczenia konkretnego leksemu.
- [Tae Kim, Negative Verbs](https://guidetojapanese.org/learn/grammar/negativeverbs): koniugacja przeczeń, wyjątek ある oraz rozróżnienie istnienia istot żywych.
- [Tae Kim, Other uses of the te-form](https://guidetojapanese.org/learn/grammar/teform): stan wynikowy, wiedza, różnica względem samej czynności i czasowniki ruchu.
- [Tae Kim, Potential Form](https://guidetojapanese.org/learn/grammar/potential): formy potencjalne i ich konstrukcja.
- [Tae Kim, Causative and Passive Verbs](https://guidetojapanese.org/learn/grammar/causepass): zmiana ról uczestników, odczyt kauzatywny i bierny.
- [Tae Kim, Making commands](https://guidetojapanese.org/learn/complete/command): wyjątek くれる → くれ.
- [Tae Kim, Giving and Receiving](https://guidetojapanese.org/learn/complete/giving_receiving): perspektywa dającego/otrzymującego.
- [WSJP PAN, zapominać, o kłopotach](https://wsjp.pl/haslo/podglad/16991/zapominac/3776885/o-klopotach): warianty rekcji, w tym dopełniacz/biernik i „o + miejscownik”.

Źródła wspierają zasady i wymienione rozróżnienia. Nie zastępują decyzji o docelowym znaczeniu słowa w Kotomi. W szczególności audyt nie proponuje automatycznej poprawy japońskich form ani polskiej odmiany na podstawie samego paradygmatu.

## 17. Historyczne wyniki pomiarów czasu

**Wyniki sprzed review, nieuruchomione ponownie.** Wszystkie liczby w tej sekcji dotyczą starego zestawu 34 A / 316 wpisów / 33 role / 307 par, nie aktualnego zakresu. Zachowano je jako materiał historyczny, bez deklaracji bieżącej wydajności.

| Wzorzec | Tryb | Operacja | Przed, mediana ms | Po, mediana ms | Mediana zmiany w parach |
|---|---|---|---:|---:|---:|
| dopełnieniowy | cold | load | 75.69 | 74.60 | -3.40% |
| dopełnieniowy | cold | compatibility | 10.42 | 10.93 | +11.87% |
| dopełnieniowy | cold | exists | 8.65 | 8.79 | +2.60% |
| dopełnieniowy | cold | count | 508.21 | 508.33 | +2.38% |
| dopełnieniowy | cold | first_question | 11.40 | 11.09 | -7.85% |
| dopełnieniowy | warm | compatibility | 9.87 | 9.74 | -0.48% |
| dopełnieniowy | warm | exists | 8.44 | 8.18 | -1.33% |
| dopełnieniowy | warm | count | 539.10 | 522.19 | -5.57% |
| dopełnieniowy | warm | first_question | 10.78 | 10.59 | -0.68% |
| podmiotowy | cold | load | 74.93 | 71.45 | -8.91% |
| podmiotowy | cold | compatibility | 14.70 | 16.67 | +36.29% |
| podmiotowy | cold | exists | 11.44 | 17.28 | +51.33% |
| podmiotowy | cold | count | 21.43 | 110.44 | +434.59% |
| podmiotowy | cold | first_question | 13.54 | 19.21 | +36.75% |
| podmiotowy | warm | compatibility | 11.33 | 16.35 | +51.09% |
| podmiotowy | warm | exists | 11.31 | 15.97 | +36.70% |
| podmiotowy | warm | count | 18.86 | 114.77 | +516.41% |
| podmiotowy | warm | first_question | 15.11 | 18.35 | +21.40% |

Pierwsza seria pokazała +11,87% w cold compatibility istniejącego wzorca dopełnieniowego. Dlatego wykonano dokładnie jedną dodatkową, izolowaną serię 21 naprzemiennych par: 9.92 → 10.01 ms, mediana zmian w parach **+0.83%**. Pierwotne próbki zachowano. Nie potwierdzono w tej powtórce pogorszenia przekraczającego 10%.

Dla rozszerzonego wzorca podmiotowego liczenie rośnie z około 19–21 ms do 110–115 ms przy wzroście puli z 100 do 1535 realizacji na formę. Pierwsze pytanie na świeżym projekcie ma medianę około 19 ms zamiast 14 ms. To mierzalny koszt nowych danych, nie wynik zerowy; pozostaje mały w tym środowisku, ale nie stanowi gwarancji szybkości na telefonie. C2 powinno zachować ten scenariusz pomiarowy i wykonać kontrolę docelowego urządzenia.

Zmiana procentowa jest medianą ilorazów wewnątrz par, dlatego nie musi być równa ilorazowi dwóch osobno podanych median. Warm question oznacza kolejne pytanie po jednym wywołaniu rozgrzewającym. Nie zmieniono żadnego limitu ani solvera.
