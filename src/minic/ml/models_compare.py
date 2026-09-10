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


# --------------------------------------------------------------------------- #
#  pick each model's best abstain margin, then rank models                     #
# --------------------------------------------------------------------------- #
REGRESS_CAP = 0.10


def best_config(r: dict) -> dict:
    """r is one compare() row.  Choose margin 0 or the best sweep entry that keeps
    regressions <= REGRESS_CAP, maximising reco speedup."""
    opts = [{"margin": 0.0, "reco_speedup_mean": r["reco_speedup_mean"],
             "capture": r["capture"], "regression_rate": r["regression_rate"]}]
    for m, sc in r.get("by_margin", {}).items():
        opts.append({"margin": m, **{k: sc[k] for k in
                     ("reco_speedup_mean", "capture", "regression_rate")}})
    safe = [o for o in opts if o["regression_rate"] <= REGRESS_CAP] or opts
    best = max(safe, key=lambda o: (round(o["reco_speedup_mean"], 3),
                                    round(o["capture"], 3),
                                    -o["regression_rate"]))
    return best


def rank(rows: List[dict]) -> List[dict]:
    out = []
    for r in rows:
        bc = best_config(r)
        out.append({**r, "best_margin": bc["margin"],
                    "reco": bc["reco_speedup_mean"], "cap": bc["capture"],
                    "regress": bc["regression_rate"]})
    out.sort(key=lambda r: (-round(r["reco"], 3), -round(r["cap"], 3), r["regress"]))
    return out


# --------------------------------------------------------------------------- #
#  deployment cost: model size + inference latency                            #
# --------------------------------------------------------------------------- #
def measure_deploy_cost(name: str, ds, seqs, seed: int = 0) -> dict:
    import io
    import pickle
    pa = to_program_arrays(ds, seqs if MODEL_SPECS[name] in ("sequence", "hybrid") else None)
    need_tokens = MODEL_SPECS[name] in ("sequence", "hybrid")
    n_probe = min(24, len(pa["pids"]))

    if name in TORCH_MODELS:
        from .models_torch import TorchSpeedupModel
        m = TorchSpeedupModel(name, seed=seed, n_static=pa["n_static"], epochs=6)
        m.fit(pa["feats"], pa["tokens"] if need_tokens else None,
              pa["speedup"], pa["mask"])
        size_kb = m.state_size_kb()
        t0 = time.perf_counter()
        m.predict(pa["feats"][:n_probe], pa["tokens"][:n_probe] if need_tokens else None)
        lat = (time.perf_counter() - t0) / n_probe * 1000
    else:
        X = np.asarray(ds.X, float)
        y = np.asarray(ds.y, float)
        groups = np.asarray(ds.groups)
        reg = _sk_factory(name, seed)
        reg.fit(X, y)
        buf = io.BytesIO()
        pickle.dump(reg, buf)
        size_kb = len(buf.getvalue()) / 1024
        probe_rows = np.concatenate(
            [np.where(groups == pa["pids"][i])[0] for i in range(n_probe)])
        t0 = time.perf_counter()
        reg.predict(X[probe_rows])
        lat = (time.perf_counter() - t0) / n_probe * 1000
    return {"model_size_kb": round(size_kb, 1),
            "predict_latency_ms": round(lat, 2)}


# --------------------------------------------------------------------------- #
#  markdown report                                                            #
# --------------------------------------------------------------------------- #
_PRETTY = {"linear": "Linear (Ridge)", "random_forest": "Random Forest",
           "hist_gradient_boosting": "HistGradient Boosting", "mlp": "MLP",
           "cnn1d": "1D-CNN", "gru": "GRU (RNN)",
           "cnn1d_hybrid": "1D-CNN + features", "gru_hybrid": "GRU + features"}
_TRACK = {"tabular": "features", "sequence": "TAC sequence", "hybrid": "both"}


