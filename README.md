# Kotomi Data

Public learning data and distributable quiz packages for Kotomi.

This repository is intentionally separate from the private Kotomi application source. It contains dictionaries, lessons, grammar definitions, sentence maps and contexts. It also provides the public delivery location for independently updateable quiz packages generated from the private source repository.

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
- `database_update_manifest.json`

Kotomi installs these XML files under `shared/quiz_data/`. The database manifest keeps installation paths separate from this repository layout.

## Quiz packages

Public quiz distribution uses:

```text
quizzes/
quiz_update_manifest.json
```

Each package is stored under `quizzes/<package-id>/`, while the manifest installs it under `apps/<package-id>/` in Kotomi. Package files are generated from the private Kotomi source repository. They should not be edited independently here because the next publication would replace those edits.

From a Kotomi checkout with this repository initialized as its submodule, publish the current packages with:

```powershell
python tools\publish_quiz_packages.py 1.1.1
```

Review and commit the generated `quizzes/` directory and `quiz_update_manifest.json` in this repository.

## Development checkout

The private Kotomi repository mounts this repository as a Git submodule at:

```text
shared/quiz_data
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

Application, quiz and learning-data updates are separate channels. Users may later point the quiz or database updater at their own compatible source without changing where the Kotomi application itself is updated from.
