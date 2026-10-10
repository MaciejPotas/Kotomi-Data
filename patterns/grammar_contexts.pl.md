# Konteksty gramatyczne i wspólne wybory słów

Alias wybiera słowo raz. Dwa wystąpienia `noun@item` nadal oznaczają jeden
rzeczownik, a dwa `adjective@quality` jeden przymiotnik. `OccurrenceId` wskazuje
konkretny token w pytaniu lub odpowiedzi. Kontekst gramatyczny łączy jego lokalną
realizację z ilością, orzeczeniem i opcjonalnym przymiotnikiem. To trzy osobne
tożsamości. Nazwanie kontekstu nie tworzy kolejnego wyboru słowa.

## Jak to zapisać

Przy policzonym rzeczowniku z rekcją dodaj `occurrence:left`. Pozostałe składniki
mogą podać tę samą nazwę albo wskazać ją przez zależność, np.
`agree:@item#left`. To odwołanie do efektywnej realizacji rzeczownika w lewym
kontekście, a nie do drugiej książki w słowniku. Zależności jednego składnika
muszą wskazywać ten sam kontekst. Przy jednym kontekście nadal wystarczy
`agree:@item`. Jeśli rzeczownik ma kilka kontekstów, trzeba dopisać adres.

Liczebnik ma również `case:@item#left`, ponieważ potrzebuje przypadku całej
konstrukcji. Przy przymiotniku nie powtarzamy `case`: kontekstowe `agree` dostarcza
zarówno klasę uzgodnienia, jak i efektywny przypadek. Dlatego mamy „pięć czerwonych
książek”, choć twierdząca konstrukcja ma mianownik. Poza konstrukcjami liczebnymi
jawne uzgodnienie i przypadek zachowują osobne znaczenia.

Planer rozpoznaje konstrukcję po zależnościach i cesze `existential`. Nie ma już
pola ani atrybutu `semantics_version`, nie zastępuje go żaden ukryty tryb.
Zostają wersja schematu XML, wersja aplikacji i rewizja Content.

## Działający pattern

```xml
<sentence_pattern id="Dwie policzone grupy opisanych rzeczowników" category="counting">
      <question>{verb@existence[role:subject, feature:existential, form, occurrence:left, agree:@left_count#left].translation} {number@left_count[set:one_to_ten, occurrence:left, agree:@item#left, case:@item#left].translation} {adjective@quality[form:attributive_nonpast, occurrence:left, agree:@item#left].translation} {noun@item[occurrence:left, quantity:@left_count#left, government:@existence#left]}, a obok {verb@existence[role:subject, feature:existential, form, occurrence:right, agree:@right_count#right].translation} {number@right_count[set:one_to_ten, occurrence:right, agree:@item#right, case:@item#right].translation} {adjective@quality[form:attributive_nonpast, occurrence:right, agree:@item#right].translation} {noun@item[occurrence:right, quantity:@right_count#right, government:@existence#right]}.</question>
      <answer>{adjective@quality[form:attributive_nonpast]}{noun@item}が{counter@unit[counts:@item, preferred, quantity:@left_count]}{verb@existence[role:subject, feature:existential, form]}。そのとなりに{adjective@quality[form:attributive_nonpast]}{noun@item}が{counter@unit[counts:@item, preferred, quantity:@right_count]}{verb@existence[role:subject, feature:existential, form]}。</answer>
    </sentence_pattern>
```

Pattern jest w quizie Liczenie (`counting`). Japońska odpowiedź używa dwóch zdań
połączonych znaczeniowo przez そのとなりに, czyli „obok tego”. Obie części mają
własną ilość, ale wspólny rzeczownik, przymiotnik i wybór ある/いる.

Dla book, akai, ilości 1 i 5 oraz formy past_plain silnik daje:

> Była jedna czerwona książka, a obok było pięć czerwonych książek.
>
> あかいほんがいっさつあった。そのとなりにあかいほんがごさつあった。

Osobne wybory to `number@left_count` i `number@right_count`. Wspólne pozostają
`noun@item`, `adjective@quality`, `verb@existence` i `counter@unit`.

## Co robi silnik

`RealizationPlan.constructions` przechowuje osobne zależności konstrukcji,
a `occurrence_requests` przypisuje żądania do `OccurrenceId`. Widok indeksowany
tekstem tokena służy istniejącym podglądom i diagnostyce. Składanie zdania używa
wartości konkretnych wystąpień i mechanizmu `render_occurrences`. Gotowy tekst nie jest
ponownie parsowany, więc nawiasy klamrowe w wartości pozostają tekstem.
Cache wyniku nie jest indeksowany samym aliasem słowa.
Zapis do mapowania (także `update`, `setdefault` i `|=`) aktualizuje pasujące
wystąpienia, a usunięcie klucza usuwa ich wartości. `copy()` zachowuje niezależne
wartości lokalne. `render_text(fragment, preview.replacements)` używa widoku
indeksowanego tekstem tokena dla innego fragmentu, zachowując API mapowania.
Formatowanie polskiego pytania zmienia wyłącznie wskazane wystąpienie w pytaniu.

