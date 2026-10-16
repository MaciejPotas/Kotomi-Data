# C2.1 acceptance, 2026-10-16

Baseline Content: `9227fd02c3c315c3d49ea9357a652a0a4d9c36bc` (revision 60).
Engine: `9c01404465837f55d32ce1b4056fbb6e99817440`. Candidate Content: revision 61.
The local engine snapshot was checked against its Git tree: all 492 Python/XML/JSON files outside bundled Content matched, with none missing. The remote main ref matched the pinned engine revision.

## Data and correctness

- Exactly seven verbs, 56 translations and six subject roles, selected only from C1 `changes`.
- Preflight checked A status, parent paths, absent entries and dependencies before any write.
- Reversing only those additions restores the baseline XML structure, including existing values, roles and node order. Replacing the seven changed blocks restores the original file bytes. Other dictionaries are byte-identical.
- Full project load/validation succeeds before and after, with no errors.
- Subject pairs: 20 → 70 per form. Contextual realizations: 100 → 350 per form. Four forms checked; the increase is exactly 50 pairs.
- All 30,940 object-relative full signatures and statistics are unchanged (7,735 per form).
- Availability is unchanged for all 92 patterns across four forms.
- 2,068 out-of-role noun availability rejections pass, with additional bound-render rejection checks.
- Explicit and implicit agreement pass for every subject pair/form, including bound rendering and exact Polish/Japanese output.
- 100 seeded generated questions match valid output pairs and accept their canonical answers.
- Content manifest rebuilt with the existing Kotomi builder; only revision metadata and the verbs entry changed. Quiz manifest/packages are untouched.
- Historical C1 files and validator are unchanged. C1 static and engine checks passed before implementation; production dictionaries at the C1 pinned base and the C2.1 baseline are identical.
- Remaining scope: 26 A verbs for C2.2; no B/C proposals applied.

## Tests and CI cost

- Repository suite with `KOTOMI_PATH`: 77 passed in 0.172 s, including eight new synthetic mutation tests.
- Standard CI environment without the engine: 73 passed, four existing engine contract tests explicitly skipped (77 discovered, 0.149 s).
- Existing Kotomi agreement/persistence/catalog-boundary suites: 112 passed in 4.95 s, using independent fixtures.
- Repository and question-pattern validators pass. The added structural check took 6.002 ms including proposal JSON loading, reusing the already parsed verbs XML (one local observation, not a performance SLA).
- No new production-dependent unit test, exception registration, engine dependency or expensive CI job. Integration and benchmarks remain opt-in.

## Performance

B3 measurement method, focused on the requested operations: seven alternating before/after process pairs per pattern, one CPU, cold/warm modes, seven samples per object operation and 21 per subject operation. All samples of this focused run are retained in `verb_subject_c21_performance.json`. An initial exploratory full benchmark was stopped before completion because project-validation timing dominated its runtime; it is not used in this comparison.
Cold means a new project, not an OS cold cache. Values below are medians of the seven round medians, in milliseconds. Change is the median of paired after/before ratios, so it need not equal the ratio of the two displayed aggregate medians.

### Zdania przydawkowe

| Operation | Before (ms) | After (ms) | Paired change |
|---|---:|---:|---:|
| `cold/load` | 66.106 | 68.428 | +3.2% |
| `cold/compatibility` | 10.734 | 10.768 | +3.9% |
| `cold/exists` | 8.298 | 8.296 | +2.2% |
| `cold/count` | 501.255 | 477.972 | -6.2% |
| `cold/first_question` | 10.780 | 10.561 | -3.1% |
| `warm/load` | 68.418 | 64.470 | -2.9% |
| `warm/compatibility` | 9.588 | 9.301 | +0.8% |
| `warm/exists` | 7.965 | 7.646 | -1.2% |
| `warm/count` | 479.909 | 474.609 | -0.8% |
| `warm/first_question` | 10.259 | 10.076 | -2.1% |

### Zdania przydawkowe podmiotowe

| Operation | Before (ms) | After (ms) | Paired change |
|---|---:|---:|---:|
| `cold/load` | 69.123 | 71.155 | +1.6% |
| `cold/compatibility` | 11.039 | 12.280 | +11.2% |
| `cold/exists` | 11.230 | 12.077 | +6.7% |
| `cold/count` | 18.753 | 34.288 | +87.8% |
| `cold/first_question` | 13.194 | 14.508 | +10.5% |
| `warm/load` | 66.755 | 64.979 | +0.7% |
| `warm/compatibility` | 10.151 | 11.921 | +17.4% |
| `warm/exists` | 10.730 | 12.018 | +9.1% |
| `warm/count` | 17.517 | 34.775 | +96.7% |
| `warm/first_question` | 12.267 | 14.143 | +13.0% |

The unchanged object-relative path stays within the 10% regression limit for every measured operation. Subject-relative work has a larger candidate domain (3 → 10 verbs; 20 → 70 pairs), so its compatibility, availability, counting and first-question costs are interpreted as expanded work. No engine code changed. Loading is measured separately.

## Limits and merge readiness

No unresolved data or integration blocker was found. Native Windows/Android device interaction was not performed. Results refer to the pinned baseline and supplied audit configuration, not every user quiz filter. This PR is intentionally unmerged.
