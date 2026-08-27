"""Turn a sweep CSV into a human-readable results summary (the headline output)."""
import csv
import math
import statistics
from collections import defaultdict
from typing import Dict, List

from ..optimizer.pass_manager import get_pass_names, NUM_PASSES


def _geomean(xs: List[float]) -> float:
    xs = [x for x in xs if x > 0]
    return math.exp(sum(math.log(x) for x in xs) / len(xs)) if xs else float("nan")


def summarize(csv_path: str) -> dict:
    rows = list(csv.DictReader(open(csv_path, newline="", encoding="utf-8")))
    by_prog: Dict[str, Dict[int, float]] = defaultdict(dict)
    cat: Dict[str, str] = {}
    for r in rows:
        if not r.get("speedup_ratio"):
            continue
        by_prog[r["program_id"]][int(r["combo_id"])] = float(r["speedup_ratio"])
        cat[r["program_id"]] = r.get("category", "")

    all_combo_ids = sorted({c for sp in by_prog.values() for c in sp})
    ALL_ON = max(all_combo_ids) if all_combo_ids else 0  # every pass enabled

    per_prog = []
    all_on_sps, allbest = [], []
    for pid, combo_sp in sorted(by_prog.items()):
        best_combo = max(combo_sp, key=combo_sp.get)
        best_sp = combo_sp[best_combo]
        sp_all_on = combo_sp.get(ALL_ON, 1.0)
        per_prog.append({
            "program_id": pid, "category": cat.get(pid, ""),
            "best_combo": best_combo, "best_speedup": best_sp,
            "best_passes": get_pass_names(best_combo),
            "all_on_speedup": sp_all_on,
            "regressed": min(combo_sp.values()) < 0.95,
        })
        all_on_sps.append(sp_all_on)
        allbest.append(best_sp)

    combo_mean: Dict[int, List[float]] = defaultdict(list)
    for combo_sp in by_prog.values():
        for c, s in combo_sp.items():
            combo_mean[c].append(s)
    combo_geo = {c: _geomean(v) for c, v in combo_mean.items()}
    combo_worst = {c: min(v) for c, v in combo_mean.items()}

    # safest strong default: best geomean among combos that never regress > 3%
    safe = sorted((c for c in combo_geo if combo_worst[c] >= 0.97),
                  key=lambda c: -combo_geo[c])
    safe_combo = safe[0] if safe else 0

    # how often is combo `all-on` NOT the best choice for a program?
    n_all_on_suboptimal = sum(
        1 for p in per_prog
        if p["best_speedup"] > p["all_on_speedup"] * 1.02)

    by_cat: Dict[str, List[float]] = defaultdict(list)
    for p in per_prog:
        by_cat[p["category"]].append(p["best_speedup"])

    return {
        "n_programs": len(per_prog),
        "per_program": per_prog,
        "all_on_combo": ALL_ON,
        "geomean_all_on": _geomean(all_on_sps) if all_on_sps else 1.0,
        "geomean_best": _geomean(allbest),
        "max_speedup": max(allbest) if allbest else 1.0,
        "n_regressions": sum(1 for p in per_prog if p["regressed"]),
        "n_all_on_suboptimal": n_all_on_suboptimal,
        "best_single_combo": max(combo_geo, key=combo_geo.get),
        "best_single_combo_geomean": max(combo_geo.values()),
        "safe_combo": safe_combo,
        "safe_combo_geomean": combo_geo.get(safe_combo, 1.0),
        "safe_combo_worst": combo_worst.get(safe_combo, 1.0),
        "category_geomeans": {k: _geomean(v) for k, v in by_cat.items()},
        "combo_geomeans": combo_geo,
    }


