"""Apply and validate the split Availability package publication."""

from __future__ import annotations

import base64
import gzip
import hashlib
import json
from pathlib import Path
import py_compile
import subprocess

ROOT = Path(__file__).resolve().parents[1]
PATCH_DIRECTORY = ROOT / ".github" / "availability-data-patch"
PATCH_PATH = ROOT / ".git" / "availability-data-publication.patch"

PUBLIC_PATHS = {
    "quiz_update_manifest.json",
    "quizzes/availability/Kotomi_availability.py",
    "quizzes/availability/logic.py",
    "quizzes/availability/mobile.py",
}
BASE_TEMPORARY_PATHS = {"tools/apply_availability_publication.py"}
EXPECTED_PACKAGE_FILES = [
    "apps/availability/Kotomi_availability.py",
    "apps/availability/logic.py",
    "apps/availability/mobile.py",
    "apps/availability/app.json",
]


def run(*arguments: str, capture_output: bool = False) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        arguments,
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=capture_output,
    )


def validate_publication() -> None:
    manifest = json.loads(
        (ROOT / "quiz_update_manifest.json").read_text(encoding="utf-8")
    )
    package = next(
        item for item in manifest.get("packages", [])
        if item.get("id") == "availability"
    )
    if package.get("files") != EXPECTED_PACKAGE_FILES:
        raise RuntimeError(
            "Availability package file list does not match the split package."
        )

    entries = {
        item["path"]: item
        for item in manifest.get("files", [])
        if isinstance(item, dict) and "path" in item
    }
    for path in EXPECTED_PACKAGE_FILES:
        relative = path.removeprefix("apps/availability/")
        source = ROOT / "quizzes" / "availability" / relative
        if not source.is_file():
            raise RuntimeError(f"Missing published Availability file: {source}")
        digest = hashlib.sha256(source.read_bytes()).hexdigest()
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


def main() -> int:
    parts = sorted(PATCH_DIRECTORY.glob("part-*.txt"))
    if not parts:
        raise RuntimeError(f"No publication patch parts found in {PATCH_DIRECTORY}")

    part_paths = {part.relative_to(ROOT).as_posix() for part in parts}
    temporary_paths = BASE_TEMPORARY_PATHS | part_paths
    encoded = "".join(part.read_text(encoding="ascii").strip() for part in parts)
    PATCH_PATH.write_bytes(gzip.decompress(base64.b64decode(encoded)))
    try:
        run("git", "apply", "--index", "--whitespace=error-all", str(PATCH_PATH))
    finally:
        PATCH_PATH.unlink(missing_ok=True)

    validate_publication()

    for name in temporary_paths:
        (ROOT / name).unlink(missing_ok=True)
    if PATCH_DIRECTORY.exists():
        PATCH_DIRECTORY.rmdir()

    run("git", "add", "-u", "--", *sorted(temporary_paths))
    run("git", "diff", "--cached", "--check")

    staged = {
        line.strip()
        for line in run(
            "git", "diff", "--cached", "--name-only", capture_output=True
        ).stdout.splitlines()
        if line.strip()
    }
    expected = PUBLIC_PATHS | temporary_paths
    if staged != expected:
        missing = sorted(expected - staged)
        unexpected = sorted(staged - expected)
        raise RuntimeError(
            "Unexpected staged publication paths. "
            f"Missing: {missing or 'none'}; unexpected: {unexpected or 'none'}."
        )

    run("git", "status", "--short")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
