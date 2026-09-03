# Kotomi Data

This repository contains Kotomi's public learning database, Studio/project quiz content, and distributable quiz packages.

The root is intentionally kept small. Files at the root are repository contracts or update entrypoints. Content is grouped by update ownership below them.

## Layout

| Path | Purpose | Update owner |
| --- | --- | --- |
| `quiz_project.xml` | Canonical Schema 1 project entrypoint. | Quiz |
| `dictionaries/` | Word dictionaries for verbs, nouns, adjectives, and copulas. | Database |
| `grammar/` | Grammar definitions and reusable context pools edited through the project/Studio layer. | Quiz |
| `patterns/` | Sentence maps and sentence-quiz definitions. | Quiz |
| `lessons/` | Schema 4 lesson catalog. | Database |
| `quizzes/` | Published Python quiz packages consumed by Kotomi's quiz update channel. | Quiz |
| `tools/` | Repository validation and maintenance helpers. | Repository tooling |
| `database_revision.json` | Identity of the published dictionaries/lessons database. | Database |
| `database_update_manifest.json` | Dictionary and lesson update inventory. | Database |
| `quiz_update_manifest.json` | Quiz packages plus Studio/project XML update inventory. | Quiz |

A Kotomi installation mirrors public content below its `data/` directory. For example, `dictionaries/verbs.xml` is installed as `data/dictionaries/verbs.xml`, while `patterns/sentence_maps.xml` is installed as `data/patterns/sentence_maps.xml`.

## Project entrypoint

Kotomi opens `data/quiz_project.xml`. References inside the project file are relative to that file, so dictionaries and supporting XML can live in their own directories without special runtime lookup rules.

The project/pattern files use Schema 1. The lesson catalog uses Schema 4.

## Database updates

The Database channel is intentionally limited to content learned as vocabulary/lessons:

- `dictionaries/*.xml`
- `lessons/lessons.xml`
- `database_revision.json`

When dictionaries or lessons change:

1. Edit the appropriate dictionary or lesson file.
2. Increase `database_revision.json` when publishing a new database state.
3. Regenerate `database_update_manifest.json`.
4. Run `python tools/validate_repository.py`.
5. Commit the content and manifest changes together.

Changing a sentence pattern, grammar rule, context pool, sentence-quiz profile, or `quiz_project.xml` must not increase the database revision.

## Quiz updates

The Quiz channel owns both executable quiz packages and the declarative project content used to build/run quizzes:

- generated package copies under `quizzes/`, installed under `apps/`
- `quiz_project.xml`
- `grammar/*.xml`
- `patterns/*.xml`

This matches Studio ownership: changes Studio makes to quiz definitions, grammar/project configuration, or sentence patterns travel through `quiz_update_manifest.json` together with quiz package releases when required.

`quizzes/` contains generated public copies of first-party quiz packages. Their source is maintained in the private Kotomi repository under `apps/`. Do not hand-edit generated package contents here.

The Database and Quiz channels are independent. A lesson/dictionary release does not require a Quiz release, and a new pattern or quiz profile does not require a Database revision.

## Validation

Run:

```text
python tools/validate_repository.py
```

CI runs the same validation for pull requests and `main`.

## Kotomi integration

The Kotomi source repository mounts this repository as the `data` git submodule. Desktop builds and mobile packages include the complete `data/` tree, preserving this directory structure.