def render_markdown(ranked_rows: List[dict], deploy: Dict[str, dict],
                    n_programs: int, n_combos: int = 64, seeds: int = 1) -> str:
    L = ["# Model comparison — which model recommends the best passes\n"]
    L.append(f"All {len(ranked_rows)} models predict `speedup_ratio` for a "
             f"(program, pass-combo) pair and are scored **identically**: one "
             f"shared 5-fold split over {n_programs} programs, ranked on the true "
             f"speedup of the combo each model recommends, with the same "
             f"abstain-margin sweep the production recommender uses.\n")
    L.append(f"- Tabular models see the 27 static features + 6 pass bits.")
    L.append(f"- Sequence models (CNN, GRU) see the tokenised combo-0 TAC + 6 pass bits.")
    L.append(f"- Hybrids see both."
             + (f"  Neural rows are the mean of {seeds} seeds." if seeds > 1 else "") + "\n")

    L.append("## Results\n")
    L.append("| # | model | input | reco speedup | oracle capture | regressions | "
             "speedup MAE | size | train | infer |")
    L.append("|--:|---|---|--:|--:|--:|--:|--:|--:|--:|")
    for i, r in enumerate(ranked_rows, 1):
        d = deploy.get(r["model"], {})
        mae = "--" if r["cv_mae"] != r["cv_mae"] else f"{r['cv_mae']:.3f}"
        L.append(
            f"| {i} | **{_PRETTY.get(r['model'], r['model'])}** | "
            f"{_TRACK[MODEL_SPECS[r['model']]]} | "
            f"**x{r['reco']:.3f}** | {100*r['cap']:.0f}% | {100*r['regress']:.0f}% | "
            f"{mae} | {_kb(d.get('model_size_kb'))} | "
            f"{r['train_time_s']:.1f}s | {d.get('predict_latency_ms', '--')} ms |")
    L.append("")
    L.append(f"*reco speedup* = held-out true speedup of the recommended combo "
             f"(at each model's best abstain margin). *capture* = fraction of the "
             f"oracle-best gain recovered. *infer* = ms to score all {n_combos} "
             f"combos for one program.\n")

    win = ranked_rows[0]
    L.append(f"**Winner: {_PRETTY.get(win['model'], win['model'])}** — "
             f"reco x{win['reco']:.3f}, {100*win['cap']:.0f}% capture, "
             f"{100*win['regress']:.0f}% regressions"
             + (f", abstain margin x{1+win['best_margin']:.2f}" if win['best_margin'] else "")
             + ".\n")

    # per-category grid
    cats = sorted({c for r in ranked_rows for c in r["per_category"]})
    L.append("## Recommendation speedup by program type\n")
    L.append("| model | " + " | ".join(cats) + " |")
    L.append("|---|" + "|".join("--:" for _ in cats) + "|")
    for r in ranked_rows:
        cells = [f"x{r['per_category'].get(c, float('nan')):.2f}"
                 if c in r["per_category"] else "--" for c in cats]
        L.append(f"| {_PRETTY.get(r['model'], r['model'])} | " + " | ".join(cells) + " |")
    ns = ranked_rows[0].get("per_category_n", {})
    L.append("\n" + "  ".join(f"`{c}`: {ns.get(c, '?')}" for c in cats) + "  (held-out program counts)\n")

    L.append("## Method notes\n")
    L.append("- Same GroupKFold-by-program split for every model — a program's 64 "
             "rows share features, so a random row split would leak.")
    L.append("- Sequence models are trained program-batched (one encode per "
             "program, all 64 combos scored together); on CPU the row-batched "
             "version is ~50x slower.")
    L.append("- The GRU is a compact 1-layer model capped at 320 tokens — a "
             "bidirectional / multi-layer RNN on 640-token programs needs a GPU.")
    L.append("- All models use identical inputs otherwise and the identical "
             "abstain-margin recommendation rule.")
    return "\n".join(L)


def _kb(v):
    if v is None:
        return "--"
    return f"{v/1024:.1f} MB" if v >= 1024 else f"{v:.0f} KB"


# --------------------------------------------------------------------------- #
#  orchestrator                                                               #
# --------------------------------------------------------------------------- #
def _mean_rows(runs: List[List[dict]]) -> List[dict]:
    """Average matching-model rows across seeds (scalars only; keep run 0's dicts)."""
    by_name = {}
    for run in runs:
        for r in run:
            by_name.setdefault(r["model"], []).append(r)
    out = []
    for name, rs in by_name.items():
        base = dict(rs[0])
        for k in ("reco_speedup_mean", "capture", "regression_rate", "cv_mae",
                  "oracle_speedup_mean", "train_time_s"):
            base[k] = statistics.mean(r[k] for r in rs)
        base["by_margin"] = {
            m: {kk: statistics.mean(r["by_margin"][m][kk] for r in rs)
                for kk in rs[0]["by_margin"][m]}
            for m in rs[0].get("by_margin", {})}
        base["seeds"] = len(rs)
        out.append(base)
    return out


def run_full_comparison(csv_path: str = "data/benchmark_dataset.csv",
                        seq_path: str = "data/tac_sequences.npz",
                        out_md: str = "MODEL_COMPARISON.md",
                        n_splits: int = 5, seeds: int = 1,
                        models: List[str] = None, progress=print) -> dict:
    from .dataset import load_dataset as _ld
    from .sequences import load_sequences as _ls
    models = models or list(MODEL_SPECS)
    ds = _ld(csv_path)
    seqs = _ls(seq_path)
    n_programs = len(set(np.asarray(ds.groups)))

    runs = []
    for s in range(seeds):
        progress(f"\n=== seed {s} ===")
        runs.append(compare(csv_path, seq_path, models, n_splits, seed=s, progress=progress))
    rows = _mean_rows(runs) if seeds > 1 else runs[0]

    ranked = rank(rows)
    progress("\nmeasuring model size / inference latency ...")
    deploy = {name: measure_deploy_cost(name, ds, seqs, seed=0) for name in models}

    md = render_markdown(ranked, deploy, n_programs, seeds=seeds)
    with open(out_md, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(md)
    progress(f"\nwrote {out_md}")
    return {"ranked": ranked, "deploy": deploy, "winner": ranked[0]}


def _main(argv=None):
    import argparse
    p = argparse.ArgumentParser(description="Compare recommendation models")
    p.add_argument("--csv", default="data/benchmark_dataset.csv")
    p.add_argument("--seq", default="data/tac_sequences.npz")
    p.add_argument("--out", default="MODEL_COMPARISON.md")
    p.add_argument("--splits", type=int, default=5)
    p.add_argument("--seeds", type=int, default=1)
    p.add_argument("--models", default="", help="comma list; default all 8")
    a = p.parse_args(argv)
    run_full_comparison(a.csv, a.seq, a.out, a.splits, a.seeds,
                        [m.strip() for m in a.models.split(",")] if a.models else None)


if __name__ == "__main__":
    _main()
