# Import kanji 156–165, raport językowy i techniczny

Data analizy: 2026-10-28. Materiały: *新漢字16-1（156–160）* i *新漢字16-2（161–165）*, po jednej stronie PDF; 10 kanji i 39 pozycji. Stan bazowy: Kotomi-Data main Content 69, Kotomi main na dzień analizy. Branch docelowy: `feature/kanji-16-vocabulary-156-165`. Bez zmian kodu Python, DSL i istniejących wzorców. Nowa kategoria jest definiowana deklaratywnie w oddzielnym branchu Kotomi. Bez PR.

## A. Pełna inwentaryzacja (39/39)

| Kanji nr | Japoński zapis | Kana | Znaczenie źródłowe | ID | Słownik / semantyka | Status | Formy | Uwagi |
|---:|---|---|---|---|---|---|---|---|
| 156 | 私 | わたし／わたくし | ja | brak | nieobsługiwane | Wymaga decyzji | Brak | Zaimek osobowy; brak odrębnego kontraktu zaimków i odmiany pierwszej osoby. |
| 156 | 私立 | しりつ | prywatny | brak | nieobsługiwane | Wymaga decyzji | Brak | Rzeczownik/no-adjective z 〜の, nie regularny na-adjective. |
| 156 | 私用 | しよう | prywatny użytek; prywatna sprawa | `shiyou` | `nouns` / abstract | Dodane | 7 przypadków | Przyjęto sens «prywatny użytek»; drugie znaczenie do osobnej analizy. |
| 157 | 兄 | あに | starszy brat (własny) | `ani` | `nouns` / person | Dodane | 7 + few/many | Odniesienie do własnej rodziny jest pragmatyczne. |
| 157 | お兄さん | おにいさん | starszy brat (czyjś) | `oniisan` | `nouns` / person | Dodane | 7 + few/many | Honorificzne określenie; polski przekład koliduje z 兄. |
| 157 | 父兄 | ふけい | rodzice, opiekunowie | `fukei` | `nouns` / person | Dodane | 7 (pluralia) | Kontekst szkolny; słowo tradycyjne, preferuje się 保護者. |
| 158 | 弟 | おとうと | młodszy brat | `otouto` | `nouns` / person | Dodane | 7 + few/many | Relacja wieku zakodowana w polskich przypadkach. |
| 158 | 兄弟 | きょうだい | rodzeństwo; bracia | `kyoudai` | `nouns` / abstract | Dodane | 7 (zbiorowe) | Wybrano neutralne rodzeństwo, nie mylono grupy z osobą. |
| 159 | 姉 | あね | starsza siostra (własna) | `sister` | `nouns` / person | Uzupełnione | 7 + few/many | Korekta wcześniejszego, zbyt ogólnego «siostra». |
| 159 | お姉さん | おねえさん | starsza siostra (czyjaś) | `oneesan` | `nouns` / person | Dodane | 7 + few/many | Honorificzne określenie; polski przekład koliduje z 姉. |
| 160 | 妹 | いもうと | młodsza siostra | `imouto` | `nouns` / person | Dodane | 7 + few/many | Rozróżnienie starsza/młodsza utrzymane. |
| 160 | 姉妹 | しまい | siostry | `shimai` | `nouns` / person | Dodane | 7 (liczba mnoga) | Zbiorowa grupa żeńska, brak jednostkowego licznika. |
| 161 | 親 | おや | rodzic | `oya` | `nouns` / person | Dodane | 7 + few/many | Japoński rodzic nie wymusza płci, polski rodzic ma rodzaj gramatyczny. |
| 161 | 親指 | おやゆび | kciuk | `oyayubi` | `nouns` / body_part | Poprawione deklaratywnie | 7 + few/many | Brak kategorii «część ciała»; użyto szerokiego konkretu i licznika 本. |
| 161 | 親しい | したしい | bliski, dobrze znany | `shitashii` | `adjectives` / describes: person | Dodane | 15 japońskich + PL | Przymiotnik i, bliski relacyjnie, nie bez ograniczeń dla wszystkich rzeczy. |
| 161 | 両親 | りょうしん | rodzice | `ryoushin` | `nouns` / person | Dodane | 7 (liczba mnoga) | Zbiorowość rodziców, nie dowolna pojedyncza osoba. |
| 161 | 親友 | しんゆう | przyjaciel | `shinyuu` | `nouns` / person | Dodane | 7 + few/many | Bliski przyjaciel, nie każdy znajomy. |
| 161 | 肉親 | にくしん | krewny | `nikushin` | `nouns` / person | Dodane | 7 + few/many | Bliski krewny, nie ogólna grupa rodzinna. |
| 162 | 主 | あるじ | głowa rodu | `aruji` | `nouns` / person | Dodane | 7 + few/many | Sens gospodarz/pan domu; inne użycia kontekstowe. |
| 162 | 主な | おもな | główny | brak | nieobsługiwane | Wymaga decyzji | Brak | Funkcja wyłącznie przydawkowa, nie regularna odmiana na-adjective. |
| 162 | 主人 | しゅじん | mąż; właściciel; pan domu | `shujin_husband + shujin_owner` | `nouns` / person | Dodane (2 sensy) | 7 + few/many | Rozdzielono męża i właściciela. Lekcja referuje sens «mąż». |
| 162 | 主要な | しゅような | główny | `shuyou` | `adjectives` / describes: abstract person place | Dodane, blokada lekcji | 11 japońskich + PL | Lemma 主要 jest poprawna, ale dictionary_ref nie wybiera 主要な. |
| 162 | 主語 | しゅご | podmiot | `shugo` | `nouns` / abstract | Dodane | 7 + few/many | Pojęcie gramatyczne, nie człowiek. |
| 162 | 主張する | しゅちょうする | twierdzić, upierać się | `shuchousuru` | `verbs` / subject: person; reporting | Dodane | 17 japońskich + uzgodnienia | Składnia zdań podrzędnych (〜と) nieobsługiwana przez proste role. |
| 163 | 祖父 | そふ | dziadek | `sofu` | `nouns` / person | Dodane | 7 + few/many | Wpis osobowy. |
| 163 | 祖母 | そぼ | babcia | `sobo` | `nouns` / person | Dodane | 7 + few/many | Wpis osobowy. |
| 163 | 祖父母 | そふぼ | dziadkowie | `sofubo` | `nouns` / person | Dodane | 7 (liczba mnoga) | Zbiorowa para/grupa dziadków. |
| 163 | 祖国 | そこく | ojczyzna | `sokoku` | `nouns` / country | Dodane | 7 przypadków | Ojczyzna jako kraj pochodzenia/przynależności. |
| 163 | 祖先 | そせん | przodek | `sosen` | `nouns` / person | Dodane | 7 + few/many | Synonim 先祖, możliwa kolizja w quizach. |
| 163 | 先祖 | せんぞ | przodek | `senzo` | `nouns` / person | Dodane | 7 + few/many | Synonim 祖先, inne słowo/odczyt, bez sztucznego duplikowania ID. |
| 164 | 家族 | かぞく | rodzina | `kazoku` | `nouns` / abstract | Dodane | 7 przypadków | Jednostka społeczna, nie pojedynczy człowiek; brak kategorii kolektywnej. |
| 164 | 一族 | いちぞく | cała rodzina, klan | `ichizoku` | `nouns` / abstract | Dodane | 7 przypadków | Klan lub rozbudowana wspólnota rodowa. |
| 164 | 民族 | みんぞく | rasa, naród, nacja | `minzoku` | `nouns` / abstract | Dodane | 7 przypadków | Przyjęto «grupa etniczna», bez utożsamiania z rasą biologiczną. |
| 164 | 種族 | しゅぞく | rasa, plemię | `shuzoku` | `nouns` / abstract | Dodane | 7 przypadków | «Plemię»; biologiczna klasyfikacja wymaga odrębnego sensu. |
| 165 | 犬 | いぬ | pies | `inu` | `nouns` / animal | Istniejące | 7 + few/many | Zachowano istniejące poprawne ID. |
| 165 | 子犬 | こいぬ | szczenię | `koinu` | `nouns` / animal | Dodane | 7 + few/many | Licznik 匹, polski rodzaj nijaki. |
| 165 | 犬小屋 | いぬごや | buda dla psa | `inugoya` | `nouns` / building | Dodane | 7 + few/many | Buda jako obiekt/schronienie; ogólne liczenie obiektów. |
| 165 | 野良犬 | のらいぬ | bezpański pies | `norainu` | `nouns` / animal | Dodane | 7 + few/many | Pies bez właściciela, często miejski bezdomny. |
| 165 | 野犬 | やけん | bezpański pies | `yaken` | `nouns` / animal | Dodane | 7 + few/many | Nie wymuszano interpretacji «zdziczały», możliwy szerszy sens. |

