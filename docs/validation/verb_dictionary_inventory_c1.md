# C1: pełne zestawienie czasowników

Każdy wiersz odnosi się do przypiętych rewizji z raportu głównego. A/B/C/D opisuje cztery formy priorytetowe i zwykłe przydawki podmiotowe. Pozostałe formy mają niezależną ocenę w pliku form. Liczba Agreement to liczba obecnych form z mapą, nie liczba klas.

Skróty podmiotów: **P** = friend, mother, sister, teacher, roujin, hito, programmer, madogiwazoku; **P+Z** = P oraz inu/tori; **P+pies** = P oraz inu. W B to tylko kandydaci do decyzji, nie nowe role. Pełne bieżące dopasowania wszystkich ról są w JSON.

| ID | Znaczenie | Typ | Role obecne | Subject | Agreement | Braki | Podmioty | Ryzyko | Kategoria | Rekomendacja |
|---|---|---|---|---|---|---|---|---|---|---|
| abiru | brać prysznic | ichidan | location | do decyzji | 0 | decyzja przed mapami | P | medium | B | Samodzielne あびる nie nazywa prysznica; ustalić, czy pomijany シャワー jest uzasadniony w tym quizie. Negacja wymaga prysznica. |
| ageru | podnosić | ichidan | object, location | do decyzji | 0 | decyzja przed mapami | P | medium | B | Znaczenie 上げる, nie dawanie. Bez przedmiotu podnoszenia przydawka jest niedookreślona; lista object dopuszcza m.in. muzykę i abstrakcyjne nośniki. |
| ajiwau | delektować się | godan | object, location | do decyzji | 0 | decyzja przed mapami | P | medium | B | Potrzebny przedmiot doświadczenia; instrumental_object jest zgodny z polskim delektować się czymś. Passive jest smakowane zmienia perspektywę i znaczenie. |
| akeru | otwierać | ichidan | object, location | do decyzji | 0 | decyzja przed mapami | P | medium | B | Otwiera coś, odmiennie od aku. Zachować bag/box; dla podmiotowej przydawki potrzebne jawne dopełnienie albo zatwierdzony kontekst. |
| aku | otwierać się | godan | subject, location | istnieje | 4 | brak w zakresie | bag, box | low | D | Cztery formy i klasy feminine/neuter już poprawnie zapisane dla bag/box. Nie rozszerzać na osoby ani drzwi bez obsługi liczby mnogiej. |
| arau | myć | godan | object, location | do decyzji | 0 | decyzja przed mapami | P | medium | B | Myje kogoś lub coś, a nie myje się. Bez dopełnienia grozi zmianą interpretacji; nie dodawać się automatycznie. |
| aru_possessive | mieć | godan | subject | istnieje | 0 | decyzja przed mapami | brak bezpiecznych obecnie | high | C | Subject oznacza rzecz posiadaną, nie właściciela. Nie dodawać tych kandydatów jako agreement: pudełko ma byłoby odwróceniem argumentów. Ten wpis nie ma cechy existential. |
| aru_existential | być, istnieć | godan | subject | istnieje | 0 | decyzja przed mapami | brak bezpiecznych obecnie | high | C | Istnienie z government:existential_subject i katalogiem. Negacja nie ma/nie było wymaga dopełniacza, nie mianownikowego podmiotu i zwykłego B2. |
| aruku | iść pieszo | godan | destination, location | zalecane | 0 | 4 mapy | P | low | A | Samodzielny ruch pieszy ma naturalnego wykonawcę; do C2 tylko ludzie, bo pies idzie pieszo jest stylistycznie nienaturalne. |
| asobu | bawić się | godan | companion, location | zalecane | 0 | 4 mapy | P+Z | low | A | Zabawa ludzi i zwierząt może wystąpić bez wskazania towarzysza. Zachować istniejącą rekcję towarzysza. |
| au | spotykać się | godan | companion, location | do decyzji | 0 | decyzja przed mapami | P | medium | B | Przy liczbie pojedynczej potrzebny partner spotkania lub kontekst. Nie utożsamiać samotnego spotyka się z pełną konstrukcją wzajemną. |
| ayamaru | przepraszać | godan | target, location | zalecane | 0 | 4 mapy | P | low | A | Osoba może przepraszać bez jawnego adresata; target pozostaje niezależną rolą, bez poszerzania jej obecnej listy. |
| chigau | różnić się | godan | brak | do decyzji | 0 | decyzja przed mapami | keikaku, yotei, aji, book | medium | B | Wymaga rozstrzygnięcia różnić się od czegoś versus być innym/błędnym; brak wspólnego kontekstu porównania. ちがえる nie oznacza zwykle zdolności różnienia się. |
| dasu | wyjmować | godan | object, location | do decyzji | 0 | decyzja przed mapami | P | medium | B | Bez wyjmowanego przedmiotu zdanie niepełne; abstract/media w object wymagają przeglądu wybranego znaczenia 出す. |
| dekiru | móc | ichidan | brak | osobna konstrukcja | 0 | decyzja przed mapami | P | high | C | Modalne móc wymaga dopełnienia bezokolicznikowego. Istnieje konstrukcja ことができる; nie potrzeba nowego DSL, ale zwykła podmiotowa przydawka sama nie wystarcza. |
| deru | wychodzić | ichidan | route | zalecane | 0 | 4 mapy | P+Z | low | A | Ludzie i zwierzęta mogą wychodzić bez jawnego miejsca wyjścia. Zachować route; nie rozszerzać na publikacje i pojazdy w tym znaczeniu. |
| fuku | wiać | godan | location | do decyzji | 0 | decyzja przed mapami | brak bezpiecznych obecnie | medium | B | Meteorologiczne 吹く wymaga wiatru jako nazwanego podmiotu, którego brak w rzeczownikach. Obecna bezosobowa forma wiało jest poprawna w konstrukcji pogodowej. |
| furu | padać | godan | location | do decyzji | 0 | decyzja przed mapami | brak bezpiecznych obecnie | medium | B | Brak rzeczowników deszcz/śnieg. Nie uzgadniać z dowolną rzeczą; potencjalność pogody nie jest automatycznie zdolnością działania. |
| hairu | wchodzić | godan | target | zalecane | 0 | 4 mapy | P+Z | low | A | Wchodzenie ludzi i zwierząt jest naturalne bez jawnego celu w krótkiej przydawce. Zachować target=place. |
| hajimeru | zaczynać | ichidan | object, location | do decyzji | 0 | decyzja przed mapami | P | medium | B | Przechodnie zaczynać coś; nie zamieniać na zaczyna się. Subject dopiero z treścią rozpoczynanej czynności lub kontekstem. |
| hanashiau | rozmawiać ze sobą | godan | companion, location | osobna konstrukcja | 0 | decyzja przed mapami | P | high | C | Obecne rozmawiamy ze sobą jest mnogie. Potrzebny partner przy liczbie pojedynczej, np. rozmawia z mamą; istniejąca rola companion może go reprezentować po sprawdzeniu rekcji. |
| hanasu | rozmawiać, mówić | godan | companion, location | zalecane | 0 | 4 mapy | P | low | A | Rozmawia może opisywać osobę bez jawnego partnera. Nie rozszerzać na zwierzęta ani zastępować tego automatycznie znaczeniem opowiadać o czymś. |
| harau | płacić | godan | object, location | zalecane | 0 | 4 mapy | P | low | A | Samodzielne płaci/zapłacił jest naturalne; zachować object=okane. Nie zmieniać znaczenia na usuwać/strzepywać. |
| hareru | przejaśniać się | ichidan | location | do decyzji | 0 | decyzja przed mapami | brak bezpiecznych obecnie | medium | B | Aktualne formy są pogodowe i bezosobowe; brak nieba jako rzeczownika. Mieszanie przejaśnia się/rozpogodziło się wymaga decyzji leksykalnej. |
| hashiru | biec | godan | destination, location | zalecane | 0 | 4 mapy | P+Z | low | A | Bieg ludzi i zwierząt jest samodzielną czynnością. Pojazdy i programy pominięte, bo wymagałyby innego polskiego znaczenia. |
| hataraku | pracować | godan | subject, location | istnieje | 4 | brak w zakresie | P | low | D | Obecna dokładna lista ośmiu osób oraz dwie klasy w czterech formach wystarczają. Inne formy nie otrzymują B2 w C1. |
| hiraku | otwierać | godan | object, location | do decyzji | 0 | decyzja przed mapami | P | medium | B | 開く ma zastosowania przechodnie i nieprzechodnie. Obecny wpis jest przechodni; book/school to różne ramy semantyczne, nie dodawać samoczynnie otwiera się. |
| iku | iść | godan | destination | zalecane | 0 | 4 mapy | P+Z | low | A | Idzie/poszedł z żywym wykonawcą jest naturalne. いって/いった są wyjątkami; ている oznacza często stan po odejściu, nie po prostu idzie. |
| ireru | wkładać | ichidan | object, target | do decyzji | 0 | decyzja przed mapami | P | medium | B | Potrzebny wkładany przedmiot, często też cel. accepts i nouns są alternatywami OR; okane dopisuje pieniądze, nie zawęża kategorii. |
| iru | być | ichidan | subject | istnieje | 0 | decyzja przed mapami | brak bezpiecznych obecnie | high | C | Zachować katalog existential i governed noun. Nie kopiować osobowych form jestem/nie ma mnie do przydawek; potrzebna osobna realizacja negacji i miejsca. |
| isogu | śpieszyć się | godan | destination, location | zalecane | 0 | 4 mapy | P | low | A | Samodzielna czynność osoby; zachować zaakceptowaną pisownię śpieszyć, bez kosmetycznej zmiany na spieszyć. |
| iu | powiedzieć | godan | location | do decyzji | 0 | decyzja przed mapami | P | medium | B | Obecny wpis łączy mówi i powiedzieć; w przydawce powiedział zwykle wymaga treści. Istniejące reporting trzeba zachować. |
| kaeru | wracać | godan | destination | zalecane | 0 | 4 mapy | P+Z | low | A | Powrót żywego wykonawcy można opisać bez jawnego celu. Nie zmieniać na ogólne zmieniać, które jest innym czasownikiem. |
| kaku | pisać | godan | object, location | zalecane | 0 | 4 mapy | P | low | A | Pisanie jest naturalne bez jawnego tekstu, np. osoba, która pisze. Zachować object=text i direct_object. |
| kangaeru | zastanawiać się | ichidan | object, location | zalecane | 0 | 4 mapy | P | low | A | Zastanawia się jest samodzielne; przy dopełnieniu pozostaje nad_instrumental. Pojazd jako przedmiot namysłu nie oznacza podmiotu. |
| kariru | pożyczać od kogoś | ichidan | object, target, location | do decyzji | 0 | decyzja przed mapami | P | medium | B | Kierunek pożyczki musi pozostać od dawcy. Tekst od kogoś plus jawny target może dublować argument; nie włączać bez sprawdzenia wzorca. |
| kau | kupować | godan | object, location | zalecane | 0 | 4 mapy | P | low | A | Kupuje może być użyte absolutnie dla kupującej osoby; precyzyjny zakup wymaga object. Zachować istniejące role. |
| kayou | uczęszczać | godan | target | do decyzji | 0 | decyzja przed mapami | P | medium | B | Polskie uczęszcza wymaga dokąd/na co. Obecne school/taiikukan są właściwymi kandydatami, lecz brak celu w przydawce wymaga kontekstu. |
| keikosuru | trenować | irregular | object, location | do decyzji | 0 | decyzja przed mapami | P | medium | B | 稽古する dotyczy ćwiczenia umiejętności/sztuki; trenuję muzykę/piosenkę jest niezgrabne. Rozstrzygnąć ćwiczyć a trenować przed rozszerzeniem. |
| kesu | wyłączać | godan | object, location | do decyzji | 0 | decyzja przed mapami | P | medium | B | Wyłącza telewizję, ale usuwa mail/notatkę. Jeden polski leksem nie realizuje bezpiecznie wszystkich obecnych object. |
| kikokusuru | wracać do kraju | irregular | brak | zalecane | 0 | 4 mapy | P | low | A | 帰国する zawiera powrót do własnego kraju; podmiot ludzki, argument celu zawarty w tłumaczeniu. Nie poszerzać na zwierzęta. |
| kiku | słuchać, pytać | godan | object, location | do decyzji | 0 | decyzja przed mapami | P | medium | B | Słuchać i pytać są różnymi ramami. Passive jestem pytany przełącza znaczenie względem słucham; abstract dopuszcza nieoczywiste przedmioty słuchania. |
| kiru | nosić | ichidan | object, location | do decyzji | 0 | decyzja przed mapami | P | medium | B | 着る to zakładać ubranie, 着ている to nosić/mieć na sobie. Base nosić i potential mogę nosić wymagają wyrównania znaczenia; nie mieszać z 切る. |
| kotaeru | odpowiadać | ichidan | target, location | zalecane | 0 | 4 mapy | P | low | A | Odpowiada może wystąpić bez jawnego pytania. Existing target=abstract pozostaje osobną kwestią precyzji dopełnienia. |
| kumoru | chmurzyć się | godan | location | do decyzji | 0 | decyzja przed mapami | brak bezpiecznych obecnie | medium | B | Pogodowe bezosobowe zachmurzyło się nie ma obecnie właściwego rzeczownika. Zaproponowane osobowe formy wyłącznie dla przyszłego konkretnego podmiotu, nie do XML. |
| kuru | przychodzić | irregular | destination | zalecane | 0 | 4 mapy | P+Z | low | A | Przychodzi żywa osoba/zwierzę. Jawnie uwzględnić nieregularne きた/こない; nie traktować 来ている jako zawsze czynności trwającej. |
| matsu | czekać | godan | object, location | zalecane | 0 | 4 mapy | P+Z | low | A | Czekanie ludzi i zwierząt jest naturalne bez jawnego obiektu; na_accusative pozostaje dla dopełnienia. |
| mieru | być widocznym | ichidan | subject | istnieje | 0 | decyzja przed mapami | dokładna lista w JSON (51) | medium | B | Uzgodnienie dotyczy także przymiotnika w teraźniejszości. concrete obejmuje media, np. głos/muzykę, więc potrzebna kontrola widzialności i precyzyjna lista. |
| migaku | szorować | godan | object, location | do decyzji | 0 | decyzja przed mapami | P | medium | B | Szorować/polerować zależy od przedmiotu. Nie dodawać podmiotu bez dopełnienia i kontroli rzeczy dopuszczonych przez thing. |
| miru | oglądać, patrzeć, widzieć | ichidan | object, location | do decyzji | 0 | decyzja przed mapami | P | medium | B | Widzieć, patrzeć i oglądać nie są wymienne. Wildcard object dopuszcza np. jutro/smak; wymagana selekcja znaczenia przed bezpiecznym rozszerzeniem. |
| mochiageru | podnosić | ichidan | object, location | do decyzji | 0 | decyzja przed mapami | P | medium | B | 持ち上げる podnosi przedmiot; samodzielna przydawka wymaga kontekstu. Nie zakładać, że podnoszenie muzyki jest dosłowną czynnością. |
| motsu | trzymać | godan | object, location | do decyzji | 0 | decyzja przed mapami | P | medium | B | 持つ i 持っている rozróżniają zdarzenie/stan; object=abstract obejmuje posiadanie planu. Trzyma bez dopełnienia nie nadaje się do automatycznego A. |
| motteiku | zabierać | godan | object, destination, location | do decyzji | 0 | decyzja przed mapami | P | medium | B | Zabiera coś w kierunku od punktu odniesienia. Potrzebny przedmiot, zachować odmianę końcowego 行く i jego wyjątki. |
| mottekuru | przynosić | irregular | object, destination, location | do decyzji | 0 | decyzja przed mapami | P | medium | B | Przynosi coś do punktu odniesienia. Zapis 持ってくる odmienia kana końcowego くる; to nie błąd kanji. |
| naku | płakać | godan | subject, location | istnieje | 0 | decyzja przed mapami | P | medium | B | 泣く oznacza płakać, a nie neutralny głos ptaka/psa 鳴く. Obecne animal i hitori wymagają przeglądu, zanim translation odblokuje całą klasę. |
| nakusu | gubić | godan | object, location | do decyzji | 0 | decyzja przed mapami | P | medium | B | Zgubił bez przedmiotu wymaga kontekstu. Zachować rozróżnienie zgubić/przegrać/utracić i selekcję rzeczowników. |
| nareru | przyzwyczajać się | ichidan | target, location | do decyzji | 0 | decyzja przed mapami | P | medium | B | Przyzwyczaja się jest możliwe kontekstowo, lecz target=* i brak dopełnienia do czegoś wymagają weryfikacji polskiej rekcji. |
| naru | stawać się | godan | target | osobna konstrukcja | 0 | decyzja przed mapami | P | high | C | Stawać się wymaga orzecznika; samo osoba, która staje się jest niekompletne. Potrzebny jawny argument wyniku, nie fikcyjna rola subject. |
| neru | spać | ichidan | subject, location | istnieje | 4 | brak w zakresie | P+Z | low | D | Cztery formy i trzy klasy są gotowe dla ośmiu osób oraz inu/tori. Zachować odczyt zwyczajowy/przyszły; ている wymaga osobnej interpretacji stanu. |
| nomu | pić | godan | object, location | zalecane | 0 | 4 mapy | P+Z | low | A | Picie ma naturalnego żywego wykonawcę i może nie mieć jawnego napoju; pozostawić object=drink. |
| nonbiri_suru | leniuchować | irregular | location | zalecane | 0 | 4 mapy | P | low | A | Lenistwo/odpoczynek osoby jest samodzielny; zachować obecne potoczne tłumaczenie, nie rozszerzać na przedmioty. |
| noru | jechać | godan | vehicle, location | do decyzji | 0 | decyzja przed mapami | P | medium | B | 乗る może oznaczać wsiadać, a 乗っている jechać/być na pokładzie. Obecne jadę/jechałem wymaga decyzji aspektowej przed uzgodnieniem. |
| nugu | zdejmować | godan | object, location | do decyzji | 0 | decyzja przed mapami | P | medium | B | 脱ぐ dotyczy odzieży; zdejmowanie torby zwykle wymaga innego czasownika. Sprawdzić bag i dopełnienie przed rolą podmiotu. |
| oboeru | zapamiętywać | ichidan | object | do decyzji | 0 | decyzja przed mapami | P | medium | B | Zapamiętuje wymaga treści lub kontekstu. object=* zbyt szerokie dla części znaczeń; 覚えている bywa pamięta, nie właśnie zapamiętuje. |
| ochiru | upadać | ichidan | subject, location | istnieje | 0 | decyzja przed mapami | dokładna lista w JSON (17) | medium | B | 落ちる może oznaczać spadać, a nie zawsze upadać. Obecne drink/media dopuszczają np. kawę i muzykę; zakres podmiotów wymaga przeglądu. |
| okiru | budzić się | ichidan | subject, location | istnieje | 0 | decyzja przed mapami | P+Z | medium | B | Znaczenie budzić się jest poprawne dla istot żywych; istniejące person dopuszcza hitori. Wdrożenie tłumaczeń odblokuje też problematyczne ilościowe użycie 一人. |
| okoru | rozgniewać się | godan | target, location | zalecane | 0 | 4 mapy | P | low | A | 怒る w wybranym znaczeniu emocji osoby jest samodzielne. Nie rozszerzać na homofoniczne 起こる ani bezpośrednio na karcenie kogoś. |
| omoidasu | przypominać sobie | godan | object | do decyzji | 0 | decyzja przed mapami | P | medium | B | Obiekt pamięci zwykle potrzebny w przydawce; wildcard wymaga kontroli. Passive jestem wspominany zmienia uczestnika. |
| omou | myśleć | godan | location | zalecane | 0 | 4 mapy | P | low | A | Myśli/pomyślał można użyć absolutnie. Zachować reporting i istniejący wybór aspektu; nie dodawać posiadania opinii o dowolnym przedmiocie. |
| oshieru | uczyć | ichidan | object, target, location | do decyzji | 0 | decyzja przed mapami | P | medium | B | Uczyć kogoś czegoś i informować to różne ramy. object=* może dawać uczę pieniędzy; subject nie rozwiązuje wymaganych argumentów. |
| osu | naciskać | godan | location | do decyzji | 0 | decyzja przed mapami | P | medium | B | Brak roli object mimo przechodniego naciskać/pchać. Dodać rolę dopiero po wskazaniu istniejących właściwych rzeczowników; nie zastępować jej location. |
| owaru | kończyć się | godan | subject, location | istnieje | 0 | decyzja przed mapami | shigoto, meal, yotei | medium | B | Praca i posiłek się kończą; yotei=plan może wymagać skończyło się wykonywanie planu. Wspólna klasa masculine_inanimate obejmie meal i yotei, więc sam brak klasy nie odseparuje znaczeń. |
| oyogu | pływać | godan | location | zalecane | 0 | 4 mapy | P+pies | low | A | Ludzie i pies mogą pływać. Nie dopuszczać ogólnego ptaka, bo nie wszystkie ptaki pływają, ani łodzi, która wymaga innego japońskiego orzeczenia. |
| renshuusuru | ćwiczyć | irregular | object, location | zalecane | 0 | 4 mapy | P | low | A | Ćwiczy w znaczeniu doskonalenia umiejętności jest samodzielne. Object=music/song zostaje bez zmian i wymaga osobnej oceny idiomatyczności ćwiczyć muzykę. |
| sageru | opuszczać | ichidan | object, location | do decyzji | 0 | decyzja przed mapami | P | medium | B | 下げる oznacza obniżać/opuszczać przedmiot, nie opuszczać miejsce. Potrzebne dopełnienie i kontrola wieloznacznego polskiego tłumaczenia. |
| sawaru | dotykać | godan | target, location | do decyzji | 0 | decyzja przed mapami | P | medium | B | Dotykać czegoś, a nie komuś; target particle に nie wyznacza polskiego przypadka. concrete obejmuje nieoczywiste media, wymaga przeglądu. |
| sentakusuru | prać | irregular | object, location | zalecane | 0 | 4 mapy | P | low | A | Prać można bez jawnego ubrania; object=clothes pozostaje poprawnym zakresem. Nie dopuszczać przypadkowych rzeczy jako wykonawców. |
| shimaru | zamykać się | godan | subject, location | istnieje | 0 | 4 mapy | bag, box | low | A | Nieprzechodnie zamykanie torby/pudełka; istniejąca precyzyjna rola wystarcza. Dodać tylko feminine/neuter w czterech formach. |
| shimeru | zamykać | ichidan | object, location | do decyzji | 0 | decyzja przed mapami | P | medium | B | Zamyka coś, odmiennie od shimaru. W przydawce podmiotowej potrzebne dopełnienie lub zatwierdzony kontekst. |
| shinu | umrzeć | godan | subject, location | istnieje | 0 | decyzja przed mapami | P+Z | medium | B | Istoty żywe są poprawnymi podmiotami, ale person zawiera hitori. Sprawdzić też różnicę umrze/umiera w plain nonpast i stan 死んでいる. |
| shiru | dowiedzieć się | godan | object, location | do decyzji | 0 | decyzja przed mapami | P | medium | B | 知らない zwykle znaczy nie wie/nie zna, nie mechanicznie nie dowiaduje się. 知っている wyraża wiedzę. Potrzebna decyzja o znaczeniu i rekcji, zanim powstaną uzgodnione przeczenia. |
| soujisuru | sprzątać | irregular | object, location | zalecane | 0 | 4 mapy | P | low | A | Sprzątanie jest samodzielną czynnością osoby; nie zmieniać object ani location. Dodatkowe dane nie naprawiają wszystkich obecnych dopełnień thing. |
| sugosu | spędzać | godan | object, companion, location | do decyzji | 0 | decyzja przed mapami | P | medium | B | Spędzać wymaga czasu, tu jikan. Nie tworzyć przydawki osoba, która spędza bez jawnego dopełnienia. |
| suru | robić | irregular | object, location | do decyzji | 0 | decyzja przed mapami | P | medium | B | Ogólne robić wymaga treści. Obecne robię obietnicę i robię sprawę do załatwienia są kolokacyjnie podejrzane; nie traktować całej listy object jako A. |
| susumu | posuwać się naprzód | godan | destination, location | do decyzji | 0 | decyzja przed mapami | P | medium | B | Może opisywać ruch osoby albo postęp planu/pracy, ale te znaczenia mają różne naturalne polskie realizacje. Wariant osobowy wymaga akceptacji stylistycznej. |
| suu | wciągać | godan | location | do decyzji | 0 | decyzja przed mapami | P | medium | B | Base wciągać, formy palę i potential mogę wciągać są niespójne. Dla palić tytoń potrzebny kontekst タバコ; nie wybierać znaczenia automatycznie. |
| suwaru | siedzieć | godan | location | do decyzji | 0 | decyzja przed mapami | P+Z | medium | B | 座る to siadać, 座っている to siedzieć. Teraźniejsze siedzę nie odpowiada neutralnie temu samemu aspektowi co usiadłem; decyzja przed C2. |
| taberu | jeść | ichidan | object, location | zalecane | 0 | 4 mapy | P+Z | low | A | Jeść można bez jawnego jedzenia; żywy podmiot i object=food są rozdzielnymi rolami. Nie dopuszczać żywności jako wykonawcy. |
| tanoshimu | cieszyć się | godan | object, location | do decyzji | 0 | decyzja przed mapami | P | medium | B | 楽しむ to czerpać przyjemność z czegoś. Samo cieszy się może oznaczać 喜ぶ; object=* i polska realizacja wymagają doprecyzowania. |
| tateru | budować | ichidan | object, location | do decyzji | 0 | decyzja przed mapami | P | medium | B | Buduje bez dopełnienia jest możliwe kontekstowo; dla jednoznacznego materiału dydaktycznego wskazać home/school/taiikukan i ramę podmiot+obiekt. |
| tatsu | stać | godan | subject, location | istnieje | 0 | decyzja przed mapami | P+Z | medium | B | 立つ to stanąć/wstać, 立っている to stać. Obecne stoję/stałem oraz thing nie są bezpieczną podstawą masowego uzgodnienia. |
| teishutsusuru | składać | irregular | object, target | do decyzji | 0 | decyzja przed mapami | P | medium | B | 提出する to przedkładać dokument. book/note/keikaku i teacher/school potrzebują kontroli kolokacji; składa bez dokumentu wieloznaczne. |
| tojiru | zamykać | ichidan | object, location | do decyzji | 0 | decyzja przed mapami | P | medium | B | Zamyka książkę/pudełko, może też występować nieprzechodnio. Obecny wpis traktować jako przechodni; nie mieszać z shimaru. |
| tomaru | zatrzymywać się | godan | target, location | do decyzji | 0 | decyzja przed mapami | friend, mother, sister, teacher, roujin, hito, programmer, madogiwazoku, car, motorcycle, fune | medium | B | Zapisane 止まる oznacza zatrzymanie ruchu, nie nocleg 泊まる. Podmiotem mogą być ludzie i pojazdy; zatwierdzić osobno zakres, a target=place ocenić jako miejsce zatrzymania. |
| tooru | przechodzić przez | godan | route | do decyzji | 0 | decyzja przed mapami | P+Z | medium | B | 通る przechodzi przez dane miejsce; obecna rola route jest właściwa. Bez trasy polskie przechodzi może być niejednoznaczne. |
| torihazusu | demontować | godan | object, location | do decyzji | 0 | decyzja przed mapami | P | medium | B | Demontować coś lub zdejmować element; vehicle/thing obejmuje rzeczy, których zwykle się nie demontuje. Wymaga przedmiotu i dokładniejszej listy. |
| toru | brać | godan | object, location | do decyzji | 0 | decyzja przed mapami | P | medium | B | Brać jest przechodnie i wieloznaczne. abstract/animal/thing wymagają kontroli kontekstu; nie dodawać bierze bez jawnego obiektu. |
| tsukareru | być zmęczonym | ichidan | subject, location | istnieje | 0 | decyzja przed mapami | P+Z | medium | B | 疲れる opisuje męczenie się/zmęczenie, stan jest zwykle 疲れている. Obecne jestem zmęczony i potential/imperative wymagają oceny, a person zawiera hitori. |
| tsukau | używać | godan | object, location | do decyzji | 0 | decyzja przed mapami | P | medium | B | Używać wymaga czegoś; wildcard object obejmuje także abstrakty niepasujące do wybranego znaczenia. Zachować genitive do czasu osobnego przeglądu. |
| tsukeru | włączać | ichidan | object, location | do decyzji | 0 | decyzja przed mapami | P | medium | B | Dla television włączać jest naturalne, ale bez obiektu niejednoznaczne. Nie rozszerzać na inne znaczenia 付ける automatycznie. |
| tsukuru | robić | godan | object, location | do decyzji | 0 | decyzja przed mapami | P | medium | B | 作る oznacza wytwarzać/przygotowywać; object=* dopuszcza osoby/dni. Potrzebna selekcja produktu i wybór robić/tworzyć przed subject. |
| tsuzukeru | kontynuować | ichidan | object, location | do decyzji | 0 | decyzja przed mapami | P | medium | B | Kontynuować wymaga treści; music/song to raczej kontynuować granie/śpiewanie. Potrzebne dopełnienie, nie automatyczne poszerzanie podmiotów. |
| ugoku | ruszać się | godan | subject, location | istnieje | 0 | decyzja przed mapami | friend, mother, sister, teacher, roujin, hito, programmer, madogiwazoku, inu, tori, car, motorcycle, fune | medium | B | Ruch osoby, zwierzęcia, pojazdu i rzeczy możliwy, lecz thing obejmuje statyczne przedmioty. Rozstrzygnąć ruch samoczynny i bierne poruszenie, hitori oraz kontekst. |
| ukeru | odbierać | ichidan | object, location | do decyzji | 0 | decyzja przed mapami | P | medium | B | 受ける z shigoto zwykle przyjąć pracę/zlecenie, nie odebrać pracę w sensie technicznym. Zatwierdzić znaczenie i rekcję przed rozszerzeniem. |
| undousuru | ćwiczyć fizycznie | irregular | location | zalecane | 0 | 4 mapy | P | low | A | Samodzielna aktywność fizyczna osoby; bez dodawania narzędzi i bez utożsamienia z ćwiczeniem utworu. |
| usowotsuku | kłamać | godan | target, location | zalecane | 0 | 4 mapy | P | low | A | Kłamać można bez jawnego adresata; うそをつく jest całym zapisanym leksemem. Nie tworzyć drugiego slotu dla うそ. |
| utau | śpiewać | godan | object, location | zalecane | 0 | 4 mapy | P | low | A | Śpiew osoby jest samodzielny. Ptaki zwykle 鳴く/さえずる; nie dodawać ich do A. Object=media odrębnie wymaga wykluczenia np. głosu. |
| wakaru | rozumieć | godan | subject, location | istnieje | 0 | decyzja przed mapami | brak bezpiecznych obecnie | high | C | Obecny subject oznacza rozumianą treść, nie osobę rozumiejącą. Uzgodnienie do niego dałoby książka rozumie. Potrzebna rama doświadczającego albo inny polski predykat, bez zmiany znaczenia roli. |
| warau | śmiać się | godan | object, location | zalecane | 0 | 4 mapy | P | low | A | Śmiech osoby może być samodzielny. Zachować z_genitive dla wyśmiewanej osoby/zwierzęcia; podmiot nie jest tym samym argumentem co object. |
| wasureru | zapominać | ichidan | object, location | do decyzji | 0 | decyzja przed mapami | P | medium | B | Zapomina może być samodzielne, ale object=* i warianty dopełniacz/biernik/o+miejscownik zależą od znaczenia. Nie uznawać genitive automatycznie za błąd. |
| yomu | czytać | godan | object, location | zalecane | 0 | 4 mapy | P | low | A | Czytanie ma naturalne użycie bez jawnego tekstu. Precyzyjna lista ludzi, zachować object=text; nie dodawać zwierząt ani rzeczy. |
| ageru_give | dawać komuś | ichidan | object, target, location | do decyzji | 0 | decyzja przed mapami | P | medium | B | Dawanie od nadawcy do odbiorcy; potrzebny przedmiot i perspektywa あげる. Zapis komuś może dublować jawny target. |
| kaesu | oddawać, zwracać | godan | object, target, location | do decyzji | 0 | decyzja przed mapami | P | medium | B | Oddaje rzecz komuś; bez obiektu lub adresata jest kontekstowe. Nie łączyć z kaeru wracać. |
| kasu | pożyczać komuś | godan | object, target, location | do decyzji | 0 | decyzja przed mapami | P | medium | B | Dający pożyczkę, odmiennie od kariru. Rozstrzygnąć wstawiony tekst komuś i jawnego adresata przed subject. |
| kureru | dawać mi, nam | ichidan | object, target, location | do decyzji | 0 | decyzja przed mapami | P | medium | B | Perspektywa beneficjenta mi/nam wymaga wyboru. Rozkaz くれ jest poprawnym wyjątkiem; nie zmieniać na mechaniczne くれろ. |
| morau | otrzymywać | godan | object, target, location | do decyzji | 0 | decyzja przed mapami | P | medium | B | Otrzymuje coś od kogoś; samodzielna przydawka bez rzeczy jest niedookreślona. Nie kopiować kierunku target z czasowników dawania. |
| odoroku | być zaskoczonym | godan | reaction_target, location | do decyzji | 0 | decyzja przed mapami | P | medium | B | 驚く jest reakcją, stan bycia zaskoczonym wymaga kontekstu. Obecne jestem/byłem zaskoczony i causative zaskakiwać kogoś mają różną osobę/postać. |
| damaru | milczeć | godan | subject, location | istnieje | 0 | decyzja przed mapami | P | medium | B | 黙る to zamilknąć, 黙っている to milczeć. Obecne person animal obejmuje też hitori i ptaka; decyzja aspektowa przed agreement. |
| watasu | podawać, przekazywać | godan | object, target, location | do decyzji | 0 | decyzja przed mapami | P | medium | B | Przekazuje coś komuś. Wildcard-like szeroki object obejmuje abstrakty; podaję obietnicę nie jest neutralnym odpowiednikiem. |
| sukuu | ratować | godan | object, location | do decyzji | 0 | decyzja przed mapami | P | medium | B | Ratować można absolutnie, ale wybór 救う oraz object=inochi wymaga spójności ratować życie versus ratować osobę. Zachować jako kandydat do późniejszej weryfikacji. |
| shinjiru | wierzyć | ichidan | object, location | zalecane | 0 | 4 mapy | P | low | A | Wierzy może opisywać osobę bez jawnego obiektu wiary. Zachować w_accusative; wiara w osobę i ufanie osobie nie są automatycznie tą samą rekcją. |
| sumu | mieszkać | godan | target | do decyzji | 0 | decyzja przed mapami | P | medium | B | 住む może oznaczać zamieszkać, a 住んでいる stan mieszkania. Sama przydawka mieszka bez miejsca wymaga kontekstu; nie dodawać automatycznie subject. |

