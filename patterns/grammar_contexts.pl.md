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
wartości konkretnych wystąpień i `render_occurrences`. Gotowy tekst nie jest
ponownie parsowany, więc nawiasy klamrowe w wartości pozostają tekstem.
Cache wyniku nie jest indeksowany samym aliasem słowa.

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
w szablonie: orzeczenie rozpoczyna zdanie, jeśli przed jego tokenem są tylko
białe znaki. W środku zdania zachowuje zapis z katalogu. Nie obniżamy bezwarunkowo
wielkości liter całego fragmentu i nie analizujemy interpunkcji gotowego wyniku.

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

Content 52 wymaga Kotomi 1.5, aplikacja ma wersję 1.5.0. Starsza aplikacja odrzuci
nowe dane przed instalacją. Nie obsługujemy historycznego XML z usuniętym atrybutem.
Najpierw zmerguj PR Data, potem PR aplikacji. Zachowaj commit przypięty gitlinkiem;
po squash merge zaktualizuj przypięcie i sprawdź je przed merge aplikacji.
Oba PR-y wymagają review i zielonego CI, bez automatycznego merge.


Przymiotnik nieodmienny nie ma obecnie trwałej deklaracji nieodmienności. Normalizacja usuwa nadpisania identyczne z formą wspólną. Przy wymaganym rodzaju żeńskim, nijakim w mianowniku lub liczbie mnogiej brak nadpisania daje Unsupported. Dodanie takich samych wartości jako nadpisań nie jest obejściem tego ograniczenia.
