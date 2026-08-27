"""Build benchmarks/ground_truth.csv -- the authoritative expected exit code for
each benchmark, taken from the unoptimized (combo 0) build.  Every optimized
combo must reproduce it; the sweeper enforces that per row.
"""
import csv
import os
import subprocess

from .sweeper import discover_benchmarks, frontend
from .compiler import compile_c, cleanup
from ..optimizer import optimize_program
from ..codegen import CEmitter


def build(bench_root: str = "benchmarks",
          out_csv: str = "benchmarks/ground_truth.csv") -> str:
    rows = []
    for path in discover_benchmarks(bench_root):
        pid = os.path.splitext(os.path.basename(path))[0]
        _, tac = frontend(open(path, encoding="utf-8").read())
        cr = compile_c(CEmitter().emit(optimize_program(tac, 0)), tag=pid)
        if not cr.ok:
            rows.append({"program_id": pid, "expected_exit_code": "COMPILE_ERROR",
                         "source": os.path.relpath(path)})
            continue
        rc = subprocess.run([cr.binary_path], capture_output=True).returncode
        cleanup(cr.c_path, cr.binary_path)
        rows.append({"program_id": pid, "expected_exit_code": rc,
                     "source": os.path.relpath(path).replace("\\", "/")})

    with open(out_csv, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["program_id", "expected_exit_code", "source"])
        w.writeheader()
        w.writerows(rows)
    return out_csv


if __name__ == "__main__":
    p = build()
    print(f"wrote {p}")
    print(open(p).read())
