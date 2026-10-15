"""B3 release UI smoke using real callbacks with the checkout's fake Kivy controls.
Requires Kotomi development dependencies. Reads the supplied production project;
settings are written only to a temporary directory. No unit test imports this.
"""
import json,sys,random,tempfile
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock
import pytest
import argparse
parser = argparse.ArgumentParser(description='Opt-in B3 release UI smoke with test controls, never a native device test.')
parser.add_argument('--kotomi', type=Path, required=True)
parser.add_argument('--data', type=Path, default=Path(__file__).resolve().parents[1])
parser.add_argument('--output', type=Path, required=True)
args = parser.parse_args()
sys.path[:0] = [str(args.kotomi.resolve()), str(args.kotomi.resolve() / 'tests')]
from kotomi.application.quiz_project import QuizProject
from kotomi.application.generation_engine import SharedQuizEngine
from kotomi.application.instruction_languages import InstructionSelection
from platforms.desktop.studio_base import SimulatorTab
from platforms.mobile import presentation
from apps.grammar import logic,mobile
from apps.availability import mobile as sentence_mobile
from test_mobile_quiz_runtime_smoke import _fake_kivy_modules,_FakeApp,_FakeWindow
p=QuizProject.load(args.data.resolve() / 'quiz_project.xml');assert p.validate()==[]
key='Zdania przydawkowe podmiotowe';forms=p.patterns[key].allowed_forms
rows=[]
with tempfile.TemporaryDirectory() as temp, pytest.MonkeyPatch.context() as patch:
 patch.setattr(presentation,'mobile_font_path',lambda *_:'synthetic-font')
 patch.setattr(sentence_mobile,'mobile_font_path',lambda *_:'synthetic-font')
 for name,module in _fake_kivy_modules().items():patch.setitem(sys.modules,name,module)
 logic.configure_quiz_profile('relative_clauses',project=p);policy=logic.snapshot_quiz_policy()
 policy.quiz_settings_path=lambda:Path(temp)/'settings.xml'
 def unexpected_load(*a,**kw):raise AssertionError('preloaded project must be reused')
 patch.setattr(QuizProject,'load',unexpected_load)
 for restart in range(2):
  controller=mobile.create_embedded_controller(policy)
  controller.instruction_selection=InstructionSelection(p.language_context,p.manifest_path)
  controller.preloaded_project=p;controller.user_data_dir=temp
  patch.setattr(_FakeApp,'_running_app',controller)
  try:
   controller.build();assert controller.engine is not None,controller.engine_error
   for patterns in [['Zdania przydawkowe'],[key],['Zdania przydawkowe',key]]:
    settings=policy.QUIZ_SETTINGS_CLASS(enabled_patterns=patterns,enabled_forms=list(policy.FORM_GROUPS),polite_output=False,plain_output=True)
    assert controller.engine.has_possible_question(settings)
    for _ in range(8):
     q=controller.engine.generate_question(settings);assert q.pattern_id in patterns
    rows.append({'restart':restart,'patterns':patterns,'generated':8})
  finally:
   controller.prepare_for_unload();_FakeWindow._callbacks.clear()
 engine=SharedQuizEngine(p,random.Random(173))
 for form in forms:
  for verb,noun in [('hataraku','hito'),('neru','inu'),('aku','box')]:
   words={'verb@action':verb};entities={'noun@item':noun}
   expected=engine.preview(key,form_name=form,word_choices=words,entity_choices=entities)
   errors=[]
   tab=SimpleNamespace(app=SimpleNamespace(engine=engine,set_status=Mock(),tr=lambda key:key),engine=engine,
      pattern_var=SimpleNamespace(get=lambda:key),_locked_slot_choices=lambda _:(words,entities),
      _selected_form=lambda:form,_choice_scope=lambda:None,_apply_completed_choices=Mock(),
      _refresh_slot_options=Mock(),_show_preview=Mock(),_show_error=errors.append)
   SimulatorTab.generate(tab);assert not errors,errors
   assert (tab.current_preview.source,tab.current_preview.answer)==(expected.source,expected.answer)
report={'mobile_headless':rows,'simulator_bound_examples':12,'preloaded_project_reused':True,
 'limits':'Real production callbacks with fake Kivy/Tk controls. No native Windows/Android device operation.'}
args.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('Mobile: 2 controller lifecycles, 3 pattern selections, 48 questions. Simulator: 12 bound examples. Passed.')
