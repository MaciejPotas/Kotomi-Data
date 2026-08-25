from __future__ import annotations

import hashlib
import json
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
VERSION = "1.1.1"
TEXT_SUFFIXES = {".py", ".xml", ".json", ".md", ".txt", ".bat", ".yml", ".yaml"}


def canonical_bytes(path: Path) -> bytes:
    data = path.read_bytes()
    if path.suffix.lower() in TEXT_SUFFIXES or path.name == "LICENSE":
        data = data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return data


def digest(path: Path) -> str:
    return hashlib.sha256(canonical_bytes(path)).hexdigest()


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")


def migrate_logic(quiz_id: str) -> None:
    path = ROOT / "quizzes" / quiz_id / "logic.py"
    text = path.read_text(encoding="utf-8")
    old = (
        'SCRIPT_DIR = Path(__file__).resolve().parent\n'
        'REPOSITORY_SHARED_DIR = SCRIPT_DIR.parents[1] / "shared"\n'
        'INSTALL_ROOT = REPOSITORY_SHARED_DIR.parent\n'
        'REPOSITORY_DATA_DIR = INSTALL_ROOT / "data"\n'
        'for import_root in (INSTALL_ROOT, REPOSITORY_SHARED_DIR):\n'
        '    if str(import_root) not in sys.path:\n'
        '        sys.path.insert(0, str(import_root))\n'
    )
    new = (
        'SCRIPT_DIR = Path(__file__).resolve().parent\n'
        'INSTALL_ROOT = SCRIPT_DIR.parents[1]\n'
        'REPOSITORY_DATA_DIR = INSTALL_ROOT / "data"\n'
        'if str(INSTALL_ROOT) not in sys.path:\n'
        '    sys.path.insert(0, str(INSTALL_ROOT))\n'
    )
    if old not in text:
        raise RuntimeError(f"Install-root compatibility block missing in {path}")
    text = text.replace(old, new, 1)
    text = text.replace("from quiz_core import (", "from kotomi_core.project import (")
    text = text.replace("from quiz_core import ProjectError, Word", "from kotomi_core.project import ProjectError, Word")
    text = text.replace("from quiz_core import Entity, ProjectError, Word", "from kotomi_core.project import Entity, ProjectError, Word")
    text = text.replace("from quiz_engine import ", "from kotomi_core.generation import ")
    text = text.replace("from mobile_ui import ", "from kotomi_ui.mobile import ")
    text = text.replace('        REPOSITORY_SHARED_DIR / "quiz_data" / "quiz_project.xml",\n', "")
    text = text.replace('    "REPOSITORY_SHARED_DIR",\n', "")
    write_text(path, text)


def migrate_lessons() -> None:
    path = ROOT / "quizzes" / "lessons" / "logic.py"
    text = path.read_text(encoding="utf-8")
    text = text.replace("from shared.mobile_ui import ", "from kotomi_ui.mobile import ")
    start = text.index('SHARED_DIR = INSTALL_ROOT / "shared"\n')
    end_marker = 'QUIZ_PROJECT = QUIZ_DATA_DIR / "quiz_project.xml"\n'
    end = text.index(end_marker, start) + len(end_marker)
    text = text[:start] + (
        'QUIZ_DATA_DIR = INSTALL_ROOT / "data"\n'
        'QUIZ_PROJECT = QUIZ_DATA_DIR / "quiz_project.xml"\n'
    ) + text[end:]
    for export in ("SHARED_DIR", "CANONICAL_QUIZ_DATA_DIR", "LEGACY_QUIZ_DATA_DIR"):
        text = text.replace(f'    "{export}",\n', "")
    write_text(path, text)


