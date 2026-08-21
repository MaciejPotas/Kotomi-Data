"""Publish the split Grammar quiz package and refresh its manifest entries."""

from __future__ import annotations

import ast
import copy
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "quizzes" / "grammar"
WRAPPER = PACKAGE / "Kotomi_grammar.py"
LOGIC = PACKAGE / "logic.py"
MOBILE = PACKAGE / "mobile.py"
MANIFEST = ROOT / "quiz_update_manifest.json"
SELF = Path(__file__).resolve()
TRIGGER = ROOT / ".github" / "apply-grammar-public-split.trigger"

FINAL_PATHS = {
    "quiz_update_manifest.json",
    "quizzes/grammar/Kotomi_grammar.py",
    "quizzes/grammar/logic.py",
    "quizzes/grammar/mobile.py",
}
TEMPORARY_PATHS = {
    ".github/apply-grammar-public-split.trigger",
    "tools/apply_grammar_public_split.py",
}


def run(*arguments: str, capture_output: bool = False) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        arguments,
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=capture_output,
    )


def replace_module_docstring(source: str, replacement: str) -> str:
    tree = ast.parse(source)
    if not tree.body:
        return replacement + source
    first = tree.body[0]
    if not (
        isinstance(first, ast.Expr)
        and isinstance(first.value, ast.Constant)
        and isinstance(first.value.value, str)
    ):
        return replacement + source
    lines = source.splitlines(keepends=True)
    return "".join(lines[: first.lineno - 1]) + replacement + "".join(
        lines[first.end_lineno :]
    )


def split_source(source: str) -> tuple[str, str, str]:
    tree = ast.parse(source)
    create_node = next(
        (
            node
            for node in tree.body
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            and node.name == "create_app_class"
        ),
        None,
    )
    if create_node is None:
        raise RuntimeError("Published Grammar source has no create_app_class().")

    lines = source.splitlines(keepends=True)
    split_index = create_node.lineno - 1
    prefix = "".join(lines[:split_index]).rstrip() + "\n"
    suffix = "".join(lines[split_index:]).lstrip()

    aliases: set[str] = set()
    alias_pattern = re.compile(
        r"from\s+apps\.availability\s+import\s+"
        r"Kotomi_availability\s+as\s+(\w+)"
    )
    for match in alias_pattern.finditer(prefix):
        aliases.add(match.group(1))
    prefix = alias_pattern.sub(
        lambda match: (
            "from apps.availability import logic as " + match.group(1)
        ),
        prefix,
    )
    prefix = prefix.replace(
        "apps.availability.Kotomi_availability",
        "apps.availability.logic",
    )
    if not aliases:
        for candidate in ("availability", "availability_quiz"):
            if f"{candidate}.create_app_class" in suffix:
                aliases.add(candidate)

    logic_docstring = (
        '"""Platform-neutral settings and generation policy for Grammar.\n\n'
        "This module intentionally imports no Kivy or Tkinter classes. "
        "Desktop and\nMobile presentations use the same settings, engine, "
        "session, and question\nmodels from here.\n"
        '"""\n'
    )
    logic_source = replace_module_docstring(prefix, logic_docstring)

    suffix = re.sub(
        r"^from __future__ import annotations\s*",
        "",
        suffix,
    )
    for alias in aliases:
        suffix = suffix.replace(
            f"{alias}.create_app_class",
            "availability_mobile.create_app_class",
        )
        suffix = suffix.replace(
            f"{alias}.create_embedded_controller",
            "availability_mobile.create_embedded_controller",
        )
    suffix = suffix.replace(
        "policy=sys.modules[__name__]",
        "policy=_logic",
    )
    suffix = suffix.replace(
        "sys.modules[__name__],",
        "_logic,",
    )

    mobile_header = '''"""Kivy presentation adapter for the Grammar quiz.

Grammar-specific settings and generation live in :mod:`logic`. This module
connects that policy to the reusable Availability mobile presentation.
"""

from __future__ import annotations

import sys

try:
    from .logic import *
    from .logic import _safe_float, _safe_int
    from . import logic as _logic
except ImportError:  # Direct execution from the quiz package directory.
    from logic import *
    from logic import _safe_float, _safe_int
    import logic as _logic

try:
    from apps.availability import mobile as availability_mobile
except ImportError:
    from availability import mobile as availability_mobile

'''
    mobile_source = mobile_header + suffix

    wrapper_source = '''"""Backwards-compatible entrypoint for the Grammar quiz package."""

from __future__ import annotations

try:
    from .logic import *
    from .mobile import create_app_class, create_embedded_controller, main
except ImportError:  # Direct execution from the quiz package directory.
    from logic import *
    from mobile import create_app_class, create_embedded_controller, main


if __name__ == "__main__":
    raise SystemExit(main())
'''

    for name, generated in (
        ("logic.py", logic_source),
        ("mobile.py", mobile_source),
        ("Kotomi_grammar.py", wrapper_source),
    ):
        ast.parse(generated, filename=name)
    return logic_source, mobile_source, wrapper_source


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def public_path(app_path: str) -> str:
    return app_path.replace("apps/grammar/", "quizzes/grammar/", 1)


