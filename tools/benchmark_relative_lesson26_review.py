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
from time import perf_counter, process_time


def menu_worker(args):
    """Opt-in real Kivy event loop; never used by CI. No widget doubles.

    SDL offscreen on Linux measures real widgets/layout but is NOT Windows DPI
    verification. Callbacks and timings run on the UI thread. Nested stage
    times are inclusive and must not be summed.
    """
    from contextlib import ExitStack
    from tempfile import TemporaryDirectory
    from unittest.mock import patch
    sys.path.insert(0, str(args.kotomi.resolve()))
    from kivy.app import App
    from kivy.base import EventLoop
    from kivy.core.window import Window
    from platforms.mobile import app as mobile
    from kotomi.application.quiz_project import QuizProject
    from kotomi.application.quiz_registry import discover_apps
    from kotomi.application.settings import AppSettings
    from kotomi.application.storage import SettingsStore
    from kotomi.application.instruction_languages import InstructionSelection
    Window.size = (1366, 768)
    result = {'runtime': 'real Kivy, '+sys.platform, 'openings': []}
    with TemporaryDirectory() as directory, ExitStack() as patches:
        path = Path(directory)/'launcher.xml'
        SettingsStore(path).save(AppSettings(instruction_language_id='pl').to_dict())
        patches.enter_context(patch.object(mobile, 'LAUNCHER_SETTINGS_PATH', path))
        master = mobile.create_master_app_class()()
        App._running_app = master
        master.root = master.build()
        master.instruction_selection = InstructionSelection(
            master.language_context, (args.data/'quiz_project.xml').resolve())
        Window.add_widget(master.root)
        EventLoop.ensure_window()
        descriptor = next(d for d in discover_apps(args.kotomi)[0] if d.id == args.selection)
        for repeat in range(2):
            row = {'stages_ms': {}, 'calls': {}}
            def measured(name, operation):
                def run(*a, **kw):
                    start = perf_counter()
                    try:
                        return operation(*a, **kw)
                    finally:
                        row['stages_ms'][name] = row['stages_ms'].get(name, 0)+(perf_counter()-start)*1000
                        row['calls'][name] = row['calls'].get(name, 0)+1
                return run
            original_loader = mobile.load_app_module
            with ExitStack() as stages:
                def load(*a, **kw):
                    module = measured('module_and_profile', original_loader)(*a, **kw)
                    original_factory = getattr(module, descriptor.factory)
                    def factory():
                        controller = measured('controller', original_factory)()
                        controller.build = measured('widgets_and_engine', controller.build)
                        controller.reload_engine = measured('engine', controller.reload_engine)
                        return controller
                    stages.enter_context(patch.object(module, descriptor.factory, factory))
                    store = getattr(module, 'SETTINGS_STORE_CLASS', module.SettingsStore)
                    stages.enter_context(patch.object(store, 'load', measured('settings', store.load)))
                    return module
                stages.enter_context(patch.object(mobile, 'load_app_module', load))
                stages.enter_context(patch.object(QuizProject, 'load', measured('project_load', QuizProject.load)))
                stages.enter_context(patch.object(QuizProject, 'validate', measured('validation', QuizProject.validate)))
                stages.enter_context(patch.object(QuizProject, 'analyze_pattern', measured('analysis', QuizProject.analyze_pattern)))
                start = perf_counter()
                master.open_quiz(descriptor)
                row['callback_to_popup_ms'] = (perf_counter()-start)*1000
                longest = 0
                while getattr(master, '_quiz_loading', None) is not None:
                    tick = perf_counter(); EventLoop.idle()
                    longest = max(longest, (perf_counter()-tick)*1000)
                    if perf_counter()-start > 12:
                        raise TimeoutError('Menu did not become ready within 12s')
                EventLoop.idle()
                row['ready_ms'] = (perf_counter()-start)*1000
                row['longest_ui_frame_ms'] = longest
                controller = master.active_quiz_controller
                if controller is None:
                    raise RuntimeError(master.update_message)
                start = perf_counter(); controller.open_settings()
                EventLoop.idle(); EventLoop.idle()
                row['settings_navigation_ms'] = (perf_counter()-start)*1000
                if args.menu_layout:
                    from kivy.uix.button import Button
                    from kivy.uix.scrollview import ScrollView
                    screen = controller.manager.get_screen('settings')
                    scroll = next(w for w in screen.walk() if isinstance(w, ScrollView))
                    layout = []
                    for size in ((1366,768), (1093,614), (911,512), (1920,1080)):
                        Window.size = size
                        for _ in range(30): EventLoop.idle()
                        footer = screen.children[0].children[0]
                        buttons = [w for w in footer.walk() if isinstance(w, Button)]
                        assert buttons and all(w.y >= 0 and w.top <= screen.height for w in buttons)
                        scroll.scroll_y = 0
                        for _ in range(3): EventLoop.idle()
                        checks = list(screen.pattern_checks.values())+list(screen.form_checks.values())
                        last = checks[-1]
                        scroll.scroll_to(last, animate=False)
                        for _ in range(3): EventLoop.idle()
                        original = last.active; last.active = not original; last.active = original
                        layout.append({'size':size, 'scrollable':scroll.height < scroll.children[0].height,
                                       'footer_visible':True, 'toggle_preserved':last.active == original})
                    row['layout'] = layout
                if args.menu_start and repeat == 1:
                    start = perf_counter(); controller.start_quiz()
                    while getattr(controller, '_quiz_loading', None) is not None:
                        EventLoop.idle()
                        if perf_counter()-start > 12:
                            raise TimeoutError('Start did not finish within 12s')
                    assert controller.manager.current == 'quiz'
                    row['start_to_question_ms'] = (perf_counter()-start)*1000
            result['openings'].append(row)
            master.return_to_launcher(); EventLoop.idle()
        Window.remove_widget(master.root)
    print(json.dumps(result, ensure_ascii=False))


