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
| `hairu` | `do_genitive` | wnętrze; do + dopełniacz; tylko enclosed_space |
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

`kayou` zachowuje `education_facility sports_facility`. Nowa szkoła lub sala odpowiedniej kategorii jest dostępna bez edycji czasownika. Zwykły `building` nie jest miejscem regularnego uczęszczania. `kariru` i `kasu` zachowują `person`; zwierzę nie staje się pożyczkodawcą.

`hairu` wybiera `enclosed_space`, nową kategorię semantyczną pod `place`. `building` dziedziczy po niej; kuchnia (`daidokoro`), pokój (`room`) i biuro (`jimusitsu`) otrzymują tę kategorię. Dotychczasowe dopasowania do `place` i `concrete` zostają zachowane. Rola hairu traci pięć par: kaigan, park, bazaaru, naka, oku. Park i bazar mogą występować z hairu w innych sensach, ale polskie „na” i kontekst przekraczania granicy wymagają osobnej analizy. `naka`/`oku` to relacyjne pojęcia wymagające uzupełnienia. Kategoria nie jest listą dozwolonych ID. Nowe pomieszczenia dziedziczą dopasowanie.

Nie zmieniono pozostałych `accepts` ani list `nouns`. Dawne wyjątki ireru, kotaeru i teishutsusuru pozostają bez zmian i bez dopuszczenia do nowego wzorca. Nie rozszerzono kategorii globalnie, by wymusić ich obsługę.

## Tłumaczenie z jawnym argumentem

Opcjonalny `target_translation` jest atrybutem konkretnej formy:

```xml
<form ref="dictionary" kana="かりる" translation="pożyczam od kogoś"
      target_translation="pożyczam" />
```

Wybór korzysta z `analysis.driver_for_entity` i `role_for_entity`: tylko rzeczownik powiązany z rolą target tego samego czasownika aktywuje wariant. Jawne `government:@action` i automatyczne `government` zachowują się identycznie. Nie wystarczy target innego czasownika. Działa też target obok jawnego object. Nie jest potrzebne przeszukiwanie zdań ani nowy selektor DSL.

Brak wariantu zachowuje zwykłe tłumaczenie. Quiz samego czasownika nadal pokazuje „pożyczam od kogoś”. Wariant dodano tylko dla ośmiu form kariru, kasu i ageru_give. W Studio jest to edytowalna kolumna **Tłumaczenie z jawnym target (opcjonalne)** w tabeli form czasownika. Puste pole usuwa wariant; generowanie japońskich form zachowuje go. Po wyłączeniu języka źródłowego XML jest zachowywany jako nieaktywne rozszerzenie.

Wariant dotyczy zwykłego `.translation` wybranej formy. Nie zastępuje jawnego `translation:base` ani osobnego katalogu `agree` dla odmiany przez podmiot. Łączenie obu wariantów w przyszłej konstrukcji z jawnym podmiotem wymaga osobnego projektu, bez automatycznego obcinania tekstu.

## Przykłady i ograniczenia

| Polski | Japoński |
|---|---|
| uczęszczam do szkoły. | がっこうにかよう。 |
| uczęszczam do sali gimnastycznej. | たいいくかんにかよう。 |
| wchodzę do szkoły. | がっこうにはいる。 |
| pożyczam od siostry. | あねにかりる。 |
| pożyczam siostrze. | あねにかす。 |
| nie pożyczam od siostry. | あねにかりない。 |

Relacja rzeczownika `destination` może dawać „na salę gimnastyczną”, ale w tym wzorcu ramka kayou daje „do sali gimnastycznej”. Brak rozbudowy rekcji zależnej jednocześnie od typu rzeczownika i czasownika jest świadomą granicą tej wersji. Zdania transferu pomijają rzecz znaną z kontekstu; nie przedstawiają pełnego zdarzenia bez kontekstu. Tłumaczenia form przeszłych zachowują istniejącą męską pierwszą osobę.

## Publikacja i weryfikacja

Content 64 wymaga manifestu formatu 3. Format 2 pozostaje barierą dla rewizji 63, format 1 dla starszych danych. Nowy klient akceptuje wszystkie trzy; klient C3 odrzuca format 3 przed pobieraniem plików. Walidacja całego snapshotu, hashy i rollback pozostają bez zmian. Najpierw należy udostępnić kompatybilną aplikację. Nowa rewizja jest potrzebna z powodu pola formy, kategorii i wzorca.

Testy aplikacji używają niezależnych fixture v1: `test_universal_target.py`, `test_target_translation_persistence.py` i istniejących testów C3/C3.1. Produkcyjne przykłady i liczenie sprawdza osobny opt-in `tools/validate_target_c32.py --kotomi ../Kotomi`, poza zwykłymi testami. Raporty w `docs/validation` opisują dokładny zakres i pomiary. Historyczne raporty C3 pozostają dowodem tamtego etapu, nie aktualnym snapshotem C3.2.

Pomiary: 15 rund cold/warm, skala 1/10/50/200 po 21 rund. Odchylenie pojedynczej ścieżki potwierdzono w 7 naprzemiennych procesach po 301 próbek: +2,34%. Brak potwierdzonej regresji ponad 10%. Polecenia: `tools/benchmark_lesson_focus.py --rounds 15` oraz `tools/benchmark_target_c32.py --kotomi CHECKOUT --output report.json`. Protokół: `tools/updates/validate_content_compatibility_c32.py --kotomi CHECKOUT` (dla poprzedniego main dodaj `--legacy-c3`). Raporty akceptacji i wydajności są w Kotomi-Data: `docs/validation/target_c32_acceptance.json`, `target_c32_performance.json`.
