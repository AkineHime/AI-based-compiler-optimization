"""Multi-model comparison: Linear / RF / HGBT / MLP / 1D-CNN / GRU (+ hybrids).

Every model predicts ``speedup_ratio`` for a (program, combo) pair and is scored
identically -- GroupKFold by ``program_id``, ranked on the true speedup of the
combo it recommends (with the same abstain-margin sweep the production model
uses).  Tabular models see the 27 features + 6 pass bits; sequence models see
the tokenised combo-0 TAC + 6 pass bits; hybrids see both.

The sequence models are trained **program-batched** (encode each program once,
score all 64 combos in one shot) -- on CPU the naive row-batched version would
take ~15 h.
"""
import statistics
import time
from typing import Dict, List

import numpy as np
from sklearn.linear_model import Ridge
from sklearn.model_selection import KFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from .dataset import FLAG_BITS, load_dataset
from .model import make_regressor

MARGINS = (0.0, 0.03, 0.05, 0.08, 0.12, 0.18, 0.25)
NUM_COMBOS = 64
_ALL_BITS = np.array([[1.0 if c & b else 0.0 for b in FLAG_BITS]
                      for c in range(NUM_COMBOS)], dtype=np.float32)  # (64, 6)

# name -> input representation
MODEL_SPECS: Dict[str, str] = {
    "linear": "tabular",
    "random_forest": "tabular",
    "hist_gradient_boosting": "tabular",
    "mlp": "tabular",
    "cnn1d": "sequence",
    "gru": "sequence",
    "cnn1d_hybrid": "hybrid",
    "gru_hybrid": "hybrid",
}
TORCH_MODELS = {"mlp", "cnn1d", "gru", "cnn1d_hybrid", "gru_hybrid"}


# --------------------------------------------------------------------------- #
#  reshape rows -> per-program arrays                                          #
# --------------------------------------------------------------------------- #
def to_program_arrays(ds, seqs=None) -> dict:
    X = np.asarray(ds.X, float)
    y = np.asarray(ds.y, float)
    groups = np.asarray(ds.groups)
    combos = np.asarray(ds.combo_ids)
    n_static = len(ds.feature_names) - len(FLAG_BITS)

    pids = sorted(set(groups))
    P = len(pids)
    feats = np.zeros((P, n_static), np.float32)
    sp = np.full((P, NUM_COMBOS), np.nan, np.float32)
    for pi, g in enumerate(pids):
        idx = np.where(groups == g)[0]
        feats[pi] = X[idx[0], :n_static]
        for i in idx:
            sp[pi, int(combos[i])] = y[i]
    mask = ~np.isnan(sp)
    sp_filled = np.nan_to_num(sp, nan=1.0)

    tokens = None
    if seqs is not None:
        missing = [g for g in pids if g not in seqs["by_pid"]]
        if missing:
            raise KeyError(f"{len(missing)} programs have no TAC sequence, e.g. {missing[:3]}")
        tokens = np.stack([np.asarray(seqs["by_pid"][g]) for g in pids]).astype(np.int64)

    return {"pids": pids, "feats": feats, "tokens": tokens,
            "speedup": sp_filled, "mask": mask, "n_static": n_static}


# --------------------------------------------------------------------------- #
#  scoring (model-agnostic)                                                   #
# --------------------------------------------------------------------------- #
def _score(picks_true: List[float], oracle: List[float], base: List[float]) -> dict:
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


def _pick(pred_by: dict, margin: float) -> int:
    best = max(pred_by, key=pred_by.get)
    if margin and pred_by[best] < 1.0 + margin:
        return 0
    return best


def _aggregate(per_prog: List[dict], margins=MARGINS) -> dict:
    """per_prog: [{pid, category, true_by, pred_by}] -> scores + by_margin + per_category."""
    def scored(margin):
        pt, orc, bas = [], [], []
        for r in per_prog:
            pt.append(r["true_by"].get(_pick(r["pred_by"], margin), 1.0))
            orc.append(max(r["true_by"].values()))
            bas.append(r["true_by"].get(0, 1.0))
        return _score(pt, orc, bas)

    mae = statistics.mean(
        abs(r["pred_by"][c] - r["true_by"][c])
        for r in per_prog for c in r["true_by"] if c in r["pred_by"])

    out = {"cv_mae": mae, **scored(0.0),
           "by_margin": {m: scored(m) for m in margins if m > 0}}

    # per-category reco speedup at margin 0 (whichever margin wins is applied later)
    cats: Dict[str, List[float]] = {}
    for r in per_prog:
        cats.setdefault(r["category"], []).append(
            r["true_by"].get(_pick(r["pred_by"], 0.0), 1.0))
    out["per_category"] = {k: statistics.mean(v) for k, v in sorted(cats.items())}
    out["per_category_n"] = {k: len(v) for k, v in sorted(cats.items())}
    return out


