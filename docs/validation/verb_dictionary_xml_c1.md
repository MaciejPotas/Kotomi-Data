# C1: dokładne fragmenty propozycji A

Nie jest to plik słownika ani polecenie wykonania C2. Fragmenty dodaje się do istniejących węzłów wskazanych ścieżką. Nie zastępują całego word/form ani istniejących atrybutów.

### aruku

Samodzielny ruch pieszy ma naturalnego wykonawcę; do C2 tylko ludzie, bo pies idzie pieszo jest stylistycznie nienaturalne.

```xml
<!-- aruku: append only to the indicated existing word/form. -->
<role ref="subject" nouns="friend mother sister teacher roujin hito programmer madogiwazoku" />
<!-- /dictionary/words/word[@id='aruku']/forms/form[@ref="dictionary"] -->
<agreement_translations>
  <translation class="masculine_personal" value="idzie pieszo" />
  <translation class="feminine" value="idzie pieszo" />
</agreement_translations>
<!-- /dictionary/words/word[@id='aruku']/forms/form[@ref="plain_negative"] -->
<agreement_translations>
  <translation class="masculine_personal" value="nie idzie pieszo" />
  <translation class="feminine" value="nie idzie pieszo" />
</agreement_translations>
<!-- /dictionary/words/word[@id='aruku']/forms/form[@ref="past_plain"] -->
<agreement_translations>
  <translation class="masculine_personal" value="szedł pieszo" />
  <translation class="feminine" value="szła pieszo" />
</agreement_translations>
<!-- /dictionary/words/word[@id='aruku']/forms/form[@ref="past_negative_plain"] -->
<agreement_translations>
  <translation class="masculine_personal" value="nie szedł pieszo" />
  <translation class="feminine" value="nie szła pieszo" />
</agreement_translations>
```

### asobu

Zabawa ludzi i zwierząt może wystąpić bez wskazania towarzysza. Zachować istniejącą rekcję towarzysza.

```xml
<!-- asobu: append only to the indicated existing word/form. -->
<role ref="subject" nouns="friend mother sister teacher roujin hito programmer madogiwazoku inu tori" />
<!-- /dictionary/words/word[@id='asobu']/forms/form[@ref="dictionary"] -->
<agreement_translations>
  <translation class="masculine_personal" value="bawi się" />
  <translation class="masculine_animate" value="bawi się" />
  <translation class="feminine" value="bawi się" />
</agreement_translations>
<!-- /dictionary/words/word[@id='asobu']/forms/form[@ref="plain_negative"] -->
<agreement_translations>
  <translation class="masculine_personal" value="nie bawi się" />
  <translation class="masculine_animate" value="nie bawi się" />
  <translation class="feminine" value="nie bawi się" />
</agreement_translations>
<!-- /dictionary/words/word[@id='asobu']/forms/form[@ref="past_plain"] -->
<agreement_translations>
  <translation class="masculine_personal" value="bawił się" />
  <translation class="masculine_animate" value="bawił się" />
  <translation class="feminine" value="bawiła się" />
</agreement_translations>
<!-- /dictionary/words/word[@id='asobu']/forms/form[@ref="past_negative_plain"] -->
<agreement_translations>
  <translation class="masculine_personal" value="nie bawił się" />
  <translation class="masculine_animate" value="nie bawił się" />
  <translation class="feminine" value="nie bawiła się" />
</agreement_translations>
```

### ayamaru

Osoba może przepraszać bez jawnego adresata; target pozostaje niezależną rolą, bez poszerzania jej obecnej listy.

```xml
<!-- ayamaru: append only to the indicated existing word/form. -->
<role ref="subject" nouns="friend mother sister teacher roujin hito programmer madogiwazoku" />
<!-- /dictionary/words/word[@id='ayamaru']/forms/form[@ref="dictionary"] -->
<agreement_translations>
  <translation class="masculine_personal" value="przeprasza" />
  <translation class="feminine" value="przeprasza" />
</agreement_translations>
<!-- /dictionary/words/word[@id='ayamaru']/forms/form[@ref="plain_negative"] -->
<agreement_translations>
  <translation class="masculine_personal" value="nie przeprasza" />
  <translation class="feminine" value="nie przeprasza" />
</agreement_translations>
<!-- /dictionary/words/word[@id='ayamaru']/forms/form[@ref="past_plain"] -->
<agreement_translations>
  <translation class="masculine_personal" value="przeprosił" />
  <translation class="feminine" value="przeprosiła" />
</agreement_translations>
<!-- /dictionary/words/word[@id='ayamaru']/forms/form[@ref="past_negative_plain"] -->
<agreement_translations>
  <translation class="masculine_personal" value="nie przeprosił" />
  <translation class="feminine" value="nie przeprosiła" />
</agreement_translations>
```

### deru

Ludzie i zwierzęta mogą wychodzić bez jawnego miejsca wyjścia. Zachować route; nie rozszerzać na publikacje i pojazdy w tym znaczeniu.

```xml
<!-- deru: append only to the indicated existing word/form. -->
<role ref="subject" nouns="friend mother sister teacher roujin hito programmer madogiwazoku inu tori" />
<!-- /dictionary/words/word[@id='deru']/forms/form[@ref="dictionary"] -->
<agreement_translations>
  <translation class="masculine_personal" value="wychodzi" />
  <translation class="masculine_animate" value="wychodzi" />
  <translation class="feminine" value="wychodzi" />
</agreement_translations>
<!-- /dictionary/words/word[@id='deru']/forms/form[@ref="plain_negative"] -->
<agreement_translations>
  <translation class="masculine_personal" value="nie wychodzi" />
  <translation class="masculine_animate" value="nie wychodzi" />
  <translation class="feminine" value="nie wychodzi" />
</agreement_translations>
<!-- /dictionary/words/word[@id='deru']/forms/form[@ref="past_plain"] -->
<agreement_translations>
  <translation class="masculine_personal" value="wyszedł" />
  <translation class="masculine_animate" value="wyszedł" />
  <translation class="feminine" value="wyszła" />
</agreement_translations>
<!-- /dictionary/words/word[@id='deru']/forms/form[@ref="past_negative_plain"] -->
<agreement_translations>
  <translation class="masculine_personal" value="nie wyszedł" />
  <translation class="masculine_animate" value="nie wyszedł" />
  <translation class="feminine" value="nie wyszła" />
</agreement_translations>
```

