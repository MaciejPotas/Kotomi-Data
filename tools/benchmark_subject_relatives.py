"""Opt-in release benchmark; use alternating before/after processes on one CPU.

Cold means a freshly loaded project, not an OS cold start. Load is measured
separately; first_question measures SharedQuizEngine.build_question. Each warm
operation has its own project, warm-up and retained samples. No tests import it.
"""
import argparse
import json
import os
from pathlib import Path
import random
import statistics
import sys
from time import perf_counter


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--kotomi', type=Path, required=True)
    parser.add_argument('--data', type=Path, required=True)
    parser.add_argument('--pattern', default='Zdania przydawkowe')
    parser.add_argument('--samples', type=int, default=7)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--operations', nargs='+', choices=['load', 'validation',
        'compatibility', 'exists', 'count', 'first_question', 'next_question', 'render_agreement'],
        help='Optional focused measurement set; default retains the complete B3 benchmark.')
    args = parser.parse_args()
    if args.samples < 1:
        parser.error('--samples must be positive')
    if hasattr(os, 'sched_getaffinity'):
        os.sched_setaffinity(0, {min(os.sched_getaffinity(0))})
    sys.path.insert(0, str(args.kotomi.resolve()))
    from kotomi.application.quiz_project import QuizProject
    from kotomi.application.generation_engine import SharedQuizEngine
    from kotomi.core.generation.models import EngineRequest
    from kotomi.core.generation.compatibility import CompatibilityProbe
    from kotomi.core.generation import rendering
    manifest = args.data.resolve() / 'quiz_project.xml'
    key, form = args.pattern, 'past_negative_plain'
    load = lambda: QuizProject.load(manifest)
    request = EngineRequest(key, form_name=form)
    def operation(p, name):
        engine = SharedQuizEngine(p, random.Random(173))
        if name == 'load': return load
        if name == 'validation': return p.validate
        if name == 'compatibility': return lambda: p.compatible_choices(key, form_name=form)
        if name == 'exists': return lambda: CompatibilityProbe(p, p.analyze_pattern(key), form).exists()
        if name == 'count': return lambda: p.count_possibilities(key, form_name=form)
        if name in ('first_question', 'next_question'):
            if name == 'next_question': engine.build_question(request)
            return lambda: engine.build_question(request)
        if name == 'render_agreement':
            preview = p.build_preview(key, form_name=form)
            word = p.words['verbs'][preview.words['verb@action']]
            noun = p.entities[preview.entities['noun@item']]
            return lambda: rendering._agreement_value(p, word, form, noun.agreement_class, '')
        raise AssertionError(name)
    names = ['load', 'validation', 'compatibility', 'exists', 'count', 'first_question', 'next_question']
    if key.endswith('podmiotowe'): names.append('render_agreement')
    if args.operations: names = args.operations
    output = {'pattern': key, 'samples': args.samples, 'python': sys.version,
              'cpu': sorted(os.sched_getaffinity(0)) if hasattr(os, 'sched_getaffinity') else None,
              'timings': {}}
    for mode in ('cold', 'warm'):
        for name in names:
            p = load(); call = operation(p, name)
            if mode == 'warm': call()
            samples = []
            for _ in range(args.samples):
                if mode == 'cold': call = operation(load(), name)
                start = perf_counter(); value = call(); samples.append((perf_counter() - start) * 1000)
                if name == 'validation': assert value == []
                if name == 'exists': assert value
            output['timings'][mode + '/' + name] = {'median_ms': statistics.median(samples), 'samples_ms': samples}
    args.output.write_text(json.dumps(output, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
