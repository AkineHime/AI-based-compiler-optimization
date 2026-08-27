"""Regenerate docs/results.html from the current dataset + a fresh CV bake-off.

Only the data island and a few headline spans are rewritten; the page's markup
and styling live in the file and are left untouched.
"""
import json
import os
import re

from .report import summarize
from ..ml.train import choose_strategy, train_final

PAGE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))), "docs", "results.html")


def build(csv_path="data/benchmark_dataset.csv", model_out="data/trained_model.pkl",
          _precomputed=None):
    s = summarize(csv_path)
    if _precomputed is not None:
        win, cv, model = _precomputed
    else:
        win = choose_strategy(csv_path)
        strat = ("per_pass" if win["strategy"] == "per_pass"
                 else "margin" if win["margin"] else "argmax")
        kind = win["reg_kind"]
        model = train_final(csv_path, model_out, kind=kind, strategy=strat,
                            margin=win["margin"])
        amx = next((t for t in win["table"] if t["strategy"] == "argmax"
                    and t["kind"] == kind), win)
        cv = {"kind": kind, "strategy": win["strategy"], "margin": win["margin"],
              "argmax_reco": amx["reco_speedup_mean"],
              "argmax_regress": amx["regression_rate"],
              "held_out_programs": win["held_out_programs"], "n_groups": win["n_groups"],
              "n_splits": win["n_splits"], "cv_mae": win.get("cv_mae", float("nan")),
              "reco_speedup_mean": win["reco_speedup_mean"],
              "oracle_speedup_mean": win["oracle_speedup_mean"],
              "baseline_mean": win["baseline_mean"], "capture": win["capture"],
              "regression_rate": win["regression_rate"]}
    # the page frames these as "static program features" -> drop the pass-flag
    # inputs (which unsurprisingly dominate raw importance) for that list
    _imp = model.metadata.get("top_features", [])
    top_feats = [f[2:] for f in _imp if f.startswith("f_")][:7]

    ranked = sorted(s["per_program"], key=lambda p: -p["best_speedup"])
    data = [
        [p["program_id"], p["category"], round(p["best_speedup"], 2),
         round(p["all_on_speedup"], 2), p["best_combo"]]
        for p in ranked[:26]
    ]
    # speedup distribution over ALL programs
    edges = [1.0, 1.05, 1.1, 1.2, 1.35, 1.6, 2.0, 99]
    hist = [0] * (len(edges) - 1)
    for p in s["per_program"]:
        v = p["best_speedup"]
        for b in range(len(edges) - 1):
            if edges[b] <= v < edges[b + 1]:
                hist[b] += 1
                break
    cats = sorted(s["category_geomeans"].items(), key=lambda kv: -kv[1])

    payload = {
        "n_programs": s["n_programs"],
        "n_combos": 64,
        "geomean_best": round(s["geomean_best"], 3),
        "geomean_all_on": round(s["geomean_all_on"], 3),
        "max_speedup": round(s["max_speedup"], 2),
        "max_program": data[0][0] if data else "",
        "n_all_on_suboptimal": s["n_all_on_suboptimal"],
        "safe_combo": s["safe_combo"],
        "safe_geomean": round(s["safe_combo_geomean"], 2),
        "safe_worst": round(s["safe_combo_worst"], 2),
        "best_fixed_combo": s["best_single_combo"],
        "best_fixed_geomean": round(s["best_single_combo_geomean"], 2),
        "cv": {
            "kind": cv["kind"],
            "strategy": cv["strategy"],
            "margin": cv["margin"],
            "argmax_reco": round(cv["argmax_reco"], 2),
            "argmax_regress": round(100 * cv["argmax_regress"]),
            "held_out": cv["held_out_programs"],
            "n_groups": cv["n_groups"],
            "folds": cv["n_splits"],
            "mae": round(cv["cv_mae"], 3),
            "reco": round(cv["reco_speedup_mean"], 2),
            "oracle": round(cv["oracle_speedup_mean"], 2),
            "baseline": round(cv["baseline_mean"], 2),
            "capture": round(100 * cv["capture"]),
            "regression_rate": round(100 * cv["regression_rate"]),
        },
        "data": data,
        "hist": hist,
        "hist_labels": ["1.0-1.05", "1.05-1.1", "1.1-1.2", "1.2-1.35",
                        "1.35-1.6", "1.6-2.0", "2.0+"],
        "cats": [[c, round(g, 2)] for c, g in cats],
        "top_features": top_feats,
    }

    html = open(PAGE, encoding="utf-8").read()
    island = "const RESULTS = " + json.dumps(payload, indent=2) + ";"
    if "const RESULTS =" in html:
        html = re.sub(r"const RESULTS = \{.*?\n\};", island, html, count=1, flags=re.S)
    else:
        html = html.replace("<script>", "<script>\n" + island, 1)
    open(PAGE, "w", encoding="utf-8", newline="\n").write(html)
    print(f"updated {PAGE}")
    print(json.dumps({k: payload[k] for k in
                      ("n_programs", "geomean_best", "max_speedup")}, indent=2))
    return payload


if __name__ == "__main__":
    build()
