# Repository instructions

- Write every Git commit message in English, including merge and squash commit messages. This is a standing project rule.

- New tests must use bounded, versioned fixtures. Never load, copy or regenerate fixtures from production vocabulary during tests.
- Any new exception reading shipped Content requires an explicit PR rationale: the production invariant being checked, why a fixture cannot check it, the exact files needed, and the expected cost as Content grows. Merely naming a lesson or calling a check a data audit is not a justification.
- Register approved exceptions by exact test ID. A marker alone never grants production access. Keep release-metadata checks separate from lexical-content access.

- Do not freeze a real lesson or quiz inventory in tests, including word counts and group-specific rules. Use bounded mutation fixtures for validator behavior and keep general published-reference/lexical-quality checks.
- The companion Kotomi `tests/conftest.py` registers each Content exception with `invariant`, `fixture_gap`, `file_scope`, and `growth_cost`, and enforces file scope during the combined suite.
- Keep `docs/pl` and `docs/eng` guides equivalent. Retirement belongs only in `quiz_project.xml`; never delete user files merely because a dictionary is retired.
