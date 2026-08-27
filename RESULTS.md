# MiniC optimizer: measured speedup results

**270 MiniC benchmarks**, each emitted as C at every one of the **64 pass combinations** (6 independently toggleable passes), compiled with **`gcc -O0`**, and timed (median of 6 wall-clock runs after 3 warm-ups).

`speedup = time(combo 0, no passes) / time(combo)` -- how much the MiniC TAC optimizer beats *not* optimizing, with the C compiler pinned at `-O0` so the measured gain is ours, not gcc's.

## Headline

- **Best combo per program, geomean speedup: x1.50**  (max **x4.57**)
- All 6 passes on (combo 63): geomean x1.21
- Safe strong default -- combo 0 [baseline]: geomean x1.00, and never worse than x1.00 on any program
- No single combo is best everywhere: the all-passes combo is left on the table (>2% slower than the per-program best) on **243 / 270** programs -- which is why a per-program recommender is worth having.

### by category (best-combo geomean)

- structs: x3.08
- loops: x1.81
- strings: x1.57
- generated: x1.47
- numeric: x1.37
- recursion: x1.24

## ML recommendation (RandomForest, GroupKFold by program_id)

Cross-validation holds *whole programs* out -- a program's rows share identical static features, so a random split would leak.

- Model: **hist gradient boosting**, 270 held-out programs (270 programs, 5 folds)
- Speedup-prediction MAE: 0.163
- Recommendations that regress the program (>2% slower than baseline): **21%**
- **Model-recommended combo, mean true speedup on unseen programs: x1.26**
- Baseline (combo 0): x1.00   |   oracle (best combo in hindsight): x1.54
- Model captures **49%** of the available speedup without ever having timed the program.

## Per-program

