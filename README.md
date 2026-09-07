# Kotomi Data

This repository contains the public learning database and distributable quiz content used by Kotomi.

The root is intentionally kept small. Files at the root are repository contracts or update entrypoints. Content is grouped by responsibility below them.

## Layout

| Path | Purpose | Update channel |
| --- | --- | --- |
| `quiz_project.xml` | Canonical Schema 1 project entrypoint. | Quiz |
| `dictionaries/` | Word dictionaries for verbs, nouns, adjectives, and copulas. | Database |
| `grammar/` | Grammar definitions and reusable context pools. | Quiz |
| `patterns/` | Sentence maps and sentence-quiz definitions. | Quiz |
| `lessons/` | Schema 4 lesson catalog. | Database |
| `quizzes/` | Published first-party quiz package files. | Quiz |
| `tools/` | Repository validation and maintenance helpers. | Repository only |
| `database_revision.json` | Identity of the published Database state. | Database |
| `database_update_manifest.json` | Database update inventory. | Database |
| `quiz_update_manifest.json` | Quiz package and Studio-content inventory. | Quiz |

A Kotomi installation mirrors public content below its `data/` and `apps/` directories. For example, `dictionaries/verbs.xml` is installed as `data/dictionaries/verbs.xml`, while `quizzes/verbs/logic.py` is installed as `apps/verbs/logic.py`.

## Update ownership

The update channels intentionally have non-overlapping ownership.

### Database Update

Database Update owns only:

```text
dictionaries/**
lessons/**
database_revision.json
```

The published manifest is `database_update_manifest.json`. A Database publication must not include `quiz_project.xml`, `grammar/**`, or `patterns/**`.

Advance `database_revision.json` when publishing a new official Database state. SHA-256 hashes decide which individual files are downloaded, while the integer revision identifies the published state.

### Quiz Update

Quiz Update owns:

```text
quizzes/**              -> installed as apps/**
quiz_project.xml        -> installed as data/quiz_project.xml
grammar/**              -> installed as data/grammar/**
patterns/**             -> installed as data/patterns/**
```

The published manifest is `quiz_update_manifest.json`.

The package files below `quizzes/` are generated from the private Kotomi repository's `apps/` directory and should not be edited independently. The same publication step also adds the current Studio/project XML to the Quiz manifest.

From a Kotomi checkout with this repository mounted as its `data` submodule, publish the current Quiz catalog with:

```text
python tools/updates/publish_quiz_packages.py 1.1.1
```

The catalog version is independent from the Database revision.

## Project entrypoint

Kotomi opens `data/quiz_project.xml`. References inside the project file are relative to that file, so dictionaries and supporting XML can live in their own directories without special runtime lookup rules.

The project/pattern files use Schema 1. The lesson catalog uses Schema 4.

## Publishing changes

When changing dictionaries or lessons:

1. Edit the Database-owned content.
2. Advance `database_revision.json` when publishing a new official Database state.
3. Regenerate `database_update_manifest.json` from the Kotomi tooling.
4. Run `python tools/validate_repository.py`.
5. Commit the content and manifest together.

When changing `quiz_project.xml`, `grammar/**`, `patterns/**`, or first-party quiz package code:

1. Make the source change in the appropriate repository.
2. Run `python tools/updates/publish_quiz_packages.py <catalog-version>` from the Kotomi checkout.
3. Run `python tools/validate_repository.py` in this repository.
4. Commit the generated Quiz publication together.

Do not regenerate one channel from the inventory of the other channel.

## Validation

Run:

```text
python tools/validate_repository.py
```

CI runs the same validation for pull requests and `main`. The validator checks canonical layout, XML schemas, hashes, package inventories, Database ownership, Quiz ownership, and manifest ordering.

## Kotomi integration

The Kotomi source repository mounts this repository as the `data` git submodule. Desktop builds and mobile packages include the complete `data/` tree, preserving this directory structure.
