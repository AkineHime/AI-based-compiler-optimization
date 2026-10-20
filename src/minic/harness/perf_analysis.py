"""Performance analysis of the sweep: how the 6 passes actually behave on real hardware.

    python -m src.minic.harness.perf_analysis                       # -> PERF_ANALYSIS.md
    python -m src.minic.harness.perf_analysis data/benchmark_dataset.csv -o PERF_ANALYSIS.md

Answers the questions a cost model would have to get right, straight from the
57,600 timed configurations:
  * what does each pass buy on its own vs. averaged over every other-pass context?
  * are pass effects additive (could you predict the all-on speedup from singles)?
  * how much search does it take to find a good combo without a model?
  * how noisy is the measurement itself?
"""
import argparse
import math

import numpy as np
import pandas as pd

from ..optimizer.pass_manager import PASS_ABBR, NUM_PASSES


def _gm(x) -> float:
    return float(np.exp(np.mean(np.log(x))))


def _greedy(row: np.ndarray):
    """Greedy forward selection on measured speedups; returns (combo, timed runs used)."""
    cur, runs = 0, 1
    while True:
        cand = [cur | (1 << i) for i in range(NUM_PASSES) if not cur & (1 << i)]
        if not cand:
            return cur, runs
        runs += len(cand)
        nxt = max(cand, key=lambda c: row[c])
        if row[nxt] <= row[cur]:
            return cur, runs
        cur = nxt


def analyse(csv_path: str) -> dict:
    d = pd.read_csv(csv_path)
    t = d.pivot_table(index="program_id", columns="combo_id", values="min_time_ms")
    n_combos = 1 << NUM_PASSES
    names = [PASS_ABBR[1 << i] for i in range(NUM_PASSES)]

    passes = []
    for i, name in enumerate(names):
        bit = 1 << i
        # log-speedup of adding this pass, for every context (combo without it) x program
        r = np.array([np.log(t[c] / t[c | bit]) for c in range(n_combos) if not c & bit])
        per_prog = np.exp(r.mean(0))
        per_ctx = np.exp(r.mean(1))
        passes.append({
            "name": name,
            "alone": _gm(t[0] / t[bit]),
            "marginal": float(np.exp(r.mean())),
            "ctx_lo": float(per_ctx.min()), "ctx_hi": float(per_ctx.max()),
            "helps": float((per_prog > 1.02).mean()), "hurts": float((per_prog < 0.98).mean()),
        })

    pred = np.prod([t[0] / t[1 << i] for i in range(NUM_PASSES)], axis=0)
    act = t[0] / t[n_combos - 1]
    err = np.abs(np.log(pred / act))

    sp = t[0].values[:, None] / t.values
    best = sp.max(1)
    g = [_greedy(sp[k]) for k in range(len(sp))]
    g_sp = np.array([sp[k, c] for k, (c, _) in enumerate(g)])

    noise = d.median_time_ms / d.min_time_ms
    return {
        "n_programs": len(t), "n_configs": len(d),
        "base_ms": (float(t[0].min()), float(t[0].median()), float(t[0].max())),
        "passes": passes,
        "additive_pred": _gm(pred), "additive_actual": _gm(act),
        "additive_med_err": math.exp(float(np.median(err))) - 1,
        "additive_off10": int((err > math.log(1.1)).sum()),
        "oracle": _gm(best), "all_on": _gm(sp[:, n_combos - 1]), "greedy": _gm(g_sp),
        "oracle_mean": float(best.mean()), "all_on_mean": float(sp[:, n_combos - 1].mean()),
        "greedy_mean": float(g_sp.mean()), "greedy_runs": float(np.mean([r for _, r in g])),
        "greedy_miss": int((g_sp < best / 1.02).sum()),
        "regress_frac": float((sp[:, 1:] < 0.98).mean()),
        "noise_med": float(noise.median()), "noise_p95": float(noise.quantile(0.95)),
    }