### hairu

Wchodzenie ludzi i zwierząt jest naturalne bez jawnego celu w krótkiej przydawce. Zachować target=place.

```xml
<!-- hairu: append only to the indicated existing word/form. -->
<role ref="subject" nouns="friend mother sister teacher roujin hito programmer madogiwazoku inu tori" />
<!-- /dictionary/words/word[@id='hairu']/forms/form[@ref="dictionary"] -->
<agreement_translations>
  <translation class="masculine_personal" value="wchodzi" />
  <translation class="masculine_animate" value="wchodzi" />
  <translation class="feminine" value="wchodzi" />
</agreement_translations>
<!-- /dictionary/words/word[@id='hairu']/forms/form[@ref="plain_negative"] -->
<agreement_translations>
  <translation class="masculine_personal" value="nie wchodzi" />
  <translation class="masculine_animate" value="nie wchodzi" />
  <translation class="feminine" value="nie wchodzi" />
</agreement_translations>
<!-- /dictionary/words/word[@id='hairu']/forms/form[@ref="past_plain"] -->
<agreement_translations>
  <translation class="masculine_personal" value="wszedł" />
  <translation class="masculine_animate" value="wszedł" />
  <translation class="feminine" value="weszła" />
</agreement_translations>
<!-- /dictionary/words/word[@id='hairu']/forms/form[@ref="past_negative_plain"] -->
<agreement_translations>
  <translation class="masculine_personal" value="nie wszedł" />
  <translation class="masculine_animate" value="nie wszedł" />
  <translation class="feminine" value="nie weszła" />
</agreement_translations>
```

### hanasu

Rozmawia może opisywać osobę bez jawnego partnera. Nie rozszerzać na zwierzęta ani zastępować tego automatycznie znaczeniem opowiadać o czymś.

```xml
<!-- hanasu: append only to the indicated existing word/form. -->
<role ref="subject" nouns="friend mother sister teacher roujin hito programmer madogiwazoku" />
<!-- /dictionary/words/word[@id='hanasu']/forms/form[@ref="dictionary"] -->
<agreement_translations>
  <translation class="masculine_personal" value="rozmawia" />
  <translation class="feminine" value="rozmawia" />
</agreement_translations>
<!-- /dictionary/words/word[@id='hanasu']/forms/form[@ref="plain_negative"] -->
<agreement_translations>
  <translation class="masculine_personal" value="nie rozmawia" />
  <translation class="feminine" value="nie rozmawia" />
</agreement_translations>
<!-- /dictionary/words/word[@id='hanasu']/forms/form[@ref="past_plain"] -->
<agreement_translations>
  <translation class="masculine_personal" value="rozmawiał" />
  <translation class="feminine" value="rozmawiała" />
</agreement_translations>
<!-- /dictionary/words/word[@id='hanasu']/forms/form[@ref="past_negative_plain"] -->
<agreement_translations>
  <translation class="masculine_personal" value="nie rozmawiał" />
  <translation class="feminine" value="nie rozmawiała" />
</agreement_translations>
```

### harau

Samodzielne płaci/zapłacił jest naturalne; zachować object=okane. Nie zmieniać znaczenia na usuwać/strzepywać.

```xml
<!-- harau: append only to the indicated existing word/form. -->
<role ref="subject" nouns="friend mother sister teacher roujin hito programmer madogiwazoku" />
<!-- /dictionary/words/word[@id='harau']/forms/form[@ref="dictionary"] -->
<agreement_translations>
  <translation class="masculine_personal" value="płaci" />
  <translation class="feminine" value="płaci" />
</agreement_translations>
<!-- /dictionary/words/word[@id='harau']/forms/form[@ref="plain_negative"] -->
<agreement_translations>
  <translation class="masculine_personal" value="nie płaci" />
  <translation class="feminine" value="nie płaci" />
</agreement_translations>
<!-- /dictionary/words/word[@id='harau']/forms/form[@ref="past_plain"] -->
<agreement_translations>
  <translation class="masculine_personal" value="zapłacił" />
  <translation class="feminine" value="zapłaciła" />
</agreement_translations>
<!-- /dictionary/words/word[@id='harau']/forms/form[@ref="past_negative_plain"] -->
<agreement_translations>
  <translation class="masculine_personal" value="nie zapłacił" />
  <translation class="feminine" value="nie zapłaciła" />
</agreement_translations>
```

### hashiru

Bieg ludzi i zwierząt jest samodzielną czynnością. Pojazdy i programy pominięte, bo wymagałyby innego polskiego znaczenia.

```xml
<!-- hashiru: append only to the indicated existing word/form. -->
<role ref="subject" nouns="friend mother sister teacher roujin hito programmer madogiwazoku inu tori" />
<!-- /dictionary/words/word[@id='hashiru']/forms/form[@ref="dictionary"] -->
<agreement_translations>
  <translation class="masculine_personal" value="biegnie" />
  <translation class="masculine_animate" value="biegnie" />
  <translation class="feminine" value="biegnie" />
</agreement_translations>
<!-- /dictionary/words/word[@id='hashiru']/forms/form[@ref="plain_negative"] -->
<agreement_translations>
  <translation class="masculine_personal" value="nie biegnie" />
  <translation class="masculine_animate" value="nie biegnie" />
  <translation class="feminine" value="nie biegnie" />
</agreement_translations>
<!-- /dictionary/words/word[@id='hashiru']/forms/form[@ref="past_plain"] -->
<agreement_translations>
  <translation class="masculine_personal" value="biegł" />
  <translation class="masculine_animate" value="biegł" />
  <translation class="feminine" value="biegła" />
</agreement_translations>
<!-- /dictionary/words/word[@id='hashiru']/forms/form[@ref="past_negative_plain"] -->
<agreement_translations>
  <translation class="masculine_personal" value="nie biegł" />
  <translation class="masculine_animate" value="nie biegł" />
  <translation class="feminine" value="nie biegła" />
</agreement_translations>
```

### iku

Idzie/poszedł z żywym wykonawcą jest naturalne. いって/いった są wyjątkami; ている oznacza często stan po odejściu, nie po prostu idzie.

