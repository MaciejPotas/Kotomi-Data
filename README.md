# Kotomi Data

This repository contains the public learning database and distributable quiz packages used by Kotomi.

The root is intentionally kept small. Files at the root are repository contracts or update entrypoints. Learning content is grouped by responsibility below them.

## Layout

| Path | Purpose |
| --- | --- |
| `quiz_project.xml` | Canonical Schema 1 project entrypoint. |
| `dictionaries/` | Word dictionaries for verbs, nouns, adjectives, and copulas. |
| `grammar/` | Grammar definitions and reusable context pools. |
| `patterns/` | Sentence maps and sentence-quiz definitions. |
| `lessons/` | Schema 4 lesson catalog. |
| `quizzes/` | Published quiz packages consumed by Kotomi's quiz update channel. |
| `tools/` | Repository validation and maintenance helpers. |
| `database_revision.json` | Identity of the published learning database. |
| `database_update_manifest.json` | Database update inventory. |
| `quiz_update_manifest.json` | Quiz package update inventory. |

A Kotomi installation mirrors the learning-data tree below its `data/` directory. For example, `dictionaries/verbs.xml` is installed as `data/dictionaries/verbs.xml`.

## Project entrypoint

Kotomi opens `data/quiz_project.xml`. References inside the project file are relative to that file, so dictionaries and supporting XML can live in their own directories without special runtime lookup rules.

The project/pattern files use Schema 1. The lesson catalog uses Schema 4.

## Updating data

When the public learning data changes:

1. Edit the appropriate content directory.
2. Update `database_revision.json` when publishing a new database state.
3. Regenerate or update `database_update_manifest.json`.
4. Run `python tools/validate_repository.py`.
5. Commit the content and manifest changes together.

The database and quiz channels are independent. Changing learning data does not require republishing quiz packages unless the quiz package code itself changed.

## Quiz packages

`quizzes/` contains generated public copies of first-party quiz packages. Their source is maintained in the private Kotomi repository under `apps/`. Do not hand-edit generated package contents here.

## Validation

Run:

```text
python tools/validate_repository.py
```

CI runs the same validation for pull requests and `main`.

## Kotomi integration

The Kotomi source repository mounts this repository as the `data` git submodule. Desktop builds and mobile packages include the complete `data/` tree, preserving this directory structure.