# --------------------------------------------------------------------------- #
#  one model, cross-validated                                                 #
# --------------------------------------------------------------------------- #
def _sk_factory(name, seed):
    if name == "linear":
        return make_pipeline(StandardScaler(), Ridge(alpha=1.0, random_state=seed))
    return make_regressor(name, seed)


def _program_folds(pids: List[str], n_splits: int, seed: int):
    """One shared program partition every model is evaluated on."""
    P = len(pids)
    kf = KFold(n_splits=min(n_splits, P), shuffle=True, random_state=seed)
    return list(kf.split(np.arange(P)))


def cross_validate_model(name: str, ds, seqs, cat_of: Dict[str, str],
                         n_splits: int = 5, seed: int = 0, folds=None) -> dict:
    spec = MODEL_SPECS[name]
    combos = np.asarray(ds.combo_ids)
    groups = np.asarray(ds.groups)
    X = np.asarray(ds.X, float)
    y = np.asarray(ds.y, float)

    pa = to_program_arrays(ds, seqs if spec in ("sequence", "hybrid") else None)
    pids = pa["pids"]
    pidx = {g: i for i, g in enumerate(pids)}
    row_of = {g: np.where(groups == g)[0] for g in pids}
    folds = folds or _program_folds(pids, n_splits, seed)

    per_prog: List[dict] = []
    fit_times: List[float] = []
    use_torch = name in TORCH_MODELS
    need_tokens = spec in ("sequence", "hybrid")

    for tr_p, te_p in folds:
        if use_torch:
            from .models_torch import TorchSpeedupModel
            m = TorchSpeedupModel(name, seed=seed, n_static=pa["n_static"])
            tok_tr = pa["tokens"][tr_p] if need_tokens else None
            t0 = time.perf_counter()
            m.fit(pa["feats"][tr_p], tok_tr, pa["speedup"][tr_p], pa["mask"][tr_p])
            fit_times.append(time.perf_counter() - t0)
            pred = m.predict(pa["feats"][te_p],
                             pa["tokens"][te_p] if need_tokens else None)  # (n_te, 64)
            for row_i, p_i in enumerate(te_p):
                exists = np.where(pa["mask"][p_i])[0]
                per_prog.append({
                    "pid": pids[p_i], "category": cat_of.get(pids[p_i], "?"),
                    "true_by": {int(c): float(pa["speedup"][p_i, c]) for c in exists},
                    "pred_by": {int(c): float(pred[row_i, c]) for c in exists}})
        else:
            tr_rows = np.concatenate([row_of[pids[i]] for i in tr_p])
            reg = _sk_factory(name, seed)
            t0 = time.perf_counter()
            reg.fit(X[tr_rows], y[tr_rows])
            fit_times.append(time.perf_counter() - t0)
            for p_i in te_p:
                idx = row_of[pids[p_i]]
                pred = reg.predict(X[idx])
                per_prog.append({
                    "pid": pids[p_i], "category": cat_of.get(pids[p_i], "?"),
                    "true_by": {int(combos[i]): float(y[i]) for i in idx},
                    "pred_by": {int(combos[i]): float(p) for i, p in zip(idx, pred)}})

    agg = _aggregate(per_prog)
    agg.update({"model": name, "n_splits": len(folds),
                "held_out_programs": len(per_prog),
                "train_time_s": statistics.mean(fit_times) if fit_times else 0.0})
    return agg


# --------------------------------------------------------------------------- #
#  full comparison                                                            #
# --------------------------------------------------------------------------- #
def compare(csv_path: str, seq_path: str = "data/tac_sequences.npz",
            models: List[str] = None, n_splits: int = 5, seed: int = 0,
            progress=print) -> List[dict]:
    from .sequences import load_sequences
    ds = load_dataset(csv_path)
    seqs = load_sequences(seq_path)
    cat_of = _category_map(csv_path)
    models = models or list(MODEL_SPECS)
    pids = sorted(set(np.asarray(ds.groups)))
    folds = _program_folds(pids, n_splits, seed)  # every model, same partition

    rows = []
    for name in models:
        progress(f"  {name} ...")
        t0 = time.time()
        r = cross_validate_model(name, ds, seqs, cat_of, n_splits, seed, folds=folds)
        r["wall_s"] = round(time.time() - t0, 1)
        rows.append(r)
        progress(f"    reco x{r['reco_speedup_mean']:.3f}  "
                 f"capture {100*r['capture']:.0f}%  regress {100*r['regression_rate']:.0f}%  "
                 f"({r['wall_s']}s)")
    return rows


def _category_map(csv_path: str) -> Dict[str, str]:
    import csv as _csv
    out = {}
    with open(csv_path, newline="", encoding="utf-8") as fh:
        for row in _csv.DictReader(fh):
            out[row["program_id"]] = row.get("pattern") or row.get("category", "?")
    return out
