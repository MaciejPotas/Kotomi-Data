# Learning Data

This directory is the complete Kotomi learning XML payload. When this repository is mounted as the `data` submodule in Kotomi, this directory becomes `data/learning/`.

`quiz_project.xml` is the sentence-project entry point. It references files below `dictionaries/` and `grammar/` using paths relative to this directory. The repository-level `database_revision.json` identifies the published database state.

Directory ownership is intentionally strict:

- `dictionaries/` contains lexical dictionaries only.
- `grammar/` contains contexts, grammar relationships, sentence patterns, and sentence-quiz definitions.
- `lessons/` contains the lesson catalog only.

Do not place learning XML directly at the repository root. Do not place generated quiz Python packages in this directory. The repository validator enforces these boundaries.

The application must access this directory through Kotomi's canonical path helpers rather than assuming individual XML files live next to update manifests.
