# Kotomi Data

This repository contains Kotomi's public Content snapshot and distributable quiz packages.

The two public update channels have deliberately different responsibilities. **Content Update** publishes the complete declarative learning and sentence-generation project as one compatible revision. **Quiz Update** publishes executable quiz packages only.

## Layout

| Path | Purpose | Update channel |
| --- | --- | --- |
| `quiz_project.xml` | Canonical Schema 2 project entrypoint. | Content |
| `dictionaries/` | Complete dictionary entries, including Japanese and source lexical values. | Content |
| `grammar/` | Context options, lexical counter bindings and number sets. | Content |
| `patterns/` | Sentence maps and sentence-quiz definitions. | Content |
| `lessons/` | Schema 4 lesson catalog. | Content |
| `quizzes/` | Published first-party executable quiz package files. | Quiz |
| `tools/` | Repository validation and maintenance helpers. | Repository only |
| `content_revision.json` | Identity of the published Content snapshot. | Content |
| `content_update_manifest.json` | Atomic Content update inventory. | Content |
| `quiz_update_manifest.json` | Executable quiz package inventory. | Quiz |

A Kotomi installation mirrors declarative content below `data/` and executable quiz packages below `apps/`. For example, `dictionaries/verbs.xml` is installed as `data/dictionaries/verbs.xml`, while `quizzes/verbs/logic.py` is installed as `apps/verbs/logic.py`.

## Content Update

Content Update owns one semantic snapshot:

```text
quiz_project.xml
dictionaries/**
grammar/**
patterns/**
lessons/**
content_revision.json
```

The published manifest is `content_update_manifest.json`. These files are intentionally versioned together because they reference one another. Dictionaries and patterns reference grammar IDs supplied by the compatible Kotomi version, plus contexts and other words from this Content revision. Updating only one side could create a project that loads but cannot generate valid sentences.

Advance `content_revision.json` when publishing a new official Content state. SHA-256 hashes decide which individual files need downloading, while the integer revision identifies the complete compatible snapshot. Installation is atomic at the manifest level.

## Quiz Update

Quiz Update owns executable packages only:

```text
quizzes/** -> installed as apps/**
```

The published manifest is `quiz_update_manifest.json`. It must not contain `data/**` entries.

The package files below `quizzes/` are generated from the private Kotomi repository's `apps/` directory and should not be edited independently. From a Kotomi checkout with this repository mounted as its `data` submodule, publish the current Quiz catalog with:

```text
python tools/updates/publish_quiz_packages.py 1.1.1
```

The Quiz catalog version is independent from the Content revision.

## Project entrypoint

Kotomi opens `data/quiz_project.xml`. References inside the project file are relative to that file, so dictionaries, grammar, contexts, patterns, and sentence-quiz definitions form one project without special runtime lookup rules.

The project/pattern files use Schema 2. The lesson catalog uses Schema 4.

## Counting data

Schema 2 keeps semantic numbers and counters as separate selections. The dictionaries provide lexical numbers 1 through 10 plus 20, exact counter realizations for 人, 匹, 本, 枚, 冊, 台, 個, 時, 分, 歳 and 階, and the symbolic how_many quantity. All full-quantity irregulars, including 20歳 as はたち, are stored explicitly. Grammar owns the generated numeric domain, terminal digit/unit counter composition, Polish source count profiles with periodic suffix mappings, and named lexical number sets. Generated ranges expose value/kana/kanji/romaji rather than synthesized Polish number words.

## Publishing changes

When changing any declarative project or learning content:

1. Edit the required dictionaries, lessons, grammar, contexts, patterns, or project declaration together.
2. Advance `content_revision.json` for the new official Content state.
3. Regenerate `content_update_manifest.json` from the Kotomi tooling.
4. Run `python tools/validate_repository.py`.
5. Commit the complete Content snapshot and manifest together.

When changing first-party executable quiz package code:

1. Make the package source change in the Kotomi repository under `apps/`.
2. Run `python tools/updates/publish_quiz_packages.py <catalog-version>` from the Kotomi checkout.
3. Run `python tools/validate_repository.py` in this repository.
4. Commit the generated Quiz publication together.

Do not put declarative `data/**` project files into the Quiz manifest.

## Validation

Run:

```text
python tools/validate_repository.py
```

CI runs the same validation for pull requests and `main`. The validator checks canonical layout, XML schemas, project references, shared grammar dependencies, hashes, Content inventory, package inventories, Quiz package-only ownership, and manifest ordering.

## Kotomi integration

The Kotomi source repository mounts this repository as the `data` git submodule. Desktop builds and mobile packages include the complete Content snapshot plus the separately owned executable quiz packages required for a fresh installation.

## Content and Kotomi grammar

A dictionary contains complete word entries: Japanese surfaces, translations,
lexical forms, cases and assignments to grammar IDs. One edit has one dictionary
owner. Grammar selection never selects a different Content database. Default
uses opaque source text; Polish enables optional enrichment on the same Word.
Switching grammar is non-destructive and does not mutate Content. Test-only
providers and fixtures are not published in this repository.

Kotomi provides form catalogs, roles/categories/features, agreement templates,
government frames, noun relation profiles, source clitics and counting rules.
Content references these IDs but does not define grammar or Studio field schemas.
`grammar/counting.xml` contains lexical counter bindings and learning number sets;
contexts, patterns, quizzes and lessons also remain Content.

`quiz_project.xml` declares `min_kotomi_version="1.2"`. The update manifest copies
this requirement automatically. Compatible Kotomi versions have the same major
and a minor at least as high; patch is ignored. Thus 1.1.3 and 2.0.0 cannot install
Content requiring 1.2, while 1.2.0 and 1.3.0 can. Current Content requires 1.4. No separate grammar version is maintained.

Data CI validates lexical structure and local references. Kotomi's integration
suite validates these references against the shipped grammar using its pinned
Data commit, so Data does not maintain a duplicate grammar registry.