## B. Decyzje semantyczne i gramatyczne

1. **Osoby w liczbie mnogiej i zbiorowości.** `父兄`, `姉妹`, `両親`, `祖父母` oznaczają konkretne osoby, dlatego mają `person` i niezależne klasy polskiej liczby mnogiej. `家族`, `一族`, `民族`, `種族`, `兄弟` nadal mają `abstract` jako grupy lub rzeczownik zbiorowy, z ryzykiem niewykorzystania naturalnych ról dla grup.
2. **Liczba mnoga.** `父兄`, `姉妹`, `両親` i `祖父母` otrzymały poprawne polskie realizacje liczby mnogiej oraz stosowną klasę `plural_masculine_personal` albo `plural_non_masculine_personal`. Nie wstawiono im fikcyjnej liczby pojedynczej ani profilów liczenia. `兄弟` ma polski zbiorowy rzeczownik `rodzeństwo`, a nie obowiązkowe `bracia`.
3. **Kategoria cielesna.** `親指` ma `body_part`, selekcjonowalne dziecko `concrete`, dodane deklaratywnie na branchu Kotomi. Nie dziedziczy po `purchasable` ani `thing`. Licznik `long_object` odpowiada 本 dla palców. Kategoria jest dostępna tylko w wersji Kotomi zawierającej nową gramatykę.
4. **Czasownik.** `主張する` jest czasownikiem `irregular` typu suru. Ma naturalny `subject` z kategorią `person`; nie otrzymał wymuszonego dopełnienia `accepts="*"`. Istniejący wzorzec `Cytowana opinia` obsługuje cytowane twierdzenia przez cechę `reporting`, dlatego dodano ją bez zmian silnika. Obsługa dowolnego zdania podrzędnego pozostaje osobnym zagadnieniem. W tym wpisie są 17 form japońskich i realizacje uzgodnienia dla 11 form, w siedmiu klasach.
5. **Rozdzielenie homografów i znaczeń.** `主人` ma oddzielne wpisy `shujin_husband` i `shujin_owner`, ponieważ polskie `mąż` oraz `właściciel` nie są gramatycznie równoważnymi synonimami w każdym zdaniu. Lekcja zawiera jedno źródłowe hasło i referuje pierwsze znaczenie. Odrębny właściciel pozostaje w słowniku na przyszłość.
6. **Pragmatyka japońska.** `兄`/`お兄さん` oraz `姉`/`お姉さん` różnią się honoryfikatywnością i odniesieniem do własnej/cudzej rodziny. Polskie tłumaczenia mogą być identyczne, co wymaga ostrożności w quizach. Nie dodano sztucznych wyrażeń do tłumaczeń wyłącznie w celu eliminacji kolizji.
7. **Znaczenia z materiałów.** `民族` opisuje wspólnotę etniczną, nie biologiczną rasę; użyto `grupa etniczna`. `野犬` i `野良犬` mogą oznaczać psa bez właściciela. Potoczna różnica dzikości nie została narzucona jako obligatoryjna. `父兄` w kontekście szkolnym jest tradycyjną nazwą opiekunów, częściej zastępowaną współcześnie przez `保護者`.
8. **Liczenie.** Profile `few` i `many` dodano tam, gdzie istnieje naturalny sposób policzenia danego referenta. Nie dopisano `general_item` zbiorowościom lub wyrażeniom masowym wyłącznie dla pokrycia walidacji.
9. **Przymiotniki.** `親しい` ma 15 naturalnych form japońskich i polską odmianę przez wszystkie obsługiwane klasy. `主要` ma 11 użytecznych form i selektywny zakres `describes`: `abstract person place`; obejmuje ważne osoby, budynki i kraje bez całego `concrete`, pominięto mechanicznie możliwe, lecz w zwykłym użyciu nienaturalne `主要さ`, `主要そう`, `主要すぎる`, `主要に`. Każda część `polish_forms` obejmuje wszystkie przypadki i klasy, nie polega na kopiowaniu formy męskiej.
10. **Regresja `姉`.** Zachowano istniejące ID `sister`, klasę `feminine`, kategorię `person` i licznik `person`. Zmieniono tylko tłumaczenie oraz realizacje przypadków i `few/many` na `starsza siostra`. Ta zmiana jest semantycznie uzasadniona, lecz nie było możliwości uruchomienia pełnych poprzednich quizów.