## Kandydaci tłumaczeń czterech form

Każdy tekst jest jawną propozycją. Tabele B/C nie są dopuszczeniem do wdrożenia. Klas nie należy używać jako filtrów znaczenia rzeczowników. Wartości A znajdują się również w dokładnych fragmentach XML.

### abiru (B)

Samodzielne あびる nie nazywa prysznica; ustalić, czy pomijany シャワー jest uzasadniony w tym quizie. Negacja wymaga prysznica.

Zatwierdzić znaczenie/argumenty opisane w uwadze. Wariant 1: zachować wykluczenie z prostych przydawek. Wariant 2: zatwierdzić podane tłumaczenia i dokładne podmioty, po kontroli pełnego zdania.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | bierze prysznic | nie bierze prysznica | wziął prysznic | nie wziął prysznica |
| żeńska | bierze prysznic | nie bierze prysznica | wzięła prysznic | nie wzięła prysznica |

### ageru (B)

Znaczenie 上げる, nie dawanie. Bez przedmiotu podnoszenia przydawka jest niedookreślona; lista object dopuszcza m.in. muzykę i abstrakcyjne nośniki.

Zatwierdzić znaczenie/argumenty opisane w uwadze. Wariant 1: zachować wykluczenie z prostych przydawek. Wariant 2: zatwierdzić podane tłumaczenia i dokładne podmioty, po kontroli pełnego zdania.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | podnosi | nie podnosi | podniósł | nie podniósł |
| żeńska | podnosi | nie podnosi | podniosła | nie podniosła |

