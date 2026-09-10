"""End-to-end Person C pipeline:  sweep -> dataset -> train (GroupKFold) -> RESULTS.md

    python run_experiment.py                 # full 64-combo sweep, then train + report
    python run_experiment.py --quick         # combos {0,CF,DCE,CSE,LICM,SR,LU,all} only
    python run_experiment.py --skip-sweep    # reuse data/benchmark_dataset.csv
    python run_experiment.py --skip-sweep --compare-models   # + the 8-model bake-off
"""
import argparse
import os
import sys
import time

from src.minic.harness.sweeper import sweep
from src.minic.harness.report import render_markdown
from src.minic.ml.train import choose_strategy, train_final

DATASET = "data/benchmark_dataset.csv"
SEQUENCES = "data/tac_sequences.npz"
MODEL = "data/trained_model.pkl"
RESULTS = "RESULTS.md"
MODEL_COMPARISON = "MODEL_COMPARISON.md"

QUICK_COMBOS = [0, 1, 2, 4, 8, 16, 32, 63]


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("--quick", action="store_true", help="sweep only 7 key combos")
    p.add_argument("--skip-sweep", action="store_true", help="reuse the existing dataset CSV")
    p.add_argument("--compare-models", action="store_true",
                   help="also run the 8-model bake-off -> MODEL_COMPARISON.md")
    p.add_argument("--seeds", type=int, default=1, help="seeds for the neural models")
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
        # keep the TAC sequences in sync with the freshly-swept corpus
        from src.minic.ml.sequences import export_sequences
        export_sequences(args.bench_root, SEQUENCES)
    else:
        print(f"reusing {DATASET}")

    print("\n" + "=" * 70)
    print("Strategy bake-off (GroupKFold / KFold by program_id):")
    win = choose_strategy(DATASET, n_splits=5)
    print(f"  {'strategy':14s} {'model':22s} {'reco':>6} {'oracle':>7} "
          f"{'capture':>8} {'regress%':>9}")
    for t in sorted(win["table"], key=lambda t: (t["regression_rate"], -t["capture"])):
        print(f"  {t['strategy']:14s} {t['kind']:22s} x{t['reco_speedup_mean']:4.2f} "
              f"x{t['oracle_speedup_mean']:5.2f} {100*t['capture']:7.0f}% "
              f"{100*t['regression_rate']:8.0f}%")
    print(f"\n  winner: {win['strategy']} / {win['kind']}  "
          f"({win['held_out_programs']} held-out programs, {win['n_splits']} folds)")

    strat = ("per_pass" if win["strategy"] == "per_pass"
             else "margin" if win["margin"] else "argmax")
    kind = win["reg_kind"]
    m = train_final(DATASET, MODEL, kind=kind, strategy=strat, margin=win["margin"])
    print(f"  final model -> {MODEL}  ({m.metadata['n_rows']} rows, {kind} / {strat})")

    cv = {"kind": kind, "strategy": win["strategy"],
          "held_out_programs": win["held_out_programs"], "n_groups": win["n_groups"],
          "n_splits": win["n_splits"], "cv_mae": win.get("cv_mae", float("nan")),
          "reco_speedup_mean": win["reco_speedup_mean"],
          "oracle_speedup_mean": win["oracle_speedup_mean"],
          "baseline_mean": win["baseline_mean"], "capture": win["capture"],
          "regression_rate": win["regression_rate"]}
    md = render_markdown(DATASET, cv)
    with open(RESULTS, "w", encoding="utf-8") as fh:
        fh.write(md)
    print(f"\nwrote {RESULTS}  ({time.time() - t0:.0f}s total)")
    print("\n" + md)

    if args.compare_models:
        print("\n" + "=" * 70)
        print("Model bake-off: Linear / RF / HGBT / MLP / CNN1D / GRU (+ hybrids)")
        from src.minic.ml.models_compare import run_full_comparison
        res = run_full_comparison(DATASET, SEQUENCES, MODEL_COMPARISON,
                                  n_splits=5, seeds=args.seeds)
        w = res["winner"]
        print(f"\n  model winner: {w['model']}  reco x{w['reco']:.3f}  "
              f"{100*w['cap']:.0f}% capture  {100*w['regress']:.0f}% regress")
        print(f"  wrote {MODEL_COMPARISON}  ({time.time() - t0:.0f}s total)")


if __name__ == "__main__":
    main()
