"""End-to-end Person C pipeline:  sweep -> dataset -> train (GroupKFold) -> RESULTS.md

    python run_experiment.py                 # full 32-combo sweep, then train + report
    python run_experiment.py --quick         # combos {0,CF,DCE,CSE,LICM,SR,all} only
    python run_experiment.py --skip-sweep    # reuse data/benchmark_dataset.csv
"""
import argparse
import os
import sys
import time

from src.minic.harness.sweeper import sweep
from src.minic.harness.report import render_markdown
from src.minic.ml.train import cross_validate, train_final

DATASET = "data/benchmark_dataset.csv"
MODEL = "data/trained_model.pkl"
RESULTS = "RESULTS.md"

QUICK_COMBOS = [0, 1, 2, 4, 8, 16, 31]


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("--quick", action="store_true", help="sweep only 7 key combos")
    p.add_argument("--skip-sweep", action="store_true", help="reuse the existing dataset CSV")
    p.add_argument("--runs", type=int, default=8)
    p.add_argument("--warmup", type=int, default=2)
    p.add_argument("--bench-root", default="benchmarks")
    args = p.parse_args(argv)

    t0 = time.time()
    if not args.skip_sweep:
        combos = QUICK_COMBOS if args.quick else None
        sweep(args.bench_root, DATASET, runs=args.runs, warmup=args.warmup, combos=combos)
    else:
        print(f"reusing {DATASET}")

    print("\n" + "=" * 70)
    cv = cross_validate(DATASET, n_splits=5)
    print("GroupKFold CV (grouped by program_id):")
    print(f"  {cv['held_out_programs']} held-out programs over {cv['n_splits']} folds")
    print(f"  speedup-prediction MAE : {cv['cv_mae']:.4f}")
    print(f"  baseline (combo 0)     : x{cv['baseline_mean']:.3f}")
    print(f"  ML-recommended combo   : x{cv['reco_speedup_mean']:.3f}")
    print(f"  oracle (best in hindsight): x{cv['oracle_speedup_mean']:.3f}")

    m = train_final(DATASET, MODEL)
    print(f"  final model -> {MODEL}  ({m.metadata['n_rows']} rows)")

    md = render_markdown(DATASET, cv)
    with open(RESULTS, "w", encoding="utf-8") as fh:
        fh.write(md)
    print(f"\nwrote {RESULTS}  ({time.time() - t0:.0f}s total)")
    print("\n" + md)


if __name__ == "__main__":
    main()
