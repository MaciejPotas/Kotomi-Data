# B3 release review / przegląd wydania

Status: implementation, release audit and performance review completed.
Kotomi CI is green; Content CI is recorded in the PR. Do not deploy Content 60 before Kotomi #213 is integrated.
No automatic merge or B4 Content pin update is part of this work.

## Exact baseline

- Kotomi main: `7e72245a3e4636c53109ffb58c00176f648f6ce2` (merged B2).
- Kotomi-Data main: `817cdef693ee004b20fd032dcc4a95b5c214e576`, Content 59.
- Separate engine correction: [Kotomi #213](https://github.com/MaciejPotas/Kotomi/pull/213),
  head `55b3c53dabbdecf7c431593c809ee8d034bb3c2f`.
- New Content: 60. Application version, Quiz revision and app Content gitlink are unchanged.

## Reviewed content

| Verb | Rationale | Subject restriction | Stored classes |
|---|---|---|---|
| hataraku | Human work, required reference example | Eight explicit person nouns | masculine_personal, feminine |
| neru | Sleep, both human and animal subjects | Same eight people plus inu/tori | masculine_personal, masculine_animate, feminine |
| aku | Intransitive change, distinct from akeru | Existing bag/box list unchanged | feminine, neuter |

Each verb has explicit translations for dictionary, plain_negative, past_plain
and past_negative_plain. Old translations, other forms, Japanese spellings,
existing roles and all noun metadata are unchanged. Missing and unused classes
remain absent. The isolated B2 suite covers all five singular classes; this
Content deliberately exercises only the four classes reachable by its nouns.

The pattern is exactly the proposed dynamic XML, with two slots and no new
random dimension. The existing `relative_clauses` quiz now references both
patterns, preserving its attributes and updating its description to match.

## Semantic findings

1. `person` includes `hitori`, a quantified expression. New ordinary subject
   roles use existing exact-noun constraints to exclude it locally.
2. Broad `thing` is unsuitable for working/sleeping subjects. The exact lists
   reject book + hataraku, car + neru and people + aku, without category changes.
3. B2's existential catalog admitted predicates without explicit lexical
   agreement translations. It produced `osoba, która nie ma` and `osoba, która
   nie było`. Kotomi #213 rejects noun agreement in an ungoverned subject
   binding for that catalog. Governed nouns, number/interrogative agreement and
   legacy counting remain supported. This is a real engine prerequisite,
   not a data workaround or a hidden filter.
4. No further semantic defect was found in the 80 generated B3 pairs reviewed.
   Plain nonpast forms do not promise the ongoing-action meaning of te-iru.

## Counts and regression

| Metric | Per form | All four forms |
|---|---:|---:|
| Distinct verb/noun pairs | 20 | 20 (same vocabulary) |
| Generated realizations, including hidden contexts | 100 | 400 |
| Unique Polish questions | 20 | 80 |
| Unique Japanese answers | 20 | 80 |
| Unique question-answer pairs | 20 | 80 |

The 20 pairs split into 8 hataraku, 10 neru and 2 aku pairs. Five context choices
produce the same visible text. Do not present 400 as the unique-question count.

Every realization was reconstructed with explicit words, nouns, forms and
context. Every form's exists, compatibility, enumeration and count agree.
The audit also checks 36 explicit invalid verb/noun/form selections and 100
canonical questions with seed 173, reproduced in a second run with identical
output and accepted expected answers. All 80 pairs are in the JSON report.

Existing non-relative patterns that select a subject also require the existential
feature; the newly assigned subjects do not enter them. The only existing
verb+noun simple patterns without an explicit role either require reporting
verbs or fix the verb to iru. Existing location/destination/object roles are
unchanged, and all pre-existing word/form glosses and Japanese spellings match.

Existing object relatives have 7,735 realizations per form, 30,940 overall.
Their full signatures (texts, words, nouns, forms and contexts) and statistics
match baseline exactly. Both patterns selected together yield 31,340 realizations.

## Verification boundaries

- Content repository validator, question validator and all 34 unittest tests pass.
- Application focused suite: 271 passed (B1/B2, existential/quantity regression,
  Studio, change-aware persistence, fragment saves and the new boundary cases).
- Final application CI [38747457557](https://github.com/MaciejPotas/Kotomi/actions/runs/38747457557):
  all three jobs passed. Windows/Python 3.11: **3,622 passed and 6,195 subtests
  passed in 685.08 s**, branch coverage 66.9%. The unchanged 8-second gate passed:
  nine initially slow calls, zero confirmed failures after isolated rechecks.
  Python 3.10 source compatibility and the main/PR lesson benchmark also passed.
  The initial local run's stale manifest checks were fixed by regeneration;
  all affected checks passed before publication.
- Production release audit: no project validation errors/warnings; all four
  forms, exact candidates, reconstruction and fixed-seed generation pass.
- Studio data paths: allowed-form labels/availability, relative alias completion,
  preview, no-op Save All preserving bytes/mtime, editing one agreed translation,
  saving only verbs.xml and reloading every agreement mapping pass.
- Shared Windows/Mobile grammar policy: object-only, subject-only and combined
  selection, availability, statistics and generated questions pass. Existing
  independent fixture tests exercise actual simulator callbacks, Mobile
  controller setup and actual verb editor callbacks with headless controls.
- Additional production UI smoke: two real Mobile controller build/unload
  lifecycles, all three pattern selections and 48 questions, with fake Kivy
  controls. The real SimulatorTab.generate callback passes 12 locked examples
  (three verbs × four forms). Unexpected project reload is an explicit failure.
  See [UI evidence](subject_relatives_b3_ui.json) and the reproducible opt-in tool.
- Hints contain the chosen verb and noun; the invisible context is omitted.
- Native Windows layout, physical Android interaction and deployment/restart on
  a device were not manually tested. These remain device acceptance, not claims
  of this report. No test was weakened or made production-dependent.

## Reproduce

See [the audit instructions](../../tools/README.md). The explicit release tool
reads production Content; the application unit tests use bounded fixtures only.
[Audit details](subject_relatives_b3.json) and [all timing samples](subject_relatives_b3_performance.json)
are committed with this report. The benchmark alternates seven before/after
fresh-process pairs and reports median paired ratios. Cold refers to freshly
loaded project state, not OS/disk cache eviction. Full-project validation
naturally includes one additional production pattern.


## Performance result

Seven alternating process pairs, seven samples per operation/mode, on one CPU.
All 14 existing-scenario paired median changes are below +10%; the largest is
**+5.51%** (warm full-project validation, which now includes one more pattern).
No reproducible >10% regression was observed. Shared-host timings are not a
hardware latency guarantee. No limits were raised and no samples discarded.

| Existing object-relative operation | Cold paired change | Warm paired change |
|---|---:|---:|
| Project load | -2.95% | +1.91% |
| Full project validation | +3.50% | +5.51% |
| Compatibility | +3.11% | +3.27% |
| exists() | +3.75% | -1.15% |
| count_possibilities() | +1.91% | +0.83% |
| First canonical question | +5.33% | -0.08% |
| Next canonical question | -1.50% | +0.81% |

The percentages are medians of within-round ratios, not ratios of the separately
reported absolute medians. Existing object-relative cardinality is unchanged.
Selecting both patterns adds 400 realizations to 30,940, so a larger total
enumeration workload is expected and is not an algorithm change.

New subject-relative path, 21 samples per cell, past_negative_plain:

| Operation | Cold median ms | Warm median ms |
|---|---:|---:|
| Project load | 69.5656 | 82.2246 |
| Full project validation | 3427.4394 | 3342.5197 |
| Compatibility | 10.8645 | 10.1052 |
| exists() | 10.9683 | 13.2907 |
| Count (100 contextual realizations) | 17.7887 | 20.9334 |
| First canonical question | 13.4379 | 14.4719 |
| Next canonical question | 12.6811 | 13.7974 |
| Stored verb agreement lookup | 0.0044 | 0.0004 |

Cold means a fresh project. Load is timed separately; first-question timing
uses the already loaded project, as the shared application engine does.