### ajiwau (B)

Potrzebny przedmiot doświadczenia; instrumental_object jest zgodny z polskim delektować się czymś. Passive jest smakowane zmienia perspektywę i znaczenie.

Zatwierdzić znaczenie/argumenty opisane w uwadze. Wariant 1: zachować wykluczenie z prostych przydawek. Wariant 2: zatwierdzić podane tłumaczenia i dokładne podmioty, po kontroli pełnego zdania.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | delektuje się | nie delektuje się | delektował się | nie delektował się |
| żeńska | delektuje się | nie delektuje się | delektowała się | nie delektowała się |

### akeru (B)

Otwiera coś, odmiennie od aku. Zachować bag/box; dla podmiotowej przydawki potrzebne jawne dopełnienie albo zatwierdzony kontekst.

Zatwierdzić znaczenie/argumenty opisane w uwadze. Wariant 1: zachować wykluczenie z prostych przydawek. Wariant 2: zatwierdzić podane tłumaczenia i dokładne podmioty, po kontroli pełnego zdania.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | otwiera | nie otwiera | otworzył | nie otworzył |
| żeńska | otwiera | nie otwiera | otworzyła | nie otworzyła |

### aku (D)

Cztery formy i klasy feminine/neuter już poprawnie zapisane dla bag/box. Nie rozszerzać na osoby ani drzwi bez obsługi liczby mnogiej.

Zachować obecne cztery formy i podmioty; brak potrzeby nowych wpisów w priorytetowym zakresie.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| żeńska | otwiera się | nie otwiera się | otworzyła się | nie otworzyła się |
| nijaka | otwiera się | nie otwiera się | otworzyło się | nie otworzyło się |

### arau (B)

Myje kogoś lub coś, a nie myje się. Bez dopełnienia grozi zmianą interpretacji; nie dodawać się automatycznie.

