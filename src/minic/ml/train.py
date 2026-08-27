"""Train the speedup recommender with GroupKFold(program_id) cross-validation.

A program's 64 rows share identical static features, so a random split leaks;
GroupKFold holds *whole programs* out.  What we actually care about is not the
regression MAE but the **recommendation quality**: for a held-out program, does
the strategy land on a genuinely fast combo -- and, just as important, does it
avoid picking a combo that is *slower* than not optimizing at all?

Three selection strategies are baked off:

* ``argmax``   -- pick the combo with the highest predicted speedup.
* ``margin:k`` -- same, but abstain to combo 0 (guaranteed x1.00) unless the
                  predicted best clears ``1 + k``.  Trades a little capture for
                  far fewer regressions -- a recommender should decline when unsure.
* ``per_pass`` -- 6 independent classifiers ("should pass P be on?"), trained on
                  the per-program best combo, assembled into one combo at inference.
"""
import argparse
import statistics
from typing import Dict, List

import numpy as np
from sklearn.inspection import permutation_importance
from sklearn.model_selection import GroupKFold

from .dataset import FLAG_BITS, load_dataset
from .model import SpeedupModel, make_classifier, make_regressor, REGRESSORS

MARGINS = (0.03, 0.05, 0.08, 0.12, 0.18)
N_STATIC = None  # set lazily = len(feature_names) - len(FLAG_BITS)


# --------------------------------------------------------------------------- #
#  regression-based strategies (argmax / margin)                              #
# --------------------------------------------------------------------------- #
def _per_program_predictions(reg, X, y, groups, combos, test_idx):
    """For each held-out program: {combo: true_sp}, {combo: pred_sp}."""
    out = []
    for g in sorted(set(groups[test_idx])):
        idx = np.where(groups == g)[0]
        true_by = {int(combos[i]): float(y[i]) for i in idx}
        pred = reg.predict(X[idx])
        pred_by = {int(combos[i]): float(p) for i, p in zip(idx, pred)}
        out.append((g, true_by, pred_by))
    return out


def _pick_argmax(pred_by, margin=0.0):
    pick = max(pred_by, key=pred_by.get)
    if margin and pred_by[pick] < 1.0 + margin:
        return 0
    return pick


def _score(picks_true, oracle, base):
    reco_m = statistics.mean(picks_true)
    base_m = statistics.mean(base)
    gap = statistics.mean(oracle) - base_m
    return {
        "reco_speedup_mean": reco_m,
        "baseline_mean": base_m,
        "oracle_speedup_mean": statistics.mean(oracle),
        "capture": ((reco_m - base_m) / gap) if gap > 1e-9 else 1.0,
        "regression_rate": statistics.mean(1 if r < 0.98 else 0 for r in picks_true),
    }


# --------------------------------------------------------------------------- #
#  per-pass classifier strategy                                               #
# --------------------------------------------------------------------------- #
def _per_program_table(ds):
    """One row per program: static features (no flag bits) + best-combo bit labels."""
    n_static = len(ds.feature_names) - len(FLAG_BITS)
    X = np.asarray(ds.X, float)
    y = np.asarray(ds.y, float)
    groups = np.asarray(ds.groups)
    combos = np.asarray(ds.combo_ids)

    progs, feats, best_combo = [], [], []
    for g in sorted(set(groups)):
        idx = np.where(groups == g)[0]
        feats.append(X[idx[0], :n_static])
        bc = int(combos[idx[np.argmax(y[idx])]])
        progs.append(g)
        best_combo.append(bc)
    Y = np.array([[1 if bc & b else 0 for b in FLAG_BITS] for bc in best_combo])
    return progs, np.asarray(feats, float), Y, n_static


def _pass_cv(ds, random_state=0, n_splits=5):
    from sklearn.model_selection import KFold

    progs, F, Y, n_static = _per_program_table(ds)
    X = np.asarray(ds.X, float)
    y = np.asarray(ds.y, float)
    groups = np.asarray(ds.groups)
    combos = np.asarray(ds.combo_ids)
    true_lookup = {
        g: {int(combos[i]): float(y[i]) for i in np.where(groups == g)[0]}
        for g in progs
    }

    picks_true, oracle, base = [], [], []
    kf = KFold(n_splits=min(n_splits, len(progs)), shuffle=True, random_state=random_state)
    for tr, te in kf.split(F):
        clfs = []
        for b in range(len(FLAG_BITS)):
            c = make_classifier(random_state)
            # a pass that is never / always in the best combo -> constant predict
            if len(set(Y[tr, b])) < 2:
                clfs.append(int(Y[tr, b][0]))
            else:
                c.fit(F[tr], Y[tr, b])
                clfs.append(c)
        for row, prog in zip(F[te], (progs[i] for i in te)):
            bits = 0
            for b, clf in enumerate(clfs):
                on = clf if isinstance(clf, int) else int(clf.predict([row])[0])
                if on:
                    bits |= FLAG_BITS[b]
            tb = true_lookup[prog]
            picks_true.append(tb.get(bits, 1.0))
            oracle.append(max(tb.values()))
            base.append(tb.get(0, 1.0))
    return _score(picks_true, oracle, base)


