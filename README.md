# AI-Based Compiler Optimization for MiniC

Which optimization passes should a compiler run on *this* program? This project
answers it on the clock instead of with a hand-tuned cost model. It contains a
complete compiler for **MiniC** (a pointer-free C dialect), six toggleable
optimization passes, a parallel timing harness, and a model that predicts the
speedup of any pass combination **without running the program**.

**57,600 measured configurations**: 900 programs x all 64 pass combinations, each
emitted to C, compiled with `gcc -O0`, checked for correctness, and timed on real
binaries. `gcc` is pinned at `-O0` so every measured gain comes from *our* passes.

## Key findings

| | |
|---|---|
| Best combo per program (oracle) | **x1.31** geomean, up to **x4.37** |
| Gap left by "turn every pass on" | all-on is >2% short of the per-program best on **715 / 900** programs, and **2.3x slower** than no optimization on the worst one |
| Pass effects are **not additive** | the product of single-pass speedups predicts x1.10 all-on; measured is x1.19. It is >10% off on **680 / 900** programs |
| A pass that usually hurts | strength reduction slows down **25%** of programs at `-O0` and helps only 16% |
| Blind search is costly and unsafe | **25%** of all configurations are slower than doing nothing; greedy search needs **16.4 timed runs** per program to reach x1.25 |
| Learned model (zero runs, held-out programs) | **x1.21** mean speedup with **9%** regressions. All-on gives x1.22 with 12.4% regressions |
| Measurement noise under parallel load | median/min run time is 1.10 (p95 **1.41**), so the harness records the least-interfered of 15 runs |

**Honest result:** the learned model *matches* the "all passes on" heuristic in
average speedup and cuts regressions by about a quarter (12.4% to 9%). It does
**not yet beat it**. Neither does any fallback variant tried: abstaining to
all-on instead of no-passes peaks at x1.223. The remaining gap to the oracle
(x1.33 mean) is the open problem. Static features miss the pass interactions
that dominate the measured speedups (see finding 3).

Write-ups:
[`PERF_ANALYSIS.md`](PERF_ANALYSIS.md): per-pass marginal effects, non-additivity, search cost, noise ·
[`RESULTS.md`](RESULTS.md): per-program and per-category speedups ·
[`MODEL_COMPARISON.md`](MODEL_COMPARISON.md): 8-model bake-off (Ridge / RF / HistGBT / MLP / 1D-CNN / GRU / hybrids) ·
[`docs/results.html`](docs/results.html): visual report ·
[`docs/WALKTHROUGH.md`](docs/WALKTHROUGH.md): one program traced through every stage

## Quickstart

```bash
pip install -r requirements.txt

# compile a MiniC program: AST / TAC / features / optimized C / run it
python -m src.minic.driver canonical_example.mc --tac --features
python -m src.minic.driver canonical_example.mc --optimize 63 --emit-c --run

# ask the model which passes to use, then prove it on the clock
python -m demo.cli recommend benchmarks/loops/licm_arith.mc --verify

# browser playground: editor -> compile two ways -> speedup + optimization report
python -m demo.app            # http://127.0.0.1:5005

# run the whole experiment (sweep -> dataset -> model bake-off -> RESULTS.md)
python run_experiment.py                 # ~3.5 h full sweep (900 programs, 8 workers)
python run_experiment.py --skip-sweep    # ~3 min: re-bake / retrain from the CSV
python run_experiment.py --skip-sweep --compare-models   # + 8-model bake-off -> MODEL_COMPARISON.md (~25 min)
python -m src.minic.harness.perf_analysis                 # ~5 s: PERF_ANALYSIS.md from the CSV
```

Requirements: Python 3.9+ for the compiler itself; `numpy` / `scikit-learn` /
`pandas` (and `flask` for the demo) for the ML pipeline. `gcc` on `PATH`.

## Methodology

- **Correctness gate:** every one of the 64 combos must reproduce the
  unoptimized binary's exit code before its timing is recorded, so a miscompile
  contributes no data.
