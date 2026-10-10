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
    "dictionaries/adverbs.xml",
    "dictionaries/demonstratives.xml",
    "dictionaries/expressions.xml",
    "dictionaries/connectors.xml",
    "dictionaries/copulas.xml",
    "dictionaries/counters.xml",
    "dictionaries/interrogatives.xml",
    "dictionaries/nouns.xml",
    "dictionaries/numbers.xml",
    "dictionaries/verbs.xml",
    "grammar/contexts.xml",
    "grammar/counting.xml",
    "patterns/sentence_maps.xml",
    "patterns/sentence_quizzes.xml",
}
LESSON_SCHEMA_FILE = "lessons/lessons.xml"
LEARNING_XML_FILES = PROJECT_SCHEMA_FILES | {LESSON_SCHEMA_FILE}
CONTENT_MANIFEST_ORDER = [
    "data/content_revision.json",
    "data/dictionaries/adjectives.xml",
    "data/dictionaries/adverbs.xml",
    "data/dictionaries/connectors.xml",
    "data/dictionaries/copulas.xml",
    "data/dictionaries/counters.xml",
    "data/dictionaries/demonstratives.xml",
    "data/dictionaries/expressions.xml",
    "data/dictionaries/interrogatives.xml",
    "data/dictionaries/nouns.xml",
    "data/dictionaries/numbers.xml",
    "data/dictionaries/verbs.xml",
    "data/grammar/contexts.xml",
    "data/grammar/counting.xml",
    "data/lessons/lessons.xml",
    "data/patterns/sentence_maps.xml",
    "data/patterns/sentence_quizzes.xml",
    "data/quiz_project.xml",
]
CONTENT_MANIFEST_ORDER.sort(key=str.casefold)
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
WORD_FORM_ATTRIBUTES = {
    "ref",
    "translation",
    "kana",
    "kanji",
    "romaji",
}

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
            if root.get("schema_version") != "2":
                raise AssertionError(f"{relative} must use project/pattern Schema 2")
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


def validate_content_grammar_boundary() -> None:
    """Grammar IDs resolve against Kotomi in its integration suite, not a duplicate registry here."""
    forbidden = {"form_catalogs", "agreement_catalogs", "noun_case_by_form", "polish_government",
                 "polish_noun_relations", "polish_clitics", "count_source_profiles",
                 "number_composition", "counter_composition_profiles", "counting_classes", "editor"}
    for path in ROOT.rglob("*.xml"):
        root = ET.parse(path).getroot()
        for node in root.iter():
            if node.tag in forbidden or "shared_target" in node.attrib:
                raise AssertionError(f"{path}: grammar definition {node.tag} does not belong in Content")
        if root.tag == "dictionary":
            for word in root.findall("./words/word"):
                if not all(word.get(key) for key in ("id", "translation", "kana")):
                    raise AssertionError(f"{path}: words must contain complete lexical data")
                for form in word.findall("./forms/form"):
                    if not form.get("ref") or unexpected_word_form_attributes(form.attrib):
                        raise AssertionError(f"{path}: forms must reference a Kotomi grammar ID")
        if root.tag == "quiz_project":
            if not root.get("min_kotomi_version") or root.find("grammar") is not None:
                raise AssertionError(f"{path}: Content must declare its minimum Kotomi version")


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


def validate_lesson_references(root: Path | None = None) -> None:
    root = ROOT if root is None else root
    project_root = ET.parse(root / "quiz_project.xml").getroot()
    dictionary_files = {
        str(node.get("id", "")): str(node.get("file", ""))
        for node in project_root.findall("./dictionaries/dictionary")
    }
    dictionary_words: dict[str, set[str]] = {}
    for dictionary_id, relative in dictionary_files.items():
        if not dictionary_id or not relative:
            raise AssertionError("quiz_project.xml contains an incomplete dictionary entry")
        dictionary_root = ET.parse(root / relative).getroot()
        dictionary_words[dictionary_id] = {
            str(word.get("id", ""))
            for word in dictionary_root.findall("./words/word")
            if word.get("id")
        }

    lessons_root = ET.parse(root / LESSON_SCHEMA_FILE).getroot()
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