def fit_pass_classifiers(csv_path: str, random_state: int = 0):
    ds = load_dataset(csv_path)
    _progs, F, Y, n_static = _per_program_table(ds)
    clfs = []
    for b in range(len(FLAG_BITS)):
        if len(set(Y[:, b])) < 2:
            clfs.append(int(Y[0, b]))
        else:
            c = make_classifier(random_state)
            c.fit(F, Y[:, b])
            clfs.append(c)
    return clfs, n_static


# --------------------------------------------------------------------------- #
#  cross-validation entry points                                              #
# --------------------------------------------------------------------------- #
def cross_validate(csv_path: str, kind: str = "random_forest",
                   n_splits: int = 5, random_state: int = 0,
                   margins=MARGINS) -> dict:
    """Regressor CV.  Returns the plain-argmax scores plus, under ``by_margin``,
    the scores for each abstain margin (evaluated on the same fitted folds)."""
    ds = load_dataset(csv_path)
    n_groups = len(set(ds.groups))
    n_splits = min(n_splits, n_groups)
    X = np.asarray(ds.X, float)
    y = np.asarray(ds.y, float)
    groups = np.asarray(ds.groups)
    combos = np.asarray(ds.combo_ids)

    gkf = GroupKFold(n_splits=n_splits)
    maes = []
    argmax_true, oracle, base = [], [], []
    margin_true = {m: [] for m in margins}
    for tr, te in gkf.split(X, y, groups):
        reg = make_regressor(kind, random_state)
        reg.fit(X[tr], y[tr])
        maes.append(float(np.mean(np.abs(reg.predict(X[te]) - y[te]))))
        for _g, true_by, pred_by in _per_program_predictions(reg, X, y, groups, combos, te):
            oracle.append(max(true_by.values()))
            base.append(true_by.get(0, 1.0))
            argmax_true.append(true_by.get(_pick_argmax(pred_by), 1.0))
            for m in margins:
                margin_true[m].append(true_by.get(_pick_argmax(pred_by, m), 1.0))

    res = {
        "kind": kind, "n_splits": n_splits, "n_groups": n_groups,
        "held_out_programs": len(argmax_true),
        "cv_mae": statistics.mean(maes),
        **_score(argmax_true, oracle, base),
        "by_margin": {m: _score(margin_true[m], oracle, base) for m in margins},
    }
    return res


def bakeoff(csv_path: str, n_splits: int = 5) -> List[dict]:
    results = [cross_validate(csv_path, k, n_splits) for k in REGRESSORS]
    results.sort(key=lambda r: (-r["reco_speedup_mean"], r["regression_rate"]))
    return results


def choose_strategy(csv_path: str, n_splits: int = 5) -> dict:
    """Full bake-off: 3 regressors x {argmax, margin sweep} + per-pass classifiers.
    Returns a dict describing the winning strategy and its held-out scores, with
    the full comparison under ``table``."""
    regs = [cross_validate(csv_path, k, n_splits) for k in REGRESSORS]
    ds = load_dataset(csv_path)
    pp = _pass_cv(ds, n_splits=n_splits)

    table = []
    for r in regs:
        table.append({"strategy": "argmax", "kind": r["kind"], "margin": 0.0,
                      "cv_mae": r["cv_mae"], **{k: r[k] for k in
                      ("reco_speedup_mean", "oracle_speedup_mean", "baseline_mean",
                       "capture", "regression_rate")}})
        for m, sc in r["by_margin"].items():
            table.append({"strategy": f"margin:{m:.2f}", "kind": r["kind"], "margin": m,
                          "cv_mae": r["cv_mae"], **sc})
    table.append({"strategy": "per_pass", "kind": "hgb_clf", "margin": 0.0,
                  "cv_mae": float("nan"), **pp})

    # winner: the most useful recommender that still keeps regressions rare.
    # "rare" = at most REGRESS_CAP of held-out programs land >2% below baseline;
    # among those, take the highest true speedup.  (Pure "min regressions" would
    # just always pick baseline: 0% regress, 0% capture.)
    REGRESS_CAP = 0.10
    safe = [t for t in table if t["regression_rate"] <= REGRESS_CAP]
    pool = safe or table
    ranked = sorted(pool, key=lambda t: (-round(t["reco_speedup_mean"], 3),
                                         -round(t["capture"], 3),
                                         t["regression_rate"]))
    best_reg = min(regs, key=lambda r: r["cv_mae"])
    win = dict(ranked[0])
    # regressor kind to actually persist (drives the demo's predicted-speedup
    # readout even when the *pick* comes from per_pass)
    win["reg_kind"] = win["kind"] if win["kind"] in REGRESSORS else best_reg["kind"]
    win["cv_mae"] = best_reg["cv_mae"]
    win.update({"held_out_programs": regs[0]["held_out_programs"],
                "n_groups": regs[0]["n_groups"], "n_splits": regs[0]["n_splits"],
                "table": table})
    return win