| program | category | best combo | passes | best speedup | all-on |
|---|---|--:|---|--:|--:|
| distance_accum | structs | 63 | CF, DCE, CSE, LICM, SR, LU | **x4.57** | x4.57 |
| complex_arith | structs | 63 | CF, DCE, CSE, LICM, SR, LU | **x4.39** | x4.39 |
| bbox | structs | 63 | CF, DCE, CSE, LICM, SR, LU | **x3.22** | x3.22 |
| cse_subexpr | loops | 6 | DCE, CSE | **x2.61** | x2.15 |
| licm_div | loops | 55 | CF, DCE, CSE, SR, LU | **x2.59** | x2.37 |
| const_fold | loops | 55 | CF, DCE, CSE, SR, LU | **x2.51** | x2.30 |
| cse_mod | loops | 54 | DCE, CSE, SR, LU | **x2.37** | x1.94 |
| const_prop | loops | 39 | CF, DCE, CSE, LU | **x2.36** | x1.84 |
| g_div_004 | generated | 51 | CF, DCE, SR, LU | **x2.31** | x1.96 |
| g_cse_025 | generated | 55 | CF, DCE, CSE, SR, LU | **x2.26** | x1.70 |
| g_cse_057 | generated | 46 | DCE, CSE, LICM, LU | **x2.21** | x1.52 |
| g_cse_017 | generated | 54 | DCE, CSE, SR, LU | **x2.14** | x1.52 |
| g_licm_080 | generated | 43 | CF, DCE, LICM, LU | **x2.10** | x1.49 |
| g_cf_091 | generated | 59 | CF, DCE, LICM, SR, LU | **x2.06** | x1.60 |
| g_comp_085_div-div-licm | generated | 3 | CF, DCE | **x2.06** | x1.29 |
| g_cse_081 | generated | 6 | DCE, CSE | **x2.06** | x1.80 |
| g_comp_080_neutral-licm | generated | 47 | CF, DCE, CSE, LICM, LU | **x2.04** | x1.45 |
| g_div_012 | generated | 12 | CSE, LICM | **x2.03** | x1.64 |
| g_comp_128_licm-cf | generated | 29 | CF, CSE, LICM, SR | **x2.03** | x1.44 |
| g_comp_094_cf-cse | generated | 15 | CF, DCE, CSE, LICM | **x2.02** | x1.30 |
| g_licm_024 | generated | 35 | CF, DCE, LU | **x2.01** | x1.36 |
| polynomial | loops | 38 | DCE, CSE, LU | **x2.01** | x1.85 |
| g_licm_032 | generated | 11 | CF, DCE, LICM | **x2.01** | x1.22 |
| g_cse_049 | generated | 23 | CF, DCE, CSE, SR | **x2.01** | x1.75 |
| g_licm_008 | generated | 19 | CF, DCE, SR | **x1.99** | x1.38 |
| g_comp_078_cse-licm-unroll-unroll | generated | 46 | DCE, CSE, LICM, LU | **x1.99** | x1.29 |
| licm_arith | loops | 63 | CF, DCE, CSE, LICM, SR, LU | **x1.98** | x1.98 |
| g_comp_092_cf-cf-sr | generated | 15 | CF, DCE, CSE, LICM | **x1.98** | x1.43 |
| g_comp_044_unroll-sr | generated | 63 | CF, DCE, CSE, LICM, SR, LU | **x1.97** | x1.97 |
| g_cf_035 | generated | 11 | CF, DCE, LICM | **x1.97** | x1.60 |
| g_comp_090_cf-div-div | generated | 35 | CF, DCE, LU | **x1.96** | x1.35 |
| g_div_092 | generated | 63 | CF, DCE, CSE, LICM, SR, LU | **x1.91** | x1.91 |
| nested_licm | loops | 55 | CF, DCE, CSE, SR, LU | **x1.91** | x1.90 |
| g_comp_140_cse-cse-unroll-cse | generated | 30 | DCE, CSE, LICM, SR | **x1.90** | x1.52 |
| g_comp_117_cse-cse | generated | 63 | CF, DCE, CSE, LICM, SR, LU | **x1.89** | x1.89 |
| g_cse_009 | generated | 54 | DCE, CSE, SR, LU | **x1.89** | x1.42 |
| g_comp_088_div-struct-neutral-cf | generated | 15 | CF, DCE, CSE, LICM | **x1.88** | x1.47 |
| g_comp_114_cse-cf-cse-unroll | generated | 47 | CF, DCE, CSE, LICM, LU | **x1.87** | x1.30 |
| g_licm_072 | generated | 7 | CF, DCE, CSE | **x1.87** | x1.54 |
| g_div_020 | generated | 63 | CF, DCE, CSE, LICM, SR, LU | **x1.86** | x1.86 |
| g_comp_038_sr-cf-licm | generated | 63 | CF, DCE, CSE, LICM, SR, LU | **x1.86** | x1.86 |
| g_comp_049_cse-sr | generated | 52 | CSE, SR, LU | **x1.85** | x1.25 |
| g_cf_051 | generated | 3 | CF, DCE | **x1.84** | x1.43 |
| g_comp_103_unroll-licm-unroll-licm | generated | 29 | CF, CSE, LICM, SR | **x1.83** | x1.34 |
| g_comp_142_sr-unroll-cse-cf | generated | 46 | DCE, CSE, LICM, LU | **x1.82** | x1.23 |
| g_licm_040 | generated | 47 | CF, DCE, CSE, LICM, LU | **x1.81** | x1.67 |
| licm_mixed | loops | 47 | CF, DCE, CSE, LICM, LU | **x1.81** | x1.58 |
| g_cf_067 | generated | 51 | CF, DCE, SR, LU | **x1.81** | x1.78 |
| g_comp_021_licm-cf-licm | generated | 39 | CF, DCE, CSE, LU | **x1.81** | x1.63 |
| g_div_060 | generated | 45 | CF, CSE, LICM, LU | **x1.80** | x1.45 |
| g_comp_046_unroll-struct-div-unroll | generated | 57 | CF, LICM, SR, LU | **x1.79** | x1.47 |
| g_div_068 | generated | 15 | CF, DCE, CSE, LICM | **x1.77** | x1.48 |
| g_comp_113_cf-unroll-licm | generated | 55 | CF, DCE, CSE, SR, LU | **x1.77** | x1.27 |
| g_comp_096_cse-sr-licm | generated | 28 | CSE, LICM, SR | **x1.76** | x1.37 |
| g_comp_095_struct-sr-struct-cf | generated | 35 | CF, DCE, LU | **x1.75** | x1.41 |
| g_comp_019_cf-neutral-cf | generated | 41 | CF, LICM, LU | **x1.74** | x1.52 |
| g_div_028 | generated | 27 | CF, DCE, LICM, SR | **x1.73** | x1.19 |
| cse_chain | loops | 38 | DCE, CSE, LU | **x1.73** | x1.70 |
| g_comp_056_struct-struct | generated | 60 | CSE, LICM, SR, LU | **x1.72** | x1.25 |
| g_comp_060_div-div | generated | 35 | CF, DCE, LU | **x1.72** | x1.35 |
| g_comp_138_cse-licm-struct | generated | 61 | CF, CSE, LICM, SR, LU | **x1.72** | x1.42 |
| g_comp_025_licm-div | generated | 19 | CF, DCE, SR | **x1.72** | x1.44 |
| g_comp_081_cse-cse-neutral-cf | generated | 55 | CF, DCE, CSE, SR, LU | **x1.72** | x1.36 |
| g_comp_143_licm-cf | generated | 43 | CF, DCE, LICM, LU | **x1.72** | x1.67 |
| g_cf_003 | generated | 7 | CF, DCE, CSE | **x1.71** | x1.19 |
| g_cse_073 | generated | 38 | DCE, CSE, LU | **x1.70** | x1.25 |
| g_comp_091_cse-unroll-cse | generated | 14 | DCE, CSE, LICM | **x1.70** | x1.48 |
| dotprod | numeric | 62 | DCE, CSE, LICM, SR, LU | **x1.70** | x1.37 |
| g_comp_016_struct-sr-cf | generated | 46 | DCE, CSE, LICM, LU | **x1.69** | x1.55 |
| g_comp_007_cf-cse-sr-struct | generated | 63 | CF, DCE, CSE, LICM, SR, LU | **x1.68** | x1.68 |
| g_comp_109_struct-sr-cf | generated | 25 | CF, LICM, SR | **x1.68** | x1.33 |
| g_comp_079_cse-cf-licm-neutral | generated | 55 | CF, DCE, CSE, SR, LU | **x1.67** | x1.33 |
| g_comp_020_unroll-cf-licm | generated | 61 | CF, CSE, LICM, SR, LU | **x1.67** | x1.42 |
| g_comp_121_cf-unroll-cf | generated | 12 | CSE, LICM | **x1.67** | x1.18 |
| g_cf_083 | generated | 25 | CF, LICM, SR | **x1.67** | x1.57 |
| g_cse_041 | generated | 55 | CF, DCE, CSE, SR, LU | **x1.66** | x1.30 |
| g_comp_052_licm-cse-struct-div | generated | 7 | CF, DCE, CSE | **x1.66** | x1.57 |
| g_comp_017_cf-cse-cf | generated | 43 | CF, DCE, LICM, LU | **x1.65** | x1.17 |
| g_comp_023_cf-struct-struct | generated | 45 | CF, CSE, LICM, LU | **x1.65** | x1.13 |
| g_licm_016 | generated | 10 | DCE, LICM | **x1.65** | x1.26 |
| g_cf_019 | generated | 23 | CF, DCE, CSE, SR | **x1.64** | x1.28 |
| licm_cond | loops | 11 | CF, DCE, LICM | **x1.64** | x1.35 |
| vowel_count | strings | 59 | CF, DCE, LICM, SR, LU | **x1.63** | x1.56 |
| g_comp_035_sr-licm | generated | 15 | CF, DCE, CSE, LICM | **x1.63** | x1.23 |
| g_unroll_006 | generated | 6 | DCE, CSE | **x1.62** | x1.21 |
| g_sr_050 | generated | 62 | DCE, CSE, LICM, SR, LU | **x1.62** | x1.09 |
| g_comp_118_struct-sr-cf-struct | generated | 31 | CF, DCE, CSE, LICM, SR | **x1.62** | x1.24 |
| g_comp_076_unroll-sr | generated | 5 | CF, CSE | **x1.62** | x1.32 |
| g_comp_105_licm-licm-licm-div | generated | 17 | CF, SR | **x1.61** | x1.39 |
| g_comp_062_cf-sr-struct-neutral | generated | 15 | CF, DCE, CSE, LICM | **x1.60** | x1.41 |
| g_unroll_046 | generated | 22 | DCE, CSE, SR | **x1.60** | x1.07 |
| g_comp_051_unroll-sr-div-cse | generated | 45 | CF, CSE, LICM, LU | **x1.60** | x1.01 |
| g_licm_088 | generated | 51 | CF, DCE, SR, LU | **x1.59** | x1.09 |
| g_struct_093 | generated | 54 | DCE, CSE, SR, LU | **x1.59** | x1.17 |
| g_div_044 | generated | 62 | DCE, CSE, LICM, SR, LU | **x1.59** | x1.49 |
| g_comp_125_cse-cse-struct-div | generated | 14 | DCE, CSE, LICM | **x1.58** | x1.30 |
| g_comp_054_sr-licm-licm | generated | 25 | CF, LICM, SR | **x1.58** | x1.18 |
| g_sr_034 | generated | 29 | CF, CSE, LICM, SR | **x1.58** | x1.12 |
| g_comp_070_div-unroll | generated | 35 | CF, DCE, LU | **x1.58** | x1.11 |
| g_comp_077_unroll-div-licm | generated | 61 | CF, CSE, LICM, SR, LU | **x1.57** | x1.55 |
| g_comp_043_sr-struct-div | generated | 62 | DCE, CSE, LICM, SR, LU | **x1.57** | x1.44 |
| g_sr_002 | generated | 30 | DCE, CSE, LICM, SR | **x1.56** | x1.05 |
| g_comp_058_sr-unroll-licm | generated | 57 | CF, LICM, SR, LU | **x1.56** | x1.02 |
| g_unroll_078 | generated | 21 | CF, CSE, SR | **x1.55** | x1.19 |
| g_sr_082 | generated | 7 | CF, DCE, CSE | **x1.54** | x1.12 |
| g_div_084 | generated | 1 | CF | **x1.54** | x1.50 |
| g_struct_005 | generated | 15 | CF, DCE, CSE, LICM | **x1.54** | x1.05 |
| g_sr_018 | generated | 30 | DCE, CSE, LICM, SR | **x1.53** | x1.02 |
| g_comp_050_neutral-neutral-cf-sr | generated | 39 | CF, DCE, CSE, LU | **x1.53** | x1.18 |
| g_cf_059 | generated | 11 | CF, DCE, LICM | **x1.52** | x1.25 |
| g_comp_123_sr-div-neutral-struct | generated | 62 | DCE, CSE, LICM, SR, LU | **x1.52** | x1.36 |
| g_comp_139_unroll-struct-cf | generated | 55 | CF, DCE, CSE, SR, LU | **x1.52** | x1.06 |
| g_comp_010_licm-sr-licm | generated | 9 | CF, LICM | **x1.52** | x1.38 |
| vector_scale | numeric | 47 | CF, DCE, CSE, LICM, LU | **x1.51** | x1.48 |
| caesar | strings | 54 | DCE, CSE, SR, LU | **x1.51** | x1.32 |
| g_sr_090 | generated | 15 | CF, DCE, CSE, LICM | **x1.50** | x1.29 |
| g_comp_014_neutral-cf | generated | 27 | CF, DCE, LICM, SR | **x1.50** | x1.17 |
| g_div_036 | generated | 51 | CF, DCE, SR, LU | **x1.50** | x1.21 |
| g_sr_042 | generated | 23 | CF, DCE, CSE, SR | **x1.50** | x1.27 |
| g_unroll_094 | generated | 44 | CSE, LICM, LU | **x1.49** | x1.14 |
| g_comp_041_struct-cse | generated | 63 | CF, DCE, CSE, LICM, SR, LU | **x1.49** | x1.49 |
| g_licm_064 | generated | 12 | CSE, LICM | **x1.49** | x1.15 |
| g_comp_030_cse-neutral-licm-cse | generated | 46 | DCE, CSE, LICM, LU | **x1.49** | x1.48 |
| g_comp_089_sr-struct | generated | 39 | CF, DCE, CSE, LU | **x1.49** | x1.20 |
| g_struct_053 | generated | 55 | CF, DCE, CSE, SR, LU | **x1.49** | x1.02 |
| g_comp_065_cf-unroll-unroll-cf | generated | 15 | CF, DCE, CSE, LICM | **x1.49** | x1.01 |
| g_cf_011 | generated | 7 | CF, DCE, CSE | **x1.47** | x1.15 |
| g_comp_009_cf-cse | generated | 23 | CF, DCE, CSE, SR | **x1.47** | x1.17 |
| g_comp_137_struct-licm-licm-unroll | generated | 35 | CF, DCE, LU | **x1.47** | x1.29 |
| g_cf_027 | generated | 29 | CF, CSE, LICM, SR | **x1.47** | x1.15 |
| g_comp_027_cse-div | generated | 15 | CF, DCE, CSE, LICM | **x1.47** | x1.21 |
| g_comp_071_cf-div-struct | generated | 9 | CF, LICM | **x1.47** | x1.27 |
| g_comp_024_licm-div-struct | generated | 33 | CF, LU | **x1.47** | x1.44 |
| g_div_052 | generated | 36 | CSE, LU | **x1.47** | x1.16 |
| g_comp_064_cf-unroll-neutral | generated | 45 | CF, CSE, LICM, LU | **x1.46** | x1.19 |
| g_struct_045 | generated | 34 | DCE, LU | **x1.46** | x1.15 |
| g_comp_136_struct-div-cf-licm | generated | 43 | CF, DCE, LICM, LU | **x1.46** | x1.25 |
| g_unroll_014 | generated | 55 | CF, DCE, CSE, SR, LU | **x1.45** | x0.94 |
| g_cf_075 | generated | 55 | CF, DCE, CSE, SR, LU | **x1.45** | x1.16 |
| g_comp_120_licm-div | generated | 28 | CSE, LICM, SR | **x1.45** | x1.24 |
| g_comp_082_struct-sr | generated | 30 | DCE, CSE, LICM, SR | **x1.45** | x1.09 |
| g_comp_099_sr-cf-sr | generated | 3 | CF, DCE | **x1.44** | x0.95 |
| g_comp_069_unroll-cf-unroll-neutral | generated | 15 | CF, DCE, CSE, LICM | **x1.44** | x1.32 |
| g_comp_042_sr-neutral | generated | 59 | CF, DCE, LICM, SR, LU | **x1.44** | x1.10 |
| g_comp_036_cse-cse | generated | 44 | CSE, LICM, LU | **x1.43** | x1.30 |
| g_comp_053_neutral-licm-licm | generated | 15 | CF, DCE, CSE, LICM | **x1.43** | x1.29 |
| g_comp_110_cse-unroll-neutral-neutral | generated | 23 | CF, DCE, CSE, SR | **x1.43** | x1.39 |
| g_comp_040_cse-sr | generated | 62 | DCE, CSE, LICM, SR, LU | **x1.42** | x1.01 |
| g_comp_106_div-unroll | generated | 34 | DCE, LU | **x1.42** | x1.15 |
| g_struct_021 | generated | 17 | CF, SR | **x1.42** | x0.96 |
| g_comp_073_unroll-cf-sr | generated | 19 | CF, DCE, SR | **x1.41** | x1.06 |
| g_struct_061 | generated | 23 | CF, DCE, CSE, SR | **x1.41** | x1.19 |
| g_comp_072_licm-cf-cse-div | generated | 7 | CF, DCE, CSE | **x1.41** | x1.26 |
| g_sr_058 | generated | 37 | CF, CSE, LU | **x1.41** | x1.06 |
| g_comp_116_unroll-licm-licm-div | generated | 55 | CF, DCE, CSE, SR, LU | **x1.41** | x0.97 |
| g_comp_097_div-sr | generated | 14 | DCE, CSE, LICM | **x1.41** | x0.98 |
| g_comp_075_neutral-neutral | generated | 56 | LICM, SR, LU | **x1.40** | x1.21 |
| g_comp_015_struct-cf | generated | 30 | DCE, CSE, LICM, SR | **x1.40** | x1.11 |
| g_comp_031_neutral-div | generated | 29 | CF, CSE, LICM, SR | **x1.40** | x0.93 |
| g_comp_032_cf-licm-struct | generated | 46 | DCE, CSE, LICM, LU | **x1.40** | x0.98 |
| g_struct_077 | generated | 50 | DCE, SR, LU | **x1.39** | x1.30 |
| g_comp_004_unroll-struct-neutral-sr | generated | 47 | CF, DCE, CSE, LICM, LU | **x1.39** | x1.11 |
| g_comp_107_cf-unroll-cf-struct | generated | 29 | CF, CSE, LICM, SR | **x1.39** | x0.96 |
| g_comp_101_unroll-licm-div | generated | 25 | CF, LICM, SR | **x1.39** | x1.18 |
| g_comp_131_neutral-sr | generated | 38 | DCE, CSE, LU | **x1.39** | x1.06 |
| g_comp_063_unroll-sr | generated | 22 | DCE, CSE, SR | **x1.38** | x0.78 |
| particle_sim | structs | 52 | CSE, SR, LU | **x1.38** | x1.30 |
| g_comp_124_sr-div | generated | 39 | CF, DCE, CSE, LU | **x1.38** | x1.03 |
| g_comp_127_licm-sr-unroll | generated | 62 | DCE, CSE, LICM, SR, LU | **x1.38** | x1.08 |
| g_comp_018_unroll-div | generated | 31 | CF, DCE, CSE, LICM, SR | **x1.37** | x1.03 |
| g_comp_066_cse-licm-div | generated | 45 | CF, CSE, LICM, LU | **x1.37** | x0.91 |
| g_comp_115_sr-cse-div-struct | generated | 12 | CSE, LICM | **x1.37** | x1.07 |
| g_sr_026 | generated | 12 | CSE, LICM | **x1.37** | x0.94 |
| g_comp_119_sr-struct-licm-neutral | generated | 6 | DCE, CSE | **x1.37** | x1.16 |
| g_comp_061_licm-struct | generated | 43 | CF, DCE, LICM, LU | **x1.37** | x0.91 |
| g_sr_074 | generated | 11 | CF, DCE, LICM | **x1.37** | x1.08 |
| g_comp_045_struct-neutral | generated | 2 | DCE | **x1.37** | x1.27 |
| g_comp_141_cse-sr-struct | generated | 60 | CSE, LICM, SR, LU | **x1.37** | x1.05 |
| g_comp_093_cse-struct-neutral | generated | 37 | CF, CSE, LU | **x1.37** | x0.85 |
| g_comp_067_sr-unroll | generated | 44 | CSE, LICM, LU | **x1.36** | x1.07 |
| g_unroll_070 | generated | 48 | SR, LU | **x1.36** | x0.96 |
| g_comp_122_unroll-unroll | generated | 46 | DCE, CSE, LICM, LU | **x1.36** | x1.07 |
| g_cf_043 | generated | 3 | CF, DCE | **x1.36** | x1.19 |
| g_struct_085 | generated | 55 | CF, DCE, CSE, SR, LU | **x1.36** | x1.26 |
| g_unroll_030 | generated | 55 | CF, DCE, CSE, SR, LU | **x1.36** | x0.92 |
| g_licm_056 | generated | 57 | CF, LICM, SR, LU | **x1.35** | x0.88 |
| g_comp_135_licm-licm | generated | 62 | DCE, CSE, LICM, SR, LU | **x1.35** | x1.08 |
| stencil_1d | numeric | 54 | DCE, CSE, SR, LU | **x1.35** | x1.26 |
| g_comp_006_cse-cse-neutral-div | generated | 20 | CSE, SR | **x1.35** | x1.27 |
| g_comp_102_licm-licm-cse-cf | generated | 13 | CF, CSE, LICM | **x1.34** | x1.31 |
| g_comp_084_cse-struct | generated | 30 | DCE, CSE, LICM, SR | **x1.34** | x1.01 |
| fib | recursion | 62 | DCE, CSE, LICM, SR, LU | **x1.34** | x1.33 |
| g_comp_005_licm-sr | generated | 43 | CF, DCE, LICM, LU | **x1.34** | x1.06 |
| g_comp_029_div-cf-neutral | generated | 3 | CF, DCE | **x1.33** | x1.18 |
| g_div_076 | generated | 43 | CF, DCE, LICM, LU | **x1.33** | x1.00 |
| g_comp_059_sr-cse-cse | generated | 54 | DCE, CSE, SR, LU | **x1.33** | x0.93 |
| g_licm_048 | generated | 19 | CF, DCE, SR | **x1.32** | x0.97 |
| g_cse_065 | generated | 39 | CF, DCE, CSE, LU | **x1.32** | x1.04 |
| strength_reduce | loops | 55 | CF, DCE, CSE, SR, LU | **x1.31** | x1.19 |
| conv1d | numeric | 55 | CF, DCE, CSE, SR, LU | **x1.31** | x1.28 |
| g_unroll_054 | generated | 37 | CF, CSE, LU | **x1.30** | x0.82 |
| g_comp_022_cse-struct-unroll | generated | 39 | CF, DCE, CSE, LU | **x1.30** | x1.22 |
| g_comp_057_struct-neutral | generated | 47 | CF, DCE, CSE, LICM, LU | **x1.30** | x1.06 |
| g_comp_111_neutral-unroll | generated | 7 | CF, DCE, CSE | **x1.29** | x1.04 |
| g_comp_008_div-neutral | generated | 50 | DCE, SR, LU | **x1.28** | x1.15 |
| g_cse_033 | generated | 38 | DCE, CSE, LU | **x1.28** | x1.13 |
| g_comp_011_unroll-unroll | generated | 51 | CF, DCE, SR, LU | **x1.27** | x1.01 |
| g_comp_132_cf-struct-cse-unroll | generated | 63 | CF, DCE, CSE, LICM, SR, LU | **x1.27** | x1.27 |
| g_comp_100_div-cf | generated | 9 | CF, LICM | **x1.26** | x1.26 |
| g_comp_013_struct-div-div | generated | 62 | DCE, CSE, LICM, SR, LU | **x1.26** | x1.02 |
| g_cse_001 | generated | 47 | CF, DCE, CSE, LICM, LU | **x1.26** | x1.00 |
| g_comp_012_div-sr-cf-div | generated | 15 | CF, DCE, CSE, LICM | **x1.25** | x1.16 |
| g_comp_098_div-sr-struct-unroll | generated | 14 | DCE, CSE, LICM | **x1.25** | x0.85 |
| g_comp_026_unroll-sr | generated | 13 | CF, CSE, LICM | **x1.25** | x1.03 |
| tak | recursion | 61 | CF, CSE, LICM, SR, LU | **x1.24** | x0.93 |
| g_comp_112_unroll-unroll | generated | 4 | CSE | **x1.24** | x0.91 |
| g_struct_037 | generated | 34 | DCE, LU | **x1.23** | x0.85 |
| g_comp_000_cf-neutral-cf-neutral | generated | 49 | CF, SR, LU | **x1.22** | x1.15 |
| g_comp_002_struct-struct-struct | generated | 20 | CSE, SR | **x1.22** | x1.10 |
| g_unroll_022 | generated | 34 | DCE, LU | **x1.20** | x0.99 |
| g_comp_087_licm-unroll-neutral | generated | 21 | CF, CSE, SR | **x1.20** | x1.04 |
| g_struct_069 | generated | 37 | CF, CSE, LU | **x1.20** | x0.96 |
| g_sr_066 | generated | 36 | CSE, LU | **x1.20** | x0.91 |
| g_cse_089 | generated | 38 | DCE, CSE, LU | **x1.20** | x0.94 |
| g_unroll_038 | generated | 54 | DCE, CSE, SR, LU | **x1.20** | x0.92 |
| histogram | numeric | 55 | CF, DCE, CSE, SR, LU | **x1.20** | x1.09 |
| g_comp_055_div-neutral-cse-sr | generated | 1 | CF | **x1.20** | x0.92 |
| matrix_mult | numeric | 63 | CF, DCE, CSE, LICM, SR, LU | **x1.19** | x1.19 |
| g_struct_029 | generated | 47 | CF, DCE, CSE, LICM, LU | **x1.19** | x0.94 |
| g_comp_048_struct-neutral | generated | 16 | SR | **x1.19** | x1.05 |
| g_neutral_007 | generated | 17 | CF, SR | **x1.19** | x1.05 |
| g_neutral_095 | generated | 20 | CSE, SR | **x1.18** | x1.04 |
| g_neutral_087 | generated | 59 | CF, DCE, LICM, SR, LU | **x1.18** | x1.12 |
| gcd_repeat | loops | 35 | CF, DCE, LU | **x1.18** | x1.04 |
| g_comp_039_struct-neutral-neutral-sr | generated | 47 | CF, DCE, CSE, LICM, LU | **x1.18** | x0.99 |
| g_comp_037_unroll-cse | generated | 7 | CF, DCE, CSE | **x1.18** | x1.04 |
| g_comp_134_div-cse-neutral-unroll | generated | 30 | DCE, CSE, LICM, SR | **x1.18** | x1.15 |
| g_comp_047_struct-licm-licm-cf | generated | 35 | CF, DCE, LU | **x1.17** | x1.03 |
| g_unroll_062 | generated | 34 | DCE, LU | **x1.17** | x0.89 |
| g_comp_108_licm-sr | generated | 29 | CF, CSE, LICM, SR | **x1.16** | x0.98 |
| g_sr_010 | generated | 50 | DCE, SR, LU | **x1.16** | x0.89 |
| g_neutral_071 | generated | 17 | CF, SR | **x1.15** | x1.00 |
| ackermann | recursion | 18 | DCE, SR | **x1.15** | x1.13 |
| g_neutral_023 | generated | 13 | CF, CSE, LICM | **x1.15** | x0.98 |
| g_neutral_079 | generated | 14 | DCE, CSE, LICM | **x1.15** | x1.00 |
| prime_sieve | loops | 55 | CF, DCE, CSE, SR, LU | **x1.15** | x1.14 |
| g_neutral_015 | generated | 29 | CF, CSE, LICM, SR | **x1.14** | x0.98 |
| newton_isqrt | loops | 52 | CSE, SR, LU | **x1.13** | x0.99 |
| g_comp_129_neutral-licm-cf-unroll | generated | 38 | DCE, CSE, LU | **x1.13** | x1.01 |
| g_comp_083_licm-cse | generated | 49 | CF, SR, LU | **x1.12** | x0.71 |
| g_comp_001_licm-cse | generated | 30 | DCE, CSE, LICM, SR | **x1.12** | x1.03 |
| g_licm_000 | generated | 45 | CF, CSE, LICM, LU | **x1.11** | x0.81 |
| g_comp_126_sr-licm-struct | generated | 57 | CF, LICM, SR, LU | **x1.11** | x0.86 |
| g_comp_074_neutral-div-neutral-struct | generated | 39 | CF, DCE, CSE, LU | **x1.10** | x1.09 |
| g_comp_086_licm-struct-div-div | generated | 31 | CF, DCE, CSE, LICM, SR | **x1.10** | x0.84 |
| g_comp_133_neutral-struct-div | generated | 31 | CF, DCE, CSE, LICM, SR | **x1.10** | x0.90 |
| g_neutral_047 | generated | 7 | CF, DCE, CSE | **x1.09** | x1.00 |
| g_neutral_039 | generated | 32 | LU | **x1.09** | x0.96 |
| g_neutral_055 | generated | 22 | DCE, CSE, SR | **x1.09** | x1.07 |
| g_comp_003_licm-cse | generated | 23 | CF, DCE, CSE, SR | **x1.08** | x1.00 |
| g_neutral_063 | generated | 14 | DCE, CSE, LICM | **x1.08** | x0.97 |
| g_unroll_086 | generated | 31 | CF, DCE, CSE, LICM, SR | **x1.08** | x0.77 |
| g_neutral_031 | generated | 3 | CF, DCE | **x1.07** | x0.97 |
| g_comp_104_struct-unroll | generated | 25 | CF, LICM, SR | **x1.06** | x0.95 |
| g_comp_034_unroll-unroll-licm | generated | 20 | CSE, SR | **x1.05** | x0.82 |
| g_comp_068_cse-unroll | generated | 32 | LU | **x1.02** | x0.64 |
| g_struct_013 | generated | 22 | DCE, CSE, SR | **x1.02** | x1.00 |
| g_comp_028_sr-unroll | generated | 31 | CF, DCE, CSE, LICM, SR | **x1.02** | x0.95 |
| g_comp_130_neutral-neutral | generated | 11 | CF, DCE, LICM | **x1.01** | x0.81 |
| g_comp_033_cse-sr | generated | 0 | - | **x1.00** | x0.88 |

## Method notes

- `gcc -O0` is intentional: at `-O0` the C compiler does essentially no optimization, so the delta is what the MiniC optimizer contributed.
- Benchmarks are sized so combo 0 runs ~40-200 ms, well above scheduler noise; several are division-heavy because an integer divide is a large, non-pipelined cost that removing is clearly visible.
- Every combo is verified to reproduce combo 0's exit code before its time is recorded (`benchmarks/ground_truth.csv`); a miscompiled binary never contributes a timing sample.
- Strength reduction can slightly *pessimize* tight loops where the multiply it removes is already cheap under `-O0` -- visible in the corpus, and exactly the kind of call the recommender learns to make.