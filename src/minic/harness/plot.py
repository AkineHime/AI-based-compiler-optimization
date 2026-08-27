"""Render the per-program speedup bar chart from the sweep CSV."""
import csv
from collections import defaultdict

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from .report import summarize


def plot_speedups(csv_path: str, out_png: str = "docs/speedups.png") -> str:
    import os
    os.makedirs(os.path.dirname(out_png) or ".", exist_ok=True)
    s = summarize(csv_path)
    progs = sorted(s["per_program"], key=lambda p: -p["best_speedup"])
    names = [p["program_id"] for p in progs]
    best = [p["best_speedup"] for p in progs]
    allon = [p["all_on_speedup"] for p in progs]

    fig, ax = plt.subplots(figsize=(11, 6.5))
    y = range(len(names))
    ax.barh([i + 0.2 for i in y], best, height=0.38, label="best combo",
            color="#2563eb")
    ax.barh([i - 0.2 for i in y], allon, height=0.38, label="all passes",
            color="#93c5fd")
    ax.axvline(1.0, color="#111", lw=1, ls="--")
    ax.set_yticks(list(y))
    ax.set_yticklabels(names)
    ax.set_xlabel("speedup vs. unoptimized baseline  (gcc -O0, higher is better)")
    ax.set_title(f"MiniC TAC optimizer speedup  "
                 f"(geomean best x{s['geomean_best']:.2f}, "
                 f"max x{s['max_speedup']:.2f})")
    ax.legend(loc="lower right")
    ax.set_xlim(0.9, max(2.4, max(best) + 0.2))
    for i, v in zip(y, best):
        ax.text(v + 0.02, i + 0.2, f"x{v:.2f}", va="center", fontsize=8)
    fig.tight_layout()
    fig.savefig(out_png, dpi=130)
    plt.close(fig)
    return out_png


if __name__ == "__main__":
    import sys
    print(plot_speedups(sys.argv[1] if len(sys.argv) > 1 else "data/benchmark_dataset.csv"))
