"""Kivy presentation for the Lessons package.

All lesson catalog, quiz generation, session, and hint policy comes from
:mod:`apps.lessons.logic`. This module owns only the mobile Kivy screens,
interaction, embedded launcher integration, and lesson editor presentation.
"""

from __future__ import annotations

import copy
from pathlib import Path
import sys
import threading
from typing import Dict, List, Optional
from uuid import uuid4


APP_ROOT = Path(__file__).resolve().parent
INSTALL_ROOT = APP_ROOT.parents[1]
if str(INSTALL_ROOT) not in sys.path:
    sys.path.insert(0, str(INSTALL_ROOT))

from apps.lessons.logic import *
from kotomi_core.settings_xml import settings_path
from kotomi_core.paths import FONTS_DIR
from kotomi_core.app_identity import (
    app_icon_png_path,
    apply_kivy_window_icon,
    configure_windows_app_id,
)
from kotomi_ui.mobile import (
    FocusRequest,
    MOBILE_BUTTON_BACKGROUND,
    MOBILE_BUTTON_TEXT,
    MOBILE_CORRECT_BACKGROUND,
    MOBILE_QUIZ_LAYOUT,
    MOBILE_WRONG_BACKGROUND,
    MobileReviewInputMixin,
    fitted_compact_text_layout,
    fitted_single_line_font_size,
    format_grammatical_hint_entry,
    format_mobile_hint_entries,
    mobile_font_path,
    scaled_button_height,
)
from kotomi_core.mobile_i18n import mobile_error_text, mobile_text


MOBILE_FONT = mobile_font_path(FONTS_DIR)
POLISH_FONT = MOBILE_FONT
JAPANESE_FONT = MOBILE_FONT