```xml
<!-- iku: append only to the indicated existing word/form. -->
<role ref="subject" nouns="friend mother sister teacher roujin hito programmer madogiwazoku inu tori" />
<!-- /dictionary/words/word[@id='iku']/forms/form[@ref="dictionary"] -->
<agreement_translations>
  <translation class="masculine_personal" value="idzie" />
  <translation class="masculine_animate" value="idzie" />
  <translation class="feminine" value="idzie" />
</agreement_translations>
<!-- /dictionary/words/word[@id='iku']/forms/form[@ref="plain_negative"] -->
<agreement_translations>
  <translation class="masculine_personal" value="nie idzie" />
  <translation class="masculine_animate" value="nie idzie" />
  <translation class="feminine" value="nie idzie" />
</agreement_translations>
<!-- /dictionary/words/word[@id='iku']/forms/form[@ref="past_plain"] -->
<agreement_translations>
  <translation class="masculine_personal" value="poszedł" />
  <translation class="masculine_animate" value="poszedł" />
  <translation class="feminine" value="poszła" />
</agreement_translations>
<!-- /dictionary/words/word[@id='iku']/forms/form[@ref="past_negative_plain"] -->
<agreement_translations>
  <translation class="masculine_personal" value="nie poszedł" />
  <translation class="masculine_animate" value="nie poszedł" />
  <translation class="feminine" value="nie poszła" />
</agreement_translations>
```

### isogu

Samodzielna czynność osoby; zachować zaakceptowaną pisownię śpieszyć, bez kosmetycznej zmiany na spieszyć.

```xml
<!-- isogu: append only to the indicated existing word/form. -->
<role ref="subject" nouns="friend mother sister teacher roujin hito programmer madogiwazoku" />
<!-- /dictionary/words/word[@id='isogu']/forms/form[@ref="dictionary"] -->
<agreement_translations>
  <translation class="masculine_personal" value="śpieszy się" />
  <translation class="feminine" value="śpieszy się" />
</agreement_translations>
<!-- /dictionary/words/word[@id='isogu']/forms/form[@ref="plain_negative"] -->
<agreement_translations>
  <translation class="masculine_personal" value="nie śpieszy się" />
  <translation class="feminine" value="nie śpieszy się" />
</agreement_translations>
<!-- /dictionary/words/word[@id='isogu']/forms/form[@ref="past_plain"] -->
<agreement_translations>
  <translation class="masculine_personal" value="śpieszył się" />
  <translation class="feminine" value="śpieszyła się" />
</agreement_translations>
<!-- /dictionary/words/word[@id='isogu']/forms/form[@ref="past_negative_plain"] -->
<agreement_translations>
  <translation class="masculine_personal" value="nie śpieszył się" />
  <translation class="feminine" value="nie śpieszyła się" />
</agreement_translations>
```

### kaeru

Powrót żywego wykonawcy można opisać bez jawnego celu. Nie zmieniać na ogólne zmieniać, które jest innym czasownikiem.

```xml
<!-- kaeru: append only to the indicated existing word/form. -->
<role ref="subject" nouns="friend mother sister teacher roujin hito programmer madogiwazoku inu tori" />
<!-- /dictionary/words/word[@id='kaeru']/forms/form[@ref="dictionary"] -->
<agreement_translations>
  <translation class="masculine_personal" value="wraca" />
  <translation class="masculine_animate" value="wraca" />
  <translation class="feminine" value="wraca" />
</agreement_translations>
<!-- /dictionary/words/word[@id='kaeru']/forms/form[@ref="plain_negative"] -->
<agreement_translations>
  <translation class="masculine_personal" value="nie wraca" />
  <translation class="masculine_animate" value="nie wraca" />
  <translation class="feminine" value="nie wraca" />
</agreement_translations>
<!-- /dictionary/words/word[@id='kaeru']/forms/form[@ref="past_plain"] -->
<agreement_translations>
  <translation class="masculine_personal" value="wrócił" />
  <translation class="masculine_animate" value="wrócił" />
  <translation class="feminine" value="wróciła" />
</agreement_translations>
<!-- /dictionary/words/word[@id='kaeru']/forms/form[@ref="past_negative_plain"] -->
<agreement_translations>
  <translation class="masculine_personal" value="nie wrócił" />
  <translation class="masculine_animate" value="nie wrócił" />
  <translation class="feminine" value="nie wróciła" />
</agreement_translations>
```

### kaku

Pisanie jest naturalne bez jawnego tekstu, np. osoba, która pisze. Zachować object=text i direct_object.

```xml
<!-- kaku: append only to the indicated existing word/form. -->
<role ref="subject" nouns="friend mother sister teacher roujin hito programmer madogiwazoku" />
<!-- /dictionary/words/word[@id='kaku']/forms/form[@ref="dictionary"] -->
<agreement_translations>
  <translation class="masculine_personal" value="pisze" />
  <translation class="feminine" value="pisze" />
</agreement_translations>
<!-- /dictionary/words/word[@id='kaku']/forms/form[@ref="plain_negative"] -->
<agreement_translations>
  <translation class="masculine_personal" value="nie pisze" />
  <translation class="feminine" value="nie pisze" />
</agreement_translations>
<!-- /dictionary/words/word[@id='kaku']/forms/form[@ref="past_plain"] -->
<agreement_translations>
  <translation class="masculine_personal" value="pisał" />
  <translation class="feminine" value="pisała" />
</agreement_translations>
<!-- /dictionary/words/word[@id='kaku']/forms/form[@ref="past_negative_plain"] -->
<agreement_translations>
  <translation class="masculine_personal" value="nie pisał" />
  <translation class="feminine" value="nie pisała" />
</agreement_translations>
```

### kangaeru

Zastanawia się jest samodzielne; przy dopełnieniu pozostaje nad_instrumental. Pojazd jako przedmiot namysłu nie oznacza podmiotu.