Zatwierdzić znaczenie/argumenty opisane w uwadze. Wariant 1: zachować wykluczenie z prostych przydawek. Wariant 2: zatwierdzić podane tłumaczenia i dokładne podmioty, po kontroli pełnego zdania.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | myje | nie myje | umył | nie umył |
| żeńska | myje | nie myje | umyła | nie umyła |

### aru_possessive (C)

Subject oznacza rzecz posiadaną, nie właściciela. Nie dodawać tych kandydatów jako agreement: pudełko ma byłoby odwróceniem argumentów. Ten wpis nie ma cechy existential.

Nie dodawać B2 do obecnej roli. Użyć lub opracować konstrukcję wskazaną w uwadze, z osobną weryfikacją argumentów.

Nie proponuję map do XML. Osobowe kandydaty do ewentualnej innej ramy: ma; miał / miała / miało. Formy dyskusyjne, nie przypisywać do obecnego subject; przeczenia i argumenty wymagają konstrukcji.

### aru_existential (C)

Istnienie z government:existential_subject i katalogiem. Negacja nie ma/nie było wymaga dopełniacza, nie mianownikowego podmiotu i zwykłego B2.

Nie dodawać B2 do obecnej roli. Użyć lub opracować konstrukcję wskazaną w uwadze, z osobną weryfikacją argumentów.

Nie proponuję map do XML. Osobowe kandydaty do ewentualnej innej ramy: jest; był / była / było. Formy dyskusyjne, nie przypisywać do obecnego subject; przeczenia i argumenty wymagają konstrukcji.

### aruku (A)

Samodzielny ruch pieszy ma naturalnego wykonawcę; do C2 tylko ludzie, bo pies idzie pieszo jest stylistycznie nienaturalne.

Przyjąć wyłącznie wymienione propozycje; inne formy pozostają poza C2-A.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | idzie pieszo | nie idzie pieszo | szedł pieszo | nie szedł pieszo |
| żeńska | idzie pieszo | nie idzie pieszo | szła pieszo | nie szła pieszo |

### asobu (A)

Zabawa ludzi i zwierząt może wystąpić bez wskazania towarzysza. Zachować istniejącą rekcję towarzysza.

Przyjąć wyłącznie wymienione propozycje; inne formy pozostają poza C2-A.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | bawi się | nie bawi się | bawił się | nie bawił się |
| męskożywotna | bawi się | nie bawi się | bawił się | nie bawił się |
| żeńska | bawi się | nie bawi się | bawiła się | nie bawiła się |

### au (B)

Przy liczbie pojedynczej potrzebny partner spotkania lub kontekst. Nie utożsamiać samotnego spotyka się z pełną konstrukcją wzajemną.

Zatwierdzić znaczenie/argumenty opisane w uwadze. Wariant 1: zachować wykluczenie z prostych przydawek. Wariant 2: zatwierdzić podane tłumaczenia i dokładne podmioty, po kontroli pełnego zdania.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | spotyka się | nie spotyka się | spotkał się | nie spotkał się |
| żeńska | spotyka się | nie spotyka się | spotkała się | nie spotkała się |

### ayamaru (A)

Osoba może przepraszać bez jawnego adresata; target pozostaje niezależną rolą, bez poszerzania jej obecnej listy.

Przyjąć wyłącznie wymienione propozycje; inne formy pozostają poza C2-A.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | przeprasza | nie przeprasza | przeprosił | nie przeprosił |
| żeńska | przeprasza | nie przeprasza | przeprosiła | nie przeprosiła |

### chigau (B)

Wymaga rozstrzygnięcia różnić się od czegoś versus być innym/błędnym; brak wspólnego kontekstu porównania. ちがえる nie oznacza zwykle zdolności różnienia się.

Zatwierdzić znaczenie/argumenty opisane w uwadze. Wariant 1: zachować wykluczenie z prostych przydawek. Wariant 2: zatwierdzić podane tłumaczenia i dokładne podmioty, po kontroli pełnego zdania.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskonieżywotna | różni się | nie różni się | różnił się | nie różnił się |
| żeńska | różni się | nie różni się | różniła się | nie różniła się |

### dasu (B)

Bez wyjmowanego przedmiotu zdanie niepełne; abstract/media w object wymagają przeglądu wybranego znaczenia 出す.

Zatwierdzić znaczenie/argumenty opisane w uwadze. Wariant 1: zachować wykluczenie z prostych przydawek. Wariant 2: zatwierdzić podane tłumaczenia i dokładne podmioty, po kontroli pełnego zdania.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | wyjmuje | nie wyjmuje | wyjął | nie wyjął |
| żeńska | wyjmuje | nie wyjmuje | wyjęła | nie wyjęła |

### dekiru (C)

Modalne móc wymaga dopełnienia bezokolicznikowego. Istnieje konstrukcja ことができる; nie potrzeba nowego DSL, ale zwykła podmiotowa przydawka sama nie wystarcza.

Nie dodawać B2 do obecnej roli. Użyć lub opracować konstrukcję wskazaną w uwadze, z osobną weryfikacją argumentów.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | może | nie może | mógł | nie mógł |
| żeńska | może | nie może | mogła | nie mogła |

### deru (A)

Ludzie i zwierzęta mogą wychodzić bez jawnego miejsca wyjścia. Zachować route; nie rozszerzać na publikacje i pojazdy w tym znaczeniu.

Przyjąć wyłącznie wymienione propozycje; inne formy pozostają poza C2-A.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | wychodzi | nie wychodzi | wyszedł | nie wyszedł |
| męskożywotna | wychodzi | nie wychodzi | wyszedł | nie wyszedł |
| żeńska | wychodzi | nie wychodzi | wyszła | nie wyszła |

### fuku (B)

Meteorologiczne 吹く wymaga wiatru jako nazwanego podmiotu, którego brak w rzeczownikach. Obecna bezosobowa forma wiało jest poprawna w konstrukcji pogodowej.

Zatwierdzić znaczenie/argumenty opisane w uwadze. Wariant 1: zachować wykluczenie z prostych przydawek. Wariant 2: zatwierdzić podane tłumaczenia i dokładne podmioty, po kontroli pełnego zdania.

Nie proponuję map do XML. Osobowe kandydaty do ewentualnej innej ramy: wieje; wiał / wiała / wiało. Formy dyskusyjne, nie przypisywać do obecnego subject; przeczenia i argumenty wymagają konstrukcji.

### furu (B)

Brak rzeczowników deszcz/śnieg. Nie uzgadniać z dowolną rzeczą; potencjalność pogody nie jest automatycznie zdolnością działania.

Zatwierdzić znaczenie/argumenty opisane w uwadze. Wariant 1: zachować wykluczenie z prostych przydawek. Wariant 2: zatwierdzić podane tłumaczenia i dokładne podmioty, po kontroli pełnego zdania.

Nie proponuję map do XML. Osobowe kandydaty do ewentualnej innej ramy: pada; padał / padała / padało. Formy dyskusyjne, nie przypisywać do obecnego subject; przeczenia i argumenty wymagają konstrukcji.

### hairu (A)

Wchodzenie ludzi i zwierząt jest naturalne bez jawnego celu w krótkiej przydawce. Zachować target=place.

Przyjąć wyłącznie wymienione propozycje; inne formy pozostają poza C2-A.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | wchodzi | nie wchodzi | wszedł | nie wszedł |
| męskożywotna | wchodzi | nie wchodzi | wszedł | nie wszedł |
| żeńska | wchodzi | nie wchodzi | weszła | nie weszła |

### hajimeru (B)

Przechodnie zaczynać coś; nie zamieniać na zaczyna się. Subject dopiero z treścią rozpoczynanej czynności lub kontekstem.

Zatwierdzić znaczenie/argumenty opisane w uwadze. Wariant 1: zachować wykluczenie z prostych przydawek. Wariant 2: zatwierdzić podane tłumaczenia i dokładne podmioty, po kontroli pełnego zdania.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | zaczyna | nie zaczyna | zaczął | nie zaczął |
| żeńska | zaczyna | nie zaczyna | zaczęła | nie zaczęła |

### hanashiau (C)

Obecne rozmawiamy ze sobą jest mnogie. Potrzebny partner przy liczbie pojedynczej, np. rozmawia z mamą; istniejąca rola companion może go reprezentować po sprawdzeniu rekcji.

Nie dodawać B2 do obecnej roli. Użyć lub opracować konstrukcję wskazaną w uwadze, z osobną weryfikacją argumentów.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | rozmawia z kimś | nie rozmawia z kimś | rozmawiał z kimś | nie rozmawiał z kimś |
| żeńska | rozmawia z kimś | nie rozmawia z kimś | rozmawiała z kimś | nie rozmawiała z kimś |

### hanasu (A)

Rozmawia może opisywać osobę bez jawnego partnera. Nie rozszerzać na zwierzęta ani zastępować tego automatycznie znaczeniem opowiadać o czymś.

Przyjąć wyłącznie wymienione propozycje; inne formy pozostają poza C2-A.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | rozmawia | nie rozmawia | rozmawiał | nie rozmawiał |
| żeńska | rozmawia | nie rozmawia | rozmawiała | nie rozmawiała |

### harau (A)

Samodzielne płaci/zapłacił jest naturalne; zachować object=okane. Nie zmieniać znaczenia na usuwać/strzepywać.

Przyjąć wyłącznie wymienione propozycje; inne formy pozostają poza C2-A.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | płaci | nie płaci | zapłacił | nie zapłacił |
| żeńska | płaci | nie płaci | zapłaciła | nie zapłaciła |

### hareru (B)

Aktualne formy są pogodowe i bezosobowe; brak nieba jako rzeczownika. Mieszanie przejaśnia się/rozpogodziło się wymaga decyzji leksykalnej.

Zatwierdzić znaczenie/argumenty opisane w uwadze. Wariant 1: zachować wykluczenie z prostych przydawek. Wariant 2: zatwierdzić podane tłumaczenia i dokładne podmioty, po kontroli pełnego zdania.

Nie proponuję map do XML. Osobowe kandydaty do ewentualnej innej ramy: przejaśnia się; przejaśnił się / przejaśniła się / przejaśniło się. Formy dyskusyjne, nie przypisywać do obecnego subject; przeczenia i argumenty wymagają konstrukcji.

### hashiru (A)

Bieg ludzi i zwierząt jest samodzielną czynnością. Pojazdy i programy pominięte, bo wymagałyby innego polskiego znaczenia.

Przyjąć wyłącznie wymienione propozycje; inne formy pozostają poza C2-A.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | biegnie | nie biegnie | biegł | nie biegł |
| męskożywotna | biegnie | nie biegnie | biegł | nie biegł |
| żeńska | biegnie | nie biegnie | biegła | nie biegła |

### hataraku (D)

Obecna dokładna lista ośmiu osób oraz dwie klasy w czterech formach wystarczają. Inne formy nie otrzymują B2 w C1.

Zachować obecne cztery formy i podmioty; brak potrzeby nowych wpisów w priorytetowym zakresie.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | pracuje | nie pracuje | pracował | nie pracował |
| żeńska | pracuje | nie pracuje | pracowała | nie pracowała |

### hiraku (B)

開く ma zastosowania przechodnie i nieprzechodnie. Obecny wpis jest przechodni; book/school to różne ramy semantyczne, nie dodawać samoczynnie otwiera się.

Zatwierdzić znaczenie/argumenty opisane w uwadze. Wariant 1: zachować wykluczenie z prostych przydawek. Wariant 2: zatwierdzić podane tłumaczenia i dokładne podmioty, po kontroli pełnego zdania.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | otwiera | nie otwiera | otworzył | nie otworzył |
| żeńska | otwiera | nie otwiera | otworzyła | nie otworzyła |

### iku (A)

Idzie/poszedł z żywym wykonawcą jest naturalne. いって/いった są wyjątkami; ている oznacza często stan po odejściu, nie po prostu idzie.

Przyjąć wyłącznie wymienione propozycje; inne formy pozostają poza C2-A.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | idzie | nie idzie | poszedł | nie poszedł |
| męskożywotna | idzie | nie idzie | poszedł | nie poszedł |
| żeńska | idzie | nie idzie | poszła | nie poszła |

### ireru (B)

Potrzebny wkładany przedmiot, często też cel. accepts i nouns są alternatywami OR; okane dopisuje pieniądze, nie zawęża kategorii.

Zatwierdzić znaczenie/argumenty opisane w uwadze. Wariant 1: zachować wykluczenie z prostych przydawek. Wariant 2: zatwierdzić podane tłumaczenia i dokładne podmioty, po kontroli pełnego zdania.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | wkłada | nie wkłada | włożył | nie włożył |
| żeńska | wkłada | nie wkłada | włożyła | nie włożyła |

### iru (C)

Zachować katalog existential i governed noun. Nie kopiować osobowych form jestem/nie ma mnie do przydawek; potrzebna osobna realizacja negacji i miejsca.

