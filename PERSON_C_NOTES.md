# Person C — Timing Harness, 64-combo Sweep, ML Recommendation, CLI

## Layout

```
benchmarks/                 18 MiniC programs, 5 categories, high trip counts
  loops/ numeric/ structs/ recursion/ strings/
src/minic/harness/
  compiler.py               gcc -O0 wrapper -> runnable binary
  timer.py                  measure_execution_time(): N runs, drop warmups, median ms
  sweeper.py                per (program x 64 combos): features + median time + speedup vs combo 0
  report.py                 dataset CSV -> RESULTS.md (geomean / best / per-program table)
src/minic/ml/
  dataset.py                CSV -> X (19 features + 5 flag bits), y (speedup), groups (program_id)
  model.py                  RandomForestRegressor wrapper + pickle persistence
  train.py                  GroupKFold(program_id) CV + final fit
  predictor.py              recommend_combo(features, model) -> best combo 0..63
demo/cli.py                 `recommend` (features + ML pick) and `benchmark` (time across combos)
run_experiment.py           sweep -> dataset -> train -> RESULTS.md, one command
data/
  benchmark_dataset.csv     the sweep output
  trained_model.pkl         the fitted model
```

## What "speedup" means here

Every program is emitted as C at each of the 64 optimization combos, compiled
with **`gcc -O0`**, and timed. `speedup_ratio = time(combo 0) / time(combo)`.
The C compiler is pinned at `-O0` on purpose: the experiment measures what the
MiniC TAC optimizer itself contributes, not what gcc would do anyway. `combo 0`
(no passes) is the baseline; `> 1.0` means our optimizer made the binary faster.

## Run it

```bash
pip install -r requirements.txt
python run_experiment.py            # ~20-30 min: full 64-combo sweep + train + report
python run_experiment.py --quick    # ~4 min: 7 key combos, smaller dataset
python -m demo.cli recommend benchmarks/loops/licm_arith.mc --verify
python -m demo.cli benchmark benchmarks/structs/distance_accum.mc
```

## GroupKFold — why it matters

A program's 64 rows share the same 19 static features, differing only in the 5
flag bits and the timing. A random train/test split would put near-identical
rows on both sides and massively overstate accuracy. `GroupKFold(program_id)`
holds *whole programs* out, so the CV number answers the real question: "given a
MiniC program we have never timed, how good is the combo we recommend?"

## Dataset schema

`program_id, category, f_<19 features>, combo_id, flag_cf, flag_dce, flag_cse,
flag_licm, flag_sr, exit_code, median_time_ms, speedup_ratio`

The 19 features are `FEATURE_NAMES` from `src/minic/features/extractor.py`
(`variable_count` was split into `named_variable_count` + `temp_variable_count`).

## Notes / limits

- Timing is wall-clock via `time.perf_counter_ns()` around `subprocess.run`;
  on a noisy machine widen `--runs`. Programs are sized so `gcc -O0` combo 0 is
  ~50-200 ms, comfortably above scheduler noise.
- The corpus is a Person C bootstrap so the pipeline runs end to end; Person D's
  fuller 30-40 program corpus drops into `benchmarks/` with no code change
  (the sweeper globs `benchmarks/**/*.mc`).
- Streamlit demo not built (CLI only, by request).