def validate_context_references(root: Path | None = None) -> None:
    """Check lexical references without depending on the application's engine."""
    root = ROOT if root is None else root
    manifest = ET.parse(root / "quiz_project.xml").getroot()
    dictionaries = {
        node.get("id"): {word.get("id") for word in ET.parse(root / node.get("file")).getroot().findall("./words/word")}
        for node in manifest.findall("./dictionaries/dictionary")
    }
    contexts = ET.parse(root / "grammar/contexts.xml").getroot()
    for option in contexts.findall("./context/option"):
        dictionary, word = option.get("dictionary", ""), option.get("word", "")
        if bool(dictionary) != bool(word):
            raise AssertionError("Context reference requires dictionary and word together")
        if dictionary:
            if option.get("kana") or option.get("translation"):
                raise AssertionError("Context reference cannot mix inline lexical text")
            if word not in dictionaries.get(dictionary, set()):
                raise AssertionError(f"Context references missing word {dictionary}:{word}")
        elif option.get("kana_suffix") or option.get("translation_suffix"):
            raise AssertionError("Context suffixes require a word reference")


def validate_counting_data() -> None:
    """Validate the complete Schema 2 counting acceptance inventory."""

    numbers = ET.parse(ROOT / "dictionaries" / "numbers.xml").getroot()
    counters = ET.parse(ROOT / "dictionaries" / "counters.xml").getroot()
    nouns = ET.parse(ROOT / "dictionaries" / "nouns.xml").getroot()
    interrogatives = ET.parse(
        ROOT / "dictionaries" / "interrogatives.xml"
    ).getroot()
    counting_grammar = ET.parse(ROOT / "grammar" / "counting.xml").getroot()
    patterns = ET.parse(ROOT / "patterns" / "sentence_maps.xml").getroot()

    if counting_grammar.get("source_language"):
        raise AssertionError("Content counter bindings are not source grammar")
    number_values: dict[int, str] = {}
    for word in numbers.findall("./words/word"):
        word_id = str(word.get("id", ""))
        try:
            value = int(str(word.get("value", "")))
        except ValueError as exc:
            raise AssertionError(f"Number {word_id} has invalid value") from exc
        if value in number_values:
            raise AssertionError(f"Duplicate number value: {value}")
        number_values[value] = word_id
    missing_values = (set(range(1, 11)) | {20}) - set(number_values)
    if missing_values:
        raise AssertionError(
            f"Counting numbers are missing values: {sorted(missing_values)}"
        )

    quantity_sources = {
        str(word.get("quantity_symbol", "")): str(word.get("id", ""))
        for word in interrogatives.findall("./words/word")
        if word.get("quantity_symbol")
    }
    if quantity_sources.get("how_many") != "how_many":
        raise AssertionError(
            "Interrogative how_many must expose quantity_symbol='how_many'"
        )

    class_ids = {
        str(node.get("ref", ""))
        for node in counting_grammar.findall("./counter_bindings/class")
    }
    required_classes = {
        "person", "small_animal", "long_object", "flat_object",
        "bound_volume", "machine", "small_object",
    }
    if not required_classes.issubset(class_ids):
        raise AssertionError(
            "Missing counting classes: "
            + ", ".join(sorted(required_classes - class_ids))
        )

    counter_words = {
        str(word.get("id", "")): word
        for word in counters.findall("./words/word")
    }
    if any(word.find("./counts") is not None for word in counter_words.values()):
        raise AssertionError(
            "Counter compatibility must be defined only in counting.xml"
        )
    required_counters = {
        "nin", "hiki", "hon", "mai", "satsu", "dai", "ko",
        "ji", "fun", "sai", "kai", "kai_times",
    }
    if not required_counters.issubset(counter_words):
        raise AssertionError(
            "Missing counters: "
            + ", ".join(sorted(required_counters - set(counter_words)))
        )
    counters_by_class: dict[str, set[str]] = {}
    defaults_by_class: dict[str, str] = {}
    for class_node in counting_grammar.findall("./counter_bindings/class"):
        class_id = str(class_node.get("ref", ""))
        refs = [
            str(counter.get("ref", ""))
            for counter in class_node.findall("./counter")
        ]
        default_counter = str(class_node.get("default_counter", ""))
        if not refs:
            raise AssertionError(f"Counting class {class_id} has no counters")
        if len(refs) != len(set(refs)):
            raise AssertionError(
                f"Counting class {class_id} repeats a counter reference"
            )
        if default_counter not in refs:
            raise AssertionError(
                f"Counting class {class_id} has invalid default counter"
            )
        unknown = set(refs) - set(counter_words)
        if unknown:
            raise AssertionError(
                f"Counting class {class_id} references unknown counters: "
                + ", ".join(sorted(unknown))
            )
        counters_by_class[class_id] = set(refs)
        defaults_by_class[class_id] = default_counter
    for counter_id in required_counters:
        word = counter_words[counter_id]
        composition = word.find("./composition")
        if (
            composition is None
            or not composition.get("profile")
        ):
            raise AssertionError(
                f"Counter {counter_id} needs a valid composition profile"
            )
        if counter_id == "kai_times":
            continue
        identities = {
            ("number", str(node.get("number")))
            if node.get("number") is not None
            else ("symbol", str(node.get("symbol")))
            for node in word.findall("./quantity_realizations/realization")
        }
        required = {("number", str(value)) for value in range(1, 11)}
        required.add(("symbol", "how_many"))
        if not required.issubset(identities):
            raise AssertionError(
                f"Counter {counter_id} lacks required 1..10/how_many data"
            )
    sai_twenty = counter_words["sai"].find(
        "./quantity_realizations/realization[@number='20']"
    )
    if sai_twenty is None or sai_twenty.get("kana") != "はたち":
        raise AssertionError("Counter sai must realize 20 exactly as はたち")
    kai_times = counter_words.get("kai_times")
    kai_times_composition = (
        kai_times.find("./composition") if kai_times is not None else None
    )
    if (
        kai_times_composition is None
        or kai_times_composition.get("profile") != "kai_times"
    ):
        raise AssertionError(
            "Counter kai_times must use its dedicated composition profile"
        )
    kai_times_hundred = (
        kai_times.find(
            "./quantity_realizations/realization[@number='100']"
        )
        if kai_times is not None else None
    )
    if (
        kai_times_hundred is None
        or kai_times_hundred.get("kana") != "ひゃっかい"
        or kai_times_hundred.get("kanji") != "百回"
        or kai_times_hundred.get("romaji") != "hyakkai"
    ):
        raise AssertionError(
            "Counter kai_times must realize 100 exactly as ひゃっかい / 百回"
        )
    kai_times_question = (
        kai_times.find(
            "./quantity_realizations/realization[@symbol='how_many']"
        )
        if kai_times is not None else None
    )
    if (
        kai_times_question is None
        or kai_times_question.get("kana") != "なんかい"
        or kai_times_question.get("kanji") != "何回"
    ):
        raise AssertionError(
            "Counter kai_times must realize how_many as なんかい / 何回"
        )

    counted_classes: set[str] = set()
    for word in nouns.findall("./words/word"):
        counting = word.find("./counting")
        if counting is None:
            continue
        classes = set(str(counting.get("classes", "")).split())
        unknown = classes - class_ids
        if unknown:
            raise AssertionError(
                f"Noun {word.get('id')} uses unknown counting classes: "
                + ", ".join(sorted(unknown))
            )
        counted_classes.update(classes)
        preferred = str(counting.get("preferred_counter", ""))
        defaults = {
            defaults_by_class[class_id]
            for class_id in classes
            if defaults_by_class.get(class_id)
        }
        if len(defaults) > 1 and not preferred:
            raise AssertionError(
                f"Noun {word.get('id')} has ambiguous class defaults and "
                "must declare preferred_counter"
            )
        compatible = set().union(*(
            counters_by_class.get(class_id, set()) for class_id in classes
        )) if classes else set()
        if preferred and preferred not in compatible:
            raise AssertionError(
                f"Noun {word.get('id')} uses incompatible preferred counter {preferred}"
            )
        if counting.find("./source_forms/form[@profile='one']") is not None:
            raise AssertionError(
                f"Noun {word.get('id')} duplicates one instead of noun_case fallback"
            )
    if not required_classes.issubset(counted_classes):
        raise AssertionError(
            "No noun example for classes: "
            + ", ".join(sorted(required_classes - counted_classes))
        )

    pattern_ids = {
        str(node.get("id", ""))
        for node in patterns.findall("./sentence_patterns/sentence_pattern")
    }
    required_patterns = {
        "Istnienie policzonych rzeczowników",
        "Ile jest policzonych rzeczowników",
        "Godzina zegarowa", "Wiek", "Ile razy w miesiącu",
        "Liczba razy w miesiącu", "Numer piętra",
    }
    if not required_patterns.issubset(pattern_ids):
        raise AssertionError(
            "Missing counting patterns: "
            + ", ".join(sorted(required_patterns - pattern_ids))
        )
    retired_patterns = {
        "Rozpoznaj liczbę z 匹",
        "Wybierz counter dla rzeczownika",
        "Trzy minuty",
        "Wiek dwadzieścia lat",
    }
    if retired_patterns & pattern_ids:
        raise AssertionError(
            "Retired counting patterns remain: "
            + ", ".join(sorted(retired_patterns & pattern_ids))
        )

    patterns_by_id = {
        str(node.get("id", "")): node
        for node in patterns.findall("./sentence_patterns/sentence_pattern")
    }
    existential = patterns_by_id["Istnienie policzonych rzeczowników"]
    existential_text = "".join(existential.itertext())
    required_fragments = {
        "role:subject",
        "feature:existential",
        "agree:@count",
        "quantity:@count",
        "counts:@item, preferred",
    }
    if not required_fragments.issubset(set(
        fragment
        for fragment in required_fragments
        if fragment in existential_text
    )):
        raise AssertionError(
            "Generic existential counting pattern is missing a data-driven "
            "dependency."
        )
    forbidden = ("id:iru", "id:aru", "id:hiki", "id:satsu", "id:dai", "いる", "ある")
    if any(value in existential_text for value in forbidden):
        raise AssertionError(
            "Generic existential counting pattern hardcodes a verb or counter."
        )
    query_answer = patterns_by_id[
        "Ile jest policzonych rzeczowników"
    ].findtext("answer", default="")
    if "role:subject" not in query_answer or "id:iru" in query_answer:
        raise AssertionError(
            "Count question must resolve its existential verb through role data."
        )
    query_question = patterns_by_id[
        "Ile jest policzonych rzeczowników"
    ].findtext("question", default="")
    if "interrogative@amount[asks_for:count]" not in query_question:
        raise AssertionError(
            "Count question must select its interrogative semantically."
        )
    age = patterns_by_id["Wiek"]
    if "range:1..150" not in age.findtext("question", default=""):
        raise AssertionError(
            "Age pattern must use the generated range 1..150."
        )
    frequency_answer = patterns_by_id[
        "Ile razy w miesiącu"
    ].findtext("answer", default="")
    if "id:kai_times" not in frequency_answer or "一か月に" not in frequency_answer:
        raise AssertionError(
            "Monthly frequency pattern must use the dedicated 回 counter."
        )
    numeric_frequency = patterns_by_id["Liczba razy w miesiącu"]
    numeric_frequency_question = numeric_frequency.findtext(
        "question", default=""
    )
    numeric_frequency_answer = numeric_frequency.findtext(
        "answer", default=""
    )
    if "range:1..500" not in numeric_frequency_question:
        raise AssertionError(
            "Numeric monthly frequency must use generated range 1..500."
        )
    if (
        "id:kai_times" not in numeric_frequency_answer
        or "quantity:@count" not in numeric_frequency_answer
        or ".kanji" not in numeric_frequency_answer
    ):
        raise AssertionError(
            "Numeric monthly frequency must render generated 回 quantities."
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
    validate_content_grammar_boundary()
    validate_composite_case_scopes()
    validate_lesson_references()
    validate_context_references()
    validate_counting_data()
    validate_content_manifest()
    validate_quiz_manifest()
    print("Kotomi-Data validation passed")


if __name__ == "__main__":
    main()
