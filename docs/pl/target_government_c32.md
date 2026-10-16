# C3.2: uniwersalny target i polska rekcja

`target` oznacza argument relacji danego czasownika, zwykle z に. Nie jest synonimem `object` (np. pożyczana książka z を) ani `destination` (cel ruchu). Target może oznaczać źródło pożyczki, odbiorcę, adresata gniewu albo miejsce uczęszczania. Japońskie に pozostaje tekstem wzorca; sama rola nie wstawia partykuły.

`government` na konkretnej roli czasownika wskazuje współdzieloną polską ramkę. Silnik nadal wykorzystuje istniejące wiązanie i `role_matches`, także przy kilku rolach jednego czasownika. Brak ramki odrzuca kandydata do tego wzorca. Nie ma listy ID w patternie ani tabeli czasownik–rzeczownik.

## Wzorzec produkcyjny

```xml
<sentence_pattern id="Czasownik z target" category="basic"
    forms="dictionary polite_nonpast plain_negative polite_negative past_plain past_polite past_negative_plain past_negative_polite">
  <question>{verb@action[role:target, form].translation} {noun@target[government:@action].phrase}.</question>
  <answer>{noun@target}に{verb@action[form]}。</answer>
</sentence_pattern>
```

Jedynym uzupełnieniem proponowanego XML jest istniejący atrybut `forms`. Osiem podstawowych form zachowuje role uczestników; strona bierna, kauzatywna i samodzielne formy łączące nie należą do tej konstrukcji. Ograniczenie dotyczy wzorca, nie słownika.

## Audyt wszystkich 21 deklaracji

11 czasowników otrzymuje rekcję; 10 pozostaje bez ramki target. Poniższe decyzje dotyczą obecnego znaczenia słownikowego i dopuszczonych argumentów.

| Czasownik | Ramka / gotowość | Znaczenie, rekcja i granica |
|---|---|---|
| `ayamaru` | `direct_object` | osoba przepraszana; biernik, przy negacji dopełniacz |
| `hairu` | `do_genitive` | wnętrze; do + dopełniacz; building (budynki i pomieszczenia) |
| `ireru` | `poza / excluded` | pojemnik; do + dopełniacz, ale konstrukcja wymaga sensownego wkładanego przedmiotu |
| `kariru` | `od_genitive` | źródło pożyczki; od + dopełniacz; wariant tłumaczenia |
| `kayou` | `do_genitive` | miejsce regularnego uczęszczania; do + dopełniacz |
| `kotaeru` | `poza / excluded` | osoba: celownik; wiadomość: na + biernik; jeden profil nie wystarcza |
| `nareru` | `poza / excluded` | obiekt przyzwyczajenia; do + dopełniacz, ale wildcard obejmuje nieodpowiednie pojęcia i ilości |
| `naru` | `poza / excluded` | rezultat przemiany; narzędnik; wildcard nie określa możliwych rezultatów |
| `okoru` | `na_accusative` | adresat gniewu; na + biernik również w przeczeniu |
| `oshieru` | `poza / excluded` | uczę osobę (biernik/dopełniacz) albo przekazuję coś osobie (celownik); zależy od konstrukcji i znaczenia |
| `sawaru` | `poza / excluded` | dotykany obiekt; dopełniacz, ale concrete zawiera też muzykę, głos i mail |
| `teishutsusuru` | `poza / excluded` | adresat składania; nauczycielowi / w szkole; potrzebny przedmiot i różne rekcje |
| `tomaru` | `poza / excluded` | miejsce zatrzymania; w/na/przy; dodatkowo rozróżnienie 止まる i 泊まる |
| `usowotsuku` | `dative` | osoba okłamywana; celownik |
| `ageru_give` | `dative` | odbiorca poza mówiącym; celownik; wariant tłumaczenia; rzecz pominięta kontekstowo |
| `kaesu` | `dative` | odbiorca zwrotu; celownik; rzecz pominięta kontekstowo |
| `kasu` | `dative` | pożyczkobiorca; celownik; wariant tłumaczenia |
| `kureru` | `poza / excluded` | odbiorca z perspektywy mówiącego; celownik; dowolna osoba nie zachowuje deiksy mi/nam |
| `morau` | `od_genitive` | dawca; od + dopełniacz; rzecz pominięta kontekstowo |
| `watasu` | `dative` | odbiorca przekazywanego przedmiotu; celownik; rzecz pominięta kontekstowo |
| `sumu` | `poza / excluded` | miejsce zamieszkania; w/na + miejscownik; place obejmuje też miejsca niezamieszkiwalne |

## Ramki i kategorie