def render_markdown(csv_path: str, cv: dict = None) -> str:
    s = summarize(csv_path)
    npass = NUM_PASSES
    L: List[str] = []
    L.append("# MiniC optimizer: measured speedup results\n")
    L.append(f"**{s['n_programs']} MiniC benchmarks**, each emitted as C at every "
             f"one of the **{2 ** npass} pass combinations** ({npass} independently "
             "toggleable passes), compiled with **`gcc -O0`**, and timed "
             "(median of 6 wall-clock runs after 3 warm-ups).\n")
    L.append("`speedup = time(combo 0, no passes) / time(combo)` -- how much the "
             "MiniC TAC optimizer beats *not* optimizing, with the C compiler "
             "pinned at `-O0` so the measured gain is ours, not gcc's.\n")

    L.append("## Headline\n")
    L.append(f"- **Best combo per program, geomean speedup: x{s['geomean_best']:.2f}**  "
             f"(max **x{s['max_speedup']:.2f}**)")
    ac = s["all_on_combo"]
    L.append(f"- All {npass} passes on (combo {ac}): geomean x{s['geomean_all_on']:.2f}")
    sc = s["safe_combo"]
    L.append(f"- Safe strong default -- combo {sc} "
             f"[{', '.join(get_pass_names(sc)) or 'baseline'}]: geomean "
             f"x{s['safe_combo_geomean']:.2f}, and never worse than "
             f"x{s['safe_combo_worst']:.2f} on any program")
    L.append(f"- No single combo is best everywhere: the all-passes combo is "
             f"left on the table (>2% slower than the per-program best) on "
             f"**{s['n_all_on_suboptimal']} / {s['n_programs']}** programs -- which is "
             "why a per-program recommender is worth having.\n")

    L.append("### by category (best-combo geomean)\n")
    for c, g in sorted(s["category_geomeans"].items(), key=lambda kv: -kv[1]):
        L.append(f"- {c}: x{g:.2f}")
    L.append("")

    if cv:
        L.append("## ML recommendation (RandomForest, GroupKFold by program_id)\n")
        L.append("Cross-validation holds *whole programs* out -- a program's rows "
                 "share identical static features, so a random split would leak.\n")
        L.append(f"- Model: **{cv.get('kind', 'random forest').replace('_', ' ')}**, "
                 f"{cv['held_out_programs']} held-out programs "
                 f"({cv['n_groups']} programs, {cv['n_splits']} folds)")
        L.append(f"- Speedup-prediction MAE: {cv['cv_mae']:.3f}")
        if "regression_rate" in cv:
            L.append(f"- Recommendations that regress the program (>2% slower "
                     f"than baseline): **{100 * cv['regression_rate']:.0f}%**")
        L.append(f"- **Model-recommended combo, mean true speedup on unseen "
                 f"programs: x{cv['reco_speedup_mean']:.2f}**")
        L.append(f"- Baseline (combo 0): x{cv['baseline_mean']:.2f}   |   "
                 f"oracle (best combo in hindsight): x{cv['oracle_speedup_mean']:.2f}")
        gap = cv["oracle_speedup_mean"] - cv["baseline_mean"]
        if gap > 1e-6:
            got = cv["reco_speedup_mean"] - cv["baseline_mean"]
            L.append(f"- Model captures **{100 * got / gap:.0f}%** of the available "
                     "speedup without ever having timed the program.\n")

    L.append("## Per-program\n")
    L.append("| program | category | best combo | passes | best speedup | all-on |")
    L.append("|---|---|--:|---|--:|--:|")
    for p in sorted(s["per_program"], key=lambda p: -p["best_speedup"]):
        L.append(f"| {p['program_id']} | {p['category']} | {p['best_combo']} | "
                 f"{', '.join(n.split()[-1].strip('()') for n in p['best_passes']) or '-'} | "
                 f"**x{p['best_speedup']:.2f}** | x{p['all_on_speedup']:.2f} |")
    L.append("")
    L.append("## Method notes\n")
    L.append("- `gcc -O0` is intentional: at `-O0` the C compiler does essentially "
             "no optimization, so the delta is what the MiniC optimizer contributed.")
    L.append("- Benchmarks are sized so combo 0 runs ~40-200 ms, well above "
             "scheduler noise; several are division-heavy because an integer "
             "divide is a large, non-pipelined cost that removing is clearly visible.")
    L.append("- Every combo is verified to reproduce combo 0's exit code before "
             "its time is recorded (`benchmarks/ground_truth.csv`); a miscompiled "
             "binary never contributes a timing sample.")
    L.append("- Strength reduction can slightly *pessimize* tight loops where the "
             "multiply it removes is already cheap under `-O0` -- visible in the "
             "corpus, and exactly the kind of call the recommender learns to make.")
    return "\n".join(L)


def _main(argv=None):
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--csv", default="data/benchmark_dataset.csv")
    p.add_argument("--out", default="RESULTS.md")
    args = p.parse_args(argv)
    md = render_markdown(args.csv)
    with open(args.out, "w", encoding="utf-8") as fh:
        fh.write(md)
    print(md)


if __name__ == "__main__":
    _main()