def cloned_entry(template: dict[str, object], app_path: str) -> dict[str, object]:
    entry = copy.deepcopy(template)
    old_path = str(entry.get("path", ""))
    file_path = ROOT / public_path(app_path)
    entry["path"] = app_path
    if "sha256" in entry:
        entry["sha256"] = sha256(file_path)
    if "size" in entry:
        entry["size"] = file_path.stat().st_size
    if "url" in entry:
        old_public = public_path(old_path) if old_path else ""
        url = str(entry["url"])
        if old_public and old_public in url:
            entry["url"] = url.replace(old_public, public_path(app_path))
        elif old_path and old_path in url:
            entry["url"] = url.replace(old_path, app_path)
        else:
            entry["url"] = public_path(app_path)
    return entry


def refresh_file_list(value: object, app_paths: list[str]) -> object:
    if not isinstance(value, list):
        return value
    if not value:
        return app_paths
    if all(isinstance(item, str) for item in value):
        return app_paths
    if not all(isinstance(item, dict) for item in value):
        raise RuntimeError("Unsupported Grammar manifest file-list format.")

    entries = [dict(item) for item in value]
    existing = {
        str(item.get("path", "")): item
        for item in entries
        if str(item.get("path", "")).startswith("apps/grammar/")
    }
    python_template = next(
        (
            item
            for path, item in existing.items()
            if path.endswith(".py")
        ),
        entries[0],
    )
    json_template = next(
        (
            item
            for path, item in existing.items()
            if path.endswith(".json")
        ),
        python_template,
    )
    result: list[dict[str, object]] = []
    for app_path in app_paths:
        template = existing.get(app_path)
        if template is None:
            template = json_template if app_path.endswith(".json") else python_template
        result.append(cloned_entry(template, app_path))
    return result


def refresh_manifest() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    packages = manifest.get("packages")
    if not isinstance(packages, list):
        raise RuntimeError("quiz_update_manifest.json has no packages list.")
    grammar = next(
        (
            item
            for item in packages
            if isinstance(item, dict) and item.get("id") == "grammar"
        ),
        None,
    )
    if grammar is None:
        raise RuntimeError("Quiz manifest has no Grammar package.")

    app_paths = [
        "apps/grammar/Kotomi_grammar.py",
        "apps/grammar/app.json",
        "apps/grammar/logic.py",
        "apps/grammar/mobile.py",
    ]
    grammar["files"] = refresh_file_list(grammar.get("files"), app_paths)

    top_files = manifest.get("files")
    if isinstance(top_files, list):
        unrelated = []
        grammar_entries = []
        for item in top_files:
            path = item if isinstance(item, str) else str(item.get("path", ""))
            if path.startswith("apps/grammar/"):
                grammar_entries.append(item)
            else:
                unrelated.append(item)
        if grammar_entries:
            manifest["files"] = unrelated + list(
                refresh_file_list(grammar_entries, app_paths)
            )

    MANIFEST.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def main() -> int:
    if LOGIC.exists() or MOBILE.exists():
        raise RuntimeError("Published Grammar package is already split.")
    source = WRAPPER.read_text(encoding="utf-8")
    logic_source, mobile_source, wrapper_source = split_source(source)
    LOGIC.write_text(logic_source, encoding="utf-8", newline="\n")
    MOBILE.write_text(mobile_source, encoding="utf-8", newline="\n")
    WRAPPER.write_text(wrapper_source, encoding="utf-8", newline="\n")
    refresh_manifest()

    SELF.unlink()
    TRIGGER.unlink(missing_ok=True)
    run("git", "add", "--", *sorted(FINAL_PATHS))
    run("git", "add", "-u", "--", *sorted(TEMPORARY_PATHS))
    run("git", "diff", "--cached", "--check")

    staged = {
        line.strip()
        for line in run(
            "git", "diff", "--cached", "--name-only", capture_output=True
        ).stdout.splitlines()
        if line.strip()
    }
    expected = FINAL_PATHS | TEMPORARY_PATHS
    if staged != expected:
        raise RuntimeError(
            "Unexpected staged public Grammar paths. "
            f"Missing: {sorted(expected - staged) or 'none'}; "
            f"unexpected: {sorted(staged - expected) or 'none'}."
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
