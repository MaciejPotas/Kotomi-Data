# Audyt pełnych uzgodnień polskich, Content 69

Audyt obejmuje wszystkie **394 wpisy w 11 słownikach**, wszystkie zapisane formy czasowników, siedem klas zgodności, przypadki rzeczowników i profile liczebników. Punktem odniesienia jest Content `e604502180113b47235a7724a09fe37f7dc9ca3b` (rewizja 68). Raport per słowo i forma: [polish_agreement_review.json](../validation/polish_agreement_review.json). To dokument audytu, nie konfiguracja silnika ani fixture testowy.

## Wyniki i poprawki

| Zakres | Wynik |
|---|---|
| Czasowniki | 124 przejrzane, 118 uzupełnionych, **7388 dodanych komórek**, łącznie 9612 |
| Podstawowe formy skończone | 115 czasowników z siedmioma klasami; 3 procesowe z czterema klasami zgodnymi z rolą; 6 wyjątków opisanych poniżej |
| Pozostałe formy czasownika | Uzupełnione istniejące formy potencjalne, warunkowe, kauzatywne, progressive, desiderative oraz 58 prostych form biernych |
| Rzeczowniki | 90/90 ma siedem przypadków; wszystkie 68 wpisów z liczeniem ma pełne istniejące profile few/many |
| Przymiotniki | 92/92 ma pełną macierz siedmiu klas i siedmiu przypadków |
| Pytajniki | Pięć odmieniających się przymiotnikowo ma pełną macierz; pozostałych 17 wymaga właściwej konstrukcji, a nie 49 komórek odmiany |
| Zaimki wskazujące | Trzy określniki mają pełną macierz; trzy samodzielne zaimki zachowują własną odmianę |
| Liczebniki | 11/11 sprawdzonych, **90 dodanych komórek**; jawna nowa klasa męskoosobowa, poprawne „dwaj/trzej/czterej”, „dwóch/trzech/czterech”; „jeden” ma też wołacz przymiotnikowy |
| Pozostałe słowniki | 16 przysłówków, 7 łączników, 1 kopula, 23 liczniki, 2 wyrażenia; kopula i złożenia liczebnikowe korzystają z katalogów, brak podstaw do dopisywania im odmiany czasownikowej |

Zachowano dotychczasowe tłumaczenia bazowe, japońskie formy i kategorie ról. Dodano 28 brakujących form japońskich (21 progressive i 7 desiderative) wraz z przekładami i uzgodnieniami oraz oznaczono siedem czasowników ruchu jako nieprzechodnie. Uzupełnienia czasowników zachowują aspekt i zwrotność konkretnej zapisanej formy, np. „podniosłem” daje „podniósł/podniosła/podnieśli”, a nie formy od bezokolicznika „podnosić”. Odmianę sprawdzono przez SGJP/Morfeusz 2; warianty „otworzył” i „śmiali się” oraz konstrukcje opisowe zostały rozstrzygnięte jawnie. Nowe mapy `kureru` odnoszą się do dawcy („daje mi / dają mi”), zachowując odbiorcę „mi”.

## Przykład: hataraku

| Forma | Mężczyzna | Kobieta | Grupa męskoosobowa | Grupa niemęskoosobowa |
|---|---|---|---|---|
| polite_nonpast | pracuje | pracuje | pracują | pracują |
| past_polite | pracował | pracowała | pracowali | pracowały |
| past_negative_polite | nie pracował | nie pracowała | nie pracowali | nie pracowały |
| potential | może pracować | może pracować | mogą pracować | mogą pracować |
| tara | jeśli pracuje | jeśli pracuje | jeśli pracują | jeśli pracują |
| causative | każe komuś pracować | każe komuś pracować | każą komuś pracować | każą komuś pracować |

Są też osobne komórki rodzaju nijakiego i obu pozostałych rodzajów męskich oraz formy potoczne i progressive. Zwykły quiz bez `agree` nadal korzysta z oryginalnego „pracuję”.

## Uzasadnione puste pola

