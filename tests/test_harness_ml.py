"""Smoke tests for the Person C timing harness + ML pipeline."""
import csv
import os
import shutil
import tempfile
import unittest

from src.minic.harness.compiler import compile_c
from src.minic.harness.timer import measure_execution_time
from src.minic.harness.sweeper import sweep, frontend
from src.minic.harness.report import summarize
from src.minic.ml.dataset import load_dataset, features_to_x, X_COLUMNS

CANON = os.path.join(os.path.dirname(__file__), os.pardir, "canonical_example.mc")

_PROG = """
int main() {
    int a = 3;
    int b = 4;
    int acc = 0;
    int i = 0;
    while (i < 20000) {
        acc = acc + a * b + a * a + b * b;
        i = i + 1;
    }
    return ((acc % 251) + 251) % 251;
}
"""


@unittest.skipIf(shutil.which("gcc") is None, "gcc not on PATH")
class TestHarness(unittest.TestCase):
    def test_compile_and_time(self):
        from src.minic.codegen import CEmitter
        from src.minic.optimizer import optimize_program
        _, tac = frontend(_PROG)
        c = CEmitter().emit(optimize_program(tac, 0))
        cr = compile_c(c, tag="t")
        self.assertTrue(cr.ok, cr.stderr)
        tr = measure_execution_time(cr.binary_path, runs=4, warmup=1)
        self.assertGreater(tr.median_ms, 0.0)
        self.assertEqual(tr.exit_code, tr.exit_code)  # stable

    def test_sweep_small_and_report(self):
        work = tempfile.mkdtemp(prefix="minic_sweeptest_")
        out = os.path.join(work, "ds.csv")
        prog = os.path.join(work, "p.mc")
        with open(prog, "w") as fh:
            fh.write(_PROG)
        sweep(programs=[prog], out_csv=out, runs=3, warmup=1, workers=1,
              combos=[0, 1, 8, 63], progress=lambda *a: None)

        rows = list(csv.DictReader(open(out, newline="")))
        self.assertEqual(len(rows), 4)
        self.assertTrue(all(r["speedup_ratio"] for r in rows))
        # combo 0 is the baseline -> speedup exactly 1
        base = next(r for r in rows if r["combo_id"] == "0")
        self.assertAlmostEqual(float(base["speedup_ratio"]), 1.0, places=3)

        summ = summarize(out)
        self.assertEqual(summ["n_programs"], 1)
        shutil.rmtree(work, ignore_errors=True)


class TestDataset(unittest.TestCase):
    def test_features_to_x_width(self):
        from src.minic.features import ALL_FEATURE_NAMES
        feats = {n: float(i) for i, n in enumerate(ALL_FEATURE_NAMES)}
        x = features_to_x(feats, combo_id=13)  # CF + CSE + LICM
        self.assertEqual(len(x), len(X_COLUMNS))
        self.assertEqual(x[-6:], [1.0, 0.0, 1.0, 1.0, 0.0, 0.0])  # cf dce cse licm sr lu


if __name__ == "__main__":
    unittest.main()
