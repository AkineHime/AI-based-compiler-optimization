"""Automated feature-extraction + full pass-combo timing sweep over a benchmark corpus.

Produces ``data/benchmark_dataset.csv`` with one row per (program, combo):
the 27 features (19 static + 8 opportunity, identical across a program's rows), the 6 flag bits,
the timing, and the speedup vs. that program's combo-0 baseline.

Parallelism is *across programs* with a worker cap below the core count, and the
speedup basis is the **minimum** observed time (the least-interfered sample) --
both keep the numbers honest when several benchmarks time concurrently.
"""
import csv
import glob
import os
import shutil
import tempfile
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import Dict, List, Optional

from ..frontend.lexer import Lexer
from ..frontend.parser import Parser
from ..frontend.sema import SemanticAnalyzer
from ..ir.ir_generator import IRGenerator
from ..features import all_features, ALL_FEATURE_NAMES
from ..optimizer import optimize_program
from ..optimizer.pass_manager import NUM_COMBOS
from ..codegen import CEmitter
from .compiler import compile_c, cleanup
from .timer import measure_execution_time

FLAG_COLUMNS = ["flag_cf", "flag_dce", "flag_cse", "flag_licm", "flag_sr", "flag_lu"]
FLAG_BITS = {"flag_cf": 1, "flag_dce": 2, "flag_cse": 4,
             "flag_licm": 8, "flag_sr": 16, "flag_lu": 32}
FIELDNAMES = (["program_id", "category"]
              + [f"f_{n}" for n in ALL_FEATURE_NAMES]
              + ["combo_id"] + FLAG_COLUMNS
              + ["exit_code", "median_time_ms", "min_time_ms", "speedup_ratio"])


def _category(path: str) -> str:
    parts = os.path.normpath(path).split(os.sep)
    return parts[-2] if len(parts) >= 2 else "misc"


def discover_benchmarks(root: str = "benchmarks") -> List[str]:
    return sorted(glob.glob(os.path.join(root, "**", "*.mc"), recursive=True))


def frontend(source: str):
    tokens = Lexer(source).tokenize()
    ast = Parser(tokens, source).parse()
    SemanticAnalyzer(source).analyze(ast)
    tac = IRGenerator().generate(ast)
    return ast, tac


def _sweep_one(path: str, combos: List[int], runs: int, warmup: int) -> dict:
    pid = os.path.splitext(os.path.basename(path))[0]
    cat = _category(path)
    source = open(path, encoding="utf-8").read()
    try:
        ast, tac = frontend(source)
    except Exception as e:  # noqa: BLE001
        return {"pid": pid, "error": f"frontend: {e}", "rows": []}
    feats = all_features(ast, tac)

    workdir = tempfile.mkdtemp(prefix=f"minic_sw_{pid}_")
    baseline = None
    oracle_rc = None
    per_combo: Dict[int, tuple] = {}
    try:
        for combo in combos:
            c_src = CEmitter().emit(optimize_program(tac, combo))
            cr = compile_c(c_src, out_dir=workdir, tag=f"{pid}_{combo}")
            if not cr.ok:
                per_combo[combo] = (None, None, None)
                cleanup(cr.c_path)
                continue
            try:
                tr = measure_execution_time(cr.binary_path, expected_exit_code=oracle_rc,
                                            runs=runs, warmup=warmup, timeout=60.0)
            except RuntimeError:
                per_combo[combo] = (None, None, None)
                cleanup(cr.c_path, cr.binary_path)
                continue
            if oracle_rc is None:
                oracle_rc = tr.exit_code
            if combo == 0:
                baseline = tr.min_ms
            per_combo[combo] = (tr.median_ms, tr.min_ms, tr.exit_code)
            cleanup(cr.c_path, cr.binary_path)
    finally:
        shutil.rmtree(workdir, ignore_errors=True)

    rows = []
    for combo in combos:
        med, mn, rc = per_combo.get(combo, (None, None, None))
        row = {"program_id": pid, "category": cat}
        for n in ALL_FEATURE_NAMES:
            row[f"f_{n}"] = feats[n]
        row["combo_id"] = combo
        for col in FLAG_COLUMNS:
            row[col] = 1 if combo & FLAG_BITS[col] else 0
        row["exit_code"] = rc if rc is not None else ""
        row["median_time_ms"] = f"{med:.4f}" if med is not None else ""
        row["min_time_ms"] = f"{mn:.4f}" if mn is not None else ""
        row["speedup_ratio"] = (f"{baseline / mn:.4f}"
                                if (mn and baseline) else "")
        rows.append(row)

    best = min((mn for _, mn, _ in per_combo.values() if mn), default=None)
    return {
        "pid": pid, "error": None, "rows": rows,
        "baseline_ms": baseline, "best_ms": best,
        "speedup": (baseline / best) if (baseline and best) else 1.0,
    }


def sweep(bench_root: str = "benchmarks",
          out_csv: str = "data/benchmark_dataset.csv",
          runs: int = 12, warmup: int = 3,
          combos: Optional[List[int]] = None,
          programs: Optional[List[str]] = None,
          workers: Optional[int] = None,
          progress=print) -> str:
    combos = list(range(NUM_COMBOS)) if combos is None else combos
    paths = programs if programs is not None else discover_benchmarks(bench_root)
    if not paths:
        raise SystemExit(f"no .mc benchmarks found under {bench_root!r}")
    if workers is None:
        workers = max(1, min(8, (os.cpu_count() or 2) // 2))

    os.makedirs(os.path.dirname(out_csv) or ".", exist_ok=True)
    t0 = time.time()
    all_rows: List[Dict] = []
    done = 0

    def note(res):
        nonlocal done
        done += 1
        if res["error"]:
            progress(f"[{done}/{len(paths)}] {res['pid']:22s} ERROR {res['error']}")
        else:
            b, k, s = res.get("baseline_ms"), res.get("best_ms"), res.get("speedup", 1.0)
            progress(f"[{done}/{len(paths)}] {res['pid']:22s} "
                     f"baseline={b:8.2f}ms best={k:8.2f}ms  x{s:.3f}  "
                     f"({time.time() - t0:.0f}s)")
        all_rows.extend(res["rows"])

    if workers == 1:
        for p in paths:
            note(_sweep_one(p, combos, runs, warmup))
    else:
        with ProcessPoolExecutor(max_workers=workers) as ex:
            futs = {ex.submit(_sweep_one, p, combos, runs, warmup): p for p in paths}
            for fut in as_completed(futs):
                note(fut.result())

    all_rows.sort(key=lambda r: (r["program_id"], r["combo_id"]))
    with open(out_csv, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDNAMES)
        w.writeheader()
        w.writerows(all_rows)
    progress(f"\nwrote {len(all_rows)} rows -> {out_csv}  "
             f"({time.time() - t0:.0f}s total, {workers} workers)")
    return out_csv


def _main(argv=None):
    import argparse
    p = argparse.ArgumentParser(description="MiniC pass-combo timing sweep")
    p.add_argument("--bench-root", default="benchmarks")
    p.add_argument("--out", default="data/benchmark_dataset.csv")
    p.add_argument("--runs", type=int, default=15)
    p.add_argument("--warmup", type=int, default=4)
    p.add_argument("--workers", type=int, default=None)
    p.add_argument("--combos", default="", help="comma list; default all 64")
    args = p.parse_args(argv)
    combos = [int(x) for x in args.combos.split(",")] if args.combos else None
    sweep(args.bench_root, args.out, args.runs, args.warmup, combos,
          workers=args.workers)


if __name__ == "__main__":
    _main()