Brak zależności daje Pending, więc nie odrzuca jeszcze poprawnego częściowego
wyboru. Dopiero kompletny kontekst bez wymaganej odmiany daje Unsupported.
Obecny solver MRV sprawdza gotowe żądania i przed zaakceptowaniem zdania wymaga
wszystkich obowiązkowych realizacji. Preview, wyjaśnienia, enumeracja, statystyki,
quiz i bound rendering korzystają z tego samego planu oraz reguł warstwy języka.
Zakresy liczbowe są nadal leniwe. Polskie formy liczb pochodzą ze skończonego
katalogu, bez przechodzenia po milionie wartości.

Żeby odtworzyć preview przez bound rendering, przekaż jego słowa, rzeczowniki,
formy i wybrany kontekst sytuacyjny. Dynamiczne orzeczenie wymaga jawnej formy.
Obie części mogą współdzielić czas i negację. Wielka litera wynika z pozycji
w szablonie: orzeczenie rozpoczyna zdanie na początku szablonu lub po znaku
kończącym zdanie (`.`, `!`, `?`, `。`, `！`, `？`) w poprzedzającym statycznym
fragmencie. Po tym znaku mogą wystąpić białe znaki, cudzysłowy i nawiasy, ale nie
tekst słowny. Pozostałe orzeczenia zachowują zapis z katalogu. Ta konwencja
szablonu nie rozróżnia skrótów od końca zdania. Kropki w składni placeholderów
ani interpunkcja wygenerowanych wartości nie wyznaczają granic zdań.

Composite nadaje kontekstom ten sam zakres `embedded_*` co aliasom, osobno dla
każdego osadzenia. Wewnątrz fragmentu zachowuje wspólne wybory, między osadzeniami
je rozdziela. Analiza odrzuca nieznane adresy, duplikaty, brakujące składniki,
sprzeczne zależności, niejednoznaczne odwołania i cykle przypadków. Studio podpowiada
nazwy kontekstów i adresy, a błędy sprawdza tym samym analizatorem.

## Zakres i wydanie

Obsługiwane są rodzaje: żeński, nijaki, męski nieżywotny i męski żywotny;
jeden opcjonalny przymiotnik na kontekst; teraźniejszość, przeszłość, twierdzenie,
negacja oraz japońskie formy zwykłe i grzeczne. Negacja dotyczy braku wskazanej
grupy, nie ogólnego rozstrzygania zakresu zaprzeczenia. Męskoosobowość, liczebniki
zbiorowe, pluralia tantum, łańcuchy słów i generator fleksji pozostają poza zakresem.
Przymiotniki nieodmienne zachowują dotychczasowe ograniczenie jawnych nadpisań.

Nazwane konteksty dotyczą obecnie źródłowych konstrukcji liczebnych. Japońskie
liczniki korzystają z osobnych `quantity:@alias`. Różne selekcje orzeczenia dla
jednego wspólnego rzeczownika są nadal odrzucane przez analizę rekcji. Użyj
wspólnego `verb@existence`, jak w przykładzie. Jeden kontekst ma po jednej
źródłowej realizacji składnika; kolejne użycie wymaga osobnego kontekstu.
Nie powstał drugi solver ani osobny edytor kontekstów.

Aktualny Content 57 wymaga Kotomi 1.7, aplikacja ma wersję 1.7.0. Ta wersja obejmuje także referencje kontekstów. Starsza aplikacja odrzuci
nowe dane przed instalacją. Nie obsługujemy historycznego XML z usuniętym atrybutem.
Najpierw zmerguj PR Data, potem PR aplikacji. Zachowaj commit przypięty gitlinkiem;
po squash merge zaktualizuj przypięcie i sprawdź je przed merge aplikacji.
Oba PR-y wymagają review i zielonego CI, bez automatycznego merge.


Przymiotnik nieodmienny nie ma obecnie trwałej deklaracji nieodmienności. Normalizacja usuwa nadpisania identyczne z formą wspólną. Przy wymaganym rodzaju żeńskim, nijakim w mianowniku lub liczbie mnogiej brak nadpisania daje Unsupported. Dodanie takich samych wartości jako nadpisań nie jest obejściem tego ograniczenia.

## Pytania o nieznaną ilość

`how_many` oznacza pytanie „ile”, a nie konkretną liczbę. Wybiera je
`interrogative@amount[asks_for:count]`. Tożsamość `Symbolic("how_many")`
pozostaje niezmieniona również po wybraniu polskiego profilu `many`.
Profil nie podstawia piątki i nie uruchamia przeglądania zakresów liczbowych.

