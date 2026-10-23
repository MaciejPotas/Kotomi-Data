"""Optional bounded release measurements, outside CI/test discovery.

Reads the declared Content graph to measure real inventory costs. Independent
fixtures cannot establish release latency. Three fresh-process samples per
scenario; statistics is killed after 12 seconds, never extrapolated to a total.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import random
import statistics
import subprocess
import sys
from time import perf_counter


def worker(args):
    sys.path.insert(0, str(args.kotomi.resolve()))
    from kotomi.application.quiz_project import QuizProject
    from apps.grammar import logic
    result = {}
    def timed(name, operation):
        start = perf_counter()
        value = operation()
        result[name] = round((perf_counter() - start) * 1000, 3)
        return value
    p = timed('load_ms', lambda: QuizProject.load(args.data / 'quiz_project.xml'))
    if args.omit_new:
        p.patterns = {k:v for k,v in p.patterns.items() if not k.startswith('Przydawki / ')}
        for quiz in p.sentence_quizzes.values():
            quiz.pattern_ids = [k for k in quiz.pattern_ids if not k.startswith('Przydawki / ')]
    if args.worker == 'project':
        # First preview precedes validation so it cannot reuse validation caches.
        timed('old_first_preview_ms', lambda: p.build_preview('Zdania przydawkowe', form_name='past_plain', rng=random.Random(26)))
        issues = timed('validate_ms', p.validate)
        assert not issues, issues
    else:
        logic.configure_quiz_profile('relative_clauses', project=p)
        policy = logic.snapshot_quiz_policy()
        engine = timed('engine_from_preloaded_ms', lambda: policy.QUIZ_ENGINE_CLASS(p.manifest_path, rng=random.Random(26), project=p))
        keys = [k for k in p.sentence_quizzes['relative_clauses'].pattern_ids if k.startswith('Przydawki / ')]
        selected = {'one':['Przydawki / Osoba i dopełnienie'], 'light':['Przydawki / Pragnienie podróży'],
                    'new':keys, 'all':p.sentence_quizzes['relative_clauses'].pattern_ids}[args.selection]
        settings = policy.QUIZ_SETTINGS_CLASS(enabled_patterns=selected, enabled_forms=list(policy.FORM_GROUPS), plain_output=True, polite_output=False)
        if args.worker == 'count':
            result['statistics'] = timed('statistics_ms', lambda: engine.statistics(settings))
        else:
            assert timed('availability_ms', lambda: engine.has_possible_question(settings))
            q = timed('first_question_ms', lambda: engine.generate_question(settings))
            assert q.pattern_id in selected
            result['first_pair'] = [q.source_sentence, q.expected_answer]
    print(json.dumps(result, ensure_ascii=False))


def main(args):
    scenarios = [('before_review', args.before_kotomi, args.before_data, False),
                 ('after_review', args.kotomi, args.data, False),
                 ('main_content_current_engine', args.kotomi, args.main_data, False),
                 ('expanded_content_without_new_patterns', args.kotomi, args.data, True)]
    samples = {name:[] for name, *_ in scenarios}
    def launch(code, data, mode, selection='all', omit=False):
        command = [sys.executable, str(Path(__file__).resolve()), '--worker', mode, '--kotomi', str(code.resolve()),
                   '--data', str(data.resolve()), '--selection', selection]
        if omit: command.append('--omit-new')
        timeout = 12 if mode == 'count' else 45
        try:
            p = subprocess.run(command, text=True, capture_output=True, timeout=timeout, check=True)
            return json.loads(p.stdout)
        except subprocess.TimeoutExpired:
            return {'incomplete':True, 'process_timeout_s':timeout, 'total':None}
    for repeat in range(3):
        for name, code, data, omit in scenarios:
            print(name, repeat + 1, flush=True)
            samples[name].append(launch(code,data,'project',omit=omit))
    quiz = {}
    for name,code,data,_ in scenarios[:2]:
        quiz[name] = {}
        for selection in ('one','new','all'):
            print(name,selection,flush=True)
            quiz[name][selection] = [launch(code,data,'quiz',selection) for _ in range(3)]
    counts = {}
    for name,code,data,_ in scenarios[:2]:
        counts[name] = {}
        for selection in ('light','one','new','all'):
            print('bounded count',name,selection,flush=True)
            counts[name][selection] = launch(code,data,'count',selection)
    medians = {name:{key:round(statistics.median(row[key] for row in rows),3)
                    for key in ('load_ms','old_first_preview_ms','validate_ms')}
               for name,rows in samples.items()}
    report = {'method':'Three interleaved fresh-process samples; same machine/interpreter. First legacy preview BEFORE validation. Quiz uses a preloaded project, availability then first question. Cold validation is measured separately. Count process deadline 12s includes imports/load; null total means NOT measured. No optimization or CI performance threshold.',
              'baseline_heads':{'Kotomi':'16b6c24eb5405e1e5ef2e0d6bbb8053c6cb6efa4','Kotomi-Data':'269786eea1232bf9fbe9b1b7fe01c9cb5797a42b','main_content':'aa14564f8a45d5a63b4c62e880fc6237dc407240'},
              'project_samples':samples,'project_medians':medians,'quiz_samples':quiz,'bounded_statistics':counts}
    args.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(medians,indent=2))


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ('kotomi','data','before-kotomi','before-data','main-data','output'):
        parser.add_argument('--'+name,type=Path)
    parser.add_argument('--worker',choices=('project','quiz','count'))
    parser.add_argument('--selection',default='all')
    parser.add_argument('--omit-new',action='store_true')
    args=parser.parse_args()
    worker(args) if args.worker else main(args)