# --------------------------------------------------------------------------- #
#  final fit                                                                   #
# --------------------------------------------------------------------------- #
def _top_features(reg, ds, kind):
    if hasattr(reg, "feature_importances_"):
        imp = list(reg.feature_importances_)
    else:
        X = np.asarray(ds.X, float)
        y = np.asarray(ds.y, float)
        take = min(4000, len(y))
        rs = np.random.RandomState(0).choice(len(y), take, replace=False)
        pi = permutation_importance(reg, X[rs], y[rs], n_repeats=4,
                                    random_state=0, n_jobs=-1)
        imp = list(pi.importances_mean)
    order = sorted(zip(ds.feature_names, (float(v) for v in imp)), key=lambda kv: -kv[1])
    return [n for n, _v in order][:16]


def train_final(csv_path: str, model_path: str, kind: str = "random_forest",
                random_state: int = 0, strategy: str = "argmax",
                margin: float = 0.0) -> SpeedupModel:
    ds = load_dataset(csv_path)
    reg = make_regressor(kind if kind in REGRESSORS else "hist_gradient_boosting",
                         random_state)
    reg.fit(np.asarray(ds.X, float), np.asarray(ds.y, float))

    pass_clfs, n_static = (None, None)
    if strategy == "per_pass":
        pass_clfs, n_static = fit_pass_classifiers(csv_path, random_state)

    model = SpeedupModel(
        regressor=reg, feature_names=ds.feature_names,
        pass_classifiers=pass_clfs,
        metadata={"n_rows": len(ds), "kind": kind, "strategy": strategy,
                  "margin": float(margin), "n_static": n_static,
                  "top_features": _top_features(reg, ds, kind)})
    model.save(model_path)
    return model


def main(argv=None):
    p = argparse.ArgumentParser(description="Bake off the MiniC speedup recommender")
    p.add_argument("--csv", default="data/benchmark_dataset.csv")
    p.add_argument("--model-out", default="data/trained_model.pkl")
    p.add_argument("--splits", type=int, default=5)
    args = p.parse_args(argv)

    win = choose_strategy(args.csv, args.splits)
    print("=== strategy bake-off (GroupKFold / KFold by program) ===")
    print(f"{'strategy':14s} {'model':22s} {'reco':>6} {'oracle':>7} "
          f"{'capture':>8} {'regress%':>9}")
    for t in sorted(win["table"], key=lambda t: (t["regression_rate"], -t["capture"])):
        print(f"{t['strategy']:14s} {t['kind']:22s} x{t['reco_speedup_mean']:4.2f} "
              f"x{t['oracle_speedup_mean']:5.2f} {100*t['capture']:7.0f}% "
              f"{100*t['regression_rate']:8.0f}%")
    print(f"\nwinner: {win['strategy']} / {win['kind']}  "
          f"(reco x{win['reco_speedup_mean']:.2f}, {100*win['capture']:.0f}% capture, "
          f"{100*win['regression_rate']:.0f}% regress)")

    m = train_final(args.csv, args.model_out, kind=win["reg_kind"],
                    strategy="per_pass" if win["strategy"] == "per_pass" else
                    ("margin" if win["margin"] else "argmax"),
                    margin=win["margin"])
    print(f"final model -> {args.model_out}  ({m.metadata['n_rows']} rows)")
    print("top features:", ", ".join(m.metadata["top_features"]))
    return win


if __name__ == "__main__":
    main()