Nie dodawać B2 do obecnej roli. Użyć lub opracować konstrukcję wskazaną w uwadze, z osobną weryfikacją argumentów.

Nie proponuję map do XML. Osobowe kandydaty do ewentualnej innej ramy: jest; był / była / było. Formy dyskusyjne, nie przypisywać do obecnego subject; przeczenia i argumenty wymagają konstrukcji.

### isogu (A)

Samodzielna czynność osoby; zachować zaakceptowaną pisownię śpieszyć, bez kosmetycznej zmiany na spieszyć.

Przyjąć wyłącznie wymienione propozycje; inne formy pozostają poza C2-A.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | śpieszy się | nie śpieszy się | śpieszył się | nie śpieszył się |
| żeńska | śpieszy się | nie śpieszy się | śpieszyła się | nie śpieszyła się |

### iu (B)

Obecny wpis łączy mówi i powiedzieć; w przydawce powiedział zwykle wymaga treści. Istniejące reporting trzeba zachować.

Zatwierdzić znaczenie/argumenty opisane w uwadze. Wariant 1: zachować wykluczenie z prostych przydawek. Wariant 2: zatwierdzić podane tłumaczenia i dokładne podmioty, po kontroli pełnego zdania.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | mówi | nie mówi | powiedział | nie powiedział |
| żeńska | mówi | nie mówi | powiedziała | nie powiedziała |

### kaeru (A)

Powrót żywego wykonawcy można opisać bez jawnego celu. Nie zmieniać na ogólne zmieniać, które jest innym czasownikiem.

Przyjąć wyłącznie wymienione propozycje; inne formy pozostają poza C2-A.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | wraca | nie wraca | wrócił | nie wrócił |
| męskożywotna | wraca | nie wraca | wrócił | nie wrócił |
| żeńska | wraca | nie wraca | wróciła | nie wróciła |

### kaku (A)

Pisanie jest naturalne bez jawnego tekstu, np. osoba, która pisze. Zachować object=text i direct_object.

Przyjąć wyłącznie wymienione propozycje; inne formy pozostają poza C2-A.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | pisze | nie pisze | pisał | nie pisał |
| żeńska | pisze | nie pisze | pisała | nie pisała |

### kangaeru (A)

Zastanawia się jest samodzielne; przy dopełnieniu pozostaje nad_instrumental. Pojazd jako przedmiot namysłu nie oznacza podmiotu.

Przyjąć wyłącznie wymienione propozycje; inne formy pozostają poza C2-A.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | zastanawia się | nie zastanawia się | zastanawiał się | nie zastanawiał się |
| żeńska | zastanawia się | nie zastanawia się | zastanawiała się | nie zastanawiała się |

### kariru (B)

Kierunek pożyczki musi pozostać od dawcy. Tekst od kogoś plus jawny target może dublować argument; nie włączać bez sprawdzenia wzorca.

Zatwierdzić znaczenie/argumenty opisane w uwadze. Wariant 1: zachować wykluczenie z prostych przydawek. Wariant 2: zatwierdzić podane tłumaczenia i dokładne podmioty, po kontroli pełnego zdania.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | pożycza od kogoś | nie pożycza od kogoś | pożyczył od kogoś | nie pożyczył od kogoś |
| żeńska | pożycza od kogoś | nie pożycza od kogoś | pożyczyła od kogoś | nie pożyczyła od kogoś |

### kau (A)

Kupuje może być użyte absolutnie dla kupującej osoby; precyzyjny zakup wymaga object. Zachować istniejące role.

Przyjąć wyłącznie wymienione propozycje; inne formy pozostają poza C2-A.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | kupuje | nie kupuje | kupił | nie kupił |
| żeńska | kupuje | nie kupuje | kupiła | nie kupiła |

### kayou (B)

Polskie uczęszcza wymaga dokąd/na co. Obecne school/taiikukan są właściwymi kandydatami, lecz brak celu w przydawce wymaga kontekstu.

Zatwierdzić znaczenie/argumenty opisane w uwadze. Wariant 1: zachować wykluczenie z prostych przydawek. Wariant 2: zatwierdzić podane tłumaczenia i dokładne podmioty, po kontroli pełnego zdania.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | uczęszcza | nie uczęszcza | uczęszczał | nie uczęszczał |
| żeńska | uczęszcza | nie uczęszcza | uczęszczała | nie uczęszczała |

### keikosuru (B)

稽古する dotyczy ćwiczenia umiejętności/sztuki; trenuję muzykę/piosenkę jest niezgrabne. Rozstrzygnąć ćwiczyć a trenować przed rozszerzeniem.

Zatwierdzić znaczenie/argumenty opisane w uwadze. Wariant 1: zachować wykluczenie z prostych przydawek. Wariant 2: zatwierdzić podane tłumaczenia i dokładne podmioty, po kontroli pełnego zdania.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | trenuje | nie trenuje | trenował | nie trenował |
| żeńska | trenuje | nie trenuje | trenowała | nie trenowała |

### kesu (B)

Wyłącza telewizję, ale usuwa mail/notatkę. Jeden polski leksem nie realizuje bezpiecznie wszystkich obecnych object.

Zatwierdzić znaczenie/argumenty opisane w uwadze. Wariant 1: zachować wykluczenie z prostych przydawek. Wariant 2: zatwierdzić podane tłumaczenia i dokładne podmioty, po kontroli pełnego zdania.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | wyłącza | nie wyłącza | wyłączył | nie wyłączył |
| żeńska | wyłącza | nie wyłącza | wyłączyła | nie wyłączyła |

### kikokusuru (A)

帰国する zawiera powrót do własnego kraju; podmiot ludzki, argument celu zawarty w tłumaczeniu. Nie poszerzać na zwierzęta.

Przyjąć wyłącznie wymienione propozycje; inne formy pozostają poza C2-A.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | wraca do kraju | nie wraca do kraju | wrócił do kraju | nie wrócił do kraju |
| żeńska | wraca do kraju | nie wraca do kraju | wróciła do kraju | nie wróciła do kraju |

### kiku (B)

Słuchać i pytać są różnymi ramami. Passive jestem pytany przełącza znaczenie względem słucham; abstract dopuszcza nieoczywiste przedmioty słuchania.

Zatwierdzić znaczenie/argumenty opisane w uwadze. Wariant 1: zachować wykluczenie z prostych przydawek. Wariant 2: zatwierdzić podane tłumaczenia i dokładne podmioty, po kontroli pełnego zdania.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | słucha | nie słucha | słuchał | nie słuchał |
| żeńska | słucha | nie słucha | słuchała | nie słuchała |

### kiru (B)

着る to zakładać ubranie, 着ている to nosić/mieć na sobie. Base nosić i potential mogę nosić wymagają wyrównania znaczenia; nie mieszać z 切る.

Zatwierdzić znaczenie/argumenty opisane w uwadze. Wariant 1: zachować wykluczenie z prostych przydawek. Wariant 2: zatwierdzić podane tłumaczenia i dokładne podmioty, po kontroli pełnego zdania.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | zakłada | nie zakłada | założył | nie założył |
| żeńska | zakłada | nie zakłada | założyła | nie założyła |

### kotaeru (A)

Odpowiada może wystąpić bez jawnego pytania. Existing target=abstract pozostaje osobną kwestią precyzji dopełnienia.

Przyjąć wyłącznie wymienione propozycje; inne formy pozostają poza C2-A.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | odpowiada | nie odpowiada | odpowiedział | nie odpowiedział |
| żeńska | odpowiada | nie odpowiada | odpowiedziała | nie odpowiedziała |

### kumoru (B)

Pogodowe bezosobowe zachmurzyło się nie ma obecnie właściwego rzeczownika. Zaproponowane osobowe formy wyłącznie dla przyszłego konkretnego podmiotu, nie do XML.

Zatwierdzić znaczenie/argumenty opisane w uwadze. Wariant 1: zachować wykluczenie z prostych przydawek. Wariant 2: zatwierdzić podane tłumaczenia i dokładne podmioty, po kontroli pełnego zdania.

Nie proponuję map do XML. Osobowe kandydaty do ewentualnej innej ramy: chmurzy się; zachmurzył się / zachmurzyła się / zachmurzyło się. Formy dyskusyjne, nie przypisywać do obecnego subject; przeczenia i argumenty wymagają konstrukcji.

### kuru (A)

Przychodzi żywa osoba/zwierzę. Jawnie uwzględnić nieregularne きた/こない; nie traktować 来ている jako zawsze czynności trwającej.

Przyjąć wyłącznie wymienione propozycje; inne formy pozostają poza C2-A.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | przychodzi | nie przychodzi | przyszedł | nie przyszedł |
| męskożywotna | przychodzi | nie przychodzi | przyszedł | nie przyszedł |
| żeńska | przychodzi | nie przychodzi | przyszła | nie przyszła |

### matsu (A)

Czekanie ludzi i zwierząt jest naturalne bez jawnego obiektu; na_accusative pozostaje dla dopełnienia.

Przyjąć wyłącznie wymienione propozycje; inne formy pozostają poza C2-A.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | czeka | nie czeka | czekał | nie czekał |
| męskożywotna | czeka | nie czeka | czekał | nie czekał |
| żeńska | czeka | nie czeka | czekała | nie czekała |

### mieru (B)

Uzgodnienie dotyczy także przymiotnika w teraźniejszości. concrete obejmuje media, np. głos/muzykę, więc potrzebna kontrola widzialności i precyzyjna lista.

Zatwierdzić znaczenie/argumenty opisane w uwadze. Wariant 1: zachować wykluczenie z prostych przydawek. Wariant 2: zatwierdzić podane tłumaczenia i dokładne podmioty, po kontroli pełnego zdania.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | jest widoczny | nie jest widoczny | był widoczny | nie był widoczny |
| męskożywotna | jest widoczny | nie jest widoczny | był widoczny | nie był widoczny |
| męskonieżywotna | jest widoczny | nie jest widoczny | był widoczny | nie był widoczny |
| żeńska | jest widoczna | nie jest widoczna | była widoczna | nie była widoczna |
| nijaka | jest widoczne | nie jest widoczne | było widoczne | nie było widoczne |

### migaku (B)

Szorować/polerować zależy od przedmiotu. Nie dodawać podmiotu bez dopełnienia i kontroli rzeczy dopuszczonych przez thing.

Zatwierdzić znaczenie/argumenty opisane w uwadze. Wariant 1: zachować wykluczenie z prostych przydawek. Wariant 2: zatwierdzić podane tłumaczenia i dokładne podmioty, po kontroli pełnego zdania.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | szoruje | nie szoruje | wyszorował | nie wyszorował |
| żeńska | szoruje | nie szoruje | wyszorowała | nie wyszorowała |

### miru (B)

Widzieć, patrzeć i oglądać nie są wymienne. Wildcard object dopuszcza np. jutro/smak; wymagana selekcja znaczenia przed bezpiecznym rozszerzeniem.

Zatwierdzić znaczenie/argumenty opisane w uwadze. Wariant 1: zachować wykluczenie z prostych przydawek. Wariant 2: zatwierdzić podane tłumaczenia i dokładne podmioty, po kontroli pełnego zdania.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | ogląda | nie ogląda | oglądał | nie oglądał |
| żeńska | ogląda | nie ogląda | oglądała | nie oglądała |

### mochiageru (B)

持ち上げる podnosi przedmiot; samodzielna przydawka wymaga kontekstu. Nie zakładać, że podnoszenie muzyki jest dosłowną czynnością.

Zatwierdzić znaczenie/argumenty opisane w uwadze. Wariant 1: zachować wykluczenie z prostych przydawek. Wariant 2: zatwierdzić podane tłumaczenia i dokładne podmioty, po kontroli pełnego zdania.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | podnosi | nie podnosi | podniósł | nie podniósł |
| żeńska | podnosi | nie podnosi | podniosła | nie podniosła |

### motsu (B)

持つ i 持っている rozróżniają zdarzenie/stan; object=abstract obejmuje posiadanie planu. Trzyma bez dopełnienia nie nadaje się do automatycznego A.

Zatwierdzić znaczenie/argumenty opisane w uwadze. Wariant 1: zachować wykluczenie z prostych przydawek. Wariant 2: zatwierdzić podane tłumaczenia i dokładne podmioty, po kontroli pełnego zdania.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | trzyma | nie trzyma | trzymał | nie trzymał |
| żeńska | trzyma | nie trzyma | trzymała | nie trzymała |

### motteiku (B)

Zabiera coś w kierunku od punktu odniesienia. Potrzebny przedmiot, zachować odmianę końcowego 行く i jego wyjątki.

Zatwierdzić znaczenie/argumenty opisane w uwadze. Wariant 1: zachować wykluczenie z prostych przydawek. Wariant 2: zatwierdzić podane tłumaczenia i dokładne podmioty, po kontroli pełnego zdania.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | zabiera | nie zabiera | zabrał | nie zabrał |
| żeńska | zabiera | nie zabiera | zabrała | nie zabrała |

