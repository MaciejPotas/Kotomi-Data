"""Synchronize PR #29 published quiz logic with Kotomi PR #113."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

PATCHES = {
    "quizzes/adjectives/logic.py": {
        '"adjective_predicate": "Po rzeczowniku z partykułą wa"': '"Przymiotnik po temacie": "Po rzeczowniku z partykułą wa"',
        '"adjective_simple": "Proste zdanie wskazujące"': '"Sam przymiotnik": "Proste zdanie wskazujące"',
        '"adjective_attributive": "Przymiotnik przed rzeczownikiem"': '"Przymiotnik przed rzeczownikiem": "Przymiotnik przed rzeczownikiem"',
        'if "adjective_predicate" in settings.enabled_patterns:': 'if "Przymiotnik po temacie" in settings.enabled_patterns:',
        'self.project.patterns["adjective_predicate"]': 'self.project.patterns["Przymiotnik po temacie"]',
        'if "adjective_simple" in settings.enabled_patterns:': 'if "Sam przymiotnik" in settings.enabled_patterns:',
        'self.project.patterns["adjective_simple"]': 'self.project.patterns["Sam przymiotnik"]',
        'if "adjective_attributive" in settings.enabled_patterns:': 'if "Przymiotnik przed rzeczownikiem" in settings.enabled_patterns:',
        'self.project.patterns["adjective_attributive"]': 'self.project.patterns["Przymiotnik przed rzeczownikiem"]',
    },
    "quizzes/availability/logic.py": {
        '"verb_noun_ga_aru__simple": "Sam czasownik"': '"Dostępność 〜がある / Sam czasownik": "Sam czasownik"',
        '"verb_noun_ga_aru__transitive_object": "Dopełnienie"': '"Dostępność 〜がある / Czasownik z dopełnieniem": "Dopełnienie"',
        '"verb_noun_ga_aru__destination": "Cel ruchu"': '"Dostępność 〜がある / Cel ruchu": "Cel ruchu"',
        '"verb_noun_ga_aru__companion": "Towarzysz"': '"Dostępność 〜がある / Towarzysz": "Towarzysz"',
        '"verb_noun_ga_aru__place": "Miejsce"': '"Dostępność 〜がある / Miejsce czynności": "Miejsce"',
        'pattern.composite_id != "verb_noun_ga_aru"': 'pattern.composite_id != "Dostępność 〜がある"',
    },
    "quizzes/grammar/logic.py": {
        '"koto_ga_dekiru__simple": "ことができる, sam czasownik"': '"Możliwość ことができる / Sam czasownik": "ことができる, sam czasownik"',
        '"koto_ga_dekiru__transitive_object": "ことができる, dopełnienie"': '"Możliwość ことができる / Czasownik z dopełnieniem": "ことができる, dopełnienie"',
        '"koto_ga_dekiru__place": "ことができる, miejsce"': '"Możliwość ことができる / Miejsce czynności": "ことができる, miejsce"',
    },
    "quizzes/verbs/logic.py": {
        '"simple": "Proste zdanie"': '"Sam czasownik": "Proste zdanie"',
        '"transitive_object": "Zdanie z dopełnieniem"': '"Czasownik z dopełnieniem": "Zdanie z dopełnieniem"',
        '"destination": "Zdanie z celem ruchu"': '"Cel ruchu": "Zdanie z celem ruchu"',
        '"companion": "Zdanie z towarzyszem"': '"Towarzysz": "Zdanie z towarzyszem"',
        '"place": "Zdanie z miejscem czynności"': '"Miejsce czynności": "Zdanie z miejscem czynności"',
        '"vehicle": "Zdanie ze środkiem transportu"': '"Środek transportu": "Zdanie ze środkiem transportu"',
        '"subject": "Zdanie z podmiotem i が"': '"Podmiot z が": "Zdanie z podmiotem i が"',
    },
}


def patch_file(relative: str, replacements: dict[str, str]) -> None:
    path = ROOT / relative
    text = path.read_text(encoding="utf-8")
    for old, new in replacements.items():
        if old not in text:
            raise RuntimeError(f"Expected text not found in {relative}: {old}")
        text = text.replace(old, new)
    path.write_text(text, encoding="utf-8", newline="\n")


def update_quiz_manifest() -> None:
    manifest_path = ROOT / "quiz_update_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    changed = set(PATCHES)
    for item in manifest["files"]:
        public_path = "quizzes/" + item["path"].removeprefix("apps/")
        if public_path not in changed:
            continue
        digest = hashlib.sha256((ROOT / public_path).read_bytes()).hexdigest()
        item["sha256"] = digest
        item["url"] = f"{public_path}?kotomi_sha256={digest}"
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def validate() -> None:
    manifest = json.loads((ROOT / "quiz_update_manifest.json").read_text(encoding="utf-8"))
    entries = {item["path"]: item for item in manifest["files"]}
    for public_path in PATCHES:
        app_path = "apps/" + public_path.removeprefix("quizzes/")
        digest = hashlib.sha256((ROOT / public_path).read_bytes()).hexdigest()
        item = entries[app_path]
        if item["sha256"] != digest:
            raise RuntimeError(f"Stale hash for {app_path}")
        expected_url = f"{public_path}?kotomi_sha256={digest}"
        if item["url"] != expected_url:
            raise RuntimeError(f"Stale URL for {app_path}")


def main() -> int:
    for relative, replacements in PATCHES.items():
        patch_file(relative, replacements)
    update_quiz_manifest()
    validate()

    Path(__file__).unlink()
    workflow = ROOT / ".github" / "workflows" / "publish-pattern-identity-pr29.yml"
    workflow.unlink(missing_ok=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
