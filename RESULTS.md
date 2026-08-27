# MiniC optimizer: measured speedup results

Corpus: **18 MiniC benchmarks**. Each program is emitted as C at every one of the 64 optimization combos, compiled with `gcc -O0`, and timed (median wall-clock). Speedup is `time(combo 0) / time(combo)` -- i.e. how much our TAC optimizer beats *not* optimizing, with the C compiler held at `-O0`.

## Headline

- **Geomean speedup, all 5 passes on:** x1.291
- **Geomean speedup, best combo per program:** x1.378
- **Largest single speedup:** x2.63
- **Programs regressed (any combo >5% slower than baseline):** 6 / 18
- **Best fixed combo across the corpus:** 47 [Constant Folding (CF), Dead Code Elimination (DCE), Common Subexpression Elimination (CSE), Loop-Invariant Code Motion (LICM)], geomean x1.322

## ML recommendation (GroupKFold, grouped by program_id)

- Held-out programs: 18  (18 programs, 5 folds)
- Speedup-prediction MAE: 0.1985
- Model-recommended combo, mean true speedup: **x1.286**
- Oracle (best combo, hindsight): x1.443
- Model captures **65%** of the available speedup on unseen programs

## Per-program

| program | category | best combo | passes | best speedup | all-on speedup |
|---|---|---|---|---|---|
| ackermann | recursion | 6 | Dead Code Elimination (DCE), Common Subexpression Elimination (CSE) | **x1.02** | x1.00 |
| caesar | strings | 62 | Dead Code Elimination (DCE), Common Subexpression Elimination (CSE), Loop-Invariant Code Motion (LICM), Strength Reduction (SR) | **x1.17** | x1.15 |
| const_fold | loops | 57 | Constant Folding (CF), Loop-Invariant Code Motion (LICM), Strength Reduction (SR) | **x1.79** | x1.63 |
| cse_mod | loops | 6 | Dead Code Elimination (DCE), Common Subexpression Elimination (CSE) | **x1.64** | x1.53 |
| cse_subexpr | loops | 22 | Dead Code Elimination (DCE), Common Subexpression Elimination (CSE), Strength Reduction (SR) | **x1.70** | x1.63 |
| distance_accum | structs | 15 | Constant Folding (CF), Dead Code Elimination (DCE), Common Subexpression Elimination (CSE), Loop-Invariant Code Motion (LICM) | **x2.21** | x2.15 |
| fib | recursion | 43 | Constant Folding (CF), Dead Code Elimination (DCE), Loop-Invariant Code Motion (LICM) | **x1.01** | x1.00 |
| licm_arith | loops | 45 | Constant Folding (CF), Common Subexpression Elimination (CSE), Loop-Invariant Code Motion (LICM) | **x1.79** | x1.58 |
| licm_div | loops | 61 | Constant Folding (CF), Common Subexpression Elimination (CSE), Loop-Invariant Code Motion (LICM), Strength Reduction (SR) | **x2.63** | x2.42 |
| matrix_mult | numeric | 12 | Common Subexpression Elimination (CSE), Loop-Invariant Code Motion (LICM) | **x1.19** | x0.95 |
| nested_licm | loops | 11 | Constant Folding (CF), Dead Code Elimination (DCE), Loop-Invariant Code Motion (LICM) | **x1.70** | x1.56 |
| particle_sim | structs | 2 | Dead Code Elimination (DCE) | **x1.01** | x1.00 |
| polynomial | loops | 7 | Constant Folding (CF), Dead Code Elimination (DCE), Common Subexpression Elimination (CSE) | **x1.65** | x1.58 |
| prime_sieve | loops | 53 | Constant Folding (CF), Common Subexpression Elimination (CSE), Strength Reduction (SR) | **x1.07** | x1.03 |
| stencil_1d | numeric | 14 | Dead Code Elimination (DCE), Common Subexpression Elimination (CSE), Loop-Invariant Code Motion (LICM) | **x1.07** | x1.03 |
| strength_reduce | loops | 15 | Constant Folding (CF), Dead Code Elimination (DCE), Common Subexpression Elimination (CSE), Loop-Invariant Code Motion (LICM) | **x1.01** | x0.83 |
| vector_scale | numeric | 63 | Constant Folding (CF), Dead Code Elimination (DCE), Common Subexpression Elimination (CSE), Loop-Invariant Code Motion (LICM), Strength Reduction (SR) | **x1.29** | x1.29 |
| vowel_count | strings | 43 | Constant Folding (CF), Dead Code Elimination (DCE), Loop-Invariant Code Motion (LICM) | **x1.01** | x0.97 |
