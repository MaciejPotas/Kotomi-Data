from __future__ import annotations

import hashlib
import json
from pathlib import Path
from urllib.parse import parse_qs, urlsplit
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
LEARNING_ROOT = ROOT / "learning"
PROJECT_MANIFEST = LEARNING_ROOT / "quiz_project.xml"
DATABASE_REVISION_PATH = ROOT / "database_revision.json"
TEXT_SUFFIXES = {".py", ".xml", ".json", ".md", ".txt"}
SCHEMA_FILES = {
    LEARNING_ROOT / "dictionaries" / "adjectives.xml": "1",
    LEARNING_ROOT / "dictionaries" / "copulas.xml": "1",
    LEARNING_ROOT / "dictionaries" / "nouns.xml": "1",
    LEARNING_ROOT / "dictionaries" / "verbs.xml": "1",
    LEARNING_ROOT / "grammar" / "contexts.xml": "1",
    LEARNING_ROOT / "grammar" / "grammar_rules.xml": "1",
    LEARNING_ROOT / "grammar" / "sentence_maps.xml": "1",
    LEARNING_ROOT / "grammar" / "sentence_quizzes.xml": "1",
    LEARNING_ROOT / "lessons" / "lessons.xml": "4",
    PROJECT_MANIFEST: "1",
}
REQUIRED_READMES = {
    ROOT / "README.md",
    LEARNING_ROOT / "README.md",
    LEARNING_ROOT / "dictionaries" / "README.md",
    LEARNING_ROOT / "grammar" / "README.md",
    LEARNING_ROOT / "lessons" / "README.md",
    ROOT / "quizzes" / "README.md",
    ROOT / "tools" / "README.md",
}


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


def relative(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()


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


def validate_layout_and_docs() -> None:
    root_xml = sorted(ROOT.glob("*.xml"))
    if root_xml:
        raise AssertionError(
            "Learning XML must not live at repository root: "
            + ", ".join(path.name for path in root_xml)
        )
    if not DATABASE_REVISION_PATH.is_file():
        raise AssertionError("Missing root database_revision.json")
    for path in sorted(REQUIRED_READMES):
        if not path.is_file():
            raise AssertionError(f"Missing directory documentation: {relative(path)}")


def validate_xml_and_schemas() -> None:
    actual_xml = {path.resolve() for path in LEARNING_ROOT.rglob("*.xml")}
    expected_xml = {path.resolve() for path in SCHEMA_FILES}
    if actual_xml != expected_xml:
        missing = sorted(relative(path) for path in expected_xml - actual_xml)
        extra = sorted(relative(path) for path in actual_xml - expected_xml)
        raise AssertionError(
            f"Learning XML inventory mismatch, missing={missing}, extra={extra}"
        )

    for path, expected_schema in sorted(
        SCHEMA_FILES.items(), key=lambda item: item[0].as_posix()
    ):
        try:
            root = ET.parse(path).getroot()
        except ET.ParseError as exc:
            raise AssertionError(f"Malformed XML in {relative(path)}: {exc}") from exc
        if root.get("schema_version") != expected_schema:
            raise AssertionError(
                f"{relative(path)} must use Schema {expected_schema}"
            )


def validate_project_references() -> None:
    root = ET.parse(PROJECT_MANIFEST).getroot()
    references = {
        node.get("file", "")
        for node in root.iter()
        if node.get("file") is not None
    }
    if not references:
        raise AssertionError("learning/quiz_project.xml has no file references")
    for value in sorted(references):
        if not value:
            raise AssertionError("learning/quiz_project.xml contains an empty file reference")
        path = (PROJECT_MANIFEST.parent / value).resolve()
        if LEARNING_ROOT.resolve() not in path.parents:
            raise AssertionError(f"Project reference escapes learning/: {value}")
        if not path.is_file():
            raise AssertionError(f"Project reference points to missing file: {value}")


def validate_database_manifest() -> None:
    revision = load_json(DATABASE_REVISION_PATH)
    manifest = load_json(ROOT / "database_update_manifest.json")

    if revision.get("format") != 1 or manifest.get("format") != 1:
        raise AssertionError("Database revision and manifest must use format 1")
    revision_number = revision.get("revision")
    if not isinstance(revision_number, int) or isinstance(revision_number, bool):
        raise AssertionError("Database revision must be an integer")
    if revision_number <= 0:
        raise AssertionError("Database revision must be positive")
    if manifest.get("revision") != revision_number:
        raise AssertionError("Database manifest revision must match database_revision.json")

    entries = manifest.get("files")
    if not isinstance(entries, list):
        raise AssertionError("Database manifest files must be a list")

    install_paths: set[str] = set()
    source_paths: set[Path] = set()
    for raw_entry in entries:
        if not isinstance(raw_entry, dict):
            raise AssertionError("Database manifest file entries must be objects")
        install_path = str(raw_entry.get("path", ""))
        if install_path in install_paths:
            raise AssertionError(f"Duplicate Database manifest path: {install_path}")
        install_paths.add(install_path)
        source_paths.add(validate_manifest_file(raw_entry, "data/"))

    expected_sources = {
        path.resolve() for path in SCHEMA_FILES
    } | {DATABASE_REVISION_PATH.resolve()}
    if source_paths != expected_sources:
        missing = sorted(relative(path) for path in expected_sources - source_paths)
        extra = sorted(relative(path) for path in source_paths - expected_sources)
        raise AssertionError(
            f"Database manifest inventory mismatch, missing={missing}, extra={extra}"
        )

    expected_install_paths = {
        f"data/{relative(path)}" for path in expected_sources
    }
    if install_paths != expected_install_paths:
        raise AssertionError("Database install paths do not match canonical learning inventory")


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
                    f"Quiz package {package_id} catalog field {field} does not match app.json"
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
    for raw_entry in entries:
        if not isinstance(raw_entry, dict):
            raise AssertionError("Quiz manifest file entries must be objects")
        install_path = str(raw_entry.get("path", ""))
        if install_path in manifest_paths:
            raise AssertionError(f"Duplicate Quiz manifest path: {install_path}")
        manifest_paths.add(install_path)
        source = validate_manifest_file(raw_entry, "apps/")
        if not source.relative_to(ROOT).as_posix().startswith("quizzes/"):
            raise AssertionError(
                f"Quiz manifest URL must resolve below quizzes/: {install_path}"
            )

    if manifest_paths != catalog_paths:
        raise AssertionError(
            "Quiz manifest flat inventory must equal the package catalog inventory"
        )


def main() -> None:
    validate_layout_and_docs()
    validate_xml_and_schemas()
    validate_project_references()
    validate_database_manifest()
    validate_quiz_manifest()
    print("Kotomi-Data validation passed")


if __name__ == "__main__":
    main()
