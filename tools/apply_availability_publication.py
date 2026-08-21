"""Publish and validate the split Availability package from an exported archive."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import py_compile
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_PACKAGE_FILES = [
    "apps/availability/Kotomi_availability.py",
    "apps/availability/logic.py",
    "apps/availability/mobile.py",
    "apps/availability/app.json",
]


def publish(package_root: Path) -> None:
    source = package_root / "apps" / "availability"
    destination = ROOT / "quizzes" / "availability"
    destination.mkdir(parents=True, exist_ok=True)
    for name in ("Kotomi_availability.py", "logic.py", "mobile.py", "app.json"):
        input_path = source / name
        if not input_path.is_file():
            raise RuntimeError(f"Missing exported Availability file: {input_path}")
        shutil.copy2(input_path, destination / name)

    manifest_path = ROOT / "quiz_update_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    package = next(
        item for item in manifest.get("packages", [])
        if item.get("id") == "availability"
    )
    package["files"] = EXPECTED_PACKAGE_FILES

    entries = [
        item for item in manifest.get("files", [])
        if not str(item.get("path", "")).startswith("apps/availability/")
    ]
    for path in EXPECTED_PACKAGE_FILES:
        relative = path.removeprefix("apps/availability/")
        file_path = destination / relative
        digest = hashlib.sha256(file_path.read_bytes()).hexdigest()
        entries.append(
            {
                "path": path,
                "sha256": digest,
                "url": (
                    f"quizzes/availability/{relative}"
                    f"?kotomi_sha256={digest}"
                ),
            }
        )
    manifest["files"] = sorted(entries, key=lambda item: item["path"])
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def validate() -> None:
    manifest = json.loads(
        (ROOT / "quiz_update_manifest.json").read_text(encoding="utf-8")
    )
    package = next(
        item for item in manifest.get("packages", [])
        if item.get("id") == "availability"
    )
    if package.get("files") != EXPECTED_PACKAGE_FILES:
        raise RuntimeError("Incorrect Availability package file list.")

    entries = {item["path"]: item for item in manifest.get("files", [])}
    for path in EXPECTED_PACKAGE_FILES:
        relative = path.removeprefix("apps/availability/")
        file_path = ROOT / "quizzes" / "availability" / relative
        digest = hashlib.sha256(file_path.read_bytes()).hexdigest()
        entry = entries.get(path)
        if entry is None or entry.get("sha256") != digest:
            raise RuntimeError(f"Incorrect manifest SHA-256 for {path}.")
        expected_url = (
            f"quizzes/availability/{relative}?kotomi_sha256={digest}"
        )
        if entry.get("url") != expected_url:
            raise RuntimeError(f"Incorrect manifest URL for {path}.")

    for name in ("Kotomi_availability.py", "logic.py", "mobile.py"):
        py_compile.compile(
            str(ROOT / "quizzes" / "availability" / name),
            doraise=True,
        )


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        raise SystemExit("usage: apply_availability_publication.py <package-root>")
    publish(Path(argv[1]).resolve())
    validate()
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
