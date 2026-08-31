# Kotomi Data

Public learning data and distributable quiz packages for Kotomi.

This repository is intentionally separate from the private Kotomi application source. It owns the learning database and the public delivery copy of independently updateable quiz packages generated from the private repository.

## Repository layout

```text
Kotomi-Data/
├── dictionaries/
│   ├── adjectives.xml
│   ├── copulas.xml
│   ├── nouns.xml
│   └── verbs.xml
├── grammar/
│   ├── contexts.xml
│   ├── grammar_rules.xml
│   ├── sentence_maps.xml
│   └── sentence_quizzes.xml
├── quizzes/
├── tools/
├── lessons.xml
├── quiz_project.xml
├── database_revision.json
├── database_update_manifest.json
└── quiz_update_manifest.json
```

The root contains only stable application entry points and publication metadata. Reusable lexical content belongs under `dictionaries/`, grammar and sentence-pattern content belongs under `grammar/`, generated public quiz packages belong under `quizzes/`, and repository maintenance scripts belong under `tools/`.

Each hand-maintained directory contains its own README with the local contract and ownership rules.

## Stable application entry points

The private Kotomi repository mounts this repository as the Git submodule `data/`.

`quiz_project.xml` deliberately remains at the repository root, so Kotomi and independently published quiz packages can continue to use `data/quiz_project.xml`. The manifest now references dictionaries and grammar files through grouped relative paths.

`lessons.xml` deliberately remains at the repository root as the canonical lesson-catalog entry point `data/lessons.xml`.

This gives the content repository a clean internal layout without forcing an application-path migration or breaking already-published quiz packages.

## Database revision

The learning database has an independent positive integer revision stored in root `database_revision.json`. It is not the Kotomi application version and it is not a schema version.

The current state uses Database revision 2. Revision 2 introduces grouped dictionary and grammar directories while retaining the stable `quiz_project.xml` and `lessons.xml` entry points.

SHA-256 hashes decide which files are downloaded. The revision identifies a published database state.

## Schema versions

Project and pattern XML currently use Schema 1. `lessons.xml` uses lesson catalog Schema 4. Schema numbers are owned by the private Kotomi parser code and must not be changed here in isolation.

A schema change requires matching parser and writer changes in Kotomi, migrated data, tests, documentation, and regenerated update manifests.

## Quiz packages

Public quiz distribution uses `quizzes/` together with the root `quiz_update_manifest.json`.

Each generated package lives under `quizzes/<package-id>/` and installs under `apps/<package-id>/` in Kotomi. These package directories are generated from the private Kotomi source repository. Do not make independent manual changes inside them because the next publication replaces those files.

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

The validator checks the root contract, directory documentation, XML schemas, project references, database revision and manifest inventory, manifest hashes, public quiz catalog, package inventories, and Python 3.10 source compatibility.

CI runs the same validator for pull requests and changes to `main`.

## Development checkout

After cloning Kotomi, initialize the `data` submodule with:

```bash
git submodule update --init --recursive
```

The application continues to use `data/quiz_project.xml` and `data/lessons.xml`. The files referenced by the project are now organized below `data/dictionaries/` and `data/grammar/`.

## Update URLs

The public manifest endpoints intentionally remain unchanged:

```text
https://raw.githubusercontent.com/MaciejPotas/Kotomi-Data/main/database_update_manifest.json
https://raw.githubusercontent.com/MaciejPotas/Kotomi-Data/main/quiz_update_manifest.json
```

Keeping these endpoints and the two application entry points stable lets the repository structure evolve without forcing users to reconfigure Kotomi.