def worker(args):
    sys.path.insert(0, str(args.kotomi.resolve()))
    from kotomi.application.quiz_project import QuizProject
    from apps.grammar import logic
    result = {}
    def timed(name, operation):
        start = perf_counter()
        cpu = process_time()
        value = operation()
        result[name] = round((perf_counter() - start) * 1000, 3)
        result[name.replace('_ms', '_cpu_ms')] = round((process_time() - cpu) * 1000, 3)
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
        profile = 'grammar' if args.selection == 'old_quiz' else 'relative_clauses'
        logic.configure_quiz_profile(profile, project=p)
        policy = logic.snapshot_quiz_policy()
        if args.selection in ('simple','independent_legacy'):
            key = 'Sam czasownik' if args.selection == 'simple' else 'Trzy lubiane rzeczy'
            policy.QUIZ_SETTINGS_CLASS = type('SimpleSettings', (policy.QUIZ_SETTINGS_CLASS,), {'supported_patterns':(key,)})
            policy.QUIZ_ENGINE_CLASS = type('SimpleEngine', (policy.QUIZ_ENGINE_CLASS,), {'profile_expansions':{}})
        engine = timed('engine_from_preloaded_ms', lambda: policy.QUIZ_ENGINE_CLASS(p.manifest_path, rng=random.Random(26), project=p))
        keys = [k for k in p.sentence_quizzes['relative_clauses'].pattern_ids if k.startswith('Przydawki / ')]
        selected = {'one':['Przydawki / Osoba i dopełnienie'], 'light':['Przydawki / Pragnienie podróży'],
                    'new':keys, 'all':p.sentence_quizzes['relative_clauses'].pattern_ids,
                    'old_quiz':list(policy.PATTERN_LABELS),
                    'old_pattern':['Zdania przydawkowe podmiotowe'], 'simple':['Sam czasownik'], 'independent_legacy':['Trzy lubiane rzeczy']}[args.selection]
        settings = policy.QUIZ_SETTINGS_CLASS(enabled_patterns=selected, enabled_forms=list(policy.FORM_GROUPS), plain_output=True, polite_output=False)
        if args.worker == 'fallback':
            counted = engine.shared_engine.iter_counted_previews
            runs = {'canonical':[], 'weighted':[]}
            for repeat in range(5):
                methods = [('canonical',None),('weighted',counted)]
                if repeat % 2: methods.reverse()
                for name,method in methods:
                    engine.shared_engine.iter_counted_previews = method
                    start = perf_counter()
                    value = engine.statistics(settings)
                    runs[name].append({'statistics_ms':(perf_counter()-start)*1000, 'statistics':value})
            result['fallback_runs'] = runs
        elif args.worker == 'count':
            timed('analysis_ms', lambda: [p.analyze_pattern(key) for selected_id in selected for key in engine.pattern_expansions.get(selected_id,(selected_id,))])
            result['statistics'] = timed('statistics_ms', lambda: engine.statistics(settings))
        else:
            assert timed('availability_ms', lambda: engine.has_possible_question(settings))
            q = timed('first_question_ms', lambda: engine.generate_question(settings))
            assert q.pattern_id in {key for selected_id in selected for key in engine.pattern_expansions.get(selected_id,(selected_id,))}
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