- **Timing:** 4 warm-up runs, then the minimum of 15 wall-clock runs, with 8
  programs swept in parallel. The minimum is the least-interfered sample. The
  median is 10-40% noisier under this load.
- **`gcc -O0`:** the backend adds nothing, so a speedup is attributable to the
  MiniC passes alone. `gcc -O2` appears only as a reference point.
- **No leakage:** cross-validation uses GroupKFold by program. All 64 rows of a
  program share its static features, so a random split would leak.
- **Metrics:** speedup = `time(no passes) / time(combo)`. "Regression" means
  >2% slower than no passes. Means are arithmetic unless marked geomean, and
  comparisons always use the same kind.

## Pipeline

```
MiniC .mc
  │  lexer → parser → AST → semantic analysis            src/minic/frontend/
  ▼
Three-address code (TAC)                                 src/minic/ir/
  │  + 27 static features (19 structural + 8 "opportunity")   src/minic/features/
  ▼
6 toggleable optimization passes, 64 combos              src/minic/optimizer/
  │  CF · DCE · CSE · LICM · SR · loop unrolling
  │  canonical order CF→CSE→LU→LICM→SR→DCE, iterated to a fixed point
  ▼
value-semantics C  (arrays/structs/strings → one-field wrapper structs)   src/minic/codegen/
  │  gcc -O0 → timed (least of 15 runs, parallel sweep)  src/minic/harness/
  ▼
dataset  →  GroupKFold model bake-off  →  recommender    src/minic/ml/
```

MiniC has no pointers and no dynamic memory, so there is **no aliasing** — which
is what makes the passes provably sound and the whole approach tractable.

### The recommender

`src/minic/ml/train.py::choose_strategy` cross-validates the *selection strategy*
itself, not just the regressor: it compares plain argmax-over-predicted-speedup,
an abstain-margin sweep (fall back to "no passes" unless the predicted gain clears
a threshold), and per-pass classifiers — and picks the most useful one whose
held-out regression rate stays under 10%. The winning model carries its strategy
in its metadata; `demo/` surfaces when it abstains.

## Repository layout

```
src/minic/            the compiler + harness + ML
  frontend/  ir/  features/  optimizer/  codegen/  harness/  ml/
  driver.py           CLI: python -m src.minic.driver <file.mc> [--tac --optimize N --run ...]
demo/
  app.py              Flask browser playground (port 5005)
  cli.py              minic-opt recommend | benchmark
benchmarks/           30 hand-written programs (5 categories) + ground_truth.csv
  generated/          870 parametric programs (committed; _manifest.csv maps each to its pattern)
tests/                pytest — front end, IR, every pass × 64 combos, harness, ML
data/                 benchmark_dataset.csv (tracked); trained_model.pkl (gitignored)
run_experiment.py     one command: sweep → dataset → bake-off → train → RESULTS.md
RESULTS.md            current measured results
PERF_ANALYSIS.md      pass interactions, search cost, measurement noise
MODEL_COMPARISON.md   8-model bake-off (tabular / sequence / hybrid)
reports/              course reports (Review 1 / Final) + their generators
docs/
  results.html        the visual results report
  WALKTHROUGH.md      one program traced through every stage (lexer → … → ML)
  spec/               MiniC language specification
  planning/           original design plan, workflow, prompt log
  team/               per-person notes, contribution map, continuation guide
```

## Testing

```bash
python -m pytest -q
```

The suite runs the front end, IR, each
pass individually and in 64-combo sweeps, the harness, and the ML dataset plumbing.

## Team

Four roles — front end / IR / features (A), optimization passes + codegen (B),
timing harness + ML + demo (C), benchmark corpus (D). See
[`docs/team/CONTRIBUTIONS.md`](docs/team/CONTRIBUTIONS.md) for the area→owner map
and [`docs/team/TEAM_CONTINUATION_GUIDE.md`](docs/team/TEAM_CONTINUATION_GUIDE.md)
to pick up the work.
