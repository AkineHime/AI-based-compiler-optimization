# Changelog

## Unreleased

### Optimizer
- **Loop unrolling** added as pass 6 (factor 4, remainder loop); 6 passes -> 64 combos.
- Pass manager now iterates the canonical sequence (CF -> CSE -> LU -> LICM -> SR -> DCE)
  to a fixed point.
- Constant folding: whole-function propagation of single-assignment literal locals;
  32-bit C integer semantics; multiply-defined temps no longer propagated across blocks.
- CSE: local copy propagation (scalar temps + scalar vars).
- LICM & SR: build a real labelled pre-header and redirect the loop's entry edges
  when the header is not reached by fall-through (e.g. after unrolling).
- Fixed: SR now requires its induction variable to be written exactly once;
  SR accumulator is a named var, not a temp.
- Codegen: struct/wrapper typedefs emitted in dependency order; globals no longer
  shadowed by per-function local declarations.

### Front end / IR
- Nested aggregate l-values (`a[i].f = v`, `s.g.h = v`) lower to a
  load / mutate-copy / store-back chain; array-element and struct-field load
  temps are typed from the real element/field type.
- `variable_count` feature split into `named_variable_count` + `temp_variable_count`
  (feature vector 18 -> 19).
- Python 3.13 import fixes (`Any` in `lexer.py`, `Tuple` in `ir/tac.py`).

### Person C -- harness, ML, demo
- `src/minic/harness/`: `gcc -O0` / `-O2` compiler wrapper, median+min timer,
  parallel across-programs sweeper, results report + chart, ground-truth oracle.
- `src/minic/harness/gen_corpus.py`: parametric benchmark generator
  (single-pattern parameter sweeps + weighted composites).
- `src/minic/features/opportunity.py`: 8 "what would each pass do" features
  (feature vector 19 -> 27 for ML).
- `src/minic/ml/`: RandomForest / ExtraTrees / HistGradientBoosting, GroupKFold
  bake-off scored on recommendation quality, predictor.
- ML recommender is now **risk-aware**: a cross-validated strategy bake-off
  (plain argmax vs. abstain-margin sweep vs. per-pass classifiers) picks the
  most useful recommender that keeps regressions <=10%. Winner on the 270-program
  corpus: HGBT + abstain margin x1.12 -> recommendation regressions 21% -> 9%,
  capture 44%. Model artifact carries `strategy` / `margin`; the demo surfaces
  when it abstains.
- `demo/cli.py` (`recommend` / `benchmark`) and `demo/app.py` + `static/`
  (browser playground: editor -> compile both ways -> speedup + optimization
  report + TAC diff + `gcc -O2` reference).
- `run_experiment.py`: one command -> sweep -> bake-off -> train -> `RESULTS.md`.
- Correctness: every combo of every benchmark verified to reproduce the
  unoptimized exit code before its time is recorded.
- Measured result: 270 programs x 64 combos = 17,280 timed configs; best combo
  per program geomean **x1.50** (max x4.57); recommender x1.23 held-out, 9% regress.
- `demo`: default example now shows a real speedup (was the tiny canonical fixture
  timing at x0.99 noise); honest `gcc -O2` comparison when we already beat `-O2`.

### Repository housekeeping
- Docs moved under `docs/`: `spec/` (language spec), `planning/` (original design
  plan, workflow, prompt log), `team/` (per-person notes, contribution map,
  continuation guide). `README.md`, `CHANGELOG.md`, `RESULTS.md` stay at root.
- Real `README.md` (was a one-line stub).
- Spec/planning PDFs untracked (`*.pdf` gitignored); the `.md` alongside is the
  source of truth. Stray `test.mc` untracked (docs tell you to create your own).
- `tests/test_optimizer.py`, `tests/test_codegen.py`, `src/minic/driver.py` build
  into a `tempfile` dir instead of the repo root -- no more `temp_*.exe` litter.
- `driver --features` now prints all 27 features (was 19 structural only).
