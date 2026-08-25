"""Kivy presentation for the Verbs quiz.

All settings, filtering, generation, statistics, and session behavior comes
from :mod:`logic`. This module owns mobile rendering, interaction, hints, and
update controls.
"""

from __future__ import annotations

from pathlib import Path
import re
import sys
import threading
from typing import Dict, List, Optional, Set


SCRIPT_DIR = Path(__file__).resolve().parent
INSTALL_ROOT = SCRIPT_DIR.parents[1]
if str(INSTALL_ROOT) not in sys.path:
    sys.path.insert(0, str(INSTALL_ROOT))

from apps.verbs.logic import *
from apps.verbs.logic import _safe_float, _safe_int
from kotomi_core.project import ProjectError
from kotomi_core.settings_xml import settings_path
from kotomi_core.paths import FONTS_DIR
from kotomi_ui.mobile import (
    FocusRequest,
    MOBILE_BUTTON_BACKGROUND,
    MOBILE_BUTTON_TEXT,
    MOBILE_CORRECT_BACKGROUND,
    MOBILE_QUIZ_LAYOUT,
    MOBILE_WRONG_BACKGROUND,
    MobileReviewInputMixin,
    fitted_compact_text_layout,
    format_grammatical_hint_entry,
    format_mobile_hint_entries,
    format_mobile_hint_entry,
    mobile_font_path,
    scaled_button_height,
    validate_mobile_button_scale,
)
from kotomi_core.app_identity import (
    app_icon_png_path,
    apply_kivy_window_icon,
    configure_windows_app_id,
)
from kotomi_core.mobile_i18n import mobile_error_text, mobile_text
from kotomi_core.update_transport import QuizUpdater, UpdateError, load_update_url


MOBILE_FONT = mobile_font_path(FONTS_DIR)


def mobile_sentence_hint_items(
    question: VerbQuestion,
    project: object,
) -> List[str]:
    """Resolve the vocabulary used by a mobile question without revealing it.

    The specialized desktop quiz keeps its existing hint presentation.  This
    small adapter is consumed only by the Kivy screen and turns the engine's
    completed bindings into compact dictionary-form Japanese vocabulary.
    """

    bindings: List[tuple[str, str]] = []
    for binding in re.split(r"[,;]", question.bindings or ""):
        slot, separator, identifiers = binding.strip().partition("=")
        if not separator:
            continue
        for identifier in identifiers.split("+"):
            selected = (slot.strip(), identifier.strip())
            if selected[1] and selected not in bindings:
                bindings.append(selected)

    dictionaries = getattr(project, "words", {})
    entities = getattr(project, "entities", {})
    slots = {}
    try:
        slots = project.analyze_pattern(question.pattern_id).slots
    except (AttributeError, KeyError, ValueError, ProjectError):
        slots = {}

    result: List[tuple[str, str, str]] = []
    seen: set[tuple[str, str]] = set()

    def append_item(item: object, key: tuple[str, str]) -> None:
        if item is None or key in seen:
            return
        seen.add(key)
        kana = str(getattr(item, "kana", "") or "").strip()
        kanji = str(getattr(item, "kanji", "") or "").strip()
        translation = str(
            getattr(item, "translation", "") or ""
        ).strip()
        if kana.casefold() == "n/a":
            kana = ""
        if kanji.casefold() == "n/a":
            kanji = ""
        if translation.casefold() == "n/a":
            translation = ""
        if translation or kana or kanji:
            formatted = format_grammatical_hint_entry(item)
            if formatted and formatted not in result:
                result.append(formatted)

    # Context is selected during generation and carried explicitly. Never
    # infer it by scanning prompt or answer text.
    context_entry = (
        str(question.context_translation or "").strip(),
        str(question.context_kana or "").strip().rstrip(" 、。"),
        "",
    )
    if any(context_entry):
        formatted_context = format_mobile_hint_entry(context_entry)
        if formatted_context and formatted_context not in result:
            result.append(formatted_context)

    for slot, identifier in bindings:
        slot_definition = slots.get(slot)
        item = None
        dictionary_id = ""
        if getattr(slot_definition, "kind", "") == "entity":
            item = entities.get(identifier)
            dictionary_id = "entity"
        else:
            dictionary_id = str(
                getattr(slot_definition, "dictionary", "") or ""
            )
            item = dictionaries.get(dictionary_id, {}).get(identifier)
        if item is None:
            for candidate_id, dictionary in dictionaries.items():
                if identifier in dictionary:
                    item = dictionary[identifier]
                    dictionary_id = str(candidate_id)
                    break
        if item is None:
            item = entities.get(identifier)
            dictionary_id = "entity"
        append_item(item, (dictionary_id, identifier))

    if not result:
        fallback = type("MobileHintWord", (), {
            "translation": question.word_meaning,
            "kana": question.word_kana,
            "kanji": question.word_kanji,
        })()
        append_item(fallback, ("verbs", question.word_id))
    return result

