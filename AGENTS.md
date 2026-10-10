# Repository instructions

- Write every Git commit message in English, including merge and squash commit messages. This is a standing project rule.

- New tests must use bounded, versioned fixtures. Never load, copy or regenerate fixtures from production vocabulary during tests.
- Any new exception reading shipped Content requires an explicit PR rationale: the production invariant being checked, why a fixture cannot check it, the exact files needed, and the expected cost as Content grows. Merely naming a lesson or calling a check a data audit is not a justification.
- Register approved exceptions by exact test ID. A marker alone never grants production access. Keep release-metadata checks separate from lexical-content access.
