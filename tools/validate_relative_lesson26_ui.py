"""Opt-in headless release smoke, not a native Windows/Android device test.

Uses production content with fake Kivy controls. Only bounded question generation
is performed: one per configured new pattern, then a small mixed selection.
"""
import argparse,json,random,sys,tempfile
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--kotomi',type=Path,required=True)
    parser.add_argument('--data',type=Path,default=Path(__file__).resolve().parents[1])
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    sys.path[:0]=[str(args.kotomi.resolve()),str(args.kotomi.resolve()/'tests')]
    import pytest
    from platforms.mobile import presentation
    # All widgets are fake; this tool does not inspect or render a font.
    with pytest.MonkeyPatch.context() as patch, tempfile.TemporaryDirectory() as temp:
        patch.setattr(presentation,'mobile_font_path',lambda *_:'headless-fixture-font')
        from test_mobile_quiz_runtime_smoke import _fake_kivy_modules,_FakeApp,_FakeWindow
        from apps.grammar import logic,mobile
        from kotomi.application.quiz_project import QuizProject
        from kotomi.application.instruction_languages import InstructionSelection
        from kotomi.application.generation_engine import SharedQuizEngine
        from platforms.desktop.studio_base import SimulatorTab
        from validate_relative_lesson26 import CASES
        for name,module in _fake_kivy_modules().items():patch.setitem(sys.modules,name,module)
        p=QuizProject.load(args.data.resolve()/'quiz_project.xml')
        logic.configure_quiz_profile('relative_clauses',project=p); policy=logic.snapshot_quiz_policy()
        policy.quiz_settings_path=lambda:Path(temp)/'settings.xml'
        controller=mobile.create_embedded_controller(policy)
        controller.instruction_selection=InstructionSelection(p.language_context,p.manifest_path)
        controller.preloaded_project=p;controller.user_data_dir=temp
        patch.setattr(_FakeApp,'_running_app',controller)
        def unexpected_load(*a,**kw):raise AssertionError('must reuse preloaded project')
        patch.setattr(QuizProject,'load',unexpected_load)
        rows=[]
        try:
            controller.build();assert controller.engine is not None,controller.engine_error
            keys=[k for k in p.sentence_quizzes['relative_clauses'].pattern_ids if k.startswith('Przydawki / ')]
            for selected in [[k] for k in keys]+[keys,p.sentence_quizzes['relative_clauses'].pattern_ids]:
                settings=policy.QUIZ_SETTINGS_CLASS(enabled_patterns=selected,enabled_forms=list(policy.FORM_GROUPS),plain_output=True,polite_output=False)
                assert controller.engine.has_possible_question(settings),selected
                question=controller.engine.generate_question(settings)
                assert question.pattern_id in selected
                assert question.source_sentence and question.expected_answer
                rows.append({'selection':selected,'generated_pattern':question.pattern_id})
            engine=SharedQuizEngine(p,random.Random(26))
            for title,form,verb,nouns,extra,source,answer in CASES:
                key='Przydawki / '+title
                words={**({'verb@action':verb} if verb else {}),**extra}
                entities={'noun@'+k:v for k,v in nouns.items()}
                errors=[]
                tab=SimpleNamespace(app=SimpleNamespace(engine=engine,set_status=Mock(),tr=lambda key:key),engine=engine,
                    pattern_var=SimpleNamespace(get=lambda:key),_locked_slot_choices=lambda _:(words,entities),
                    _selected_form=lambda:form,_choice_scope=lambda:None,_apply_completed_choices=Mock(),
                    _refresh_slot_options=Mock(),_show_preview=Mock(),_show_error=errors.append)
                SimulatorTab.generate(tab);assert not errors,errors
                assert (tab.current_preview.source,tab.current_preview.answer)==(source,answer)
        finally:
            controller.prepare_for_unload();_FakeWindow._callbacks.clear()
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps({'mobile':rows,'simulator_exact_pairs':len(CASES),
        'limits':'Fake widgets and font. No native device UI or APK build. No full production Cartesian count.'},ensure_ascii=False,indent=2)+'\n')
    print(f'Passed {len(rows)} Mobile selections and {len(CASES)} exact simulator pairs.')

if __name__=='__main__':main()
