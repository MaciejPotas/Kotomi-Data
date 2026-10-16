"""Opt-in paired C2.2 benchmark. Never imported or invoked by mandatory CI."""
import argparse
import json
import os
from pathlib import Path
import statistics
import subprocess
import sys
import tempfile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--kotomi', type=Path, required=True)
    parser.add_argument('--data', type=Path, required=True)
    parser.add_argument('--baseline-data', type=Path, required=True)
    parser.add_argument('--engine-revision', required=True)
    parser.add_argument('--baseline-revision', required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--rounds', type=int, default=5)
    parser.add_argument('--samples', type=int, default=7)
    parser.add_argument('--patterns', nargs='+', default=['Sam czasownik', 'Czasownik z dopełnieniem',
        'Zdania przydawkowe', 'Zdania przydawkowe podmiotowe'])
    parser.add_argument('--operations', nargs='+', default=['load', 'compatibility', 'exists', 'count', 'first_question'],
                        choices=['load', 'compatibility', 'exists', 'count', 'first_question'])
    args = parser.parse_args()
    if args.rounds < 1 or args.samples < 1:
        parser.error('rounds and samples must be positive')
    evidence = {'engine_revision': args.engine_revision, 'baseline_data_revision': args.baseline_revision,
        'method': 'Sequential paired fresh processes, alternating AB/BA order, fixed PYTHONHASHSEED=173; '
                  'same pinned CPU where supported; cold=fresh project, warm=one priming call; '
                  'no concurrent tests; all samples retained. Ratios are median paired after/before.',
        'rounds': args.rounds, 'samples_per_operation': args.samples, 'results': {}}
    env = {**os.environ, 'PYTHONHASHSEED': '173'}
    driver = Path(__file__).with_name('benchmark_subject_relatives.py')
    with tempfile.TemporaryDirectory(prefix='kotomi-c22-benchmark-') as directory:
        target = Path(directory) / 'sample.json'
        for pattern in args.patterns:
            rounds = []
            for index in range(args.rounds):
                pair = {}
                order = [('before', args.baseline_data), ('after', args.data)]
                if index % 2:
                    order.reverse()
                for label, data in order:
                    subprocess.run([sys.executable, str(driver), '--kotomi', str(args.kotomi),
                        '--data', str(data), '--pattern', pattern, '--samples', str(args.samples),
                        '--operations', *args.operations,
                        '--output', str(target)], check=True, env=env)
                    pair[label] = json.loads(target.read_text(encoding='utf-8'))
                rounds.append(pair)
                print(f'{pattern}: round {index + 1}/{args.rounds}', flush=True)
            ratios = {key: statistics.median(r['after']['timings'][key]['median_ms'] /
                r['before']['timings'][key]['median_ms'] for r in rounds)
                for key in rounds[0]['before']['timings']}
            evidence['results'][pattern] = {'rounds': rounds, 'median_paired_ratios': ratios}
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
            print(ratios, flush=True)


if __name__ == '__main__':
    main()