Dodano `do_genitive`, `od_genitive`, `dative` w katalogu języka polskiego aplikacji. Wykorzystano też istniejące `direct_object` i `na_accusative`. Wszystkie pięć ramek jest współdzielone. Przeczenie nie zmienia dopełniacza po do/od ani celownika; direct_object zmienia biernik na dopełniacz.

Końcowa hierarchia to `attendance_facility → building → place → concrete`. `building` świadomie obejmuje budynki i pomieszczenia. `attendance_facility` łączy placówki edukacyjne i sportowe odpowiednie do regularnego uczęszczania, bez rozróżniania ich funkcji instytucjonalnej. Dodatkowa warstwa wnętrz jest zbędna w tym praktycznym modelu.

`kayou` przyjmuje `attendance_facility`; tę kategorię mają school i taiikukan. Nowe rzeczowniki i podtypy dziedziczą dopasowanie bez edycji czasownika. Zwykły budynek (bank, biurowiec) nie wystarcza. `hairu` przyjmuje `building`: szkoła, pokój, daidokoro i jimusitsu działają z `do_genitive`. Pokój, kuchnia i biuro mają teraz `building`. Dopasowania do place/concrete pozostają dziedziczone. Kaigan, park, bazaaru, naka i oku zachowują `place` i pozostają poza obecną rekcją hairu. `kariru` i `kasu` zachowują `person`.

Audyt aktualnych słowników wykazał bezpośrednie odwołania do usuwanych kategorii tylko w hairu i kayou. Pozostałe accepts/nouns są niezmienione, w tym dziesięć wyłączonych czasowników target. Historyczne raporty C3 zachowują ówczesny katalog.

