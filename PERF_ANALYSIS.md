# Performance analysis: how the passes behave on real hardware

Computed from **57,600 timed configurations** (900 programs x 64 pass combos, `gcc -O0`, least of 15 runs). Unoptimized run time per program: 5.6-210.5 ms (median 12.1 ms). Regenerate with `python -m src.minic.harness.perf_analysis`.

## 1. Per-pass effect: alone vs. in context

*alone* = geomean speedup of enabling only that pass. *marginal* = geomean speedup of adding it, averaged over all 32 contexts of the other five passes. *context range* = the spread of that marginal across contexts. *helps / hurts* = share of programs where adding the pass is >2% faster / slower on average.

| pass | alone | marginal | context range | helps | hurts |
|---|--:|--:|--:|--:|--:|
| CF | x1.043 | x1.042 | x1.006 - x1.093 | 45% | 5% |
| DCE | x0.997 | x1.035 | x0.994 - x1.104 | 64% | 3% |
| CSE | x1.034 | x1.055 | x1.010 - x1.130 | 63% | 4% |
| LICM | x1.018 | x1.029 | x0.994 - x1.050 | 45% | 9% |
| SR | x0.983 | x0.995 | x0.975 - x1.013 | 16% | 25% |
| LU | x1.021 | x1.034 | x1.019 - x1.047 | 35% | 17% |

## 2. Pass effects are not additive

Multiplying the six single-pass speedups predicts an all-on geomean of **x1.099**; the measured all-on geomean is **x1.190**. Per program, the additive model is off by a median of 24% and by more than 10% on **680 / 900** programs. Passes enable each other (CSE and constant folding create the dead code DCE removes), so a per-pass cost model is the wrong shape. The recommender instead scores whole (program, combo) pairs.

## 3. Cost of finding a good combo

| strategy | timed runs per program | mean speedup | geomean speedup |
|---|--:|--:|--:|
| no passes | 1 | x1.000 | x1.000 |
| all 6 passes | 1 | x1.222 | x1.190 |
| ML recommender, held-out programs (RESULTS.md) | **0** | x1.21 | - |
| greedy forward search on the real clock | 16.4 | x1.280 | x1.253 |
| exhaustive search (oracle) | 64 | x1.333 | x1.305 |

Greedy search still misses the best combo by >2% on 486 / 900 programs, and **25% of all non-empty configurations are >2% slower than doing nothing**. Picking blindly is risky, and that is why the recommender is allowed to abstain.

## 4. Measurement noise

Median-of-15 / min-of-15 run time: median ratio **1.102**, 95th percentile **1.411**. The sweep runs 8 programs in parallel, so the median carries 10-40% interference. The harness therefore records the *minimum* (least-interfered) sample after 4 warm-ups, and only after the binary's exit code matches the unoptimized build.
