"""Opt-in bounded before/after release comparison, not a unit fixture.

Reads the declared Content graph because release compatibility cannot be proven
from independent vocabulary. At most four previews for each of 18 representative
legacy families plus four forced reflexive questions; never enumerates choices.
"""
import argparse
import hashlib
import json
from pathlib import Path
import random
import subprocess
import sys
import xml.etree.ElementTree as ET

FAMILIES = ('Zdania przydawkowe', 'Zdania przydawkowe podmiotowe', 'Sam czasownik',
    'Czasownik z target', 'Czasownik z dopełnieniem', 'Opisane dopełnienie',
    'Cel ruchu', 'Towarzysz', 'Miejsce czynności', 'Środek transportu',
    'Przed inną czynnością', 'Możliwość ことができる', 'Czynność w toku 〜ている',
    'Pytanie o miejsce', 'Pytanie kiedy', 'Pytanie dlaczego', 'Łącznik だから', 'Reakcja na przyczynę')
FORMS = ('dictionary','plain_negative','past_plain','past_negative_plain')


def worker(args):
    sys.path.insert(0,str(args.kotomi.resolve()))
    from kotomi.application.quiz_project import QuizProject
    p=QuizProject.load(args.data/'quiz_project.xml')
    if args.bindings:
        rows=json.loads(args.bindings.read_text())
        for row in rows:
            v=p.build_preview(row['pattern'], form_name=row['form'], word_choices=row['bindings']['word_choices'], entity_choices=row['bindings']['entity_choices'], rng=random.Random(26))
            pair=(v.source,v.answer)
            assert list(pair)==row['pair'],(row['pattern'],row['pair'],pair)
    else:
        rows=[]
        def append(key,form,words=None):
            v=p.build_preview(key,form_name=form,word_choices=words,rng=random.Random(26))
            v=p.build_preview(key,form_name=form,word_choices=v.words,entity_choices=v.entities,rng=random.Random(26))
            rows.append({'pattern':key,'form':form,'pair':[v.source,v.answer],
                'bindings':{'word_choices':v.words,'entity_choices':v.entities,
                            'form_overrides':v.forms,'context_pool':v.context_pool,'context_option':v.context_option}})
        for family in FAMILIES:
            keys=[k for k in p.patterns if k==family or k.startswith(family+' / ')]
            if not keys:
                # Composite IDs use an internal separator; follow its expansion.
                keys=list(p.composite_patterns[family].expanded_pattern_ids) if hasattr(p.composite_patterns.get(family),'expanded_pattern_ids') else [k for k in p.patterns if k.startswith(family)]
            assert keys,family
            for form in FORMS:
                append(sorted(keys)[0],form)
        for form in FORMS:
            append('Pytanie kiedy / Sam czasownik',form,{'verb@embedded_verb':'asobu'})
    print(json.dumps(rows,ensure_ascii=False))


def main(args):
    import tempfile
    def run(code,data,bindings=None):
        command=[sys.executable,str(Path(__file__).resolve()),'--worker','--kotomi',str(code.resolve()),'--data',str(data.resolve())]
        if bindings: command+=['--bindings',str(bindings)]
        result=subprocess.run(command,capture_output=True,text=True,timeout=45)
        if result.returncode:
            raise RuntimeError(result.stderr)
        return json.loads(result.stdout)
    baseline=run(args.before_kotomi,args.before_data)
    with tempfile.TemporaryDirectory() as temp:
        path=Path(temp)/'bindings.json';path.write_text(json.dumps(baseline,ensure_ascii=False))
        assert run(args.kotomi,args.data,path)==baseline
    preserved={}
    for directory in ('dictionaries','grammar','lessons'):
        for path in sorted((args.before_data/directory).glob('*.xml')):
            relative=path.relative_to(args.before_data)
            assert path.read_bytes()==(args.data/relative).read_bytes(),relative
            preserved[str(relative)]=hashlib.sha256(path.read_bytes()).hexdigest()
    for relative in ('patterns/sentence_quizzes.xml',):
        assert (args.before_data/relative).read_bytes()==(args.data/relative).read_bytes()
    def patterns(data):
        root=ET.parse(data/'patterns/sentence_maps.xml').getroot()
        return {n.get('id'):ET.tostring(n,encoding='unicode').strip() for n in root.iter('sentence_pattern') if not n.get('id','').startswith('Przydawki / ')}
    assert patterns(args.before_data)==patterns(args.data)
    args.output.write_text(json.dumps({'method':__doc__,'unchanged_full_pairs':baseline,
        'unchanged_xml_sha256':preserved,'old_pattern_definitions_unchanged':True,'quiz_definition_unchanged':True},ensure_ascii=False,indent=2)+'\n')
    print(f'Preserved {len(baseline)} complete legacy pairs and {len(preserved)} XML files.')

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    for key in ('kotomi','data','before-kotomi','before-data','output','bindings'):
        parser.add_argument('--'+key,type=Path)
    parser.add_argument('--worker',action='store_true')
    args=parser.parse_args()
    worker(args) if args.worker else main(args)
