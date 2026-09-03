from __future__ import annotations

import hashlib
import json
from pathlib import Path
from urllib.parse import parse_qs, urlsplit
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
TEXT_SUFFIXES = {".py", ".xml", ".json", ".md", ".txt"}

PROJECT_SCHEMA_FILES = {
    "quiz_project.xml",
    "dictionaries/adjectives.xml",
    "dictionaries/copulas.xml",
    "dictionaries/nouns.xml",
    "dictionaries/verbs.xml",
    "grammar/contexts.xml",
    "grammar/grammar_rules.xml",
    "patterns/sentence_maps.xml",
    "patterns/sentence_quizzes.xml",
}
LESSON_SCHEMA_FILE = "lessons/lessons.xml"
LEARNING_XML_FILES = PROJECT_SCHEMA_FILES | {LESSON_SCHEMA_FILE}

DATABASE_MANIFEST_ORDER = [
    "data/dictionaries/adjectives.xml",
    "data/dictionaries/copulas.xml",
    "data/database_revision.json",
    "data/lessons/lessons.xml",
    "data/dictionaries/nouns.xml",
    "data/dictionaries/verbs.xml",
]
DATABASE_CONTENT_FILES = {
    path.removeprefix("data/")
    for path in DATABASE_MANIFEST_ORDER
    if path != "data/database_revision.json"
}
QUIZ_CONTENT_FILES = {
    "quiz_project.xml",
    "grammar/contexts.xml",
    "grammar/grammar_rules.xml",
    "patterns/sentence_maps.xml",
    "patterns/sentence_quizzes.xml",
}

CONTENT_DIRECTORIES = {
    "dictionaries",
    "grammar",
    "lessons",
    "patterns",
    "quizzes",
    "tools",
}
ROOT_XML_FILES = {"quiz_project.xml"}


