# MiniC optimizer: measured speedup results

**30 MiniC benchmarks**, each emitted as C at every one of the **32 pass combinations** (5 independently toggleable passes), compiled with **`gcc -O0`**, and timed (median of 6 wall-clock runs after 3 warm-ups).

`speedup = time(combo 0, no passes) / time(combo)` -- how much the MiniC TAC optimizer beats *not* optimizing, with the C compiler pinned at `-O0` so the measured gain is ours, not gcc's.

## Headline

- **Best combo per program, geomean speedup: x1.38**  (max **x2.66**)
- All 5 passes on (combo 31): geomean x1.31
- Safe strong default -- combo 12 [Common Subexpression Elimination (CSE), Loop-Invariant Code Motion (LICM)]: geomean x1.16, and never worse than x0.98 on any program
- No single combo is best everywhere: the all-passes combo is left on the table (>2% slower than the per-program best) on **20 / 30** programs -- which is why a per-program recommender is worth having.

### by category (best-combo geomean)

- structs: x1.87
- loops: x1.48
- numeric: x1.14
- strings: x1.09
- recursion: x1.07

## ML recommendation (RandomForest, GroupKFold by program_id)

Cross-validation holds *whole programs* out -- a program's rows share identical static features, so a random split would leak.

- Held-out programs scored: 30  (30 programs, 5 folds)
- Speedup-prediction MAE: 0.137
- **Model-recommended combo, mean true speedup on unseen programs: x1.37**
- Baseline (combo 0): x1.00   |   oracle (best combo in hindsight): x1.44
- Model captures **85%** of the available speedup without ever having timed the program.

## Per-program

| program | category | best combo | passes | best speedup | all-on |
|---|---|--:|---|--:|--:|
| complex_arith | structs | 31 | CF, DCE, CSE, LICM, SR | **x2.66** | x2.66 |
| licm_div | loops | 3 | CF, DCE | **x2.57** | x2.47 |
| distance_accum | structs | 15 | CF, DCE, CSE, LICM | **x2.28** | x2.11 |
| bbox | structs | 30 | DCE, CSE, LICM, SR | **x2.01** | x1.94 |
| const_fold | loops | 7 | CF, DCE, CSE | **x1.84** | x1.79 |
| cse_subexpr | loops | 22 | DCE, CSE, SR | **x1.78** | x1.70 |
| licm_arith | loops | 7 | CF, DCE, CSE | **x1.74** | x1.55 |
| nested_licm | loops | 13 | CF, CSE, LICM | **x1.68** | x1.54 |
| cse_mod | loops | 7 | CF, DCE, CSE | **x1.67** | x1.56 |
| polynomial | loops | 6 | DCE, CSE | **x1.66** | x1.65 |
| licm_cond | loops | 27 | CF, DCE, LICM, SR | **x1.59** | x1.57 |
| cse_chain | loops | 7 | CF, DCE, CSE | **x1.47** | x1.42 |
| const_prop | loops | 27 | CF, DCE, LICM, SR | **x1.44** | x1.29 |
| licm_mixed | loops | 19 | CF, DCE, SR | **x1.44** | x1.41 |
| vector_scale | numeric | 23 | CF, DCE, CSE, SR | **x1.27** | x1.20 |
| caesar | strings | 6 | DCE, CSE | **x1.18** | x1.16 |
| matrix_mult | numeric | 12 | CSE, LICM | **x1.18** | x0.89 |
| ackermann | recursion | 5 | CF, CSE | **x1.16** | x1.09 |
| dotprod | numeric | 7 | CF, DCE, CSE | **x1.15** | x1.12 |
| conv1d | numeric | 7 | CF, DCE, CSE | **x1.12** | x1.12 |
| stencil_1d | numeric | 15 | CF, DCE, CSE, LICM | **x1.06** | x1.04 |
| histogram | numeric | 15 | CF, DCE, CSE, LICM | **x1.05** | x1.04 |
| newton_isqrt | loops | 12 | CSE, LICM | **x1.05** | x0.96 |
| tak | recursion | 6 | DCE, CSE | **x1.04** | x1.02 |
| strength_reduce | loops | 2 | DCE | **x1.03** | x0.89 |
| prime_sieve | loops | 7 | CF, DCE, CSE | **x1.03** | x0.99 |
| fib | recursion | 21 | CF, CSE, SR | **x1.02** | x1.00 |
| vowel_count | strings | 23 | CF, DCE, CSE, SR | **x1.01** | x0.99 |
| gcd_repeat | loops | 12 | CSE, LICM | **x1.01** | x0.97 |
| particle_sim | structs | 29 | CF, CSE, LICM, SR | **x1.01** | x1.00 |

## Method notes

- `gcc -O0` is intentional: at `-O0` the C compiler does essentially no optimization, so the delta is what the MiniC optimizer contributed.
- Benchmarks are sized so combo 0 runs ~40-200 ms, well above scheduler noise; several are division-heavy because an integer divide is a large, non-pipelined cost that removing is clearly visible.
- Every combo is verified to reproduce combo 0's exit code before its time is recorded (`benchmarks/ground_truth.csv`); a miscompiled binary never contributes a timing sample.
- Strength reduction can slightly *pessimize* tight loops where the multiply it removes is already cheap under `-O0` -- visible in the corpus, and exactly the kind of call the recommender learns to make.