# MiniC optimizer: measured speedup results

**900 MiniC benchmarks**, each emitted as C at every one of the **64 pass combinations** (6 independently toggleable passes), compiled with **`gcc -O0`**, and timed (least of 15 wall-clock runs after 4 warm-ups -- the least-interfered sample, since the sweep runs programs in parallel).

`speedup = time(combo 0, no passes) / time(combo)` -- how much the MiniC TAC optimizer beats *not* optimizing, with the C compiler pinned at `-O0` so the measured gain is ours, not gcc's.

## Headline

- **Best combo per program, geomean speedup: x1.31**  (max **x4.37**)
- All 6 passes on (combo 63): geomean x1.19
- There is no safe fixed set of passes to always enable: every non-empty combo regresses more than 3% on at least one program.
- No single combo is best everywhere: the all-passes combo is left on the table (>2% slower than the per-program best) on **715 / 900** programs -- which is why a per-program recommender is worth having.

### by category (best-combo geomean)

- structs: x2.70
- loops: x1.75
- numeric: x1.36
- strings: x1.35
- generated: x1.29
- recursion: x1.13

## ML recommendation (abstain-margin recommender, GroupKFold by program_id)

Cross-validation holds *whole programs* out -- a program's rows share identical static features, so a random split would leak. The selection strategy is itself cross-validated: from plain argmax, an abstain-margin sweep, and per-pass classifiers, the winner is the most useful recommender that keeps regressions under 10%.

- Model: **hist gradient boosting**, 900 held-out programs (900 programs, 5 folds)
- Speedup-prediction MAE: 0.105
- Recommendations that regress the program (>2% slower than baseline): **9%**
- **Model-recommended combo, mean true speedup on unseen programs: x1.21**
- Baseline (combo 0): x1.00   |   oracle (best combo in hindsight): x1.33
- Model captures **62%** of the available speedup without ever having timed the program.

## Per-program

