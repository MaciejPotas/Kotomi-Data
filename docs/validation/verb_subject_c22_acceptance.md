# C2.2 acceptance / Akceptacja C2.2

## Integracja / Integration

- Baseline Content: `83c36863ee56f606a00a1f02f38d8d75d0595193`, revision 61.
- Candidate Content: revision 62. Engine: `2656c5a270489141661561701d0a064c8a1dcbd4`.
- 33 A verbs / 308 translations / 32 added roles verified against unchanged C1.
- Per form: 70 → 300 subject pairs; 350 → 1500 context realizations; 70 → 300 unique questions and answers.
- Four forms; explicit and implicit agreement; all bound realizations; 104 generated questions.
- 368 pattern availability probes unchanged; both full project validations and the lesson catalog pass.
- Object relative realizations: 7735 → 7645 per form. Exactly 90 hitori bindings removed; all others identical.
- Counters XML unchanged. One person still renders as ひとり; affirmative count questions still use なんにん.
- Negative count questions retain their previous rejection policy.
- Historical C1/C2.1 documents and evidence, all other learning XML, non-subject roles and base verb forms unchanged.

## Metoda pomiaru / Measurement method

Linux, Python 3.12; sequential fresh before/after processes on the same pinned CPU, fixed hash seed 173.
Five paired rounds × seven samples per operation, alternating AB/BA. No tests ran concurrently.
Cold means a fresh project/analysis, not an OS cold start. Warm means one priming call.
First question calls SharedQuizEngine.build_question. Loading is measured separately.
Before/after columns are medians of round medians; change is the median of paired ratios, so it can differ from the ratio of those two columns.
Kolumny przed/po są medianami median serii; zmiana jest medianą ilorazów sparowanych serii.
All initial samples are retained in [the primary report](verb_subject_c22_performance.json).

| Pattern | Operation | Before ms | After ms | Paired change |
| --- | --- | ---: | ---: | ---: |
| Sam czasownik | cold/load | 66.067 | 66.030 | +0.0% |
| Sam czasownik | cold/compatibility | 1.346 | 1.262 | -5.2% |
| Sam czasownik | cold/exists | 0.362 | 0.350 | -4.3% |
| Sam czasownik | cold/count | 20.417 | 21.256 | -0.2% |
| Sam czasownik | cold/first_question | 0.793 | 0.830 | +5.4% |
| Sam czasownik | warm/load | 65.459 | 70.486 | +7.2% |
| Sam czasownik | warm/compatibility | 0.214 | 0.212 | -4.1% |
| Sam czasownik | warm/exists | 0.183 | 0.187 | +3.9% |
| Sam czasownik | warm/count | 20.304 | 21.391 | +5.4% |
| Sam czasownik | warm/first_question | 0.509 | 0.564 | +10.7% |
| Czasownik z dopełnieniem | cold/load | 69.045 | 71.473 | +3.5% |
| Czasownik z dopełnieniem | cold/compatibility | 4.872 | 4.783 | -1.8% |
| Czasownik z dopełnieniem | cold/exists | 4.042 | 4.117 | +1.9% |
| Czasownik z dopełnieniem | cold/count | 503.463 | 504.470 | +0.2% |
| Czasownik z dopełnieniem | cold/first_question | 6.220 | 6.086 | -0.8% |
| Czasownik z dopełnieniem | warm/load | 69.496 | 69.258 | +4.9% |
| Czasownik z dopełnieniem | warm/compatibility | 3.969 | 4.049 | +5.4% |
| Czasownik z dopełnieniem | warm/exists | 3.745 | 4.002 | +7.9% |
| Czasownik z dopełnieniem | warm/count | 492.712 | 502.646 | +2.6% |
| Czasownik z dopełnieniem | warm/first_question | 5.632 | 5.804 | +1.2% |
| Zdania przydawkowe | cold/load | 74.384 | 71.058 | -4.5% |
| Zdania przydawkowe | cold/compatibility | 10.818 | 10.700 | -1.1% |
| Zdania przydawkowe | cold/exists | 8.371 | 8.214 | -2.0% |
| Zdania przydawkowe | cold/count | 481.689 | 494.383 | +2.9% |
| Zdania przydawkowe | cold/first_question | 10.491 | 10.859 | +1.0% |
| Zdania przydawkowe | warm/load | 66.689 | 67.680 | -0.8% |
| Zdania przydawkowe | warm/compatibility | 9.280 | 9.953 | +2.8% |
| Zdania przydawkowe | warm/exists | 7.653 | 7.618 | +1.2% |
| Zdania przydawkowe | warm/count | 492.931 | 463.931 | -5.9% |
| Zdania przydawkowe | warm/first_question | 10.856 | 10.290 | -5.2% |
| Zdania przydawkowe podmiotowe | cold/load | 65.720 | 74.052 | +13.5% |
| Zdania przydawkowe podmiotowe | cold/compatibility | 12.149 | 16.365 | +36.4% |
| Zdania przydawkowe podmiotowe | cold/exists | 11.869 | 15.446 | +29.7% |
| Zdania przydawkowe podmiotowe | cold/count | 35.194 | 107.780 | +207.0% |
| Zdania przydawkowe podmiotowe | cold/first_question | 14.633 | 18.497 | +26.6% |
| Zdania przydawkowe podmiotowe | warm/load | 80.459 | 69.927 | -12.4% |
| Zdania przydawkowe podmiotowe | warm/compatibility | 12.299 | 15.608 | +26.7% |
| Zdania przydawkowe podmiotowe | warm/exists | 11.685 | 15.097 | +28.3% |
| Zdania przydawkowe podmiotowe | warm/count | 34.243 | 106.419 | +216.7% |
| Zdania przydawkowe podmiotowe | warm/first_question | 13.829 | 17.236 | +25.7% |

