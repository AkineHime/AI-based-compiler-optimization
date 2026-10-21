"""Build docs/results.html, the visual results report, from the measured dataset.

    python minic.py results                  # rebuild from the dataset + cached model scores
    python minic.py results --recompute      # also re-run the held-out ML evaluation (~1 min)

The page is a static, self-contained HTML file (no server, no CDN): this module
computes a JSON payload and injects it into docs/results_template.html.

Everything shown is computed from data/benchmark_dataset.csv except the model's
held-out picks, which need a 5-fold cross-validation; those are cached in
data/results_summary.json so the page rebuilds in seconds.
"""
import json
import os
import re
from typing import Dict, List

import numpy as np
import pandas as pd

from ..optimizer.pass_manager import PASS_ABBR, NUM_PASSES
from .perf_analysis import analyse

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
CSV = os.path.join(ROOT, "data", "benchmark_dataset.csv")
CACHE = os.path.join(ROOT, "data", "results_summary.json")
TEMPLATE = os.path.join(ROOT, "docs", "results_template.html")
PAGE = os.path.join(ROOT, "docs", "results.html")
MODEL_TABLE = os.path.join(ROOT, "MODEL_COMPARISON.md")

ALL_ON = (1 << NUM_PASSES) - 1
REGRESS = 0.98  # "slower than doing nothing" = more than 2% slower than combo 0


def _gm(x) -> float:
    x = np.asarray(x, float)
    return float(np.exp(np.log(x).mean()))


def _family(category: str, pattern: str) -> str:
    return pattern if category == "generated" else category


def _held_out_ml_picks(csv_path: str) -> Dict[str, float]:
    """True speedup of the recommender's pick for every program, each predicted by a
    model that never saw that program (GroupKFold by program, HistGBT + 5% margin,
    i.e. the shipped configuration)."""
    from sklearn.model_selection import GroupKFold
    from ..ml.dataset import load_dataset
    from ..ml.model import make_regressor

    ds = load_dataset(csv_path)
    X, y = np.asarray(ds.X, float), np.asarray(ds.y, float)
    g, c = np.asarray(ds.groups), np.asarray(ds.combo_ids).astype(int)
    picks = {}
    for tr, te in GroupKFold(5).split(X, y, g):
        reg = make_regressor("hist_gradient_boosting", 0)
        reg.fit(X[tr], y[tr])
        pred = reg.predict(X[te])
        for prog in np.unique(g[te]):
            m = g[te] == prog
            true_by = dict(zip(c[te][m], y[te][m]))
            pred_by = dict(zip(c[te][m], pred[m]))
            best = max(pred_by, key=pred_by.get)
            pick = best if pred_by[best] >= 1.05 else 0  # abstain margin
            picks[str(prog)] = float(true_by[pick])
    return picks


def _model_table() -> List[dict]:
    rows = []
    if not os.path.exists(MODEL_TABLE):
        return rows
    pat = re.compile(r"^\|\s*\d+\s*\|\s*\*\*(.+?)\*\*\s*\|\s*(.+?)\s*\|\s*\*\*x([\d.]+)\*\*\s*\|"
                     r"\s*(\d+)%\s*\|\s*(\d+)%\s*\|\s*[\d.]+\s*\|\s*(.+?)\s*\|")
    for line in open(MODEL_TABLE, encoding="utf-8"):
        m = pat.match(line)
        if m:
            rows.append({"model": m[1], "input": m[2], "reco": float(m[3]),
                         "capture": int(m[4]), "regress": int(m[5]), "size": m[6]})
    return rows


EXAMPLE = """int main() {
    int a = 6;
    int b = 7;
    int sum = 0;
    int i = 0;
    while (i < 100) {
        int k = a * b;
        sum = sum + k * 2;
        i = i + 1;
    }
    return sum;
}
"""


def _example() -> dict:
    """The page's worked example, produced by the real compiler (not hand-written)."""
    from .sweeper import frontend
    from ..ir.ir_printer import IRPrinter
    from ..optimizer import optimize_program
    from ..codegen import CEmitter

    _ast, tac = frontend(EXAMPLE)
    before = IRPrinter.format_program(tac)
    opt = optimize_program(tac, ALL_ON)
    after = IRPrinter.format_program(opt)
    count = lambda s: sum(1 for l in s.splitlines() if l.startswith("    ") and l.strip())
    return {"source": EXAMPLE, "tac": before, "tac_opt": after,
            "n_tac": count(before), "n_tac_opt": count(after),
            "c": CEmitter().emit(opt)}