### mottekuru (B)

Przynosi coś do punktu odniesienia. Zapis 持ってくる odmienia kana końcowego くる; to nie błąd kanji.

Zatwierdzić znaczenie/argumenty opisane w uwadze. Wariant 1: zachować wykluczenie z prostych przydawek. Wariant 2: zatwierdzić podane tłumaczenia i dokładne podmioty, po kontroli pełnego zdania.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | przynosi | nie przynosi | przyniósł | nie przyniósł |
| żeńska | przynosi | nie przynosi | przyniosła | nie przyniosła |

### naku (B)

泣く oznacza płakać, a nie neutralny głos ptaka/psa 鳴く. Obecne animal i hitori wymagają przeglądu, zanim translation odblokuje całą klasę.

Zatwierdzić znaczenie/argumenty opisane w uwadze. Wariant 1: zachować wykluczenie z prostych przydawek. Wariant 2: zatwierdzić podane tłumaczenia i dokładne podmioty, po kontroli pełnego zdania.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | płacze | nie płacze | płakał | nie płakał |
| żeńska | płacze | nie płacze | płakała | nie płakała |

### nakusu (B)

Zgubił bez przedmiotu wymaga kontekstu. Zachować rozróżnienie zgubić/przegrać/utracić i selekcję rzeczowników.

Zatwierdzić znaczenie/argumenty opisane w uwadze. Wariant 1: zachować wykluczenie z prostych przydawek. Wariant 2: zatwierdzić podane tłumaczenia i dokładne podmioty, po kontroli pełnego zdania.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | gubi | nie gubi | zgubił | nie zgubił |
| żeńska | gubi | nie gubi | zgubiła | nie zgubiła |

### nareru (B)

Przyzwyczaja się jest możliwe kontekstowo, lecz target=* i brak dopełnienia do czegoś wymagają weryfikacji polskiej rekcji.

Zatwierdzić znaczenie/argumenty opisane w uwadze. Wariant 1: zachować wykluczenie z prostych przydawek. Wariant 2: zatwierdzić podane tłumaczenia i dokładne podmioty, po kontroli pełnego zdania.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | przyzwyczaja się | nie przyzwyczaja się | przyzwyczaił się | nie przyzwyczaił się |
| żeńska | przyzwyczaja się | nie przyzwyczaja się | przyzwyczaiła się | nie przyzwyczaiła się |

### naru (C)

Stawać się wymaga orzecznika; samo osoba, która staje się jest niekompletne. Potrzebny jawny argument wyniku, nie fikcyjna rola subject.

Nie dodawać B2 do obecnej roli. Użyć lub opracować konstrukcję wskazaną w uwadze, z osobną weryfikacją argumentów.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | staje się | nie staje się | stał się | nie stał się |
| żeńska | staje się | nie staje się | stała się | nie stała się |

### neru (D)

Cztery formy i trzy klasy są gotowe dla ośmiu osób oraz inu/tori. Zachować odczyt zwyczajowy/przyszły; ている wymaga osobnej interpretacji stanu.

Zachować obecne cztery formy i podmioty; brak potrzeby nowych wpisów w priorytetowym zakresie.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | śpi | nie śpi | spał | nie spał |
| męskożywotna | śpi | nie śpi | spał | nie spał |
| żeńska | śpi | nie śpi | spała | nie spała |

### nomu (A)

Picie ma naturalnego żywego wykonawcę i może nie mieć jawnego napoju; pozostawić object=drink.

Przyjąć wyłącznie wymienione propozycje; inne formy pozostają poza C2-A.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | pije | nie pije | pił | nie pił |
| męskożywotna | pije | nie pije | pił | nie pił |
| żeńska | pije | nie pije | piła | nie piła |

### nonbiri_suru (A)

Lenistwo/odpoczynek osoby jest samodzielny; zachować obecne potoczne tłumaczenie, nie rozszerzać na przedmioty.

Przyjąć wyłącznie wymienione propozycje; inne formy pozostają poza C2-A.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | leniuchuje | nie leniuchuje | leniuchował | nie leniuchował |
| żeńska | leniuchuje | nie leniuchuje | leniuchowała | nie leniuchowała |

### noru (B)

乗る może oznaczać wsiadać, a 乗っている jechać/być na pokładzie. Obecne jadę/jechałem wymaga decyzji aspektowej przed uzgodnieniem.

Zatwierdzić znaczenie/argumenty opisane w uwadze. Wariant 1: zachować wykluczenie z prostych przydawek. Wariant 2: zatwierdzić podane tłumaczenia i dokładne podmioty, po kontroli pełnego zdania.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | jedzie | nie jedzie | jechał | nie jechał |
| żeńska | jedzie | nie jedzie | jechała | nie jechała |

### nugu (B)

脱ぐ dotyczy odzieży; zdejmowanie torby zwykle wymaga innego czasownika. Sprawdzić bag i dopełnienie przed rolą podmiotu.

Zatwierdzić znaczenie/argumenty opisane w uwadze. Wariant 1: zachować wykluczenie z prostych przydawek. Wariant 2: zatwierdzić podane tłumaczenia i dokładne podmioty, po kontroli pełnego zdania.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | zdejmuje | nie zdejmuje | zdjął | nie zdjął |
| żeńska | zdejmuje | nie zdejmuje | zdjęła | nie zdjęła |

### oboeru (B)

Zapamiętuje wymaga treści lub kontekstu. object=* zbyt szerokie dla części znaczeń; 覚えている bywa pamięta, nie właśnie zapamiętuje.

Zatwierdzić znaczenie/argumenty opisane w uwadze. Wariant 1: zachować wykluczenie z prostych przydawek. Wariant 2: zatwierdzić podane tłumaczenia i dokładne podmioty, po kontroli pełnego zdania.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | zapamiętuje | nie zapamiętuje | zapamiętał | nie zapamiętał |
| żeńska | zapamiętuje | nie zapamiętuje | zapamiętała | nie zapamiętała |

### ochiru (B)

落ちる może oznaczać spadać, a nie zawsze upadać. Obecne drink/media dopuszczają np. kawę i muzykę; zakres podmiotów wymaga przeglądu.

Zatwierdzić znaczenie/argumenty opisane w uwadze. Wariant 1: zachować wykluczenie z prostych przydawek. Wariant 2: zatwierdzić podane tłumaczenia i dokładne podmioty, po kontroli pełnego zdania.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | upada | nie upada | upadł | nie upadł |
| męskożywotna | upada | nie upada | upadł | nie upadł |
| męskonieżywotna | upada | nie upada | upadł | nie upadł |
| żeńska | upada | nie upada | upadła | nie upadła |
| nijaka | upada | nie upada | upadło | nie upadło |

### okiru (B)

Znaczenie budzić się jest poprawne dla istot żywych; istniejące person dopuszcza hitori. Wdrożenie tłumaczeń odblokuje też problematyczne ilościowe użycie 一人.

Zatwierdzić znaczenie/argumenty opisane w uwadze. Wariant 1: zachować wykluczenie z prostych przydawek. Wariant 2: zatwierdzić podane tłumaczenia i dokładne podmioty, po kontroli pełnego zdania.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | budzi się | nie budzi się | obudził się | nie obudził się |
| męskożywotna | budzi się | nie budzi się | obudził się | nie obudził się |
| żeńska | budzi się | nie budzi się | obudziła się | nie obudziła się |

### okoru (A)

怒る w wybranym znaczeniu emocji osoby jest samodzielne. Nie rozszerzać na homofoniczne 起こる ani bezpośrednio na karcenie kogoś.

Przyjąć wyłącznie wymienione propozycje; inne formy pozostają poza C2-A.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | złości się | nie złości się | zezłościł się | nie zezłościł się |
| żeńska | złości się | nie złości się | zezłościła się | nie zezłościła się |

### omoidasu (B)

Obiekt pamięci zwykle potrzebny w przydawce; wildcard wymaga kontroli. Passive jestem wspominany zmienia uczestnika.

Zatwierdzić znaczenie/argumenty opisane w uwadze. Wariant 1: zachować wykluczenie z prostych przydawek. Wariant 2: zatwierdzić podane tłumaczenia i dokładne podmioty, po kontroli pełnego zdania.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | przypomina sobie | nie przypomina sobie | przypomniał sobie | nie przypomniał sobie |
| żeńska | przypomina sobie | nie przypomina sobie | przypomniała sobie | nie przypomniała sobie |

### omou (A)

Myśli/pomyślał można użyć absolutnie. Zachować reporting i istniejący wybór aspektu; nie dodawać posiadania opinii o dowolnym przedmiocie.

Przyjąć wyłącznie wymienione propozycje; inne formy pozostają poza C2-A.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | myśli | nie myśli | pomyślał | nie pomyślał |
| żeńska | myśli | nie myśli | pomyślała | nie pomyślała |

### oshieru (B)

Uczyć kogoś czegoś i informować to różne ramy. object=* może dawać uczę pieniędzy; subject nie rozwiązuje wymaganych argumentów.

Zatwierdzić znaczenie/argumenty opisane w uwadze. Wariant 1: zachować wykluczenie z prostych przydawek. Wariant 2: zatwierdzić podane tłumaczenia i dokładne podmioty, po kontroli pełnego zdania.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | uczy | nie uczy | uczył | nie uczył |
| żeńska | uczy | nie uczy | uczyła | nie uczyła |

### osu (B)

Brak roli object mimo przechodniego naciskać/pchać. Dodać rolę dopiero po wskazaniu istniejących właściwych rzeczowników; nie zastępować jej location.

Zatwierdzić znaczenie/argumenty opisane w uwadze. Wariant 1: zachować wykluczenie z prostych przydawek. Wariant 2: zatwierdzić podane tłumaczenia i dokładne podmioty, po kontroli pełnego zdania.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | naciska | nie naciska | nacisnął | nie nacisnął |
| żeńska | naciska | nie naciska | nacisnęła | nie nacisnęła |

### owaru (B)

Praca i posiłek się kończą; yotei=plan może wymagać skończyło się wykonywanie planu. Wspólna klasa masculine_inanimate obejmie meal i yotei, więc sam brak klasy nie odseparuje znaczeń.

Zatwierdzić znaczenie/argumenty opisane w uwadze. Wariant 1: zachować wykluczenie z prostych przydawek. Wariant 2: zatwierdzić podane tłumaczenia i dokładne podmioty, po kontroli pełnego zdania.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskonieżywotna | kończy się | nie kończy się | skończył się | nie skończył się |
| żeńska | kończy się | nie kończy się | skończyła się | nie skończyła się |

### oyogu (A)

Ludzie i pies mogą pływać. Nie dopuszczać ogólnego ptaka, bo nie wszystkie ptaki pływają, ani łodzi, która wymaga innego japońskiego orzeczenia.

Przyjąć wyłącznie wymienione propozycje; inne formy pozostają poza C2-A.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | pływa | nie pływa | pływał | nie pływał |
| męskożywotna | pływa | nie pływa | pływał | nie pływał |
| żeńska | pływa | nie pływa | pływała | nie pływała |

### renshuusuru (A)

Ćwiczy w znaczeniu doskonalenia umiejętności jest samodzielne. Object=music/song zostaje bez zmian i wymaga osobnej oceny idiomatyczności ćwiczyć muzykę.

Przyjąć wyłącznie wymienione propozycje; inne formy pozostają poza C2-A.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | ćwiczy | nie ćwiczy | ćwiczył | nie ćwiczył |
| żeńska | ćwiczy | nie ćwiczy | ćwiczyła | nie ćwiczyła |

### sageru (B)

下げる oznacza obniżać/opuszczać przedmiot, nie opuszczać miejsce. Potrzebne dopełnienie i kontrola wieloznacznego polskiego tłumaczenia.

Zatwierdzić znaczenie/argumenty opisane w uwadze. Wariant 1: zachować wykluczenie z prostych przydawek. Wariant 2: zatwierdzić podane tłumaczenia i dokładne podmioty, po kontroli pełnego zdania.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | opuszcza | nie opuszcza | opuścił | nie opuścił |
| żeńska | opuszcza | nie opuszcza | opuściła | nie opuściła |

### sawaru (B)

Dotykać czegoś, a nie komuś; target particle に nie wyznacza polskiego przypadka. concrete obejmuje nieoczywiste media, wymaga przeglądu.

Zatwierdzić znaczenie/argumenty opisane w uwadze. Wariant 1: zachować wykluczenie z prostych przydawek. Wariant 2: zatwierdzić podane tłumaczenia i dokładne podmioty, po kontroli pełnego zdania.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | dotyka | nie dotyka | dotknął | nie dotknął |
| żeńska | dotyka | nie dotyka | dotknęła | nie dotknęła |

### sentakusuru (A)

Prać można bez jawnego ubrania; object=clothes pozostaje poprawnym zakresem. Nie dopuszczać przypadkowych rzeczy jako wykonawców.