```xml
<!-- kangaeru: append only to the indicated existing word/form. -->
<role ref="subject" nouns="friend mother sister teacher roujin hito programmer madogiwazoku" />
<!-- /dictionary/words/word[@id='kangaeru']/forms/form[@ref="dictionary"] -->
<agreement_translations>
  <translation class="masculine_personal" value="zastanawia się" />
  <translation class="feminine" value="zastanawia się" />
</agreement_translations>
<!-- /dictionary/words/word[@id='kangaeru']/forms/form[@ref="plain_negative"] -->
<agreement_translations>
  <translation class="masculine_personal" value="nie zastanawia się" />
  <translation class="feminine" value="nie zastanawia się" />
</agreement_translations>
<!-- /dictionary/words/word[@id='kangaeru']/forms/form[@ref="past_plain"] -->
<agreement_translations>
  <translation class="masculine_personal" value="zastanawiał się" />
  <translation class="feminine" value="zastanawiała się" />
</agreement_translations>
<!-- /dictionary/words/word[@id='kangaeru']/forms/form[@ref="past_negative_plain"] -->
<agreement_translations>
  <translation class="masculine_personal" value="nie zastanawiał się" />
  <translation class="feminine" value="nie zastanawiała się" />
</agreement_translations>
```

### kau

Kupuje może być użyte absolutnie dla kupującej osoby; precyzyjny zakup wymaga object. Zachować istniejące role.

```xml
<!-- kau: append only to the indicated existing word/form. -->
<role ref="subject" nouns="friend mother sister teacher roujin hito programmer madogiwazoku" />
<!-- /dictionary/words/word[@id='kau']/forms/form[@ref="dictionary"] -->
<agreement_translations>
  <translation class="masculine_personal" value="kupuje" />
  <translation class="feminine" value="kupuje" />
</agreement_translations>
<!-- /dictionary/words/word[@id='kau']/forms/form[@ref="plain_negative"] -->
<agreement_translations>
  <translation class="masculine_personal" value="nie kupuje" />
  <translation class="feminine" value="nie kupuje" />
</agreement_translations>
<!-- /dictionary/words/word[@id='kau']/forms/form[@ref="past_plain"] -->
<agreement_translations>
  <translation class="masculine_personal" value="kupił" />
  <translation class="feminine" value="kupiła" />
</agreement_translations>
<!-- /dictionary/words/word[@id='kau']/forms/form[@ref="past_negative_plain"] -->
<agreement_translations>
  <translation class="masculine_personal" value="nie kupił" />
  <translation class="feminine" value="nie kupiła" />
</agreement_translations>
```

### kikokusuru

帰国する zawiera powrót do własnego kraju; podmiot ludzki, argument celu zawarty w tłumaczeniu. Nie poszerzać na zwierzęta.

```xml
<!-- kikokusuru: append only to the indicated existing word/form. -->
<role ref="subject" nouns="friend mother sister teacher roujin hito programmer madogiwazoku" />
<!-- /dictionary/words/word[@id='kikokusuru']/forms/form[@ref="dictionary"] -->
<agreement_translations>
  <translation class="masculine_personal" value="wraca do kraju" />
  <translation class="feminine" value="wraca do kraju" />
</agreement_translations>
<!-- /dictionary/words/word[@id='kikokusuru']/forms/form[@ref="plain_negative"] -->
<agreement_translations>
  <translation class="masculine_personal" value="nie wraca do kraju" />
  <translation class="feminine" value="nie wraca do kraju" />
</agreement_translations>
<!-- /dictionary/words/word[@id='kikokusuru']/forms/form[@ref="past_plain"] -->
<agreement_translations>
  <translation class="masculine_personal" value="wrócił do kraju" />
  <translation class="feminine" value="wróciła do kraju" />
</agreement_translations>
<!-- /dictionary/words/word[@id='kikokusuru']/forms/form[@ref="past_negative_plain"] -->
<agreement_translations>
  <translation class="masculine_personal" value="nie wrócił do kraju" />
  <translation class="feminine" value="nie wróciła do kraju" />
</agreement_translations>
```

### kotaeru

Odpowiada może wystąpić bez jawnego pytania. Existing target=abstract pozostaje osobną kwestią precyzji dopełnienia.

```xml
<!-- kotaeru: append only to the indicated existing word/form. -->
<role ref="subject" nouns="friend mother sister teacher roujin hito programmer madogiwazoku" />
<!-- /dictionary/words/word[@id='kotaeru']/forms/form[@ref="dictionary"] -->
<agreement_translations>
  <translation class="masculine_personal" value="odpowiada" />
  <translation class="feminine" value="odpowiada" />
</agreement_translations>
<!-- /dictionary/words/word[@id='kotaeru']/forms/form[@ref="plain_negative"] -->
<agreement_translations>
  <translation class="masculine_personal" value="nie odpowiada" />
  <translation class="feminine" value="nie odpowiada" />
</agreement_translations>
<!-- /dictionary/words/word[@id='kotaeru']/forms/form[@ref="past_plain"] -->
<agreement_translations>
  <translation class="masculine_personal" value="odpowiedział" />
  <translation class="feminine" value="odpowiedziała" />
</agreement_translations>
<!-- /dictionary/words/word[@id='kotaeru']/forms/form[@ref="past_negative_plain"] -->
<agreement_translations>
  <translation class="masculine_personal" value="nie odpowiedział" />
  <translation class="feminine" value="nie odpowiedziała" />
</agreement_translations>
```

### kuru

Przychodzi żywa osoba/zwierzę. Jawnie uwzględnić nieregularne きた/こない; nie traktować 来ている jako zawsze czynności trwającej.

```xml
<!-- kuru: append only to the indicated existing word/form. -->
<role ref="subject" nouns="friend mother sister teacher roujin hito programmer madogiwazoku inu tori" />
<!-- /dictionary/words/word[@id='kuru']/forms/form[@ref="dictionary"] -->
<agreement_translations>
  <translation class="masculine_personal" value="przychodzi" />
  <translation class="masculine_animate" value="przychodzi" />
  <translation class="feminine" value="przychodzi" />
</agreement_translations>
<!-- /dictionary/words/word[@id='kuru']/forms/form[@ref="plain_negative"] -->
<agreement_translations>
  <translation class="masculine_personal" value="nie przychodzi" />
  <translation class="masculine_animate" value="nie przychodzi" />
  <translation class="feminine" value="nie przychodzi" />
</agreement_translations>
<!-- /dictionary/words/word[@id='kuru']/forms/form[@ref="past_plain"] -->
<agreement_translations>
  <translation class="masculine_personal" value="przyszedł" />
  <translation class="masculine_animate" value="przyszedł" />
  <translation class="feminine" value="przyszła" />
</agreement_translations>
<!-- /dictionary/words/word[@id='kuru']/forms/form[@ref="past_negative_plain"] -->
<agreement_translations>
  <translation class="masculine_personal" value="nie przyszedł" />
  <translation class="masculine_animate" value="nie przyszedł" />
  <translation class="feminine" value="nie przyszła" />
</agreement_translations>
```