def create_app_class():
    configure_windows_app_id()
    """Import Kivy lazily and return the mobile application class."""
    from kivy.app import App
    from kivy.clock import Clock
    from kivy.core.text import Label as CoreLabel
    from kivy.core.window import Window
    from kivy.metrics import dp, sp
    from kivy.uix.anchorlayout import AnchorLayout
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.button import Button
    from kivy.uix.label import Label
    from kivy.uix.progressbar import ProgressBar
    from kivy.uix.screenmanager import (
        Screen,
        ScreenManager,
        SlideTransition,
    )
    from kivy.uix.scrollview import ScrollView
    from kivy.uix.slider import Slider
    from kivy.uix.spinner import Spinner
    from kivy.uix.textinput import TextInput
    from kivy.uix.widget import Widget
    from kivy.utils import escape_markup

    def quiz_app():
        """Return the quiz controller in standalone or master mode."""
        running_app = App.get_running_app()
        controller = getattr(running_app, "active_quiz_controller", None)
        return controller or running_app

    def tr(key: str, **values: object) -> str:
        """Translate mobile chrome using the launcher-selected language."""
        return mobile_text(quiz_app(), key, **values)

    def mode_label(mode: str) -> str:
        key = (
            "specialized.mode.transform_japanese"
            if mode == MODE_TRANSFORMATION
            else "specialized.mode.write_japanese"
        )
        return tr(key)

    def target_label(question: VerbQuestion) -> str:
        for group_id, group in FORM_GROUPS.items():
            for style_id in ("plain", "polite"):
                if question.target_form == str(group[style_id]):
                    return (
                        f"{tr(f'specialized.form_group.{group_id}')}, "
                        f"{tr(f'specialized.{style_id}')}"
                    )
        return question.target_label

    def settings_summary(settings: VerbQuizSettings) -> str:
        forms = ", ".join(
            tr(f"specialized.form_group.{name}")
            for name in settings.enabled_forms
        )
        patterns = ", ".join(
            tr(f"specialized.pattern.{name}")
            for name in settings.enabled_patterns
        )
        return "\n".join(
            (
                mode_label(settings.mode),
                f"{tr('specialized.question_count')}: {settings.question_count}",
                f"{tr('specialized.tab.forms')}: {forms}",
                f"{tr('specialized.tab.patterns')}: {patterns}",
                f"{tr('specialized.text_scale')}: {round(settings.font_scale * 100)}%; "
                f"{tr('specialized.button_scale')}: "
                f"{round(settings.mobile_button_scale * 100)}%",
            )
        )

    def return_to_quiz_menu() -> bool:
        """Return an embedded quiz to Kotomi's main quiz selector."""
        controller = quiz_app()
        host_callback = getattr(controller, "host_quiz_menu_callback", None)
        if callable(host_callback):
            host_callback()
            return True
        running_app = App.get_running_app()
        fallback = getattr(running_app, "return_to_launcher", None)
        if callable(fallback) and getattr(controller, "embedded_mode", False):
            fallback()
            return True
        return False

    def leave_quiz() -> None:
        """Return to the host selector, or stop only in standalone mode."""
        if not return_to_quiz_menu():
            quiz_app().stop()

    Window.clearcolor = (1, 1, 1, 1)
    try:
        Window.softinput_mode = "resize"
    except Exception:
        pass

    label_color = (0.12, 0.12, 0.12, 1)
    button_background = (0.92, 0.92, 0.92, 1)
    button_text = (0.0, 0.0, 0.0, 1)
    accent_ok = (0.10, 0.45, 0.15, 1)
    accent_bad = (0.65, 0.10, 0.10, 1)
    accent_info = (0.15, 0.20, 0.55, 1)
    input_active_background = (1.0, 1.0, 1.0, 1.0)
    input_correct_background = (0.84, 0.96, 0.87, 1.0)
    input_wrong_background = (1.0, 0.86, 0.86, 1.0)
    hint_active_background = (0.76, 0.88, 0.97, 1.0)
    font_scale_state = {"value": 1.0}
    button_scale_state = {"value": 1.0}

    def polish_font() -> str:
        return MOBILE_FONT

    def japanese_font() -> str:
        return MOBILE_FONT

    def current_font_scale() -> float:
        return float(font_scale_state["value"])

    def scaled_font_size(value: float) -> float:
        return float(value) * current_font_scale()

    def current_button_scale() -> float:
        return float(button_scale_state["value"])

    def mobile_button_height(base_height: float) -> float:
        return dp(
            scaled_button_height(base_height, current_button_scale())
        )

    def mobile_action_row(
        base_height: float,
        **kwargs,
    ) -> BoxLayout:
        kwargs.setdefault("size_hint_y", None)
        kwargs.setdefault("spacing", dp(6))
        kwargs["height"] = mobile_button_height(base_height)
        row = BoxLayout(**kwargs)
        row._mobile_action_base_height = float(base_height)
        return row

    class PolishLabel(Label):
        def __init__(self, **kwargs):
            kwargs.setdefault("font_name", polish_font())
            kwargs.setdefault("color", label_color)
            if "font_size" in kwargs:
                kwargs["font_size"] = scaled_font_size(
                    kwargs["font_size"]
                )
            super().__init__(**kwargs)

    class JapaneseLabel(Label):
        def __init__(self, **kwargs):
            kwargs.setdefault("font_name", japanese_font())
            kwargs.setdefault("color", label_color)
            if "font_size" in kwargs:
                kwargs["font_size"] = scaled_font_size(
                    kwargs["font_size"]
                )
            super().__init__(**kwargs)

    class AdaptiveSingleLineLabel(Label):
        """Fit long mixed-language text inside a permanently fixed slot."""

        def __init__(self, **kwargs):
            self._base_preferred_font_sp = float(
                kwargs.pop("preferred_font_sp", 18.0)
            )
            self._base_minimum_font_sp = float(
                kwargs.pop("minimum_font_sp", 10.0)
            )
            self._maximum_fit_lines = max(
                1, int(kwargs.pop("maximum_fit_lines", 1))
            )
            self._fit_plain_text = str(
                kwargs.pop("fit_plain_text", kwargs.get("text", ""))
            )
            self._font_fit_running = False
            kwargs.setdefault("font_name", japanese_font())
            kwargs.setdefault("color", label_color)
            kwargs.setdefault("halign", "left")
            kwargs.setdefault("valign", "middle")
            kwargs.setdefault("shorten", False)
            kwargs["font_size"] = sp(
                scaled_font_size(self._base_preferred_font_sp)
            )
            super().__init__(**kwargs)
            self._quiz_base_font_size = sp(self._base_preferred_font_sp)
            self.bind(width=self._fit_font_to_width, text=self._fit_font_to_width)
            Clock.schedule_once(self._fit_font_to_width, 0)

        def set_fitted_text(self, markup_text: str, plain_text: str) -> None:
            # Every mobile slot is one physical line.  Removing embedded line
            # breaks also prevents a stale second texture line from drawing
            # over the following question on Android.
            self._fit_plain_text = str(plain_text).replace("\r", " ").replace(
                "\n", " "
            )
            fitted_markup = str(markup_text).replace("\r", " ").replace(
                "\n", " "
            )
            self.text = ""
            self.text = fitted_markup
            self._fit_font_to_width()

        def _fit_font_to_width(self, *_args) -> None:
            if self._font_fit_running:
                return
            available_width = max(0.0, self.width - dp(4))
            if available_width <= 0:
                return
            height_sp = self.height / max(sp(1.0), 0.01)
            preferred_sp = min(
                scaled_font_size(self._base_preferred_font_sp),
                height_sp * 0.80,
            )
            # Font scaling expresses preference, not permission to crop a
            # fixed mobile row. Keep the readability floor independent from
            # the user scale and constrain the final size by line height.
            minimum_sp = min(self._base_minimum_font_sp, preferred_sp)
            self._font_fit_running = True
            try:
                probe = CoreLabel(
                    text=self._fit_plain_text,
                    font_name=self.font_name,
                    font_size=sp(preferred_sp),
                )
                probe.refresh()
                fitted_lines, fitted_sp = fitted_compact_text_layout(
                    float(probe.texture.size[0]),
                    available_width,
                    preferred_sp=preferred_sp,
                    minimum_sp=minimum_sp,
                    maximum_lines=self._maximum_fit_lines,
                )
                fitted_sp = min(
                    fitted_sp,
                    height_sp * 0.80 / max(1, fitted_lines),
                )
                # The full question must remain visible.  Ellipsis would hide
                # exactly the part the learner needs to translate.
                self.shorten = False
                if hasattr(self, "max_lines"):
                    self.max_lines = 1
                self.font_size = sp(fitted_sp)
                self.text_size = (available_width, max(0.0, self.height))
            finally:
                self._font_fit_running = False

    class PolishButton(Button):
        def __init__(self, **kwargs):
            kwargs.setdefault("font_name", polish_font())
            kwargs.setdefault("background_normal", "")
            kwargs.setdefault("background_color", button_background)
            kwargs.setdefault("color", button_text)
            base_height = kwargs.get("height")
            if base_height is not None:
                kwargs["height"] = mobile_button_height(base_height)
            if "font_size" in kwargs:
                kwargs["font_size"] = scaled_font_size(
                    kwargs["font_size"]
                )
            super().__init__(**kwargs)
            if base_height is not None:
                self._mobile_button_base_height = float(base_height)

    class PolishInput(TextInput):
        def __init__(self, **kwargs):
            kwargs.setdefault("font_name", polish_font())
            if "font_size" in kwargs:
                kwargs["font_size"] = scaled_font_size(
                    kwargs["font_size"]
                )
            super().__init__(**kwargs)

    class MobileSettingToggle(PolishButton):
        """A full-width settings toggle with a phone-sized touch target."""

        def __init__(self, setting_text: str, active: bool = True, **kwargs):
            self.setting_text = setting_text
            self._active = bool(active)
            self._setting_callback = kwargs.pop("setting_callback", None)
            kwargs.setdefault("size_hint_y", None)
            kwargs.setdefault("height", 64)
            kwargs.setdefault("font_size", 19)
            kwargs.setdefault("halign", "left")
            kwargs.setdefault("valign", "middle")
            super().__init__(**kwargs)
            self.bind(
                size=lambda instance, _value: setattr(
                    instance, "text_size", instance.size
                ),
                on_release=lambda *_: self.toggle(),
            )
            self._refresh_state()

        @property
        def active(self) -> bool:
            return self._active

        @active.setter
        def active(self, value: bool) -> None:
            self._active = bool(value)
            self._refresh_state()

        def toggle(self) -> None:
            self.active = not self.active
            if callable(self._setting_callback):
                self._setting_callback(self.active)

        def _refresh_state(self) -> None:
            self.text = (
                f"✓  {self.setting_text}"
                if self._active
                else f"     {self.setting_text}"
            )
            self.background_color = (
                hint_active_background if self._active else button_background
            )

    class PolishSpinner(Spinner):
        def __init__(self, **kwargs):
            kwargs.setdefault("font_name", polish_font())
            kwargs.setdefault("option_cls", PolishButton)
            if "font_size" in kwargs:
                kwargs["font_size"] = scaled_font_size(
                    kwargs["font_size"]
                )
            super().__init__(**kwargs)

    class JapaneseInput(MobileReviewInputMixin, TextInput):
        def __init__(self, **kwargs):
            kwargs.setdefault("font_name", japanese_font())
            kwargs.setdefault("background_color", (1, 1, 1, 1))
            kwargs.setdefault("foreground_color", (0, 0, 0, 1))
            kwargs.setdefault("multiline", False)
            kwargs.setdefault("unfocus_on_touch", False)
            kwargs.setdefault("text_validate_unfocus", False)
            kwargs.setdefault("write_tab", False)
            if "font_size" in kwargs:
                kwargs["font_size"] = scaled_font_size(
                    kwargs["font_size"]
                )
            super().__init__(**kwargs)

    def wrap_label(label: Label) -> None:
        label.bind(size=lambda instance, _value: setattr(
            instance,
            "text_size",
            instance.size,
        ))

    def constrain_single_line(label: Label) -> None:
        """Clip a reserved mobile row horizontally instead of wrapping it."""
        label.shorten = True
        if hasattr(label, "max_lines"):
            label.max_lines = 1
        wrap_label(label)

    def setting_row(
        text: str,
        active: bool,
        callback,
    ) -> tuple[BoxLayout, MobileSettingToggle]:
        row = BoxLayout(size_hint_y=None, height=mobile_button_height(64))
        row._mobile_action_base_height = 64
        toggle = MobileSettingToggle(
            setting_text=text,
            active=active,
            setting_callback=callback,
        )
        row.add_widget(toggle)
        return row, toggle

    class HomeScreen(Screen):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            embedded_mode = bool(
                getattr(quiz_app(), "embedded_mode", False)
            )
            root = BoxLayout(
                orientation="vertical",
                padding=24,
                spacing=14,
            )
            root.add_widget(
                PolishLabel(
                    text="Kotomi",
                    font_size=34,
                    size_hint_y=None,
                    height=54,
                )
            )
            root.add_widget(
                JapaneseLabel(
                    text="どうしのクイズ",
                    font_size=28,
                    size_hint_y=None,
                    height=46,
                )
            )
            self.summary = PolishLabel(
                text="",
                font_size=19,
                halign="left",
                valign="middle",
                size_hint_y=None,
                height=150,
            )
            wrap_label(self.summary)
            root.add_widget(self.summary)

            self.start_button = PolishButton(
                text=tr("specialized.start_quiz"),
                font_size=24,
                size_hint_y=None,
                height=76,
            )
            self.start_button.bind(
                on_release=lambda *_: quiz_app().start_quiz()
            )
            root.add_widget(self.start_button)
            settings_button = PolishButton(
                text=tr("action.settings"),
                font_size=22,
                size_hint_y=None,
                height=70,
            )
            settings_button.bind(
                on_release=lambda *_: quiz_app().open_settings()
            )
            root.add_widget(settings_button)
            help_button = PolishButton(
                text=tr("specialized.help"),
                font_size=22,
                size_hint_y=None,
                height=70,
            )
            help_button.bind(
                on_release=lambda *_: quiz_app().open_help()
            )
            root.add_widget(help_button)
            exit_button = PolishButton(
                text=(
                    tr("specialized.launcher_menu")
                    if embedded_mode
                    else tr("specialized.exit")
                ),
                font_size=22,
                size_hint_y=None,
                height=70,
            )
            exit_button.bind(
                on_release=lambda *_: leave_quiz()
            )
            root.add_widget(exit_button)
            root.add_widget(Widget())
            self.add_widget(root)

        def on_pre_enter(self, *_args):
            app = quiz_app()
            self.summary.text = app.home_summary()
            self.start_button.disabled = app.restart_required

        def show_update_state(self) -> None:
            app = quiz_app()
            self.summary.text = app.home_summary()
            self.start_button.disabled = app.restart_required

    class SettingsScreen(Screen):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.form_checks: Dict[str, MobileSettingToggle] = {}
            self.pattern_checks: Dict[str, MobileSettingToggle] = {}
            self.value_checks: Dict[str, MobileSettingToggle] = {}

            root = BoxLayout(
                orientation="vertical",
                padding=dp(8),
                spacing=dp(8),
            )
            scroll = ScrollView(
                do_scroll_x=False,
                do_scroll_y=True,
                scroll_type=["content", "bars"],
                bar_width=dp(12),
            )
            self.content = BoxLayout(
                orientation="vertical",
                padding=dp(4),
                spacing=dp(8),
                size_hint_y=None,
            )
            self.content.bind(
                minimum_height=self.content.setter("height")
            )
            self.content.add_widget(
                PolishLabel(
                    text=(
                        f"{tr('specialized.verbs_title')} "
                        f"{tr('specialized.settings_suffix')}"
                    ),
                    font_size=24,
                    size_hint_y=None,
                    height=48,
                )
            )
            self._section(tr("specialized.question_type"))
            self.mode_spinner = PolishSpinner(
                text=mode_label(MODE_POLISH_TO_JAPANESE),
                values=[mode_label(mode) for mode in MODE_LABELS],
                font_size=19,
                size_hint_y=None,
                height=64,
            )
            self.content.add_widget(self.mode_spinner)

            self._section(tr("specialized.direction"))
            self._boolean_row(
                "polite_to_plain",
                tr("specialized.polite_to_plain"),
            )
            self._boolean_row(
                "plain_to_polite",
                tr("specialized.plain_to_polite"),
            )

            self._section(tr("specialized.answer_style"))
            self._boolean_row("plain_output", tr("specialized.plain"))
            self._boolean_row("polite_output", tr("specialized.polite"))

            self._section(tr("specialized.tab.forms"))
            for form_id, form in FORM_GROUPS.items():
                row, checkbox = setting_row(
                    tr(f"specialized.form_group.{form_id}"),
                    True,
                    lambda _value: None,
                )
                self.form_checks[form_id] = checkbox
                self.content.add_widget(row)

            self._section(tr("specialized.tab.patterns"))
            for pattern_id, label_text in PATTERN_LABELS.items():
                row, checkbox = setting_row(
                    tr(f"specialized.pattern.{pattern_id}"),
                    True,
                    lambda _value: None,
                )
                self.pattern_checks[pattern_id] = checkbox
                self.content.add_widget(row)

            self._section(tr("specialized.word_filter"))
            filter_help = PolishLabel(
                text=tr(
                    "specialized.word_filter_help",
                    example="ending=su,ru;type=godan",
                ),
                font_size=15,
                halign="left",
                valign="middle",
                size_hint_y=None,
                height=70,
            )
            wrap_label(filter_help)
            self.content.add_widget(filter_help)
            self.word_filter = PolishInput(
                multiline=False,
                font_size=18,
                size_hint_y=None,
                height=64,
                hint_text="ending=su,ru;type=godan",
            )
            self.content.add_widget(self.word_filter)

            self._section(tr("specialized.flow"))
            font_row = BoxLayout(
                orientation="vertical",
                size_hint_y=None,
                height=96,
                spacing=dp(4),
            )
            font_title = BoxLayout(size_hint_y=None, height=36)
            font_label = PolishLabel(
                text=tr("specialized.text_scale"),
                font_size=18,
                halign="left",
                valign="middle",
            )
            wrap_label(font_label)
            self.font_scale_slider = Slider(
                min=0.7,
                max=1.6,
                step=0.05,
                value=1.0,
            )
            self.font_scale_value = PolishLabel(
                text="100%",
                font_size=18,
                size_hint_x=None,
                width=72,
            )
            self.font_scale_slider.bind(
                value=self._font_scale_changed
            )
            font_title.add_widget(font_label)
            font_title.add_widget(self.font_scale_value)
            font_row.add_widget(font_title)
            font_row.add_widget(self.font_scale_slider)
            self.content.add_widget(font_row)
            button_row = BoxLayout(
                orientation="vertical",
                size_hint_y=None,
                height=dp(96),
                spacing=dp(4),
            )
            button_title = BoxLayout(size_hint_y=None, height=dp(36))
            button_label = PolishLabel(
                text=tr("specialized.button_scale"),
                font_size=18,
                halign="left",
                valign="middle",
            )
            wrap_label(button_label)
            self.mobile_button_scale_slider = Slider(
                min=0.8,
                max=1.6,
                step=0.05,
                value=1.0,
            )
            self.mobile_button_scale_value = PolishLabel(
                text="100%",
                font_size=18,
                size_hint_x=None,
                width=dp(72),
            )
            self.mobile_button_scale_slider.bind(
                value=self._mobile_button_scale_changed
            )
            button_title.add_widget(button_label)
            button_title.add_widget(self.mobile_button_scale_value)
            button_row.add_widget(button_title)
            button_row.add_widget(self.mobile_button_scale_slider)
            self.content.add_widget(button_row)
            self.question_count = self._number_input(
                tr("specialized.question_count"),
            )
            self.auto_advance = self._number_input(
                tr("specialized.auto_advance"),
                decimal=True,
            )

            statistics_button = PolishButton(
                text=tr("specialized.calculate_options"),
                font_size=19,
                size_hint_y=None,
                height=62,
            )
            statistics_button.bind(
                on_release=lambda *_: self.calculate_statistics()
            )
            self.content.add_widget(statistics_button)
            self.statistics = PolishLabel(
                text="",
                color=accent_info,
                font_size=17,
                halign="left",
                valign="middle",
                size_hint_y=None,
                height=120,
            )
            wrap_label(self.statistics)
            self.content.add_widget(self.statistics)

            if not getattr(quiz_app(), "embedded_mode", False):
                self._section(tr("settings.updates"))
                self.settings_check_update_button = PolishButton(
                    text=tr("action.check_updates"),
                    font_size=19,
                    size_hint_y=None,
                    height=62,
                )
                self.settings_check_update_button.bind(
                    on_release=lambda *_: quiz_app().check_for_updates()
                )
                self.content.add_widget(self.settings_check_update_button)
                self.settings_update_button = PolishButton(
                    text=tr("action.update"),
                    font_size=19,
                    size_hint_y=None,
                    height=62,
                )
                self.settings_update_button.bind(
                    on_release=lambda *_: quiz_app().update_quiz()
                )
                self.content.add_widget(self.settings_update_button)
                self.update_status = PolishLabel(
                    text=tr("settings.update_not_checked"),
                    color=accent_info,
                    font_size=16,
                    halign="left",
                    valign="middle",
                    size_hint_y=None,
                    height=64,
                )
                wrap_label(self.update_status)
                self.content.add_widget(self.update_status)
            else:
                self.settings_check_update_button = None
                self.settings_update_button = None
                self.update_status = None

            self.status = PolishLabel(
                text="",
                color=accent_bad,
                font_size=17,
                halign="left",
                valign="middle",
                size_hint_y=None,
                height=70,
            )
            wrap_label(self.status)
            self.content.add_widget(self.status)
            scroll.add_widget(self.content)
            root.add_widget(scroll)

            buttons = BoxLayout(
                orientation="vertical",
                size_hint_y=None,
                height=mobile_button_height(136) + dp(8),
                spacing=dp(8),
            )
            buttons._mobile_action_base_height = 144
            save_row = mobile_action_row(68, spacing=dp(8))
            save = PolishButton(text=tr("action.save"), font_size=19)
            save.bind(on_release=lambda *_: self.save(False))
            save_start = PolishButton(
                text=tr("specialized.save_start"),
                font_size=18,
            )
            save_start.bind(on_release=lambda *_: self.save(True))
            back = PolishButton(text=tr("action.back"), font_size=19)
            back.bind(
                on_release=lambda *_: quiz_app().go_home()
            )
            save_row.add_widget(save)
            save_row.add_widget(save_start)
            buttons.add_widget(save_row)
            back_row = mobile_action_row(68)
            back_row.add_widget(back)
            buttons.add_widget(back_row)
            root.add_widget(buttons)
            self.add_widget(root)

        def _section(self, text: str) -> None:
            label = PolishLabel(
                text=text,
                color=accent_info,
                font_size=21,
                halign="left",
                valign="middle",
                size_hint_y=None,
                height=48,
            )
            wrap_label(label)
            self.content.add_widget(label)

        def _boolean_row(self, key: str, text: str) -> None:
            row, toggle = setting_row(
                text,
                True,
                lambda _value: None,
            )
            self.value_checks[key] = toggle
            self.content.add_widget(row)

        def _number_input(
            self,
            title: str,
            decimal: bool = False,
        ) -> TextInput:
            row = BoxLayout(
                orientation="vertical",
                size_hint_y=None,
                height=104,
                spacing=dp(4),
            )
            label = PolishLabel(
                text=title,
                font_size=18,
                halign="left",
                valign="middle",
                size_hint_y=None,
                height=36,
            )
            wrap_label(label)
            value = PolishInput(
                multiline=False,
                input_filter=None if decimal else "int",
                font_size=22,
                size_hint_y=None,
                height=64,
            )
            row.add_widget(label)
            row.add_widget(value)
            self.content.add_widget(row)
            return value

        def on_pre_enter(self, *_args):
            self.populate(quiz_app().settings)
            self.show_update_state()

        def show_update_state(self) -> None:
            if self.settings_update_button is None:
                return
            app = quiz_app()
            self.settings_update_button.text = app.update_button_text
            self.settings_update_button.disabled = (
                app.update_in_progress or app.restart_required
            )
            if self.settings_check_update_button is not None:
                self.settings_check_update_button.disabled = app.update_in_progress
            if self.update_status is not None:
                self.update_status.text = (
                    app.update_message or tr("settings.update_not_checked")
                )

        def populate(self, settings: VerbQuizSettings) -> None:
            self.mode_spinner.text = mode_label(settings.mode)
            for key in (
                "polite_to_plain",
                "plain_to_polite",
                "plain_output",
                "polite_output",
            ):
                self.value_checks[key].active = bool(
                    getattr(settings, key)
                )
            for name, checkbox in self.form_checks.items():
                checkbox.active = name in settings.enabled_forms
            for name, checkbox in self.pattern_checks.items():
                checkbox.active = name in settings.enabled_patterns
            self.word_filter.text = settings.word_filter
            self.question_count.text = str(settings.question_count)
            self.auto_advance.text = str(
                settings.auto_advance_seconds
            )
            self.font_scale_slider.value = settings.font_scale
            self._font_scale_changed(
                self.font_scale_slider,
                settings.font_scale,
            )
            self.mobile_button_scale_slider.value = (
                settings.mobile_button_scale
            )
            self._mobile_button_scale_changed(
                self.mobile_button_scale_slider,
                settings.mobile_button_scale,
            )
            self.status.text = ""
            self.statistics.text = ""

        def read_settings(self) -> VerbQuizSettings:
            settings = VerbQuizSettings(
                mode=LABEL_TO_MODE.get(
                    self.mode_spinner.text,
                    next(
                        (
                            mode
                            for mode in MODE_LABELS
                            if mode_label(mode) == self.mode_spinner.text
                        ),
                        MODE_TRANSFORMATION,
                    ),
                ),
                polite_to_plain=self.value_checks[
                    "polite_to_plain"
                ].active,
                plain_to_polite=self.value_checks[
                    "plain_to_polite"
                ].active,
                plain_output=self.value_checks["plain_output"].active,
                polite_output=self.value_checks["polite_output"].active,
                enabled_forms=[
                    name
                    for name, checkbox in self.form_checks.items()
                    if checkbox.active
                ],
                enabled_patterns=[
                    name
                    for name, checkbox in self.pattern_checks.items()
                    if checkbox.active
                ],
                word_filter=self.word_filter.text.strip(),
                question_count=_safe_int(self.question_count.text, 0),
                number_of_tries=1,
                random_order=True,
                auto_advance_seconds=_safe_float(
                    self.auto_advance.text,
                    -1.0,
                ),
                font_scale=float(self.font_scale_slider.value),
                mobile_button_scale=float(
                    self.mobile_button_scale_slider.value
                ),
            )
            settings.validate()
            return settings

        def _font_scale_changed(
            self,
            _slider,
            value: float,
        ) -> None:
            self.font_scale_value.text = f"{round(value * 100)}%"

        def _mobile_button_scale_changed(
            self,
            _slider,
            value: float,
        ) -> None:
            self.mobile_button_scale_value.text = (
                f"{round(value * 100)}%"
            )

        def save(self, start_after_save: bool) -> None:
            try:
                settings = self.read_settings()
                app = quiz_app()
                app.save_settings(settings)
                self.status.color = accent_ok
                self.status.text = tr("settings.saved")
                if start_after_save:
                    app.start_quiz()
            except (MobileQuizError, OSError) as exception:
                self.status.color = accent_bad
                self.status.text = mobile_error_text(self, exception)

        def calculate_statistics(self) -> None:
            try:
                settings = self.read_settings()
                self.statistics.text = tr("specialized.counting")
                quiz_app().calculate_statistics(
                    settings,
                    self._statistics_ready,
                )
            except MobileQuizError as exception:
                self.statistics.text = mobile_error_text(self, exception)

        def _statistics_ready(
            self,
            values: Optional[Dict[str, int]],
            error: str,
        ) -> None:
            if error:
                self.statistics.text = error
                return
            if values is None:
                self.statistics.text = tr("specialized.count_failed")
                return
            self.statistics.text = "\n".join(
                (
                    tr("specialized.available_words", count=values["words"]),
                    tr("specialized.active_patterns", count=values["patterns"]),
                    tr("specialized.available_entities", count=values["entities"]),
                    tr("specialized.noun_categories", count=values["categories"]),
                    tr("specialized.possible_questions", count=values["possible"]),
                )
            )

    class HelpScreen(Screen):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            root = BoxLayout(
                orientation="vertical",
                padding=16,
                spacing=10,
            )
            scroll = ScrollView(do_scroll_x=False)
            content = BoxLayout(
                orientation="vertical",
                padding=12,
                spacing=12,
                size_hint_y=None,
            )
            content.bind(minimum_height=content.setter("height"))
            sections = (
                (
                    tr("specialized.help.how"),
                    tr("specialized.help.verbs.how"),
                ),
                (
                    tr("specialized.help.keyboard"),
                    tr("specialized.help.verbs.keyboard"),
                ),
                (
                    tr("specialized.help.hint"),
                    tr("specialized.help.verbs.hint"),
                ),
                (
                    tr("specialized.help.settings"),
                    tr("specialized.help.settings_body"),
                ),
                (
                    tr("specialized.help.filters"),
                    tr("specialized.help.verbs.filters"),
                ),
                (
                    tr("specialized.help.files"),
                    tr("specialized.help.files_body"),
                ),
            )
            content.add_widget(
                PolishLabel(
                    text=tr("specialized.help"),
                    font_size=30,
                    size_hint_y=None,
                    height=54,
                )
            )
            for title, body in sections:
                title_label = PolishLabel(
                    text=title,
                    color=accent_info,
                    font_size=22,
                    halign="left",
                    valign="middle",
                    size_hint_y=None,
                    height=44,
                )
                wrap_label(title_label)
                content.add_widget(title_label)
                body_label = PolishLabel(
                    text=body,
                    font_size=19,
                    halign="left",
                    valign="middle",
                    size_hint_y=None,
                    height=120,
                )
                wrap_label(body_label)
                content.add_widget(body_label)
            scroll.add_widget(content)
            root.add_widget(scroll)
            back = PolishButton(
                text=tr("action.back"),
                font_size=21,
                size_hint_y=None,
                height=68,
            )
            back.bind(
                on_release=lambda *_: quiz_app().go_home()
            )
            root.add_widget(back)
            self.add_widget(root)

    class QuizScreen(Screen):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.session: Optional[VerbQuizSession] = None
            self.auto_event = None
            self.focus_request = FocusRequest()
            self.screen_active = False
            self.hint_visible = False
            root = BoxLayout(
                orientation="vertical",
                padding=dp(MOBILE_QUIZ_LAYOUT.root_padding),
                spacing=dp(MOBILE_QUIZ_LAYOUT.root_spacing),
            )

            header = mobile_action_row(
                MOBILE_QUIZ_LAYOUT.header_height,
                spacing=dp(6),
            )
            self.progress = AdaptiveSingleLineLabel(
                text="",
                fit_plain_text="",
                preferred_font_sp=14,
                minimum_font_sp=8,
                halign="left",
                valign="middle",
            )
            embedded_mode = bool(getattr(quiz_app(), "embedded_mode", False))
            menu_button = PolishButton(
                text=(
                    tr("specialized.launcher_menu")
                    if embedded_mode
                    else tr("specialized.menu")
                ),
                font_size=sp(16),
                size_hint_x=None,
                width=dp(104 if embedded_mode else 92),
            )
            menu_button.bind(
                on_release=(
                    (lambda *_: leave_quiz())
                    if embedded_mode
                    else (lambda *_: self.leave_to_menu())
                )
            )
            header.add_widget(self.progress)
            header.add_widget(menu_button)
            root.add_widget(header)
            self.progress_bar = ProgressBar(
                max=1.0,
                value=0.0,
                size_hint_y=None,
                height=dp(MOBILE_QUIZ_LAYOUT.progress_height),
            )
            root.add_widget(self.progress_bar)
            self.form_line = AdaptiveSingleLineLabel(
                text="",
                fit_plain_text="",
                markup=True,
                preferred_font_sp=13,
                minimum_font_sp=MOBILE_QUIZ_LAYOUT.prompt_minimum_sp,
                size_hint_y=None,
                height=dp(MOBILE_QUIZ_LAYOUT.form_height),
            )
            root.add_widget(self.form_line)

            answer_placeholder = f"{tr('mobile.answer')}:"
            self.status = AdaptiveSingleLineLabel(
                text=answer_placeholder,
                fit_plain_text=answer_placeholder,
                markup=True,
                preferred_font_sp=MOBILE_QUIZ_LAYOUT.review_preferred_sp,
                minimum_font_sp=MOBILE_QUIZ_LAYOUT.review_minimum_sp,
                halign="left",
                valign="middle",
                size_hint_y=None,
                height=dp(MOBILE_QUIZ_LAYOUT.review_height),
            )
            root.add_widget(self.status)

            content = BoxLayout(
                orientation="vertical",
                padding=[
                    dp(MOBILE_QUIZ_LAYOUT.content_horizontal_padding),
                    0,
                    dp(MOBILE_QUIZ_LAYOUT.content_horizontal_padding),
                    0,
                ],
                spacing=dp(MOBILE_QUIZ_LAYOUT.content_spacing),
                size_hint_y=None,
            )
            content.bind(minimum_height=content.setter("height"))
            self.question_line = AdaptiveSingleLineLabel(
                text="",
                fit_plain_text="",
                markup=True,
                preferred_font_sp=MOBILE_QUIZ_LAYOUT.prompt_preferred_sp,
                minimum_font_sp=MOBILE_QUIZ_LAYOUT.prompt_minimum_sp,
                maximum_fit_lines=MOBILE_QUIZ_LAYOUT.prompt_maximum_lines,
                shorten=False,
                halign="left",
                valign="middle",
                size_hint_y=None,
                height=dp(MOBILE_QUIZ_LAYOUT.prompt_height),
            )
            content.add_widget(self.question_line)

            self.answer_input = JapaneseInput(
                font_size=sp(23),
                size_hint_y=None,
                height=dp(MOBILE_QUIZ_LAYOUT.input_height),
                padding=[dp(10), dp(5), dp(10), dp(5)],
                hint_text=tr("specialized.answer_placeholder"),
            )
            self.answer_input._mobile_base_font_size = sp(23)
            self.answer_input._mobile_max_font_size = dp(27)
            self.answer_input.font_size = min(
                float(self.answer_input.font_size),
                self.answer_input._mobile_max_font_size,
            )
            self.answer_input.bind(
                on_text_validate=lambda *_: self.input_action()
            )
            content.add_widget(self.answer_input)

            self.hint = AdaptiveSingleLineLabel(
                text="",
                fit_plain_text="",
                markup=True,
                color=accent_info,
                preferred_font_sp=MOBILE_QUIZ_LAYOUT.hint_preferred_sp,
                minimum_font_sp=MOBILE_QUIZ_LAYOUT.hint_minimum_sp,
                halign="left",
                valign="middle",
                size_hint_y=None,
                height=dp(MOBILE_QUIZ_LAYOUT.hint_height),
                opacity=0,
            )
            content.add_widget(self.hint)

            first_row = mobile_action_row(
                MOBILE_QUIZ_LAYOUT.action_height,
                spacing=dp(6),
            )
            self.primary_button = PolishButton(
                text=tr("specialized.check"),
                font_size=sp(18),
            )
            self.primary_button.bind(
                on_release=lambda *_: self._button_action(
                    self.primary_action
                )
            )
            self.secondary_button = PolishButton(
                text=tr("specialized.hint_button"),
                font_size=sp(18),
            )
            self.secondary_button.bind(
                on_release=lambda *_: self._button_action(
                    self.secondary_action
                )
            )
            first_row.add_widget(self.primary_button)
            first_row.add_widget(self.secondary_button)
            content.add_widget(first_row)
            content.add_widget(Widget())

            # The active quiz is intentionally not a ScrollView.  Keeping a
            # fixed-height slot for every state prevents finger drags, hints,
            # and answer feedback from moving the controls vertically.  The
            # explicit top anchor also keeps the question fixed if a very
            # small keyboard viewport cannot display the lowest feedback row.
            content_anchor = AnchorLayout(anchor_x="left", anchor_y="top")
            content_anchor.add_widget(content)
            root.add_widget(content_anchor)
            self.add_widget(root)

        def set_session(self, session: VerbQuizSession) -> None:
            self._cancel_auto_advance()
            self.cancel_focus()
            self.session = session
            self.next_question()

        def _button_action(self, callback) -> None:
            callback()
            self.keep_keyboard_visible()

        def keep_keyboard_visible(self) -> None:
            self.focus_request.schedule(
                Clock.schedule_once,
                self._restore_answer_focus,
                self._focus_is_active,
            )

        def _restore_answer_focus(self) -> None:
            self.answer_input.focus = True

        def _focus_is_active(self) -> bool:
            controller = quiz_app()
            manager = getattr(controller, "manager", None)
            return bool(
                self.screen_active
                and manager is not None
                and manager.current == self.name
                and self.session is not None
                and self.session.current_question is not None
            )

        def cancel_focus(self) -> None:
            self.focus_request.cancel()

        def on_enter(self, *_args):
            self.screen_active = True
            self.keep_keyboard_visible()

        def configure_actions(self) -> None:
            """Update labels and colors without replacing either button."""
            if self.session is None:
                return
            primary = self.primary_button
            secondary = self.secondary_button
            primary.opacity = 1
            primary.disabled = False
            primary.color = MOBILE_BUTTON_TEXT
            secondary.color = MOBILE_BUTTON_TEXT
            if self.session.waiting_for_next:
                if self.session.current_outcome == "wrong":
                    primary.text = tr("quiz.accept")
                    primary.background_color = MOBILE_CORRECT_BACKGROUND
                    secondary.text = tr("quiz.wrong")
                    secondary.opacity = 1
                    secondary.disabled = False
                    secondary.background_color = MOBILE_WRONG_BACKGROUND
                else:
                    primary.text = tr("quiz.next")
                    primary.background_color = MOBILE_CORRECT_BACKGROUND
                    secondary.text = ""
                    secondary.opacity = 0
                    secondary.disabled = True
                    secondary.background_color = MOBILE_BUTTON_BACKGROUND
                return
            primary.text = tr("specialized.check")
            primary.background_color = MOBILE_BUTTON_BACKGROUND
            secondary.text = tr("specialized.hint_button")
            secondary.opacity = 1
            secondary.disabled = False
            secondary.background_color = (
                hint_active_background
                if self.hint_visible
                else MOBILE_BUTTON_BACKGROUND
            )

        def update_progress(self) -> None:
            """Refresh the compact Written-style question and score header."""
            if self.session is None:
                return
            total = max(1, int(self.session.settings.question_count))
            current = min(total, max(0, self.session.current_index + 1))
            question_text = tr(
                "mobile.compact_question_progress",
                current=current,
                total=total,
            )
            progress_text = (
                f"{question_text}   ✓{self.session.correct_answers}  "
                f"×{self.session.wrong_answers}  "
                f"✓+{self.session.accepted_answers}"
            )
            self.progress.set_fitted_text(progress_text, progress_text)
            self.progress_bar.value = current / total

        def next_question(self) -> None:
            self._cancel_auto_advance()
            if self.session is None:
                return
            if (
                self.session.current_question is not None
                and not self.session.waiting_for_next
            ):
                self.status.color = accent_info
                message = tr("specialized.check_or_skip_first")
                self.status.set_fitted_text(message, message)
                return
            # Clear every question-owned texture before requesting the next
            # card.  This protects Pydroid/Kivy from briefly reusing a long
            # previous texture while the new card is being generated.
            self.form_line.set_fitted_text("", "")
            self.question_line.set_fitted_text("", "")
            answer_placeholder = f"{tr('mobile.answer')}:"
            self.status.set_fitted_text(
                answer_placeholder,
                answer_placeholder,
            )
            self.hint.set_fitted_text("", "")
            self.hint.opacity = 0
            try:
                question = self.session.next_question()
            except (MobileQuizError, ProjectError) as exception:
                self.status.color = accent_bad
                message = mobile_error_text(self, exception)
                self.status.set_fitted_text(escape_markup(message), message)
                return
            if question is None:
                self.show_results()
                return
            self.update_progress()
            target_plain = f"[{target_label(question)}]"
            source_plain = " ".join(question.source_sentence.split())
            context_plain = " ".join(question.context_question.split())
            target = escape_markup(target_plain)
            source = escape_markup(source_plain)
            context = escape_markup(context_plain)
            target_markup = f"[color=#26338C]{target}[/color]"
            self.form_line.set_fitted_text(target_markup, target_plain)
            question_markup = (
                source
                + (
                    f"  [color=#5B6472]· {context}[/color]"
                    if context
                    else ""
                )
            )
            question_plain = source_plain + (
                f"  · {context_plain}" if context_plain else ""
            )
            self.question_line.set_fitted_text(question_markup, question_plain)
            self.answer_input.set_review_locked(False)
            self.answer_input.background_color = input_active_background
            self.answer_input.text = ""
            answer_placeholder = f"{tr('mobile.answer')}:"
            self.status.set_fitted_text(
                answer_placeholder,
                answer_placeholder,
            )
            self.status.color = label_color
            self.hint_visible = False
            self.hint.set_fitted_text("", "")
            self.hint.opacity = 0
            self.configure_actions()
            if self.screen_active:
                self.keep_keyboard_visible()

        def primary_action(self) -> None:
            if self.session is None:
                return
            if self.session.waiting_for_next:
                if self.session.current_outcome == "wrong":
                    self.accept_or_skip()
                else:
                    self.next_question()
            else:
                self.check_answer()

        def input_action(self) -> None:
            """Check before review; keep Enter inert in every terminal state."""
            if self.session is None or self.session.waiting_for_next:
                return
            self.check_answer()

        def secondary_action(self) -> None:
            if self.session is None:
                return
            if self.session.waiting_for_next:
                if self.session.current_outcome == "wrong":
                    self.next_question()
                return
            self.show_hint()

        def check_answer(self) -> None:
            if self.session is None:
                return
            if self.session.waiting_for_next:
                self.next_question()
                return
            result = self.session.submit(self.answer_input.text)
            self.update_progress()
            if result.state == "correct":
                self._show_terminal_review(
                    result.expected_answer,
                    correct=True,
                )
                delay = self.session.settings.auto_advance_seconds
                if delay > 0:
                    self.auto_event = Clock.schedule_once(
                        lambda _dt: self.next_question(),
                        delay,
                    )
            elif result.state == "wrong":
                self._show_terminal_review(
                    result.expected_answer,
                    correct=False,
                )
            elif result.state == "retry":
                message = tr(
                    "specialized.retry",
                    current=self.session.current_try,
                    total=self.session.settings.number_of_tries,
                )
                self.status.set_fitted_text(escape_markup(message), message)
                self.status.color = accent_bad
                self.keep_keyboard_visible()
            if result.state in {"correct", "wrong"}:
                self.keep_keyboard_visible()

        def _show_terminal_review(
            self,
            expected: str,
            correct: bool,
        ) -> None:
            """Lock editing and fill the full-width correct-answer line."""
            self.status.color = label_color
            answer_markup = (
                f"[color=#2F7A40]{escape_markup(expected)}[/color]"
            )
            self.status.set_fitted_text(answer_markup, expected)
            self.answer_input.set_review_locked(True)
            self.answer_input.background_color = (
                input_correct_background if correct else input_wrong_background
            )
            self.configure_actions()

        def show_hint(self) -> None:
            if (
                self.session is None
                or self.session.current_question is None
            ):
                return
            if self.hint_visible:
                self.hint_visible = False
                self.hint.set_fitted_text("", "")
                self.hint.opacity = 0
                self.configure_actions()
                self.keep_keyboard_visible()
                return
            question = self.session.current_question
            hint_text = format_mobile_hint_entries(
                mobile_sentence_hint_items(
                    question, quiz_app().engine.project
                )
            )
            if not hint_text:
                hint_text = tr("specialized.no_hint")
            self.hint.set_fitted_text(
                escape_markup(hint_text),
                hint_text,
            )
            self.hint_visible = True
            self.hint.opacity = 1
            self.configure_actions()
            self.keep_keyboard_visible()

        def _resize_hint(self, *_args) -> None:
            if not self.hint_visible or not self.hint.text:
                self.hint.opacity = 0
                return
            self.hint._fit_font_to_width()

        def accept_or_skip(self) -> None:
            if self.session is None:
                return
            self._cancel_auto_advance()
            self.session.accept_or_skip()
            self.next_question()

        def show_results(self) -> None:
            if self.session is None:
                return
            self.screen_active = False
            self.cancel_focus()
            self.answer_input.focus = False
            app = quiz_app()
            results = app.manager.get_screen("results")
            results.set_session(self.session)
            app.manager.transition = SlideTransition(direction="left")
            app.manager.current = "results"

        def _cancel_auto_advance(self) -> None:
            if self.auto_event is not None:
                self.auto_event.cancel()
                self.auto_event = None

        def leave_to_menu(self) -> None:
            self.screen_active = False
            self.cancel_focus()
            self._cancel_auto_advance()
            self.answer_input.focus = False
            quiz_app().go_home()

        def on_leave(self, *_args):
            self.screen_active = False
            self.cancel_focus()
            self._cancel_auto_advance()
            self.answer_input.focus = False

    class ResultsScreen(Screen):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            root = BoxLayout(
                orientation="vertical",
                padding=24,
                spacing=16,
            )
            root.add_widget(
                PolishLabel(
                    text=tr("specialized.finished"),
                    color=accent_info,
                    font_size=30,
                    size_hint_y=None,
                    height=58,
                )
            )
            self.results = PolishLabel(
                text="",
                font_size=23,
                halign="center",
                valign="middle",
                size_hint_y=None,
                height=220,
            )
            wrap_label(self.results)
            root.add_widget(self.results)
            again = PolishButton(
                text=tr("specialized.again"),
                font_size=22,
                size_hint_y=None,
                height=72,
            )
            again.bind(
                on_release=lambda *_: quiz_app().start_quiz()
            )
            root.add_widget(again)
            settings_button = PolishButton(
                text=tr("action.settings"),
                font_size=21,
                size_hint_y=None,
                height=70,
            )
            settings_button.bind(
                on_release=lambda *_: quiz_app().open_settings()
            )
            root.add_widget(settings_button)
            home = PolishButton(
                text=tr("specialized.main_menu"),
                font_size=21,
                size_hint_y=None,
                height=70,
            )
            home.bind(
                on_release=lambda *_: quiz_app().go_home()
            )
            root.add_widget(home)
            root.add_widget(Widget())
            self.add_widget(root)

        def set_session(self, session: VerbQuizSession) -> None:
            self.results.text = tr(
                "specialized.results",
                correct=session.correct_answers,
                wrong=session.wrong_answers,
                accepted=session.accepted_answers,
            )

    class KotomiVerbsApp(App):
        icon = app_icon_png_path()
        def build(self):
            apply_kivy_window_icon(Window)
            self.title = tr("specialized.verbs_title")
            self.project_path = resolve_project_path()
            self.settings_store = SettingsStore(
                settings_path(INSTALL_ROOT, SETTINGS_FILENAME)
            )
            self.settings = self.settings_store.load()
            font_scale_state["value"] = self.settings.font_scale
            button_scale_state["value"] = validate_mobile_button_scale(
                self.settings.mobile_button_scale
            )
            self.engine: Optional[VerbQuizEngine] = None
            self.engine_error = ""
            self.update_message = ""
            self.update_button_text = tr("action.update")
            self.update_in_progress = False
            self.restart_required = False
            self.reload_engine()

            self.manager = ScreenManager()
            self.manager.add_widget(HomeScreen(name="home"))
            self.manager.add_widget(SettingsScreen(name="settings"))
            self.manager.add_widget(HelpScreen(name="help"))
            self.manager.add_widget(QuizScreen(name="quiz"))
            self.manager.add_widget(ResultsScreen(name="results"))
            if not getattr(self, "embedded_mode", False):
                Window.bind(on_keyboard=self._on_keyboard)
            return self.manager

        def prepare_for_unload(self) -> None:
            if not hasattr(self, "manager"):
                return
            quiz = self.manager.get_screen("quiz")
            quiz._cancel_auto_advance()
            quiz.screen_active = False
            quiz.cancel_focus()
            quiz.answer_input.focus = False

        def reload_engine(self) -> bool:
            try:
                if self.engine is None:
                    self.engine = VerbQuizEngine(self.project_path)
                else:
                    self.engine.reload()
                self.engine_error = ""
                return True
            except (MobileQuizError, ProjectError, OSError) as exception:
                self.engine = None
                self.engine_error = mobile_error_text(self, exception)
                return False

        def home_summary(self) -> str:
            if self.engine_error:
                summary = tr(
                    "hub.cannot_open",
                    title=self.title,
                    detail=self.engine_error,
                )
            else:
                summary = settings_summary(self.settings)
            if self.update_message:
                summary += "\n\n" + self.update_message
            return summary

        def _refresh_home_update_state(self) -> None:
            if not hasattr(self, "manager"):
                return
            home = self.manager.get_screen("home")
            home.show_update_state()
            settings = self.manager.get_screen("settings")
            settings.show_update_state()

        def check_for_updates(self) -> None:
            if self.update_in_progress:
                return
            try:
                manifest_url = load_update_url(
                    INSTALL_ROOT / "mobile_update_config.json"
                )
                updater = QuizUpdater(INSTALL_ROOT, manifest_url)
            except UpdateError as exception:
                self.update_message = tr(
                    "settings.update_check_failed",
                    detail=mobile_error_text(
                        self, exception, key="mobile.update_failed"
                    ),
                )
                self._refresh_home_update_state()
                return

            self.update_in_progress = True
            self.update_message = tr("hub.checking_updates")
            self._refresh_home_update_state()

            def worker() -> None:
                try:
                    result = updater.check()
                    Clock.schedule_once(
                        lambda _dt: self._finish_update_check(result, ""),
                        0,
                    )
                except Exception as exception:
                    message = mobile_error_text(
                        self, exception, key="mobile.update_failed"
                    )
                    Clock.schedule_once(
                        lambda _dt: self._finish_update_check(None, message),
                        0,
                    )

            threading.Thread(target=worker, daemon=True).start()

        def _finish_update_check(self, result, error: str) -> None:
            self.update_in_progress = False
            if error:
                self.update_message = tr(
                    "settings.update_check_failed", detail=error
                )
            elif result.changed:
                self.update_message = tr(
                    "settings.update_available", version=result.version
                )
            else:
                self.update_message = tr(
                    "settings.update_current", version=result.version
                )
            self._refresh_home_update_state()

        def update_quiz(self) -> None:
            if self.update_in_progress:
                return
            try:
                manifest_url = load_update_url(
                    INSTALL_ROOT / "mobile_update_config.json"
                )
                updater = QuizUpdater(INSTALL_ROOT, manifest_url)
            except UpdateError as exception:
                self.update_message = mobile_error_text(
                    self,
                    exception,
                    key="mobile.update_failed",
                )
                self.update_button_text = tr("action.update")
                self._refresh_home_update_state()
                return

            self.update_in_progress = True
            self.update_message = tr("hub.checking_updates")
            self.update_button_text = tr("hub.checking_updates")
            self._refresh_home_update_state()

            def worker() -> None:
                try:
                    result = updater.update()
                    Clock.schedule_once(
                        lambda _dt: self._finish_update(result, ""),
                        0,
                    )
                except Exception as exception:
                    message = mobile_error_text(
                        self,
                        exception,
                        key="mobile.update_failed",
                    )
                    Clock.schedule_once(
                        lambda _dt: self._finish_update(None, message),
                        0,
                    )

            threading.Thread(target=worker, daemon=True).start()

        def _finish_update(self, result, error: str) -> None:
            self.update_in_progress = False
            self.update_button_text = tr("action.update")
            if error:
                self.update_message = tr("hub.update_failed", detail=error)
                self._refresh_home_update_state()
                return

            if not result.changed:
                self.update_message = tr(
                    "hub.version_current", version=result.version
                )
            elif result.restart_required:
                self.restart_required = True
                self.update_message = tr(
                    "hub.updated_restart", version=result.version
                )
                self.update_button_text = tr("hub.restart_required")
            else:
                self.reload_engine()
                self.update_message = tr(
                    "hub.updated_active", version=result.version
                )
            self._refresh_home_update_state()

        def save_settings(self, settings: VerbQuizSettings) -> None:
            previous_scale = self.settings.font_scale
            self.settings_store.save(settings)
            self.settings = settings
            font_scale_state["value"] = settings.font_scale
            if abs(previous_scale - settings.font_scale) > 0.001:
                self._rescale_widget_fonts(
                    self.manager,
                    settings.font_scale / previous_scale,
                )
            self.apply_mobile_button_scale(settings.mobile_button_scale)

        def _rescale_widget_fonts(
            self,
            widget,
            ratio: float,
        ) -> None:
            if hasattr(widget, "font_size"):
                base = getattr(widget, "_mobile_base_font_size", None)
                resized = (
                    float(base) * current_font_scale()
                    if base is not None
                    else float(widget.font_size) * ratio
                )
                maximum = getattr(widget, "_mobile_max_font_size", None)
                widget.font_size = (
                    min(resized, float(maximum))
                    if maximum is not None
                    else resized
                )
            for child in getattr(widget, "children", []):
                self._rescale_widget_fonts(child, ratio)

        def _rescale_widget_buttons(self, widget) -> None:
            base_height = getattr(
                widget,
                "_mobile_button_base_height",
                None,
            )
            if base_height is not None:
                widget.height = mobile_button_height(base_height)
            base_row_height = getattr(
                widget,
                "_mobile_action_base_height",
                None,
            )
            if base_row_height is not None:
                widget.height = mobile_button_height(base_row_height)
            for child in getattr(widget, "children", []):
                self._rescale_widget_buttons(child)

        def apply_mobile_button_scale(self, scale: float) -> None:
            button_scale_state["value"] = validate_mobile_button_scale(
                scale
            )
            if hasattr(self, "manager"):
                self._rescale_widget_buttons(self.manager)

        def start_quiz(self) -> None:
            if self.restart_required:
                self.update_message = tr("hub.restart_required")
                self.go_home()
                return
            if not self.reload_engine() or self.engine is None:
                self.go_home()
                return
            try:
                session = VerbQuizSession(self.engine, self.settings)
                quiz = self.manager.get_screen("quiz")
                self.manager.transition = SlideTransition(direction="left")
                self.manager.current = "quiz"
                quiz.set_session(session)
            except (MobileQuizError, ProjectError) as exception:
                self.engine_error = mobile_error_text(self, exception)
                self.go_home()

        def open_settings(self) -> None:
            self.manager.transition = SlideTransition(direction="left")
            self.manager.current = "settings"

        def open_help(self) -> None:
            self.manager.transition = SlideTransition(direction="left")
            self.manager.current = "help"

        def go_home(self) -> None:
            if hasattr(self, "manager") and self.manager.has_screen("quiz"):
                quiz = self.manager.get_screen("quiz")
                quiz.screen_active = False
                quiz.cancel_focus()
                quiz.answer_input.focus = False
            self.manager.transition = SlideTransition(direction="right")
            self.manager.current = "home"

        def calculate_statistics(
            self,
            settings: VerbQuizSettings,
            callback,
        ) -> None:
            if self.engine is None:
                callback(None, self.engine_error)
                return
            engine = self.engine

            def worker() -> None:
                try:
                    result = engine.statistics(settings)
                    Clock.schedule_once(
                        lambda _dt: callback(result, ""),
                        0,
                    )
                except Exception as exception:
                    message = mobile_error_text(
                        self,
                        exception,
                        key="mobile.update_failed",
                    )
                    Clock.schedule_once(
                        lambda _dt: callback(None, message),
                        0,
                    )

            threading.Thread(target=worker, daemon=True).start()

        def _on_keyboard(self, _window, key, *_args):
            if key in (282, 290) and self.manager.current == "quiz":
                self.manager.get_screen("quiz").show_hint()
                return True
            if key not in (27, 1001):
                return False
            if self.manager.current == "home":
                self.stop()
            else:
                self.go_home()
            return True

        def on_stop(self):
            if not getattr(self, "embedded_mode", False):
                Window.unbind(on_keyboard=self._on_keyboard)

    return KotomiVerbsApp


def create_embedded_controller():
    """Create the verb UI controller for the Kotomi master app."""
    app_class = create_app_class()
    controller = app_class()
    controller.embedded_mode = True
    return controller


def main() -> int:
    try:
        app_class = create_app_class()
    except ModuleNotFoundError as exception:
        if exception.name == "kivy":
            print(
                "Kivy nie jest zainstalowane. Uruchom skrypt w środowisku "
                "telefonu z obsługą Kivy, na przykład w Pydroid 3."
            )
            return 1
        raise
    app_class().run()
    return 0