| program | category | best combo | passes | best speedup | all-on |
|---|---|--:|---|--:|--:|
| complex_arith | structs | 62 | DCE, CSE, LICM, SR, LU | **x4.37** | x4.15 |
| licm_div | loops | 47 | CF, DCE, CSE, LICM, LU | **x4.04** | x3.94 |
| distance_accum | structs | 62 | DCE, CSE, LICM, SR, LU | **x3.34** | x3.33 |
| bbox | structs | 63 | CF, DCE, CSE, LICM, SR, LU | **x3.27** | x3.27 |
| const_fold | loops | 39 | CF, DCE, CSE, LU | **x2.43** | x2.31 |
| g_nested_339 | generated | 63 | CF, DCE, CSE, LICM, SR, LU | **x2.39** | x2.39 |
| g_nested_229 | generated | 63 | CF, DCE, CSE, LICM, SR, LU | **x2.37** | x2.37 |
| g_recur_241 | generated | 50 | DCE, SR, LU | **x2.37** | x2.08 |
| g_nested_009 | generated | 63 | CF, DCE, CSE, LICM, SR, LU | **x2.36** | x2.36 |
| g_nested_163 | generated | 46 | DCE, CSE, LICM, LU | **x2.35** | x2.33 |
| g_recur_153 | generated | 40 | LICM, LU | **x2.34** | x0.95 |
| g_div_015 | generated | 15 | CF, DCE, CSE, LICM | **x2.30** | x2.16 |
| cse_subexpr | loops | 46 | DCE, CSE, LICM, LU | **x2.27** | x2.04 |
| cse_mod | loops | 46 | DCE, CSE, LICM, LU | **x2.19** | x2.00 |
| g_div_202 | generated | 51 | CF, DCE, SR, LU | **x2.19** | x2.01 |
| g_div_246 | generated | 30 | DCE, CSE, LICM, SR | **x2.18** | x2.03 |
| g_div_301 | generated | 55 | CF, DCE, CSE, SR, LU | **x2.15** | x2.14 |
| g_nested_152 | generated | 63 | CF, DCE, CSE, LICM, SR, LU | **x2.14** | x2.14 |
| g_nested_185 | generated | 63 | CF, DCE, CSE, LICM, SR, LU | **x2.13** | x2.13 |
| g_div_224 | generated | 15 | CF, DCE, CSE, LICM | **x2.12** | x1.76 |
| g_cse_199 | generated | 55 | CF, DCE, CSE, SR, LU | **x2.10** | x1.83 |
| g_div_323 | generated | 46 | DCE, CSE, LICM, LU | **x2.10** | x1.89 |
| g_nested_240 | generated | 63 | CF, DCE, CSE, LICM, SR, LU | **x2.09** | x2.09 |
| g_div_092 | generated | 23 | CF, DCE, CSE, SR | **x2.09** | x2.07 |
| g_comp_173_div-cse-cse-recur | generated | 62 | DCE, CSE, LICM, SR, LU | **x2.08** | x1.80 |
| g_div_180 | generated | 30 | DCE, CSE, LICM, SR | **x2.07** | x1.95 |
| g_recur_054 | generated | 63 | CF, DCE, CSE, LICM, SR, LU | **x2.03** | x2.03 |
| g_div_345 | generated | 27 | CF, DCE, LICM, SR | **x2.02** | x1.97 |
| const_prop | loops | 63 | CF, DCE, CSE, LICM, SR, LU | **x2.00** | x2.00 |
| g_nested_020 | generated | 46 | DCE, CSE, LICM, LU | **x1.99** | x1.87 |
| g_div_125 | generated | 31 | CF, DCE, CSE, LICM, SR | **x1.97** | x1.82 |
| g_cse_320 | generated | 22 | DCE, CSE, SR | **x1.97** | x1.95 |
| g_nested_218 | generated | 55 | CF, DCE, CSE, SR, LU | **x1.97** | x1.79 |
| g_nested_273 | generated | 54 | DCE, CSE, SR, LU | **x1.94** | x1.89 |
| g_nested_251 | generated | 55 | CF, DCE, CSE, SR, LU | **x1.94** | x1.80 |
| g_div_235 | generated | 11 | CF, DCE, LICM | **x1.93** | x1.89 |
| g_div_026 | generated | 19 | CF, DCE, SR | **x1.93** | x1.87 |
| g_comp_455_neutral-nested | generated | 46 | DCE, CSE, LICM, LU | **x1.92** | x1.72 |
| g_nested_086 | generated | 63 | CF, DCE, CSE, LICM, SR, LU | **x1.91** | x1.91 |
| g_recur_010 | generated | 36 | CSE, LU | **x1.91** | x1.77 |
| g_div_268 | generated | 59 | CF, DCE, LICM, SR, LU | **x1.90** | x1.75 |
| g_cse_287 | generated | 31 | CF, DCE, CSE, LICM, SR | **x1.89** | x1.72 |
| g_comp_162_struct-recur-recur | generated | 62 | DCE, CSE, LICM, SR, LU | **x1.89** | x1.17 |
| g_div_059 | generated | 62 | DCE, CSE, LICM, SR, LU | **x1.89** | x1.80 |
| g_comp_340_nested-recur | generated | 43 | CF, DCE, LICM, LU | **x1.89** | x1.16 |
| g_div_312 | generated | 59 | CF, DCE, LICM, SR, LU | **x1.88** | x1.78 |
| g_recur_076 | generated | 56 | LICM, SR, LU | **x1.87** | x1.16 |
| g_div_147 | generated | 62 | DCE, CSE, LICM, SR, LU | **x1.87** | x1.84 |
| g_div_279 | generated | 59 | CF, DCE, LICM, SR, LU | **x1.87** | x1.82 |
| polynomial | loops | 47 | CF, DCE, CSE, LICM, LU | **x1.86** | x1.82 |
| g_nested_064 | generated | 55 | CF, DCE, CSE, SR, LU | **x1.86** | x1.66 |
| g_nested_317 | generated | 54 | DCE, CSE, SR, LU | **x1.86** | x1.85 |
| g_nested_196 | generated | 47 | CF, DCE, CSE, LICM, LU | **x1.85** | x1.69 |
| g_comp_257_recur-cse | generated | 47 | CF, DCE, CSE, LICM, LU | **x1.85** | x1.66 |
| g_comp_460_recur-nested-licm | generated | 59 | CF, DCE, LICM, SR, LU | **x1.82** | x1.15 |
| g_cse_078 | generated | 63 | CF, DCE, CSE, LICM, SR, LU | **x1.82** | x1.82 |
| g_div_169 | generated | 14 | DCE, CSE, LICM | **x1.81** | x1.78 |
| g_comp_121_cf-nested | generated | 63 | CF, DCE, CSE, LICM, SR, LU | **x1.81** | x1.81 |
| g_div_114 | generated | 55 | CF, DCE, CSE, SR, LU | **x1.80** | x1.65 |
| g_comp_057_recur-div-nested-nested | generated | 63 | CF, DCE, CSE, LICM, SR, LU | **x1.80** | x1.80 |
| g_div_004 | generated | 23 | CF, DCE, CSE, SR | **x1.79** | x1.56 |
| g_comp_048_struct-recur | generated | 39 | CF, DCE, CSE, LU | **x1.79** | x1.57 |
| g_div_048 | generated | 63 | CF, DCE, CSE, LICM, SR, LU | **x1.78** | x1.78 |
| g_nested_031 | generated | 55 | CF, DCE, CSE, SR, LU | **x1.78** | x1.76 |
| g_div_290 | generated | 43 | CF, DCE, LICM, LU | **x1.77** | x1.76 |
| g_comp_309_sr-licm | generated | 7 | CF, DCE, CSE | **x1.77** | x1.70 |
| nested_licm | loops | 55 | CF, DCE, CSE, SR, LU | **x1.77** | x1.71 |
| g_cse_276 | generated | 30 | DCE, CSE, LICM, SR | **x1.77** | x1.63 |
| g_div_191 | generated | 55 | CF, DCE, CSE, SR, LU | **x1.77** | x1.45 |
| g_comp_369_nested-recur-branch | generated | 38 | DCE, CSE, LU | **x1.77** | x1.08 |
| g_cse_331 | generated | 31 | CF, DCE, CSE, LICM, SR | **x1.76** | x1.74 |
| g_comp_227_nested-nested-cf-div | generated | 46 | DCE, CSE, LICM, LU | **x1.76** | x1.68 |
| licm_arith | loops | 27 | CF, DCE, LICM, SR | **x1.76** | x1.69 |
| cse_chain | loops | 54 | DCE, CSE, SR, LU | **x1.75** | x1.70 |
| g_comp_310_cse-struct-nested | generated | 63 | CF, DCE, CSE, LICM, SR, LU | **x1.74** | x1.74 |
| licm_mixed | loops | 62 | DCE, CSE, LICM, SR, LU | **x1.74** | x1.65 |
| g_cse_232 | generated | 62 | DCE, CSE, LICM, SR, LU | **x1.73** | x1.70 |
| g_nested_328 | generated | 47 | CF, DCE, CSE, LICM, LU | **x1.73** | x1.61 |
| g_comp_218_div-cse-nested | generated | 39 | CF, DCE, CSE, LU | **x1.73** | x1.65 |
| g_comp_041_recur-nested | generated | 34 | DCE, LU | **x1.73** | x1.54 |
| g_div_257 | generated | 59 | CF, DCE, LICM, SR, LU | **x1.73** | x1.70 |
| g_comp_198_recur-cf-nested | generated | 63 | CF, DCE, CSE, LICM, SR, LU | **x1.72** | x1.72 |
| g_div_103 | generated | 25 | CF, LICM, SR | **x1.72** | x1.54 |
| g_cse_067 | generated | 31 | CF, DCE, CSE, LICM, SR | **x1.72** | x1.53 |
| g_comp_145_branch-recur-cse | generated | 6 | DCE, CSE | **x1.72** | x1.00 |
| g_comp_398_cf-recur | generated | 15 | CF, DCE, CSE, LICM | **x1.70** | x1.45 |
| g_div_334 | generated | 55 | CF, DCE, CSE, SR, LU | **x1.70** | x1.68 |
| g_div_070 | generated | 62 | DCE, CSE, LICM, SR, LU | **x1.70** | x1.65 |
| g_cse_144 | generated | 30 | DCE, CSE, LICM, SR | **x1.69** | x1.57 |
| g_comp_335_branch-nested-cf-cse | generated | 55 | CF, DCE, CSE, SR, LU | **x1.69** | x1.63 |
| g_comp_283_struct-nested-recur | generated | 51 | CF, DCE, SR, LU | **x1.69** | x1.65 |
| g_cse_056 | generated | 38 | DCE, CSE, LU | **x1.69** | x1.46 |
| g_comp_383_div-div-cse-nested | generated | 63 | CF, DCE, CSE, LICM, SR, LU | **x1.69** | x1.69 |
| g_cse_133 | generated | 55 | CF, DCE, CSE, SR, LU | **x1.68** | x1.65 |
| g_comp_425_div-div-cf-branch | generated | 55 | CF, DCE, CSE, SR, LU | **x1.67** | x1.43 |
| g_nested_284 | generated | 54 | DCE, CSE, SR, LU | **x1.67** | x1.58 |
| g_comp_499_div-nested | generated | 63 | CF, DCE, CSE, LICM, SR, LU | **x1.67** | x1.67 |
| g_comp_514_branch-cf-recur-div | generated | 39 | CF, DCE, CSE, LU | **x1.66** | x1.04 |
| g_nested_119 | generated | 47 | CF, DCE, CSE, LICM, LU | **x1.66** | x1.60 |
| g_comp_432_recur-unroll | generated | 27 | CF, DCE, LICM, SR | **x1.66** | x1.62 |
| g_div_037 | generated | 55 | CF, DCE, CSE, SR, LU | **x1.66** | x1.57 |
| g_comp_392_sr-nested-sr | generated | 62 | DCE, CSE, LICM, SR, LU | **x1.66** | x1.62 |
| g_comp_471_div-nested-struct-cf | generated | 47 | CF, DCE, CSE, LICM, LU | **x1.66** | x1.57 |
| licm_cond | loops | 35 | CF, DCE, LU | **x1.66** | x1.51 |
| g_comp_045_div-licm-nested-nested | generated | 46 | DCE, CSE, LICM, LU | **x1.66** | x1.58 |
| vector_scale | numeric | 47 | CF, DCE, CSE, LICM, LU | **x1.66** | x1.37 |
| g_nested_262 | generated | 39 | CF, DCE, CSE, LU | **x1.66** | x1.53 |
| g_div_213 | generated | 51 | CF, DCE, SR, LU | **x1.65** | x1.32 |
| g_comp_386_nested-branch-cf | generated | 46 | DCE, CSE, LICM, LU | **x1.65** | x1.35 |
| g_cse_342 | generated | 22 | DCE, CSE, SR | **x1.65** | x1.42 |
| g_cse_210 | generated | 62 | DCE, CSE, LICM, SR, LU | **x1.65** | x1.52 |
| g_nested_306 | generated | 63 | CF, DCE, CSE, LICM, SR, LU | **x1.65** | x1.65 |
| g_cse_122 | generated | 31 | CF, DCE, CSE, LICM, SR | **x1.64** | x1.43 |
| g_comp_016_sr-cse | generated | 62 | DCE, CSE, LICM, SR, LU | **x1.63** | x1.55 |
| g_comp_230_sr-cse-div | generated | 31 | CF, DCE, CSE, LICM, SR | **x1.63** | x1.55 |
| g_comp_362_branch-cse-cf | generated | 47 | CF, DCE, CSE, LICM, LU | **x1.63** | x1.53 |
| g_comp_259_sr-branch-recur | generated | 39 | CF, DCE, CSE, LU | **x1.63** | x1.42 |
| g_comp_497_sr-cf | generated | 35 | CF, DCE, LU | **x1.63** | x1.62 |
| g_licm_044 | generated | 23 | CF, DCE, CSE, SR | **x1.62** | x1.50 |
| g_comp_417_cse-branch-recur-nested | generated | 38 | DCE, CSE, LU | **x1.62** | x1.02 |
| g_comp_189_unroll-cse | generated | 63 | CF, DCE, CSE, LICM, SR, LU | **x1.61** | x1.61 |
| g_cse_166 | generated | 14 | DCE, CSE, LICM | **x1.61** | x1.49 |
| g_comp_284_struct-nested-unroll-recur | generated | 55 | CF, DCE, CSE, SR, LU | **x1.61** | x1.38 |
| g_div_158 | generated | 19 | CF, DCE, SR | **x1.60** | x1.55 |
| g_nested_295 | generated | 47 | CF, DCE, CSE, LICM, LU | **x1.60** | x1.44 |
| g_comp_280_recur-sr-branch-unroll | generated | 30 | DCE, CSE, LICM, SR | **x1.60** | x1.17 |
| g_div_081 | generated | 30 | DCE, CSE, LICM, SR | **x1.60** | x1.30 |
| g_nested_075 | generated | 38 | DCE, CSE, LU | **x1.60** | x1.45 |
| g_cse_221 | generated | 31 | CF, DCE, CSE, LICM, SR | **x1.60** | x1.51 |
| g_div_136 | generated | 7 | CF, DCE, CSE | **x1.60** | x1.38 |
| g_comp_260_div-cse-div | generated | 30 | DCE, CSE, LICM, SR | **x1.60** | x1.54 |
| g_cse_023 | generated | 54 | DCE, CSE, SR, LU | **x1.59** | x1.54 |
| g_comp_328_nested-nested | generated | 46 | DCE, CSE, LICM, LU | **x1.59** | x1.51 |
| g_cf_036 | generated | 31 | CF, DCE, CSE, LICM, SR | **x1.59** | x1.54 |
| g_recur_164 | generated | 63 | CF, DCE, CSE, LICM, SR, LU | **x1.59** | x1.59 |
| g_cse_188 | generated | 47 | CF, DCE, CSE, LICM, LU | **x1.59** | x1.26 |
| g_comp_456_branch-cf-recur | generated | 63 | CF, DCE, CSE, LICM, SR, LU | **x1.59** | x1.59 |
| g_cse_001 | generated | 6 | DCE, CSE | **x1.58** | x1.57 |
| g_cf_014 | generated | 43 | CF, DCE, LICM, LU | **x1.58** | x1.57 |
| g_licm_110 | generated | 35 | CF, DCE, LU | **x1.58** | x1.55 |
| g_comp_308_div-struct-div | generated | 47 | CF, DCE, CSE, LICM, LU | **x1.57** | x1.46 |
| g_comp_446_licm-nested-div | generated | 55 | CF, DCE, CSE, SR, LU | **x1.57** | x1.50 |
| g_licm_264 | generated | 15 | CF, DCE, CSE, LICM | **x1.57** | x1.48 |
| g_cse_309 | generated | 63 | CF, DCE, CSE, LICM, SR, LU | **x1.57** | x1.57 |
| g_comp_345_cse-div | generated | 23 | CF, DCE, CSE, SR | **x1.57** | x1.36 |
| g_cf_267 | generated | 15 | CF, DCE, CSE, LICM | **x1.57** | x1.55 |
| g_licm_187 | generated | 7 | CF, DCE, CSE | **x1.57** | x1.52 |
| g_comp_219_cse-cse-struct-cf | generated | 62 | DCE, CSE, LICM, SR, LU | **x1.57** | x1.50 |
| g_comp_047_unroll-cse-cf | generated | 47 | CF, DCE, CSE, LICM, LU | **x1.56** | x1.48 |
| g_comp_199_recur-branch-div | generated | 11 | CF, DCE, LICM | **x1.55** | x1.17 |
| g_comp_344_nested-div-branch | generated | 45 | CF, CSE, LICM, LU | **x1.55** | x1.51 |
| g_cse_243 | generated | 30 | DCE, CSE, LICM, SR | **x1.55** | x1.55 |
| g_cf_003 | generated | 3 | CF, DCE | **x1.55** | x1.41 |
| g_licm_242 | generated | 9 | CF, LICM | **x1.55** | x1.43 |
| g_comp_396_nested-nested-div | generated | 46 | DCE, CSE, LICM, LU | **x1.55** | x1.38 |
| g_comp_441_recur-recur | generated | 7 | CF, DCE, CSE | **x1.55** | x1.43 |
| g_comp_029_recur-branch-nested | generated | 38 | DCE, CSE, LU | **x1.54** | x1.02 |
| g_comp_030_cse-div-branch | generated | 31 | CF, DCE, CSE, LICM, SR | **x1.54** | x1.45 |
| g_comp_157_cf-licm-div | generated | 31 | CF, DCE, CSE, LICM, SR | **x1.54** | x1.28 |
| g_licm_088 | generated | 11 | CF, DCE, LICM | **x1.54** | x1.52 |
| g_comp_123_div-licm-nested-div | generated | 55 | CF, DCE, CSE, SR, LU | **x1.54** | x1.45 |
| caesar | strings | 47 | CF, DCE, CSE, LICM, LU | **x1.54** | x1.42 |
| g_comp_104_cse-recur-cf | generated | 15 | CF, DCE, CSE, LICM | **x1.54** | x1.06 |
| dotprod | numeric | 46 | DCE, CSE, LICM, LU | **x1.54** | x1.43 |
| g_cf_080 | generated | 31 | CF, DCE, CSE, LICM, SR | **x1.53** | x1.43 |
| g_cse_155 | generated | 62 | DCE, CSE, LICM, SR, LU | **x1.53** | x1.35 |
| g_comp_073_licm-recur-neutral-unroll | generated | 39 | CF, DCE, CSE, LU | **x1.53** | x1.19 |
| g_licm_220 | generated | 47 | CF, DCE, CSE, LICM, LU | **x1.52** | x1.27 |
| g_comp_334_licm-nested-licm | generated | 39 | CF, DCE, CSE, LU | **x1.52** | x1.52 |
| g_comp_483_cse-struct-div-div | generated | 39 | CF, DCE, CSE, LU | **x1.52** | x1.41 |
| g_comp_476_neutral-recur-cf-cf | generated | 25 | CF, LICM, SR | **x1.52** | x1.47 |
| g_comp_087_nested-licm | generated | 39 | CF, DCE, CSE, LU | **x1.52** | x1.51 |
| g_comp_214_cf-cse | generated | 23 | CF, DCE, CSE, SR | **x1.52** | x1.27 |
| g_cse_089 | generated | 63 | CF, DCE, CSE, LICM, SR, LU | **x1.52** | x1.52 |
| g_cse_034 | generated | 54 | DCE, CSE, SR, LU | **x1.52** | x1.44 |
| g_cf_333 | generated | 3 | CF, DCE | **x1.52** | x1.42 |
| g_comp_170_cse-recur | generated | 23 | CF, DCE, CSE, SR | **x1.52** | x1.15 |
| g_cse_012 | generated | 63 | CF, DCE, CSE, LICM, SR, LU | **x1.52** | x1.52 |
| g_comp_421_struct-struct-recur-cse | generated | 22 | DCE, CSE, SR | **x1.52** | x1.21 |
| g_cf_025 | generated | 31 | CF, DCE, CSE, LICM, SR | **x1.51** | x1.50 |
| g_comp_348_unroll-cse-cse-cse | generated | 23 | CF, DCE, CSE, SR | **x1.51** | x1.47 |
| g_comp_082_sr-div-recur | generated | 30 | DCE, CSE, LICM, SR | **x1.51** | x1.09 |
| g_comp_299_nested-struct | generated | 63 | CF, DCE, CSE, LICM, SR, LU | **x1.51** | x1.51 |
| g_comp_133_cf-div-cf-branch | generated | 3 | CF, DCE | **x1.51** | x1.44 |
| g_comp_107_cse-div | generated | 63 | CF, DCE, CSE, LICM, SR, LU | **x1.50** | x1.50 |
| g_comp_454_cse-licm-recur | generated | 55 | CF, DCE, CSE, SR, LU | **x1.50** | x1.40 |
| g_comp_306_div-recur-cf | generated | 45 | CF, CSE, LICM, LU | **x1.50** | x1.43 |
| g_comp_132_cf-recur-licm | generated | 27 | CF, DCE, LICM, SR | **x1.50** | x1.43 |
| g_cse_254 | generated | 6 | DCE, CSE | **x1.50** | x1.41 |
| g_cf_146 | generated | 43 | CF, DCE, LICM, LU | **x1.50** | x1.34 |
| g_comp_014_recur-cf-nested-div | generated | 63 | CF, DCE, CSE, LICM, SR, LU | **x1.50** | x1.50 |
| g_comp_379_cf-recur | generated | 3 | CF, DCE | **x1.49** | x1.26 |
| g_comp_294_div-struct-licm | generated | 39 | CF, DCE, CSE, LU | **x1.49** | x1.24 |
| g_comp_080_unroll-recur-div | generated | 63 | CF, DCE, CSE, LICM, SR, LU | **x1.49** | x1.49 |
| g_comp_256_div-div-struct-cf | generated | 15 | CF, DCE, CSE, LICM | **x1.49** | x1.40 |
| g_comp_188_struct-cse-branch-div | generated | 63 | CF, DCE, CSE, LICM, SR, LU | **x1.49** | x1.49 |
| g_comp_027_branch-nested-unroll-recur | generated | 40 | LICM, LU | **x1.49** | x1.19 |
| g_comp_172_branch-div-licm | generated | 47 | CF, DCE, CSE, LICM, LU | **x1.49** | x1.25 |
| g_comp_096_cf-cf-unroll-branch | generated | 31 | CF, DCE, CSE, LICM, SR | **x1.49** | x1.37 |
| g_cf_201 | generated | 51 | CF, DCE, SR, LU | **x1.49** | x1.44 |
| g_comp_175_cse-licm-licm-div | generated | 63 | CF, DCE, CSE, LICM, SR, LU | **x1.48** | x1.48 |
| g_comp_301_div-recur | generated | 41 | CF, LICM, LU | **x1.48** | x1.33 |
| g_cf_311 | generated | 27 | CF, DCE, LICM, SR | **x1.48** | x1.41 |
| g_comp_480_nested-licm-cf-cf | generated | 35 | CF, DCE, LU | **x1.48** | x1.46 |
| g_cse_100 | generated | 23 | CF, DCE, CSE, SR | **x1.48** | x1.18 |
| g_cf_289 | generated | 31 | CF, DCE, CSE, LICM, SR | **x1.48** | x1.47 |
| g_comp_281_nested-neutral-nested | generated | 63 | CF, DCE, CSE, LICM, SR, LU | **x1.47** | x1.47 |
| g_cf_234 | generated | 15 | CF, DCE, CSE, LICM | **x1.47** | x1.42 |
| g_comp_412_cse-struct-nested | generated | 46 | DCE, CSE, LICM, LU | **x1.47** | x1.39 |
| g_comp_413_sr-recur | generated | 22 | DCE, CSE, SR | **x1.47** | x0.86 |
| g_comp_359_recur-branch | generated | 13 | CF, CSE, LICM | **x1.46** | x1.07 |
| g_comp_464_struct-licm-div | generated | 47 | CF, DCE, CSE, LICM, LU | **x1.46** | x1.31 |
| g_comp_295_neutral-neutral-div-struct | generated | 15 | CF, DCE, CSE, LICM | **x1.46** | x1.34 |
| g_comp_279_unroll-nested-cse | generated | 46 | DCE, CSE, LICM, LU | **x1.46** | x1.42 |
| g_comp_009_struct-cf | generated | 55 | CF, DCE, CSE, SR, LU | **x1.46** | x1.37 |
| g_comp_506_div-branch-branch | generated | 46 | DCE, CSE, LICM, LU | **x1.45** | x1.28 |
| g_licm_319 | generated | 57 | CF, LICM, SR, LU | **x1.45** | x1.38 |
| g_comp_275_struct-cse-div | generated | 46 | DCE, CSE, LICM, LU | **x1.45** | x1.16 |
| g_comp_415_branch-nested-neutral-cse | generated | 47 | CF, DCE, CSE, LICM, LU | **x1.45** | x1.36 |
| g_cf_124 | generated | 27 | CF, DCE, LICM, SR | **x1.45** | x1.31 |
| g_comp_241_cf-struct-nested-cse | generated | 46 | DCE, CSE, LICM, LU | **x1.45** | x1.25 |
| g_comp_520_div-nested | generated | 47 | CF, DCE, CSE, LICM, LU | **x1.45** | x1.34 |
| g_comp_263_licm-struct | generated | 63 | CF, DCE, CSE, LICM, SR, LU | **x1.45** | x1.45 |
| g_comp_011_div-cse-div | generated | 55 | CF, DCE, CSE, SR, LU | **x1.45** | x1.40 |
| g_licm_022 | generated | 7 | CF, DCE, CSE | **x1.45** | x1.40 |
| g_comp_469_cse-div-cf-licm | generated | 39 | CF, DCE, CSE, LU | **x1.45** | x1.25 |
| g_comp_478_branch-cse | generated | 23 | CF, DCE, CSE, SR | **x1.44** | x1.40 |
| g_cf_223 | generated | 19 | CF, DCE, SR | **x1.44** | x1.29 |
| g_comp_247_neutral-licm-cf | generated | 15 | CF, DCE, CSE, LICM | **x1.44** | x1.35 |
| g_cse_298 | generated | 7 | CF, DCE, CSE | **x1.44** | x1.40 |
| g_comp_220_cf-licm-sr-licm | generated | 27 | CF, DCE, LICM, SR | **x1.44** | x1.16 |
| g_cf_157 | generated | 55 | CF, DCE, CSE, SR, LU | **x1.44** | x1.29 |
| g_comp_193_recur-branch-licm | generated | 51 | CF, DCE, SR, LU | **x1.44** | x1.40 |
| g_licm_341 | generated | 55 | CF, DCE, CSE, SR, LU | **x1.44** | x1.40 |
| g_comp_371_cf-branch-nested | generated | 39 | CF, DCE, CSE, LU | **x1.44** | x1.23 |
| g_comp_338_nested-recur | generated | 58 | DCE, LICM, SR, LU | **x1.43** | x1.41 |
| g_comp_213_licm-cf | generated | 15 | CF, DCE, CSE, LICM | **x1.43** | x1.32 |
| g_nested_141 | generated | 46 | DCE, CSE, LICM, LU | **x1.43** | x1.35 |
| g_nested_174 | generated | 46 | DCE, CSE, LICM, LU | **x1.43** | x1.27 |
| g_comp_429_div-licm-cf | generated | 11 | CF, DCE, LICM | **x1.43** | x1.41 |
| g_comp_254_recur-unroll-div-nested | generated | 63 | CF, DCE, CSE, LICM, SR, LU | **x1.43** | x1.43 |
| g_comp_461_div-neutral-div-cse | generated | 62 | DCE, CSE, LICM, SR, LU | **x1.42** | x1.33 |
| g_comp_074_unroll-nested | generated | 39 | CF, DCE, CSE, LU | **x1.42** | x1.32 |
| g_comp_179_cf-struct-struct-cf | generated | 15 | CF, DCE, CSE, LICM | **x1.42** | x1.36 |
| g_cse_177 | generated | 15 | CF, DCE, CSE, LICM | **x1.42** | x1.32 |
| g_comp_012_recur-licm | generated | 47 | CF, DCE, CSE, LICM, LU | **x1.42** | x0.99 |
| g_comp_411_licm-sr-cf-div | generated | 46 | DCE, CSE, LICM, LU | **x1.41** | x1.40 |
| g_recur_329 | generated | 55 | CF, DCE, CSE, SR, LU | **x1.41** | x1.18 |
| g_comp_181_nested-nested-unroll | generated | 39 | CF, DCE, CSE, LU | **x1.41** | x1.20 |
| g_comp_311_cse-nested | generated | 39 | CF, DCE, CSE, LU | **x1.41** | x1.34 |
| g_comp_138_neutral-nested | generated | 39 | CF, DCE, CSE, LU | **x1.41** | x1.32 |
| g_comp_361_nested-nested-cf-struct | generated | 63 | CF, DCE, CSE, LICM, SR, LU | **x1.41** | x1.41 |
| g_comp_131_nested-branch-licm | generated | 47 | CF, DCE, CSE, LICM, LU | **x1.41** | x1.24 |
| g_comp_153_div-struct | generated | 62 | DCE, CSE, LICM, SR, LU | **x1.41** | x1.34 |
| g_licm_286 | generated | 19 | CF, DCE, SR | **x1.41** | x1.37 |
| g_comp_146_div-licm-cse | generated | 23 | CF, DCE, CSE, SR | **x1.41** | x1.23 |
| g_comp_248_cf-neutral-nested-cf | generated | 63 | CF, DCE, CSE, LICM, SR, LU | **x1.41** | x1.41 |
| g_licm_099 | generated | 15 | CF, DCE, CSE, LICM | **x1.41** | x1.33 |
| g_licm_253 | generated | 25 | CF, LICM, SR | **x1.41** | x1.39 |
| g_comp_312_struct-cse-neutral-nested | generated | 54 | DCE, CSE, SR, LU | **x1.40** | x1.28 |
| g_comp_296_div-nested | generated | 46 | DCE, CSE, LICM, LU | **x1.40** | x1.15 |
| g_comp_161_recur-struct-branch-branch | generated | 54 | DCE, CSE, SR, LU | **x1.40** | x1.20 |
| g_comp_125_branch-nested | generated | 46 | DCE, CSE, LICM, LU | **x1.40** | x1.39 |
| g_comp_077_struct-sr-recur-cf | generated | 14 | DCE, CSE, LICM | **x1.40** | x1.32 |
| g_comp_427_sr-recur-div | generated | 9 | CF, LICM | **x1.40** | x1.35 |
| g_comp_341_recur-sr-cf-cf | generated | 13 | CF, CSE, LICM | **x1.39** | x1.32 |
| g_comp_510_cf-nested-neutral | generated | 54 | DCE, CSE, SR, LU | **x1.39** | x1.25 |
| g_comp_395_cf-struct | generated | 19 | CF, DCE, SR | **x1.39** | x1.32 |
| g_comp_208_recur-cse | generated | 5 | CF, CSE | **x1.39** | x1.17 |
| g_comp_258_unroll-licm-cf-unroll | generated | 51 | CF, DCE, SR, LU | **x1.39** | x1.36 |
| g_cse_045 | generated | 55 | CF, DCE, CSE, SR, LU | **x1.39** | x1.15 |
| g_comp_403_licm-licm | generated | 13 | CF, CSE, LICM | **x1.39** | x1.38 |
| g_comp_025_recur-struct-sr | generated | 39 | CF, DCE, CSE, LU | **x1.39** | x1.03 |
| g_cf_091 | generated | 15 | CF, DCE, CSE, LICM | **x1.39** | x1.30 |
| g_comp_377_div-licm-neutral | generated | 41 | CF, LICM, LU | **x1.39** | x1.25 |
| g_cse_111 | generated | 39 | CF, DCE, CSE, LU | **x1.39** | x1.18 |
| g_comp_389_neutral-branch-div-recur | generated | 23 | CF, DCE, CSE, SR | **x1.39** | x1.13 |
| g_cf_300 | generated | 15 | CF, DCE, CSE, LICM | **x1.39** | x1.39 |
| g_comp_490_cse-sr-recur | generated | 55 | CF, DCE, CSE, SR, LU | **x1.38** | x1.22 |
| g_comp_292_licm-cse-div | generated | 39 | CF, DCE, CSE, LU | **x1.38** | x1.20 |
| g_comp_261_cf-licm-nested | generated | 59 | CF, DCE, LICM, SR, LU | **x1.38** | x1.34 |
| g_comp_273_sr-neutral-cse-cf | generated | 39 | CF, DCE, CSE, LU | **x1.38** | x1.36 |
| g_comp_238_div-recur | generated | 35 | CF, DCE, LU | **x1.38** | x1.31 |
| g_comp_171_cf-licm | generated | 19 | CF, DCE, SR | **x1.37** | x1.20 |
| g_comp_365_div-div-licm | generated | 15 | CF, DCE, CSE, LICM | **x1.37** | x1.28 |
| g_comp_166_branch-div-licm | generated | 63 | CF, DCE, CSE, LICM, SR, LU | **x1.37** | x1.37 |
| g_comp_426_neutral-div | generated | 14 | DCE, CSE, LICM | **x1.37** | x1.30 |
| g_comp_003_cf-nested | generated | 63 | CF, DCE, CSE, LICM, SR, LU | **x1.37** | x1.37 |
| g_comp_496_sr-div | generated | 41 | CF, LICM, LU | **x1.37** | x1.27 |
| g_comp_302_sr-cse-cf | generated | 39 | CF, DCE, CSE, LU | **x1.37** | x1.34 |
| g_cf_322 | generated | 51 | CF, DCE, SR, LU | **x1.37** | x1.16 |
| g_nested_130 | generated | 36 | CSE, LU | **x1.37** | x1.28 |
| g_cf_212 | generated | 19 | CF, DCE, SR | **x1.37** | x1.33 |
| g_comp_317_cf-div-div-struct | generated | 15 | CF, DCE, CSE, LICM | **x1.36** | x1.24 |
| g_comp_033_sr-sr | generated | 2 | DCE | **x1.36** | x1.11 |
| g_licm_165 | generated | 35 | CF, DCE, LU | **x1.36** | x1.33 |
| g_cf_344 | generated | 27 | CF, DCE, LICM, SR | **x1.36** | x1.35 |
| g_comp_160_div-unroll-cse-licm | generated | 31 | CF, DCE, CSE, LICM, SR | **x1.36** | x1.30 |
| g_comp_066_sr-nested-nested | generated | 46 | DCE, CSE, LICM, LU | **x1.36** | x1.13 |
| g_comp_084_licm-licm-struct-cse | generated | 55 | CF, DCE, CSE, SR, LU | **x1.36** | x1.33 |
| g_nested_097 | generated | 63 | CF, DCE, CSE, LICM, SR, LU | **x1.36** | x1.36 |
| g_licm_330 | generated | 57 | CF, LICM, SR, LU | **x1.36** | x1.28 |
| stencil_1d | numeric | 63 | CF, DCE, CSE, LICM, SR, LU | **x1.36** | x1.36 |
| g_comp_196_cf-struct-cse-unroll | generated | 62 | DCE, CSE, LICM, SR, LU | **x1.36** | x1.32 |
| g_comp_086_div-unroll-unroll-struct | generated | 23 | CF, DCE, CSE, SR | **x1.35** | x1.28 |
| g_comp_112_struct-cse-licm-cf | generated | 31 | CF, DCE, CSE, LICM, SR | **x1.35** | x1.24 |
| g_comp_500_nested-cse | generated | 62 | DCE, CSE, LICM, SR, LU | **x1.35** | x1.10 |
| g_comp_502_recur-struct-neutral | generated | 9 | CF, LICM | **x1.35** | x0.99 |
| g_comp_266_cf-struct-div | generated | 15 | CF, DCE, CSE, LICM | **x1.35** | x1.26 |
| g_comp_090_div-neutral-recur-cse | generated | 7 | CF, DCE, CSE | **x1.35** | x1.07 |
| g_licm_066 | generated | 41 | CF, LICM, LU | **x1.35** | x1.32 |
| g_licm_275 | generated | 23 | CF, DCE, CSE, SR | **x1.35** | x1.33 |
| g_cf_168 | generated | 63 | CF, DCE, CSE, LICM, SR, LU | **x1.35** | x1.35 |
| g_branch_272 | generated | 46 | DCE, CSE, LICM, LU | **x1.35** | x1.26 |
| g_comp_154_nested-unroll-cse-licm | generated | 23 | CF, DCE, CSE, SR | **x1.35** | x1.22 |
| g_comp_434_licm-nested | generated | 39 | CF, DCE, CSE, LU | **x1.34** | x1.32 |
| g_comp_034_licm-recur-nested-struct | generated | 59 | CF, DCE, LICM, SR, LU | **x1.34** | x1.00 |
| g_comp_287_unroll-recur-div-struct | generated | 39 | CF, DCE, CSE, LU | **x1.34** | x1.25 |
| g_comp_232_cse-nested-struct | generated | 54 | DCE, CSE, SR, LU | **x1.34** | x1.23 |
| g_comp_044_licm-nested-sr | generated | 63 | CF, DCE, CSE, LICM, SR, LU | **x1.34** | x1.34 |
| g_comp_380_nested-neutral-cse-nested | generated | 54 | DCE, CSE, SR, LU | **x1.34** | x1.25 |
| g_comp_290_nested-branch | generated | 47 | CF, DCE, CSE, LICM, LU | **x1.34** | x1.06 |
| g_cf_190 | generated | 39 | CF, DCE, CSE, LU | **x1.34** | x1.29 |
| g_branch_305 | generated | 35 | CF, DCE, LU | **x1.34** | x1.24 |
| g_comp_274_div-div-nested | generated | 35 | CF, DCE, LU | **x1.34** | x1.23 |
| g_comp_353_cse-cse-sr | generated | 55 | CF, DCE, CSE, SR, LU | **x1.34** | x1.11 |
| g_comp_236_licm-recur | generated | 44 | CSE, LICM, LU | **x1.34** | x1.08 |
| g_comp_046_recur-branch-sr | generated | 62 | DCE, CSE, LICM, SR, LU | **x1.34** | x1.19 |
| g_comp_053_div-cf-licm | generated | 47 | CF, DCE, CSE, LICM, LU | **x1.34** | x1.28 |
| g_comp_331_licm-licm-branch | generated | 51 | CF, DCE, SR, LU | **x1.33** | x1.31 |
| g_comp_276_recur-unroll | generated | 43 | CF, DCE, LICM, LU | **x1.33** | x0.97 |
| g_comp_178_nested-cf-recur-licm | generated | 62 | DCE, CSE, LICM, SR, LU | **x1.33** | x1.26 |
| g_comp_492_cse-div | generated | 31 | CF, DCE, CSE, LICM, SR | **x1.33** | x1.07 |
| g_comp_068_struct-branch-recur-cf | generated | 31 | CF, DCE, CSE, LICM, SR | **x1.33** | x1.10 |
| g_comp_139_cf-recur-recur-licm | generated | 15 | CF, DCE, CSE, LICM | **x1.33** | x1.25 |
| g_comp_239_licm-div | generated | 57 | CF, LICM, SR, LU | **x1.33** | x1.27 |
| g_comp_249_struct-branch-nested-cf | generated | 55 | CF, DCE, CSE, SR, LU | **x1.33** | x1.22 |
| g_branch_074 | generated | 38 | DCE, CSE, LU | **x1.33** | x1.22 |
| g_nested_207 | generated | 35 | CF, DCE, LU | **x1.33** | x1.23 |
| g_comp_376_div-recur | generated | 59 | CF, DCE, LICM, SR, LU | **x1.33** | x1.27 |
| g_comp_489_branch-cse-recur-nested | generated | 52 | CSE, SR, LU | **x1.33** | x0.81 |
| g_comp_504_struct-licm-struct-cf | generated | 55 | CF, DCE, CSE, SR, LU | **x1.33** | x1.21 |
| g_comp_021_licm-nested | generated | 55 | CF, DCE, CSE, SR, LU | **x1.32** | x1.31 |
| g_comp_105_neutral-div | generated | 35 | CF, DCE, LU | **x1.32** | x1.01 |
| g_comp_355_struct-struct-recur | generated | 39 | CF, DCE, CSE, LU | **x1.32** | x1.17 |
| g_licm_132 | generated | 45 | CF, CSE, LICM, LU | **x1.32** | x1.31 |
| g_cf_058 | generated | 31 | CF, DCE, CSE, LICM, SR | **x1.32** | x1.31 |
| g_comp_022_branch-div-neutral-nested | generated | 47 | CF, DCE, CSE, LICM, LU | **x1.32** | x1.25 |
| g_licm_011 | generated | 51 | CF, DCE, SR, LU | **x1.32** | x1.30 |
| g_recur_230 | generated | 26 | DCE, LICM, SR | **x1.32** | x1.23 |
| g_licm_143 | generated | 63 | CF, DCE, CSE, LICM, SR, LU | **x1.32** | x1.32 |
| g_comp_518_div-cse | generated | 39 | CF, DCE, CSE, LU | **x1.32** | x1.30 |
| g_branch_140 | generated | 11 | CF, DCE, LICM | **x1.32** | x1.00 |
| g_comp_384_cf-div-neutral | generated | 57 | CF, LICM, SR, LU | **x1.32** | x1.17 |
| g_comp_144_struct-div-cf-licm | generated | 3 | CF, DCE | **x1.32** | x1.22 |
| g_comp_399_licm-unroll-nested-struct | generated | 46 | DCE, CSE, LICM, LU | **x1.32** | x1.26 |
| g_comp_512_licm-unroll-struct-licm | generated | 47 | CF, DCE, CSE, LICM, LU | **x1.32** | x1.19 |
| g_comp_035_licm-nested-cf | generated | 39 | CF, DCE, CSE, LU | **x1.32** | x1.02 |
| g_comp_110_licm-branch-div-struct | generated | 47 | CF, DCE, CSE, LICM, LU | **x1.32** | x1.23 |
| g_comp_163_struct-unroll-recur-neutral | generated | 50 | DCE, SR, LU | **x1.32** | x1.16 |
| g_nested_042 | generated | 38 | DCE, CSE, LU | **x1.31** | x1.14 |
| g_cf_256 | generated | 19 | CF, DCE, SR | **x1.31** | x1.16 |
| g_cf_278 | generated | 43 | CF, DCE, LICM, LU | **x1.31** | x1.19 |
| g_comp_458_cf-branch-cse | generated | 46 | DCE, CSE, LICM, LU | **x1.31** | x1.24 |
| g_comp_113_cse-licm-neutral-licm | generated | 47 | CF, DCE, CSE, LICM, LU | **x1.31** | x1.29 |
| g_comp_128_div-recur-sr-sr | generated | 62 | DCE, CSE, LICM, SR, LU | **x1.31** | x0.83 |
| g_cf_135 | generated | 47 | CF, DCE, CSE, LICM, LU | **x1.31** | x1.30 |
| g_comp_407_cse-cf | generated | 39 | CF, DCE, CSE, LU | **x1.31** | x1.13 |
| g_licm_176 | generated | 19 | CF, DCE, SR | **x1.31** | x1.24 |
| g_comp_519_cse-nested | generated | 46 | DCE, CSE, LICM, LU | **x1.31** | x1.22 |
| g_comp_272_licm-unroll | generated | 55 | CF, DCE, CSE, SR, LU | **x1.31** | x1.09 |
| g_comp_330_cse-unroll-cse | generated | 7 | CF, DCE, CSE | **x1.31** | x1.08 |
| g_comp_194_cse-cse-sr | generated | 31 | CF, DCE, CSE, LICM, SR | **x1.31** | x1.21 |
| g_recur_120 | generated | 18 | DCE, SR | **x1.31** | x1.21 |
| g_licm_154 | generated | 61 | CF, CSE, LICM, SR, LU | **x1.31** | x1.30 |
| g_recur_043 | generated | 5 | CF, CSE | **x1.31** | x0.75 |
| g_comp_462_recur-licm | generated | 7 | CF, DCE, CSE | **x1.31** | x0.93 |
| g_recur_109 | generated | 14 | DCE, CSE, LICM | **x1.31** | x0.72 |
| g_recur_098 | generated | 46 | DCE, CSE, LICM, LU | **x1.30** | x0.91 |
| g_comp_482_unroll-licm | generated | 57 | CF, LICM, SR, LU | **x1.30** | x1.19 |
| g_licm_297 | generated | 43 | CF, DCE, LICM, LU | **x1.30** | x1.25 |
| g_comp_324_struct-licm-sr | generated | 63 | CF, DCE, CSE, LICM, SR, LU | **x1.30** | x1.30 |
| g_comp_130_branch-licm-neutral | generated | 59 | CF, DCE, LICM, SR, LU | **x1.30** | x1.12 |
| g_comp_135_recur-licm-cf | generated | 45 | CF, CSE, LICM, LU | **x1.30** | x0.86 |
| g_comp_203_sr-branch-div-struct | generated | 63 | CF, DCE, CSE, LICM, SR, LU | **x1.30** | x1.30 |
| g_comp_463_recur-sr-neutral-nested | generated | 38 | DCE, CSE, LU | **x1.30** | x1.16 |
| g_cf_047 | generated | 51 | CF, DCE, SR, LU | **x1.30** | x1.23 |
| g_comp_183_recur-sr | generated | 15 | CF, DCE, CSE, LICM | **x1.30** | x1.13 |
| g_comp_004_sr-unroll | generated | 58 | DCE, LICM, SR, LU | **x1.30** | x1.22 |
| g_comp_020_licm-cf-sr-unroll | generated | 59 | CF, DCE, LICM, SR, LU | **x1.30** | x1.25 |
| g_comp_343_unroll-branch | generated | 44 | CSE, LICM, LU | **x1.30** | x1.09 |
| g_comp_391_branch-branch-cse | generated | 15 | CF, DCE, CSE, LICM | **x1.30** | x0.69 |
| g_comp_190_licm-neutral | generated | 59 | CF, DCE, LICM, SR, LU | **x1.30** | x1.15 |
| g_comp_142_cse-licm | generated | 55 | CF, DCE, CSE, SR, LU | **x1.29** | x1.28 |
| g_licm_055 | generated | 13 | CF, CSE, LICM | **x1.29** | x1.20 |
| g_comp_117_recur-branch-cf | generated | 14 | DCE, CSE, LICM | **x1.29** | x1.21 |
| g_comp_495_nested-unroll | generated | 63 | CF, DCE, CSE, LICM, SR, LU | **x1.29** | x1.29 |
| g_comp_313_licm-neutral-cse | generated | 55 | CF, DCE, CSE, SR, LU | **x1.29** | x1.15 |
| g_cse_265 | generated | 30 | DCE, CSE, LICM, SR | **x1.29** | x1.20 |
| g_comp_453_unroll-cf-struct-struct | generated | 7 | CF, DCE, CSE | **x1.29** | x1.23 |
| g_comp_297_neutral-struct-recur | generated | 63 | CF, DCE, CSE, LICM, SR, LU | **x1.29** | x1.29 |
| g_comp_298_div-struct | generated | 23 | CF, DCE, CSE, SR | **x1.29** | x1.23 |
| g_comp_459_nested-struct-struct | generated | 54 | DCE, CSE, SR, LU | **x1.29** | x1.20 |
| g_cf_102 | generated | 39 | CF, DCE, CSE, LU | **x1.29** | x1.14 |
| g_comp_093_licm-div-unroll | generated | 19 | CF, DCE, SR | **x1.29** | x1.25 |
| g_comp_109_neutral-div | generated | 59 | CF, DCE, LICM, SR, LU | **x1.28** | x1.22 |
| g_comp_424_cse-unroll-recur-sr | generated | 46 | DCE, CSE, LICM, LU | **x1.28** | x1.13 |
| g_comp_191_unroll-struct-nested-nested | generated | 62 | DCE, CSE, LICM, SR, LU | **x1.28** | x1.27 |
| g_comp_388_recur-branch-sr-struct | generated | 4 | CSE | **x1.28** | x1.09 |
| g_comp_026_cse-neutral-unroll-nested | generated | 54 | DCE, CSE, SR, LU | **x1.28** | x1.12 |
| g_comp_467_recur-unroll-licm-cse | generated | 39 | CF, DCE, CSE, LU | **x1.28** | x1.13 |
| g_comp_269_recur-nested-div | generated | 44 | CSE, LICM, LU | **x1.28** | x1.03 |
| g_cf_179 | generated | 15 | CF, DCE, CSE, LICM | **x1.28** | x1.21 |
| g_comp_067_cf-licm-cf | generated | 3 | CF, DCE | **x1.28** | x1.18 |
| g_comp_422_cf-sr | generated | 62 | DCE, CSE, LICM, SR, LU | **x1.28** | x1.22 |
| g_comp_176_cf-sr-cf | generated | 55 | CF, DCE, CSE, SR, LU | **x1.28** | x1.21 |
| g_comp_350_cf-branch-cf | generated | 47 | CF, DCE, CSE, LICM, LU | **x1.28** | x1.06 |
| g_licm_209 | generated | 35 | CF, DCE, LU | **x1.28** | x1.28 |
| g_comp_151_struct-cf-recur | generated | 3 | CF, DCE | **x1.28** | x1.12 |
| g_comp_031_nested-nested-cse-struct | generated | 47 | CF, DCE, CSE, LICM, LU | **x1.28** | x1.18 |
| g_comp_078_neutral-cf-recur | generated | 59 | CF, DCE, LICM, SR, LU | **x1.27** | x1.03 |
| g_comp_210_sr-cf | generated | 55 | CF, DCE, CSE, SR, LU | **x1.27** | x1.14 |
| g_comp_349_div-struct | generated | 36 | CSE, LU | **x1.27** | x1.20 |
| g_comp_062_cse-cf-struct | generated | 15 | CF, DCE, CSE, LICM | **x1.27** | x1.10 |
| g_comp_401_unroll-nested | generated | 38 | DCE, CSE, LU | **x1.27** | x1.16 |
| g_comp_202_sr-recur-div-licm | generated | 14 | DCE, CSE, LICM | **x1.27** | x1.01 |
| g_comp_000_branch-cse-branch | generated | 55 | CF, DCE, CSE, SR, LU | **x1.27** | x1.08 |
| g_comp_278_div-unroll | generated | 31 | CF, DCE, CSE, LICM, SR | **x1.27** | x1.24 |
| g_branch_184 | generated | 43 | CF, DCE, LICM, LU | **x1.27** | x1.24 |
| g_comp_017_branch-cf-neutral | generated | 63 | CF, DCE, CSE, LICM, SR, LU | **x1.27** | x1.27 |
| g_comp_431_licm-licm-cse-branch | generated | 47 | CF, DCE, CSE, LICM, LU | **x1.27** | x1.15 |
| g_comp_127_recur-div-sr | generated | 23 | CF, DCE, CSE, SR | **x1.27** | x1.24 |
| g_comp_336_licm-licm-nested-struct | generated | 31 | CF, DCE, CSE, LICM, SR | **x1.27** | x1.19 |
| g_comp_018_sr-recur | generated | 44 | CSE, LICM, LU | **x1.27** | x1.22 |
| g_comp_134_neutral-cse-struct | generated | 30 | DCE, CSE, LICM, SR | **x1.27** | x1.23 |
| g_comp_373_branch-div | generated | 27 | CF, DCE, LICM, SR | **x1.27** | x1.19 |
| g_struct_126 | generated | 23 | CF, DCE, CSE, SR | **x1.27** | x1.21 |
| g_comp_243_div-sr-cse | generated | 30 | DCE, CSE, LICM, SR | **x1.27** | x1.21 |
| g_cf_245 | generated | 35 | CF, DCE, LU | **x1.27** | x1.24 |
| g_comp_329_unroll-struct-nested-licm | generated | 55 | CF, DCE, CSE, SR, LU | **x1.26** | x1.15 |
| g_comp_333_cf-unroll-branch | generated | 35 | CF, DCE, LU | **x1.26** | x1.23 |
| g_comp_442_nested-branch-recur | generated | 48 | SR, LU | **x1.26** | x1.19 |
| g_comp_061_div-cse-sr | generated | 7 | CF, DCE, CSE | **x1.26** | x1.10 |
| g_comp_229_div-div-neutral-neutral | generated | 59 | CF, DCE, LICM, SR, LU | **x1.26** | x1.24 |
| g_licm_308 | generated | 23 | CF, DCE, CSE, SR | **x1.26** | x1.22 |
| g_comp_433_cf-struct-unroll | generated | 15 | CF, DCE, CSE, LICM | **x1.26** | x1.20 |
| g_comp_358_branch-licm-recur | generated | 9 | CF, LICM | **x1.26** | x0.99 |
| g_licm_231 | generated | 19 | CF, DCE, SR | **x1.26** | x1.17 |
| g_comp_451_cf-branch-licm-struct | generated | 47 | CF, DCE, CSE, LICM, LU | **x1.26** | x1.22 |
| g_licm_121 | generated | 63 | CF, DCE, CSE, LICM, SR, LU | **x1.26** | x1.26 |
| g_comp_099_branch-cse | generated | 6 | DCE, CSE | **x1.26** | x1.22 |
| g_comp_165_struct-div | generated | 31 | CF, DCE, CSE, LICM, SR | **x1.26** | x1.06 |
| g_comp_475_struct-branch-branch-recur | generated | 7 | CF, DCE, CSE | **x1.26** | x0.94 |
| g_comp_141_cf-licm-sr-branch | generated | 23 | CF, DCE, CSE, SR | **x1.26** | x1.24 |
| g_branch_327 | generated | 35 | CF, DCE, LU | **x1.25** | x1.19 |
| g_comp_356_cf-nested-unroll | generated | 35 | CF, DCE, LU | **x1.25** | x1.24 |
| g_comp_374_neutral-cf-struct | generated | 27 | CF, DCE, LICM, SR | **x1.25** | x1.05 |
| g_licm_198 | generated | 13 | CF, CSE, LICM | **x1.25** | x1.02 |
| g_comp_363_cf-nested-neutral-nested | generated | 47 | CF, DCE, CSE, LICM, LU | **x1.25** | x1.18 |
| g_recur_252 | generated | 9 | CF, LICM | **x1.25** | x1.12 |
| g_comp_098_sr-licm | generated | 55 | CF, DCE, CSE, SR, LU | **x1.25** | x1.24 |
| g_comp_342_branch-div | generated | 51 | CF, DCE, SR, LU | **x1.25** | x0.94 |
| g_comp_055_nested-branch | generated | 46 | DCE, CSE, LICM, LU | **x1.25** | x1.25 |
| g_comp_038_licm-div-recur | generated | 7 | CF, DCE, CSE | **x1.25** | x1.08 |
| g_comp_206_struct-licm | generated | 55 | CF, DCE, CSE, SR, LU | **x1.25** | x1.06 |
| matrix_mult | numeric | 53 | CF, CSE, SR, LU | **x1.25** | x1.09 |
| g_comp_059_cse-cf-branch-recur | generated | 55 | CF, DCE, CSE, SR, LU | **x1.25** | x0.86 |
| g_comp_197_recur-struct-recur-unroll | generated | 22 | DCE, CSE, SR | **x1.24** | x0.93 |
| g_comp_182_cf-struct | generated | 23 | CF, DCE, CSE, SR | **x1.24** | x1.05 |
| g_comp_316_neutral-branch-branch-nested | generated | 56 | LICM, SR, LU | **x1.24** | x1.12 |
| g_comp_414_cse-branch-sr-div | generated | 55 | CF, DCE, CSE, SR, LU | **x1.24** | x1.18 |
| g_comp_177_licm-struct | generated | 55 | CF, DCE, CSE, SR, LU | **x1.24** | x1.13 |
| g_comp_430_cf-cf | generated | 39 | CF, DCE, CSE, LU | **x1.24** | x1.09 |
| conv1d | numeric | 47 | CF, DCE, CSE, LICM, LU | **x1.24** | x1.19 |
| g_comp_466_div-struct-licm-sr | generated | 55 | CF, DCE, CSE, SR, LU | **x1.24** | x1.20 |
| g_comp_049_cse-div | generated | 31 | CF, DCE, CSE, LICM, SR | **x1.24** | x1.13 |
| g_nested_053 | generated | 62 | DCE, CSE, LICM, SR, LU | **x1.24** | x1.14 |
| strength_reduce | loops | 55 | CF, DCE, CSE, SR, LU | **x1.24** | x1.23 |
| g_branch_173 | generated | 63 | CF, DCE, CSE, LICM, SR, LU | **x1.24** | x1.24 |
| g_comp_481_sr-cse-branch | generated | 23 | CF, DCE, CSE, SR | **x1.24** | x1.01 |
| g_comp_293_recur-neutral-div | generated | 9 | CF, LICM | **x1.23** | x0.95 |
| g_comp_438_cse-nested | generated | 63 | CF, DCE, CSE, LICM, SR, LU | **x1.23** | x1.23 |
| g_cf_069 | generated | 59 | CF, DCE, LICM, SR, LU | **x1.23** | x1.21 |
| g_unroll_017 | generated | 46 | DCE, CSE, LICM, LU | **x1.23** | x1.19 |
| g_comp_264_cse-cf | generated | 62 | DCE, CSE, LICM, SR, LU | **x1.23** | x1.14 |
| g_comp_307_branch-branch-nested-branch | generated | 55 | CF, DCE, CSE, SR, LU | **x1.23** | x1.06 |
| g_comp_498_sr-cse-nested | generated | 54 | DCE, CSE, SR, LU | **x1.23** | x1.17 |
| g_comp_465_cse-unroll | generated | 55 | CF, DCE, CSE, SR, LU | **x1.23** | x1.12 |
| g_comp_114_recur-branch-div | generated | 41 | CF, LICM, LU | **x1.23** | x1.20 |
| g_comp_326_sr-recur-neutral-recur | generated | 55 | CF, DCE, CSE, SR, LU | **x1.23** | x0.86 |
| g_comp_083_unroll-cse-unroll-struct | generated | 14 | DCE, CSE, LICM | **x1.23** | x1.16 |
| g_comp_246_cf-cf | generated | 23 | CF, DCE, CSE, SR | **x1.23** | x0.98 |
| g_comp_019_branch-licm-unroll-licm | generated | 51 | CF, DCE, SR, LU | **x1.23** | x1.22 |
| g_comp_108_licm-licm-licm | generated | 61 | CF, CSE, LICM, SR, LU | **x1.23** | x1.04 |
| g_nested_108 | generated | 40 | LICM, LU | **x1.23** | x0.95 |
| g_comp_509_cse-cf-struct | generated | 47 | CF, DCE, CSE, LICM, LU | **x1.23** | x1.14 |
| g_comp_511_cf-branch-cse | generated | 63 | CF, DCE, CSE, LICM, SR, LU | **x1.23** | x1.23 |
| g_comp_501_cf-unroll | generated | 47 | CF, DCE, CSE, LICM, LU | **x1.23** | x0.97 |
| g_comp_089_cf-sr-cse-branch | generated | 23 | CF, DCE, CSE, SR | **x1.23** | x1.16 |
| g_comp_486_licm-recur | generated | 57 | CF, LICM, SR, LU | **x1.23** | x0.99 |
| g_comp_008_cf-cse | generated | 7 | CF, DCE, CSE | **x1.23** | x1.21 |
| g_comp_488_sr-recur | generated | 60 | CSE, LICM, SR, LU | **x1.23** | x0.98 |
| g_comp_201_struct-cse-licm-neutral | generated | 31 | CF, DCE, CSE, LICM, SR | **x1.22** | x1.17 |
| g_branch_085 | generated | 63 | CF, DCE, CSE, LICM, SR, LU | **x1.22** | x1.22 |
| g_comp_143_licm-sr-nested | generated | 55 | CF, DCE, CSE, SR, LU | **x1.22** | x1.20 |
| g_comp_244_recur-nested | generated | 54 | DCE, CSE, SR, LU | **x1.22** | x1.12 |
| g_struct_060 | generated | 62 | DCE, CSE, LICM, SR, LU | **x1.22** | x1.16 |
| g_comp_468_sr-cf-nested-neutral | generated | 35 | CF, DCE, LU | **x1.22** | x1.19 |
| g_comp_028_cf-struct-cf-unroll | generated | 31 | CF, DCE, CSE, LICM, SR | **x1.22** | x1.13 |
| g_cf_113 | generated | 51 | CF, DCE, SR, LU | **x1.22** | x1.19 |
| g_comp_251_branch-div-cse-nested | generated | 54 | DCE, CSE, SR, LU | **x1.22** | x1.11 |
| g_comp_286_branch-div | generated | 41 | CF, LICM, LU | **x1.22** | x1.10 |
| g_comp_240_branch-cf-sr-div | generated | 55 | CF, DCE, CSE, SR, LU | **x1.22** | x1.02 |
| g_comp_408_cse-recur | generated | 39 | CF, DCE, CSE, LU | **x1.22** | x1.00 |
| g_comp_457_struct-unroll-div-recur | generated | 63 | CF, DCE, CSE, LICM, SR, LU | **x1.21** | x1.21 |
| g_comp_423_sr-cse-branch-struct | generated | 31 | CF, DCE, CSE, LICM, SR | **x1.21** | x1.10 |
| g_comp_200_div-nested-branch | generated | 62 | DCE, CSE, LICM, SR, LU | **x1.21** | x1.18 |
| g_comp_228_struct-unroll | generated | 30 | DCE, CSE, LICM, SR | **x1.21** | x1.17 |
| g_comp_485_cse-div-branch | generated | 55 | CF, DCE, CSE, SR, LU | **x1.21** | x1.14 |
| g_comp_252_branch-licm | generated | 3 | CF, DCE | **x1.21** | x1.20 |
| g_comp_291_neutral-licm-div | generated | 63 | CF, DCE, CSE, LICM, SR, LU | **x1.21** | x1.21 |
| g_comp_195_cse-licm | generated | 63 | CF, DCE, CSE, LICM, SR, LU | **x1.21** | x1.21 |
| g_comp_005_recur-unroll-cse-cse | generated | 7 | CF, DCE, CSE | **x1.21** | x0.95 |
| g_comp_267_neutral-struct-cse-nested | generated | 54 | DCE, CSE, SR, LU | **x1.21** | x1.20 |
| g_comp_288_div-struct | generated | 39 | CF, DCE, CSE, LU | **x1.21** | x1.19 |
| g_comp_042_cf-recur-cse | generated | 31 | CF, DCE, CSE, LICM, SR | **x1.21** | x0.75 |
| g_comp_517_neutral-cse | generated | 30 | DCE, CSE, LICM, SR | **x1.21** | x1.06 |
| g_comp_085_unroll-branch | generated | 35 | CF, DCE, LU | **x1.21** | x1.17 |
| g_comp_103_branch-cf-sr | generated | 43 | CF, DCE, LICM, LU | **x1.21** | x1.07 |
| g_unroll_314 | generated | 62 | DCE, CSE, LICM, SR, LU | **x1.21** | x1.17 |
| g_branch_030 | generated | 7 | CF, DCE, CSE | **x1.21** | x1.18 |
| g_comp_416_unroll-struct-nested | generated | 62 | DCE, CSE, LICM, SR, LU | **x1.21** | x1.02 |
| g_struct_115 | generated | 38 | DCE, CSE, LU | **x1.21** | x1.17 |
| g_comp_368_cse-neutral-nested-neutral | generated | 63 | CF, DCE, CSE, LICM, SR, LU | **x1.21** | x1.21 |
| g_comp_147_cse-sr-branch | generated | 7 | CF, DCE, CSE | **x1.20** | x1.09 |
| g_comp_505_neutral-unroll-unroll-recur | generated | 22 | DCE, CSE, SR | **x1.20** | x1.09 |
| g_comp_470_branch-div-sr-unroll | generated | 47 | CF, DCE, CSE, LICM, LU | **x1.20** | x0.99 |
| g_comp_215_struct-cse-branch | generated | 22 | DCE, CSE, SR | **x1.20** | x1.10 |
| g_comp_234_licm-licm-unroll | generated | 23 | CF, DCE, CSE, SR | **x1.20** | x1.18 |
| g_comp_174_licm-cse-neutral-cse | generated | 46 | DCE, CSE, LICM, LU | **x1.20** | x1.05 |
| g_comp_387_struct-branch-struct-cf | generated | 46 | DCE, CSE, LICM, LU | **x1.20** | x1.11 |
| g_comp_439_licm-unroll-cse-cf | generated | 39 | CF, DCE, CSE, LU | **x1.20** | x1.17 |
| g_comp_158_cf-cf-neutral-cf | generated | 29 | CF, CSE, LICM, SR | **x1.20** | x1.11 |
| g_comp_354_cse-unroll-branch | generated | 47 | CF, DCE, CSE, LICM, LU | **x1.20** | x1.17 |
| g_comp_513_recur-neutral-div | generated | 30 | DCE, CSE, LICM, SR | **x1.20** | x1.07 |
| g_comp_222_div-neutral-struct | generated | 55 | CF, DCE, CSE, SR, LU | **x1.20** | x1.07 |
| g_comp_149_unroll-div | generated | 25 | CF, LICM, SR | **x1.20** | x1.00 |
| g_comp_271_cf-unroll-cf | generated | 51 | CF, DCE, SR, LU | **x1.20** | x1.10 |
| g_comp_327_nested-unroll-neutral-div | generated | 62 | DCE, CSE, LICM, SR, LU | **x1.20** | x1.09 |
| g_comp_209_div-struct | generated | 47 | CF, DCE, CSE, LICM, LU | **x1.20** | x1.16 |
| g_comp_216_cf-branch-unroll-sr | generated | 62 | DCE, CSE, LICM, SR, LU | **x1.20** | x1.18 |
| g_comp_516_struct-sr-licm | generated | 63 | CF, DCE, CSE, LICM, SR, LU | **x1.20** | x1.20 |
| g_sr_090 | generated | 31 | CF, DCE, CSE, LICM, SR | **x1.19** | x1.18 |
| g_comp_217_unroll-cse-sr | generated | 63 | CF, DCE, CSE, LICM, SR, LU | **x1.19** | x1.19 |
| g_comp_001_div-struct | generated | 41 | CF, LICM, LU | **x1.19** | x1.09 |
| g_comp_122_struct-div-struct | generated | 46 | DCE, CSE, LICM, LU | **x1.19** | x1.07 |
| g_comp_473_struct-cse | generated | 30 | DCE, CSE, LICM, SR | **x1.19** | x1.12 |
| histogram | numeric | 6 | DCE, CSE | **x1.19** | x1.16 |
| g_licm_077 | generated | 9 | CF, LICM | **x1.19** | x1.17 |
| g_comp_382_branch-cf-sr-sr | generated | 31 | CF, DCE, CSE, LICM, SR | **x1.19** | x1.02 |
| g_comp_106_licm-struct | generated | 7 | CF, DCE, CSE | **x1.19** | x1.12 |
| g_branch_294 | generated | 35 | CF, DCE, LU | **x1.19** | x1.14 |
| g_recur_175 | generated | 43 | CF, DCE, LICM, LU | **x1.19** | x1.13 |
| g_struct_104 | generated | 38 | DCE, CSE, LU | **x1.19** | x1.15 |
| g_comp_007_struct-struct-div | generated | 30 | DCE, CSE, LICM, SR | **x1.19** | x1.04 |
| vowel_count | strings | 44 | CSE, LICM, LU | **x1.19** | x1.16 |
| g_struct_335 | generated | 63 | CF, DCE, CSE, LICM, SR, LU | **x1.19** | x1.19 |
| g_comp_006_branch-licm | generated | 10 | DCE, LICM | **x1.19** | x1.05 |
| g_licm_033 | generated | 25 | CF, LICM, SR | **x1.18** | x1.14 |
| g_comp_072_licm-sr | generated | 63 | CF, DCE, CSE, LICM, SR, LU | **x1.18** | x1.18 |
| g_comp_250_neutral-div-neutral-neutral | generated | 25 | CF, LICM, SR | **x1.18** | x1.12 |
| g_comp_120_recur-licm-recur-neutral | generated | 31 | CF, DCE, CSE, LICM, SR | **x1.18** | x0.82 |
| g_comp_207_nested-cf | generated | 39 | CF, DCE, CSE, LU | **x1.18** | x1.04 |
| g_comp_148_struct-struct-cf | generated | 35 | CF, DCE, LU | **x1.18** | x1.05 |
| g_comp_436_recur-cse-cse | generated | 63 | CF, DCE, CSE, LICM, SR, LU | **x1.18** | x1.18 |
| g_comp_406_unroll-neutral-struct | generated | 11 | CF, DCE, LICM | **x1.18** | x1.15 |
| g_comp_129_cse-struct-recur | generated | 54 | DCE, CSE, SR, LU | **x1.18** | x0.96 |
| g_licm_000 | generated | 19 | CF, DCE, SR | **x1.18** | x1.11 |
| g_comp_136_struct-nested-branch | generated | 39 | CF, DCE, CSE, LU | **x1.18** | x1.04 |
| g_comp_245_cse-neutral-cse | generated | 30 | DCE, CSE, LICM, SR | **x1.18** | x1.14 |
| g_comp_428_branch-struct-sr | generated | 63 | CF, DCE, CSE, LICM, SR, LU | **x1.18** | x1.18 |
| g_comp_435_neutral-div-recur | generated | 47 | CF, DCE, CSE, LICM, LU | **x1.18** | x1.15 |
| g_comp_367_recur-cse | generated | 39 | CF, DCE, CSE, LU | **x1.18** | x0.84 |
| g_comp_184_licm-licm-cf | generated | 11 | CF, DCE, LICM | **x1.18** | x1.12 |
| g_comp_226_struct-cse | generated | 54 | DCE, CSE, SR, LU | **x1.18** | x1.12 |
| g_struct_313 | generated | 46 | DCE, CSE, LICM, LU | **x1.18** | x1.11 |
| g_comp_036_sr-struct | generated | 31 | CF, DCE, CSE, LICM, SR | **x1.17** | x1.12 |
| g_comp_270_licm-struct-div-branch | generated | 23 | CF, DCE, CSE, SR | **x1.17** | x1.11 |
| g_comp_111_licm-unroll-unroll | generated | 55 | CF, DCE, CSE, SR, LU | **x1.17** | x1.09 |
| g_comp_321_sr-div | generated | 63 | CF, DCE, CSE, LICM, SR, LU | **x1.17** | x1.17 |
| g_comp_058_branch-nested-unroll | generated | 46 | DCE, CSE, LICM, LU | **x1.17** | x1.09 |
| g_comp_023_struct-cf | generated | 62 | DCE, CSE, LICM, SR, LU | **x1.17** | x1.15 |
| g_comp_339_neutral-div | generated | 29 | CF, CSE, LICM, SR | **x1.17** | x1.11 |
| g_branch_129 | generated | 41 | CF, LICM, LU | **x1.17** | x1.11 |
| g_struct_071 | generated | 39 | CF, DCE, CSE, LU | **x1.17** | x1.14 |
| g_recur_186 | generated | 8 | LICM | **x1.17** | x0.63 |
| g_comp_115_licm-unroll-recur-unroll | generated | 23 | CF, DCE, CSE, SR | **x1.17** | x1.08 |
| g_comp_445_nested-neutral | generated | 58 | DCE, LICM, SR, LU | **x1.17** | x1.06 |
| g_struct_236 | generated | 62 | DCE, CSE, LICM, SR, LU | **x1.17** | x1.06 |
| g_struct_280 | generated | 55 | CF, DCE, CSE, SR, LU | **x1.17** | x1.14 |
| g_comp_101_sr-licm-branch | generated | 10 | DCE, LICM | **x1.17** | x1.02 |
| g_comp_452_div-neutral-neutral-cse | generated | 62 | DCE, CSE, LICM, SR, LU | **x1.17** | x1.12 |
| g_comp_277_unroll-struct | generated | 31 | CF, DCE, CSE, LICM, SR | **x1.17** | x1.13 |
| g_branch_118 | generated | 45 | CF, CSE, LICM, LU | **x1.17** | x1.11 |
| g_comp_479_neutral-cse | generated | 62 | DCE, CSE, LICM, SR, LU | **x1.16** | x1.06 |
| g_comp_440_nested-cf | generated | 35 | CF, DCE, LU | **x1.16** | x1.08 |
| g_recur_285 | generated | 29 | CF, CSE, LICM, SR | **x1.16** | x0.75 |
| g_comp_372_unroll-struct-neutral-licm | generated | 30 | DCE, CSE, LICM, SR | **x1.16** | x1.11 |
| g_comp_303_licm-div-sr-neutral | generated | 30 | DCE, CSE, LICM, SR | **x1.16** | x1.05 |
| g_struct_181 | generated | 55 | CF, DCE, CSE, SR, LU | **x1.16** | x1.13 |
| g_struct_016 | generated | 23 | CF, DCE, CSE, SR | **x1.16** | x1.11 |
| g_comp_237_cf-neutral-cse-neutral | generated | 55 | CF, DCE, CSE, SR, LU | **x1.16** | x1.15 |
| g_comp_081_neutral-cf | generated | 7 | CF, DCE, CSE | **x1.16** | x1.05 |
| g_comp_320_branch-branch-neutral | generated | 11 | CF, DCE, LICM | **x1.16** | x0.99 |
| g_comp_268_recur-cse-neutral | generated | 38 | DCE, CSE, LU | **x1.16** | x1.02 |
| g_comp_152_cse-neutral-neutral | generated | 14 | DCE, CSE, LICM | **x1.15** | x1.07 |
| g_comp_050_div-neutral-cse-sr | generated | 55 | CF, DCE, CSE, SR, LU | **x1.15** | x1.14 |
| g_comp_419_recur-cf-struct-branch | generated | 39 | CF, DCE, CSE, LU | **x1.15** | x0.96 |
| g_sr_200 | generated | 30 | DCE, CSE, LICM, SR | **x1.15** | x1.10 |
| g_comp_069_sr-div | generated | 47 | CF, DCE, CSE, LICM, LU | **x1.15** | x0.94 |
| g_comp_332_struct-struct-unroll-nested | generated | 46 | DCE, CSE, LICM, LU | **x1.15** | x1.03 |
| tak | recursion | 57 | CF, LICM, SR, LU | **x1.15** | x1.01 |
| g_comp_167_cse-branch-struct | generated | 62 | DCE, CSE, LICM, SR, LU | **x1.15** | x1.09 |
| g_comp_449_licm-neutral | generated | 41 | CF, LICM, LU | **x1.15** | x1.12 |
| g_comp_507_neutral-sr-neutral | generated | 32 | LU | **x1.15** | x1.12 |
| g_comp_013_nested-sr-sr | generated | 63 | CF, DCE, CSE, LICM, SR, LU | **x1.15** | x1.15 |
| g_comp_164_neutral-struct-nested-branch | generated | 33 | CF, LU | **x1.15** | x1.11 |
| prime_sieve | loops | 39 | CF, DCE, CSE, LU | **x1.15** | x1.14 |
| g_branch_338 | generated | 44 | CSE, LICM, LU | **x1.15** | x1.09 |
| g_sr_277 | generated | 54 | DCE, CSE, SR, LU | **x1.15** | x1.14 |
| g_comp_262_struct-unroll-sr | generated | 54 | DCE, CSE, SR, LU | **x1.15** | x1.10 |
| g_comp_140_branch-struct-cse-branch | generated | 7 | CF, DCE, CSE | **x1.15** | x1.14 |
| g_comp_400_sr-licm-unroll-neutral | generated | 29 | CF, CSE, LICM, SR | **x1.14** | x1.10 |
| g_comp_212_sr-sr | generated | 55 | CF, DCE, CSE, SR, LU | **x1.14** | x0.92 |
| g_struct_247 | generated | 55 | CF, DCE, CSE, SR, LU | **x1.14** | x1.08 |
| g_comp_071_unroll-neutral | generated | 33 | CF, LU | **x1.14** | x1.13 |
| g_comp_223_licm-struct-struct-unroll | generated | 31 | CF, DCE, CSE, LICM, SR | **x1.14** | x0.98 |
| g_unroll_138 | generated | 55 | CF, DCE, CSE, SR, LU | **x1.14** | x1.10 |
| g_branch_008 | generated | 7 | CF, DCE, CSE | **x1.14** | x1.00 |
| g_branch_052 | generated | 55 | CF, DCE, CSE, SR, LU | **x1.14** | x1.00 |
| g_recur_340 | generated | 43 | CF, DCE, LICM, LU | **x1.14** | x0.75 |
| g_sr_035 | generated | 14 | DCE, CSE, LICM | **x1.14** | x1.12 |
| g_branch_107 | generated | 47 | CF, DCE, CSE, LICM, LU | **x1.14** | x1.11 |
| g_branch_151 | generated | 57 | CF, LICM, SR, LU | **x1.14** | x1.10 |
| g_comp_322_neutral-sr | generated | 2 | DCE | **x1.14** | x1.11 |
| g_comp_056_sr-sr-unroll-div | generated | 23 | CF, DCE, CSE, SR | **x1.14** | x1.14 |
| g_comp_192_div-struct-branch | generated | 47 | CF, DCE, CSE, LICM, LU | **x1.14** | x0.93 |
| g_comp_393_recur-branch-neutral-cse | generated | 31 | CF, DCE, CSE, LICM, SR | **x1.14** | x0.82 |
| g_comp_346_struct-nested-licm-branch | generated | 35 | CF, DCE, LU | **x1.13** | x1.02 |
| g_comp_088_struct-nested-branch-unroll | generated | 54 | DCE, CSE, SR, LU | **x1.13** | x0.96 |
| g_comp_100_nested-neutral-unroll-neutral | generated | 39 | CF, DCE, CSE, LU | **x1.13** | x1.10 |
| g_comp_300_cf-branch | generated | 15 | CF, DCE, CSE, LICM | **x1.13** | x1.12 |
| g_sr_057 | generated | 31 | CF, DCE, CSE, LICM, SR | **x1.13** | x1.12 |
| g_struct_082 | generated | 62 | DCE, CSE, LICM, SR, LU | **x1.13** | x1.07 |
| g_comp_314_nested-sr | generated | 55 | CF, DCE, CSE, SR, LU | **x1.13** | x1.06 |
| g_comp_503_cf-unroll | generated | 30 | DCE, CSE, LICM, SR | **x1.13** | x1.06 |
| g_comp_351_sr-unroll-div | generated | 15 | CF, DCE, CSE, LICM | **x1.13** | x1.03 |
| g_comp_352_sr-cse-branch | generated | 15 | CF, DCE, CSE, LICM | **x1.13** | x0.99 |
| g_unroll_039 | generated | 23 | CF, DCE, CSE, SR | **x1.13** | x1.12 |
| g_struct_258 | generated | 38 | DCE, CSE, LU | **x1.13** | x1.00 |
| g_sr_002 | generated | 62 | DCE, CSE, LICM, SR, LU | **x1.13** | x1.11 |
| g_comp_405_sr-neutral-sr | generated | 22 | DCE, CSE, SR | **x1.13** | x1.00 |
| g_comp_315_unroll-sr-struct | generated | 23 | CF, DCE, CSE, SR | **x1.13** | x1.07 |
| g_struct_225 | generated | 62 | DCE, CSE, LICM, SR, LU | **x1.13** | x1.12 |
| g_comp_360_sr-sr | generated | 54 | DCE, CSE, SR, LU | **x1.13** | x1.08 |
| g_sr_211 | generated | 30 | DCE, CSE, LICM, SR | **x1.13** | x0.96 |
| fib | recursion | 54 | DCE, CSE, SR, LU | **x1.13** | x1.09 |
| g_branch_019 | generated | 60 | CSE, LICM, SR, LU | **x1.13** | x1.12 |
| g_comp_325_struct-branch-branch-nested | generated | 63 | CF, DCE, CSE, LICM, SR, LU | **x1.13** | x1.13 |
| g_comp_070_struct-neutral-struct-unroll | generated | 31 | CF, DCE, CSE, LICM, SR | **x1.13** | x1.00 |
| g_comp_097_sr-struct-struct-cf | generated | 39 | CF, DCE, CSE, LU | **x1.13** | x1.08 |
| g_comp_079_unroll-unroll-recur | generated | 19 | CF, DCE, SR | **x1.13** | x0.98 |
| g_comp_010_sr-div-neutral | generated | 55 | CF, DCE, CSE, SR, LU | **x1.13** | x1.09 |
| g_unroll_105 | generated | 62 | DCE, CSE, LICM, SR, LU | **x1.13** | x1.10 |
| g_comp_493_sr-recur-neutral-sr | generated | 30 | DCE, CSE, LICM, SR | **x1.13** | x0.90 |
| g_comp_410_neutral-sr | generated | 31 | CF, DCE, CSE, LICM, SR | **x1.12** | x0.98 |
| g_comp_477_neutral-div-neutral | generated | 62 | DCE, CSE, LICM, SR, LU | **x1.12** | x1.10 |
| g_struct_137 | generated | 15 | CF, DCE, CSE, LICM | **x1.12** | x1.08 |
| g_comp_305_struct-nested-cse-branch | generated | 39 | CF, DCE, CSE, LU | **x1.12** | x1.08 |
| g_comp_060_cf-nested | generated | 39 | CF, DCE, CSE, LU | **x1.12** | x1.11 |
| g_comp_043_sr-licm-struct | generated | 43 | CF, DCE, LICM, LU | **x1.12** | x1.02 |
| g_comp_418_sr-div-branch | generated | 7 | CF, DCE, CSE | **x1.12** | x0.95 |
| g_comp_323_struct-branch-cf-unroll | generated | 63 | CF, DCE, CSE, LICM, SR, LU | **x1.12** | x1.12 |
| g_comp_255_licm-div-neutral | generated | 14 | DCE, CSE, LICM | **x1.12** | x1.03 |
| g_struct_346 | generated | 39 | CF, DCE, CSE, LU | **x1.12** | x1.08 |
| g_comp_378_licm-struct-unroll | generated | 55 | CF, DCE, CSE, SR, LU | **x1.12** | x1.11 |
| g_sr_167 | generated | 22 | DCE, CSE, SR | **x1.12** | x1.09 |
| g_sr_101 | generated | 22 | DCE, CSE, SR | **x1.12** | x1.09 |
| g_comp_024_licm-sr | generated | 23 | CF, DCE, CSE, SR | **x1.12** | x1.03 |
| g_comp_040_sr-div-nested-neutral | generated | 23 | CF, DCE, CSE, SR | **x1.12** | x0.99 |
| g_comp_508_licm-struct-neutral | generated | 21 | CF, CSE, SR | **x1.12** | x1.06 |
| g_comp_515_cse-struct-struct-neutral | generated | 23 | CF, DCE, CSE, SR | **x1.12** | x1.05 |
| g_sr_123 | generated | 62 | DCE, CSE, LICM, SR, LU | **x1.12** | x1.10 |
| g_comp_265_cse-cse-neutral | generated | 31 | CF, DCE, CSE, LICM, SR | **x1.12** | x1.09 |
| g_comp_233_unroll-licm | generated | 27 | CF, DCE, LICM, SR | **x1.12** | x0.99 |
| g_unroll_127 | generated | 14 | DCE, CSE, LICM | **x1.12** | x1.09 |
| g_comp_491_branch-recur-cf-cf | generated | 1 | CF | **x1.11** | x0.99 |
| g_comp_381_branch-unroll-struct-neutral | generated | 14 | DCE, CSE, LICM | **x1.11** | x0.99 |
| g_sr_310 | generated | 22 | DCE, CSE, SR | **x1.11** | x1.08 |
| g_struct_049 | generated | 30 | DCE, CSE, LICM, SR | **x1.11** | x1.07 |
| particle_sim | structs | 14 | DCE, CSE, LICM | **x1.11** | x1.11 |
| g_branch_162 | generated | 39 | CF, DCE, CSE, LU | **x1.11** | x1.11 |
| g_branch_063 | generated | 63 | CF, DCE, CSE, LICM, SR, LU | **x1.11** | x1.11 |
| g_comp_235_branch-branch-sr | generated | 63 | CF, DCE, CSE, LICM, SR, LU | **x1.11** | x1.11 |
| g_comp_319_nested-sr-recur | generated | 30 | DCE, CSE, LICM, SR | **x1.11** | x1.03 |
| g_struct_192 | generated | 6 | DCE, CSE | **x1.11** | x1.07 |
| g_comp_015_nested-licm-struct-branch | generated | 63 | CF, DCE, CSE, LICM, SR, LU | **x1.11** | x1.11 |
| g_comp_231_neutral-div-struct-branch | generated | 35 | CF, DCE, LU | **x1.11** | x1.05 |
| g_sr_013 | generated | 33 | CF, LU | **x1.11** | x1.04 |
| g_comp_156_unroll-struct | generated | 55 | CF, DCE, CSE, SR, LU | **x1.11** | x1.03 |
| g_comp_225_struct-branch | generated | 23 | CF, DCE, CSE, SR | **x1.11** | x1.02 |
| g_struct_269 | generated | 22 | DCE, CSE, SR | **x1.11** | x1.07 |
| g_comp_448_cf-div-neutral | generated | 39 | CF, DCE, CSE, LU | **x1.11** | x1.05 |
| g_comp_285_licm-struct | generated | 46 | DCE, CSE, LICM, LU | **x1.11** | x1.00 |
| g_comp_409_sr-unroll-sr-cse | generated | 31 | CF, DCE, CSE, LICM, SR | **x1.11** | x1.02 |
| g_struct_291 | generated | 39 | CF, DCE, CSE, LU | **x1.11** | x0.91 |
| g_comp_494_cse-sr-neutral | generated | 7 | CF, DCE, CSE | **x1.11** | x1.01 |
| g_comp_390_branch-sr-div-branch | generated | 63 | CF, DCE, CSE, LICM, SR, LU | **x1.11** | x1.11 |
| g_sr_134 | generated | 63 | CF, DCE, CSE, LICM, SR, LU | **x1.11** | x1.11 |
| g_comp_185_sr-cf-branch | generated | 35 | CF, DCE, LU | **x1.11** | x0.92 |
| g_struct_038 | generated | 22 | DCE, CSE, SR | **x1.11** | x1.01 |
| g_sr_079 | generated | 54 | DCE, CSE, SR, LU | **x1.11** | x1.08 |
| g_struct_005 | generated | 7 | CF, DCE, CSE | **x1.10** | x0.99 |
| g_unroll_006 | generated | 55 | CF, DCE, CSE, SR, LU | **x1.10** | x1.09 |
| g_struct_324 | generated | 62 | DCE, CSE, LICM, SR, LU | **x1.10** | x1.07 |
| g_branch_316 | generated | 43 | CF, DCE, LICM, LU | **x1.10** | x1.07 |
| g_branch_206 | generated | 2 | DCE | **x1.10** | x0.84 |
| g_comp_118_sr-unroll | generated | 24 | LICM, SR | **x1.10** | x1.05 |
| g_struct_027 | generated | 14 | DCE, CSE, LICM | **x1.10** | x0.90 |
| g_sr_288 | generated | 30 | DCE, CSE, LICM, SR | **x1.10** | x1.06 |
| g_sr_266 | generated | 55 | CF, DCE, CSE, SR, LU | **x1.10** | x1.06 |
| g_comp_487_div-unroll-neutral-nested | generated | 46 | DCE, CSE, LICM, LU | **x1.10** | x1.07 |
| g_comp_472_neutral-cf | generated | 11 | CF, DCE, LICM | **x1.10** | x1.06 |
| g_branch_096 | generated | 47 | CF, DCE, CSE, LICM, LU | **x1.10** | x1.00 |
| g_comp_521_sr-div | generated | 35 | CF, DCE, LU | **x1.10** | x0.91 |
| g_unroll_248 | generated | 48 | SR, LU | **x1.10** | x0.88 |
| g_sr_068 | generated | 63 | CF, DCE, CSE, LICM, SR, LU | **x1.10** | x1.10 |
| g_comp_447_sr-cf-struct | generated | 15 | CF, DCE, CSE, LICM | **x1.10** | x1.08 |
| g_comp_253_licm-licm | generated | 11 | CF, DCE, LICM | **x1.10** | x1.03 |
| g_struct_203 | generated | 30 | DCE, CSE, LICM, SR | **x1.10** | x1.08 |
| g_branch_195 | generated | 14 | DCE, CSE, LICM | **x1.10** | x0.81 |
| g_comp_385_unroll-branch-branch | generated | 5 | CF, CSE | **x1.10** | x1.07 |
| g_unroll_226 | generated | 62 | DCE, CSE, LICM, SR, LU | **x1.10** | x1.00 |
| g_comp_075_struct-struct | generated | 22 | DCE, CSE, SR | **x1.10** | x1.06 |
| g_comp_347_struct-unroll | generated | 11 | CF, DCE, LICM | **x1.09** | x1.05 |
| ackermann | recursion | 63 | CF, DCE, CSE, LICM, SR, LU | **x1.09** | x1.09 |
| g_comp_039_unroll-unroll | generated | 33 | CF, LU | **x1.09** | x1.01 |
| g_comp_052_sr-recur-branch | generated | 63 | CF, DCE, CSE, LICM, SR, LU | **x1.09** | x1.09 |
| g_neutral_018 | generated | 35 | CF, DCE, LU | **x1.09** | x1.05 |
| g_comp_137_nested-recur-recur-neutral | generated | 42 | DCE, LICM, LU | **x1.09** | x0.63 |
| g_comp_304_neutral-sr-sr | generated | 22 | DCE, CSE, SR | **x1.09** | x1.02 |
| g_comp_037_unroll-recur-cse | generated | 14 | DCE, CSE, LICM | **x1.09** | x0.71 |
| g_sr_332 | generated | 60 | CSE, LICM, SR, LU | **x1.09** | x0.97 |
| g_struct_214 | generated | 23 | CF, DCE, CSE, SR | **x1.09** | x1.08 |
| g_sr_343 | generated | 23 | CF, DCE, CSE, SR | **x1.09** | x1.02 |
| g_comp_370_nested-sr | generated | 42 | DCE, LICM, LU | **x1.09** | x0.84 |
| g_comp_094_cse-neutral | generated | 55 | CF, DCE, CSE, SR, LU | **x1.09** | x0.97 |
| g_comp_119_struct-recur-cse-branch | generated | 7 | CF, DCE, CSE | **x1.09** | x0.78 |
| g_comp_366_branch-unroll-sr | generated | 23 | CF, DCE, CSE, SR | **x1.09** | x0.97 |
| g_comp_169_cf-neutral | generated | 27 | CF, DCE, LICM, SR | **x1.09** | x1.03 |
| g_comp_357_cf-unroll-neutral | generated | 63 | CF, DCE, CSE, LICM, SR, LU | **x1.09** | x1.09 |
| g_unroll_303 | generated | 41 | CF, LICM, LU | **x1.08** | x0.99 |
| g_struct_302 | generated | 55 | CF, DCE, CSE, SR, LU | **x1.08** | x0.88 |
| g_sr_255 | generated | 22 | DCE, CSE, SR | **x1.08** | x0.94 |
| g_comp_095_nested-neutral-neutral-unroll | generated | 39 | CF, DCE, CSE, LU | **x1.08** | x0.99 |
| g_recur_296 | generated | 47 | CF, DCE, CSE, LICM, LU | **x1.08** | x1.04 |
| g_comp_337_unroll-neutral-sr | generated | 25 | CF, LICM, SR | **x1.08** | x1.02 |
| g_comp_402_sr-struct | generated | 14 | DCE, CSE, LICM | **x1.08** | x0.98 |
| g_recur_032 | generated | 19 | CF, DCE, SR | **x1.08** | x0.88 |
| g_struct_093 | generated | 6 | DCE, CSE | **x1.08** | x1.07 |
| g_comp_443_sr-neutral-struct | generated | 21 | CF, CSE, SR | **x1.08** | x1.04 |
| g_comp_168_struct-struct-branch-neutral | generated | 31 | CF, DCE, CSE, LICM, SR | **x1.08** | x1.03 |
| g_struct_159 | generated | 31 | CF, DCE, CSE, LICM, SR | **x1.08** | x1.04 |
| g_comp_484_struct-branch | generated | 31 | CF, DCE, CSE, LICM, SR | **x1.08** | x0.98 |
| g_comp_450_sr-cse-neutral | generated | 54 | DCE, CSE, SR, LU | **x1.08** | x0.99 |
| g_unroll_281 | generated | 7 | CF, DCE, CSE | **x1.08** | x1.02 |
| g_comp_474_licm-struct | generated | 30 | DCE, CSE, LICM, SR | **x1.08** | x0.98 |
| g_recur_021 | generated | 51 | CF, DCE, SR, LU | **x1.08** | x0.45 |
| g_sr_046 | generated | 23 | CF, DCE, CSE, SR | **x1.07** | x1.02 |
| g_neutral_172 | generated | 33 | CF, LU | **x1.07** | x1.04 |
| g_comp_002_recur-neutral-cse | generated | 6 | DCE, CSE | **x1.07** | x1.00 |
| g_unroll_149 | generated | 38 | DCE, CSE, LU | **x1.07** | x1.01 |
| g_sr_112 | generated | 54 | DCE, CSE, SR, LU | **x1.07** | x1.00 |
| g_unroll_237 | generated | 22 | DCE, CSE, SR | **x1.07** | x1.01 |
| g_comp_420_sr-struct-struct | generated | 39 | CF, DCE, CSE, LU | **x1.07** | x1.04 |
| g_neutral_084 | generated | 20 | CSE, SR | **x1.07** | x0.96 |
| g_comp_155_neutral-neutral-div-sr | generated | 9 | CF, LICM | **x1.07** | x1.02 |
| g_struct_170 | generated | 46 | DCE, CSE, LICM, LU | **x1.07** | x0.88 |
| g_unroll_292 | generated | 25 | CF, LICM, SR | **x1.07** | x1.01 |
| g_unroll_336 | generated | 30 | DCE, CSE, LICM, SR | **x1.07** | x1.01 |
| g_neutral_095 | generated | 24 | LICM, SR | **x1.07** | x1.01 |
| g_unroll_160 | generated | 22 | DCE, CSE, SR | **x1.07** | x1.04 |
| g_sr_321 | generated | 31 | CF, DCE, CSE, LICM, SR | **x1.07** | x1.06 |
| g_comp_116_struct-branch | generated | 63 | CF, DCE, CSE, LICM, SR, LU | **x1.07** | x1.07 |
| g_recur_318 | generated | 46 | DCE, CSE, LICM, LU | **x1.07** | x0.44 |
| g_struct_148 | generated | 63 | CF, DCE, CSE, LICM, SR, LU | **x1.07** | x1.07 |
| g_comp_159_branch-sr | generated | 62 | DCE, CSE, LICM, SR, LU | **x1.07** | x1.01 |
| g_comp_063_nested-neutral | generated | 33 | CF, LU | **x1.06** | x0.92 |
| g_comp_318_recur-struct-branch | generated | 22 | DCE, CSE, SR | **x1.06** | x0.79 |
| g_unroll_182 | generated | 38 | DCE, CSE, LU | **x1.06** | x0.94 |
| g_neutral_282 | generated | 43 | CF, DCE, LICM, LU | **x1.06** | x1.01 |
| g_comp_397_neutral-branch | generated | 14 | DCE, CSE, LICM | **x1.06** | x1.05 |
| g_recur_087 | generated | 51 | CF, DCE, SR, LU | **x1.06** | x0.87 |
| g_unroll_259 | generated | 22 | DCE, CSE, SR | **x1.06** | x1.03 |
| g_unroll_061 | generated | 3 | CF, DCE | **x1.06** | x0.97 |
| g_unroll_072 | generated | 62 | DCE, CSE, LICM, SR, LU | **x1.06** | x1.02 |
| g_sr_145 | generated | 23 | CF, DCE, CSE, SR | **x1.06** | x1.06 |
| g_unroll_215 | generated | 17 | CF, SR | **x1.06** | x0.93 |
| g_comp_394_cse-recur | generated | 23 | CF, DCE, CSE, SR | **x1.06** | x1.04 |
| g_comp_150_branch-sr-sr | generated | 55 | CF, DCE, CSE, SR, LU | **x1.06** | x1.00 |
| g_comp_289_licm-licm-neutral | generated | 27 | CF, DCE, LICM, SR | **x1.06** | x0.92 |
| g_sr_222 | generated | 62 | DCE, CSE, LICM, SR, LU | **x1.06** | x1.03 |
| g_sr_299 | generated | 54 | DCE, CSE, SR, LU | **x1.06** | x1.01 |
| g_sr_244 | generated | 22 | DCE, CSE, SR | **x1.06** | x1.05 |
| g_comp_375_unroll-struct | generated | 9 | CF, LICM | **x1.06** | x0.93 |
| g_unroll_094 | generated | 30 | DCE, CSE, LICM, SR | **x1.06** | x1.03 |
| g_neutral_139 | generated | 29 | CF, CSE, LICM, SR | **x1.05** | x0.98 |
| g_unroll_083 | generated | 43 | CF, DCE, LICM, LU | **x1.05** | x1.02 |
| g_sr_178 | generated | 1 | CF | **x1.05** | x1.03 |
| g_comp_092_licm-nested-sr | generated | 47 | CF, DCE, CSE, LICM, LU | **x1.05** | x0.86 |
| g_unroll_050 | generated | 62 | DCE, CSE, LICM, SR, LU | **x1.05** | x0.94 |
| g_comp_126_sr-recur-sr | generated | 31 | CF, DCE, CSE, LICM, SR | **x1.05** | x0.78 |
| g_comp_091_neutral-branch-recur | generated | 44 | CSE, LICM, LU | **x1.05** | x0.93 |
| g_neutral_249 | generated | 45 | CF, CSE, LICM, LU | **x1.05** | x1.02 |
| g_recur_208 | generated | 61 | CF, CSE, LICM, SR, LU | **x1.05** | x0.96 |
| g_unroll_171 | generated | 22 | DCE, CSE, SR | **x1.05** | x1.00 |
| g_recur_274 | generated | 15 | CF, DCE, CSE, LICM | **x1.05** | x0.96 |
| g_comp_221_neutral-struct-branch-neutral | generated | 40 | LICM, LU | **x1.05** | x0.95 |
| g_comp_180_cse-neutral-neutral-unroll | generated | 54 | DCE, CSE, SR, LU | **x1.05** | x1.04 |
| g_comp_065_branch-neutral-licm | generated | 3 | CF, DCE | **x1.05** | x0.93 |
| g_recur_307 | generated | 25 | CF, LICM, SR | **x1.05** | x0.60 |
| g_unroll_028 | generated | 5 | CF, CSE | **x1.05** | x0.98 |
| newton_isqrt | loops | 14 | DCE, CSE, LICM | **x1.05** | x0.85 |
| g_comp_404_sr-unroll-sr | generated | 37 | CF, CSE, LU | **x1.05** | x0.92 |
| g_unroll_116 | generated | 63 | CF, DCE, CSE, LICM, SR, LU | **x1.05** | x1.05 |
| g_sr_156 | generated | 62 | DCE, CSE, LICM, SR, LU | **x1.04** | x0.95 |
| g_branch_250 | generated | 9 | CF, LICM | **x1.04** | x0.87 |
| g_neutral_161 | generated | 40 | LICM, LU | **x1.04** | x1.00 |
| g_comp_364_recur-sr | generated | 55 | CF, DCE, CSE, SR, LU | **x1.04** | x0.70 |
| g_sr_024 | generated | 63 | CF, DCE, CSE, LICM, SR, LU | **x1.04** | x1.04 |
| g_neutral_227 | generated | 32 | LU | **x1.04** | x1.01 |
| gcd_repeat | loops | 27 | CF, DCE, LICM, SR | **x1.04** | x0.92 |
| g_comp_205_struct-cse-branch-neutral | generated | 23 | CF, DCE, CSE, SR | **x1.04** | x0.99 |
| g_comp_054_neutral-neutral | generated | 1 | CF | **x1.04** | x0.95 |
| g_comp_282_branch-neutral-struct | generated | 62 | DCE, CSE, LICM, SR, LU | **x1.04** | x0.94 |
| g_neutral_106 | generated | 28 | CSE, LICM, SR | **x1.04** | x1.00 |
| g_comp_051_neutral-unroll-neutral-cf | generated | 35 | CF, DCE, LU | **x1.04** | x1.00 |
| g_unroll_325 | generated | 41 | CF, LICM, LU | **x1.04** | x1.03 |
| g_sr_189 | generated | 63 | CF, DCE, CSE, LICM, SR, LU | **x1.04** | x1.04 |
| g_branch_261 | generated | 4 | CSE | **x1.04** | x1.00 |
| g_branch_239 | generated | 42 | DCE, LICM, LU | **x1.04** | x1.02 |
| g_comp_076_neutral-licm-recur | generated | 27 | CF, DCE, LICM, SR | **x1.04** | x0.95 |
| g_neutral_293 | generated | 5 | CF, CSE | **x1.04** | x0.95 |
| g_comp_032_neutral-branch | generated | 39 | CF, DCE, CSE, LU | **x1.04** | x1.01 |
| g_comp_444_unroll-branch-sr | generated | 54 | DCE, CSE, SR, LU | **x1.04** | x0.82 |
| g_neutral_337 | generated | 33 | CF, LU | **x1.04** | x1.02 |
| g_branch_283 | generated | 39 | CF, DCE, CSE, LU | **x1.04** | x0.86 |
| g_comp_064_sr-branch | generated | 30 | DCE, CSE, LICM, SR | **x1.04** | x1.04 |
| g_comp_437_struct-branch-sr-unroll | generated | 22 | DCE, CSE, SR | **x1.04** | x1.00 |
| g_unroll_193 | generated | 12 | CSE, LICM | **x1.04** | x1.00 |
| g_neutral_007 | generated | 2 | DCE | **x1.04** | x1.00 |
| g_unroll_204 | generated | 9 | CF, LICM | **x1.03** | x1.01 |
| g_neutral_128 | generated | 31 | CF, DCE, CSE, LICM, SR | **x1.03** | x0.99 |
| g_comp_204_recur-licm-unroll | generated | 5 | CF, CSE | **x1.03** | x0.88 |
| g_recur_142 | generated | 49 | CF, SR, LU | **x1.03** | x1.01 |
| g_neutral_271 | generated | 18 | DCE, SR | **x1.03** | x0.99 |
| g_comp_186_struct-neutral | generated | 63 | CF, DCE, CSE, LICM, SR, LU | **x1.03** | x1.03 |
| g_branch_041 | generated | 3 | CF, DCE | **x1.03** | x0.92 |
| g_recur_131 | generated | 61 | CF, CSE, LICM, SR, LU | **x1.03** | x0.99 |
| g_neutral_216 | generated | 56 | LICM, SR, LU | **x1.03** | x1.00 |
| g_neutral_304 | generated | 23 | CF, DCE, CSE, SR | **x1.03** | x1.01 |
| g_sr_233 | generated | 32 | LU | **x1.03** | x1.03 |
| g_unroll_270 | generated | 22 | DCE, CSE, SR | **x1.03** | x1.00 |
| g_recur_263 | generated | 38 | DCE, CSE, LU | **x1.03** | x0.99 |
| g_neutral_183 | generated | 2 | DCE | **x1.03** | x0.99 |
| g_neutral_117 | generated | 29 | CF, CSE, LICM, SR | **x1.03** | x0.97 |
| g_comp_224_sr-struct-sr | generated | 29 | CF, CSE, LICM, SR | **x1.03** | x0.91 |
| g_neutral_029 | generated | 20 | CSE, SR | **x1.03** | x0.98 |
| g_neutral_051 | generated | 44 | CSE, LICM, LU | **x1.03** | x0.98 |
| g_recur_219 | generated | 56 | LICM, SR, LU | **x1.03** | x0.89 |
| g_comp_102_neutral-recur-unroll-sr | generated | 27 | CF, DCE, LICM, SR | **x1.03** | x0.88 |
| g_comp_124_unroll-recur-sr-struct | generated | 39 | CF, DCE, CSE, LU | **x1.03** | x0.67 |
| g_comp_187_sr-unroll | generated | 30 | DCE, CSE, LICM, SR | **x1.03** | x1.00 |
| g_neutral_326 | generated | 56 | LICM, SR, LU | **x1.02** | x1.00 |
| g_neutral_260 | generated | 37 | CF, CSE, LU | **x1.02** | x0.99 |
| g_neutral_194 | generated | 10 | DCE, LICM | **x1.02** | x0.99 |
| g_neutral_073 | generated | 12 | CSE, LICM | **x1.02** | x1.00 |
| g_comp_211_sr-unroll-struct-recur | generated | 2 | DCE | **x1.02** | x0.81 |
| g_neutral_238 | generated | 40 | LICM, LU | **x1.02** | x1.00 |
| g_recur_197 | generated | 42 | DCE, LICM, LU | **x1.02** | x0.98 |
| g_neutral_315 | generated | 32 | LU | **x1.01** | x0.99 |
| g_neutral_205 | generated | 35 | CF, DCE, LU | **x1.01** | x0.96 |
| g_neutral_150 | generated | 8 | LICM | **x1.01** | x0.93 |
| g_branch_228 | generated | 34 | DCE, LU | **x1.01** | x0.93 |
| g_neutral_040 | generated | 2 | DCE | **x1.01** | x0.97 |
| g_unroll_347 | generated | 51 | CF, DCE, SR, LU | **x1.01** | x1.00 |
| g_comp_242_unroll-recur-unroll | generated | 11 | CF, DCE, LICM | **x1.00** | x0.85 |
| g_branch_217 | generated | 0 | - | **x1.00** | x0.99 |
| g_neutral_062 | generated | 0 | - | **x1.00** | x0.95 |
| g_recur_065 | generated | 0 | - | **x1.00** | x0.97 |

## Method notes

- `gcc -O0` is intentional: at `-O0` the C compiler does essentially no optimization, so the delta is what the MiniC optimizer contributed.
- Benchmarks are sized so combo 0 runs ~40-200 ms, well above scheduler noise; several are division-heavy because an integer divide is a large, non-pipelined cost that removing is clearly visible.
- Every combo is verified to reproduce combo 0's exit code before its time is recorded (`benchmarks/ground_truth.csv`); a miscompiled binary never contributes a timing sample.
- Strength reduction can slightly *pessimize* tight loops where the multiply it removes is already cheap under `-O0` -- visible in the corpus, and exactly the kind of call the recommender learns to make.