def optimization(args):
    """Opt-in exact release audit: bounded 12s results and separate diagnostics.

    Same declared Content graph for both engines, read-only. Cost follows full
    solver enumeration in the baseline; diagnostic processes have an explicit
    deadline. This mode is never invoked by CI or unit-test collection.
    """
    def launch(code, mode, selection='all', deadline=45):
        command = [sys.executable, str(Path(__file__).resolve()), '--worker', mode,
            '--kotomi', str(code.resolve()), '--data', str(args.data.resolve()),
            '--selection', selection]
        try:
            result = subprocess.run(command, capture_output=True, text=True,
                                    timeout=deadline, check=True)
            return json.loads(result.stdout)
        except subprocess.TimeoutExpired:
            return {'incomplete':True, 'process_timeout_s':deadline, 'total':None}

    if args.startup_recheck:
        samples = {name:{key:[] for key in ('one','new','all','simple','independent_legacy')} for name in ('before','after')}
        for repeat in range(9):
            print('startup recheck',repeat+1,flush=True)
            engines = [('before',args.before_kotomi),('after',args.kotomi)]
            if repeat % 2: engines.reverse()
            for selection in ('one','new','all','simple','independent_legacy'):
                for name,code in engines:
                    samples[name][selection].append(launch(code,'quiz',selection))
        simple_counts = {name:launch(code,'count','simple',12) for name,code in engines}
        assert simple_counts['before']['statistics'] == simple_counts['after']['statistics']
        legacy_counts = {name:launch(code,'count','independent_legacy',12) for name,code in engines}
        legacy_diagnostics = {}
        for name,code in engines:
            if legacy_counts[name].get('incomplete') and args.diagnostic_timeout:
                print('diagnostic',name,'independent_legacy',flush=True)
                legacy_diagnostics[name] = launch(code,'count','independent_legacy',args.diagnostic_timeout)
        counts = [legacy_diagnostics.get(name,legacy_counts[name]).get('statistics') for name,_ in engines]
        if all(counts): assert counts[0] == counts[1]
        previous = json.loads(args.output.read_text())
        previous['counting_optimization']['startup_recheck'] = {
            'method':'Nine fresh-process samples per engine/scenario, alternating AB/BA order for each pair, including CPU time to distinguish scheduler noise. Triggered by variable startup wall times in the initial three samples; no generation code was changed.',
            'samples':samples, 'simple_statistics':simple_counts,
            'independent_legacy_bounded':legacy_counts, 'independent_legacy_diagnostic':legacy_diagnostics}
        args.output.write_text(json.dumps(previous,ensure_ascii=False,indent=2)+'\n')
        return

    result = {'method':'Same Content and interpreter, sequential fresh processes. Three paired project/first-question samples; one exact count sample per engine/scenario. The 12s process deadline includes imports/load/analysis. Longer diagnostic counts are separate and are NOT evidence of meeting the 12s deadline. No extrapolation or approximate totals.',
        'baseline_heads':{'Kotomi':'9f9161e0968c370a39b3de85ee3669d8ed21cffe',
                          'Kotomi-Data':'f41bb61ed4f39fea39e170656b2c218d7a3497a1'},
        'project':{}, 'quiz':{}, 'bounded_statistics':{}, 'diagnostic_statistics':{}}
    engines = [('before',args.before_kotomi),('after',args.kotomi)]
    selections = ('light','one','new','all','old_quiz','old_pattern')
    def checkpoint():
        previous = json.loads(args.output.read_text()) if args.output.exists() else {}
        previous['counting_optimization'] = result
        args.output.write_text(json.dumps(previous,ensure_ascii=False,indent=2)+'\n')
    for name,_ in engines:
        result['project'][name] = []
        result['quiz'][name] = {key:[] for key in selections}
        result['bounded_statistics'][name] = {}
        result['diagnostic_statistics'][name] = {}
    for repeat in range(3):
        for name,code in engines:
            print('project',repeat,name,flush=True)
            result['project'][name].append(launch(code,'project'))
            for selection in selections:
                result['quiz'][name][selection].append(launch(code,'quiz',selection))
        checkpoint()
    for selection in selections:
        for name,code in engines:
            print('bounded',name,selection,flush=True)
            row = launch(code,'count',selection,12)
            result['bounded_statistics'][name][selection] = row
            checkpoint()
        if args.diagnostic_timeout:
            for name,code in engines:
                row = result['bounded_statistics'][name][selection]
                if row.get('incomplete'):
                    print('diagnostic',name,selection,flush=True)
                    result['diagnostic_statistics'][name][selection] = launch(
                        code,'count',selection,args.diagnostic_timeout)
                    checkpoint()
        counts=[]
        for name,_ in engines:
            row = result['diagnostic_statistics'][name].get(selection,
                    result['bounded_statistics'][name][selection])
            if 'statistics' in row:
                counts.append(row['statistics'])
        if len(counts)==2:
            assert counts[0] == counts[1], (selection,counts)
    checkpoint()


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ('kotomi','data','before-kotomi','before-data','main-data','output'):
        parser.add_argument('--'+name,type=Path)
    parser.add_argument('--worker',choices=('project','quiz','count','fallback','menu'))
    parser.add_argument('--selection',default='all')
    parser.add_argument('--omit-new',action='store_true')
    parser.add_argument('--optimization',action='store_true')
    parser.add_argument('--startup-recheck',action='store_true')
    parser.add_argument('--menu-layout',action='store_true')
    parser.add_argument('--menu-start',action='store_true')
    parser.add_argument('--diagnostic-timeout',type=float,default=0)
    args=parser.parse_args()
    menu_worker(args) if args.worker == 'menu' else worker(args) if args.worker else (optimization(args) if args.optimization else main(args))
