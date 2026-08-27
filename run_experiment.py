"""End-to-end Person C pipeline:  sweep -> dataset -> train (GroupKFold) -> RESULTS.md

    python run_experiment.py                 # full 64-combo sweep, then train + report
    python run_experiment.py --quick         # combos {0,CF,DCE,CSE,LICM,SR,LU,all} only
    python run_experiment.py --skip-sweep    # reuse data/benchmark_dataset.csv
"""
import argparse
import os
import sys
import time

from src.minic.harness.sweeper import sweep
from src.minic.harness.report import render_markdown
from src.minic.ml.train import bakeoff, cross_validate, train_final

DATASET = "data/benchmark_dataset.csv"
MODEL = "data/trained_model.pkl"
RESULTS = "RESULTS.md"

QUICK_COMBOS = [0, 1, 2, 4, 8, 16, 32, 63]


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("--quick", action="store_true", help="sweep only 7 key combos")
    p.add_argument("--skip-sweep", action="store_true", help="reuse the existing dataset CSV")
    p.add_argument("--runs", type=int, default=15)
    p.add_argument("--workers", type=int, default=None)
    p.add_argument("--warmup", type=int, default=4)
    p.add_argument("--bench-root", default="benchmarks")
    args = p.parse_args(argv)

    t0 = time.time()
    if not args.skip_sweep:
        combos = QUICK_COMBOS if args.quick else None
        sweep(args.bench_root, DATASET, runs=args.runs, warmup=args.warmup,
              combos=combos, workers=args.workers)
    else:
        print(f"reusing {DATASET}")

    print("\n" + "=" * 70)
    print("GroupKFold CV bake-off (grouped by program_id):")
    print(f"  {'model':24s} {'MAE':>7} {'reco':>7} {'oracle':>7} {'capture':>8} {'regress%':>9}")
    rows = bakeoff(DATASET, n_splits=5)
    for r in rows:
        print(f"  {r['kind']:24s} {r['cv_mae']:7.3f} x{r['reco_speedup_mean']:5.2f} "
              f"x{r['oracle_speedup_mean']:5.2f} {100*r['capture']:7.0f}% "
              f"{100*r['regression_rate']:8.0f}%")
    cv = rows[0]
    print(f"\n  winner: {cv['kind']}  ({cv['held_out_programs']} held-out programs, "
          f"{cv['n_splits']} folds)")

    m = train_final(DATASET, MODEL, cv["kind"])
    print(f"  final model -> {MODEL}  ({m.metadata['n_rows']} rows, {cv['kind']})")

    md = render_markdown(DATASET, cv)
    with open(RESULTS, "w", encoding="utf-8") as fh:
        fh.write(md)
    print(f"\nwrote {RESULTS}  ({time.time() - t0:.0f}s total)")
    print("\n" + md)


if __name__ == "__main__":
    main()
