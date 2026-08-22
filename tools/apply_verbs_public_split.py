"""Split the public Verbs package into compatibility, logic, and mobile modules."""

from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path
import py_compile
import subprocess


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "quizzes" / "verbs"
SOURCE = PACKAGE / "Kotomi_verbs.py"
LOGIC = PACKAGE / "logic.py"
MOBILE = PACKAGE / "mobile.py"
MANIFEST = ROOT / "quiz_update_manifest.json"


def _offsets(text: str) -> list[int]:
    result = [0]
    for line in text.splitlines(keepends=True):
        result.append(result[-1] + len(line))
    return result


def _split_source(source: str) -> tuple[str, str, str]:
    tree = ast.parse(source)
    offsets = _offsets(source)
    functions = {
        node.name: node
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }
    create_node = functions.get("create_app_class")
    hint_node = functions.get("mobile_sentence_hint_items")
    if create_node is None or hint_node is None:
        raise RuntimeError("Verbs split markers were not found.")

    create_start = offsets[create_node.lineno - 1]
    guard = '\nif __name__ == "__main__":\n'
    guard_start = source.rfind(guard)
    if guard_start < create_start:
        raise RuntimeError("Verbs standalone guard was not found.")

    prefix = source[:create_start]
    prefix_offsets = _offsets(prefix)
    hint_start = prefix_offsets[hint_node.lineno - 1]
    hint_end = prefix_offsets[hint_node.end_lineno]
    hint_source = prefix[hint_start:hint_end].rstrip() + "\n"
    logic_source = prefix[:hint_start] + prefix[hint_end:]

    old_doc = '''"""Mobile Kivy verb quiz backed by Kotomi schema 10 XML files.\n\nThe module keeps Kivy imports inside ``create_app_class``. This lets the XML\nengine and settings logic be tested on a computer where Kivy is not installed.\nOn a phone, run this file directly with Kivy available.\nThis is the update test.\n"""'''
    new_doc = '''"""Platform-neutral settings and generation logic for the Verbs quiz.\n\nThis module intentionally imports no Kivy or Tkinter classes. Desktop and\nMobile presentations use the same settings, engine, session, question, and\nresult models from here.\n"""'''
    if old_doc not in logic_source:
        raise RuntimeError("Unexpected Verbs module docstring.")
    logic_source = logic_source.replace(old_doc, new_doc, 1)
    logic_source = logic_source.replace("import re\n", "", 1)
    logic_source = logic_source.replace("import threading\n", "", 1)
    logic_source = logic_source.replace(
        "SHARED_DIR = REPOSITORY_SHARED_DIR\n", "", 1
    )
    logic_source = logic_source.replace(
        "from settings_xml import load_settings, save_settings, settings_path\n",
        "from settings_xml import load_settings, save_settings\n",
        1,
    )
    old_mobile_ui = '''from mobile_ui import (\n    FocusRequest,\n    MOBILE_BUTTON_BACKGROUND,\n    MOBILE_BUTTON_TEXT,\n    MOBILE_CORRECT_BACKGROUND,\n    MOBILE_QUIZ_LAYOUT,\n    MOBILE_WRONG_BACKGROUND,\n    MobileReviewInputMixin,\n    fitted_compact_text_layout,\n    format_grammatical_hint_entry,\n    format_mobile_hint_entries,\n    format_mobile_hint_entry,\n    mobile_font_path,\n    scaled_button_height,\n    validate_mobile_button_scale,\n)\n'''
    if old_mobile_ui not in logic_source:
        raise RuntimeError("Unexpected Verbs mobile UI import block.")
    logic_source = logic_source.replace(
        old_mobile_ui,
        "from mobile_ui import validate_mobile_button_scale\n",
        1,
    )
    old_mobile_only = '''from shared.app_identity import (\n    app_icon_png_path,\n    apply_kivy_window_icon,\n    configure_windows_app_id,\n)\n\ntry:\n    from shared.mobile_i18n import mobile_error_text, mobile_text\nexcept ImportError:  # Direct execution adds ``shared`` itself to sys.path.\n    from mobile_i18n import mobile_error_text, mobile_text\nfrom quiz_updater import (\n    QuizUpdater,\n    UpdateError,\n    load_update_url,\n)\n\n'''
    if old_mobile_only not in logic_source:
        raise RuntimeError("Unexpected Verbs mobile-only import block.")
    logic_source = logic_source.replace(old_mobile_only, "", 1)
    logic_source = logic_source.replace(
        "MOBILE_FONT = mobile_font_path(SHARED_DIR)\n", "", 1
    ).rstrip() + "\n"

    mobile_preamble = '''"""Kivy presentation for the Verbs quiz.\n\nAll settings, filtering, generation, statistics, and session behavior comes\nfrom :mod:`logic`. This module owns mobile rendering, interaction, hints, and\nupdate controls.\n"""\n\nfrom __future__ import annotations\n\nfrom pathlib import Path\nimport re\nimport sys\nimport threading\nfrom typing import Dict, List, Optional, Set\n\n\nSCRIPT_DIR = Path(__file__).resolve().parent\nINSTALL_ROOT = SCRIPT_DIR.parents[1]\nREPOSITORY_SHARED_DIR = INSTALL_ROOT / "shared"\nfor import_root in (INSTALL_ROOT, REPOSITORY_SHARED_DIR):\n    if str(import_root) not in sys.path:\n        sys.path.insert(0, str(import_root))\n\nfrom apps.verbs.logic import *\nfrom apps.verbs.logic import _safe_float, _safe_int\nfrom quiz_core import ProjectError\nfrom settings_xml import settings_path\nfrom mobile_ui import (\n    FocusRequest,\n    MOBILE_BUTTON_BACKGROUND,\n    MOBILE_BUTTON_TEXT,\n    MOBILE_CORRECT_BACKGROUND,\n    MOBILE_QUIZ_LAYOUT,\n    MOBILE_WRONG_BACKGROUND,\n    MobileReviewInputMixin,\n    fitted_compact_text_layout,\n    format_grammatical_hint_entry,\n    format_mobile_hint_entries,\n    format_mobile_hint_entry,\n    mobile_font_path,\n    scaled_button_height,\n    validate_mobile_button_scale,\n)\nfrom shared.app_identity import (\n    app_icon_png_path,\n    apply_kivy_window_icon,\n    configure_windows_app_id,\n)\ntry:\n    from shared.mobile_i18n import mobile_error_text, mobile_text\nexcept ImportError:  # Direct execution adds ``shared`` itself to sys.path.\n    from mobile_i18n import mobile_error_text, mobile_text\nfrom quiz_updater import QuizUpdater, UpdateError, load_update_url\n\n\nSHARED_DIR = REPOSITORY_SHARED_DIR\nMOBILE_FONT = mobile_font_path(SHARED_DIR)\n\n\n'''
    mobile_source = (
        mobile_preamble
        + hint_source
        + "\n"
        + source[create_start:guard_start].rstrip()
        + "\n"
    )
    wrapper_source = '''"""Compatibility entrypoint for the Verbs quiz package.\n\nThe platform-neutral implementation lives in :mod:`logic`, while the Kivy\npresentation lives in :mod:`mobile`. This module preserves the public API and\nentrypoint used by existing Desktop, Mobile, Pydroid, and updater installs.\n"""\n\nfrom __future__ import annotations\n\nfrom pathlib import Path\nimport sys\n\n\nSCRIPT_DIR = Path(__file__).resolve().parent\nINSTALL_ROOT = SCRIPT_DIR.parents[1]\nif str(INSTALL_ROOT) not in sys.path:\n    sys.path.insert(0, str(INSTALL_ROOT))\n\nfrom apps.verbs import logic as _logic\nfrom apps.verbs import mobile as _mobile\nfrom apps.verbs.logic import *\nfrom apps.verbs.mobile import (\n    create_app_class,\n    create_embedded_controller,\n    main,\n    mobile_sentence_hint_items,\n)\n\n\ndef __getattr__(name: str):\n    if hasattr(_logic, name):\n        return getattr(_logic, name)\n    if hasattr(_mobile, name):\n        return getattr(_mobile, name)\n    raise AttributeError(name)\n\n\nif __name__ == "__main__":\n    raise SystemExit(main())\n'''
    return logic_source, mobile_source, wrapper_source


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _refresh_manifest() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    package = next(
        item for item in manifest["packages"] if item["id"] == "verbs"
    )
    names = ["Kotomi_verbs.py", "app.json", "logic.py", "mobile.py"]
    package["files"] = [f"apps/verbs/{name}" for name in names]
    files = [
        item
        for item in manifest["files"]
        if not item["path"].startswith("apps/verbs/")
    ]
    for name in names:
        path = PACKAGE / name
        digest = _sha256(path)
        files.append(
            {
                "path": f"apps/verbs/{name}",
                "sha256": digest,
                "url": (
                    f"quizzes/verbs/{name}?kotomi_sha256={digest}"
                ),
            }
        )
    manifest["files"] = sorted(files, key=lambda item: item["path"])
    MANIFEST.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def main() -> int:
    source = SOURCE.read_text(encoding="utf-8")
    if "Compatibility entrypoint for the Verbs quiz package" in source:
        raise RuntimeError("Public Verbs package is already split.")
    logic_source, mobile_source, wrapper_source = _split_source(source)
    LOGIC.write_text(logic_source, encoding="utf-8", newline="\n")
    MOBILE.write_text(mobile_source, encoding="utf-8", newline="\n")
    SOURCE.write_text(wrapper_source, encoding="utf-8", newline="\n")
    _refresh_manifest()
    for path in (SOURCE, LOGIC, MOBILE):
        py_compile.compile(str(path), doraise=True)
    json.loads(MANIFEST.read_text(encoding="utf-8"))
    subprocess.run(
        [
            "git",
            "add",
            "--",
            "quizzes/verbs/Kotomi_verbs.py",
            "quizzes/verbs/logic.py",
            "quizzes/verbs/mobile.py",
            "quiz_update_manifest.json",
        ],
        cwd=ROOT,
        check=True,
    )
    print("Published split Verbs package.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
