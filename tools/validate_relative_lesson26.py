"""Opt-in release acceptance for the actual lesson-26 patterns.

Reads the declared project graph once. This is not a unit test or a CI inventory
freeze: each explicit reference pair checks shipped linguistic content, which an
independent engine fixture cannot certify. Cost is project load/validation plus
O(reference examples) fully locked render/count probes; no Cartesian enumeration.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys
from time import perf_counter

# Individually reviewed full sentences, not outputs captured from the engine.
CASES = [
 ('Osoba i dopełnienie', 'past_plain', 'yomu', {'subject':'hito','object':'newspaper','identity':'mother'}, {},
  'To mama jest osobą, która czytała gazetę.', 'しんぶんをよんだひとはおかあさんです。'),
 ('Osoba i dopełnienie', 'plain_negative', 'yomu', {'subject':'hito','object':'newspaper','identity':'mother'}, {},
  'To mama jest osobą, która nie czyta gazety.', 'しんぶんをよまないひとはおかあさんです。'),
 ('Pytanie o wykonawcę', 'past_plain', 'tsukuru', {'subject':'hito','object':'cake'}, {},
  'Kim jest osoba, która zrobiła ciasto?', 'ケーキをつくったひとはだれですか。'),
 ('Pytanie o wykonawcę', 'past_negative_plain', 'yomu', {'subject':'hito','object':'book'}, {},
  'Kim jest osoba, która nie czytała książki?', 'ほんをよまなかったひとはだれですか。'),
 ('Wybór przedmiotu', 'past_plain', 'kau', {'object':'watch'}, {},
  'Która z tych rzeczy to zegarek, który kupiłem?', 'わたしがかったとけいはどれですか。'),
 ('Wskazanie przedmiotu', 'past_plain', 'wasureru', {'object':'kagi'}, {},
  'Czy to klucz, którego zapomniałem?', 'わたしがわすれたかぎはこれですか。'),
 ('Lokalizacja przedmiotu', 'past_plain', 'morau', {'object':'book'}, {},
  'Gdzie jest książka, którą otrzymałem?', 'わたしがもらったほんはどこですか。'),
 ('Miejsce czynności', 'past_plain', 'umareru', {'location':'home'}, {},
  'Gdzie znajduje się dom, w którym się urodziłem?', 'わたしがうまれたうちはどこですか。'),
 ('Ocena miejsca', 'past_plain', 'tomaru_stay', {'location':'hotel'}, {},
  'Jaki był hotel, w którym nocowałem?', 'わたしがとまったホテルはどうでしたか。'),
 ('Miejsce zamieszkania', None, 'sumu', {'target':'tokoro'}, {},
  'Gdzie znajduje się miejsce, w którym mieszkam?', 'わたしがすんでいるところはどこですか。'),
 ('Dzień czynności', 'dictionary', 'kuru', {'subject':'mother','destination':'poland','day':'hi','date':'kinyoubi'}, {},
  'To piątek jest dniem, w którym mama przychodzi do Polski.', 'おかあさんがポーランドへくるひはきんようびです。'),
 ('Pytanie o dzień', 'dictionary', 'iku', {'subject':'mother','destination':'japan','day':'hi'}, {},
  'Kiedy przypada dzień, w którym mama idzie do Japonii?', 'おかあさんがにほんへいくひはいつですか。'),
 ('Pragnienie spotkania', None, 'au', {'target':'hito'}, {},
  'Kim jest osoba, z którą najbardziej chcę się spotkać?', 'わたしがいちばんあいたいひとはだれですか。'),
 ('Pragnienie podróży', None, 'iku', {'destination':'kuni','identity':'india'}, {},
  'Czy kraj, do którego najbardziej chcę pojechać, to Indie?', 'わたしがいちばんいきたいくにはインドですか。'),
 ('Upodobanie', None, None, {'item':'wine'}, {},
  'Która z tych rzeczy to wino, które najbardziej lubię?', 'わたしがいちばんすきなワインはどれですか。'),
 ('Pożądana rzecz', None, None, {'item':'watch'}, {},
  'Która z tych rzeczy to zegarek, który najbardziej chcę mieć?', 'わたしがいちばんほしいとけいはどれですか。'),
 ('Ocena przedmiotu', 'past_plain', 'tsukuru', {'object':'cake'}, {},
  'Jakie było ciasto, które zrobiłem?', 'わたしがつくったケーキはどうでしたか。'),
 ('Opis osoby', 'past_plain', 'matsu', {'object':'hito'}, {'adjective@quality':'kawaii'},
  'Czy osoba, na którą czekałem, była urocza?', 'わたしがまったひとはかわいかったですか。'),
 ('Powód czynności', 'past_negative_plain', 'yomu', {'object':'book','reason':'riyuu'}, {},
  'Jaki jest powód, dla którego nie czytałem książki?', 'わたしがほんをよまなかったりゆうはなんですか。'),
 ('Liczba osób', 'past_plain', 'kuru', {'subject':'hito','destination':'school'}, {},
  'Ile osób przyszło do szkoły?', 'がっこうへきたひとはなんにんですか。'),
 ('Osoba i dopełnienie 〜ている', None, 'yomu', {'subject':'hito','object':'newspaper','identity':'mother'}, {},
  'To mama jest osobą, która czyta gazetę.', 'しんぶんをよんでいるひとはおかあさんです。'),
 ('Pytanie o wykonawcę 〜ている', None, 'kiru', {'subject':'hito','object':'clothes'}, {},
  'Kim jest osoba, która ma na sobie ubranie?', 'ふくをきているひとはだれですか。'),
 ('Miejsce czynności 〜ている', None, 'hataraku', {'location':'jimusitsu'}, {},
  'Gdzie znajduje się biuro, w którym pracuję?', 'わたしがはたらいているじむしつはどこですか。'),
]


# Additional reviewed bindings vary gender, noun, verb and polarity.
CASES += [
 ('Osoba i dopełnienie', 'past_plain', 'tsukuru', {'subject':'hito','object':'cake','identity':'sister'}, {},
  'To siostra jest osobą, która zrobiła ciasto.', 'ケーキをつくったひとはあねです。'),
 ('Pytanie o wykonawcę', 'dictionary', 'yomu', {'subject':'teacher','object':'book'}, {},
  'Kim jest nauczyciel, który czyta książkę?', 'ほんをよむせんせいはだれですか。'),
 ('Wybór przedmiotu', 'past_negative_plain', 'yomu', {'object':'book'}, {},
  'Która z tych rzeczy to książka, której nie czytałem?', 'わたしがよまなかったほんはどれですか。'),
 ('Wskazanie przedmiotu', 'past_plain', 'tsukuru', {'object':'cake'}, {},
  'Czy to ciasto, które zrobiłem?', 'わたしがつくったケーキはこれですか。'),
 ('Lokalizacja przedmiotu', 'past_plain', 'kau', {'object':'watch'}, {},
  'Gdzie jest zegarek, który kupiłem?', 'わたしがかったとけいはどこですか。'),
 ('Miejsce czynności', 'past_negative_plain', 'hataraku', {'location':'jimusitsu'}, {},
  'Gdzie znajduje się biuro, w którym nie pracowałem?', 'わたしがはたらかなかったじむしつはどこですか。'),
 ('Ocena miejsca', 'past_plain', 'hataraku', {'location':'jimusitsu'}, {},
  'Jakie było biuro, w którym pracowałem?', 'わたしがはたらいたじむしつはどうでしたか。'),
 ('Dzień czynności', 'past_plain', 'iku', {'subject':'teacher','destination':'school','day':'hi','date':'getsuyoubi'}, {},
  'To poniedziałek jest dniem, w którym nauczyciel poszedł do szkoły.', 'せんせいががっこうへいったひはげつようびです。'),
 ('Pytanie o dzień', 'past_negative_plain', 'kuru', {'subject':'sister','destination':'school','day':'hi'}, {},
  'Kiedy przypada dzień, w którym siostra nie przyszła do szkoły?', 'あねががっこうへこなかったひはいつですか。'),
 ('Pragnienie spotkania', None, 'au', {'target':'teacher'}, {},
  'Kim jest nauczyciel, z którym najbardziej chcę się spotkać?', 'わたしがいちばんあいたいせんせいはだれですか。'),
 ('Pragnienie podróży', None, 'iku', {'destination':'kuni','identity':'japan'}, {},
  'Czy kraj, do którego najbardziej chcę pojechać, to Japonia?', 'わたしがいちばんいきたいくにはにほんですか。'),
 ('Upodobanie', None, None, {'item':'book'}, {},
  'Która z tych rzeczy to książka, którą najbardziej lubię?', 'わたしがいちばんすきなほんはどれですか。'),
 ('Pożądana rzecz', None, None, {'item':'book'}, {},
  'Która z tych rzeczy to książka, którą najbardziej chcę mieć?', 'わたしがいちばんほしいほんはどれですか。'),
 ('Ocena przedmiotu', 'past_plain', 'yomu', {'object':'book'}, {},
  'Jaka była książka, którą czytałem?', 'わたしがよんだほんはどうでしたか。'),
 ('Opis osoby', 'past_negative_plain', 'matsu', {'object':'teacher'}, {'adjective@quality':'kawaii'},
  'Czy nauczyciel, na którego nie czekałem, był uroczy?', 'わたしがまたなかったせんせいはかわいかったですか。'),
 ('Powód czynności', 'past_plain', 'tsukuru', {'object':'cake','reason':'riyuu'}, {},
  'Jaki jest powód, dla którego zrobiłem ciasto?', 'わたしがケーキをつくったりゆうはなんですか。'),
 ('Liczba osób', 'past_plain', 'iku', {'subject':'hito','destination':'school'}, {},
  'Ile osób poszło do szkoły?', 'がっこうへいったひとはなんにんですか。'),
 ('Osoba i dopełnienie 〜ている', None, 'kiru', {'subject':'hito','object':'clothes','identity':'sister'}, {},
  'To siostra jest osobą, która ma na sobie ubranie.', 'ふくをきているひとはあねです。'),
 ('Pytanie o wykonawcę 〜ている', None, 'yomu', {'subject':'teacher','object':'book'}, {},
  'Kim jest nauczyciel, który czyta książkę?', 'ほんをよんでいるせんせいはだれですか。'),
 ('Miejsce czynności 〜ている', None, 'hataraku', {'location':'school'}, {},
  'Gdzie znajduje się szkoła, w której pracuję?', 'わたしがはたらいているがっこうはどこですか。'),
]


def run(kotomi, data):
    sys.path.insert(0, str(kotomi.resolve()))
    from kotomi.application.quiz_project import QuizProject
    from kotomi.core.generation.compatibility import CompatibilityProbe
    from kotomi.application.quiz_hints import selected_vocabulary_hints, selected_context_hint
    start = perf_counter(); p = QuizProject.load(data / 'quiz_project.xml')
    timings = {'load_ms': (perf_counter()-start)*1000}
    start = perf_counter(); issues = p.validate(); timings['validate_ms'] = (perf_counter()-start)*1000
    assert not issues, issues
    rows=[]
    for title,form,verb,nouns,extra,source,answer in CASES:
        print(title, flush=True)
        key='Przydawki / '+title
        words={**({'verb@action':verb} if verb else {}),**extra}
        entities={'noun@'+k:v for k,v in nouns.items()}
        start=perf_counter()
        value=p.build_preview(key,form_name=form,word_choices=words,entity_choices=entities)
        assert source[0].isupper(), source
        assert (value.source,value.answer)==(source,answer),(title,value.source,value.answer,source,answer)
        assert p.render_bound_pattern(key,word_choices=value.words,entity_choices=value.entities,
            form_overrides=value.forms,context_pool=value.context_pool,context_option=value.context_option)==(source,answer)
        stats=p.count_possibilities(key,form_name=form,word_choices=words,entity_choices=entities)
        assert stats.generated_sentences==1,(title,stats.generated_sentences)
        hints = selected_vocabulary_hints(p, value)
        actual_hints = {(hint.dictionary_id, hint.kana) for hint in hints}
        expected_hints = {('nouns', p.entities[identifier].kana) for identifier in value.entities.values()}
        for slot, identifier in value.words.items():
            dictionary = p.analyze_pattern(key).slots[slot].dictionary
            expected_hints.add((dictionary, p.words[dictionary][identifier].kana))
        assert actual_hints == expected_hints, (key, actual_hints, expected_hints)
        assert selected_context_hint(p, value) == ('', '')
        assert key in p.sentence_quizzes['relative_clauses'].pattern_ids
        rows.append({'pattern':key,'form':form,'source':source,'answer':answer,
                     'render_and_locked_count_ms':(perf_counter()-start)*1000})
    rejected=[]
    for title,form,words,entities in [
        ('Pytanie o wykonawcę','dictionary',{'verb@action':'yomu'},{'noun@subject':'book','noun@object':'newspaper'}),
        ('Pytanie o wykonawcę','dictionary',{'verb@action':'yomu'},{'noun@subject':'hito','noun@object':'car'}),
        ('Wybór przedmiotu','dictionary',{'verb@action':'yomu'},{'noun@object':'hito'}),
        ('Pytanie o wykonawcę','polite_nonpast',{'verb@action':'yomu'},{'noun@subject':'hito','noun@object':'book'}),
        ('Miejsce czynności 〜ている',None,{'verb@action':'kiru'},{'noun@location':'hotel'}),
        ('Miejsce zamieszkania',None,{'verb@action':'sumu'},{'noun@target':'book'}),
        ('Opis osoby','past_plain',{'verb@action':'miru'},{'noun@object':'hito'}),
    ]:
        key='Przydawki / '+title
        assert not CompatibilityProbe(p,p.analyze_pattern(key),form).exists(word_choices=words,entity_choices=entities),(key,words,entities)
        rejected.append({'pattern':key,'words':words,'entities':entities,'form':form})
    # Existing B1/B3 remain covered by isolated regressions and these locked pairs.
    for key,verb,noun,expected in [
        ('Zdania przydawkowe','yomu','book',('To jest książka, której nie czytałem.','これはわたしがよまなかったほんです。')),
        ('Zdania przydawkowe podmiotowe','hataraku','hito',('To jest osoba, która nie pracowała.','これははたらかなかったひとです。'))]:
        v=p.build_preview(key,form_name='past_negative_plain',word_choices={'verb@action':verb},entity_choices={'noun@item':noun})
        assert (v.source,v.answer)==expected
    return {'scope':'Opt-in production release audit; bounded locked examples, no full enumeration',
            'timings':timings,'examples':rows,'rejected':rejected,'legacy_pairs':2}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--kotomi',type=Path,required=True)
    parser.add_argument('--data',type=Path,default=Path(__file__).resolve().parents[1])
    parser.add_argument('--output',type=Path)
    args=parser.parse_args(); report=run(args.kotomi,args.data.resolve())
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(f"Passed {len(report['examples'])} full sentence pairs, {len(report['rejected'])} rejected bindings and 2 legacy pairs.")
    print(report['timings'])