Przyjąć wyłącznie wymienione propozycje; inne formy pozostają poza C2-A.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | pierze | nie pierze | prał | nie prał |
| żeńska | pierze | nie pierze | prała | nie prała |

### shimaru (A)

Nieprzechodnie zamykanie torby/pudełka; istniejąca precyzyjna rola wystarcza. Dodać tylko feminine/neuter w czterech formach.

Przyjąć wyłącznie wymienione propozycje; inne formy pozostają poza C2-A.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| żeńska | zamyka się | nie zamyka się | zamknęła się | nie zamknęła się |
| nijaka | zamyka się | nie zamyka się | zamknęło się | nie zamknęło się |

### shimeru (B)

Zamyka coś, odmiennie od shimaru. W przydawce podmiotowej potrzebne dopełnienie lub zatwierdzony kontekst.

Zatwierdzić znaczenie/argumenty opisane w uwadze. Wariant 1: zachować wykluczenie z prostych przydawek. Wariant 2: zatwierdzić podane tłumaczenia i dokładne podmioty, po kontroli pełnego zdania.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | zamyka | nie zamyka | zamknął | nie zamknął |
| żeńska | zamyka | nie zamyka | zamknęła | nie zamknęła |

### shinu (B)

Istoty żywe są poprawnymi podmiotami, ale person zawiera hitori. Sprawdzić też różnicę umrze/umiera w plain nonpast i stan 死んでいる.

Zatwierdzić znaczenie/argumenty opisane w uwadze. Wariant 1: zachować wykluczenie z prostych przydawek. Wariant 2: zatwierdzić podane tłumaczenia i dokładne podmioty, po kontroli pełnego zdania.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | umiera | nie umiera | umarł | nie umarł |
| męskożywotna | umiera | nie umiera | umarł | nie umarł |
| żeńska | umiera | nie umiera | umarła | nie umarła |

### shiru (B)

知らない zwykle znaczy nie wie/nie zna, nie mechanicznie nie dowiaduje się. 知っている wyraża wiedzę. Potrzebna decyzja o znaczeniu i rekcji, zanim powstaną uzgodnione przeczenia.

Zatwierdzić znaczenie/argumenty opisane w uwadze. Wariant 1: zachować wykluczenie z prostych przydawek. Wariant 2: zatwierdzić podane tłumaczenia i dokładne podmioty, po kontroli pełnego zdania.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | dowiaduje się | nie wie | dowiedział się | nie wiedział |
| żeńska | dowiaduje się | nie wie | dowiedziała się | nie wiedziała |

### soujisuru (A)

Sprzątanie jest samodzielną czynnością osoby; nie zmieniać object ani location. Dodatkowe dane nie naprawiają wszystkich obecnych dopełnień thing.

Przyjąć wyłącznie wymienione propozycje; inne formy pozostają poza C2-A.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | sprząta | nie sprząta | posprzątał | nie posprzątał |
| żeńska | sprząta | nie sprząta | posprzątała | nie posprzątała |

### sugosu (B)

Spędzać wymaga czasu, tu jikan. Nie tworzyć przydawki osoba, która spędza bez jawnego dopełnienia.

Zatwierdzić znaczenie/argumenty opisane w uwadze. Wariant 1: zachować wykluczenie z prostych przydawek. Wariant 2: zatwierdzić podane tłumaczenia i dokładne podmioty, po kontroli pełnego zdania.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | spędza | nie spędza | spędził | nie spędził |
| żeńska | spędza | nie spędza | spędziła | nie spędziła |

### suru (B)

Ogólne robić wymaga treści. Obecne robię obietnicę i robię sprawę do załatwienia są kolokacyjnie podejrzane; nie traktować całej listy object jako A.

Zatwierdzić znaczenie/argumenty opisane w uwadze. Wariant 1: zachować wykluczenie z prostych przydawek. Wariant 2: zatwierdzić podane tłumaczenia i dokładne podmioty, po kontroli pełnego zdania.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | robi | nie robi | robił | nie robił |
| żeńska | robi | nie robi | robiła | nie robiła |

### susumu (B)

Może opisywać ruch osoby albo postęp planu/pracy, ale te znaczenia mają różne naturalne polskie realizacje. Wariant osobowy wymaga akceptacji stylistycznej.

Zatwierdzić znaczenie/argumenty opisane w uwadze. Wariant 1: zachować wykluczenie z prostych przydawek. Wariant 2: zatwierdzić podane tłumaczenia i dokładne podmioty, po kontroli pełnego zdania.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | posuwa się naprzód | nie posuwa się naprzód | posunął się naprzód | nie posunął się naprzód |
| żeńska | posuwa się naprzód | nie posuwa się naprzód | posunęła się naprzód | nie posunęła się naprzód |

### suu (B)

Base wciągać, formy palę i potential mogę wciągać są niespójne. Dla palić tytoń potrzebny kontekst タバコ; nie wybierać znaczenia automatycznie.

Zatwierdzić znaczenie/argumenty opisane w uwadze. Wariant 1: zachować wykluczenie z prostych przydawek. Wariant 2: zatwierdzić podane tłumaczenia i dokładne podmioty, po kontroli pełnego zdania.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | pali | nie pali | palił | nie palił |
| żeńska | pali | nie pali | paliła | nie paliła |

### suwaru (B)

座る to siadać, 座っている to siedzieć. Teraźniejsze siedzę nie odpowiada neutralnie temu samemu aspektowi co usiadłem; decyzja przed C2.

Zatwierdzić znaczenie/argumenty opisane w uwadze. Wariant 1: zachować wykluczenie z prostych przydawek. Wariant 2: zatwierdzić podane tłumaczenia i dokładne podmioty, po kontroli pełnego zdania.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | siada | nie siada | usiadł | nie usiadł |
| męskożywotna | siada | nie siada | usiadł | nie usiadł |
| żeńska | siada | nie siada | usiadła | nie usiadła |

### taberu (A)

Jeść można bez jawnego jedzenia; żywy podmiot i object=food są rozdzielnymi rolami. Nie dopuszczać żywności jako wykonawcy.

Przyjąć wyłącznie wymienione propozycje; inne formy pozostają poza C2-A.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | je | nie je | jadł | nie jadł |
| męskożywotna | je | nie je | jadł | nie jadł |
| żeńska | je | nie je | jadła | nie jadła |

### tanoshimu (B)

楽しむ to czerpać przyjemność z czegoś. Samo cieszy się może oznaczać 喜ぶ; object=* i polska realizacja wymagają doprecyzowania.

Zatwierdzić znaczenie/argumenty opisane w uwadze. Wariant 1: zachować wykluczenie z prostych przydawek. Wariant 2: zatwierdzić podane tłumaczenia i dokładne podmioty, po kontroli pełnego zdania.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | cieszy się | nie cieszy się | cieszył się | nie cieszył się |
| żeńska | cieszy się | nie cieszy się | cieszyła się | nie cieszyła się |

### tateru (B)

Buduje bez dopełnienia jest możliwe kontekstowo; dla jednoznacznego materiału dydaktycznego wskazać home/school/taiikukan i ramę podmiot+obiekt.

Zatwierdzić znaczenie/argumenty opisane w uwadze. Wariant 1: zachować wykluczenie z prostych przydawek. Wariant 2: zatwierdzić podane tłumaczenia i dokładne podmioty, po kontroli pełnego zdania.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | buduje | nie buduje | budował | nie budował |
| żeńska | buduje | nie buduje | budowała | nie budowała |

### tatsu (B)

立つ to stanąć/wstać, 立っている to stać. Obecne stoję/stałem oraz thing nie są bezpieczną podstawą masowego uzgodnienia.

Zatwierdzić znaczenie/argumenty opisane w uwadze. Wariant 1: zachować wykluczenie z prostych przydawek. Wariant 2: zatwierdzić podane tłumaczenia i dokładne podmioty, po kontroli pełnego zdania.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | staje | nie staje | stanął | nie stanął |
| męskożywotna | staje | nie staje | stanął | nie stanął |
| żeńska | staje | nie staje | stanęła | nie stanęła |

### teishutsusuru (B)

提出する to przedkładać dokument. book/note/keikaku i teacher/school potrzebują kontroli kolokacji; składa bez dokumentu wieloznaczne.

Zatwierdzić znaczenie/argumenty opisane w uwadze. Wariant 1: zachować wykluczenie z prostych przydawek. Wariant 2: zatwierdzić podane tłumaczenia i dokładne podmioty, po kontroli pełnego zdania.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | składa | nie składa | złożył | nie złożył |
| żeńska | składa | nie składa | złożyła | nie złożyła |

### tojiru (B)

Zamyka książkę/pudełko, może też występować nieprzechodnio. Obecny wpis traktować jako przechodni; nie mieszać z shimaru.

Zatwierdzić znaczenie/argumenty opisane w uwadze. Wariant 1: zachować wykluczenie z prostych przydawek. Wariant 2: zatwierdzić podane tłumaczenia i dokładne podmioty, po kontroli pełnego zdania.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | zamyka | nie zamyka | zamknął | nie zamknął |
| żeńska | zamyka | nie zamyka | zamknęła | nie zamknęła |

### tomaru (B)

Zapisane 止まる oznacza zatrzymanie ruchu, nie nocleg 泊まる. Podmiotem mogą być ludzie i pojazdy; zatwierdzić osobno zakres, a target=place ocenić jako miejsce zatrzymania.

Zatwierdzić znaczenie/argumenty opisane w uwadze. Wariant 1: zachować wykluczenie z prostych przydawek. Wariant 2: zatwierdzić podane tłumaczenia i dokładne podmioty, po kontroli pełnego zdania.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | zatrzymuje się | nie zatrzymuje się | zatrzymał się | nie zatrzymał się |
| męskonieżywotna | zatrzymuje się | nie zatrzymuje się | zatrzymał się | nie zatrzymał się |
| żeńska | zatrzymuje się | nie zatrzymuje się | zatrzymała się | nie zatrzymała się |

### tooru (B)

通る przechodzi przez dane miejsce; obecna rola route jest właściwa. Bez trasy polskie przechodzi może być niejednoznaczne.

Zatwierdzić znaczenie/argumenty opisane w uwadze. Wariant 1: zachować wykluczenie z prostych przydawek. Wariant 2: zatwierdzić podane tłumaczenia i dokładne podmioty, po kontroli pełnego zdania.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | przechodzi | nie przechodzi | przeszedł | nie przeszedł |
| męskożywotna | przechodzi | nie przechodzi | przeszedł | nie przeszedł |
| żeńska | przechodzi | nie przechodzi | przeszła | nie przeszła |

### torihazusu (B)

Demontować coś lub zdejmować element; vehicle/thing obejmuje rzeczy, których zwykle się nie demontuje. Wymaga przedmiotu i dokładniejszej listy.

Zatwierdzić znaczenie/argumenty opisane w uwadze. Wariant 1: zachować wykluczenie z prostych przydawek. Wariant 2: zatwierdzić podane tłumaczenia i dokładne podmioty, po kontroli pełnego zdania.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | demontuje | nie demontuje | zdemontował | nie zdemontował |
| żeńska | demontuje | nie demontuje | zdemontowała | nie zdemontowała |

### toru (B)

Brać jest przechodnie i wieloznaczne. abstract/animal/thing wymagają kontroli kontekstu; nie dodawać bierze bez jawnego obiektu.

Zatwierdzić znaczenie/argumenty opisane w uwadze. Wariant 1: zachować wykluczenie z prostych przydawek. Wariant 2: zatwierdzić podane tłumaczenia i dokładne podmioty, po kontroli pełnego zdania.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | bierze | nie bierze | wziął | nie wziął |
| żeńska | bierze | nie bierze | wzięła | nie wzięła |

### tsukareru (B)

疲れる opisuje męczenie się/zmęczenie, stan jest zwykle 疲れている. Obecne jestem zmęczony i potential/imperative wymagają oceny, a person zawiera hitori.

Zatwierdzić znaczenie/argumenty opisane w uwadze. Wariant 1: zachować wykluczenie z prostych przydawek. Wariant 2: zatwierdzić podane tłumaczenia i dokładne podmioty, po kontroli pełnego zdania.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | męczy się | nie męczy się | zmęczył się | nie zmęczył się |
| męskożywotna | męczy się | nie męczy się | zmęczył się | nie zmęczył się |
| żeńska | męczy się | nie męczy się | zmęczyła się | nie zmęczyła się |

### tsukau (B)

Używać wymaga czegoś; wildcard object obejmuje także abstrakty niepasujące do wybranego znaczenia. Zachować genitive do czasu osobnego przeglądu.

Zatwierdzić znaczenie/argumenty opisane w uwadze. Wariant 1: zachować wykluczenie z prostych przydawek. Wariant 2: zatwierdzić podane tłumaczenia i dokładne podmioty, po kontroli pełnego zdania.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | używa | nie używa | używał | nie używał |
| żeńska | używa | nie używa | używała | nie używała |

