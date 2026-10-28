# Import kanji 156–165, raport językowy i techniczny

Data analizy: 2026-10-28. Materiały: *新漢字16-1（156–160）* i *新漢字16-2（161–165）*, po jednej stronie PDF; 10 kanji i 39 pozycji. Stan bazowy: Kotomi-Data main Content 69, Kotomi main na dzień analizy. Branch docelowy: `feature/kanji-16-vocabulary-156-165`. Bez zmian silnika, DSL, istniejących wzorców i bez PR.

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
| 160 | 姉妹 | しまい | siostry | `shimai` | `nouns` / abstract | Dodane | 7 (liczba mnoga) | Zbiorowa grupa żeńska, brak jednostkowego licznika. |
| 161 | 親 | おや | rodzic | `oya` | `nouns` / person | Dodane | 7 + few/many | Japoński rodzic nie wymusza płci, polski rodzic ma rodzaj gramatyczny. |
| 161 | 親指 | おやゆび | kciuk | `oyayubi` | `nouns` / concrete | Dodane | 7 + few/many | Brak kategorii «część ciała»; użyto szerokiego konkretu i licznika 本. |
| 161 | 親しい | したしい | bliski, dobrze znany | `shitashii` | `adjectives` / describes: person | Dodane | 15 japońskich + PL | Przymiotnik i, bliski relacyjnie, nie bez ograniczeń dla wszystkich rzeczy. |
| 161 | 両親 | りょうしん | rodzice | `ryoushin` | `nouns` / abstract | Dodane | 7 (liczba mnoga) | Zbiorowość rodziców, nie dowolna pojedyncza osoba. |
| 161 | 親友 | しんゆう | przyjaciel | `shinyuu` | `nouns` / person | Dodane | 7 + few/many | Bliski przyjaciel, nie każdy znajomy. |
| 161 | 肉親 | にくしん | krewny | `nikushin` | `nouns` / person | Dodane | 7 + few/many | Bliski krewny, nie ogólna grupa rodzinna. |
| 162 | 主 | あるじ | głowa rodu | `aruji` | `nouns` / person | Dodane | 7 + few/many | Sens gospodarz/pan domu; inne użycia kontekstowe. |
| 162 | 主な | おもな | główny | brak | nieobsługiwane | Wymaga decyzji | Brak | Funkcja wyłącznie przydawkowa, nie regularna odmiana na-adjective. |
| 162 | 主人 | しゅじん | mąż; właściciel; pan domu | `shujin_husband + shujin_owner` | `nouns` / person | Dodane (2 sensy) | 7 + few/many | Rozdzielono męża i właściciela. Lekcja referuje sens «mąż». |
| 162 | 主要な | しゅような | główny | `shuyou` | `adjectives` / describes: abstract concrete | Dodane, blokada lekcji | 11 japońskich + PL | Lemma 主要 jest poprawna, ale dictionary_ref nie wybiera 主要な. |
| 162 | 主語 | しゅご | podmiot | `shugo` | `nouns` / abstract | Dodane | 7 + few/many | Pojęcie gramatyczne, nie człowiek. |
| 162 | 主張する | しゅちょうする | twierdzić, upierać się | `shuchousuru` | `verbs` / subject: person | Dodane | 17 japońskich + uzgodnienia | Składnia zdań podrzędnych (〜と) nieobsługiwana przez proste role. |
| 163 | 祖父 | そふ | dziadek | `sofu` | `nouns` / person | Dodane | 7 + few/many | Wpis osobowy. |
| 163 | 祖母 | そぼ | babcia | `sobo` | `nouns` / person | Dodane | 7 + few/many | Wpis osobowy. |
| 163 | 祖父母 | そふぼ | dziadkowie | `sofubo` | `nouns` / abstract | Dodane | 7 (liczba mnoga) | Zbiorowa para/grupa dziadków. |
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

