"""Remove temporary Adjectives publication helpers after validation."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_DIR = ROOT / "quizzes" / "adjectives"
MANIFEST_PATH = ROOT / "quiz_update_manifest.json"


def main() -> int:
    names = ("Kotomi_adjectives.py", "app.json", "logic.py", "mobile.py")
    for name in names:
        if not (PACKAGE_DIR / name).is_file():
            raise RuntimeError(f"Missing public Adjectives package file: {name}")

    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    package = next(item for item in manifest["packages"] if item["id"] == "adjectives")
    expected = {f"apps/adjectives/{name}" for name in names}
    if set(package["files"]) != expected:
        raise RuntimeError("Adjectives package manifest is incomplete.")
    entries = {
        item["path"]: item
        for item in manifest["files"]
        if item["path"].startswith("apps/adjectives/")
    }
    if set(entries) != expected:
        raise RuntimeError("Adjectives file manifest is incomplete.")
    for name in names:
        path = PACKAGE_DIR / name
        manifest_path = f"apps/adjectives/{name}"
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if entries[manifest_path]["sha256"] != digest:
            raise RuntimeError(f"Wrong Adjectives SHA-256 for {name}.")

    temporary = (
        ROOT / ".github" / "apply-adjectives-public-split.trigger",
        ROOT / "tools" / "apply_adjectives_public_split.py",
    )
    for path in temporary:
        if path.exists():
            path.unlink()
    subprocess.run(
        ["git", "add", "-u", "--", *[str(path.relative_to(ROOT)) for path in temporary]],
        cwd=ROOT,
        check=True,
    )
    print("Public Adjectives package is final and temporary helpers are removed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
