# Szymon / pierwsza: audyt materiału

Źródło: „Słówka z lekcji.docx”. Łącznie 58 pozycji, zachowano kolejność i pierwotny podział na materiał powtórkowy oraz nowy. Lekcja odwołuje się wyłącznie do istniejących lub uzupełnionych słowników, bez kopii `local_word`.

**15 pozycji już istniało**, **43 zostały dodane** (w tym słownikowy `住む` zamiast odrębnej pozycji `住んでいます`).

## Grupy

| Grupa | Liczba | Referencje |
|---|---:|---|
| Powtórka: pytajniki | 6 | `interrogatives/dare`, `interrogatives/donata`, `interrogatives/dono`, `interrogatives/nani`, `interrogatives/nan`, `interrogatives/dore` |
| Powtórka: zaimki wskazujące | 6 | `demonstratives/kore`, `demonstratives/sore`, `demonstratives/are`, `demonstratives/kono`, `demonstratives/sono`, `demonstratives/ano` |
| Powtórka: dni tygodnia | 7 | `nouns/getsuyoubi`, `nouns/kayoubi`, `nouns/suiyoubi`, `nouns/mokuyoubi`, `nouns/kinyoubi`, `nouns/doyoubi`, `nouns/nichiyoubi` |
| Powtórka: czas | 11 | `adverbs/mainichi`, `adverbs/asatte`, `adverbs/kinou`, `adverbs/kyou`, `nouns/ashita`, `adverbs/ototoi`, `adverbs/sensenshuu`, `adverbs/senshuu`, `adverbs/konshuu`, `adverbs/raishuu`, `adverbs/saraishuu` |
| Nowe: obiekty w mieście | 9 | `nouns/tatemono`, `nouns/yuubinkyoku`, `nouns/byouin`, `nouns/biru`, `nouns/jimusitsu`, `nouns/park`, `nouns/school`, `nouns/eigakan`, `nouns/ginkou` |
| Nowe: smaki | 7 | `nouns/aji`, `adjectives/oishii`, `adjectives/amai`, `adjectives/nigai`, `adjectives/karai`, `adjectives/suppai`, `adjectives/shoppai` |
| Nowe: słowa i zwroty | 12 | `verbs/sumu`, `nouns/programmer`, `adverbs/tokuni`, `adjectives/saikou`, `adjectives/saitei`, `expressions/shikata_ga_nai`, `expressions/shouganai`, `nouns/kikitori`, `nouns/shuumatsu`, `nouns/fukushuu`, `verbs/tsukau`, `nouns/madogiwazoku` |

## Istniejące (15)

- `interrogatives/dare`
- `interrogatives/donata`
- `interrogatives/dono`
- `interrogatives/nani`
- `interrogatives/nan`
- `interrogatives/dore`
- `nouns/ashita`
- `nouns/park`
- `nouns/school`
- `adjectives/oishii`
- `adjectives/amai`
- `adjectives/nigai`
- `adjectives/karai`
- `adjectives/suppai`
- `verbs/tsukau`

## Dodane (43)

- `demonstratives/kore`
- `demonstratives/sore`
- `demonstratives/are`
- `demonstratives/kono`
- `demonstratives/sono`
- `demonstratives/ano`
- `nouns/getsuyoubi`
- `nouns/kayoubi`
- `nouns/suiyoubi`
- `nouns/mokuyoubi`
- `nouns/kinyoubi`
- `nouns/doyoubi`
- `nouns/nichiyoubi`
- `adverbs/mainichi`
- `adverbs/asatte`
- `adverbs/kinou`
- `adverbs/kyou`
- `adverbs/ototoi`
- `adverbs/sensenshuu`
- `adverbs/senshuu`
- `adverbs/konshuu`
- `adverbs/raishuu`
- `adverbs/saraishuu`
- `nouns/tatemono`
- `nouns/yuubinkyoku`
- `nouns/byouin`
- `nouns/biru`
- `nouns/jimusitsu`
- `nouns/eigakan`
- `nouns/ginkou`
- `nouns/aji`
- `adjectives/shoppai`
- `verbs/sumu`
- `nouns/programmer`
- `adverbs/tokuni`
- `adjectives/saikou`
- `adjectives/saitei`
- `expressions/shikata_ga_nai`
- `expressions/shouganai`
- `nouns/kikitori`
- `nouns/shuumatsu`
- `nouns/fukushuu`
- `nouns/madogiwazoku`

## Co zostało uzupełnione i dlaczego

- **Rzeczowniki (20 nowych):** siedem dni tygodnia, siedem nowych lokalizacji/budynków, smak, programista, rozumienie ze słuchu, weekend, powtórka i 窓際族. Wszystkie mają siedem polskich przypadków w liczbie pojedynczej i klasę uzgodnienia. Dwanaście rzeczowników policzalnych ma przypisaną istniejącą klasę countera oraz siedem przypadków polskich w każdym profilu `few` i `many` (w formie `many` dla mianownika/biernika/wołacza uwzględniamy obowiązującą strategię ilościową Kotomi). Nie dodano sztucznego liczenia dni tygodnia i `聞き取り`.
- **Czasownik `住む`:** dodano 15 form (czasownik godan), między innymi `すんで` / `住んで`, `すみます` / `住みます`, przeszłe i przeczące, z tłumaczeniami. `住んでいます` powstaje w konstrukcji `～ています` zarządzanej przez patterny, bez osobnego wpisu w słowniku. `使う` było już obecne.
- **Przymiotniki (3 nowe):** `しょっぱい`, `最高`, `最低` mają po 15 form japońskich, kana, zapis pisany i polskie glosy. Dodano polskie uzgodnienia rodzaju, przypadka i liczby, bez nadpisywania haseł już obecnych.
- **Demonstratywy (6 nowych):** `これ`, `それ`, `あれ` otrzymały polskie przypadki, a `この`, `その`, `あの` dodatkowo polskie formy zależne od rodzaju i przypadku. W japońskim te wyrażenia są nieodmienne. Schemat `demonstrative` udostępnia token z `agree` i `case`; przypadki są zapisane we wspólnych wartościach `polish_forms`.
- **Czas (10 nowych):** `毎日`, `明後日`, `昨日`, `今日`, `一昨日`, `先々週`, `先週`, `今週`, `来週`, `再来週` w słowniku `adverbs`, współdzielone przez referencje z kontekstami. `明日` było już w `nouns/ashita` i zostało użyte ponownie.
- **Przysłówki i idiomy (3 nowe):** `特に` w `adverbs`, `仕方がない` i potoczne `しょうがない` w `expressions`, bez wymyślania ich odmiany.
- **Znaczenie idiomu:** `窓際族` jest potoczne i może być pejoratywne. Opis oznacza pracownika odsuniętego na boczny tor, a nie dosłowną „rodzinę przy oknie”.

Bez dodatkowego rozwijania patternów zdań ten PR udostępnia dane i lekcję referencyjną, nie zmienia semantyki istniejących konstrukcji.

`住む` ma rolę `target` ograniczoną do kategorii `place`, zgodnie z japońskim `場所に住む`. Nie przypisujemy mu `location`, ponieważ ta rola wybiera wzorce miejsca czynności z `で`. Forma `住んでいます` nadal powstaje z `te_form` i `いる`, bez osobnego hasła w słowniku.