1. **Grupy osób kontra pojedynczy człowiek.** `家族`, `一族`, `民族`, `種族`, `兄弟`, `姉妹`, `両親` i `祖父母` zaklasyfikowano ostrożnie jako `abstract`, ponieważ nie istnieje właściwa kategoria `group_of_people`. Słowa opisujące jednostkowych krewnych mają kategorię `person`. Nie poszerzano kategorii tylko po to, by pasowały do wzorców.
2. **Liczba mnoga.** `父兄`, `姉妹`, `両親` i `祖父母` otrzymały poprawne polskie realizacje liczby mnogiej oraz stosowną klasę `plural_masculine_personal` albo `plural_non_masculine_personal`. Nie wstawiono im fikcyjnej liczby pojedynczej ani profilów liczenia. `兄弟` ma polski zbiorowy rzeczownik `rodzeństwo`, a nie obowiązkowe `bracia`.
3. **Kategoria cielesna.** `親指` nie mieści się w obecnym drzewie bez zniekształcenia jako przedmiot handlowy. Wpis używa `concrete`, a nie `thing` (poddrzewo `purchasable`). Licznik `long_object` odpowiada japońskiemu 本 dla palców. `concrete` jest obecnie nieselekcjonowalną kategorią ogólną, co ogranicza wygodę edycji i wymaga sprawdzenia zachowania UI.
4. **Czasownik.** `主張する` jest czasownikiem `irregular` typu suru. Ma naturalny `subject` z kategorią `person`; nie otrzymał wymuszonego dopełnienia `accepts="*"`. Ważne znaczenie składniowe `〜と主張する` ("twierdzić, że...") wymaga zdania podrzędnego i nie jest modelowane przez zwykłe `object`. W tym wpisie są 17 form japońskich i realizacje uzgodnienia dla 11 form, w siedmiu klasach.
5. **Rozdzielenie homografów i znaczeń.** `主人` ma oddzielne wpisy `shujin_husband` i `shujin_owner`, ponieważ polskie `mąż` oraz `właściciel` nie są gramatycznie równoważnymi synonimami w każdym zdaniu. Lekcja zawiera jedno źródłowe hasło i referuje pierwsze znaczenie. Odrębny właściciel pozostaje w słowniku na przyszłość.
6. **Pragmatyka japońska.** `兄`/`お兄さん` oraz `姉`/`お姉さん` różnią się honoryfikatywnością i odniesieniem do własnej/cudzej rodziny. Polskie tłumaczenia mogą być identyczne, co wymaga ostrożności w quizach. Nie dodano sztucznych wyrażeń do tłumaczeń wyłącznie w celu eliminacji kolizji.
7. **Znaczenia z materiałów.** `民族` opisuje wspólnotę etniczną, nie biologiczną rasę; użyto `grupa etniczna`. `野犬` i `野良犬` mogą oznaczać psa bez właściciela. Potoczna różnica dzikości nie została narzucona jako obligatoryjna. `父兄` w kontekście szkolnym jest tradycyjną nazwą opiekunów, częściej zastępowaną współcześnie przez `保護者`.
8. **Liczenie.** Profile `few` i `many` dodano tam, gdzie istnieje naturalny sposób policzenia danego referenta. Nie dopisano `general_item` zbiorowościom lub wyrażeniom masowym wyłącznie dla pokrycia walidacji.
9. **Przymiotniki.** `親しい` ma 15 naturalnych form japońskich i polską odmianę przez wszystkie obsługiwane klasy. `主要` ma 11 użytecznych form, pominięto mechanicznie możliwe, lecz w zwykłym użyciu nienaturalne `主要さ`, `主要そう`, `主要すぎる`, `主要に`. Każda część `polish_forms` obejmuje wszystkie przypadki i klasy, nie polega na kopiowaniu formy męskiej.
10. **Regresja `姉`.** Zachowano istniejące ID `sister`, klasę `feminine`, kategorię `person` i licznik `person`. Zmieniono tylko tłumaczenie oraz realizacje przypadków i `few/many` na `starsza siostra`. Ta zmiana jest semantycznie uzasadniona, lecz nie było możliwości uruchomienia pełnych poprzednich quizów.

## C. Nieobsługiwane możliwości i decyzje blokujące

| Hasło / problem | Oczekiwanie | Ograniczenie | Wpływ | Kierunek rozwiązania | Wymaga Kotomi? |
|---|---|---|---|---|---|
| `私` | Zaimek ja z realizacjami ja/mnie/mi/mną i alternatywnymi odczytami | Brak odpowiedniego słownika osobowych zaimków oraz ich kontraktu w generatorze; `nouns/person` sugerowałby policzalną osobę | Brak referencji w lekcji 156–160 | Osobny schemat i integracja zaimków osobowych oraz wariantów odczytu | Tak |
| `私立` | Przedrzeczownikowe `私立の学校`, znaczenie prywatny | Aktualne `na_adjective` wytwarza `〜な`, nie `〜の` | Brak referencji w lekcji 156–160 | Kategoria `no_adjective` lub składnia `noun+の` obsługiwana w lekcji i wzorcach | Tak |
| `主な` | Przydawka główny z odczytem おもな | Wyłącznie przydawkowe użycie, nie pełny paradygmat na-adjective | Brak referencji w lekcji 161–165 | Typ 連体詞/prenominal albo opcjonalne formy ograniczone do przydawkowych | Tak |
| `主要な` | Pokazanie w lekcji dokładnie `主要な` | `dictionary_ref` identyfikuje tylko słownik i słowo, bez wyboru formy `attributive_nonpast` | Przymiotnik zapisany poprawnie w słowniku jako `主要`, lecz pominięty w lekcji, aby nie fałszować zapisu | Opcjonalny `form_ref` na poziomie referencji lekcji | Tak |
| `主張する` | `X は Y と主張する` z pełnym zdaniem jako twierdzeniem | Zwykłe role rzeczownikowe nie reprezentują cytatu/zdania podrzędnego | Brak konstrukcji `twierdzi, że...` w nowych wzorcach | Osobny wzorzec i kontrakt zależności zdaniowych | Tak, oddzielna decyzja |
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

**Ocena gotowości:** **NIEGOTOWE DO MERGE** do momentu rozstrzygnięcia czterech braków lekcyjnych i wykonania pełnej walidacji. Nie wykonuj merge automatycznie.

## F. Referencje zewnętrzne

- [私立, Kotobank](https://kotobank.jp/word/%E7%A7%81%E7%AB%8B-535814): rzeczownik i użycie `〜の`.
- [主要, Kotobank](https://kotobank.jp/word/%E4%B8%BB%E8%A6%81-529415): rzeczownik i przymiotnik typu na.
- [父兄, Kotobank](https://kotobank.jp/word/%E7%88%B6%E5%85%84-617681): opiekunowie szkolni.
- [野犬, Kotobank](https://kotobank.jp/word/%E9%87%8E%E7%8A%AC-596137): podstawowe znaczenie oraz różnice użycia.