**Świadomy skutek dla tateru:** jego `object accepts="building"` dopuszcza teraz pokój, kuchnię i biuro w istniejących wzorcach object, nie tylko w nowym wzorcu target. Polskie „buduję pokój/kuchnię/biuro” może opisywać prace budowlane. Japońskie 建てる dotyczy przede wszystkim wznoszenia budynku ([Daijisen, Shogakukan](https://kotobank.jp/word/建てる-561735)); w naszej ocenie językowej 部屋を建てる i 台所を建てる są mniej naturalne przy urządzaniu wnętrza niż 作る. 事務室 również oznacza pomieszczenie, niekoniecznie osobny budynek biurowy. To rzeczywiste ograniczenie naturalności połączeń w świadomie szerokiej kategorii, nie błąd solvera ani przypadku. Nie dodajemy kategorii, wyjątków nouns ani zmiany czasownika. Inne role przyjmujące place/concrete zachowują dopasowania do przodków.

**Starsze projekty użytkownika:** przy gramatyce wbudowanej ładowanie deterministycznie mapuje `enclosed_space → building` oraz `education_facility / sports_facility → attendance_facility`. To migracja wejścia, nie aliasy w katalogu wyboru. Obejmuje kategorie rzeczowników, accepts czasowników, describes przymiotników, target_categories zaimków pytających i selektory kategorii rzeczowników w pytaniach/odpowiedziach. Połączone listy są deduplikowane. Własna gramatyka projektu pozostaje nietknięta, podobnie katalogi przysłówków, ID słów, etykiety i nieznane kategorie. Nieznane ID nadal nie przechodzą walidacji. Otwarcie i zapis bez edycji niczego nie zapisują; zapis fragmentów zachowuje niezmienione stare atrybuty i niezwiązany XML, a kolejne ładowanie nadal je migruje. Jawnie zmieniane kategorie i nowe rzeczowniki używają aktualnych ID. Jeżeli połączenie kategorii scaliłoby dwa wcześniej odrębne sloty rzeczowników bez aliasów, ładowanie zgłasza konieczność nadania im różnych istniejących @aliasów; pliki pozostają bez zmian. Nie ma automatycznego destrukcyjnego przepisywania danych.

## Tłumaczenie z jawnym argumentem

Opcjonalny `target_translation` jest atrybutem konkretnej formy:

```xml
<form ref="dictionary" kana="かりる" translation="pożyczam od kogoś"
      target_translation="pożyczam" />
```

Wspólny plan realizacji zapisuje czasowniki, których target jest realizowany jako pełne `noun[government].phrase` w pytaniu, z tym samym powiązaniem roli i źródłem rekcji. Renderer sprawdza przynależność do gotowego zbioru; nie przeszukuje zdań ani nie enumeruje kandydatów. Jawne `government:@action` i automatyczne `government` działają tak samo. Target tylko w odpowiedzi, kana lub bazowe tłumaczenie rzeczownika oraz samo wyjście przypadku, przyimka lub odmienionego tłumaczenia nie aktywują wariantu. Pełny argument rekcyjny deklarujemy przez `.phrase`. Target innego czasownika nie aktywuje wariantu. Kolejność placeholderów nie ma znaczenia; target i object mogą współistnieć.

Brak wariantu zachowuje zwykłe tłumaczenie. Quiz samego czasownika nadal pokazuje „pożyczam od kogoś”. Wariant dodano tylko dla ośmiu form kariru, kasu i ageru_give. W Studio jest to edytowalna kolumna **Tłumaczenie z jawnym target (opcjonalne)** w tabeli form czasownika. Puste pole usuwa wariant; generowanie japońskich form zachowuje go. Po wyłączeniu języka źródłowego XML jest zachowywany jako nieaktywne rozszerzenie.

Wariant dotyczy zwykłego `.translation` wybranej formy. Nie zastępuje jawnego `translation:base` ani osobnego katalogu `agree` dla odmiany przez podmiot. Łączenie obu wariantów w przyszłej konstrukcji z jawnym podmiotem wymaga osobnego projektu, bez automatycznego obcinania tekstu.

## Przykłady i ograniczenia

| Polski | Japoński |
|---|---|
| uczęszczam do szkoły. | がっこうにかよう。 |
| uczęszczam do sali gimnastycznej. | たいいくかんにかよう。 |
| wchodzę do szkoły. | がっこうにはいる。 |
| wchodzę do pokoju. | へやにはいる。 |
| wchodzę do kuchni. | だいどころにはいる。 |
| wchodzę do biura. | じむしつにはいる。 |
| pożyczam od siostry. | あねにかりる。 |
| pożyczam siostrze. | あねにかす。 |
| nie pożyczam od siostry. | あねにかりない。 |

Relacja rzeczownika `destination` może dawać „na salę gimnastyczną”, ale w tym wzorcu ramka kayou daje „do sali gimnastycznej”. Brak rozbudowy rekcji zależnej jednocześnie od typu rzeczownika i czasownika jest świadomą granicą tej wersji. Zdania transferu pomijają rzecz znaną z kontekstu; nie przedstawiają pełnego zdarzenia bez kontekstu. Tłumaczenia form przeszłych zachowują istniejącą męską pierwszą osobę.

## Publikacja i weryfikacja

Content 64 wymaga manifestu formatu 3. Format 2 pozostaje barierą dla rewizji 63, format 1 dla starszych danych. Nowy klient akceptuje wszystkie trzy; klient C3 odrzuca format 3 przed pobieraniem plików. Walidacja całego snapshotu, hashy i rollback pozostają bez zmian. Najpierw należy udostępnić kompatybilną aplikację. Nowa rewizja jest potrzebna z powodu pola formy, kategorii i wzorca.

Testy aplikacji używają niezależnych fixture v2: `test_universal_target.py`, `test_target_translation_persistence.py` i istniejących testów C3/C3.1. Produkcyjne przykłady i liczenie sprawdza osobny opt-in `../Kotomi-Data/tools/validate_target_c32.py --kotomi .`, poza zwykłymi testami. Raporty w `docs/validation` opisują dokładny zakres i pomiary. Historyczne raporty C3 pozostają dowodem tamtego etapu, nie aktualnym snapshotem C3.2.

Pomiary: 15 rund cold/warm, skala 1/10/50/200 po 21 rund. Odchylenie pojedynczej ścieżki potwierdzono w 7 naprzemiennych procesach po 301 próbek: +2,34%. Brak potwierdzonej regresji ponad 10%. Polecenia: `tools/benchmark_lesson_focus.py --rounds 15` oraz `tools/benchmark_target_c32.py --kotomi CHECKOUT --output report.json`. Protokół: `tools/updates/validate_content_compatibility_c32.py --kotomi CHECKOUT` (dla poprzedniego main dodaj `--legacy-c3`). Raporty akceptacji i wydajności są w Kotomi-Data: `docs/validation/target_c32_acceptance.json`, `target_c32_performance.json`.

Poprawki po review zachowują Content 64 / manifest 3 oraz dokładną postać produkcyjnego wzorca. Wersja aplikacji, ramki rekcji i wyłączone czasowniki pozostają bez zmian.

Pomiar poprawek względem commita PR #218 `28b1229`: 31 rund, skala 1/10/50/200, także enumeracja i podgląd symulatora. Pierwsze odchylenia osiągnęły +17,70%; wszystkie ponad 10% sprawdzono ponownie w 7 naprzemiennych parach świeżych procesów (301 próbek target / 101 próbek lekcji). Największy ponownie zmierzony wzrost wyniósł +0,99%; pozostałe pierwsze pomiary były poniżej 10% (maksimum +9,80%). Brak potwierdzonej regresji ponad 10%. Ten sam raport wydajności zachowuje wyniki pierwszego i powtórzonego pomiaru.