## Wyjaśnienie przekroczeń / Review of values above 10%

PL: Rozszerzony wzorzec podmiotowy ma 4,286× więcej realizacji. Liczenie kosztuje około 3,1× więcej, a kompatybilność i pierwsze pytanie około 1,3× więcej. To koszt świadomie większego zbioru danych, bez zmian algorytmu. Czas pierwszego pytania pozostaje poniżej 20 ms w medianach tej serii.
EN: The expanded subject pattern has 4.286× more realizations. Counting costs about 3.1× more, compatibility and first question about 1.3× more. This is the deliberately larger domain with unchanged algorithms. Median first-question latency remains below 20 ms in this series.

PL: Jedyny graniczny wynik niezwiązanego wzorca to warm/first_question dla Sam czasownik (+10,7%, około 0,055 ms). Ładowanie jest tą samą operacją dla wszystkich wzorców; jedna seria podmiotowa miała +13,5% cold i -12,4% warm. Oba przypadki sprawdzono osobną większą serią 9 par × 21 próbek, zachowując wszystkie próbki. Przekroczenie 10% nie potwierdziło się.
EN: The only borderline unrelated-pattern result was warm/first_question for Sam czasownik (+10.7%, about 0.055 ms). Loading is the same operation for every pattern; one subject-pattern batch showed +13.5% cold and -12.4% warm. Both cases were checked in a separate larger run of nine pairs × 21 samples, retaining every sample. The >10% result was not reproduced.

[Follow-up raw samples](verb_subject_c22_performance_followup.json).

| Follow-up operation | Before ms | After ms | Paired change |
| --- | ---: | ---: | ---: |
| cold/load | 77.348 | 72.469 | -5.5% |
| cold/first_question | 0.857 | 0.852 | -3.8% |
| warm/load | 73.496 | 71.612 | -1.8% |
| warm/first_question | 0.525 | 0.493 | -3.0% |

Reproduce the targeted follow-up with `--patterns "Sam czasownik" --operations load first_question --rounds 9 --samples 21` using the paired command in tools/README.md.

Wyniki dotyczą silnika na tej maszynie, nie czasu malowania natywnego UI. Results cover the engine on this machine, not native UI painting.

## CI and scope

Production CI validation is structural only; fixture-based engine tests remain enabled. Real-Content integration and the above benchmarks are opt-in. The lesson benchmark workflow is manual-only. No DSL, runtime engine or Quiz package version changed.
Content manifest regenerated by the existing tool. Changed hashes: revision metadata and verbs/nouns/lessons XML only.

## Local test execution

- Kotomi-Data unit tests with `KOTOMI_PATH`: 91 passed in 0.191 s.
- Both repository and question-pattern validators passed.
- Combined Kotomi/Content pytest suite on Linux / Python 3.12: 3735 passed, 4 existing optional-engine skips, 6358 subtests passed in 127.72 s.
- Slowest test call: 1.76 s; the unchanged 8-second performance gate passes.
- Collection audit: 2587 declared application test callables, 3648 collected application items; passed.
- Source compilation passed. These local results do not replace the PR's Windows / Python 3.11 coverage run.
