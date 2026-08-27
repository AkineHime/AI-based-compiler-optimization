"""Turn a sweep CSV into a human-readable results summary (the headline output)."""
import csv
import math
import statistics
from collections import defaultdict
from typing import Dict, List

from ..optimizer.pass_manager import get_pass_names


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

    per_prog = []
    all63, allbest = [], []
    for pid, combo_sp in sorted(by_prog.items()):
        best_combo = max(combo_sp, key=combo_sp.get)
        best_sp = combo_sp[best_combo]
        sp63 = combo_sp.get(63, 1.0)
        per_prog.append({
            "program_id": pid, "category": cat.get(pid, ""),
            "best_combo": best_combo, "best_speedup": best_sp,
            "best_passes": get_pass_names(best_combo),
            "all_on_speedup": sp63,
            "regressed": min(combo_sp.values()) < 0.95,
        })
        all63.append(sp63)
        allbest.append(best_sp)

    combo_mean: Dict[int, List[float]] = defaultdict(list)
    for combo_sp in by_prog.values():
        for c, s in combo_sp.items():
            combo_mean[c].append(s)
    combo_geo = {c: _geomean(v) for c, v in combo_mean.items()}

    return {
        "n_programs": len(per_prog),
        "per_program": per_prog,
        "geomean_all_on": _geomean(all63),
        "geomean_best": _geomean(allbest),
        "max_speedup": max(allbest) if allbest else 1.0,
        "n_regressions": sum(1 for p in per_prog if p["regressed"]),
        "best_single_combo": max(combo_geo, key=combo_geo.get),
        "best_single_combo_geomean": max(combo_geo.values()),
        "combo_geomeans": combo_geo,
    }


def render_markdown(csv_path: str, cv: dict = None) -> str:
    s = summarize(csv_path)
    L: List[str] = []
    L.append("# MiniC optimizer: measured speedup results\n")
    L.append(f"Corpus: **{s['n_programs']} MiniC benchmarks**. Each program is emitted "
             "as C at every one of the 64 optimization combos, compiled with "
             "`gcc -O0`, and timed (median wall-clock). Speedup is "
             "`time(combo 0) / time(combo)` -- i.e. how much our TAC optimizer "
             "beats *not* optimizing, with the C compiler held at `-O0`.\n")
    L.append("## Headline\n")
    L.append(f"- **Geomean speedup, all 5 passes on:** x{s['geomean_all_on']:.3f}")
    L.append(f"- **Geomean speedup, best combo per program:** x{s['geomean_best']:.3f}")
    L.append(f"- **Largest single speedup:** x{s['max_speedup']:.2f}")
    L.append(f"- **Programs regressed (any combo >5% slower than baseline):** {s['n_regressions']} / {s['n_programs']}")
    bc = s["best_single_combo"]
    L.append(f"- **Best fixed combo across the corpus:** {bc} "
             f"[{', '.join(get_pass_names(bc)) or 'baseline'}], geomean x{s['best_single_combo_geomean']:.3f}\n")
    if cv:
        L.append("## ML recommendation (GroupKFold, grouped by program_id)\n")
        L.append(f"- Held-out programs: {cv['held_out_programs']}  ({cv['n_groups']} programs, {cv['n_splits']} folds)")
        L.append(f"- Speedup-prediction MAE: {cv['cv_mae']:.4f}")
        L.append(f"- Model-recommended combo, mean true speedup: **x{cv['reco_speedup_mean']:.3f}**")
        L.append(f"- Oracle (best combo, hindsight): x{cv['oracle_speedup_mean']:.3f}")
        gap = cv["oracle_speedup_mean"] - cv["baseline_mean"]
        if gap > 1e-6:
            got = cv["reco_speedup_mean"] - cv["baseline_mean"]
            L.append(f"- Model captures **{100 * got / gap:.0f}%** of the available speedup on unseen programs\n")
    L.append("## Per-program\n")
    L.append("| program | category | best combo | passes | best speedup | all-on speedup |")
    L.append("|---|---|---|---|---|---|")
    for p in s["per_program"]:
        L.append(f"| {p['program_id']} | {p['category']} | {p['best_combo']} | "
                 f"{', '.join(p['best_passes']) or '-'} | "
                 f"**x{p['best_speedup']:.2f}** | x{p['all_on_speedup']:.2f} |")
    L.append("")
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
