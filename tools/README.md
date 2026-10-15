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

`validate_repository.py` validates dictionary semantic catalogs and memberships independently of lesson membership and vocabulary size. `tests/test_semantic_categories.py` uses temporary XML mutation fixtures.

## Opt-in B3 release acceptance

Production Content validation is separate from unit tests. It checks the actual
published references and lexical realizations, which independent fixtures cannot
verify. The audit reads the declared project XML graph, enumerates only the two
relative patterns, and edits only a temporary copy. Cost grows linearly with
these patterns' realizations, plus full project validation and one save/reload.
No new production-dependent unit test or exception registration is introduced.

```sh
python tools/validate_subject_relatives.py --kotomi ../Kotomi \
  --baseline-data ../data-before \
  --output docs/validation/subject_relatives_b3.json
```

Use Kotomi main `7e72245a3e4636c53109ffb58c00176f648f6ce2` plus the fix in
[Kotomi #213](https://github.com/MaciejPotas/Kotomi/pull/213). The baseline Content
is `817cdef693ee004b20fd032dcc4a95b5c214e576`. The unpatched engine deliberately
fails the exact supported-pairs invariant because its existential catalog leaks
into ordinary subject-relative agreement.

The report covers all four forms, exact word pairs, contexts, reconstruction,
rejection, fixed-seed canonical questions and answer matching, both quiz
selections, hints, allowed-form UI data, alias completion and temporary Save All
round trips. Existing isolated application tests cover simulator callbacks,
Mobile controllers and the actual verb-editor callbacks; native device operation
remains manual acceptance.

For performance, invoke `benchmark_subject_relatives.py` in alternating fresh
before/after processes with explicit `--kotomi`, `--data`, `--samples 7` and
`--output`. Run seven pairs without discarding samples; compare the median of
paired round ratios. The process pins itself to one available CPU on Linux.
Use the default object-relative pattern on both revisions; use
`--pattern 'Zdania przydawkowe podmiotowe' --samples 21` for the new path.
Cold means a newly loaded project, with loading timed separately. All retained
samples are in `docs/validation/subject_relatives_b3_performance.json`.


The optional production UI smoke uses real Mobile and simulator callbacks with
Kotomi's test controls and development dependencies (including pytest). It checks
two controller lifecycles, three pattern selections, 48 questions and 12 locked
simulator examples without reloading the preloaded project:

```sh
python tools/validate_subject_relative_ui.py --kotomi ../Kotomi \
  --output docs/validation/subject_relatives_b3_ui.json
```

This is not native device testing and is not part of unit-test discovery.
