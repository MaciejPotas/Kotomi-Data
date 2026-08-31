# Kotomi Data

Public learning data and distributable quiz packages for Kotomi.

This repository is intentionally separate from the private Kotomi application source. It owns dictionaries, lessons, grammar definitions, sentence maps, contexts, and the public delivery copy of independently updateable quiz packages generated from the private source repository.

## Learning data

The learning-data files currently include:

- `nouns.xml`
- `verbs.xml`
- `adjectives.xml`
- `copulas.xml`
- `grammar_rules.xml`
- `contexts.xml`
- `sentence_maps.xml`
- `sentence_quizzes.xml`
- `quiz_project.xml`
- `lessons.xml`
- `database_revision.json`
- `database_update_manifest.json`

Kotomi has one supported learning-data installation location: `data/`. The Database manifest publishes the learning XML and `database_revision.json` only to that canonical path. The pre-refactor `shared/quiz_data/` layout is intentionally unsupported for the fresh-start architecture.

### Database revision

The learning database does not use the Kotomi application version. Kotomi itself uses semantic `x.y.z` versioning, while the database has one independent positive integer revision:

```text
Kotomi 1.1.1 [Database: 1]
```

`database_revision.json` is the installed human-readable database identity:

```json
{
  "format": 1,
  "revision": 1
}
```

`database_update_manifest.json` carries the same integer in its top-level `revision` field. The revision should increase when an official learning-data state is published. It does not participate in application or quiz compatibility checks.

SHA-256 hashes, not the revision number, decide which files an installation downloads. The revision therefore identifies a published database state without forcing unchanged files to be downloaded.

### XML schema versions

Schema versions are separate from both the Kotomi application version and the database revision. The current project and sentence-pattern data use **Schema 1**. This covers the project manifest, dictionaries used by the sentence engine, grammar rules, contexts, sentence maps, and sentence quiz definitions.

`lessons.xml` has its own lesson-catalog persistence format and currently uses **schema 4**. Resetting the project/pattern schema to 1 does not reset the lesson schema, and changing the database revision does not imply a schema change.

In other words, an installation can legitimately be described as:

```text
Kotomi 1.1.1
Database revision 1
Project/pattern schema 1
Lesson catalog schema 4
```

These values have different jobs and should not be kept numerically synchronized.

### Sentence maps

`sentence_maps.xml` uses the same single pattern language as Quiz Studio. Named selections use `@name`, brackets select or constrain, and dots read a property from the selected value:

```text
{verb@main[role:object][form].translation}
{verb@before[form:past_plain]}
{noun[category:place][case:genitive]}
{context[from:main].translation}
{context[pool:past].kana}
```

A bare word refers to its base dictionary value. `[form]` selects the form chosen by the quiz, while `[form:name]` selects one fixed grammatical form. Noun cases are localized scalar values, so `{noun[case:accusative]}` directly renders the selected case.

Kotomi does not keep a second compatibility dialect for retired pattern spellings. When the authoring language changes, the public sentence maps are migrated together with the application parser and tests.

## Quiz packages

Public quiz distribution uses:

```text
quizzes/
quiz_update_manifest.json
```

Each package is stored under `quizzes/<package-id>/`, while the manifest installs it under `apps/<package-id>/` in Kotomi. Package files are generated from the private Kotomi source repository and should not be edited independently because the next publication replaces those edits.

Published quiz packages use the canonical Kotomi APIs and load their project from `data/quiz_project.xml`. They are released together with the fresh-start application contract rather than carrying pre-refactor import or path fallbacks.

From a Kotomi checkout with this repository initialized as its submodule, publish the current packages with:

```powershell
python tools\publish_quiz_packages.py 1.1.1
```

Here `1.1.1` is the quiz catalog release, not the Kotomi application version and not the database revision. Each package also keeps its own `version` in `app.json`.

Review and commit the generated `quizzes/` directory and `quiz_update_manifest.json` in this repository.

## Development checkout

The private Kotomi repository mounts this repository as the Git submodule:

```text
data
```

After cloning Kotomi, initialize it with:

```bash
git submodule update --init --recursive
```

## Update URLs

Kotomi's learning-data updater uses:

```text
https://raw.githubusercontent.com/MaciejPotas/Kotomi-Data/main/database_update_manifest.json
```

The independent quiz updater uses:

```text
https://raw.githubusercontent.com/MaciejPotas/Kotomi-Data/main/quiz_update_manifest.json
```

Application, quiz, and learning-data updates are separate channels. Users may point the quiz or database updater at another compatible source without changing where the Kotomi application itself is updated from.
