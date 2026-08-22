"""Publish the split Adjectives package and refresh its manifest entries."""

from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path
import py_compile
import subprocess


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_DIR = ROOT / "quizzes" / "adjectives"
SOURCE_PATH = PACKAGE_DIR / "Kotomi_adjectives.py"
LOGIC_PATH = PACKAGE_DIR / "logic.py"
MOBILE_PATH = PACKAGE_DIR / "mobile.py"
MANIFEST_PATH = ROOT / "quiz_update_manifest.json"


def _line_offsets(text: str) -> list[int]:
    offsets = [0]
    for line in text.splitlines(keepends=True):
        offsets.append(offsets[-1] + len(line))
    return offsets


def _slice_node(text: str, node: ast.AST, offsets: list[int]) -> str:
    start = offsets[node.lineno - 1] + node.col_offset
    end = offsets[node.end_lineno - 1] + node.end_col_offset
    return text[start:end]


def _remove_node(text: str, node: ast.AST, offsets: list[int]) -> str:
    start = offsets[node.lineno - 1]
    end = offsets[node.end_lineno]
    return text[:start] + text[end:]


def _replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"Expected one {label} block, found {count}.")
    return text.replace(old, new, 1)


def _build_sources(source: str) -> tuple[str, str, str]:
    module = ast.parse(source)
    offsets = _line_offsets(source)
    functions = {
        node.name: node
        for node in module.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }
    create_node = functions.get("create_app_class")
    hint_node = functions.get("mobile_sentence_hint_items")
    if create_node is None or hint_node is None:
        raise RuntimeError("Adjectives split markers were not found.")

    create_start = offsets[create_node.lineno - 1]
    guard = '\nif __name__ == "__main__":\n'
    guard_start = source.rfind(guard)
    if guard_start < create_start:
        raise RuntimeError("Adjectives standalone guard was not found.")

    prefix = source[:create_start]
    hint_source = _slice_node(source, hint_node, offsets).rstrip() + "\n"
    prefix_offsets = _line_offsets(prefix)
    prefix_tree = ast.parse(prefix)
    prefix_hint = next(
        node
        for node in prefix_tree.body
        if isinstance(node, ast.FunctionDef)
        and node.name == "mobile_sentence_hint_items"
    )
    logic_source = _remove_node(prefix, prefix_hint, prefix_offsets)

    original_doc = (
        '"""Mobile Kivy adjective sentence quiz backed by Kotomi schema 10 XML.\n\n'
        'The generation policy mirrors ``AdjectiveSentenceQuizWidget``. Kivy is\n'
        'imported lazily so the engine, settings, and updater can be tested without a\n'
        'desktop Kivy installation.\n'
        '"""'
    )
    logic_doc = (
        '"""Platform-neutral settings and generation logic for Adjectives.\n\n'
        'This module imports no Kivy or Tkinter classes. Desktop and Mobile use the\n'
        'same settings, engine, session, question and answer models from here.\n'
        '"""'
    )
    logic_source = _replace_once(
        logic_source, original_doc, logic_doc, "module docstring"
    )
    logic_source = logic_source.replace("import threading\n", "", 1)
    logic_source = _replace_once(
        logic_source,
        "from settings_xml import load_settings, save_settings, settings_path\n",
        "from settings_xml import load_settings, save_settings\n",
        "settings import",
    )
    logic_source = _replace_once(
        logic_source,
        "from mobile_ui import (\n"
        "    DEFAULT_MOBILE_BUTTON_SCALE,\n"
        "    FocusRequest,\n"
        "    MOBILE_BUTTON_BACKGROUND,\n"
        "    MOBILE_BUTTON_TEXT,\n"
        "    MOBILE_CORRECT_BACKGROUND,\n"
        "    MOBILE_QUIZ_LAYOUT,\n"
        "    MOBILE_WRONG_BACKGROUND,\n"
        "    MobileReviewInputMixin,\n"
        "    fitted_compact_text_layout,\n"
        "    format_grammatical_hint_entry,\n"
        "    format_mobile_hint_entries,\n"
        "    format_mobile_hint_entry,\n"
        "    mobile_font_path,\n"
        "    scaled_button_height,\n"
        "    validate_mobile_button_scale,\n"
        ")\n",
        "from mobile_ui import (\n"
        "    DEFAULT_MOBILE_BUTTON_SCALE,\n"
        "    validate_mobile_button_scale,\n"
        ")\n",
        "mobile UI import",
    )
    logic_source = _replace_once(
        logic_source,
        "from shared.app_identity import (\n"
        "    app_icon_png_path,\n"
        "    apply_kivy_window_icon,\n"
        "    configure_windows_app_id,\n"
        ")\n\n"
        "try:\n"
        "    from shared.mobile_i18n import mobile_error_text, mobile_text\n"
        "except ImportError:  # Direct execution adds ``shared`` itself to sys.path.\n"
        "    from mobile_i18n import mobile_error_text, mobile_text\n"
        "from quiz_updater import (\n"
        "    QuizUpdater,\n"
        "    UpdateError,\n"
        "    load_update_url,\n"
        ")\n\n\n",
        "",
        "mobile-only imports",
    )
    logic_source = _replace_once(
        logic_source,
        "SHARED_DIR = REPOSITORY_SHARED_DIR\n"
        "MOBILE_FONT = mobile_font_path(SHARED_DIR)\n",
        "",
        "mobile resource constants",
    )
    logic_source = logic_source.rstrip() + "\n"

    mobile_preamble = '''"""Kivy presentation for the Adjectives quiz.\n\nAll settings, generation, filtering, statistics and answer behavior comes from\n:mod:`logic`. This module owns mobile rendering, interaction, hints and updater UI.\n"""\n\nfrom __future__ import annotations\n\nfrom pathlib import Path\nimport re\nimport sys\nimport threading\nfrom typing import Dict, Iterable, List, Mapping, Optional, Sequence\n\n\nSCRIPT_DIR = Path(__file__).resolve().parent\nINSTALL_ROOT = SCRIPT_DIR.parents[1]\nREPOSITORY_SHARED_DIR = INSTALL_ROOT / "shared"\nfor import_root in (INSTALL_ROOT, REPOSITORY_SHARED_DIR):\n    if str(import_root) not in sys.path:\n        sys.path.insert(0, str(import_root))\n\nfrom apps.adjectives.logic import *\nfrom apps.adjectives.logic import _safe_float, _safe_int\nfrom quiz_core import ProjectError\nfrom settings_xml import settings_path\nfrom mobile_ui import (\n    DEFAULT_MOBILE_BUTTON_SCALE,\n    FocusRequest,\n    MOBILE_BUTTON_BACKGROUND,\n    MOBILE_BUTTON_TEXT,\n    MOBILE_CORRECT_BACKGROUND,\n    MOBILE_QUIZ_LAYOUT,\n    MOBILE_WRONG_BACKGROUND,\n    MobileReviewInputMixin,\n    fitted_compact_text_layout,\n    format_grammatical_hint_entry,\n    format_mobile_hint_entries,\n    format_mobile_hint_entry,\n    mobile_font_path,\n    scaled_button_height,\n    validate_mobile_button_scale,\n)\nfrom shared.app_identity import (\n    app_icon_png_path,\n    apply_kivy_window_icon,\n    configure_windows_app_id,\n)\ntry:\n    from shared.mobile_i18n import mobile_error_text, mobile_text\nexcept ImportError:\n    from mobile_i18n import mobile_error_text, mobile_text\nfrom quiz_updater import QuizUpdater, UpdateError, load_update_url\n\n\nSHARED_DIR = REPOSITORY_SHARED_DIR\nMOBILE_FONT = mobile_font_path(SHARED_DIR)\n\n\n'''
    mobile_body = source[create_start:guard_start].rstrip() + "\n"
    mobile_source = mobile_preamble + hint_source + "\n" + mobile_body

    wrapper_source = '''"""Compatibility entrypoint for the Adjectives quiz package.\n\nThe platform-neutral implementation lives in :mod:`logic`, while the Kivy\npresentation lives in :mod:`mobile`. This module preserves the public API used\nby Desktop, Mobile, Pydroid and existing updater installations.\n"""\n\nfrom __future__ import annotations\n\nfrom pathlib import Path\nimport sys\n\n\nSCRIPT_DIR = Path(__file__).resolve().parent\nINSTALL_ROOT = SCRIPT_DIR.parents[1]\nif str(INSTALL_ROOT) not in sys.path:\n    sys.path.insert(0, str(INSTALL_ROOT))\n\nfrom apps.adjectives.logic import *\nfrom apps.adjectives.mobile import (\n    create_app_class,\n    create_embedded_controller,\n    main,\n    mobile_sentence_hint_items,\n)\n\n\nif __name__ == "__main__":\n    raise SystemExit(main())\n'''
    return logic_source, mobile_source, wrapper_source


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _refresh_manifest() -> None:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    package = next(
        item for item in manifest["packages"] if item["id"] == "adjectives"
    )
    names = ["Kotomi_adjectives.py", "app.json", "logic.py", "mobile.py"]
    package["files"] = [f"apps/adjectives/{name}" for name in names]

    files = [
        item
        for item in manifest["files"]
        if not item["path"].startswith("apps/adjectives/")
    ]
    for name in names:
        public_path = PACKAGE_DIR / name
        digest = _sha256(public_path)
        files.append(
            {
                "path": f"apps/adjectives/{name}",
                "sha256": digest,
                "url": (
                    f"quizzes/adjectives/{name}"
                    f"?kotomi_sha256={digest}"
                ),
            }
        )
    manifest["files"] = sorted(files, key=lambda item: item["path"])
    MANIFEST_PATH.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def main() -> int:
    source = SOURCE_PATH.read_text(encoding="utf-8")
    if "Compatibility entrypoint for the Adjectives quiz package" in source:
        raise RuntimeError("Public Adjectives package is already split.")
    logic_source, mobile_source, wrapper_source = _build_sources(source)
    LOGIC_PATH.write_text(logic_source, encoding="utf-8", newline="\n")
    MOBILE_PATH.write_text(mobile_source, encoding="utf-8", newline="\n")
    SOURCE_PATH.write_text(wrapper_source, encoding="utf-8", newline="\n")
    _refresh_manifest()

    for path in (SOURCE_PATH, LOGIC_PATH, MOBILE_PATH):
        py_compile.compile(str(path), doraise=True)
    json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

    paths = [
        SOURCE_PATH,
        LOGIC_PATH,
        MOBILE_PATH,
        MANIFEST_PATH,
    ]
    subprocess.run(
        ["git", "add", "--", *[str(path.relative_to(ROOT)) for path in paths]],
        cwd=ROOT,
        check=True,
    )
    print("Published split Adjectives package.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
