"""Train the speedup-regression model with GroupKFold(program_id) CV.

Random splits would leak: a program's 64 rows share the same 19 static features,
so a plain split puts near-duplicates on both sides.  GroupKFold holds whole
programs out, which is the only honest estimate of "predict for a program we
have never timed".
"""
import argparse
import statistics
from typing import Optional

import numpy as np
from sklearn.model_selection import GroupKFold

from .dataset import load_dataset
from .model import SpeedupModel, make_regressor
from ..optimizer.pass_manager import get_pass_names


def _recommend_for_program(model, feats_row_builder, combos=range(64)):
    best_combo, best_pred = 0, -1e9
    for c in combos:
        pred = model.predict([feats_row_builder(c)])[0]
        if pred > best_pred:
            best_pred, best_combo = pred, c
    return best_combo, best_pred


def cross_validate(csv_path: str, n_splits: int = 5, random_state: int = 0):
    ds = load_dataset(csv_path)
    n_groups = len(set(ds.groups))
    n_splits = min(n_splits, n_groups)
    X = np.asarray(ds.X, float)
    y = np.asarray(ds.y, float)
    groups = np.asarray(ds.groups)
    combos = np.asarray(ds.combo_ids)

    gkf = GroupKFold(n_splits=n_splits)
    fold_mae, fold_reco_speedup, fold_oracle_speedup, fold_baseline = [], [], [], []

    for tr, te in gkf.split(X, y, groups):
        reg = make_regressor(random_state=random_state)
        reg.fit(X[tr], y[tr])
        pred = reg.predict(X[te])
        fold_mae.append(float(np.mean(np.abs(pred - y[te]))))

        for g in sorted(set(groups[te])):
            mask = groups == g
            idx = np.where(mask)[0]
            true_by_combo = {int(combos[i]): float(y[i]) for i in idx}
            pred_by_combo = {int(combos[i]): float(p)
                             for i, p in zip(idx, reg.predict(X[idx]))}
            reco = max(pred_by_combo, key=pred_by_combo.get)
            fold_reco_speedup.append(true_by_combo.get(reco, 1.0))
            fold_oracle_speedup.append(max(true_by_combo.values()))
            fold_baseline.append(true_by_combo.get(0, 1.0))

    return {
        "n_splits": n_splits,
        "n_groups": n_groups,
        "cv_mae": statistics.mean(fold_mae),
        "reco_speedup_mean": statistics.mean(fold_reco_speedup),
        "oracle_speedup_mean": statistics.mean(fold_oracle_speedup),
        "baseline_mean": statistics.mean(fold_baseline),
        "held_out_programs": len(fold_reco_speedup),
    }


def train_final(csv_path: str, model_path: str, random_state: int = 0) -> SpeedupModel:
    ds = load_dataset(csv_path)
    reg = make_regressor(random_state=random_state)
    reg.fit(np.asarray(ds.X, float), np.asarray(ds.y, float))
    importances = dict(sorted(
        zip(ds.feature_names, (float(v) for v in reg.feature_importances_)),
        key=lambda kv: -kv[1]))
    model = SpeedupModel(regressor=reg, feature_names=ds.feature_names,
                         metadata={"n_rows": len(ds), "top_features": list(importances)[:8]})
    model.save(model_path)
    return model


def main(argv=None):
    p = argparse.ArgumentParser(description="Train the MiniC speedup model (GroupKFold CV)")
    p.add_argument("--csv", default="data/benchmark_dataset.csv")
    p.add_argument("--model-out", default="data/trained_model.pkl")
    p.add_argument("--splits", type=int, default=5)
    args = p.parse_args(argv)

    cv = cross_validate(args.csv, args.splits)
    print("=== GroupKFold cross-validation (grouped by program_id) ===")
    print(f"  folds                 : {cv['n_splits']}  ({cv['n_groups']} programs)")
    print(f"  held-out programs     : {cv['held_out_programs']}")
    print(f"  speedup-prediction MAE: {cv['cv_mae']:.4f}")
    print(f"  baseline (combo 0)    : x{cv['baseline_mean']:.3f}")
    print(f"  model recommendation  : x{cv['reco_speedup_mean']:.3f}  (mean true speedup of the predicted-best combo)")
    print(f"  oracle (best possible): x{cv['oracle_speedup_mean']:.3f}")
    gap = cv["oracle_speedup_mean"] - cv["baseline_mean"]
    got = cv["reco_speedup_mean"] - cv["baseline_mean"]
    if gap > 1e-6:
        print(f"  model captures        : {100 * got / gap:.0f}% of the available speedup")

    m = train_final(args.csv, args.model_out)
    print(f"\ntrained on {m.metadata['n_rows']} rows -> {args.model_out}")
    print(f"top features: {', '.join(m.metadata['top_features'])}")


if __name__ == "__main__":
    main()