- `aru_existential`, `iru`: formy skończone realizuje katalog egzystencjalny wraz z rekcją, w tym „nie ma rodziców”. Pozostałe konstrukcje wymagają odrębnej analizy uczestników.
- `fuku`, `furu`, `hareru`, `kumoru`: obecny model opisuje zjawiska pogodowe bez leksykalnej roli podmiotu. Kauzatywność i strona bierna zmieniają role uczestników, więc nie są mechaniczną odmianą pogody przez rodzaj osoby.
- `aku`, `shimaru`, `owaru`: formy podstawowe, warunkowe i potencjalne (gdy istnieją) obejmują rodzaj męski nieżywotny, żeński, nijaki i mnogi niemęskoosobowy. Wariantów osobowych nie dopisano wbrew ograniczeniom roli.
- `te_form` ma przekład imiesłowowy bez osoby/liczby, `volitional` wyraża intencję mówiącego lub pierwszą osobę mnogą, a `imperative` odnosi się do adresata. Nie należy wpisywać trzeciej osoby we wszystkie pola tych form.
- 58 zapisanych form biernych pozostaje bez map: obejmują skutki dla osoby i opisowe konstrukcje z „ktoś”, „mi”, „mnie”. Ich poprawne użycie wymaga przypadku, perspektywy i powiązania uczestników. Nie są oznaczone jako w pełni uzgodnione.
- Liczebniki główne 2+ nie mają odrębnego paradygmatu wołacza w SGJP. Nie wpisano tam sztucznych wartości. Profile few/many rzeczownika nie zmieniają jego podstawowej klasy zgodności.

## Dodatkowe ustalenia z audytu wzorców

- `mieru`: kategoria `concrete` obejmuje także `person` i `animal`. Uzupełniono więc wszystkie siedem klas, w tym „jest widoczny / są widoczni”. Poprzednie uzasadnienie ograniczenia do przedmiotów było błędne.
- `donata`: dodano sześć właściwych przypadków „kto”, w tym „kim” wymagane przez pytanie o towarzysza. Zachowano bazowe oznaczenie grzeczności.
- Wzorzec miejsca zamieszkania ma teraz jawne `id:sumu`. Wzorzec podróży bez dopełnienia wybiera czasowniki `feature:intransitive`; dotychczasowe `iku` pozostaje dostępne. Siedem odpowiednich czasowników ma tę cechę. Wzorce nie powinny polegać na przypadkowym braku form u pozostałych kandydatów.
- `hataraku` ma również nową formę `desiderative`: „chcę pracować / chce pracować / chcą pracować”.
- `sugosu/companion` otrzymał właściwą rekcję `z_instrumental`; sprawdzono ją w generatorze. Pełne znaczenie „spędzać czas” nadal wymaga argumentu czasu lub kontekstu.
- Pozostaje 11 brakujących ramek rekcji: dziesięć ról `target` ma jawne decyzje w [C3.2](target_government_c32.md), a `hanashiau/companion` zawiera perspektywę „ze sobą”. Wymagają decyzji o konstrukcji i znaczeniu. Nie dopisano jednej rekcji dla niejednorodnych dopełnień tylko po to, aby usunąć zgłoszenie audytora.

[Japońskie znaczenie ている, Japan Foundation](https://www.irodori.jpf.go.jp/assets/data/elementary02/pdf/Z_L02.pdf) rozróżnia trwającą czynność i stan wynikowy. Nowe glosy są jawne, bez generowania tłumaczeń w silniku.

## Weryfikacja i architektura

Przegląd 114 wzorców sprawdził 423 567 relacji, z czego 415 903 zweryfikował. Pozostało 4086 nieweryfikowanych jednostek (limity i nieobsługiwane zakresy); **pokrycie nie jest pełne**. Z 16 zgłoszonych błędów poprawiono cztery brakujące formy oraz rekcję `sugosu`; ponowne audyty tych pięciu słów nie wykazały błędów. Pozostałe 11 ograniczeń rekcji opisano wyżej. Nie przedstawiamy kontroli częściowej jako enumeracji wszystkich zdań.

Pełny `QuizProject.validate()` po zmianach: **0 problemów**. W rendererze sprawdzono **9612/9612 komórek czasowników**, z syntetycznymi reprezentantami klas rzeczownika i porównaniem japońskiego wyniku z zapisaną formą. Ten test diagnostyczny sprawdza komórki, nie wszystkie kombinacje ról i zdań.

Audyt aplikacji wykrył błąd autouzupełniania: SGJP zwraca wszystkie stopnie jednego leksemu, a wybór wyłącznie `pos` zmieniał „najlepszy” w „dobrzy”. Poprawka zachowuje stopień wejściowy i ma niezależne testy. Walidator używa teraz katalogu jawnych klas języka zamiast wpisanej na sztywno polskiej nazwy.

Oba narzędzia audytu pokazują brakujące klasy dla każdej formy. Zielona walidacja XML lub kompletność ośmiu form męskoosobowych nie oznacza już pełnej tabeli uzgodnień. Historyczny gate C2 zachowuje wszystkie zatwierdzone wartości i role, dopuszczając jawnie dozwolone uzupełnienia innych klas.

Nowe testy jednostkowe używają wyłącznie małych, niezależnych danych. Audyt realnego Content jest osobnym, uruchamianym na żądanie krokiem. Pełna enumeracja wszystkich zdań, kontrola językowa wszystkich dawnych tłumaczeń oraz Android nie są wynikiem tego audytu.