## C. Nieobsługiwane możliwości i decyzje blokujące

| Hasło / problem | Oczekiwanie | Ograniczenie | Wpływ | Kierunek rozwiązania | Wymaga Kotomi? |
|---|---|---|---|---|---|
| `私` | Zaimek ja z realizacjami ja/mnie/mi/mną i alternatywnymi odczytami | Brak odpowiedniego słownika osobowych zaimków oraz ich kontraktu w generatorze; `nouns/person` sugerowałby policzalną osobę | Brak referencji w lekcji 156–160 | Osobny schemat i integracja zaimków osobowych oraz wariantów odczytu | Tak |
| `私立` | Przedrzeczownikowe `私立の学校`, znaczenie prywatny | Aktualne `na_adjective` wytwarza `〜な`, nie `〜の` | Brak referencji w lekcji 156–160 | Kategoria `no_adjective` lub składnia `noun+の` obsługiwana w lekcji i wzorcach | Tak |
| `主な` | Przydawka główny z odczytem おもな | Wyłącznie przydawkowe użycie, nie pełny paradygmat na-adjective | Brak referencji w lekcji 161–165 | Typ 連体詞/prenominal albo opcjonalne formy ograniczone do przydawkowych | Tak |
| `主要な` | Pokazanie w lekcji dokładnie `主要な` | `dictionary_ref` identyfikuje tylko słownik i słowo, bez wyboru formy `attributive_nonpast` | Przymiotnik zapisany poprawnie w słowniku jako `主要`, lecz pominięty w lekcji, aby nie fałszować zapisu | Opcjonalny `form_ref` na poziomie referencji lekcji | Tak |
| `主張する` | `〜と主張する` dla twierdzenia | Istniejący wzorzec `Cytowana opinia` używa `reporting` | Możliwe bez nowego DSL w zakresie tego wzorca | Dodano `reporting`, wymagane uruchomienie podglądu i quizów | Nie dla istniejącego wzorca; tak dla pełnej obsługi dowolnego zdania podrzędnego |
| Grupy rodzinne | Predykaty poprawne dla rodziny i członków grupy z odrębnymi zgodnościami | Brak kategorii zbiorowości ludzi | Konserwatywne filtrowanie może odrzucić naturalne zdania | Semantyczna kategoria kolektywna i jasne relacje z `person` | Tak |
| Synonimy | Wyróżnianie 兄 / お兄さん, 祖先 / 先祖, 野良犬 / 野犬 | Jeden polski odpowiednik nie odróżnia wariantów kontekstowych | Ryzyko niejednoznacznych odpowiedzi | Weryfikacja wariantowych odpowiedzi w quizach, ewentualnie metadane pragmatyczne | Możliwe |