### tsukeru (B)

Dla television włączać jest naturalne, ale bez obiektu niejednoznaczne. Nie rozszerzać na inne znaczenia 付ける automatycznie.

Zatwierdzić znaczenie/argumenty opisane w uwadze. Wariant 1: zachować wykluczenie z prostych przydawek. Wariant 2: zatwierdzić podane tłumaczenia i dokładne podmioty, po kontroli pełnego zdania.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | włącza | nie włącza | włączył | nie włączył |
| żeńska | włącza | nie włącza | włączyła | nie włączyła |

### tsukuru (B)

作る oznacza wytwarzać/przygotowywać; object=* dopuszcza osoby/dni. Potrzebna selekcja produktu i wybór robić/tworzyć przed subject.

Zatwierdzić znaczenie/argumenty opisane w uwadze. Wariant 1: zachować wykluczenie z prostych przydawek. Wariant 2: zatwierdzić podane tłumaczenia i dokładne podmioty, po kontroli pełnego zdania.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | robi | nie robi | zrobił | nie zrobił |
| żeńska | robi | nie robi | zrobiła | nie zrobiła |

### tsuzukeru (B)

Kontynuować wymaga treści; music/song to raczej kontynuować granie/śpiewanie. Potrzebne dopełnienie, nie automatyczne poszerzanie podmiotów.

Zatwierdzić znaczenie/argumenty opisane w uwadze. Wariant 1: zachować wykluczenie z prostych przydawek. Wariant 2: zatwierdzić podane tłumaczenia i dokładne podmioty, po kontroli pełnego zdania.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | kontynuuje | nie kontynuuje | kontynuował | nie kontynuował |
| żeńska | kontynuuje | nie kontynuuje | kontynuowała | nie kontynuowała |

### ugoku (B)

Ruch osoby, zwierzęcia, pojazdu i rzeczy możliwy, lecz thing obejmuje statyczne przedmioty. Rozstrzygnąć ruch samoczynny i bierne poruszenie, hitori oraz kontekst.

Zatwierdzić znaczenie/argumenty opisane w uwadze. Wariant 1: zachować wykluczenie z prostych przydawek. Wariant 2: zatwierdzić podane tłumaczenia i dokładne podmioty, po kontroli pełnego zdania.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | rusza się | nie rusza się | ruszał się | nie ruszał się |
| męskożywotna | rusza się | nie rusza się | ruszał się | nie ruszał się |
| męskonieżywotna | rusza się | nie rusza się | ruszał się | nie ruszał się |
| żeńska | rusza się | nie rusza się | ruszała się | nie ruszała się |

### ukeru (B)

受ける z shigoto zwykle przyjąć pracę/zlecenie, nie odebrać pracę w sensie technicznym. Zatwierdzić znaczenie i rekcję przed rozszerzeniem.

Zatwierdzić znaczenie/argumenty opisane w uwadze. Wariant 1: zachować wykluczenie z prostych przydawek. Wariant 2: zatwierdzić podane tłumaczenia i dokładne podmioty, po kontroli pełnego zdania.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | odbiera | nie odbiera | odebrał | nie odebrał |
| żeńska | odbiera | nie odbiera | odebrała | nie odebrała |

### undousuru (A)

Samodzielna aktywność fizyczna osoby; bez dodawania narzędzi i bez utożsamienia z ćwiczeniem utworu.

Przyjąć wyłącznie wymienione propozycje; inne formy pozostają poza C2-A.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | ćwiczy fizycznie | nie ćwiczy fizycznie | ćwiczył fizycznie | nie ćwiczył fizycznie |
| żeńska | ćwiczy fizycznie | nie ćwiczy fizycznie | ćwiczyła fizycznie | nie ćwiczyła fizycznie |

### usowotsuku (A)

Kłamać można bez jawnego adresata; うそをつく jest całym zapisanym leksemem. Nie tworzyć drugiego slotu dla うそ.

Przyjąć wyłącznie wymienione propozycje; inne formy pozostają poza C2-A.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | kłamie | nie kłamie | skłamał | nie skłamał |
| żeńska | kłamie | nie kłamie | skłamała | nie skłamała |

### utau (A)

Śpiew osoby jest samodzielny. Ptaki zwykle 鳴く/さえずる; nie dodawać ich do A. Object=media odrębnie wymaga wykluczenia np. głosu.

Przyjąć wyłącznie wymienione propozycje; inne formy pozostają poza C2-A.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | śpiewa | nie śpiewa | śpiewał | nie śpiewał |
| żeńska | śpiewa | nie śpiewa | śpiewała | nie śpiewała |

### wakaru (C)

Obecny subject oznacza rozumianą treść, nie osobę rozumiejącą. Uzgodnienie do niego dałoby książka rozumie. Potrzebna rama doświadczającego albo inny polski predykat, bez zmiany znaczenia roli.

Nie dodawać B2 do obecnej roli. Użyć lub opracować konstrukcję wskazaną w uwadze, z osobną weryfikacją argumentów.

Nie proponuję map do XML. Osobowe kandydaty do ewentualnej innej ramy: rozumie; zrozumiał / zrozumiała / zrozumiało. Formy dyskusyjne, nie przypisywać do obecnego subject; przeczenia i argumenty wymagają konstrukcji.

### warau (A)

Śmiech osoby może być samodzielny. Zachować z_genitive dla wyśmiewanej osoby/zwierzęcia; podmiot nie jest tym samym argumentem co object.

Przyjąć wyłącznie wymienione propozycje; inne formy pozostają poza C2-A.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | śmieje się | nie śmieje się | śmiał się | nie śmiał się |
| żeńska | śmieje się | nie śmieje się | śmiała się | nie śmiała się |

### wasureru (B)

Zapomina może być samodzielne, ale object=* i warianty dopełniacz/biernik/o+miejscownik zależą od znaczenia. Nie uznawać genitive automatycznie za błąd.

Zatwierdzić znaczenie/argumenty opisane w uwadze. Wariant 1: zachować wykluczenie z prostych przydawek. Wariant 2: zatwierdzić podane tłumaczenia i dokładne podmioty, po kontroli pełnego zdania.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | zapomina | nie zapomina | zapomniał | nie zapomniał |
| żeńska | zapomina | nie zapomina | zapomniała | nie zapomniała |

### yomu (A)

Czytanie ma naturalne użycie bez jawnego tekstu. Precyzyjna lista ludzi, zachować object=text; nie dodawać zwierząt ani rzeczy.

Przyjąć wyłącznie wymienione propozycje; inne formy pozostają poza C2-A.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | czyta | nie czyta | czytał | nie czytał |
| żeńska | czyta | nie czyta | czytała | nie czytała |

### ageru_give (B)

Dawanie od nadawcy do odbiorcy; potrzebny przedmiot i perspektywa あげる. Zapis komuś może dublować jawny target.

Zatwierdzić znaczenie/argumenty opisane w uwadze. Wariant 1: zachować wykluczenie z prostych przydawek. Wariant 2: zatwierdzić podane tłumaczenia i dokładne podmioty, po kontroli pełnego zdania.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | daje komuś | nie daje komuś | dał komuś | nie dał komuś |
| żeńska | daje komuś | nie daje komuś | dała komuś | nie dała komuś |

### kaesu (B)

Oddaje rzecz komuś; bez obiektu lub adresata jest kontekstowe. Nie łączyć z kaeru wracać.

Zatwierdzić znaczenie/argumenty opisane w uwadze. Wariant 1: zachować wykluczenie z prostych przydawek. Wariant 2: zatwierdzić podane tłumaczenia i dokładne podmioty, po kontroli pełnego zdania.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | oddaje | nie oddaje | oddał | nie oddał |
| żeńska | oddaje | nie oddaje | oddała | nie oddała |

### kasu (B)

Dający pożyczkę, odmiennie od kariru. Rozstrzygnąć wstawiony tekst komuś i jawnego adresata przed subject.

Zatwierdzić znaczenie/argumenty opisane w uwadze. Wariant 1: zachować wykluczenie z prostych przydawek. Wariant 2: zatwierdzić podane tłumaczenia i dokładne podmioty, po kontroli pełnego zdania.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | pożycza komuś | nie pożycza komuś | pożyczył komuś | nie pożyczył komuś |
| żeńska | pożycza komuś | nie pożycza komuś | pożyczyła komuś | nie pożyczyła komuś |

### kureru (B)

Perspektywa beneficjenta mi/nam wymaga wyboru. Rozkaz くれ jest poprawnym wyjątkiem; nie zmieniać na mechaniczne くれろ.

Zatwierdzić znaczenie/argumenty opisane w uwadze. Wariant 1: zachować wykluczenie z prostych przydawek. Wariant 2: zatwierdzić podane tłumaczenia i dokładne podmioty, po kontroli pełnego zdania.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | daje mi | nie daje mi | dał mi | nie dał mi |
| żeńska | daje mi | nie daje mi | dała mi | nie dała mi |

### morau (B)

Otrzymuje coś od kogoś; samodzielna przydawka bez rzeczy jest niedookreślona. Nie kopiować kierunku target z czasowników dawania.

Zatwierdzić znaczenie/argumenty opisane w uwadze. Wariant 1: zachować wykluczenie z prostych przydawek. Wariant 2: zatwierdzić podane tłumaczenia i dokładne podmioty, po kontroli pełnego zdania.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | otrzymuje | nie otrzymuje | otrzymał | nie otrzymał |
| żeńska | otrzymuje | nie otrzymuje | otrzymała | nie otrzymała |

### odoroku (B)

驚く jest reakcją, stan bycia zaskoczonym wymaga kontekstu. Obecne jestem/byłem zaskoczony i causative zaskakiwać kogoś mają różną osobę/postać.

Zatwierdzić znaczenie/argumenty opisane w uwadze. Wariant 1: zachować wykluczenie z prostych przydawek. Wariant 2: zatwierdzić podane tłumaczenia i dokładne podmioty, po kontroli pełnego zdania.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | dziwi się | nie dziwi się | zdziwił się | nie zdziwił się |
| żeńska | dziwi się | nie dziwi się | zdziwiła się | nie zdziwiła się |

### damaru (B)

黙る to zamilknąć, 黙っている to milczeć. Obecne person animal obejmuje też hitori i ptaka; decyzja aspektowa przed agreement.

Zatwierdzić znaczenie/argumenty opisane w uwadze. Wariant 1: zachować wykluczenie z prostych przydawek. Wariant 2: zatwierdzić podane tłumaczenia i dokładne podmioty, po kontroli pełnego zdania.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | milczy | nie milczy | milczał | nie milczał |
| żeńska | milczy | nie milczy | milczała | nie milczała |

### watasu (B)

Przekazuje coś komuś. Wildcard-like szeroki object obejmuje abstrakty; podaję obietnicę nie jest neutralnym odpowiednikiem.

Zatwierdzić znaczenie/argumenty opisane w uwadze. Wariant 1: zachować wykluczenie z prostych przydawek. Wariant 2: zatwierdzić podane tłumaczenia i dokładne podmioty, po kontroli pełnego zdania.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | podaje | nie podaje | podał | nie podał |
| żeńska | podaje | nie podaje | podała | nie podała |

### sukuu (B)

Ratować można absolutnie, ale wybór 救う oraz object=inochi wymaga spójności ratować życie versus ratować osobę. Zachować jako kandydat do późniejszej weryfikacji.

Zatwierdzić znaczenie/argumenty opisane w uwadze. Wariant 1: zachować wykluczenie z prostych przydawek. Wariant 2: zatwierdzić podane tłumaczenia i dokładne podmioty, po kontroli pełnego zdania.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | ratuje | nie ratuje | uratował | nie uratował |
| żeńska | ratuje | nie ratuje | uratowała | nie uratowała |

### shinjiru (A)

Wierzy może opisywać osobę bez jawnego obiektu wiary. Zachować w_accusative; wiara w osobę i ufanie osobie nie są automatycznie tą samą rekcją.

Przyjąć wyłącznie wymienione propozycje; inne formy pozostają poza C2-A.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | wierzy | nie wierzy | wierzył | nie wierzył |
| żeńska | wierzy | nie wierzy | wierzyła | nie wierzyła |

### sumu (B)

住む może oznaczać zamieszkać, a 住んでいる stan mieszkania. Sama przydawka mieszka bez miejsca wymaga kontekstu; nie dodawać automatycznie subject.

Zatwierdzić znaczenie/argumenty opisane w uwadze. Wariant 1: zachować wykluczenie z prostych przydawek. Wariant 2: zatwierdzić podane tłumaczenia i dokładne podmioty, po kontroli pełnego zdania.

| Klasa | dictionary | plain_negative | past_plain | past_negative_plain |
|---|---|---|---|---|
| męskoosobowa | mieszka | nie mieszka | mieszkał | nie mieszkał |
| żeńska | mieszka | nie mieszka | mieszkała | nie mieszkała |