### matsu

Czekanie ludzi i zwierząt jest naturalne bez jawnego obiektu; na_accusative pozostaje dla dopełnienia.

```xml
<!-- matsu: append only to the indicated existing word/form. -->
<role ref="subject" nouns="friend mother sister teacher roujin hito programmer madogiwazoku inu tori" />
<!-- /dictionary/words/word[@id='matsu']/forms/form[@ref="dictionary"] -->
<agreement_translations>
  <translation class="masculine_personal" value="czeka" />
  <translation class="masculine_animate" value="czeka" />
  <translation class="feminine" value="czeka" />
</agreement_translations>
<!-- /dictionary/words/word[@id='matsu']/forms/form[@ref="plain_negative"] -->
<agreement_translations>
  <translation class="masculine_personal" value="nie czeka" />
  <translation class="masculine_animate" value="nie czeka" />
  <translation class="feminine" value="nie czeka" />
</agreement_translations>
<!-- /dictionary/words/word[@id='matsu']/forms/form[@ref="past_plain"] -->
<agreement_translations>
  <translation class="masculine_personal" value="czekał" />
  <translation class="masculine_animate" value="czekał" />
  <translation class="feminine" value="czekała" />
</agreement_translations>
<!-- /dictionary/words/word[@id='matsu']/forms/form[@ref="past_negative_plain"] -->
<agreement_translations>
  <translation class="masculine_personal" value="nie czekał" />
  <translation class="masculine_animate" value="nie czekał" />
  <translation class="feminine" value="nie czekała" />
</agreement_translations>
```

### nomu

Picie ma naturalnego żywego wykonawcę i może nie mieć jawnego napoju; pozostawić object=drink.

```xml
<!-- nomu: append only to the indicated existing word/form. -->
<role ref="subject" nouns="friend mother sister teacher roujin hito programmer madogiwazoku inu tori" />
<!-- /dictionary/words/word[@id='nomu']/forms/form[@ref="dictionary"] -->
<agreement_translations>
  <translation class="masculine_personal" value="pije" />
  <translation class="masculine_animate" value="pije" />
  <translation class="feminine" value="pije" />
</agreement_translations>
<!-- /dictionary/words/word[@id='nomu']/forms/form[@ref="plain_negative"] -->
<agreement_translations>
  <translation class="masculine_personal" value="nie pije" />
  <translation class="masculine_animate" value="nie pije" />
  <translation class="feminine" value="nie pije" />
</agreement_translations>
<!-- /dictionary/words/word[@id='nomu']/forms/form[@ref="past_plain"] -->
<agreement_translations>
  <translation class="masculine_personal" value="pił" />
  <translation class="masculine_animate" value="pił" />
  <translation class="feminine" value="piła" />
</agreement_translations>
<!-- /dictionary/words/word[@id='nomu']/forms/form[@ref="past_negative_plain"] -->
<agreement_translations>
  <translation class="masculine_personal" value="nie pił" />
  <translation class="masculine_animate" value="nie pił" />
  <translation class="feminine" value="nie piła" />
</agreement_translations>
```

### nonbiri_suru

Lenistwo/odpoczynek osoby jest samodzielny; zachować obecne potoczne tłumaczenie, nie rozszerzać na przedmioty.

```xml
<!-- nonbiri_suru: append only to the indicated existing word/form. -->
<role ref="subject" nouns="friend mother sister teacher roujin hito programmer madogiwazoku" />
<!-- /dictionary/words/word[@id='nonbiri_suru']/forms/form[@ref="dictionary"] -->
<agreement_translations>
  <translation class="masculine_personal" value="leniuchuje" />
  <translation class="feminine" value="leniuchuje" />
</agreement_translations>
<!-- /dictionary/words/word[@id='nonbiri_suru']/forms/form[@ref="plain_negative"] -->
<agreement_translations>
  <translation class="masculine_personal" value="nie leniuchuje" />
  <translation class="feminine" value="nie leniuchuje" />
</agreement_translations>
<!-- /dictionary/words/word[@id='nonbiri_suru']/forms/form[@ref="past_plain"] -->
<agreement_translations>
  <translation class="masculine_personal" value="leniuchował" />
  <translation class="feminine" value="leniuchowała" />
</agreement_translations>
<!-- /dictionary/words/word[@id='nonbiri_suru']/forms/form[@ref="past_negative_plain"] -->
<agreement_translations>
  <translation class="masculine_personal" value="nie leniuchował" />
  <translation class="feminine" value="nie leniuchowała" />
</agreement_translations>
```

### okoru

怒る w wybranym znaczeniu emocji osoby jest samodzielne. Nie rozszerzać na homofoniczne 起こる ani bezpośrednio na karcenie kogoś.

```xml
<!-- okoru: append only to the indicated existing word/form. -->
<role ref="subject" nouns="friend mother sister teacher roujin hito programmer madogiwazoku" />
<!-- /dictionary/words/word[@id='okoru']/forms/form[@ref="dictionary"] -->
<agreement_translations>
  <translation class="masculine_personal" value="złości się" />
  <translation class="feminine" value="złości się" />
</agreement_translations>
<!-- /dictionary/words/word[@id='okoru']/forms/form[@ref="plain_negative"] -->
<agreement_translations>
  <translation class="masculine_personal" value="nie złości się" />
  <translation class="feminine" value="nie złości się" />
</agreement_translations>
<!-- /dictionary/words/word[@id='okoru']/forms/form[@ref="past_plain"] -->
<agreement_translations>
  <translation class="masculine_personal" value="zezłościł się" />
  <translation class="feminine" value="zezłościła się" />
</agreement_translations>
<!-- /dictionary/words/word[@id='okoru']/forms/form[@ref="past_negative_plain"] -->
<agreement_translations>
  <translation class="masculine_personal" value="nie zezłościł się" />
  <translation class="feminine" value="nie zezłościła się" />
</agreement_translations>
```

