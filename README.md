# Kotomi Data

Public Japanese study data for Kotomi.

This repository is intentionally separate from the private Kotomi application source. It contains the dictionaries, lessons, grammar definitions, sentence maps, contexts and quiz definitions used by Kotomi.

## Files

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

Kotomi installs these XML files under `shared/quiz_data/`. The manifest keeps the installation paths separate from the repository layout.

## Development checkout

The private Kotomi repository mounts this repository as a Git submodule at:

```text
shared/quiz_data
```

After cloning Kotomi, initialize the data repository with:

```bash
git submodule update --init --recursive
```

## Updates

Kotomi's Database update feature uses:

```text
https://raw.githubusercontent.com/MaciejPotas/Kotomi-Data/main/database_update_manifest.json
```

Application updates and database updates are independent. Users may replace the database manifest URL with their own compatible source without changing the Kotomi application update channel.
