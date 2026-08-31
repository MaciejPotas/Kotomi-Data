# Public Quiz Packages

This directory is the generated public delivery copy of Kotomi quiz packages.

Each child directory is one independently updateable package. Package descriptors and file inventories are published through the repository-level `quiz_update_manifest.json` and are installed under `apps/<package-id>/` in Kotomi.

Do not edit package implementation files here independently. The source of truth is the private Kotomi repository. Publish them with `tools/publish_quiz_packages.py` from a Kotomi checkout, then review the generated changes in this repository.

Child package directories intentionally contain only package payload files. Hand-written documentation stays in this README so it does not become part of an installed quiz package inventory.
