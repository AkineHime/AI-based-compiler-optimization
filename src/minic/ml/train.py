"""Train the speedup recommender with GroupKFold(program_id) cross-validation.

A program's 64 rows share identical static features, so a random split leaks;
GroupKFold holds *whole programs* out.  What we actually care about is not the
regression MAE but the **recommendation quality**: for a held-out program, does
argmax over the 64 predicted speedups land on a genuinely fast combo?
"""
import argparse
import statistics
from typing import Dict, List

import numpy as np
from sklearn.model_selection import GroupKFold

from .dataset import load_dataset
from .model import SpeedupModel, make_regressor, REGRESSORS


def _score_recommendations(reg, X, y, groups, combos, test_idx):
    reco, oracle, base = [], [], []
    for g in sorted(set(groups[test_idx])):
        idx = np.where(groups == g)[0]
        true_by = {int(combos[i]): float(y[i]) for i in idx}
        pred = reg.predict(X[idx])
        pred_by = {int(combos[i]): float(p) for i, p in zip(idx, pred)}
        pick = max(pred_by, key=pred_by.get)
        reco.append(true_by.get(pick, 1.0))
        oracle.append(max(true_by.values()))
        base.append(true_by.get(0, 1.0))
    return reco, oracle, base


def cross_validate(csv_path: str, kind: str = "random_forest",
                   n_splits: int = 5, random_state: int = 0) -> dict:
    ds = load_dataset(csv_path)
    n_groups = len(set(ds.groups))
    n_splits = min(n_splits, n_groups)
    X = np.asarray(ds.X, float)
    y = np.asarray(ds.y, float)
    groups = np.asarray(ds.groups)
    combos = np.asarray(ds.combo_ids)

    gkf = GroupKFold(n_splits=n_splits)
    maes, reco, oracle, base, regret_pos = [], [], [], [], []
    for tr, te in gkf.split(X, y, groups):
        reg = make_regressor(kind, random_state)
        reg.fit(X[tr], y[tr])
        maes.append(float(np.mean(np.abs(reg.predict(X[te]) - y[te]))))
        r, o, b = _score_recommendations(reg, X, y, groups, combos, te)
        reco += r
        oracle += o
        base += b
        regret_pos += [1 if rr < 0.98 else 0 for rr in r]

    gap = statistics.mean(oracle) - statistics.mean(base)
    got = statistics.mean(reco) - statistics.mean(base)
    return {
        "kind": kind, "n_splits": n_splits, "n_groups": n_groups,
        "held_out_programs": len(reco),
        "cv_mae": statistics.mean(maes),
        "baseline_mean": statistics.mean(base),
        "reco_speedup_mean": statistics.mean(reco),
        "oracle_speedup_mean": statistics.mean(oracle),
        "capture": (got / gap) if gap > 1e-9 else 1.0,
        "regression_rate": statistics.mean(regret_pos),
    }


def bakeoff(csv_path: str, n_splits: int = 5) -> List[dict]:
    results = [cross_validate(csv_path, k, n_splits) for k in REGRESSORS]
    results.sort(key=lambda r: (-r["reco_speedup_mean"], r["regression_rate"]))
    return results


def train_final(csv_path: str, model_path: str, kind: str = "random_forest",
                random_state: int = 0) -> SpeedupModel:
    ds = load_dataset(csv_path)
    reg = make_regressor(kind, random_state)
    reg.fit(np.asarray(ds.X, float), np.asarray(ds.y, float))
    imp = {}
    if hasattr(reg, "feature_importances_"):
        imp = dict(sorted(zip(ds.feature_names, (float(v) for v in reg.feature_importances_)),
                          key=lambda kv: -kv[1]))
    model = SpeedupModel(regressor=reg, feature_names=ds.feature_names,
                         metadata={"n_rows": len(ds), "kind": kind,
                                   "top_features": list(imp)[:8]})
    model.save(model_path)
    return model


def main(argv=None):
    p = argparse.ArgumentParser(description="Train / bake off the MiniC speedup recommender")
    p.add_argument("--csv", default="data/benchmark_dataset.csv")
    p.add_argument("--model-out", default="data/trained_model.pkl")
    p.add_argument("--splits", type=int, default=5)
    p.add_argument("--kind", default="", help="force a regressor; default = bake-off winner")
    args = p.parse_args(argv)

    if args.kind:
        rows = [cross_validate(args.csv, args.kind, args.splits)]
    else:
        rows = bakeoff(args.csv, args.splits)
    best = rows[0]

    print("=== GroupKFold CV (grouped by program_id) ===")
    print(f"{'model':24s} {'MAE':>7} {'reco':>7} {'oracle':>7} {'capture':>8} {'regress%':>9}")
    for r in rows:
        print(f"{r['kind']:24s} {r['cv_mae']:7.3f} x{r['reco_speedup_mean']:5.2f} "
              f"x{r['oracle_speedup_mean']:5.2f} {100*r['capture']:7.0f}% "
              f"{100*r['regression_rate']:8.0f}%")
    print(f"\nheld-out programs: {best['held_out_programs']}  "
          f"({best['n_groups']} programs, {best['n_splits']} folds)")

    m = train_final(args.csv, args.model_out, best["kind"])
    print(f"\ntrained {best['kind']} on {m.metadata['n_rows']} rows -> {args.model_out}")
    if m.metadata["top_features"]:
        print("top features:", ", ".join(m.metadata["top_features"]))
    return best


if __name__ == "__main__":
    main()