Relacje są takie same jak w zdaniu oznajmującym: rzeczownik wskazuje ilość
przez `quantity:@amount` i orzeczenie przez `government:@existence`, a
orzeczenie wskazuje ilość przez `agree:@amount`. Interrogative ma własne
znaczenie „ile”, więc nie potrzebuje liczebnikowych `agree:@item` ani
`case:@item`. W tym kontekście `agree:@item` na przymiotniku wystarcza.
Nie dopisuj mu `case:genitive` ani `case:@item`.

Polski profil `many` wybiera zapisaną formę rzeczownika, np. „książek”,
„samochodów”, „psów” lub „jabłek”. Konstrukcja twierdząca nadal ma przypadek
nominative, ale efektywna forma rzeczownika i przymiotnika jest dopełniaczem
liczby mnogiej. Dlatego otrzymujemy „czerwonych książek”, mimo że klasa
rzeczownika to feminine. Te trzy informacje nie są zamienne.

Forma orzeczenia pochodzi z katalogu gramatyki. Pytanie ma cztery formy:

| Forma | Polski czasownik | Japońskie zakończenie dla książek |
|---|---|---|
| `dictionary` | jest | `あるの？` |
| `polite_nonpast` | jest | `ありますか？` |
| `past_plain` | było | `あったの？` |
| `past_polite` | było | `ありましたか？` |

Wybór `ある` lub `いる` nadal zależy od rzeczownika. Counter korzysta ze
swojej zapisanej realizacji `how_many`, np. `なんさつ` dla książek lub
`なんびき` dla psów. `{question}` dobiera końcówkę z rejestru formy.
Przymiotnik japoński zachowuje formę przydawkową, także `な` przy
na-adjective, np. `げんきないぬ`.

Przykłady wygenerowane przez silnik: „Ile było czerwonych książek?” →
`あかいほんがなんさつあったの？`, „Ile jest energicznych psów?” →
`げんきないぬがなんびきいるの？`.

Oba wzorce należą do quizu **Liczenie** i wybierają czas dynamicznie:

```xml
<sentence_pattern id="Ile jest policzonych rzeczowników" category="counting">
      <question>{interrogative@amount[asks_for:count].translation} {verb@existence[role:subject, feature:existential, form, agree:@amount].translation} {noun@item[quantity:@amount, government:@existence]}?</question>
      <answer>{noun@item}が{counter@unit[counts:@item, preferred, quantity:@amount]}{verb@existence[role:subject, feature:existential, form]}{question}</answer>
    </sentence_pattern>
<sentence_pattern id="Ile jest opisanych policzonych rzeczowników" category="counting">
      <question>{interrogative@amount[asks_for:count].translation} {verb@existence[role:subject, feature:existential, form, agree:@amount].translation} {adjective@quality[form:attributive_nonpast, agree:@item].translation} {noun@item[quantity:@amount, government:@existence]}?</question>
      <answer>{adjective@quality[form:attributive_nonpast]}{noun@item}が{counter@unit[counts:@item, preferred, quantity:@amount]}{verb@existence[role:subject, feature:existential, form]}{question}</answer>
    </sentence_pattern>
```

Planer rozpoznaje pytanie po zależnościach i `asks_for:count`. Nie sprawdza
nazwy wzorca ani sąsiedztwa tokenów. Zwykły `RealizationRequest` dostaje
wspólne zależności konstrukcji, a polska warstwa korzysta z tej samej operacji
co dla liczebników. Nie ma drugiego solvera. Brak wyboru daje `Pending`;
komplet wyborów bez wymaganych form daje `Unsupported`. Błąd struktury
pozostaje błędem konfiguracji. Wyjaśnienia, preview, enumeracja, statystyki,
preflight, quiz i bound rendering korzystają ze wspólnego planu.

Reguła `asks_for="count"` dopuszcza present/past i wyłącznie affirmative.
Nie obsługujemy pytań „Ile nie ma…” ani „Ile nie było…”. Wymuszona negacja
jest odrzucana także przez bound rendering i `render_answer_with_forms`.
Pozostałe intencje pytań zachowują dotychczasowe reguły. Przeczące zdania
z konkretną liczbą nadal działają. Ograniczenia klas rzeczowników i jawnych
form przymiotników opisane wyżej nadal obowiązują.

Aktualny Content 57 wymaga Kotomi 1.7. Aplikacja ma wersję 1.7.0. Najpierw zmerguj
PR danych, następnie PR aplikacji. Zachowaj commit danych wskazany przez
gitlink. Po squash merge trzeba przypiąć wynikowy commit i ponownie sprawdzić
manifesty oraz CI. Samo wdrożenie aplikacji 1.7 może nadal używać starszych danych.