def migrate_mobile(quiz_id: str) -> None:
    path = ROOT / "quizzes" / quiz_id / "mobile.py"
    text = path.read_text(encoding="utf-8")
    text = text.replace("from quiz_core import ProjectError", "from kotomi_core.project import ProjectError")
    text = text.replace("from mobile_ui import ", "from kotomi_ui.mobile import ")
    text = text.replace("from shared.mobile_ui import ", "from kotomi_ui.mobile import ")
    if "from kotomi_core.paths import FONTS_DIR\n" not in text:
        marker = "from kotomi_core.settings_xml import settings_path\n"
        if marker in text:
            text = text.replace(marker, marker + "from kotomi_core.paths import FONTS_DIR\n", 1)
        else:
            marker = "from kotomi_core.mobile_i18n import mobile_error_text, mobile_text\n"
            if marker not in text:
                raise RuntimeError(f"Cannot place FONTS_DIR import in {path}")
            text = text.replace(marker, "from kotomi_core.paths import FONTS_DIR\n" + marker, 1)
    text = text.replace('REPOSITORY_SHARED_DIR = INSTALL_ROOT / "shared"\n', "")
    text = text.replace(
        'for import_root in (INSTALL_ROOT, REPOSITORY_SHARED_DIR):\n'
        '    if str(import_root) not in sys.path:\n'
        '        sys.path.insert(0, str(import_root))\n',
        'if str(INSTALL_ROOT) not in sys.path:\n'
        '    sys.path.insert(0, str(INSTALL_ROOT))\n',
    )
    text = text.replace(
        'SHARED_DIR = REPOSITORY_SHARED_DIR\nMOBILE_FONT = mobile_font_path(SHARED_DIR)\n',
        'MOBILE_FONT = mobile_font_path(FONTS_DIR)\n',
    )
    text = text.replace('mixed_font = mobile_font_path(REPOSITORY_SHARED_DIR)', 'mixed_font = mobile_font_path(FONTS_DIR)')
    text = text.replace('MOBILE_FONT = mobile_font_path(SHARED_DIR)', 'MOBILE_FONT = mobile_font_path(FONTS_DIR)')
    write_text(path, text)


def canonicalize_all_package_imports() -> None:
    for path in ROOT.glob("quizzes/*/*.py"):
        text = path.read_text(encoding="utf-8")
        text = text.replace("from quiz_core import ", "from kotomi_core.project import ")
        text = text.replace("from quiz_engine import ", "from kotomi_core.generation import ")
        text = text.replace("from mobile_ui import ", "from kotomi_ui.mobile import ")
        text = text.replace("from shared.mobile_ui import ", "from kotomi_ui.mobile import ")
        write_text(path, text)


def rebuild_database_manifest() -> None:
    files = []
    for source in sorted(ROOT.glob("*.xml"), key=lambda value: value.name):
        sha = digest(source)
        files.append({
            "path": f"data/{source.name}",
            "sha256": sha,
            "url": f"{source.name}?kotomi_sha256={sha}",
        })
    write_text(
        ROOT / "database_update_manifest.json",
        json.dumps({"format": 1, "version": VERSION, "files": files}, indent=2, ensure_ascii=False) + "\n",
    )


def rebuild_quiz_manifest() -> None:
    path = ROOT / "quiz_update_manifest.json"
    manifest = json.loads(path.read_text(encoding="utf-8"))
    for item in manifest["files"]:
        install = PurePosixPath(str(item["path"]))
        source = ROOT.joinpath("quizzes", *install.parts[1:])
        sha = digest(source)
        public = PurePosixPath("quizzes", *install.parts[1:])
        item["sha256"] = sha
        item["url"] = f"{public.as_posix()}?kotomi_sha256={sha}"
    write_text(path, json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")


def update_readme() -> None:
    path = ROOT / "README.md"
    text = path.read_text(encoding="utf-8")
    text = text.replace(
        "The canonical Kotomi installation location is now `data/`. While Kotomi remains on version 1.1.1, `database_update_manifest.json` deliberately publishes each XML to both `data/` and the historical `shared/quiz_data/` path. This compatibility bridge keeps older 1.1.1 installations functional even when Database Update runs before Application Update. It can be removed after the application version is bumped and the legacy layout no longer needs support.",
        "Kotomi has one supported learning-data installation location: `data/`. The Database manifest publishes each XML only to that canonical path. The pre-refactor `shared/quiz_data/` layout is intentionally unsupported for the fresh-start architecture.",
    )
    text = text.replace(
        "Because version 1.1.1 installations can update quiz packages independently, the published package code keeps compatibility imports that older 1.1.1 application builds understand. Project lookup prefers the canonical `data/quiz_project.xml` and falls back to `shared/quiz_data/quiz_project.xml`.",
        "Published quiz packages use the canonical Kotomi APIs and load their project from `data/quiz_project.xml`. They are released together with the fresh-start application contract rather than carrying pre-refactor import or path fallbacks.",
    )
    write_text(path, text)


def main() -> None:
    for quiz_id in ("verbs", "adjectives", "availability", "grammar"):
        migrate_logic(quiz_id)
    migrate_lessons()
    for quiz_id in ("verbs", "adjectives", "availability", "lessons"):
        migrate_mobile(quiz_id)
    canonicalize_all_package_imports()
    rebuild_database_manifest()
    rebuild_quiz_manifest()
    update_readme()


if __name__ == "__main__":
    main()
