# Repository Tools

`validate_repository.py` is the repository integrity gate.

It checks:

- the canonical learning-data directory layout;
- XML syntax and expected schema versions;
- references from `quiz_project.xml`;
- all lesson and context dictionary references, plus every sentence-quiz pattern reference, without rules tied to a lesson or group name;
- Content revision and manifest coverage, hashes, and URLs;
- published quiz package descriptors and file inventories;
- Python syntax in published quiz packages.

Run it from any working directory with:

```text
python tools/validate_repository.py
```

The validator is also executed by GitHub Actions. Keep repository-layout and cross-reference rules in this validator so accidental flat files, broken lesson references, or missing documentation are caught before merge.