Nie dodawano obejść przez `expressions`, sztucznych `local_word`, nieprawidłowe kategorie ani zmiany istniejących wzorców.

## D. Lekcje i zgodność z PDF

- `ola_kanji_156_160`, 10 referencji; źródło 12 haseł, brakuje `私` i `私立`.
- `ola_kanji_161_165`, 25 referencji; źródło 27 haseł, brakuje `主な` i `主要な` (ostatnie dostępne już w słowniku).
- Wszystkie dodane referencje używają wyłącznie `<dictionary_ref dictionary="..." word="..." />`, bez `local_word`.
- Kolejność odpowiada kolejności bloków kanji i haseł w źródłowych PDF: w każdym bloku kolumna lewa z góry na dół, następnie prawa.

## E. Wyniki walidacji i status

**Wykonane:** odczyt aktualnych plików `main` obu repozytoriów, porównanie dokładnej pary kanji/kana z istniejącymi wpisami; statyczna kontrola zagnieżdżenia tagów w czterech zmodyfikowanych plikach XML; kontrola unikatowości identyfikatorów; kontrola obecności siedmiu przypadków w nowych lub aktualizowanych rzeczownikach; kontrola obecności `polish_forms`; sprawdzenie rozwiązywania wszystkich 35 referencji w nowych lekcjach. Pozytywny wynik tych kontroli nie zastępuje pełnego parsera ani walidatora aplikacji.

