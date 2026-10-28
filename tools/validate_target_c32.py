"""Opt-in C3.2 production acceptance. Not imported by unit-test CI.

Reads the declared project graph once, renders only the new bounded-form pattern,
and compares counts, simulator previews, bound rendering and quiz generation.
Use independent test fixtures for ordinary engine and authoring regressions.
"""
import argparse
import json
from pathlib import Path
import random
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--kotomi',type=Path,required=True)
    parser.add_argument('--output',type=Path)
    args = parser.parse_args()
    sys.path.insert(0,str(args.kotomi.resolve()))
    from kotomi.application.quiz_project import QuizProject
    from kotomi.application.generation_engine import SharedQuizEngine
    from kotomi.core.generation.models import EngineRequest
    from kotomi.core.generation.compatibility import CompatibilityProbe
    root = Path(__file__).resolve().parents[1]
    p = QuizProject.load(root/'quiz_project.xml')
    errors = p.validate()
    assert not errors, errors
    identifier = 'Czasownik z target'
    pattern = p.patterns[identifier]
    engine = SharedQuizEngine(p,random.Random(32))
    results = {'scope':'Opt-in production acceptance, not unit tests',
        'baseline_application':'a61c1002270696fe94f9dc81103b0e86735f1f9e',
        'baseline_data':'eaefaa8b287a0ea2778a44aa2bb2ced6d75f3e91',
        'revision':64,'validation_errors':errors,'counts':{},'examples':[],
        'target_audit':{}}
    for v in p.words['verbs'].values():
        if 'target' in v.usage or 'target' in v.usage_nouns:
            results['target_audit'][v.id] = {'accepts':v.usage.get('target',[]),
                'nouns':v.usage_nouns.get('target',[]),'government':v.government_by_role.get('target','')}
    for form in pattern.allowed_forms:
        values = list(p.iter_possibilities(identifier,form_name=form))
        stats = p.count_possibilities(identifier,form_name=form)
        assert len(values)==stats.generated_sentences
        assert len({v.source for v in values})==stats.unique_questions
        assert len({v.answer for v in values})==stats.unique_answers
        outputs = {(v.source,v.answer) for v in values}
        for v in values:
            assert p.render_bound_pattern(identifier,word_choices=v.words,
                entity_choices=v.entities,form_overrides=v.forms,context_pool=v.context_pool,context_option=v.context_option)==(v.source,v.answer)
            assert 'od kogoś od' not in v.source and 'komuś siostrze' not in v.source
        for _ in range(20):
            q = engine.build_question(EngineRequest(identifier,form_name=form))
            assert (q.prompt,q.expected_answer) in outputs
        results['counts'][form] = {'generated':len(values),'questions':stats.unique_questions,'answers':stats.unique_answers}
    for verb,noun,pl,jp in [
        ('kayou','school','uczęszczam do szkoły.','がっこうにかよう。'),
        ('kayou','taiikukan','uczęszczam do sali gimnastycznej.','たいいくかんにかよう。'),
        ('hairu','school','wchodzę do szkoły.','がっこうにはいる。'),
        ('hairu','room','wchodzę do pokoju.','へやにはいる。'),
        ('hairu','daidokoro','wchodzę do kuchni.','だいどころにはいる。'),
        ('hairu','jimusitsu','wchodzę do biura.','じむしつにはいる。'),
        ('kariru','sister','pożyczam od starszej siostry.','あねにかりる。'),
        ('kasu','sister','pożyczam starszej siostrze.','あねにかす。'),
        ('ageru_give','sister','daję starszej siostrze.','あねにあげる。')]:
        q = p.build_preview(identifier,form_name='dictionary',word_choices={'verb@action':verb},entity_choices={'noun@target':noun})
        assert (q.source,q.answer)==(pl,jp)
        results['examples'].append({'verb':verb,'noun':noun,'polish':q.source,'japanese':q.answer})
    probe = CompatibilityProbe(p,p.analyze_pattern(identifier),'dictionary')
    for verb,noun in [('kayou','biru'),('kariru','inu'),('sumu','school'),('kureru','sister')]:
        assert not probe.exists(word_choices={'verb@action':verb},entity_choices={'noun@target':noun})
    # The broader building category also changes existing object constructions.
    results['tateru_object_examples'] = []
    for noun in ('room','daidokoro','jimusitsu'):
        source, answer = p.render_bound_pattern('Czasownik z dopełnieniem',
            form_overrides={'verb[role:object]':'dictionary'},
            word_choices={'verb[role:object]':'tateru'}, entity_choices={'noun':noun},
            context_pool='present', context_option='neutral')
        results['tateru_object_examples'].append({'noun':noun,'polish':source,'japanese':answer})
    result = json.dumps(results,ensure_ascii=False,indent=2)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(result)
    print(result)


if __name__=='__main__':main()
