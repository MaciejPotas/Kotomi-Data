"""Synchronize the public quiz catalog with the current Kotomi 1.1.1 sources."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Mapping


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "quiz_update_manifest.json"
CATALOG_VERSION = "1.1.1"

EXPECTED_BLOB_SHA: Mapping[str, str] = {
    "quizzes/lessons/Kotomi_lessons.py": "809754880ec0703fa216b0a1b6298f40d54d2011",
    "quizzes/lessons/app.json": "ff2252c3bf1276d838d72618d432d823f1235e8f",
    "quizzes/lessons/logic.py": "25bbf71ccb8219897c6547c2cbf60984932b6162",
    "quizzes/lessons/mobile.py": "f196367530308b350b2019cd8c5886924e63dcf5",
    "quizzes/verbs/Kotomi_verbs.py": "ce741a1d72cea63ca125687862c8260a86b02132",
    "quizzes/verbs/app.json": "cdc3d7d9b607f17a90cae07daddc010a0572a7ec",
    "quizzes/verbs/logic.py": "bdab5525a67ef3c272ab1546a826767db72fa38c",
    "quizzes/verbs/mobile.py": "ee16867346f61a8f62ec9bda00fdd0e94f8080e4",
    "quizzes/adjectives/Kotomi_adjectives.py": "f96c5aac97a9f75b4ade0c708416c01916630e0a",
    "quizzes/adjectives/app.json": "437290d4740631164bdc34438b84f61a554ea028",
    "quizzes/adjectives/logic.py": "056ff85ed103cfbd106ada4e48f20e2ffb913862",
    "quizzes/adjectives/mobile.py": "075bec4bef927c367cb44ad6a804a6f84ebfb7f7",
    "quizzes/availability/Kotomi_availability.py": "1a71cbe9bd16c533a60aaa1425820e04418aec22",
    "quizzes/availability/app.json": "6783f0c81bf50d0137d0aff0dfe692f6f20f3505",
    "quizzes/availability/logic.py": "68460fddb4d860ee18def1a6be7197f650c5365f",
    "quizzes/availability/mobile.py": "950f22261e9fc6e3dc6ca0379f942608d117c0e4",
    "quizzes/grammar/Kotomi_grammar.py": "5e1bbb255bc9d8bb7220be45ff8dd98edb2c3b82",
    "quizzes/grammar/app.json": "c226543918db95faaab855e5375eb52855df6ce2",
    "quizzes/grammar/logic.py": "eecf20e4b022591a3ffb7226087914f80f24265e",
    "quizzes/grammar/mobile.py": "126219953b742777a634211c273a7dc5c2f27eb8",
}

MOBILE_I18N_BLOCK = (
    "try:\n"
    "    from shared.mobile_i18n import mobile_error_text, mobile_text\n"
    "except ImportError:  # Direct execution adds ``shared`` itself to sys.path.\n"
    "    from mobile_i18n import mobile_error_text, mobile_text\n"
)


def _canonical_bytes(path: Path) -> bytes:
    return path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def _write_text(path: Path, text: str) -> None:
    path.write_bytes(text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8"))


def _replace_once(relative: str, old: str, new: str) -> None:
    path = ROOT / relative
    text = _canonical_bytes(path).decode("utf-8")
    count = text.count(old)
    if count != 1:
        raise RuntimeError(
            f"Expected one occurrence in {relative}, found {count}: {old!r}"
        )
    _write_text(path, text.replace(old, new, 1))


def _git_blob_sha(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def _synchronize_imports() -> None:
    _replace_once(
        "quizzes/lessons/mobile.py",
        "from shared.settings_xml import settings_path",
        "from kotomi_core.settings_xml import settings_path",
    )
    _replace_once(
        "quizzes/lessons/mobile.py",
        "from shared.app_identity import (",
        "from kotomi_core.app_identity import (",
    )
    _replace_once(
        "quizzes/lessons/mobile.py",
        "from shared.mobile_i18n import mobile_error_text, mobile_text",
        "from kotomi_core.mobile_i18n import mobile_error_text, mobile_text",
    )

    for package in ("verbs", "adjectives", "availability"):
        _replace_once(
            f"quizzes/{package}/logic.py",
            "from settings_xml import load_settings, save_settings",
            "from kotomi_core.settings_xml import load_settings, save_settings",
        )
        _replace_once(
            f"quizzes/{package}/mobile.py",
            "from shared.app_identity import (",
            "from kotomi_core.app_identity import (",
        )
        _replace_once(
            f"quizzes/{package}/mobile.py",
            MOBILE_I18N_BLOCK,
            "from kotomi_core.mobile_i18n import mobile_error_text, mobile_text\n",
        )
        _replace_once(
            f"quizzes/{package}/mobile.py",
            "from quiz_updater import QuizUpdater, UpdateError, load_update_url",
            "from kotomi_core.update_transport import QuizUpdater, UpdateError, load_update_url",
        )

    _replace_once(
        "quizzes/verbs/mobile.py",
        "from settings_xml import settings_path",
        "from kotomi_core.settings_xml import settings_path",
    )
    _replace_once(
        "quizzes/adjectives/mobile.py",
        "from settings_xml import settings_path",
        "from kotomi_core.settings_xml import settings_path",
    )
    _replace_once(
        "quizzes/availability/mobile.py",
        "from settings_xml import settings_path",
        "from kotomi_core.settings_xml import settings_path",
    )
    _replace_once(
        "quizzes/grammar/logic.py",
        "from settings_xml import load_settings, save_settings, settings_path",
        "from kotomi_core.settings_xml import load_settings, save_settings, settings_path",
    )


def _verify_package_blobs() -> None:
    errors: list[str] = []
    for relative, expected in EXPECTED_BLOB_SHA.items():
        path = ROOT / relative
        if not path.is_file():
            errors.append(f"missing {relative}")
            continue
        data = _canonical_bytes(path)
        if data != path.read_bytes():
            path.write_bytes(data)
        actual = _git_blob_sha(data)
        if actual != expected:
            errors.append(f"{relative}: expected {expected}, got {actual}")
    if errors:
        raise RuntimeError("Quiz package synchronization failed:\n" + "\n".join(errors))


def _refresh_manifest() -> None:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    if manifest.get("format") != 1 or manifest.get("channel") != "quizzes":
        raise RuntimeError("Unexpected quiz manifest format or channel.")
    manifest["version"] = CATALOG_VERSION

    expected_install_paths = {
        "apps/" + relative.removeprefix("quizzes/")
        for relative in EXPECTED_BLOB_SHA
    }
    manifest_paths = {
        str(item.get("path", ""))
        for item in manifest.get("files", [])
        if isinstance(item, dict)
    }
    if manifest_paths != expected_install_paths:
        raise RuntimeError(
            "Quiz manifest inventory differs from the synchronized package files."
        )

    for item in manifest["files"]:
        install_path = str(item["path"])
        public_path = "quizzes/" + install_path.removeprefix("apps/")
        payload = _canonical_bytes(ROOT / public_path)
        digest = hashlib.sha256(payload).hexdigest()
        item["sha256"] = digest
        item["url"] = f"{public_path}?kotomi_sha256={digest}"

    MANIFEST_PATH.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def main() -> int:
    _synchronize_imports()
    _verify_package_blobs()
    _refresh_manifest()
    print("Synchronized all five public quiz packages with Kotomi main.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
