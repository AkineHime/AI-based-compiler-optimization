# Model comparison — which model recommends the best passes

All 8 models predict `speedup_ratio` for a (program, pass-combo) pair and are scored **identically**: one shared 5-fold split over 900 programs, ranked on the true speedup of the combo each model recommends, with the same abstain-margin sweep the production recommender uses.

- Tabular models see the 27 static features + 6 pass bits.
- Sequence models (CNN, GRU) see the tokenised combo-0 TAC + 6 pass bits.
- Hybrids see both.

## Results

| # | model | input | reco speedup | oracle capture | regressions | speedup MAE | size | train | infer |
|--:|---|---|--:|--:|--:|--:|--:|--:|--:|
| 1 | **HistGradient Boosting** | features | **x1.209** | 63% | 10% | 0.105 | 2.0 MB | 1.6s | 0.36 ms |
| 2 | **Random Forest** | features | **x1.206** | 62% | 10% | 0.107 | 612.9 MB | 5.7s | 2.43 ms |
| 3 | **1D-CNN** | TAC sequence | **x1.197** | 59% | 8% | 0.131 | 365 KB | 43.4s | 0.35 ms |
| 4 | **Linear (Ridge)** | features | **x1.186** | 56% | 5% | 0.136 | 2 KB | 0.0s | 0.02 ms |
| 5 | **1D-CNN + features** | both | **x1.064** | 19% | 4% | 1.179 | 434 KB | 13.0s | 0.31 ms |
| 6 | **GRU + features** | both | **x1.058** | 18% | 7% | 0.779 | 162 KB | 56.9s | 0.98 ms |
| 7 | **GRU (RNN)** | TAC sequence | **x1.035** | 11% | 2% | 0.147 | 94 KB | 134.1s | 0.33 ms |
| 8 | **MLP** | features | **x1.024** | 7% | 10% | 0.703 | 92 KB | 0.7s | 0.03 ms |

*reco speedup* = held-out true speedup of the recommended combo (at each model's best abstain margin). *capture* = fraction of the oracle-best gain recovered. *infer* = ms to score all 64 combos for one program.

**Winner: HistGradient Boosting** — reco x1.209, 63% capture, 10% regressions, abstain margin x1.05.

## Recommendation speedup by program type

| model | branch | cf | composite | cse | div | licm | loops | nested | neutral | numeric | recur | recursion | sr | strings | struct | structs | unroll |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| HistGradient Boosting | x1.07 | x1.33 | x1.16 | x1.51 | x1.74 | x1.30 | x1.76 | x1.73 | x0.99 | x1.24 | x0.98 | x1.00 | x1.05 | x1.26 | x1.06 | x2.95 | x1.04 |
| Random Forest | x1.05 | x1.33 | x1.15 | x1.48 | x1.73 | x1.32 | x1.72 | x1.74 | x0.99 | x1.25 | x0.92 | x1.04 | x1.06 | x1.29 | x1.08 | x2.86 | x1.04 |
| 1D-CNN | x1.05 | x1.32 | x1.16 | x1.48 | x1.71 | x1.32 | x1.79 | x1.68 | x0.99 | x1.27 | x0.98 | x1.05 | x1.01 | x1.35 | x1.07 | x2.80 | x1.01 |
| Linear (Ridge) | x1.06 | x1.31 | x1.16 | x1.48 | x1.70 | x1.30 | x1.78 | x1.68 | x0.99 | x1.27 | x0.95 | x1.05 | x0.99 | x1.35 | x1.07 | x2.80 | x1.01 |
| 1D-CNN + features | x1.07 | x1.34 | x1.16 | x1.52 | x1.75 | x1.31 | x1.48 | x1.60 | x0.99 | x1.23 | x1.01 | x1.05 | x1.05 | x1.26 | x1.09 | x2.15 | x1.02 |
| GRU + features | x1.07 | x1.23 | x1.12 | x1.35 | x1.59 | x1.22 | x1.63 | x1.59 | x0.99 | x1.18 | x0.97 | x1.02 | x1.00 | x1.31 | x1.04 | x2.67 | x1.00 |
| GRU (RNN) | x1.07 | x1.34 | x1.17 | x1.50 | x1.76 | x1.31 | x1.77 | x1.70 | x0.99 | x1.27 | x1.03 | x1.07 | x1.06 | x1.29 | x1.07 | x2.96 | x1.02 |
| MLP | x1.07 | x1.17 | x1.08 | x1.15 | x1.59 | x1.18 | x1.27 | x1.49 | x1.00 | x1.18 | x1.03 | x1.04 | x0.98 | x1.17 | x1.02 | x1.64 | x1.01 |

`branch`: 31  `cf`: 32  `composite`: 522  `cse`: 32  `div`: 32  `licm`: 32  `loops`: 15  `nested`: 31  `neutral`: 31  `numeric`: 6  `recur`: 31  `recursion`: 3  `sr`: 32  `strings`: 2  `struct`: 32  `structs`: 4  `unroll`: 32  (held-out program counts)

## Method notes

- Same GroupKFold-by-program split for every model — a program's 64 rows share features, so a random row split would leak.
- Sequence models are trained program-batched (one encode per program, all 64 combos scored together); on CPU the row-batched version is ~50x slower.
- The GRU is a compact 1-layer model capped at 320 tokens — a bidirectional / multi-layer RNN on 640-token programs needs a GPU.
- All models use identical inputs otherwise and the identical abstain-margin recommendation rule.