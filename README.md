# AI-Based Compiler Optimization for MiniC

A source-level optimizer for **MiniC** (a small, pointer-free, dynamic-memory-free
C dialect) plus a machine-learning model that, given a program it has never run,
**recommends which optimization passes to turn on**.

Every claim is measured, not modelled: each program is emitted to C at all 64 pass
combinations, compiled with `gcc -O0`, and timed on real binaries.

## Result

On 270 benchmarks (30 hand-written + ~240 parametric), each swept over all 64 pass
combinations = **17,280 timed configurations**:

| | |
|---|---|
| Best pass combo per program, geomean speedup | **×1.50** (max ×4.57) |
| Turning all 6 passes on | ×1.21 — and *not* the per-program best on 243 / 270 |
| No fixed non-empty combo is safe | every one regresses >3% on at least one program |
| Recommender (HistGBT + abstain margin), held-out true speedup | **×1.23** vs ×1.54 oracle — 44% of the achievable gain |
| Recommendations that regress the program | **9%** (down from 21% for naive argmax) |

The C compiler is pinned at `-O0` on purpose: the measured delta is what *our*
optimizer contributed, not what `gcc` would have done anyway. `gcc -O2` is shown
only as a reference point.

Full numbers: [`RESULTS.md`](RESULTS.md) · visual report: [`docs/results.html`](docs/results.html).

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
python run_experiment.py                 # ~75 min full sweep
python run_experiment.py --skip-sweep    # ~2 min: re-bake / retrain from the CSV
```

Requirements: Python 3.9+ for the compiler itself; `numpy` / `scikit-learn` /
`pandas` (and `flask` for the demo) for the ML pipeline. `gcc` on `PATH`.

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
  generated/          ~240 parametric programs (gitignored; regenerate with --seed 7)
tests/                pytest — front end, IR, every pass × 64 combos, harness, ML
data/                 benchmark_dataset.csv (tracked); trained_model.pkl (gitignored)
run_experiment.py     one command: sweep → dataset → bake-off → train → RESULTS.md
RESULTS.md            current measured results
docs/
  results.html        the visual results report
  spec/               MiniC language specification
  planning/           original design plan, workflow, prompt log
  team/               per-person notes, contribution map, continuation guide
```

## Testing

```bash
python -m pytest -q
```

Correctness gate: **every one of the 64 pass combinations, for every benchmark,
must reproduce the unoptimized binary's exit code** before its timing is recorded
— a miscompiled combo contributes no data. The suite runs the front end, IR, each
pass individually and in 64-combo sweeps, the harness, and the ML dataset plumbing.

## Team

Four roles — front end / IR / features (A), optimization passes + codegen (B),
timing harness + ML + demo (C), benchmark corpus (D). See
[`docs/team/CONTRIBUTIONS.md`](docs/team/CONTRIBUTIONS.md) for the area→owner map
and [`docs/team/TEAM_CONTINUATION_GUIDE.md`](docs/team/TEAM_CONTINUATION_GUIDE.md)
to pick up the work.
