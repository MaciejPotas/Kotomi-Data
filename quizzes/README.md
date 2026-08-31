# Published Quiz Packages

This directory contains public, distributable copies of Kotomi quiz packages.

Each child directory is one package and contains its `app.json` descriptor plus the Python files listed by `../quiz_update_manifest.json`.

These directories are generated from the private Kotomi repository's `apps/` sources. Do not hand-edit package files here. Make the change in Kotomi, run the quiz publishing tool, then publish the resulting package update here.

Package directories intentionally do not contain hand-maintained README files because every file inside a package is part of its published inventory.