### omou

Myśli/pomyślał można użyć absolutnie. Zachować reporting i istniejący wybór aspektu; nie dodawać posiadania opinii o dowolnym przedmiocie.

```xml
<!-- omou: append only to the indicated existing word/form. -->
<role ref="subject" nouns="friend mother sister teacher roujin hito programmer madogiwazoku" />
<!-- /dictionary/words/word[@id='omou']/forms/form[@ref="dictionary"] -->
<agreement_translations>
  <translation class="masculine_personal" value="myśli" />
  <translation class="feminine" value="myśli" />
</agreement_translations>
<!-- /dictionary/words/word[@id='omou']/forms/form[@ref="plain_negative"] -->
<agreement_translations>
  <translation class="masculine_personal" value="nie myśli" />
  <translation class="feminine" value="nie myśli" />
</agreement_translations>
<!-- /dictionary/words/word[@id='omou']/forms/form[@ref="past_plain"] -->
<agreement_translations>
  <translation class="masculine_personal" value="pomyślał" />
  <translation class="feminine" value="pomyślała" />
</agreement_translations>
<!-- /dictionary/words/word[@id='omou']/forms/form[@ref="past_negative_plain"] -->
<agreement_translations>
  <translation class="masculine_personal" value="nie pomyślał" />
  <translation class="feminine" value="nie pomyślała" />
</agreement_translations>
```

### oyogu

Ludzie i pies mogą pływać. Nie dopuszczać ogólnego ptaka, bo nie wszystkie ptaki pływają, ani łodzi, która wymaga innego japońskiego orzeczenia.

```xml
<!-- oyogu: append only to the indicated existing word/form. -->
<role ref="subject" nouns="friend mother sister teacher roujin hito programmer madogiwazoku inu" />
<!-- /dictionary/words/word[@id='oyogu']/forms/form[@ref="dictionary"] -->
<agreement_translations>
  <translation class="masculine_personal" value="pływa" />
  <translation class="masculine_animate" value="pływa" />
  <translation class="feminine" value="pływa" />
</agreement_translations>
<!-- /dictionary/words/word[@id='oyogu']/forms/form[@ref="plain_negative"] -->
<agreement_translations>
  <translation class="masculine_personal" value="nie pływa" />
  <translation class="masculine_animate" value="nie pływa" />
  <translation class="feminine" value="nie pływa" />
</agreement_translations>
<!-- /dictionary/words/word[@id='oyogu']/forms/form[@ref="past_plain"] -->
<agreement_translations>
  <translation class="masculine_personal" value="pływał" />
  <translation class="masculine_animate" value="pływał" />
  <translation class="feminine" value="pływała" />
</agreement_translations>
<!-- /dictionary/words/word[@id='oyogu']/forms/form[@ref="past_negative_plain"] -->
<agreement_translations>
  <translation class="masculine_personal" value="nie pływał" />
  <translation class="masculine_animate" value="nie pływał" />
  <translation class="feminine" value="nie pływała" />
</agreement_translations>
```

### renshuusuru

Ćwiczy w znaczeniu doskonalenia umiejętności jest samodzielne. Object=music/song zostaje bez zmian i wymaga osobnej oceny idiomatyczności ćwiczyć muzykę.

```xml
<!-- renshuusuru: append only to the indicated existing word/form. -->
<role ref="subject" nouns="friend mother sister teacher roujin hito programmer madogiwazoku" />
<!-- /dictionary/words/word[@id='renshuusuru']/forms/form[@ref="dictionary"] -->
<agreement_translations>
  <translation class="masculine_personal" value="ćwiczy" />
  <translation class="feminine" value="ćwiczy" />
</agreement_translations>
<!-- /dictionary/words/word[@id='renshuusuru']/forms/form[@ref="plain_negative"] -->
<agreement_translations>
  <translation class="masculine_personal" value="nie ćwiczy" />
  <translation class="feminine" value="nie ćwiczy" />
</agreement_translations>
<!-- /dictionary/words/word[@id='renshuusuru']/forms/form[@ref="past_plain"] -->
<agreement_translations>
  <translation class="masculine_personal" value="ćwiczył" />
  <translation class="feminine" value="ćwiczyła" />
</agreement_translations>
<!-- /dictionary/words/word[@id='renshuusuru']/forms/form[@ref="past_negative_plain"] -->
<agreement_translations>
  <translation class="masculine_personal" value="nie ćwiczył" />
  <translation class="feminine" value="nie ćwiczyła" />
</agreement_translations>
```

### sentakusuru

Prać można bez jawnego ubrania; object=clothes pozostaje poprawnym zakresem. Nie dopuszczać przypadkowych rzeczy jako wykonawców.

```xml
<!-- sentakusuru: append only to the indicated existing word/form. -->
<role ref="subject" nouns="friend mother sister teacher roujin hito programmer madogiwazoku" />
<!-- /dictionary/words/word[@id='sentakusuru']/forms/form[@ref="dictionary"] -->
<agreement_translations>
  <translation class="masculine_personal" value="pierze" />
  <translation class="feminine" value="pierze" />
</agreement_translations>
<!-- /dictionary/words/word[@id='sentakusuru']/forms/form[@ref="plain_negative"] -->
<agreement_translations>
  <translation class="masculine_personal" value="nie pierze" />
  <translation class="feminine" value="nie pierze" />
</agreement_translations>
<!-- /dictionary/words/word[@id='sentakusuru']/forms/form[@ref="past_plain"] -->
<agreement_translations>
  <translation class="masculine_personal" value="prał" />
  <translation class="feminine" value="prała" />
</agreement_translations>
<!-- /dictionary/words/word[@id='sentakusuru']/forms/form[@ref="past_negative_plain"] -->
<agreement_translations>
  <translation class="masculine_personal" value="nie prał" />
  <translation class="feminine" value="nie prała" />
</agreement_translations>
```

### shimaru

Nieprzechodnie zamykanie torby/pudełka; istniejąca precyzyjna rola wystarcza. Dodać tylko feminine/neuter w czterech formach.