def render_markdown(a: dict) -> str:
    n = a["n_programs"]
    lo, med, hi = a["base_ms"]
    out = [
        "# Performance analysis: how the passes behave on real hardware",
        "",
        f"Computed from **{a['n_configs']:,} timed configurations** ({n} programs x 64 pass combos, "
        f"`gcc -O0`, least of 15 runs). Unoptimized run time per program: {lo:.1f}-{hi:.1f} ms "
        f"(median {med:.1f} ms). Regenerate with `python -m src.minic.harness.perf_analysis`.",
        "",
        "## 1. Per-pass effect: alone vs. in context",
        "",
        "*alone* = geomean speedup of enabling only that pass. *marginal* = geomean speedup of adding it, "
        "averaged over all 32 contexts of the other five passes. *context range* = the spread of that "
        "marginal across contexts. *helps / hurts* = share of programs where adding the pass is >2% "
        "faster / slower on average.",
        "",
        "| pass | alone | marginal | context range | helps | hurts |",
        "|---|--:|--:|--:|--:|--:|",
    ]
    for p in a["passes"]:
        out.append(f"| {p['name']} | x{p['alone']:.3f} | x{p['marginal']:.3f} | "
                   f"x{p['ctx_lo']:.3f} - x{p['ctx_hi']:.3f} | {p['helps']:.0%} | {p['hurts']:.0%} |")
    out += [
        "",
        "## 2. Pass effects are not additive",
        "",
        f"Multiplying the six single-pass speedups predicts an all-on geomean of "
        f"**x{a['additive_pred']:.3f}**; the measured all-on geomean is **x{a['additive_actual']:.3f}**. "
        f"Per program, the additive model is off by a median of {a['additive_med_err']:.0%} and by more "
        f"than 10% on **{a['additive_off10']} / {n}** programs. Passes enable each other "
        "(CSE and constant folding create the dead code DCE removes), so a per-pass cost model is the "
        "wrong shape. The recommender instead scores whole (program, combo) pairs.",
        "",
        "## 3. Cost of finding a good combo",
        "",
        "| strategy | timed runs per program | mean speedup | geomean speedup |",
        "|---|--:|--:|--:|",
        "| no passes | 1 | x1.000 | x1.000 |",
        f"| all 6 passes | 1 | x{a['all_on_mean']:.3f} | x{a['all_on']:.3f} |",
        "| ML recommender, held-out programs (RESULTS.md) | **0** | x1.21 | - |",
        f"| greedy forward search on the real clock | {a['greedy_runs']:.1f} | x{a['greedy_mean']:.3f} | x{a['greedy']:.3f} |",
        f"| exhaustive search (oracle) | 64 | x{a['oracle_mean']:.3f} | x{a['oracle']:.3f} |",
        "",
        f"Greedy search still misses the best combo by >2% on {a['greedy_miss']} / {n} programs, and "
        f"**{a['regress_frac']:.0%} of all non-empty configurations are >2% slower than doing nothing**. "
        "Picking blindly is risky, and that is why the recommender is allowed to abstain.",
        "",
        "## 4. Measurement noise",
        "",
        f"Median-of-15 / min-of-15 run time: median ratio **{a['noise_med']:.3f}**, 95th percentile "
        f"**{a['noise_p95']:.3f}**. The sweep runs 8 programs in parallel, so the median carries "
        "10-40% interference. The harness therefore records the *minimum* (least-interfered) sample "
        "after 4 warm-ups, and only after the binary's exit code matches the unoptimized build.",
        "",
    ]
    return "\n".join(out)


def _main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("csv", nargs="?", default="data/benchmark_dataset.csv")
    ap.add_argument("-o", "--out", default="PERF_ANALYSIS.md")
    args = ap.parse_args(argv)
    md = render_markdown(analyse(args.csv))
    with open(args.out, "w", encoding="utf-8", newline="\n") as f:
        f.write(md)
    print(f"wrote {args.out}")


if __name__ == "__main__":
    _main()
