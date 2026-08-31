# Kotomi Data

Public learning data and distributable quiz packages for Kotomi.

This repository is intentionally separate from the private Kotomi application source. It owns the learning database and the public delivery copy of independently updateable quiz packages generated from the private repository.

## Repository layout

```text
Kotomi-Data/
├── learning/
│   ├── dictionaries/
│   │   ├── adjectives.xml
│   │   ├── copulas.xml
│   │   ├── nouns.xml
│   │   └── verbs.xml
│   ├── grammar/
│   │   ├── contexts.xml
│   │   ├── grammar_rules.xml
│   │   ├── sentence_maps.xml
│   │   └── sentence_quizzes.xml
│   ├── lessons/
│   │   └── lessons.xml
│   └── quiz_project.xml
├── quizzes/
├── tools/
├── database_revision.json
├── database_update_manifest.json
└── quiz_update_manifest.json
```

The root is reserved for repository metadata and public update metadata. Learning XML belongs under `learning/`, public generated quiz packages belong under `quizzes/`, and repository maintenance scripts belong under `tools/`.

Each hand-maintained content directory contains its own README with the local contract and ownership rules.

## Learning database

The private Kotomi repository mounts this repository as the Git submodule `data/`. Therefore `learning/` in this repository is installed as `data/learning/` in Kotomi.

`learning/quiz_project.xml` is the entry point for the sentence engine and Quiz Studio. Its file references are relative to the `learning/` directory, so dictionaries and grammar files can stay grouped without hard-coded application paths.

`learning/lessons/lessons.xml` is the lesson catalog. It is deliberately separate from the sentence-project manifest because it has its own persistence schema.

### Database revision

The learning database has an independent positive integer revision stored in root `database_revision.json`. It is publication metadata, not a learning XML payload. It is not the Kotomi application version and it is not a schema version.

The current state uses Database revision 2. Revision 2 introduces the organized `data/learning/` installation layout while keeping the learning content itself compatible with the same parser schemas.

SHA-256 hashes decide which files are downloaded. The revision identifies a published database state.

### Schema versions

Project and pattern XML currently use Schema 1. `lessons.xml` uses lesson catalog Schema 4. Schema numbers are owned by the private Kotomi parser code and must not be changed here in isolation.

A schema change requires matching parser and writer changes in Kotomi, migrated data, tests, documentation, and regenerated update manifests.

### Pattern data

`learning/grammar/sentence_maps.xml` uses the same pattern language as Quiz Studio. `learning/grammar/contexts.xml` and `learning/grammar/grammar_rules.xml` provide the supporting grammar data, while `learning/grammar/sentence_quizzes.xml` defines sentence-quiz selections.

## Quiz packages

Public quiz distribution uses `quizzes/` together with the root `quiz_update_manifest.json`.

Each generated package lives under `quizzes/<package-id>/` and installs under `apps/<package-id>/` in Kotomi. These package directories are generated from the private source repository. Do not make independent manual changes inside them because the next publication replaces those files.

Published quizzes obtain learning data through Kotomi's application path contract. Current Kotomi resolves the project under `data/learning/`.

From a Kotomi checkout with this repository initialized as its submodule, publish current packages with:

```powershell
python tools\publish_quiz_packages.py 1.1.1
```

The argument is the quiz catalog release, not the Kotomi application version and not the database revision.

## Repository validation

Run locally with:

```bash
python tools/validate_repository.py
```

The validator checks the repository layout, directory documentation, XML schemas, project references, database revision and manifest inventory, manifest hashes, public quiz catalog, package inventories, and Python 3.10 source compatibility.

CI runs the same validator for pull requests and changes to `main`.

## Development checkout

The private Kotomi repository mounts this repository at:

```text
data
```

After cloning Kotomi, initialize the submodule with:

```bash
git submodule update --init --recursive
```

The application then uses `data/learning/` as its canonical learning-data root. Root `data/database_revision.json` remains the database publication identity used by release tooling.

## Update URLs

The public manifest endpoints intentionally remain at the repository root:

```text
https://raw.githubusercontent.com/MaciejPotas/Kotomi-Data/main/database_update_manifest.json
https://raw.githubusercontent.com/MaciejPotas/Kotomi-Data/main/quiz_update_manifest.json
```

Keeping these endpoints stable lets the repository structure evolve without forcing users to reconfigure update-channel URLs.