def compute(csv_path: str = CSV, recompute: bool = False) -> dict:
    d = pd.read_csv(csv_path)
    # the stored speedup_ratio column, so numbers match RESULTS.md exactly
    t = d.pivot_table(index="program_id", columns="combo_id", values="speedup_ratio")
    meta = d.drop_duplicates("program_id").set_index("program_id")[["category", "pattern"]]
    sp = t.values                                   # programs x 64 speedups
    progs = list(t.index)
    best_c = sp.argmax(1)
    best = sp.max(1)
    all_on = sp[:, ALL_ON]

    # ---- ML held-out picks (cached)
    cache = {}
    if os.path.exists(CACHE) and not recompute:
        cache = json.load(open(CACHE, encoding="utf-8"))
    if "ml_picks" not in cache or set(cache["ml_picks"]) != set(map(str, progs)):
        print("evaluating the recommender on held-out programs (5-fold, ~1 min)...")
        cache["ml_picks"] = _held_out_ml_picks(csv_path)
        json.dump(cache, open(CACHE, "w", encoding="utf-8"), indent=0)
    ml = np.array([cache["ml_picks"][str(p)] for p in progs])

    pa = analyse(csv_path)

    def strat(name, runs, v, note):
        return {"name": name, "runs": runs, "mean": round(float(v.mean()), 5),
                "geomean": round(_gm(v), 5), "regress": round(float((v < REGRESS).mean()) * 100, 1),
                "worst": round(float(v.min()), 2), "note": note}

    strategies = [
        strat("No optimization", "1", np.ones(len(progs)), "the baseline"),
        strat("All 6 passes", "1", all_on, "the obvious default"),
        strat("ML recommender", "0", ml, "predicts from code, never runs it"),
        {"name": "Greedy search", "runs": f"{pa['greedy_runs']:.0f}",
         "mean": round(pa["greedy_mean"], 3), "geomean": round(pa["greedy"], 3),
         "regress": 0.0, "worst": 1.0, "note": "adds one pass at a time, timing each"},
        strat("Oracle", "64", best, "times every combo, keeps the fastest"),
    ]

    # ---- 64-combo grid
    combos = []
    for c in range(1 << NUM_PASSES):
        v = sp[:, c]
        combos.append({"c": c, "gm": round(_gm(v), 5), "regress": round(float((v < REGRESS).mean()) * 100, 1),
                       "best_for": int((best_c == c).sum())})

    # ---- families
    fam = [_family(meta.loc[p, "category"], meta.loc[p, "pattern"]) for p in progs]
    families = []
    for f in sorted(set(fam)):
        idx = [i for i, x in enumerate(fam) if x == f]
        families.append({"family": f, "n": len(idx), "handwritten": f in
                         ("loops", "numeric", "structs", "recursion", "strings"),
                         "best": round(_gm(best[idx]), 3), "all_on": round(_gm(all_on[idx]), 3),
                         "ml": round(_gm(ml[idx]), 3)})
    families.sort(key=lambda r: -r["best"])

    # ---- every program (for the scatter): [all_on, best, ml, family index, name, best combo]
    fam_names = [f["family"] for f in families]
    points = [[round(float(all_on[i]), 3), round(float(best[i]), 3), round(float(ml[i]), 3),
               fam_names.index(fam[i]), progs[i], int(best_c[i])] for i in range(len(progs))]

    top = sorted(range(len(progs)), key=lambda i: -best[i])[:12]
    hist_edges = [0.9, 1.0, 1.05, 1.1, 1.2, 1.35, 1.6, 2.0, 3.0, 5.0]
    hist = np.histogram(np.clip(best, 0.9, 4.99), bins=hist_edges)[0].tolist()

    return {
        "n_programs": len(progs), "n_configs": int(len(d)), "n_combos": 1 << NUM_PASSES,
        "n_handwritten": int(sum(1 for f in fam if f in ("loops", "numeric", "structs", "recursion", "strings"))),
        "passes": [PASS_ABBR[1 << i] for i in range(NUM_PASSES)],
        "headline": {
            "oracle_gm": round(_gm(best), 5), "max": round(float(best.max()), 2),
            "max_program": progs[int(best.argmax())],
            "all_on_gm": round(_gm(all_on), 5), "all_on_worst": round(float(all_on.min()), 2),
            "all_on_short": int((best > all_on * 1.02).sum()),
            "config_regress": round(pa["regress_frac"] * 100, 1),
            "additive_pred": round(pa["additive_pred"], 3), "additive_actual": round(pa["additive_actual"], 3),
            "additive_off10": pa["additive_off10"],
            "noise_med": round(pa["noise_med"], 3), "noise_p95": round(pa["noise_p95"], 3),
        },
        "pass_effects": [{k: (round(v, 3) if isinstance(v, float) else v) for k, v in p.items()}
                         for p in pa["passes"]],
        "strategies": strategies,
        "combos": combos,
        "families": families,
        "points": points,
        "top": [{"program": progs[i], "family": fam[i], "best": round(float(best[i]), 2),
                 "all_on": round(float(all_on[i]), 2), "ml": round(float(ml[i]), 2),
                 "combo": int(best_c[i])} for i in top],
        "hist": {"edges": hist_edges, "counts": hist},
        "models": _model_table(),
        "example": _example(),
    }


def build(csv_path: str = CSV, recompute: bool = False) -> str:
    payload = compute(csv_path, recompute)
    html = open(TEMPLATE, encoding="utf-8").read()
    marker = "/*__DATA__*/null"
    if marker not in html:
        raise RuntimeError(f"{TEMPLATE} has no {marker} placeholder")
    html = html.replace(marker, json.dumps(payload, separators=(",", ":")))
    with open(PAGE, "w", encoding="utf-8", newline="\n") as f:
        f.write(html)
    print(f"wrote {PAGE}")
    return PAGE


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--recompute", action="store_true")
    build(recompute=ap.parse_args().recompute)