def create_app_class():
    configure_windows_app_id()
    """Import Kivy lazily so domain tests do not require a GUI installation."""
    from kivy.app import App
    from kivy.clock import Clock
    from kivy.core.text import Label as CoreLabel
    from kivy.core.window import Window
    from kivy.graphics import Color, Line
    from kivy.metrics import dp, sp
    from kivy.properties import StringProperty
    from kivy.uix.anchorlayout import AnchorLayout
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.button import Button
    from kivy.uix.gridlayout import GridLayout
    from kivy.uix.label import Label
    from kivy.uix.popup import Popup
    from kivy.uix.progressbar import ProgressBar
    from kivy.uix.screenmanager import Screen, ScreenManager
    from kivy.uix.scrollview import ScrollView
    from kivy.uix.spinner import Spinner
    from kivy.uix.textinput import TextInput
    from kivy.uix.togglebutton import ToggleButton
    from kivy.uix.widget import Widget
    from kivy.utils import escape_markup

    Window.clearcolor = (1, 1, 1, 1)
    try:
        Window.softinput_mode = "resize"
    except Exception:
        pass

    TEXT_COLOR = (0.0, 0.0, 0.0, 1)
    MUTED_COLOR = (0.30, 0.30, 0.30, 1)
    BUTTON_COLOR = (0.92, 0.92, 0.92, 1)
    ACCENT_COLOR = (0.23, 0.53, 0.78, 1)
    BAD_COLOR = (1.0, 0.0, 0.0, 1)
    GOOD_COLOR = (0.0, 0.784, 0.325, 1)
    CHOICE_BUTTON_BACKGROUND = (1.0, 1.0, 1.0, 1.0)
    CHOICE_BORDER_COLOR = (0.58, 0.62, 0.66, 1.0)
    PROMPT_VALUE_COLOR = "#246B9E"
    CORRECT_VALUE_COLOR = "#2F7A40"
    WRONG_VALUE_COLOR = "#B83232"
    INPUT_ACTIVE_BACKGROUND = (1.0, 1.0, 1.0, 1.0)
    INPUT_REVIEW_BACKGROUND = (0.94, 0.95, 0.96, 1.0)
    INPUT_REVIEW_CORRECT_BACKGROUND = (0.84, 0.96, 0.87, 1.0)
    INPUT_REVIEW_WRONG_BACKGROUND = (1.0, 0.86, 0.86, 1.0)

    def quiz_app():
        running_app = App.get_running_app()
        controller = getattr(running_app, "active_quiz_controller", None)
        return controller or running_app

    def return_to_quiz_menu() -> bool:
        controller = quiz_app()
        host_callback = getattr(controller, "host_quiz_menu_callback", None)
        if callable(host_callback):
            host_callback()
            return True
        running_app = App.get_running_app()
        fallback = getattr(running_app, "return_to_launcher", None)
        if callable(fallback):
            fallback()
            return True
        return False

    def ui_text(key: str, fallback: str = "", **values: object) -> str:
        translated = mobile_text(quiz_app(), key, **values)
        if translated == key and fallback:
            try:
                return fallback.format(**values)
            except (KeyError, ValueError):
                return fallback
        return translated

    def compatibility_text(report) -> str:
        """Format shared sentence compatibility data in the mobile language."""
        return ui_text(
            "quiz.lesson_compatibility",
            (
                ""
            ),
            total=report.total_lesson_words,
            matched=report.matched_count,
            patterns=len(report.supported_patterns),
        )

    def possibilities_text(report) -> str:
        """Format a shared possibility report without desktop Polish prose."""
        lines = [
            ui_text(
                "quiz.possibilities_total",
                "",
                count=f"{report.total_combinations:,}",
            ),
            "",
            ui_text("quiz.possibilities_patterns", ""),
        ]
        reasons = dict(report.pattern_reasons)
        for label, count in report.pattern_counts:
            reason = reasons.get(label, "")
            suffix = (
                " " + ui_text(f"quiz.pattern_zero.{reason}")
                if reason
                else ""
            )
            lines.append(f"• {label}: {count:,}{suffix}")
        lines.extend(("", ui_text("quiz.possibilities_words", "")))
        for usage in report.word_usage:
            if usage.used:
                lines.append(ui_text(
                    "quiz.possibilities_word_used",
                    "",
                    word=usage.label,
                    patterns=", ".join(usage.pattern_labels),
                ))
                continue
            reason_key = usage.reason_code or "no_pattern_match"
            reason = ui_text(
                f"quiz.possibilities_reason.{reason_key}",
                usage.reason,
            )
            lines.append(ui_text(
                "quiz.possibilities_word_unused",
                "",
                word=usage.label,
                reason=reason,
            ))
        return "\n".join(lines)

    def bind_wrapping(
        label: Label,
        *,
        fixed_height: Optional[float] = None,
        single_line: bool = False,
    ) -> None:
        def update(instance, _value=None):
            text_height = (
                dp(fixed_height)
                if single_line and fixed_height is not None
                else None
            )
            instance.text_size = (max(0, instance.width), text_height)
            instance.texture_update()
            if fixed_height is None:
                instance.height = max(dp(32), instance.texture_size[1] + dp(10))
            else:
                instance.height = dp(fixed_height)

        label.bind(width=update, texture_size=update)
        update(label)

    class AppLabel(Label):
        def __init__(self, **kwargs):
            fixed_height = kwargs.pop("fixed_height", None)
            single_line = kwargs.pop("single_line", False)
            kwargs.setdefault("font_name", POLISH_FONT)
            kwargs.setdefault("font_size", "17sp")
            kwargs.setdefault("color", TEXT_COLOR)
            kwargs.setdefault("size_hint_y", None)
            kwargs.setdefault("halign", "left")
            kwargs.setdefault("valign", "middle")
            super().__init__(**kwargs)
            if single_line and hasattr(self, "max_lines"):
                self.max_lines = 1
            bind_wrapping(
                self,
                fixed_height=fixed_height,
                single_line=single_line,
            )

    class JapaneseLabel(AppLabel):
        def __init__(self, **kwargs):
            kwargs.setdefault("font_name", JAPANESE_FONT)
            super().__init__(**kwargs)

    class AdaptiveSingleLineLabel(AppLabel):
        """Fit a label in a fixed slot, using a second line only when allowed."""

        def __init__(self, **kwargs):
            self._preferred_font_sp = float(
                kwargs.pop("preferred_font_sp", 18.0)
            )
            self._minimum_font_sp = float(kwargs.pop("minimum_font_sp", 12.0))
            self._fit_horizontal_padding = float(
                kwargs.pop("fit_horizontal_padding", 4.0)
            )
            self._maximum_fit_lines = max(
                1,
                int(kwargs.pop("maximum_fit_lines", 1)),
            )
            self._allow_shorten = bool(kwargs.pop("allow_shorten", True))
            self._fit_plain_text = str(
                kwargs.pop("fit_plain_text", kwargs.get("text", ""))
            ).replace("\r", " ").replace("\n", " ")
            if "text" in kwargs:
                kwargs["text"] = str(kwargs["text"]).replace(
                    "\r", " "
                ).replace("\n", " ")
            self._font_fit_running = False
            kwargs["font_size"] = sp(self._preferred_font_sp)
            kwargs.setdefault("single_line", True)
            kwargs.setdefault("shorten", self._allow_shorten)
            kwargs.setdefault("shorten_from", "right")
            super().__init__(**kwargs)
            self.bind(width=self._fit_font_to_width, text=self._fit_font_to_width)
            Clock.schedule_once(self._fit_font_to_width, 0)

        def set_fitted_text(self, markup_text: str, plain_text: str) -> None:
            """Update displayed text and the markup-free measurement value."""
            self._fit_plain_text = str(plain_text).replace(
                "\r", " "
            ).replace("\n", " ")
            normalized_markup = str(markup_text).replace(
                "\r", " "
            ).replace("\n", " ")
            # Clear the old CoreLabel texture before replacing a long prompt.
            # This avoids a stale wrapped tail surviving for one Android frame.
            self.text = ""
            self.text = normalized_markup
            self._fit_font_to_width()

        def _fit_font_to_width(self, *_args) -> None:
            if self._font_fit_running:
                return
            available_width = max(
                0.0,
                self.width - dp(self._fit_horizontal_padding),
            )
            if available_width <= 0:
                return
            self._font_fit_running = True
            try:
                probe = CoreLabel(
                    text=self._fit_plain_text,
                    font_name=self.font_name,
                    font_size=sp(self._preferred_font_sp),
                )
                probe.refresh()
                fitted_lines, fitted_sp = fitted_compact_text_layout(
                    float(probe.texture.size[0]),
                    available_width,
                    preferred_sp=self._preferred_font_sp,
                    minimum_sp=self._minimum_font_sp,
                    maximum_lines=self._maximum_fit_lines,
                )
                # Kivy's shorten mode always forces one line and overrides
                # max_lines, so it must be off for the bounded wrap case.
                self.shorten = self._allow_shorten and fitted_lines == 1
                if hasattr(self, "max_lines"):
                    self.max_lines = fitted_lines
                self.font_size = sp(fitted_sp)
            finally:
                self._font_fit_running = False

    class AppButton(Button):
        def __init__(self, **kwargs):
            kwargs.setdefault("font_name", POLISH_FONT)
            kwargs.setdefault("font_size", "16sp")
            kwargs.setdefault("background_normal", "")
            kwargs.setdefault("background_color", BUTTON_COLOR)
            kwargs.setdefault("color", TEXT_COLOR)
            kwargs.setdefault("size_hint_y", None)
            controller = quiz_app()
            button_scale = getattr(
                getattr(controller, "settings", None),
                "mobile_button_scale",
                1.0,
            )
            base_height = float(kwargs.get("height", dp(56)))
            kwargs["height"] = scaled_button_height(base_height, button_scale)
            kwargs.setdefault("halign", "center")
            kwargs.setdefault("valign", "middle")
            super().__init__(**kwargs)
            self._mobile_base_height = base_height

            def fit_text(instance, _value=None) -> None:
                instance.text_size = (
                    max(0, instance.width - dp(18)),
                    max(0, instance.height - dp(10)),
                )

            self.bind(size=fit_text)
            fit_text(self)

    class JapaneseButton(AppButton):
        def __init__(self, **kwargs):
            kwargs.setdefault("font_name", JAPANESE_FONT)
            super().__init__(**kwargs)

    class MobileOptionToggle(ToggleButton):
        """Large setup option that remains easy to tap inside a ScrollView."""

        def __init__(self, *, active: bool = False, **kwargs):
            kwargs.setdefault("font_name", POLISH_FONT)
            kwargs.setdefault("font_size", "16sp")
            kwargs.setdefault("background_normal", "")
            kwargs.setdefault("background_down", "")
            kwargs.setdefault("color", TEXT_COLOR)
            kwargs.setdefault("size_hint_y", None)
            kwargs.setdefault("height", dp(48))
            kwargs.setdefault("halign", "left")
            kwargs.setdefault("valign", "middle")
            super().__init__(**kwargs)
            self.state = "down" if active else "normal"
            self.bind(size=self._fit_text, state=self._update_background)
            self._fit_text()
            self._update_background()

        @property
        def active(self) -> bool:
            """Expose the same selection interface previously used by CheckBox."""
            return self.state == "down"

        @active.setter
        def active(self, value: bool) -> None:
            self.state = "down" if value else "normal"

        def _fit_text(self, *_args) -> None:
            self.text_size = (
                max(0, self.width - dp(24)),
                max(0, self.height - dp(8)),
            )

        def _update_background(self, *_args) -> None:
            self.background_color = (
                (0.76, 0.88, 0.97, 1.0)
                if self.state == "down"
                else CHOICE_BUTTON_BACKGROUND
            )

    class ChoiceButton(JapaneseButton):
        """White answer button with a visible border on light mobile themes."""

        def __init__(self, **kwargs):
            self._preferred_font_sp = float(
                kwargs.pop("preferred_font_sp", 16.0)
            )
            self._minimum_font_sp = float(kwargs.pop("minimum_font_sp", 9.0))
            self._fit_plain_text = str(kwargs.get("text", ""))
            self._font_fit_running = False
            kwargs["font_size"] = sp(self._preferred_font_sp)
            kwargs.setdefault("background_color", CHOICE_BUTTON_BACKGROUND)
            kwargs.setdefault("background_down", "")
            kwargs.setdefault("color", MOBILE_BUTTON_TEXT)
            kwargs.setdefault("halign", "center")
            kwargs.setdefault("valign", "middle")
            super().__init__(**kwargs)
            with self.canvas.after:
                self._choice_border_color = Color(*CHOICE_BORDER_COLOR)
                self._choice_border = Line(
                    rectangle=(self.x, self.y, self.width, self.height),
                    width=dp(1.15),
                )
            self.bind(pos=self._update_choice_border, size=self._update_choice_border)
            self.bind(width=self._fit_font_to_width, text=self._capture_text_and_fit)
            Clock.schedule_once(self._fit_font_to_width, 0)

        def set_fitted_text(self, value: str) -> None:
            """Update a choice without changing its fixed row geometry."""
            self._fit_plain_text = value
            self.text = value
            self._fit_font_to_width()

        def _capture_text_and_fit(self, *_args) -> None:
            self._fit_plain_text = self.text
            self._fit_font_to_width()

        def _fit_font_to_width(self, *_args) -> None:
            if self._font_fit_running:
                return
            available_width = max(0.0, self.width - dp(18))
            if available_width <= 0:
                return
            self._font_fit_running = True
            try:
                natural_line_widths: List[float] = []
                for line in self._fit_plain_text.split("\n"):
                    probe = CoreLabel(
                        text=line or " ",
                        font_name=self.font_name,
                        font_size=sp(self._preferred_font_sp),
                    )
                    probe.refresh()
                    natural_line_widths.append(float(probe.texture.size[0]))
                fitted_lines, fitted_sp = fitted_choice_text_layout(
                    natural_line_widths,
                    available_width,
                    preferred_sp=self._preferred_font_sp,
                    minimum_sp=self._minimum_font_sp,
                )
                self.shorten = fitted_lines == 1
                if hasattr(self, "max_lines"):
                    self.max_lines = fitted_lines
                self.font_size = sp(fitted_sp)
            finally:
                self._font_fit_running = False

        def _update_choice_border(self, *_args) -> None:
            self._choice_border.rectangle = (
                self.x,
                self.y,
                self.width,
                self.height,
            )

    class AppInput(MobileReviewInputMixin, TextInput):
        def __init__(self, **kwargs):
            kwargs.setdefault("font_name", POLISH_FONT)
            kwargs.setdefault("font_size", "18sp")
            kwargs.setdefault("multiline", False)
            kwargs.setdefault("unfocus_on_touch", False)
            kwargs.setdefault("text_validate_unfocus", False)
            kwargs.setdefault("write_tab", False)
            kwargs.setdefault("size_hint_y", None)
            kwargs.setdefault("height", dp(46))
            super().__init__(**kwargs)

    def vertical_root(*, padding=12, spacing=8) -> BoxLayout:
        return BoxLayout(
            orientation="vertical",
            padding=dp(padding),
            spacing=dp(spacing),
        )

    def button_row(buttons: List[Button], height: int = 60) -> BoxLayout:
        controller = quiz_app()
        button_scale = getattr(
            getattr(controller, "settings", None),
            "mobile_button_scale",
            1.0,
        )
        row = BoxLayout(
            size_hint_y=None,
            height=dp(scaled_button_height(height, button_scale)),
            spacing=dp(8),
        )
        row._mobile_base_height = dp(height)
        for button in buttons:
            row.add_widget(button)
        return row

    def scroll_stack(
        spacing: int = 6,
        *,
        interactive_bar: bool = False,
    ) -> tuple[ScrollView, GridLayout]:
        scroll_options = {
            "do_scroll_x": False,
            "do_scroll_y": True,
        }
        if interactive_bar:
            # Kivy's default bar is only an indicator. Enabling the ``bars``
            # scroll type makes the visible Android bar draggable as users
            # expect, while ``content`` preserves normal finger scrolling.
            scroll_options.update(
                scroll_type=["content", "bars"],
                bar_width=dp(14),
                scroll_distance=dp(8),
                scroll_timeout=160,
            )
        scroll = ScrollView(**scroll_options)
        stack = GridLayout(
            cols=1,
            spacing=dp(spacing),
            size_hint_x=1,
            size_hint_y=None,
            padding=(0, 0, dp(20) if interactive_bar else dp(4), dp(10)),
        )
        stack.bind(minimum_height=stack.setter("height"))
        scroll.add_widget(stack)
        return scroll, stack

    def field_label(field_name: str) -> str:
        return ui_text(
            f"quiz_field.{field_name}",
            FIELD_LABELS.get(field_name, field_name),
        )

    def field_from_label(label: str) -> str:
        for field_name, legacy_label in FIELD_LABELS.items():
            if label in {legacy_label, field_label(field_name)}:
                return field_name
        return "translation"

    def form_label(form_name: str) -> str:
        return ui_text(
            f"quiz_form.{form_name}",
            FORM_LABELS.get(form_name, form_name),
        )

    def is_japanese_text(value: str) -> bool:
        return any(
            "\u3040" <= character <= "\u30ff"
            or "\u3400" <= character <= "\u9fff"
            for character in value
        )

    def font_markup(value: str, japanese: Optional[bool] = None) -> str:
        use_japanese = is_japanese_text(value) if japanese is None else japanese
        font = JAPANESE_FONT if use_japanese else POLISH_FONT
        return f"[font={font}]{escape_markup(value)}[/font]"

    def mixed_markup(parts: List[str] | str) -> str:
        values = parts.split(" | ") if isinstance(parts, str) else parts
        return "  |  ".join(font_markup(value) for value in values if value)

    class BaseScreen(Screen):
        @property
        def kotomi(self):
            return quiz_app()

        def show_error(self, message: str) -> None:
            self.kotomi.show_message(
                ui_text("mobile.error_title", ""),
                message,
                bad=True,
            )

    class LessonsScreen(BaseScreen):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.open_groups: set[str] = set()
            self.open_courses: set[tuple[str, str]] = set()
            self.root_layout = vertical_root()
            self.title = AppLabel(
                text=ui_text('hub.app.lessons.title', ""),
                font_size="24sp",
                color=ACCENT_COLOR,
            )
            self.root_layout.add_widget(self.title)

            settings_button = AppButton(text=ui_text("action.settings", ""))
            settings_button.bind(
                on_release=lambda *_: setattr(self.manager, "current", "settings")
            )
            grammar_button = AppButton(text=ui_text("mobile.quiz_menu", ""))
            grammar_button.bind(on_release=lambda *_: return_to_quiz_menu())
            self.root_layout.add_widget(button_row([settings_button, grammar_button]))
            self.scroll, self.stack = scroll_stack()
            self.root_layout.add_widget(self.scroll)
            self.add_widget(self.root_layout)

        def on_pre_enter(self, *_args):
            self.refresh()

        def refresh(self) -> None:
            self.stack.clear_widgets()
            hierarchy = self.kotomi.catalog.hierarchy()
            if not hierarchy:
                self.stack.add_widget(
                    AppLabel(
                        text=ui_text(
                            "mobile.no_lessons",
                            "",
                        )
                    )
                )
                return
            for group_name in sorted(hierarchy, key=str.casefold):
                group_open = group_name in self.open_groups
                group_button = AppButton(
                    text=("▼  " if group_open else "▶  ") + group_name,
                    halign="left",
                    background_color=(0.86, 0.92, 0.98, 1),
                )
                group_button.bind(
                    on_release=lambda _button, value=group_name: self.toggle_group(value)
                )
                self.stack.add_widget(group_button)
                if not group_open:
                    continue
                courses = hierarchy[group_name]
                for main_name in sorted(courses, key=str.casefold):
                    course_key = (group_name, main_name)
                    course_open = course_key in self.open_courses
                    course_button = AppButton(
                        text=("    ▼  " if course_open else "    ▶  ") + main_name,
                        halign="left",
                        height=dp(44),
                    )
                    course_button.bind(
                        on_release=lambda _button, value=course_key: self.toggle_course(value)
                    )
                    self.stack.add_widget(course_button)
                    if not course_open:
                        continue
                    for lesson in courses[main_name]:
                        count = len(lesson.word_refs)
                        button = AppButton(
                            text=f"        {lesson.sub_name}    ({count})",
                            halign="left",
                        )
                        button.bind(
                            on_release=lambda _button, lesson_id=lesson.id: (
                                self.kotomi.open_lesson(lesson_id)
                            )
                        )
                        self.stack.add_widget(button)

        def toggle_group(self, group_name: str) -> None:
            if group_name in self.open_groups:
                self.open_groups.remove(group_name)
            else:
                self.open_groups.add(group_name)
            self.refresh()

        def toggle_course(self, course_key: tuple[str, str]) -> None:
            if course_key in self.open_courses:
                self.open_courses.remove(course_key)
            else:
                self.open_courses.add(course_key)
            self.refresh()

    class SettingsScreen(BaseScreen):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            root = vertical_root()
            root.add_widget(
                AppLabel(
                    text=ui_text("settings.title", ""),
                    font_size="24sp",
                    color=ACCENT_COLOR,
                )
            )
            settings_scroll, settings_content = scroll_stack(7)
            root.add_widget(settings_scroll)
            labels = [field_label(name) for name in FIELD_LABELS]
            settings_content.add_widget(
                AppLabel(text=ui_text("settings.show", ""))
            )
            self.asked = Spinner(
                values=labels,
                font_name=POLISH_FONT,
                size_hint_y=None,
                height=dp(48),
            )
            settings_content.add_widget(self.asked)
            settings_content.add_widget(
                AppLabel(text=ui_text("settings.expect", ""))
            )
            self.answer = Spinner(
                values=labels,
                font_name=POLISH_FONT,
                size_hint_y=None,
                height=dp(48),
            )
            settings_content.add_widget(self.answer)
            flip = AppButton(text=ui_text("settings.reverse", ""))
            flip.bind(on_release=lambda *_: self.flip())
            settings_content.add_widget(flip)
            settings_content.add_widget(
                AppLabel(text=ui_text(
                    "settings.learning_target",
                    "",
                ))
            )
            self.target = AppInput(text="1", input_filter="int")
            settings_content.add_widget(self.target)
            settings_content.add_widget(
                AppLabel(text=ui_text(
                    "mobile.button_scale",
                    "",
                ))
            )
            self.button_scale = AppInput(text="100", input_filter="int")
            settings_content.add_widget(self.button_scale)
            settings_content.add_widget(
                AppLabel(
                    text=(
                        ui_text(
                            "settings.learning_help",
                            "",
                        )
                    ),
                    color=MUTED_COLOR,
                )
            )
            back = AppButton(text=ui_text("action.cancel", ""))
            back.bind(on_release=lambda *_: setattr(self.manager, "current", "lessons"))
            save = AppButton(text=ui_text("action.save", ""))
            save.bind(on_release=lambda *_: self.save())
            root.add_widget(button_row([back, save]))
            self.add_widget(root)

        def on_pre_enter(self, *_args):
            settings = self.kotomi.settings
            self.asked.text = field_label(settings.asked_field)
            self.answer.text = field_label(settings.answer_field)
            self.target.text = str(settings.required_correct_answers)
            self.button_scale.text = str(round(settings.mobile_button_scale * 100))

        def flip(self) -> None:
            asked = self.asked.text
            self.asked.text = self.answer.text
            self.answer.text = asked

        def save(self) -> None:
            try:
                settings = copy.deepcopy(self.kotomi.settings)
                settings.asked_field = field_from_label(self.asked.text)
                settings.answer_field = field_from_label(self.answer.text)
                settings.required_correct_answers = int(self.target.text)
                settings.mobile_button_scale = int(self.button_scale.text) / 100.0
                settings.validate()
            except (TypeError, ValueError) as exception:
                self.show_error(mobile_error_text(self, exception))
                return
            self.kotomi.settings = settings
            self.kotomi.settings_store.save(settings.to_dict())
            self.kotomi.apply_button_scale(settings.mobile_button_scale)
            self.manager.current = "lessons"

    class LessonDetailScreen(BaseScreen):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            root = vertical_root()
            self.title = AppLabel(font_size="22sp", color=ACCENT_COLOR)
            root.add_widget(self.title)
            back_button = AppButton(text=ui_text("action.back", ""))
            back_button.bind(on_release=lambda *_: setattr(self.manager, "current", "lessons"))
            root.add_widget(back_button)

            written = AppButton(text=ui_text("quiz.written", ""))
            written.bind(on_release=lambda *_: self.open_basic("written"))
            choice = AppButton(text=ui_text("quiz.choice", ""))
            choice.bind(on_release=lambda *_: self.open_basic("choice"))
            forms = AppButton(text=ui_text("quiz.conjugation", ""))
            forms.bind(on_release=lambda *_: setattr(self.manager, "current", "forms_setup"))
            sentences = AppButton(text=ui_text("quiz.sentence", ""))
            sentences.bind(
                on_release=lambda *_: setattr(self.manager, "current", "sentence_setup")
            )
            root.add_widget(button_row([written, choice]))
            root.add_widget(button_row([forms, sentences]))
            self.scroll, self.stack = scroll_stack()
            root.add_widget(self.scroll)
            self.add_widget(root)

        def on_pre_enter(self, *_args):
            lesson = self.kotomi.current_lesson()
            self.title.text = lesson.path
            self.stack.clear_widgets()
            for word in self.kotomi.catalog.words_for(lesson):
                values = [
                    value
                    for value in (word.translation, word.kana, word.kanji, word.romaji)
                    if is_available(value)
                ]
                self.stack.add_widget(
                    AppLabel(
                        text=mixed_markup(values),
                        markup=True,
                        font_size="17sp",
                    )
                )

        def open_basic(self, mode: str) -> None:
            self.kotomi.basic_mode = mode
            self.kotomi.settings.last_lesson_quiz_mode = mode
            self.kotomi.settings_store.save(self.kotomi.settings.to_dict())
            self.manager.current = "basic_setup"

        def confirm_delete(self) -> None:
            lesson = self.kotomi.current_lesson()
            content = vertical_root()
            content.add_widget(AppLabel(text=ui_text(
                "mobile.delete_lesson",
                "",
                lesson=lesson.path,
            )))
            popup = Popup(
                title=ui_text("mobile.delete_lesson_title", ""),
                content=content,
                size_hint=(0.90, None),
                height=dp(210),
            )
            yes = AppButton(text=ui_text("action.delete", ""))
            no = AppButton(text=ui_text("action.cancel", ""))
            yes.bind(on_release=lambda *_: self._delete(popup))
            no.bind(on_release=lambda *_: popup.dismiss())
            content.add_widget(button_row([no, yes]))
            popup.open()

        def _delete(self, popup: Popup) -> None:
            self.kotomi.catalog.delete_lesson(self.kotomi.selected_lesson_id)
            self.kotomi.catalog.remove_unreferenced_words()
            self.kotomi.save_catalog()
            popup.dismiss()
            self.manager.current = "lessons"

    class BasicSetupScreen(BaseScreen):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            root = vertical_root()
            self.title = AppLabel(font_size="22sp", color=ACCENT_COLOR)
            root.add_widget(self.title)
            root.add_widget(
                AppLabel(text=ui_text("settings.show", ""))
            )
            labels = [field_label(name) for name in FIELD_LABELS]
            self.asked = Spinner(
                text=field_label("translation"),
                values=labels,
                font_name=POLISH_FONT,
                size_hint_y=None,
                height=dp(48),
            )
            root.add_widget(self.asked)
            root.add_widget(
                AppLabel(text=ui_text("settings.expect", ""))
            )
            self.answer = Spinner(
                text=field_label("kana"),
                values=labels,
                font_name=POLISH_FONT,
                size_hint_y=None,
                height=dp(48),
            )
            root.add_widget(self.answer)
            self.count = AppLabel(color=MUTED_COLOR)
            root.add_widget(self.count)
            root.add_widget(Widget())
            start = AppButton(text=ui_text("action.start", ""))
            start.bind(on_release=lambda *_: self.start())
            back = AppButton(text=ui_text("action.back", ""))
            back.bind(on_release=lambda *_: setattr(self.manager, "current", "lesson"))
            root.add_widget(button_row([back, start]))
            self.asked.bind(text=lambda *_: self.refresh_count())
            self.answer.bind(text=lambda *_: self.refresh_count())
            self.add_widget(root)

        def on_pre_enter(self, *_args):
            label = (
                ui_text("quiz.written", "")
                if self.kotomi.basic_mode == "written"
                else ui_text("quiz.choice", "")
            )
            self.title.text = label + "\n" + self.kotomi.current_lesson().path
            self.asked.text = field_label(self.kotomi.settings.asked_field)
            self.answer.text = field_label(self.kotomi.settings.answer_field)
            self.refresh_count()

        def refresh_count(self) -> None:
            try:
                count = eligible_count(
                    self.kotomi.catalog,
                    self.kotomi.current_lesson(),
                    field_from_label(self.asked.text),
                    field_from_label(self.answer.text),
                )
                self.count.text = ui_text(
                    "mobile.available_words",
                    "",
                    count=count,
                )
            except ValueError as exception:
                self.count.text = mobile_error_text(self, exception)

        def start(self) -> None:
            asked = field_from_label(self.asked.text)
            answer = field_from_label(self.answer.text)
            try:
                updated = copy.deepcopy(self.kotomi.settings)
                updated.asked_field = asked
                updated.answer_field = answer
                updated.validate()
                self.kotomi.settings = updated
                self.kotomi.settings_store.save(updated.to_dict())
                factory = (
                    build_written_questions
                    if self.kotomi.basic_mode == "written"
                    else build_choice_questions
                )
                questions = factory(
                    self.kotomi.catalog,
                    self.kotomi.current_lesson(),
                    asked,
                    answer,
                )
                self.kotomi.start_quiz(questions, self.title.text)
            except ValueError as exception:
                self.show_error(mobile_error_text(self, exception))

    class FormsSetupScreen(BaseScreen):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            root = vertical_root()
            self.title = AppLabel(font_size="22sp", color=ACCENT_COLOR)
            root.add_widget(self.title)
            root.add_widget(
                AppLabel(text=ui_text(
                    "quiz.question_field",
                    "",
                ))
            )
            self.asked = Spinner(
                text=field_label("translation"),
                values=[field_label(name) for name in FIELD_LABELS],
                font_name=POLISH_FONT,
                size_hint_y=None,
                height=dp(48),
            )
            root.add_widget(self.asked)
            root.add_widget(AppLabel(text=ui_text("quiz.forms", "")))
            select_all = AppButton(text=ui_text("action.select_all", ""))
            select_all.bind(on_release=lambda *_: self.set_all_forms(True))
            clear = AppButton(
                text=ui_text("action.clear_selection", "")
            )
            clear.bind(on_release=lambda *_: self.set_all_forms(False))
            root.add_widget(button_row([select_all, clear]))
            scroll, self.form_stack = scroll_stack(6, interactive_bar=True)
            self.checks: Dict[str, MobileOptionToggle] = {}
            for form_name in FORM_ORDER:
                check = MobileOptionToggle(text=form_label(form_name))
                self.checks[form_name] = check
                self.form_stack.add_widget(check)
            root.add_widget(scroll)
            start = AppButton(text=ui_text("action.start", ""))
            start.bind(on_release=lambda *_: self.start())
            back = AppButton(text=ui_text("action.back", ""))
            back.bind(on_release=lambda *_: setattr(self.manager, "current", "lesson"))
            root.add_widget(button_row([back, start]))
            self.add_widget(root)

        def set_all_forms(self, active: bool) -> None:
            for check in self.checks.values():
                if not check.disabled:
                    check.active = active

        def on_pre_enter(self, *_args):
            lesson = self.kotomi.current_lesson()
            self.title.text = ui_text("quiz.conjugation", "") + "\n" + lesson.path
            self.asked.text = field_label(self.kotomi.settings.asked_field)
            available = set(available_forms(self.kotomi.catalog, lesson))
            for form_name, check in self.checks.items():
                check.disabled = form_name not in available
                check.active = (
                    form_name in available
                    and form_name in self.kotomi.settings.conjugation_forms
                )

        def start(self) -> None:
            selected = [name for name, check in self.checks.items() if check.active]
            try:
                questions = build_conjugation_questions(
                    self.kotomi.catalog,
                    self.kotomi.current_lesson(),
                    field_from_label(self.asked.text),
                    selected,
                )
                self.kotomi.settings.asked_field = field_from_label(self.asked.text)
                self.kotomi.settings.conjugation_forms = selected
                self.kotomi.settings_store.save(self.kotomi.settings.to_dict())
                self.kotomi.start_quiz(questions, self.title.text)
            except ValueError as exception:
                self.show_error(mobile_error_text(self, exception))

    class SentenceSetupScreen(BaseScreen):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            root = vertical_root()
            self.title = AppLabel(
                text=ui_text("quiz.sentence_title", ""),
                font_size="22sp",
                color=ACCENT_COLOR,
            )
            root.add_widget(self.title)
            self.report = AppLabel(color=MUTED_COLOR)
            root.add_widget(self.report)
            self.options_scroll, self.option_stack = scroll_stack(
                2,
                interactive_bar=True,
            )
            self.option_stack.add_widget(
                AppLabel(text=ui_text("quiz.patterns", ""), font_size="19sp")
            )
            self.pattern_checks: Dict[str, MobileOptionToggle] = {}
            self.form_checks: Dict[str, MobileOptionToggle] = {}
            root.add_widget(self.options_scroll)
            root.add_widget(
                AppLabel(
                    text=ui_text("mobile.question_count", ""),
                    fixed_height=32,
                    single_line=True,
                )
            )
            self.question_count = AppInput(text="10", input_filter="int")
            root.add_widget(self.question_count)
            start = AppButton(text=ui_text("action.start", ""))
            start.bind(on_release=lambda *_: self.start())
            calculate = AppButton(
                text=ui_text("quiz.calculate_possibilities", "")
            )
            calculate.bind(on_release=lambda *_: self.show_possibilities())
            back = AppButton(text=ui_text("action.back", ""))
            back.bind(on_release=lambda *_: setattr(self.manager, "current", "lesson"))
            root.add_widget(calculate)
            root.add_widget(button_row([back, start]))
            self.add_widget(root)

        def on_pre_enter(self, *_args):
            report = self.kotomi.sentence_engine.compatibility(
                self.kotomi.catalog,
                self.kotomi.current_lesson(),
            )
            self.report.text = compatibility_text(report)
            self.option_stack.clear_widgets()
            self.option_stack.add_widget(
                AppLabel(text=ui_text("quiz.patterns", ""), font_size="19sp")
            )
            self.option_stack.add_widget(
                AppLabel(
                    text=ui_text(
                        "quiz.patterns_help",
                        "",
                    ),
                    color=MUTED_COLOR,
                    font_size="15sp",
                )
            )
            all_patterns = AppButton(
                text=ui_text("action.select_all", "")
            )
            all_patterns.bind(on_release=lambda *_: self.set_all_patterns(True))
            clear_patterns = AppButton(
                text=ui_text("action.clear_selection", "")
            )
            clear_patterns.bind(on_release=lambda *_: self.set_all_patterns(False))
            self.option_stack.add_widget(button_row([all_patterns, clear_patterns]))
            self.pattern_checks = {}
            saved_patterns = set(self.kotomi.settings.sentence_patterns)
            for option in self.kotomi.sentence_engine.pattern_options():
                suffix = (
                    ui_text("quiz.composite_suffix", "")
                    if option.composite
                    else ""
                )
                if option.id not in report.supported_patterns:
                    suffix += ui_text(
                        "quiz.no_lesson_match_suffix",
                        "",
                    )
                option_toggle = MobileOptionToggle(
                    text=option.label + suffix,
                    active=(
                        option.id in saved_patterns
                        and option.id in report.supported_patterns
                    ),
                )
                option_toggle.disabled = option.id not in report.supported_patterns
                self.pattern_checks[option.id] = option_toggle
                self.option_stack.add_widget(option_toggle)
            self.option_stack.add_widget(
                AppLabel(text=ui_text("quiz.forms", ""), font_size="19sp")
            )
            all_forms = AppButton(
                text=ui_text("action.select_all", "")
            )
            all_forms.bind(on_release=lambda *_: self.set_all_forms(True))
            clear_forms = AppButton(
                text=ui_text("action.clear_selection", "")
            )
            clear_forms.bind(on_release=lambda *_: self.set_all_forms(False))
            self.option_stack.add_widget(button_row([all_forms, clear_forms]))
            self.option_stack.add_widget(
                AppLabel(
                    text=ui_text(
                        "quiz.forms_help",
                        "",
                    ),
                    color=MUTED_COLOR,
                    font_size="15sp",
                )
            )
            self.form_checks = {}
            saved_forms = set(self.kotomi.settings.sentence_forms)
            available_forms = list(
                self.kotomi.sentence_engine.available_form_names()
            )
            form_groups = (
                (
                    ui_text("quiz.verb_forms", ""),
                    [name for name in available_forms if not name.startswith("predicate_")],
                ),
                (
                    ui_text("quiz.adjective_forms", ""),
                    [name for name in available_forms if name.startswith("predicate_")],
                ),
            )
            for heading, form_names in form_groups:
                if not form_names:
                    continue
                self.option_stack.add_widget(
                    AppLabel(text=heading, font_size="17sp", color=ACCENT_COLOR)
                )
                for form_name in form_names:
                    option_toggle = MobileOptionToggle(
                        text=form_label(form_name),
                        active=form_name in saved_forms,
                    )
                    self.form_checks[form_name] = option_toggle
                    self.option_stack.add_widget(option_toggle)
            self.question_count.text = str(
                self.kotomi.settings.sentence_question_count
            )
            Clock.schedule_once(self._reset_options_scroll, 0)

        def _reset_options_scroll(self, _dt: float) -> None:
            """Start at the first option after Kivy finishes viewport layout."""
            self.options_scroll.scroll_y = 1.0

        def set_all_forms(self, active: bool) -> None:
            for check in self.form_checks.values():
                check.active = active

        def set_all_patterns(self, active: bool) -> None:
            for check in self.pattern_checks.values():
                if not check.disabled:
                    check.active = active

        def selected_values(self):
            patterns = [name for name, check in self.pattern_checks.items() if check.active]
            forms = [name for name, check in self.form_checks.items() if check.active]
            count = int(self.question_count.text)
            return patterns, forms, count

        def save_settings(self, patterns, forms, count) -> None:
            self.kotomi.settings.sentence_patterns = patterns
            self.kotomi.settings.sentence_forms = forms
            self.kotomi.settings.sentence_question_count = count
            self.kotomi.settings_store.save(self.kotomi.settings.to_dict())

        def show_possibilities(self) -> None:
            try:
                patterns, forms, count = self.selected_values()
                if not patterns:
                    raise ValueError("Wybierz co najmniej jeden wzorzec zdania.")
                self.save_settings(patterns, forms, count)
                self.kotomi.sentence_statistics_request = (patterns, forms)
                self.manager.current = "sentence_statistics"
            except (TypeError, ValueError) as exception:
                self.show_error(mobile_error_text(self, exception))

        def start(self) -> None:
            try:
                patterns, forms, count = self.selected_values()
                questions = self.kotomi.sentence_engine.build_questions(
                    self.kotomi.catalog,
                    self.kotomi.current_lesson(),
                    patterns,
                    forms,
                    count,
                )
                self.save_settings(patterns, forms, count)
                self.kotomi.start_quiz(
                    questions,
                    ui_text("quiz.sentence_title", ""),
                )
            except (ValueError, TypeError) as exception:
                self.show_error(mobile_error_text(self, exception))

    class SentenceStatisticsScreen(BaseScreen):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            root = vertical_root()
            root.add_widget(
                AppLabel(
                    text=ui_text("quiz.possibilities_title", ""),
                    font_size="22sp",
                    color=ACCENT_COLOR,
                )
            )
            root.add_widget(
                AppLabel(
                    text=ui_text(
                        "quiz.possibilities_explanation",
                        "",
                    ),
                    color=MUTED_COLOR,
                )
            )
            self.scroll, self.stack = scroll_stack(4)
            root.add_widget(self.scroll)
            back = AppButton(text=ui_text("action.back", ""))
            back.bind(on_release=lambda *_: setattr(self.manager, "current", "sentence_setup"))
            root.add_widget(back)
            self.add_widget(root)

        def on_pre_enter(self, *_args):
            self.stack.clear_widgets()
            self.stack.add_widget(
                AppLabel(
                    text=ui_text("quiz.calculating", ""),
                    color=MUTED_COLOR,
                )
            )
            request = getattr(self.kotomi, "sentence_statistics_request", ([], []))

            def calculate() -> None:
                try:
                    report = self.kotomi.sentence_engine.count_possibilities(
                        self.kotomi.catalog,
                        self.kotomi.current_lesson(),
                        request[0],
                        request[1],
                    )
                    content = possibilities_text(report)
                except (TypeError, ValueError) as exception:
                    content = mobile_error_text(self, exception)
                Clock.schedule_once(lambda _dt: self.show_content(content), 0)

            threading.Thread(target=calculate, daemon=True).start()

        def show_content(self, content: str) -> None:
            self.stack.clear_widgets()
            self.stack.add_widget(
                AppLabel(text=content, halign="left", valign="top")
            )

    class QuizScreen(BaseScreen):
        """Fixed mobile quiz surface that never becomes a draggable canvas."""

        INPUT_ANSWER_FIELDS = {"kana", "kanji", "japanese_form", "sentence"}

        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.root_layout = vertical_root(
                padding=MOBILE_QUIZ_LAYOUT.root_padding,
                spacing=MOBILE_QUIZ_LAYOUT.root_spacing,
            )
            self.add_widget(self.root_layout)
            self.answer_input: Optional[TextInput] = None
            self.result_row: Optional[BoxLayout] = None
            self.correct_result_label: Optional[AdaptiveSingleLineLabel] = None
            self.choice_buttons: Dict[str, Button] = {}
            self.choice_locked = False
            self.choice_event = None
            # Kept as compatibility attributes for embedded-controller cleanup.
            # The active quiz deliberately contains no ScrollView.
            self.quiz_scroll = None
            self.hint_scroll = None
            self.content_layout: Optional[BoxLayout] = None
            self.hint_label: Optional[AdaptiveSingleLineLabel] = None
            self.hint_button: Optional[Button] = None
            self.hint_visible = False
            self.primary_button: Optional[Button] = None
            self.secondary_button: Optional[Button] = None
            self.current_mode = ""
            self.review_locked = False
            self.focus_request = FocusRequest()
            self.progress_bar: Optional[ProgressBar] = None
            self.progress_label: Optional[AdaptiveSingleLineLabel] = None
            self.form_label: Optional[AdaptiveSingleLineLabel] = None
            self.prompt_label: Optional[AdaptiveSingleLineLabel] = None

        def tr(self, key: str, fallback: str = "", **values: object) -> str:
            translated = mobile_text(self.kotomi, key, **values)
            if translated == key and fallback:
                try:
                    return fallback.format(**values)
                except (KeyError, ValueError):
                    return fallback
            return translated

        def on_pre_enter(self, *_args):
            session = self.kotomi.session
            if session is not None and session.current is None:
                session.next_question()
            self.render()

        def on_enter(self, *_args):
            self.keep_keyboard_visible()

        def on_leave(self, *_args):
            self.focus_request.cancel()
            self.cancel_choice_event()
            if self.answer_input is not None:
                self.answer_input.focus = False

        def cancel_choice_event(self) -> None:
            if self.choice_event is not None:
                self.choice_event.cancel()
                self.choice_event = None

        @staticmethod
        def question_mode(question: Question) -> str:
            if question.options:
                return "choice"
            if question.answer_field == "japanese_form":
                return "conjugation"
            if question.answer_field == "sentence":
                return "sentence"
            return "written"

        def answer_form_label(self, question: Question) -> str:
            form_name = question.metadata.get("form", "")
            if form_name:
                key = f"quiz_form.{form_name}"
                return self.tr(key, FORM_LABELS.get(form_name, form_name))
            key = f"quiz_field.{question.answer_field}"
            fallback = field_label(question.answer_field)
            if question.answer_field == "sentence":
                fallback = self.tr("quiz.sentence", "")
            return self.tr(key, fallback)

        def question_markup(self, question: Question) -> str:
            """Return the complete question without repeating its form."""
            if self.question_mode(question) in {"conjugation", "sentence"}:
                return (
                    f"[color={PROMPT_VALUE_COLOR}]"
                    f"{font_markup(question.prompt)}[/color]"
                )
            return escape_markup(question.prompt)

        def question_plain_text(self, question: Question) -> str:
            """Return prompt text without markup for accurate width measurement."""
            return question.prompt

        def compact_progress_text(self, session: QuizSession) -> str:
            """Keep progress and outcome counters in one mobile header line."""
            current = min(session.learnt_items + 1, session.total_items)
            question_progress = self.tr(
                "mobile.compact_question_progress",
                "",
                current=current,
                total=session.total_items,
            )
            return (
                f"{question_progress}   "
                f"✓{session.correct}  ×{session.wrong}  ✓+{session.accepted}"
            )

        def form_text(self, question: Question) -> str:
            """Use the former statistics row for the requested answer form."""
            if self.question_mode(question) == "written":
                return ""
            if (
                self.question_mode(question) == "sentence"
                and question.metadata.get("pattern_kind") == "composite"
            ):
                pattern_label = (
                    question.metadata.get("pattern_label")
                    or question.metadata.get("pattern_reference")
                    or question.metadata.get("pattern", "")
                )
                pattern_reference = str(
                    question.metadata.get("pattern_reference", "") or ""
                )
                if pattern_reference:
                    pattern_label = self.tr(
                        f"quiz_pattern.{pattern_reference}",
                        str(pattern_label),
                    )
                return (
                    f"{self.tr('form.pattern', '')}: "
                    f"{pattern_label}"
                )
            return (
                f"{self.tr('form.name', '')}: "
                f"{self.answer_form_label(question)}"
            )

        def answer_placeholder_text(self) -> str:
            """Return the stable empty answer row used by typed mobile modes."""
            return f"{self.tr('mobile.answer', '')}:"

        def mount_answer_row(self) -> None:
            """Mount the fixed review row between the form and the question."""
            self.result_row = BoxLayout(
                size_hint_y=None,
                height=dp(MOBILE_QUIZ_LAYOUT.review_height),
                padding=(
                    dp(MOBILE_QUIZ_LAYOUT.content_horizontal_padding),
                    0,
                    dp(MOBILE_QUIZ_LAYOUT.content_horizontal_padding),
                    0,
                ),
            )
            placeholder = self.answer_placeholder_text()
            self.correct_result_label = AdaptiveSingleLineLabel(
                text=placeholder,
                fit_plain_text=placeholder,
                markup=True,
                color=MUTED_COLOR,
                preferred_font_sp=MOBILE_QUIZ_LAYOUT.review_preferred_sp,
                minimum_font_sp=MOBILE_QUIZ_LAYOUT.review_minimum_sp,
                allow_shorten=False,
                fixed_height=MOBILE_QUIZ_LAYOUT.review_height,
                single_line=True,
                halign="left",
            )
            self.result_row.add_widget(self.correct_result_label)
            self.root_layout.add_widget(self.result_row)

        def render(self) -> None:
            self.focus_request.cancel()
            persistent_input = self.answer_input
            if persistent_input is not None and persistent_input.parent is not None:
                persistent_input.parent.remove_widget(persistent_input)
            self.root_layout.clear_widgets()
            self.answer_input = None
            self.result_row = None
            self.correct_result_label = None
            self.choice_buttons = {}
            self.hint_label = None
            self.hint_button = None
            self.primary_button = None
            self.secondary_button = None
            self.progress_label = None
            self.form_label = None
            self.prompt_label = None
            self.hint_visible = False
            self.choice_locked = False
            self.review_locked = False
            session = self.kotomi.session
            if session is None:
                if persistent_input is not None:
                    persistent_input.focus = False
                self.root_layout.add_widget(
                    AppLabel(text=self.tr("mobile.no_active_quiz", ""))
                )
                return
            if session.current is None:
                if persistent_input is not None:
                    persistent_input.focus = False
                self.render_summary(session)
                return

            question = session.current
            self.current_mode = self.question_mode(question)
            scale = self.kotomi.settings.mobile_button_scale
            header_height = scaled_button_height(
                MOBILE_QUIZ_LAYOUT.header_height,
                scale,
            )
            title_row = BoxLayout(
                size_hint_y=None,
                height=dp(header_height),
                spacing=dp(6),
            )
            title_row._mobile_base_height = dp(
                MOBILE_QUIZ_LAYOUT.header_height
            )
            self.progress_label = AdaptiveSingleLineLabel(
                text=self.compact_progress_text(session),
                fit_plain_text=self.compact_progress_text(session),
                color=ACCENT_COLOR,
                preferred_font_sp=16,
                minimum_font_sp=8,
                maximum_fit_lines=1,
                allow_shorten=False,
                fixed_height=MOBILE_QUIZ_LAYOUT.header_height,
                single_line=True,
            )
            title_row.add_widget(self.progress_label)
            close = AppButton(
                text=self.tr("mobile.finish_quiz", ""),
                height=dp(MOBILE_QUIZ_LAYOUT.header_height),
                size_hint_x=None,
                width=dp(92),
            )
            close.bind(on_release=lambda *_: self.close_quiz())
            title_row.add_widget(close)
            self.root_layout.add_widget(title_row)
            self.progress_bar = ProgressBar(
                max=1.0,
                value=session.progress,
                size_hint_y=None,
                height=dp(MOBILE_QUIZ_LAYOUT.progress_height),
            )
            self.root_layout.add_widget(self.progress_bar)
            form_text = self.form_text(question)
            if form_text:
                self.form_label = AdaptiveSingleLineLabel(
                    text=form_text,
                    fit_plain_text=form_text,
                    color=MUTED_COLOR,
                    preferred_font_sp=14,
                    minimum_font_sp=1,
                    maximum_fit_lines=1,
                    allow_shorten=False,
                    fixed_height=MOBILE_QUIZ_LAYOUT.form_height,
                    single_line=True,
                )
                self.root_layout.add_widget(self.form_label)
            self.update_progress(session)

            if not question.options:
                self.mount_answer_row()

            # A regular BoxLayout keeps the quiz pinned to the top.  A final
            # flexible spacer consumes spare room without enabling drag/scroll.
            self.content_layout = BoxLayout(
                orientation="vertical",
                spacing=dp(MOBILE_QUIZ_LAYOUT.content_spacing),
                padding=(
                    dp(MOBILE_QUIZ_LAYOUT.content_horizontal_padding),
                    0,
                    dp(MOBILE_QUIZ_LAYOUT.content_horizontal_padding),
                    0,
                ),
                size_hint_y=None,
            )
            self.content_layout.bind(
                minimum_height=self.content_layout.setter("height")
            )
            content_anchor = AnchorLayout(anchor_x="left", anchor_y="top")
            content_anchor.add_widget(self.content_layout)
            self.root_layout.add_widget(content_anchor)
            self.prompt_label = AdaptiveSingleLineLabel(
                text=self.question_markup(question),
                fit_plain_text=self.question_plain_text(question),
                markup=True,
                preferred_font_sp=MOBILE_QUIZ_LAYOUT.prompt_preferred_sp,
                minimum_font_sp=MOBILE_QUIZ_LAYOUT.prompt_minimum_sp,
                maximum_fit_lines=MOBILE_QUIZ_LAYOUT.prompt_maximum_lines,
                allow_shorten=False,
                fixed_height=MOBILE_QUIZ_LAYOUT.prompt_height,
                single_line=True,
                halign="left",
            )
            self.content_layout.add_widget(self.prompt_label)

            if question.options:
                self.render_choices(question)
                return
            self.render_input(question, persistent_input)
            if session.waiting_for_confirmation:
                self.render_review(question)
            else:
                self.configure_actions()
            self.content_layout.add_widget(Widget())
            self.keep_keyboard_visible()

        def render_choices(self, question: Question) -> None:
            if self.content_layout is None:
                return
            scale = self.kotomi.settings.mobile_button_scale
            option_height = scaled_button_height(
                MOBILE_QUIZ_LAYOUT.action_height,
                scale,
            )
            options = GridLayout(
                cols=1,
                spacing=dp(6),
                size_hint_y=None,
                height=dp(
                    option_height * len(question.options)
                    + 6 * max(0, len(question.options) - 1)
                ),
            )
            for option in question.options:
                button = ChoiceButton(
                    text=option,
                    height=dp(MOBILE_QUIZ_LAYOUT.action_height),
                    background_color=CHOICE_BUTTON_BACKGROUND,
                    color=MOBILE_BUTTON_TEXT,
                )
                button.bind(
                    on_release=lambda _button, value=option: self.choose(value)
                )
                self.choice_buttons[option] = button
                options.add_widget(button)
            self.content_layout.add_widget(options)
            self.hint_button = AppButton(
                text=self.tr("mobile.hint_button", ""),
                height=dp(MOBILE_QUIZ_LAYOUT.action_height),
            )
            self.hint_button.bind(on_release=lambda *_: self.toggle_hint())
            self.content_layout.add_widget(self.hint_button)
            self.content_layout.add_widget(Widget())

        def render_input(
            self,
            question: Question,
            persistent_input: Optional[TextInput],
        ) -> None:
            if self.content_layout is None:
                return
            expected_font = (
                JAPANESE_FONT
                if question.answer_field in self.INPUT_ANSWER_FIELDS
                else POLISH_FONT
            )
            if persistent_input is None:
                persistent_input = AppInput(
                    font_name=expected_font,
                    height=dp(MOBILE_QUIZ_LAYOUT.input_height),
                )
                persistent_input.bind(
                    on_text_validate=lambda *_: self.submit_input()
                )
            else:
                persistent_input.font_name = expected_font
            if not self.kotomi.session.waiting_for_confirmation:
                persistent_input.text = ""
            # Keep the same focusable input mounted throughout answer review.
            self.answer_input = persistent_input
            self.set_review_lock(self.kotomi.session.waiting_for_confirmation)
            self.content_layout.add_widget(self.answer_input)

            allows_hint = self.current_mode in {"conjugation", "sentence"}
            if allows_hint:
                self.hint_label = AdaptiveSingleLineLabel(
                    text="",
                    fit_plain_text="",
                    markup=True,
                    font_name=JAPANESE_FONT,
                    color=MUTED_COLOR,
                    preferred_font_sp=MOBILE_QUIZ_LAYOUT.hint_preferred_sp,
                    minimum_font_sp=MOBILE_QUIZ_LAYOUT.hint_minimum_sp,
                    allow_shorten=False,
                    fixed_height=MOBILE_QUIZ_LAYOUT.hint_height,
                    single_line=True,
                    halign="left",
                    valign="middle",
                )
                self.content_layout.add_widget(self.hint_label)

            actions = BoxLayout(
                size_hint_y=None,
                height=dp(scaled_button_height(
                    MOBILE_QUIZ_LAYOUT.action_height,
                    self.kotomi.settings.mobile_button_scale,
                )),
                spacing=dp(6),
            )
            actions._mobile_base_height = dp(MOBILE_QUIZ_LAYOUT.action_height)
            self.primary_button = AppButton(
                height=dp(MOBILE_QUIZ_LAYOUT.action_height)
            )
            self.secondary_button = AppButton(
                height=dp(MOBILE_QUIZ_LAYOUT.action_height)
            )
            self.primary_button.bind(on_release=lambda *_: self.primary_action())
            self.secondary_button.bind(on_release=lambda *_: self.secondary_action())
            actions.add_widget(self.primary_button)
            actions.add_widget(self.secondary_button)
            self.content_layout.add_widget(actions)

        def set_review_lock(self, locked: bool) -> None:
            """Lock typing during review without releasing Android focus."""
            self.review_locked = locked
            if self.answer_input is None:
                return
            self.answer_input.set_review_locked(locked)
            background = INPUT_ACTIVE_BACKGROUND
            if locked:
                background = INPUT_REVIEW_BACKGROUND
                session = self.kotomi.session
                if session is not None and session.pending_correct is True:
                    background = INPUT_REVIEW_CORRECT_BACKGROUND
                elif session is not None and session.pending_correct is False:
                    background = INPUT_REVIEW_WRONG_BACKGROUND
            self.answer_input.background_color = background

        def configure_actions(self) -> None:
            session = self.kotomi.session
            if (
                session is None
                or self.primary_button is None
                or self.secondary_button is None
            ):
                return
            primary = self.primary_button
            secondary = self.secondary_button
            primary.opacity = 1
            primary.disabled = False
            primary.color = MOBILE_BUTTON_TEXT
            secondary.color = MOBILE_BUTTON_TEXT
            if session.waiting_for_confirmation:
                self.set_review_lock(True)
                correct = session.pending_correct is True
                primary.text = self.tr(
                    "quiz.next" if correct else "quiz.accept",
                    "Next" if correct else "Accept answer",
                )
                primary.background_color = MOBILE_CORRECT_BACKGROUND
                if correct:
                    secondary.text = ""
                    secondary.opacity = 0
                    secondary.disabled = True
                    secondary.background_color = MOBILE_BUTTON_BACKGROUND
                else:
                    secondary.text = self.tr("quiz.wrong", "")
                    secondary.opacity = 1
                    secondary.disabled = False
                    secondary.background_color = MOBILE_WRONG_BACKGROUND
                return

            primary.text = self.tr("quiz.check", "")
            primary.background_color = MOBILE_BUTTON_BACKGROUND
            self.set_review_lock(False)
            if self.current_mode in {"conjugation", "sentence"}:
                secondary.text = self.tr("mobile.hint_button", "")
                secondary.opacity = 1
                secondary.disabled = False
                secondary.background_color = (
                    ACCENT_COLOR if self.hint_visible else MOBILE_BUTTON_BACKGROUND
                )
                self.hint_button = secondary
            else:
                # Written quiz deliberately has no Hint control.  The reserved
                # slot keeps the review button geometry from jumping later.
                secondary.text = ""
                secondary.opacity = 0
                secondary.disabled = True
                secondary.background_color = MOBILE_BUTTON_BACKGROUND
                self.hint_button = None

        def update_progress(self, session: QuizSession) -> None:
            if self.progress_bar is not None:
                self.progress_bar.value = session.progress
            if self.progress_label is not None:
                text = self.compact_progress_text(session)
                self.progress_label.set_fitted_text(text, text)

        def toggle_hint(self) -> None:
            session = self.kotomi.session
            if session is None or session.current is None:
                return
            if self.current_mode == "written":
                return
            self.hint_visible = not self.hint_visible
            if self.choice_buttons:
                for option, button in self.choice_buttons.items():
                    hint = safe_option_hint(
                        session.current,
                        option,
                        self.kotomi.sentence_engine.project,
                    )
                    button.set_fitted_text(
                        f"{option}\n{hint}"
                        if self.hint_visible and hint
                        else option
                    )
                if self.hint_button is not None:
                    self.hint_button.background_color = (
                        ACCENT_COLOR if self.hint_visible else MOBILE_BUTTON_BACKGROUND
                    )
                return
            if self.hint_label is not None:
                hint_markup = (
                    self.question_hint_content(session.current)
                    if self.hint_visible
                    else ""
                )
                hint_plain = (
                    self.question_hint_plain_text(session.current)
                    if self.hint_visible
                    else ""
                )
                self.hint_label.set_fitted_text(hint_markup, hint_plain)
            self.configure_actions()
            self.keep_keyboard_visible()

        def sentence_hint_text(self, question: Question) -> str:
            """Describe selected vocabulary, never the sentence answer."""
            items = sentence_lexical_items(
                question,
                self.kotomi.sentence_engine.project,
            )
            if not items:
                return self.tr(
                    "specialized.no_hint",
                    "",
                )
            return "  ·  ".join(items)

        def conjugation_hint_text(self, question: Question) -> str:
            """Show the base word using the standard compact mobile Hint."""
            value = conjugation_lexical_hint(
                question,
                self.kotomi.sentence_engine.project,
            )
            if not value:
                return self.tr(
                    "specialized.no_hint",
                    "",
                )
            return value

        def active_hint_text(self, question: Question) -> str:
            """Return Hint content for the active typed lesson quiz mode."""
            if self.current_mode == "conjugation":
                return self.conjugation_hint_text(question)
            return self.sentence_hint_text(question)

        def question_hint_content(self, question: Question) -> str:
            value = self.active_hint_text(question)
            return (
                f"[color={PROMPT_VALUE_COLOR}]"
                f"{font_markup(value)}[/color]"
            )

        def question_hint_plain_text(self, question: Question) -> str:
            return self.active_hint_text(question)

        def primary_action(self) -> None:
            session = self.kotomi.session
            if session is None:
                return
            if not session.waiting_for_confirmation:
                self.submit_input()
            else:
                self.confirm(True)

        def secondary_action(self) -> None:
            session = self.kotomi.session
            if session is None:
                return
            if session.waiting_for_confirmation and session.pending_correct is False:
                self.confirm(False)
            elif not session.waiting_for_confirmation:
                self.toggle_hint()

        def _button_check(self) -> None:
            self.submit_input()

        def keep_keyboard_visible(self, **_unused) -> None:
            if self.answer_input is None:
                self.focus_request.cancel()
                return

            def restore() -> None:
                if self.answer_input is not None:
                    self.answer_input.focus = True

            def is_active() -> bool:
                return (
                    self.manager is not None
                    and self.manager.current == "quiz"
                    and self.answer_input is not None
                    and self.kotomi.session is not None
                )

            self.focus_request.schedule(
                Clock.schedule_once,
                restore,
                is_active,
            )

        def submit_input(self) -> None:
            session = self.kotomi.session
            if (
                self.answer_input is None
                or session is None
                or self.review_locked
                or session.waiting_for_confirmation
                or session.current is None
            ):
                return
            result = session.submit(self.answer_input.text)
            if result.state != "ignored":
                self.set_review_lock(True)
                self.render_review(session.current)
                self.keep_keyboard_visible()

        def render_review(self, question: Question) -> None:
            session = self.kotomi.session
            if (
                session is None
                or self.result_row is None
                or self.correct_result_label is None
            ):
                return
            expected = question.expected_answer
            if self.current_mode == "written":
                placeholder = self.answer_placeholder_text()
                correct_markup = (
                    f"{escape_markup(placeholder)} "
                    f"[color={CORRECT_VALUE_COLOR}]"
                    f"{font_markup(expected)}[/color]"
                )
                plain_text = f"{placeholder} {expected}"
            else:
                correct_markup = (
                    f"[color={CORRECT_VALUE_COLOR}]"
                    f"{font_markup(expected)}[/color]"
                )
                plain_text = expected
            self.correct_result_label.set_fitted_text(
                correct_markup,
                plain_text,
            )
            self.set_review_lock(True)
            self.configure_actions()

        def confirm(self, mark_correct: bool) -> None:
            session = self.kotomi.session
            if session is None:
                return
            if mark_correct:
                session.accept_current()
            else:
                session.reject_current()
            self.update_progress(session)
            session.next_question()
            self.render()

        def choose(self, value: str) -> None:
            session = self.kotomi.session
            if session is None or self.choice_locked or session.current is None:
                return
            self.choice_locked = True
            question = session.current
            result = session.submit(value)
            session.confirm_default()
            self.update_progress(session)
            correct_option = self.choice_buttons.get(question.expected_answer)
            if correct_option:
                correct_option.background_color = MOBILE_CORRECT_BACKGROUND
                correct_option.color = MOBILE_BUTTON_TEXT
            if result.was_correct is False:
                selected = self.choice_buttons.get(value)
                if selected:
                    selected.background_color = MOBILE_WRONG_BACKGROUND
                    selected.color = MOBILE_BUTTON_TEXT
            feedback_seconds = max(
                1.5,
                self.kotomi.settings.choice_feedback_ms / 1000.0,
            )
            self.choice_event = Clock.schedule_once(
                lambda _dt: self.advance_choice(),
                feedback_seconds,
            )

        def advance_choice(self) -> None:
            session = self.kotomi.session
            self.choice_event = None
            if session is None:
                return
            session.next_question()
            self.render()

        def render_summary(self, session: QuizSession) -> None:
            self.root_layout.add_widget(
                AppLabel(
                    text=self.tr("mobile.quiz_completed", ""),
                    font_size="26sp",
                    color=ACCENT_COLOR,
                )
            )
            self.root_layout.add_widget(
                AppLabel(
                    text=(
                        self.tr(
                            "mobile.result_summary",
                            "",
                            correct=session.correct,
                            wrong=session.wrong,
                        )
                        + "\n"
                        + self.tr(
                            "mobile.accepted_count",
                            "",
                            count=session.accepted,
                        )
                    ),
                    font_size="21sp",
                )
            )
            self.root_layout.add_widget(Widget())
            close = AppButton(
                text=self.tr("mobile.back_to_lesson", "")
            )
            close.bind(on_release=lambda *_: self.close_quiz())
            self.root_layout.add_widget(close)

        def close_quiz(self) -> None:
            self.focus_request.cancel()
            self.cancel_choice_event()
            if self.answer_input is not None:
                self.answer_input.focus = False
            self.kotomi.session = None
            self.manager.current = "lesson"

    class LessonEditorScreen(BaseScreen):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.working_catalog: Optional[LessonCatalog] = None
            self.working_lesson: Optional[Lesson] = None
            self.selected_word_id = ""
            root = vertical_root(padding=8, spacing=5)
            self.title = AppLabel(font_size="21sp", color=ACCENT_COLOR)
            root.add_widget(self.title)
            self.group = AppInput(hint_text=ui_text("lesson.group", ""))
            self.main_name = AppInput(
                hint_text=ui_text("lesson.category", "")
            )
            self.sub_name = AppInput(
                hint_text=ui_text("lesson.name", "")
            )
            root.add_widget(self.group)
            root.add_widget(self.main_name)
            root.add_widget(self.sub_name)
            add_grid = GridLayout(cols=2, spacing=dp(5), size_hint_y=None, height=dp(102))
            self.translation = AppInput(
                hint_text=ui_text("field.translation", "")
            )
            self.kana = AppInput(
                hint_text=ui_text("field.kana", ""),
                font_name=JAPANESE_FONT,
            )
            self.kanji = AppInput(
                hint_text=ui_text("field.kanji", ""),
                font_name=JAPANESE_FONT,
            )
            self.romaji = AppInput(
                hint_text=ui_text("field.romaji", "")
            )
            for widget in (self.translation, self.kana, self.kanji, self.romaji):
                add_grid.add_widget(widget)
            root.add_widget(add_grid)
            add_word = AppButton(text=ui_text("action.add", ""))
            add_word.bind(on_release=lambda *_: self.add_word())
            remove_word = AppButton(
                text=ui_text("lesson.remove_selected_word", "")
            )
            remove_word.bind(on_release=lambda *_: self.remove_selected())
            root.add_widget(button_row([add_word, remove_word]))
            self.scroll, self.word_stack = scroll_stack(2)
            root.add_widget(self.scroll)
            save = AppButton(text=ui_text("action.save", ""))
            save.bind(on_release=lambda *_: self.save())
            cancel = AppButton(text=ui_text("action.cancel", ""))
            cancel.bind(on_release=lambda *_: setattr(self.manager, "current", "lesson" if self.kotomi.editing_lesson_id else "lessons"))
            root.add_widget(button_row([cancel, save]))
            self.add_widget(root)

        def on_pre_enter(self, *_args):
            self.working_catalog = copy.deepcopy(self.kotomi.catalog)
            editing_id = self.kotomi.editing_lesson_id
            if editing_id:
                self.working_lesson = self.working_catalog.lesson(editing_id)
                self.title.text = ui_text("lesson.edit_title", "")
            else:
                self.working_lesson = Lesson(
                    id="lesson_" + uuid4().hex[:10],
                    group_name="",
                    main_name="",
                    sub_name="",
                )
                self.title.text = ui_text("lesson.new_title", "")
            self.group.text = self.working_lesson.group_name
            self.main_name.text = self.working_lesson.main_name
            self.sub_name.text = self.working_lesson.sub_name
            self.selected_word_id = ""
            self.refresh_words()

        def refresh_words(self) -> None:
            self.word_stack.clear_widgets()
            if self.working_catalog is None or self.working_lesson is None:
                return
            for word_id in self.working_lesson.word_refs:
                word = self.working_catalog.words.get(word_id)
                if word is None:
                    continue
                values = [
                    value
                    for value in (word.translation, word.kana, word.kanji, word.romaji)
                    if is_available(value)
                ]
                button = ToggleButton(
                    text=mixed_markup(values),
                    markup=True,
                    group="lesson_word",
                    font_name=POLISH_FONT,
                    size_hint_y=None,
                    height=dp(44),
                    background_normal="",
                    background_color=BUTTON_COLOR,
                    color=TEXT_COLOR,
                )
                button.bind(
                    on_release=lambda selected, value=word_id: self._select_word(
                        value if selected.state == "down" else ""
                    )
                )
                self.word_stack.add_widget(button)

        def _select_word(self, word_id: str) -> None:
            self.selected_word_id = word_id

        def add_word(self) -> None:
            if self.working_catalog is None or self.working_lesson is None:
                return
            candidate = LessonWord(
                id="word_" + uuid4().hex[:10],
                translation=self.translation.text.strip(),
                kana=self.kana.text.strip(),
                kanji=self.kanji.text.strip(),
                romaji=self.romaji.text.strip(),
            )
            if not any(
                is_available(value)
                for value in (
                    candidate.translation,
                    candidate.kana,
                    candidate.kanji,
                    candidate.romaji,
                )
            ):
                self.show_error(ui_text(
                    "mobile.word_value_required",
                    "",
                ))
                return
            stored = self.working_catalog.add_or_reuse_word(candidate)
            if stored.id not in self.working_lesson.word_refs:
                self.working_lesson.word_refs.append(stored.id)
            for widget in (self.translation, self.kana, self.kanji, self.romaji):
                widget.text = ""
            self.refresh_words()

        def remove_selected(self) -> None:
            if self.working_lesson is None or not self.selected_word_id:
                return
            self.working_lesson.word_refs = [
                word_id
                for word_id in self.working_lesson.word_refs
                if word_id != self.selected_word_id
            ]
            self.selected_word_id = ""
            self.refresh_words()

        def save(self) -> None:
            if self.working_catalog is None or self.working_lesson is None:
                return
            self.working_lesson.group_name = self.group.text.strip()
            self.working_lesson.main_name = self.main_name.text.strip()
            self.working_lesson.sub_name = self.sub_name.text.strip()
            if not all(
                (
                    self.working_lesson.group_name,
                    self.working_lesson.main_name,
                    self.working_lesson.sub_name,
                )
            ):
                self.show_error(ui_text(
                    "lesson.need_names",
                    "",
                ))
                return
            if not self.working_lesson.word_refs:
                self.show_error(
                    ui_text("lesson.need_word", "")
                )
                return
            if not self.kotomi.editing_lesson_id:
                self.working_catalog.add_lesson(self.working_lesson)
            self.working_catalog.remove_unreferenced_words()
            self.kotomi.catalog = self.working_catalog
            self.kotomi.save_catalog()
            self.kotomi.selected_lesson_id = self.working_lesson.id
            self.manager.current = "lesson"

    class KotomiApp(App):
        selected_lesson_id = StringProperty("")
        icon = app_icon_png_path()

        def build(self):
            apply_kivy_window_icon(Window)
            self.title = ui_text('hub.app.lessons.title', "")
            self.basic_mode = "written"
            self.editing_lesson_id: Optional[str] = None
            self.session: Optional[QuizSession] = None
            self.quiz_title = ""

            self.catalog_store = CatalogStore(QUIZ_DATA_DIR)
            self.settings_store = SettingsStore(
                settings_path(INSTALL_ROOT, "lesson_quiz_settings.xml")
            )
            self.catalog = self.catalog_store.load()
            synchronize_catalog(self.catalog, QUIZ_PROJECT)
            self.settings = AppSettings.from_dict(self.settings_store.load())
            self.sentence_engine = LessonSentenceQuiz(QUIZ_PROJECT)

            self.manager = ScreenManager()
            self.manager.add_widget(LessonsScreen(name="lessons"))
            self.manager.add_widget(SettingsScreen(name="settings"))
            self.manager.add_widget(LessonDetailScreen(name="lesson"))
            self.manager.add_widget(BasicSetupScreen(name="basic_setup"))
            self.manager.add_widget(FormsSetupScreen(name="forms_setup"))
            self.manager.add_widget(SentenceSetupScreen(name="sentence_setup"))
            self.manager.add_widget(
                SentenceStatisticsScreen(name="sentence_statistics")
            )
            self.manager.add_widget(QuizScreen(name="quiz"))
            if not getattr(self, "embedded_mode", False):
                Window.bind(on_keyboard=self._on_keyboard)
            return self.manager

        def _on_keyboard(self, _window, key, *_args):
            if key in (282, 290) and self.manager.current == "quiz":
                self.manager.get_screen("quiz").toggle_hint()
                return True
            return False

        def current_lesson(self) -> Lesson:
            return self.catalog.lesson(self.selected_lesson_id)

        def open_lesson(self, lesson_id: str) -> None:
            self.selected_lesson_id = lesson_id
            self.manager.current = "lesson"

        def open_editor(self, lesson_id: Optional[str]) -> None:
            self.editing_lesson_id = lesson_id
            self.manager.current = "editor"

        def start_quiz(self, questions, title: str) -> None:
            if not questions:
                self.show_message(
                    ui_text("mobile.no_questions_title", ""),
                    ui_text(
                        "mobile.no_questions_body",
                        "",
                    ),
                    bad=True,
                )
                return
            quiz = self.manager.get_screen("quiz")
            quiz.focus_request.cancel()
            quiz.cancel_choice_event()
            self.session = QuizSession(
                questions,
                required_correct_answers=self.settings.required_correct_answers,
            )
            self.quiz_title = title
            self.manager.current = "quiz"

        def go_home(self) -> None:
            if self.manager.current == "lessons":
                return_to_quiz_menu()
            else:
                self.manager.current = "lessons"

        def prepare_for_unload(self) -> None:
            if not hasattr(self, "manager"):
                return
            quiz = self.manager.get_screen("quiz")
            quiz.focus_request.cancel()
            quiz.cancel_choice_event()
            if quiz.answer_input is not None:
                quiz.answer_input.focus = False

        def apply_button_scale(self, scale: float) -> None:
            def resize(widget) -> None:
                base_height = getattr(widget, "_mobile_base_height", None)
                if base_height is not None:
                    widget.height = scaled_button_height(base_height, scale)
                for child in getattr(widget, "children", ()):
                    resize(child)

            if hasattr(self, "manager"):
                resize(self.manager)

        def on_stop(self):
            if not getattr(self, "embedded_mode", False):
                Window.unbind(on_keyboard=self._on_keyboard)

        def save_catalog(self) -> None:
            self.catalog_store.save(self.catalog)

        def show_message(self, title: str, message: str, bad: bool = False) -> None:
            content = vertical_root()
            content.add_widget(
                AppLabel(text=message, color=BAD_COLOR if bad else TEXT_COLOR)
            )
            close = AppButton(text=ui_text("action.ok"))
            popup = Popup(
                title=title,
                content=content,
                size_hint=(0.92, None),
                height=dp(260),
            )
            close.bind(on_release=lambda *_: popup.dismiss())
            content.add_widget(close)
            popup.open()

    return KotomiApp


def create_embedded_controller():
    """Create the lessons controller for the shared mobile quiz hub."""
    app_class = create_app_class()
    controller = app_class()
    controller.embedded_mode = True
    return controller


def main() -> int:
    try:
        app_class = create_app_class()
    except ImportError as exception:
        print(
            "Kivy nie jest zainstalowane. Zainstaluj je poleceniem "
            "'pip install kivy' lub uruchom aplikację w Pydroid 3."
        )
        print(exception)
        return 1
    app_class().run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