def load_json(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise AssertionError(f"{path.name} must contain a JSON object")
    return value


def normalized_bytes(path: Path) -> bytes:
    data = path.read_bytes()
    if path.suffix.casefold() in TEXT_SUFFIXES:
        data = data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return data


def file_hash(path: Path) -> str:
    return hashlib.sha256(normalized_bytes(path)).hexdigest()


def validate_repository_layout() -> None:
    root_xml = {path.name for path in ROOT.glob("*.xml")}
    if root_xml != ROOT_XML_FILES:
        raise AssertionError(
            "Only quiz_project.xml may remain at repository root, "
            f"found={sorted(root_xml)}"
        )

    for directory_name in sorted(CONTENT_DIRECTORIES):
        directory = ROOT / directory_name
        if not directory.is_dir():
            raise AssertionError(f"Missing repository directory: {directory_name}")
        if not (directory / "README.md").is_file():
            raise AssertionError(
                f"Repository directory {directory_name} must contain README.md"
            )

    for relative in sorted(LEARNING_XML_FILES):
        if not (ROOT / relative).is_file():
            raise AssertionError(f"Missing canonical learning XML: {relative}")


def validate_manifest_file(entry: dict[str, object], expected_prefix: str) -> Path:
    install_path = str(entry.get("path", ""))
    expected_hash = str(entry.get("sha256", ""))
    url = str(entry.get("url", ""))

    if not install_path.startswith(expected_prefix):
        raise AssertionError(
            f"Manifest path {install_path!r} does not belong to {expected_prefix!r}"
        )
    if len(expected_hash) != 64:
        raise AssertionError(f"Manifest path {install_path!r} has an invalid SHA-256")

    parsed = urlsplit(url)
    if parsed.scheme or parsed.netloc or not parsed.path:
        raise AssertionError(f"Manifest URL {url!r} must be repository-relative")
    source = (ROOT / parsed.path).resolve()
    if ROOT.resolve() not in source.parents:
        raise AssertionError(f"Manifest URL escapes repository root: {url!r}")
    if not source.is_file():
        raise AssertionError(f"Manifest URL points to missing file: {parsed.path}")

    actual_hash = file_hash(source)
    if actual_hash != expected_hash:
        raise AssertionError(
            f"Hash mismatch for {install_path}: manifest={expected_hash}, actual={actual_hash}"
        )

    query_hashes = parse_qs(parsed.query).get("kotomi_sha256", [])
    if query_hashes != [expected_hash]:
        raise AssertionError(
            f"Manifest URL hash for {install_path} must equal its sha256 field"
        )
    return source


def validate_xml_and_schemas() -> None:
    for relative in sorted(LEARNING_XML_FILES):
        path = ROOT / relative
        try:
            root = ET.parse(path).getroot()
        except ET.ParseError as exc:
            raise AssertionError(f"Malformed XML in {relative}: {exc}") from exc

        if relative in PROJECT_SCHEMA_FILES:
            if root.get("schema_version") != "1":
                raise AssertionError(f"{relative} must use project/pattern Schema 1")
        elif relative == LESSON_SCHEMA_FILE:
            if root.get("schema_version") != "4":
                raise AssertionError(
                    f"{LESSON_SCHEMA_FILE} must use lesson catalog Schema 4"
                )


def validate_project_references() -> None:
    manifest_path = ROOT / "quiz_project.xml"
    root = ET.parse(manifest_path).getroot()
    references = {
        node.get("file", "")
        for node in root.iter()
        if node.get("file") is not None
    }
    if not references:
        raise AssertionError("quiz_project.xml does not reference project files")

    expected_references = PROJECT_SCHEMA_FILES - {"quiz_project.xml"}
    if references != expected_references:
        raise AssertionError(
            "quiz_project.xml reference inventory mismatch, "
            f"missing={sorted(expected_references - references)}, "
            f"extra={sorted(references - expected_references)}"
        )

    for relative in sorted(references):
        if not relative:
            raise AssertionError("quiz_project.xml contains an empty file reference")
        path = manifest_path.parent / relative
        if not path.is_file():
            raise AssertionError(f"quiz_project.xml references missing file: {relative}")


def validate_database_manifest() -> None:
    revision = load_json(ROOT / "database_revision.json")
    manifest = load_json(ROOT / "database_update_manifest.json")

    if revision.get("format") != 1 or manifest.get("format") != 1:
        raise AssertionError("Database revision and manifest must use format 1")
    revision_number = revision.get("revision")
    if not isinstance(revision_number, int) or isinstance(revision_number, bool):
        raise AssertionError("Database revision must be an integer")
    if revision_number <= 0:
        raise AssertionError("Database revision must be positive")
    if manifest.get("revision") != revision_number:
        raise AssertionError(
            "Database manifest revision must match database_revision.json"
        )

    entries = manifest.get("files")
    if not isinstance(entries, list):
        raise AssertionError("Database manifest files must be a list")

    install_paths = [
        str(entry.get("path", ""))
        for entry in entries
        if isinstance(entry, dict)
    ]
    if len(install_paths) != len(entries):
        raise AssertionError("Database manifest file entries must be objects")
    if install_paths != DATABASE_MANIFEST_ORDER:
        raise AssertionError(
            "Database manifest must contain only dictionaries, lessons and the "
            f"database revision in canonical order: {DATABASE_MANIFEST_ORDER}"
        )

    source_paths: set[Path] = set()
    for raw_entry in entries:
        source_paths.add(validate_manifest_file(raw_entry, "data/"))

    expected_sources = {
        (ROOT / relative).resolve() for relative in DATABASE_CONTENT_FILES
    } | {(ROOT / "database_revision.json").resolve()}
    if source_paths != expected_sources:
        missing = sorted(
            path.relative_to(ROOT).as_posix()
            for path in expected_sources - source_paths
        )
        extra = sorted(
            path.relative_to(ROOT).as_posix()
            for path in source_paths - expected_sources
        )
        raise AssertionError(
            f"Database manifest inventory mismatch, missing={missing}, extra={extra}"
        )


def package_files(package_dir: Path) -> set[Path]:
    return {
        path.resolve()
        for path in package_dir.rglob("*")
        if path.is_file() and "__pycache__" not in path.parts
    }


def validate_quiz_manifest() -> None:
    manifest = load_json(ROOT / "quiz_update_manifest.json")
    if manifest.get("format") != 1:
        raise AssertionError("Quiz manifest must use format 1")
    if manifest.get("channel") != "quizzes":
        raise AssertionError("Quiz manifest channel must be 'quizzes'")

    packages = manifest.get("packages")
    entries = manifest.get("files")
    if not isinstance(packages, list) or not isinstance(entries, list):
        raise AssertionError("Quiz manifest packages/files must be lists")

    package_dirs = {
        path.name: path
        for path in (ROOT / "quizzes").iterdir()
        if path.is_dir()
    }
    package_ids = {
        str(package.get("id", ""))
        for package in packages
        if isinstance(package, dict)
    }
    if package_ids != set(package_dirs):
        raise AssertionError(
            "Quiz package catalog must exactly match public quizzes/* directories"
        )

    catalog_paths: set[str] = set()
    for raw_package in packages:
        if not isinstance(raw_package, dict):
            raise AssertionError("Quiz package entries must be objects")
        package_id = str(raw_package.get("id", ""))
        if not package_id:
            raise AssertionError("Quiz package id cannot be empty")
        package_dir = package_dirs[package_id]
        descriptor_path = package_dir / "app.json"
        if not descriptor_path.is_file():
            raise AssertionError(f"Quiz package {package_id} is missing app.json")
        descriptor = load_json(descriptor_path)

        if descriptor.get("id") != package_id:
            raise AssertionError(f"Quiz descriptor id mismatch for {package_id}")
        for field in ("version", "quiz_api", "min_app_version", "kind"):
            if descriptor.get(field) != raw_package.get(field):
                raise AssertionError(
                    f"Quiz package {package_id} catalog field {field} "
                    "does not match app.json"
                )
        if descriptor.get("kind") != "python":
            raise AssertionError(f"Unsupported public quiz package kind: {package_id}")

        entrypoint = str(descriptor.get("entrypoint", ""))
        if not entrypoint or not (package_dir / entrypoint).is_file():
            raise AssertionError(f"Quiz package {package_id} has a missing entrypoint")

        raw_files = raw_package.get("files")
        if not isinstance(raw_files, list):
            raise AssertionError(f"Quiz package {package_id} files must be a list")
        declared = {str(value) for value in raw_files}
        actual = {
            "apps/" + path.relative_to(ROOT / "quizzes").as_posix()
            for path in package_files(package_dir)
        }
        if declared != actual:
            raise AssertionError(
                f"Quiz package {package_id} inventory mismatch, "
                f"missing={sorted(actual - declared)}, extra={sorted(declared - actual)}"
            )
        catalog_paths.update(declared)

        for python_file in sorted(package_dir.rglob("*.py")):
            source = python_file.read_text(encoding="utf-8")
            compile(source, str(python_file), "exec")

    manifest_paths: set[str] = set()
    quiz_content_sources: set[Path] = set()
    for raw_entry in entries:
        if not isinstance(raw_entry, dict):
            raise AssertionError("Quiz manifest file entries must be objects")
        install_path = str(raw_entry.get("path", ""))
        if install_path in manifest_paths:
            raise AssertionError(f"Duplicate Quiz manifest path: {install_path}")
        manifest_paths.add(install_path)

        if install_path.startswith("apps/"):
            source = validate_manifest_file(raw_entry, "apps/")
            if not source.relative_to(ROOT).as_posix().startswith("quizzes/"):
                raise AssertionError(
                    f"Quiz package URL must resolve below quizzes/: {install_path}"
                )
            continue

        if install_path.startswith("data/"):
            source = validate_manifest_file(raw_entry, "data/")
            relative = source.relative_to(ROOT).as_posix()
            expected_install_path = f"data/{relative}"
            if relative not in QUIZ_CONTENT_FILES or install_path != expected_install_path:
                raise AssertionError(
                    f"Quiz data entry is not canonical Studio content: {install_path}"
                )
            quiz_content_sources.add(source)
            continue

        raise AssertionError(
            f"Quiz manifest path must belong to apps/ or data/: {install_path}"
        )

    expected_content_sources = {
        (ROOT / relative).resolve() for relative in QUIZ_CONTENT_FILES
    }
    if quiz_content_sources != expected_content_sources:
        missing = sorted(
            path.relative_to(ROOT).as_posix()
            for path in expected_content_sources - quiz_content_sources
        )
        extra = sorted(
            path.relative_to(ROOT).as_posix()
            for path in quiz_content_sources - expected_content_sources
        )
        raise AssertionError(
            f"Quiz Studio content inventory mismatch, missing={missing}, extra={extra}"
        )

    expected_manifest_paths = catalog_paths | {
        f"data/{relative}" for relative in QUIZ_CONTENT_FILES
    }
    if manifest_paths != expected_manifest_paths:
        raise AssertionError(
            "Quiz manifest must contain package files plus canonical Studio content"
        )

    ordered_paths = [str(entry["path"]) for entry in entries]
    if ordered_paths != sorted(ordered_paths):
        raise AssertionError("Quiz manifest file entries must be sorted by install path")


def main() -> None:
    validate_repository_layout()
    validate_xml_and_schemas()
    validate_project_references()
    validate_database_manifest()
    validate_quiz_manifest()
    print("Kotomi-Data validation passed")


if __name__ == "__main__":
    main()
