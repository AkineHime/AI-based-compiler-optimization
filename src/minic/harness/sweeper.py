"""Automated feature-extraction + full pass-combo timing sweep over a benchmark corpus.

Produces ``data/benchmark_dataset.csv`` with one row per (program, combo):
the 19 static features (identical across a program's rows), the 5 flag bits,
the median wall-clock time, and the speedup vs. that program's combo-0 baseline.
"""
import csv
import glob
import os
import shutil
import sys
import tempfile
import time
from typing import Dict, List, Optional

from ..frontend.lexer import Lexer
from ..frontend.parser import Parser
from ..frontend.sema import SemanticAnalyzer
from ..ir.ir_generator import IRGenerator
from ..features.extractor import FeatureExtractor, FEATURE_NAMES
from ..optimizer import optimize_program
from ..optimizer.pass_manager import PASS_FLAGS, NUM_COMBOS
from ..codegen import CEmitter
from .compiler import compile_c, cleanup
from .timer import measure_execution_time

FLAG_COLUMNS = ["flag_cf", "flag_dce", "flag_cse", "flag_licm", "flag_sr"]
FLAG_BITS = {"flag_cf": 1, "flag_dce": 2, "flag_cse": 4, "flag_licm": 8, "flag_sr": 16}


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


def sweep(bench_root: str = "benchmarks",
          out_csv: str = "data/benchmark_dataset.csv",
          runs: int = 12, warmup: int = 3,
          combos: Optional[List[int]] = None,
          programs: Optional[List[str]] = None,
          progress=print) -> str:
    combos = list(range(NUM_COMBOS)) if combos is None else combos
    paths = programs if programs is not None else discover_benchmarks(bench_root)
    if not paths:
        raise SystemExit(f"no .mc benchmarks found under {bench_root!r}")

    os.makedirs(os.path.dirname(out_csv) or ".", exist_ok=True)
    workdir = tempfile.mkdtemp(prefix="minic_sweep_")
    rows: List[Dict] = []
    t_start = time.time()

    try:
        for pi, path in enumerate(paths, 1):
            pid = os.path.splitext(os.path.basename(path))[0]
            cat = _category(path)
            source = open(path, encoding="utf-8").read()
            try:
                ast, tac = frontend(source)
            except Exception as e:  # noqa: BLE001
                progress(f"[{pi}/{len(paths)}] {pid}: FRONTEND ERROR {e}")
                continue
            feats = FeatureExtractor().extract(ast, tac)

            baseline_ms = None
            oracle_rc = None
            per_combo = {}
            for combo in combos:
                c_src = CEmitter().emit(optimize_program(tac, combo))
                cr = compile_c(c_src, out_dir=workdir, tag=f"{pid}_{combo}")
                if not cr.ok:
                    progress(f"[{pi}/{len(paths)}] {pid} combo {combo}: COMPILE FAIL")
                    per_combo[combo] = (None, None)
                    cleanup(cr.c_path)
                    continue
                try:
                    tr = measure_execution_time(
                        cr.binary_path,
                        expected_exit_code=oracle_rc,
                        runs=runs, warmup=warmup)
                except RuntimeError as e:
                    progress(f"[{pi}/{len(paths)}] {pid} combo {combo}: {e}")
                    per_combo[combo] = (None, None)
                    cleanup(cr.c_path, cr.binary_path)
                    continue
                if oracle_rc is None:
                    oracle_rc = tr.exit_code
                if combo == 0:
                    baseline_ms = tr.median_ms
                per_combo[combo] = (tr.median_ms, tr.exit_code)
                cleanup(cr.c_path, cr.binary_path)

            for combo in combos:
                med, rc = per_combo.get(combo, (None, None))
                row = {"program_id": pid, "category": cat}
                for name in FEATURE_NAMES:
                    row[f"f_{name}"] = feats[name]
                row["combo_id"] = combo
                for col in FLAG_COLUMNS:
                    row[col] = 1 if combo & FLAG_BITS[col] else 0
                row["exit_code"] = rc if rc is not None else ""
                row["median_time_ms"] = f"{med:.4f}" if med is not None else ""
                if med is not None and baseline_ms:
                    row["speedup_ratio"] = f"{baseline_ms / med:.4f}"
                else:
                    row["speedup_ratio"] = ""
                rows.append(row)

            if baseline_ms is not None:
                best = min((m for m, _ in per_combo.values() if m), default=None)
                sp = (baseline_ms / best) if best else 1.0
                progress(f"[{pi}/{len(paths)}] {pid:22s} baseline={baseline_ms:8.2f}ms "
                         f"best={best:8.2f}ms  speedup x{sp:.3f}  "
                         f"({time.time() - t_start:.0f}s elapsed)")
    finally:
        shutil.rmtree(workdir, ignore_errors=True)

    fieldnames = (["program_id", "category"]
                  + [f"f_{n}" for n in FEATURE_NAMES]
                  + ["combo_id"] + FLAG_COLUMNS
                  + ["exit_code", "median_time_ms", "speedup_ratio"])
    with open(out_csv, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)
    progress(f"\nwrote {len(rows)} rows -> {out_csv}  "
             f"({time.time() - t_start:.0f}s total)")
    return out_csv


def _main(argv=None):
    import argparse
    p = argparse.ArgumentParser(description="MiniC pass-combo timing sweep")
    p.add_argument("--bench-root", default="benchmarks")
    p.add_argument("--out", default="data/benchmark_dataset.csv")
    p.add_argument("--runs", type=int, default=12)
    p.add_argument("--warmup", type=int, default=3)
    p.add_argument("--combos", default="", help="comma list; default all 32")
    args = p.parse_args(argv)
    combos = [int(x) for x in args.combos.split(",")] if args.combos else None
    sweep(args.bench_root, args.out, args.runs, args.warmup, combos)


if __name__ == "__main__":
    _main()