**Niewykonane:** `python tools/validate_repository.py`, pełna walidacja schematów w Kotomi, uruchomienie rzeczywistych wzorców, porównanie wieloznacznych odpowiedzi quizowych i pomiar czasu startu quizów. Dostępny konektor GitHub pozwala czytać i publikować pliki, ale nie zapewnia lokalnego uruchomienia kodu z repozytorium; środowisko wykonawcze nie ma dostępu sieciowego do klonowania repozytoriów.

**Wpływ na produkcję:** zmiana istniejącego `sister` wymaga regresji integracyjnej. Niejednoznaczności synonimów oraz cztery brakujące referencje lekcji pozostają otwarte. Nie wprowadzono nowych testów Kotomi, w szczególności testów odczytujących produkcyjne dane.

**Ocena gotowości:** **PARTIAL, NIEGOTOWE DO MERGE**. `oyayubi` ma poprawną kategorię przy użyciu uzupełnionej gramatyki na branchu Kotomi. Pozostają cztery pozycje lekcyjne bez wiernego odwzorowania i niewykonane pełne testy integracyjne. Nie wykonuj merge automatycznie.

## F. Referencje zewnętrzne

- [私立, Kotobank](https://kotobank.jp/word/%E7%A7%81%E7%AB%8B-535814): rzeczownik i użycie `〜の`.
- [主要, Kotobank](https://kotobank.jp/word/%E4%B8%BB%E8%A6%81-529415): rzeczownik i przymiotnik typu na.
- [父兄, Kotobank](https://kotobank.jp/word/%E7%88%B6%E5%85%84-617681): opiekunowie szkolni.
- [野犬, Kotobank](https://kotobank.jp/word/%E9%87%8E%E7%8A%AC-596137): podstawowe znaczenie oraz różnice użycia.

## G. Poprawki po code review (2026-10-28)

| Punkt | Wynik |
|---|---|
| F-01, `sister` | Zachowano poprawną semantykę „starsza siostra” oraz zaktualizowano 6 jawnych oczekiwań w `validate_target_c32.py` i `validate_relative_lesson26.py`. Nie zmieniano istniejących wzorców ani Kotomi. |
| F-02, 39 pozycji | Potwierdzono 35 odwołań w lekcjach. `私`, `私立`, `主な` wymagają dokładniejszego kontraktu reprezentacji; `主要な` już istnieje jako forma `attributive_nonpast` hasła `shuyou`, lecz lekcja nie wskazuje formy. Nie dodano fikcyjnych wpisów. |
| F-03, `oyayubi` | Dodano `body_part` jako selekcjonowalne dziecko `concrete` w deklaratywnej gramatyce Kotomi. Uwaga na zależność wersji aplikacji. |
| F-04, `shuchousuru` | Wykorzystano istniejące `reporting` we wzorcu `Cytowana opinia`. Nie utworzono nowego wzorca. |
| F-05, `shuyou` | Ustawiono `abstract person place`. Dzięki temu `body_part` i `animal` nie pasują, a `building` i `country` pasują. `weekday`, dziedziczący po `abstract`, pozostaje niepożądanym dopasowaniem. |
| F-06, `inugoya`, `shitashii` | „Budy dla psów” jest naturalnym wariantem mnogości. `shitashii` pozostawiono przy `person`: `親しい関係` jest naturalne, lecz dołączenie całego `abstract` bez precyzyjnej kategorii byłoby zbyt szerokie. |
| Dodatkowo, `fukei` | Przywrócono `person`; liczba mnoga nie decyduje o semantycznej kategorii. Podobnie indywidualnie oceniono `ryoushin`, `sofubo`, `shimai` i ustawiono `person`. |

**Kontrole statyczne:** potwierdzono komplet siedmiu przypadków w 122 rzeczownikach, 35 referencji w dwóch lekcjach, istnienie `reporting` w gramatyce Kotomi i wzorcu `Cytowana opinia`. Sprawdzono zgodność SHA-256 zmodyfikowanych plików z aktualizowanym manifestem.

**Niewykonane:** pełna walidacja `tools/validate_repository.py`, `unittest discover`, `validate_question_patterns.py` i uruchomienie wzorców na aktualnym Kotomi. Dostęp z GitHub pozwala odczytywać i publikować pliki, ale nie uruchamiać skryptów na repozytorium. Brak uruchomionych testów nie jest pozytywnym wynikiem.

**Rewizja Content:** nadal `70`, bez zmian `quiz_update_manifest.json`.

## H. Przegląd semantyki, kompatybilności i pozostałych testów

### body_part: wybór rodzica

Wariant A, body_part pod concrete (wybrany): poprzez dziedziczenie zapewnia kategoriom części ciała naturalne powiązania z rolami sawaru (dotykać) oraz mieru (być widocznym), a także z kolorem akai. Nie dziedziczy person, animal, purchasable ani thing. Dopuszcza jednak ogólne ograniczenia concrete, w tym czasami nietrafne kolokacje z przymiotnikami ceny. Wariant B, niezależny body_part, nie daje tych nadmiarowych dopasowań, ale eliminuje również naturalne sawaru, mieru, akai. Istniejąca implementacja effective_entity_categories, role_matches i adjective_matches używa przodków kategorii, więc wybrano wariant A bez modyfikacji Pythona.

Kontrola reguł kategorii (nie pełnego generowania): sawaru + oyayubi oraz akai + oyayubi są dopuszczone, kupowanie przez kau + oyayubi nie jest dopuszczone na podstawie kategorii purchasable. Kategoria body_part jest dostępna w Studio z selekcjonowalnego katalogu. Dodano izolowane testy zachowania kategorii i zapis/odczyt przez Studio na branchu Kotomi. Nie były wykonywane w środowisku tego przeglądu.

### Osoby mnogie i zbiorowości

Indywidualnie oceniono fukei, ryoushin, sofubo i shimai: oznaczają faktyczne osoby, więc semantyczne person jest właściwe. Ich klasy uzgodnienia pozostają odpowiednio plural_masculine_personal (fukei, ryoushin, sofubo) oraz plural_non_masculine_personal (shimai). Pozwala to m.in. na role podmiotowe iku i hanasu, jak również na spotykanie przez au. Przed zmianą abstract takie role były wykluczane. Nie dodawano sztucznej liczby pojedynczej.

Kyoudai oznacza w polskich danych rodzeństwo, rzeczownik zbiorowy w liczbie pojedynczej. Kazoku, ichizoku, minzoku i shuzoku oznaczają grupy społeczne, pozostają abstract. Kategoria group_of_people sama nie rozwiązałaby problemu: jeśli nie dziedziczy person, wykluczy naturalne czasowniki, a jeśli dziedziczy person, nadal dopuszcza jednostkowe wzorce pytające o wiek. Pozostaje potrzeba osobnego kontraktu semantycznej liczebności, bez zmian silnika w tym zadaniu.

### shuyou, shitashii i inugoya

Shuyou teraz dopuszcza abstract, person, place. Przykłady na podstawie istniejących danych: hito (person), school (building) i japan (country) są objęte, podobnie jak shugo (abstract). Odrzucane są oyayubi (body_part) i koinu (animal). Pozostaje znana luka: poniedziałek getsuyoubi dziedziczy po abstract przez weekday, więc może być dopasowany. Pełne naturalne znaczenie główny nie może być zdefiniowane tylko tym jednym zestawem kategorii.

Shitashii pozostaje przy person. W wyrażeniu 親しい関係 przymiotnik opisuje relację, ale obecna klasa abstract obejmuje także dzień, powód i obietnicę. W aktualnej bazie brak kategorii relacji i takiego rzeczownika jak kankei. Rozszerzenie do całego abstract byłoby błędem. Inugoya pozostaje z formami budy dla psów jako naturalnym odniesieniem do rodzaju bud przeznaczonych dla psów. Sama liczba bud nie dowodzi liczby posiadanych psów, a budy dla psa też byłyby uzasadnione w innym kontekście. Zmiana form bez rozstrzygnięcia znaczenia byłaby arbitralna.

### reporting i regresja sister

Shuchousuru posiada istniejącą cechę reporting, a wzorzec Cytowana opinia filtruje feature:reporting. Odpowiednie formy dictionary, past_plain i plain_negative istnieją. Test wykonania podglądu i quizu jest nadal wymagany. Wcześniejsze poprawki sześciu jawnych oczekiwań dla sister w dwóch skryptach integracyjnych pozostają na branchu. Syntetyczny lub ręczny podgląd powinien potwierdzić ich wyniki.

### Pozostałe 4 z 39 pozycji lekcji

Zweryfikowano kotomi/core/lessons/io.py: load_catalog czyta z dictionary_ref tylko dictionary i word, a save_catalog zapisuje tylko te atrybuty. Nie istnieje wybór formy słownika dla referencji lekcji. Dlatego 主要な jest w słowniku formą attributive_nonpast hasła shuyou, lecz w lekcji bez rozszerzenia kontraktu wystąpiłaby podstawowa 主要. 私 jest zaimkiem osobowym, 私立 wymaga の, a 主な jest wyłącznie przydawkowe. Wymuszenie na-adjective lub local_word zniekształciłoby dane. Obecnie pozostaje 35 poprawnych referencji z 39 pozycji. Wymagany osobny projekt rozszerzenia kontraktu, bez zmian DSL i parsera w tym zadaniu.

### Publikacja i wersje

quiz_project.xml ustawia min_kotomi_version na 1.8.0, ale main Kotomi w chwili analizy ma wersję 1.1.4. Funkcja check_content_manifest sprawdza schema_version, a aktualizator Content kieruje się rewizją i hashami. Nie stwierdzono egzekwowania min_kotomi_version przy aktualizacji. Starsze Kotomi może odrzucić Content z body_part. Bezpieczna kolejność: najpierw wersja Kotomi z nowym katalogiem, dopiero potem rewizja 70 danych, pod warunkiem potwierdzenia, że na starszych klientach aktualizacja nowych danych jest wstrzymana. Nie implementowano nowego mechanizmu aktualizacji bez zgody.

### Status weryfikacji

Statycznie: sprawdzono zmienione wpisy, dziedziczenie semantyczne, klasy uzgodnienia, brak zmiany liczby wpisów, pokrycie lekcji, obecność reporting, aktualizację SHA-256 manifestu Content. Po stronie Kotomi przygotowano testy kategorii z syntetycznymi fixture, w tym Studio. Nie wykonano: pytest, python tools/validate_repository.py, python -m unittest discover -s tests -v, python tools/validate_question_patterns.py, QuizProject.validate(), podglądu Cytowana opinia, scenariuszy integracyjnych sister ani uruchomienia CI. Kod GitHub jest dostępny do odczytu i commitu, ale lokalny runtime nie może pobrać repozytoriów. Przejście kontroli statycznych nie jest równoznaczne z przejściem testów.

**Ocena: PARTIAL, bez PR i merge.** Przed udostępnieniem Content wymagane są kontrolowane testy rzeczywistego silnika i zabezpieczenie starszych aplikacji.
