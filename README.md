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
- `database_update_manifest.json`

The canonical Kotomi installation location is now `data/`. While Kotomi remains on version 1.1.1, `database_update_manifest.json` deliberately publishes each XML to both `data/` and the historical `shared/quiz_data/` path. This compatibility bridge keeps older 1.1.1 installations functional even when Database Update runs before Application Update. It can be removed after the application version is bumped and the legacy layout no longer needs support.

## Quiz packages

Public quiz distribution uses:

```text
quizzes/
quiz_update_manifest.json
```

Each package is stored under `quizzes/<package-id>/`, while the manifest installs it under `apps/<package-id>/` in Kotomi. Package files are generated from the private Kotomi source repository and should not be edited independently because the next publication replaces those edits.

Because version 1.1.1 installations can update quiz packages independently, the published package code keeps compatibility imports that older 1.1.1 application builds understand. Project lookup prefers the canonical `data/quiz_project.xml` and falls back to `shared/quiz_data/quiz_project.xml`.

From a Kotomi checkout with this repository initialized as its submodule, publish the current packages with:

```powershell
python tools\publish_quiz_packages.py 1.1.1
```

Review and commit the generated `quizzes/` directory and `quiz_update_manifest.json` in this repository.

## Development checkout

The private Kotomi repository mounts this repository as a Git submodule at:

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