```xml
<!-- shimaru: append only to the indicated existing word/form. -->
<!-- /dictionary/words/word[@id='shimaru']/forms/form[@ref="dictionary"] -->
<agreement_translations>
  <translation class="feminine" value="zamyka się" />
  <translation class="neuter" value="zamyka się" />
</agreement_translations>
<!-- /dictionary/words/word[@id='shimaru']/forms/form[@ref="plain_negative"] -->
<agreement_translations>
  <translation class="feminine" value="nie zamyka się" />
  <translation class="neuter" value="nie zamyka się" />
</agreement_translations>
<!-- /dictionary/words/word[@id='shimaru']/forms/form[@ref="past_plain"] -->
<agreement_translations>
  <translation class="feminine" value="zamknęła się" />
  <translation class="neuter" value="zamknęło się" />
</agreement_translations>
<!-- /dictionary/words/word[@id='shimaru']/forms/form[@ref="past_negative_plain"] -->
<agreement_translations>
  <translation class="feminine" value="nie zamknęła się" />
  <translation class="neuter" value="nie zamknęło się" />
</agreement_translations>
```

### soujisuru

Sprzątanie jest samodzielną czynnością osoby; nie zmieniać object ani location. Dodatkowe dane nie naprawiają wszystkich obecnych dopełnień thing.

```xml
<!-- soujisuru: append only to the indicated existing word/form. -->
<role ref="subject" nouns="friend mother sister teacher roujin hito programmer madogiwazoku" />
<!-- /dictionary/words/word[@id='soujisuru']/forms/form[@ref="dictionary"] -->
<agreement_translations>
  <translation class="masculine_personal" value="sprząta" />
  <translation class="feminine" value="sprząta" />
</agreement_translations>
<!-- /dictionary/words/word[@id='soujisuru']/forms/form[@ref="plain_negative"] -->
<agreement_translations>
  <translation class="masculine_personal" value="nie sprząta" />
  <translation class="feminine" value="nie sprząta" />
</agreement_translations>
<!-- /dictionary/words/word[@id='soujisuru']/forms/form[@ref="past_plain"] -->
<agreement_translations>
  <translation class="masculine_personal" value="posprzątał" />
  <translation class="feminine" value="posprzątała" />
</agreement_translations>
<!-- /dictionary/words/word[@id='soujisuru']/forms/form[@ref="past_negative_plain"] -->
<agreement_translations>
  <translation class="masculine_personal" value="nie posprzątał" />
  <translation class="feminine" value="nie posprzątała" />
</agreement_translations>
```

### taberu

Jeść można bez jawnego jedzenia; żywy podmiot i object=food są rozdzielnymi rolami. Nie dopuszczać żywności jako wykonawcy.

```xml
<!-- taberu: append only to the indicated existing word/form. -->
<role ref="subject" nouns="friend mother sister teacher roujin hito programmer madogiwazoku inu tori" />
<!-- /dictionary/words/word[@id='taberu']/forms/form[@ref="dictionary"] -->
<agreement_translations>
  <translation class="masculine_personal" value="je" />
  <translation class="masculine_animate" value="je" />
  <translation class="feminine" value="je" />
</agreement_translations>
<!-- /dictionary/words/word[@id='taberu']/forms/form[@ref="plain_negative"] -->
<agreement_translations>
  <translation class="masculine_personal" value="nie je" />
  <translation class="masculine_animate" value="nie je" />
  <translation class="feminine" value="nie je" />
</agreement_translations>
<!-- /dictionary/words/word[@id='taberu']/forms/form[@ref="past_plain"] -->
<agreement_translations>
  <translation class="masculine_personal" value="jadł" />
  <translation class="masculine_animate" value="jadł" />
  <translation class="feminine" value="jadła" />
</agreement_translations>
<!-- /dictionary/words/word[@id='taberu']/forms/form[@ref="past_negative_plain"] -->
<agreement_translations>
  <translation class="masculine_personal" value="nie jadł" />
  <translation class="masculine_animate" value="nie jadł" />
  <translation class="feminine" value="nie jadła" />
</agreement_translations>
```

### undousuru

Samodzielna aktywność fizyczna osoby; bez dodawania narzędzi i bez utożsamienia z ćwiczeniem utworu.

```xml
<!-- undousuru: append only to the indicated existing word/form. -->
<role ref="subject" nouns="friend mother sister teacher roujin hito programmer madogiwazoku" />
<!-- /dictionary/words/word[@id='undousuru']/forms/form[@ref="dictionary"] -->
<agreement_translations>
  <translation class="masculine_personal" value="ćwiczy fizycznie" />
  <translation class="feminine" value="ćwiczy fizycznie" />
</agreement_translations>
<!-- /dictionary/words/word[@id='undousuru']/forms/form[@ref="plain_negative"] -->
<agreement_translations>
  <translation class="masculine_personal" value="nie ćwiczy fizycznie" />
  <translation class="feminine" value="nie ćwiczy fizycznie" />
</agreement_translations>
<!-- /dictionary/words/word[@id='undousuru']/forms/form[@ref="past_plain"] -->
<agreement_translations>
  <translation class="masculine_personal" value="ćwiczył fizycznie" />
  <translation class="feminine" value="ćwiczyła fizycznie" />
</agreement_translations>
<!-- /dictionary/words/word[@id='undousuru']/forms/form[@ref="past_negative_plain"] -->
<agreement_translations>
  <translation class="masculine_personal" value="nie ćwiczył fizycznie" />
  <translation class="feminine" value="nie ćwiczyła fizycznie" />
</agreement_translations>
```

### usowotsuku

Kłamać można bez jawnego adresata; うそをつく jest całym zapisanym leksemem. Nie tworzyć drugiego slotu dla うそ.

