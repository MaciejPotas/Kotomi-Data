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
    "dictionaries/interrogatives.xml",
    "dictionaries/nouns.xml",
    "dictionaries/verbs.xml",
    "grammar/contexts.xml",
    "grammar/grammar_rules.xml",
    "patterns/sentence_maps.xml",
    "patterns/sentence_quizzes.xml",
}
LESSON_SCHEMA_FILE = "lessons/lessons.xml"
LEARNING_XML_FILES = PROJECT_SCHEMA_FILES | {LESSON_SCHEMA_FILE}
CONTENT_MANIFEST_ORDER = [
    "data/content_revision.json",
    "data/dictionaries/adjectives.xml",
    "data/dictionaries/copulas.xml",
    "data/dictionaries/interrogatives.xml",
    "data/dictionaries/nouns.xml",
    "data/dictionaries/verbs.xml",
    "data/grammar/contexts.xml",
    "data/grammar/grammar_rules.xml",
    "data/lessons/lessons.xml",
    "data/patterns/sentence_maps.xml",
    "data/patterns/sentence_quizzes.xml",
    "data/quiz_project.xml",
]
CONTENT_SOURCE_FILES = {
    path.removeprefix("data/")
    for path in CONTENT_MANIFEST_ORDER
    if path != "data/content_revision.json"
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
VALID_POLARITIES = {"affirmative", "negative"}
WORD_FORM_ATTRIBUTES = {
    "ref",
    "translation",
    "kana",
    "kanji",
    "romaji",
}
FORM_DEFINITION_ATTRIBUTES = {
    "name",
    "label",
    "lesson_name",
    "context",
    "polarity",
    "register",
}


def validate_polarity_pair(
    schema: str,
    context: str,
    register: str,
    polarities: set[str],
) -> None:
    """Validate one polarity pair derived from context and register."""

    if polarities != VALID_POLARITIES:
        raise AssertionError(
            f"Form catalog {schema} must define exactly one affirmative "
            f"and one negative form for context {context} and register "
            f"{register}"
        )


def unexpected_word_form_attributes(attributes: object) -> set[str]:
    """Return attributes that do not belong in a word-local form value."""

    return set(attributes) - WORD_FORM_ATTRIBUTES


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

    for retired in ("database_revision.json", "database_update_manifest.json"):
        if (ROOT / retired).exists():
            raise AssertionError(f"Retired Database artifact is still present: {retired}")


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
        elif root.get("schema_version") != "4":
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
    expected_references = PROJECT_SCHEMA_FILES - {"quiz_project.xml"}
    if references != expected_references:
        raise AssertionError(
            "quiz_project.xml reference inventory mismatch, "
            f"missing={sorted(expected_references - references)}, "
            f"extra={sorted(references - expected_references)}"
        )
    for relative in sorted(references):
        if not relative or not (manifest_path.parent / relative).is_file():
            raise AssertionError(f"quiz_project.xml references missing file: {relative}")


def validate_shared_grammar_dependencies() -> None:
    grammar = ET.parse(ROOT / "grammar" / "grammar_rules.xml").getroot()
    contexts = ET.parse(ROOT / "grammar" / "contexts.xml").getroot()
    defined_roles = {
        value for node in grammar.findall("./roles/role")
        for value in [node.get("id")] if value
    }
    defined_categories = {
        value for node in grammar.findall("./noun_categories/category")
        for value in [node.get("id")] if value
    }
    defined_features = {
        value for node in grammar.findall("./features/feature")
        for value in [node.get("id")] if value
    }
    defined_contexts = {
        value for node in contexts.findall("./context")
        for value in [node.get("id")] if value
    }
    dictionary_roots = [
        (path, ET.parse(path).getroot())
        for path in sorted((ROOT / "dictionaries").glob("*.xml"))
    ]
    form_catalogs: dict[str, set[str]] = {}
    form_polarities: set[str] = set()
    for catalog in grammar.findall("./form_catalogs/form_catalog"):
        schema = str(catalog.get("schema", "")).strip()
        if not schema:
            raise AssertionError("form_catalog must define schema")
        if schema in form_catalogs:
            raise AssertionError(f"Duplicate form catalog for schema: {schema}")
        names: set[str] = set()
        lesson_names: set[str] = set()
        polarity_targets: set[tuple[str, str, str]] = set()
        polarity_pairs: dict[tuple[str, str], set[str]] = {}
        for node in catalog.findall("./form"):
            unexpected = set(node.attrib) - FORM_DEFINITION_ATTRIBUTES
            if unexpected:
                raise AssertionError(
                    f"Grammar form {schema} contains unsupported attributes: "
                    f"{sorted(unexpected)}"
                )
            name = str(node.get("name", "")).strip()
            if not name:
                raise AssertionError(
                    f"form_catalog {schema} contains form without name"
                )
            if name in names:
                raise AssertionError(
                    f"Duplicate grammar form in {schema}: {name}"
                )
            names.add(name)
            label = str(node.get("label", "")).strip()
            if not label:
                raise AssertionError(
                    f"Grammar form {schema}/{name} must define label"
                )
            lesson_name = str(node.get("lesson_name", "")).strip() or name
            if lesson_name in lesson_names:
                raise AssertionError(
                    f"Form catalog {schema} defines duplicate lesson name: "
                    f"{lesson_name}"
                )
            lesson_names.add(lesson_name)
            context = str(node.get("context", "none")).strip() or "none"
            if context not in defined_contexts:
                raise AssertionError(
                    f"Grammar form {schema}/{name} references unknown "
                    f"context: {context}"
                )
            polarity = str(node.get("polarity", "")).strip()
            if polarity and polarity not in VALID_POLARITIES:
                raise AssertionError(
                    f"Grammar form {schema}/{name} has invalid polarity: "
                    f"{polarity}"
                )
            if polarity:
                form_polarities.add(polarity)
            register = str(node.get("register", "")).strip()
            if register and register not in {"plain", "polite"}:
                raise AssertionError(
                    f"Grammar form {schema}/{name} has invalid register: "
                    f"{register}"
                )
            finite_metadata = (
                context != "none"
                or bool(polarity)
                or bool(register)
            )
            if finite_metadata and not (
                context != "none"
                and polarity
                and register
            ):
                raise AssertionError(
                    f"Grammar form {schema}/{name} must define context, "
                    "polarity, and register together"
                )
            if context != "none" and polarity and register:
                target = (context, register, polarity)
                if target in polarity_targets:
                    raise AssertionError(
                        f"Form catalog {schema} defines more than one "
                        f"{polarity} form for context {context} and "
                        f"register {register}"
                    )
                polarity_targets.add(target)
                pair = polarity_pairs.setdefault(
                    (context, register),
                    set(),
                )
                pair.add(polarity)
        for (context, register), polarities in polarity_pairs.items():
            validate_polarity_pair(
                schema,
                context,
                register,
                polarities,
            )
        form_catalogs[schema] = names
    defined_cases = {
        attribute
        for _path, dictionary in dictionary_roots
        for cases in dictionary.findall(".//cases")
        for attribute in cases.attrib
        if attribute != "language"
    }
    noun_case_by_form = grammar.find("./noun_case_by_form")
    if noun_case_by_form is None:
        raise AssertionError("grammar_rules.xml must define noun_case_by_form")
    mappings = noun_case_by_form.findall("./map")
    if not mappings:
        raise AssertionError("noun_case_by_form must contain mappings")
    mapped_polarities: set[str] = set()
    for mapping in mappings:
        unexpected = set(mapping.attrib) - {"polarity", "case_ref"}
        if unexpected:
            raise AssertionError(
                "noun_case_by_form mapping contains unsupported attributes: "
                f"{sorted(unexpected)}"
            )
        polarity = str(mapping.get("polarity", "")).strip()
        case_ref = str(mapping.get("case_ref", "")).strip()
        if polarity not in VALID_POLARITIES:
            raise AssertionError(
                f"noun_case_by_form uses invalid polarity: {polarity}"
            )
        if polarity not in form_polarities:
            raise AssertionError(
                f"noun_case_by_form references unused polarity: {polarity}"
            )
        if polarity in mapped_polarities:
            raise AssertionError(
                f"noun_case_by_form maps polarity more than once: {polarity}"
            )
        if case_ref not in defined_cases:
            raise AssertionError(
                f"noun_case_by_form references unknown noun case: {case_ref}"
            )
        mapped_polarities.add(polarity)

    for path, dictionary in dictionary_roots:
        schema = str(dictionary.get("schema", "")).strip()
        catalog = form_catalogs.get(schema, set())
        word_forms = dictionary.findall("./words/word/forms/form")
        if word_forms and not catalog:
            raise AssertionError(
                f"{path.name} defines word forms but schema '{schema}' "
                "has no grammar form catalog"
            )
        if dictionary.find("./editor/forms") is not None:
            raise AssertionError(
                f"{path.name} must not define editor forms; use grammar form catalog"
            )
        for form in word_forms:
            ref = str(form.get("ref", "")).strip()
            if not ref:
                raise AssertionError(
                    f"{path.name} word form must use ref"
                )
            if ref not in catalog:
                raise AssertionError(
                    f"{path.name} references unknown {schema} form: {ref}"
                )
            unexpected = unexpected_word_form_attributes(form.attrib)
            if unexpected:
                raise AssertionError(
                    f"{path.name} form {ref} contains unsupported attributes: "
                    f"{sorted(unexpected)}"
                )
            if (form.text or "").strip():
                raise AssertionError(
                    f"{path.name} form {ref} must store Japanese values in "
                    "attributes, not element text"
                )
        for role in dictionary.findall(".//usage/role"):
            ref = role.get("ref")
            if ref and ref not in defined_roles:
                raise AssertionError(f"{path.name} references unknown role: {ref}")
            for category in (role.get("accepts") or "").split():
                if category != "*" and category not in defined_categories:
                    raise AssertionError(
                        f"{path.name} role {ref} references unknown category: {category}"
                    )
        for feature in dictionary.findall(".//features/feature"):
            ref = feature.get("ref")
            if ref and ref not in defined_features:
                raise AssertionError(f"{path.name} references unknown feature: {ref}")


def validate_composite_case_scopes() -> None:
    root = ET.parse(ROOT / "patterns" / "sentence_maps.xml").getroot()
    for pattern in root.findall("./sentence_patterns/sentence_pattern"):
        patterns = pattern.find("patterns")
        if patterns is None:
            continue
        case_scope = str(patterns.get("case_scope", "outer"))
        if case_scope not in {"outer", "embedded"}:
            pattern_id = str(pattern.get("id", "<missing>"))
            raise AssertionError(
                f"Sentence pattern {pattern_id} uses invalid case_scope: {case_scope}"
            )


def validate_lesson_references() -> None:
    project_root = ET.parse(ROOT / "quiz_project.xml").getroot()
    dictionary_files = {
        str(node.get("id", "")): str(node.get("file", ""))
        for node in project_root.findall("./dictionaries/dictionary")
    }
    dictionary_words: dict[str, set[str]] = {}
    for dictionary_id, relative in dictionary_files.items():
        if not dictionary_id or not relative:
            raise AssertionError("quiz_project.xml contains an incomplete dictionary entry")
        dictionary_root = ET.parse(ROOT / relative).getroot()
        dictionary_words[dictionary_id] = {
            str(word.get("id", ""))
            for word in dictionary_root.findall("./words/word")
            if word.get("id")
        }

    lessons_root = ET.parse(ROOT / LESSON_SCHEMA_FILE).getroot()
    for lesson in lessons_root.findall("./lessons/lesson"):
        lesson_id = str(lesson.get("id", "")) or "<missing>"
        references = lesson.findall("./word/dictionary_ref")
        if lesson.get("group") == "Tematyczne":
            if lesson.findall("./local_word"):
                raise AssertionError(
                    f"Thematic lesson {lesson_id} must contain dictionary references only"
                )
            if len(references) < 6:
                raise AssertionError(
                    f"Thematic lesson {lesson_id} must contain at least six words"
                )
        for reference in references:
            dictionary_id = str(reference.get("dictionary", ""))
            word_id = str(reference.get("word", ""))
            if dictionary_id not in dictionary_words:
                raise AssertionError(
                    f"Lesson {lesson_id} references unknown dictionary: {dictionary_id}"
                )
            if word_id not in dictionary_words[dictionary_id]:
                raise AssertionError(
                    f"Lesson {lesson_id} references missing word "
                    f"{dictionary_id}:{word_id}"
                )


def validate_content_manifest() -> None:
    revision = load_json(ROOT / "content_revision.json")
    manifest = load_json(ROOT / "content_update_manifest.json")

    if revision.get("format") != 1 or manifest.get("format") != 1:
        raise AssertionError("Content revision and manifest must use format 1")
    revision_number = revision.get("revision")
    if (
        not isinstance(revision_number, int)
        or isinstance(revision_number, bool)
        or revision_number <= 0
    ):
        raise AssertionError("Content revision must be a positive integer")
    if manifest.get("revision") != revision_number:
        raise AssertionError(
            "Content manifest revision must match content_revision.json"
        )

    entries = manifest.get("files")
    if not isinstance(entries, list):
        raise AssertionError("Content manifest files must be a list")
    install_paths = [
        str(entry.get("path", ""))
        for entry in entries
        if isinstance(entry, dict)
    ]
    if len(install_paths) != len(entries):
        raise AssertionError("Content manifest file entries must be objects")
    if install_paths != CONTENT_MANIFEST_ORDER:
        raise AssertionError(
            "Content manifest must contain the complete declarative project "
            f"snapshot in canonical order: {CONTENT_MANIFEST_ORDER}"
        )

    source_paths = {
        validate_manifest_file(raw_entry, "data/")
        for raw_entry in entries
    }
    expected_sources = {
        (ROOT / relative).resolve() for relative in CONTENT_SOURCE_FILES
    } | {(ROOT / "content_revision.json").resolve()}
    if source_paths != expected_sources:
        raise AssertionError("Content manifest inventory does not match Content files")


def package_files(package_dir: Path) -> set[Path]:
    return {
        path.resolve()
        for path in package_dir.rglob("*")
        if path.is_file() and "__pycache__" not in path.parts
    }


def validate_quiz_manifest() -> None:
    manifest = load_json(ROOT / "quiz_update_manifest.json")
    if manifest.get("format") != 1 or manifest.get("channel") != "quizzes":
        raise AssertionError("Quiz manifest must use format 1 and channel 'quizzes'")

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
            compile(python_file.read_text(encoding="utf-8"), str(python_file), "exec")

    manifest_paths: set[str] = set()
    for raw_entry in entries:
        if not isinstance(raw_entry, dict):
            raise AssertionError("Quiz manifest file entries must be objects")
        install_path = str(raw_entry.get("path", ""))
        if install_path in manifest_paths:
            raise AssertionError(f"Duplicate Quiz manifest path: {install_path}")
        if not install_path.startswith("apps/"):
            raise AssertionError(
                f"Quiz manifest may contain executable packages only: {install_path}"
            )
        manifest_paths.add(install_path)
        source = validate_manifest_file(raw_entry, "apps/")
        if not source.relative_to(ROOT).as_posix().startswith("quizzes/"):
            raise AssertionError(
                f"Quiz package URL must resolve below quizzes/: {install_path}"
            )

    if manifest_paths != catalog_paths:
        raise AssertionError("Quiz manifest must contain exactly its package files")
    ordered_paths = [str(entry["path"]) for entry in entries]
    if ordered_paths != sorted(ordered_paths):
        raise AssertionError("Quiz manifest file entries must be sorted by install path")


def main() -> None:
    validate_repository_layout()
    validate_xml_and_schemas()
    validate_project_references()
    validate_shared_grammar_dependencies()
    validate_composite_case_scopes()
    validate_lesson_references()
    validate_content_manifest()
    validate_quiz_manifest()
    print("Kotomi-Data validation passed")


if __name__ == "__main__":
    main()
