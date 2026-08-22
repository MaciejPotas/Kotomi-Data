"""Publish the split Lessons package and refresh its manifest entries."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import py_compile
import subprocess


ROOT = Path(__file__).resolve().parents[1]
LESSONS_DIR = ROOT / "quizzes" / "lessons"
ORIGINAL_COMMIT = "b1f2b072c09f422b7078bd1d3ffe26520dac1c88"
ORIGINAL_PATH = "quizzes/lessons/Kotomi_lessons.py"


def canonical_bytes(path: Path) -> bytes:
    return path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def digest(path: Path) -> str:
    return hashlib.sha256(canonical_bytes(path)).hexdigest()


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def original_source() -> str:
    return subprocess.check_output(
        ["git", "show", f"{ORIGINAL_COMMIT}:{ORIGINAL_PATH}"],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
    )


def build_modules(source: str) -> tuple[str, str, str]:
    marker = "\ndef create_app_class():\n"
    head, tail = source.split(marker, 1)
    helpers = head[head.index("def fitted_choice_text_layout(") :].strip() + "\n"

    logic = '''"""Platform-neutral Lesson quiz facade and hint policies.

The reusable written, choice, conjugation, sentence, catalog, settings, and
session implementations live in :mod:`kotomi_core`. This module exposes those
shared capabilities together with the small presentation-neutral adapters used
by the Lesson package. It intentionally imports neither Kivy nor Tkinter.
"""

from __future__ import annotations

from pathlib import Path
import sys
from typing import List


APP_ROOT = Path(__file__).resolve().parent
INSTALL_ROOT = APP_ROOT.parents[1]
for search_path in (INSTALL_ROOT, APP_ROOT):
    if str(search_path) not in sys.path:
        sys.path.insert(0, str(search_path))

from kotomi_core.basic_quiz import (
    build_choice_questions,
    build_written_questions,
    eligible_count,
)
from kotomi_core.conjugation_quiz import (
    available_forms,
    build_conjugation_questions,
    conjugation_base_hint,
)
from kotomi_core.grammar_bridge import synchronize_catalog
from kotomi_core.lessons import (
    FIELD_LABELS,
    FORM_LABELS,
    FORM_ORDER,
    Lesson,
    LessonCatalog,
    LessonWord,
    is_available,
)
from kotomi_core.questions import Question, QuizSession
from kotomi_core.sentence_quiz import LessonSentenceQuiz
from kotomi_core.settings import AppSettings
from kotomi_core.storage import CatalogStore, SettingsStore
from shared.mobile_ui import (
    fitted_compact_text_layout,
    fitted_single_line_font_size,
    format_grammatical_hint_entry,
    format_mobile_hint_entries,
)


SHARED_DIR = INSTALL_ROOT / "shared"
QUIZ_DATA_DIR = SHARED_DIR / "quiz_data"
QUIZ_PROJECT = QUIZ_DATA_DIR / "quiz_project.xml"

'''
    logic += helpers
    logic += '''\n\n__all__ = [
    "APP_ROOT",
    "INSTALL_ROOT",
    "SHARED_DIR",
    "QUIZ_DATA_DIR",
    "QUIZ_PROJECT",
    "FIELD_LABELS",
    "FORM_LABELS",
    "FORM_ORDER",
    "Lesson",
    "LessonCatalog",
    "LessonWord",
    "Question",
    "QuizSession",
    "LessonSentenceQuiz",
    "AppSettings",
    "CatalogStore",
    "SettingsStore",
    "available_forms",
    "build_choice_questions",
    "build_conjugation_questions",
    "build_written_questions",
    "conjugation_base_hint",
    "eligible_count",
    "is_available",
    "synchronize_catalog",
    "fitted_choice_text_layout",
    "sentence_lexical_items",
    "conjugation_lexical_hint",
    "lexical_hint_items",
    "safe_option_hint",
    "conjugation_translation_hint",
]
'''

    mobile = '''"""Kivy presentation for the Lessons package.

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
from shared.settings_xml import settings_path
from shared.app_identity import (
    app_icon_png_path,
    apply_kivy_window_icon,
    configure_windows_app_id,
)
from shared.mobile_ui import (
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
from shared.mobile_i18n import mobile_error_text, mobile_text


MOBILE_FONT = mobile_font_path(SHARED_DIR)
POLISH_FONT = MOBILE_FONT
JAPANESE_FONT = MOBILE_FONT

'''
    mobile += "def create_app_class():\n" + tail

    wrapper = '''"""Compatibility entrypoint for the Lessons quiz package.

Platform-neutral Lesson behavior lives in :mod:`logic`, while the Kivy
presentation lives in :mod:`mobile`. This module preserves the public API and
entrypoint used by Desktop, Mobile, Pydroid, and quiz updates.
"""

from __future__ import annotations

from pathlib import Path
import sys


SCRIPT_DIR = Path(__file__).resolve().parent
INSTALL_ROOT = SCRIPT_DIR.parents[1]
if str(INSTALL_ROOT) not in sys.path:
    sys.path.insert(0, str(INSTALL_ROOT))

from apps.lessons import logic as _logic
from apps.lessons import mobile as _mobile
from apps.lessons.logic import *
from apps.lessons.mobile import (
    create_app_class,
    create_embedded_controller,
    main,
)


def __getattr__(name: str):
    if hasattr(_logic, name):
        return getattr(_logic, name)
    if hasattr(_mobile, name):
        return getattr(_mobile, name)
    raise AttributeError(name)


if __name__ == "__main__":
    raise SystemExit(main())
'''
    return wrapper, logic, mobile


def refresh_manifest() -> None:
    manifest_path = ROOT / "quiz_update_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    package = next(item for item in manifest["packages"] if item["id"] == "lessons")
    names = ("Kotomi_lessons.py", "app.json", "logic.py", "mobile.py")
    package["files"] = sorted(f"apps/lessons/{name}" for name in names)
    manifest["files"] = [
        item
        for item in manifest["files"]
        if not str(item["path"]).startswith("apps/lessons/")
    ]
    for name in names:
        path = LESSONS_DIR / name
        value = digest(path)
        manifest["files"].append(
            {
                "path": f"apps/lessons/{name}",
                "sha256": value,
                "url": f"quizzes/lessons/{name}?kotomi_sha256={value}",
            }
        )
    manifest["files"].sort(key=lambda item: item["path"])
    write_text(
        manifest_path,
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
    )


def main() -> int:
    wrapper, logic, mobile = build_modules(original_source())
    write_text(LESSONS_DIR / "Kotomi_lessons.py", wrapper)
    write_text(LESSONS_DIR / "logic.py", logic)
    write_text(LESSONS_DIR / "mobile.py", mobile)
    refresh_manifest()
    for name in ("Kotomi_lessons.py", "logic.py", "mobile.py"):
        py_compile.compile(str(LESSONS_DIR / name), doraise=True)
    subprocess.run(
        [
            "git",
            "add",
            "quiz_update_manifest.json",
            "quizzes/lessons/Kotomi_lessons.py",
            "quizzes/lessons/logic.py",
            "quizzes/lessons/mobile.py",
        ],
        cwd=ROOT,
        check=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
