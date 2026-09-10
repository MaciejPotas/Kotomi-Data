# Kotomi Data

This repository contains Kotomi's public Content snapshot and distributable quiz packages.

The two public update channels have deliberately different responsibilities. **Content Update** publishes the complete declarative learning and sentence-generation project as one compatible revision. **Quiz Update** publishes executable quiz packages only.

## Layout

| Path | Purpose | Update channel |
| --- | --- | --- |
| `quiz_project.xml` | Canonical Schema 1 project entrypoint. | Content |
| `dictionaries/` | Word dictionaries for verbs, nouns, adjectives, and copulas. | Content |
| `grammar/` | Shared roles, categories, features, and context pools. | Content |
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

The published manifest is `content_update_manifest.json`. These files are intentionally versioned together because they reference one another. Dictionaries use role, category, feature, and context IDs from grammar data; sentence patterns use the same shared grammar vocabulary and dictionaries. Updating only one side could create a project that loads but cannot generate valid sentences.

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

The project/pattern files use Schema 1. The lesson catalog uses Schema 4.

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