```xml
<!-- usowotsuku: append only to the indicated existing word/form. -->
<role ref="subject" nouns="friend mother sister teacher roujin hito programmer madogiwazoku" />
<!-- /dictionary/words/word[@id='usowotsuku']/forms/form[@ref="dictionary"] -->
<agreement_translations>
  <translation class="masculine_personal" value="kłamie" />
  <translation class="feminine" value="kłamie" />
</agreement_translations>
<!-- /dictionary/words/word[@id='usowotsuku']/forms/form[@ref="plain_negative"] -->
<agreement_translations>
  <translation class="masculine_personal" value="nie kłamie" />
  <translation class="feminine" value="nie kłamie" />
</agreement_translations>
<!-- /dictionary/words/word[@id='usowotsuku']/forms/form[@ref="past_plain"] -->
<agreement_translations>
  <translation class="masculine_personal" value="skłamał" />
  <translation class="feminine" value="skłamała" />
</agreement_translations>
<!-- /dictionary/words/word[@id='usowotsuku']/forms/form[@ref="past_negative_plain"] -->
<agreement_translations>
  <translation class="masculine_personal" value="nie skłamał" />
  <translation class="feminine" value="nie skłamała" />
</agreement_translations>
```

### utau

Śpiew osoby jest samodzielny. Ptaki zwykle 鳴く/さえずる; nie dodawać ich do A. Object=media odrębnie wymaga wykluczenia np. głosu.

```xml
<!-- utau: append only to the indicated existing word/form. -->
<role ref="subject" nouns="friend mother sister teacher roujin hito programmer madogiwazoku" />
<!-- /dictionary/words/word[@id='utau']/forms/form[@ref="dictionary"] -->
<agreement_translations>
  <translation class="masculine_personal" value="śpiewa" />
  <translation class="feminine" value="śpiewa" />
</agreement_translations>
<!-- /dictionary/words/word[@id='utau']/forms/form[@ref="plain_negative"] -->
<agreement_translations>
  <translation class="masculine_personal" value="nie śpiewa" />
  <translation class="feminine" value="nie śpiewa" />
</agreement_translations>
<!-- /dictionary/words/word[@id='utau']/forms/form[@ref="past_plain"] -->
<agreement_translations>
  <translation class="masculine_personal" value="śpiewał" />
  <translation class="feminine" value="śpiewała" />
</agreement_translations>
<!-- /dictionary/words/word[@id='utau']/forms/form[@ref="past_negative_plain"] -->
<agreement_translations>
  <translation class="masculine_personal" value="nie śpiewał" />
  <translation class="feminine" value="nie śpiewała" />
</agreement_translations>
```

### warau

Śmiech osoby może być samodzielny. Zachować z_genitive dla wyśmiewanej osoby/zwierzęcia; podmiot nie jest tym samym argumentem co object.

```xml
<!-- warau: append only to the indicated existing word/form. -->
<role ref="subject" nouns="friend mother sister teacher roujin hito programmer madogiwazoku" />
<!-- /dictionary/words/word[@id='warau']/forms/form[@ref="dictionary"] -->
<agreement_translations>
  <translation class="masculine_personal" value="śmieje się" />
  <translation class="feminine" value="śmieje się" />
</agreement_translations>
<!-- /dictionary/words/word[@id='warau']/forms/form[@ref="plain_negative"] -->
<agreement_translations>
  <translation class="masculine_personal" value="nie śmieje się" />
  <translation class="feminine" value="nie śmieje się" />
</agreement_translations>
<!-- /dictionary/words/word[@id='warau']/forms/form[@ref="past_plain"] -->
<agreement_translations>
  <translation class="masculine_personal" value="śmiał się" />
  <translation class="feminine" value="śmiała się" />
</agreement_translations>
<!-- /dictionary/words/word[@id='warau']/forms/form[@ref="past_negative_plain"] -->
<agreement_translations>
  <translation class="masculine_personal" value="nie śmiał się" />
  <translation class="feminine" value="nie śmiała się" />
</agreement_translations>
```

### yomu

Czytanie ma naturalne użycie bez jawnego tekstu. Precyzyjna lista ludzi, zachować object=text; nie dodawać zwierząt ani rzeczy.

```xml
<!-- yomu: append only to the indicated existing word/form. -->
<role ref="subject" nouns="friend mother sister teacher roujin hito programmer madogiwazoku" />
<!-- /dictionary/words/word[@id='yomu']/forms/form[@ref="dictionary"] -->
<agreement_translations>
  <translation class="masculine_personal" value="czyta" />
  <translation class="feminine" value="czyta" />
</agreement_translations>
<!-- /dictionary/words/word[@id='yomu']/forms/form[@ref="plain_negative"] -->
<agreement_translations>
  <translation class="masculine_personal" value="nie czyta" />
  <translation class="feminine" value="nie czyta" />
</agreement_translations>
<!-- /dictionary/words/word[@id='yomu']/forms/form[@ref="past_plain"] -->
<agreement_translations>
  <translation class="masculine_personal" value="czytał" />
  <translation class="feminine" value="czytała" />
</agreement_translations>
<!-- /dictionary/words/word[@id='yomu']/forms/form[@ref="past_negative_plain"] -->
<agreement_translations>
  <translation class="masculine_personal" value="nie czytał" />
  <translation class="feminine" value="nie czytała" />
</agreement_translations>
```

### shinjiru

Wierzy może opisywać osobę bez jawnego obiektu wiary. Zachować w_accusative; wiara w osobę i ufanie osobie nie są automatycznie tą samą rekcją.

```xml
<!-- shinjiru: append only to the indicated existing word/form. -->
<role ref="subject" nouns="friend mother sister teacher roujin hito programmer madogiwazoku" />
<!-- /dictionary/words/word[@id='shinjiru']/forms/form[@ref="dictionary"] -->
<agreement_translations>
  <translation class="masculine_personal" value="wierzy" />
  <translation class="feminine" value="wierzy" />
</agreement_translations>
<!-- /dictionary/words/word[@id='shinjiru']/forms/form[@ref="plain_negative"] -->
<agreement_translations>
  <translation class="masculine_personal" value="nie wierzy" />
  <translation class="feminine" value="nie wierzy" />
</agreement_translations>
<!-- /dictionary/words/word[@id='shinjiru']/forms/form[@ref="past_plain"] -->
<agreement_translations>
  <translation class="masculine_personal" value="wierzył" />
  <translation class="feminine" value="wierzyła" />
</agreement_translations>
<!-- /dictionary/words/word[@id='shinjiru']/forms/form[@ref="past_negative_plain"] -->
<agreement_translations>
  <translation class="masculine_personal" value="nie wierzył" />
  <translation class="feminine" value="nie wierzyła" />
</agreement_translations>
```
