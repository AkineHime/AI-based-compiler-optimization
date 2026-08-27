"""Regression tests for optimizer / codegen correctness bugs.

Each program is compiled and run under **all 64** optimization combos; combo 0
(no optimization) is the oracle and every other combo must produce the same
process exit code.  A divergence is a miscompilation, not timing noise.

Covers, specifically:
  * strength reduction seeding from a non-zero induction start,
  * LICM not hoisting a possibly-trapping divide out of a zero-trip loop,
  * constant folding respecting 32-bit wrap-around and C remainder sign,
  * globals surviving DCE / CSE / codegen (no local shadow).
"""
import shutil
import tempfile
import unittest

from src.minic.optimizer import optimize_program
from src.minic.codegen import CEmitter
from src.minic.pipeline import source_to_tac, compile_and_run


PROGRAMS = {
    "sr_nonzero_start": """
        int f(int n) {
            int total = 0;
            int i = 3;
            while (i < n) {
                int val = i * 4;
                total = total + val;
                i = i + 1;
            }
            return total;
        }
        int main() { return f(10); }
    """,
    "sr_for_loop": """
        int f(int n) {
            int total = 0;
            for (int i = 0; i < n; i = i + 1) {
                total = total + i * 7;
            }
            return total;
        }
        int main() { return f(12) % 250; }
    """,
    "sr_nested": """
        int f() {
            int acc = 0;
            int i = 1;
            while (i < 6) {
                int j = 2;
                while (j < 7) {
                    acc = acc + i * 3 + j * 5;
                    j = j + 1;
                }
                i = i + 1;
            }
            return acc % 200;
        }
        int main() { return f(); }
    """,
    "licm_div_zero_trip": """
        int f(int n, int z) {
            int s = 0;
            int i = 0;
            while (i < n) {
                int q = 100 / z;
                s = s + q;
                i = i + 1;
            }
            return s;
        }
        int main() { return f(0, 0) + 77; }
    """,
    "licm_invariant": """
        int f(int n, int k) {
            int s = 0;
            int i = 0;
            while (i < n) {
                int inv = k * 100 + 9;
                s = s + inv + i;
                i = i + 1;
            }
            return s % 251;
        }
        int main() { return f(30, 4); }
    """,
    "cf_int32_overflow": """
        int main() {
            int a = 100000;
            int b = a * a;
            int c = b % 1000;
            int d = (0 - 7) % 3;
            return c + d + 100;
        }
    """,
    "global_shared_across_calls": """
        int counter = 0;
        int bump() { counter = counter + 10; return counter; }
        int main() {
            int a = counter + 5;
            bump();
            bump();
            int b = counter + 5;
            return a + b;
        }
    """,
    "global_dead_looking_store": """
        int flag = 0;
        int arm() { flag = 1; return 0; }
        int main() {
            arm();
            return flag + 40;
        }
    """,
}


@unittest.skipIf(shutil.which("gcc") is None, "gcc not on PATH")
class TestPassRegressions(unittest.TestCase):
    def _sweep(self, name: str, source: str):
        tac = source_to_tac(source)
        workdir = tempfile.mkdtemp(prefix=f"minic_reg_{name}_")
        try:
            baseline = compile_and_run(CEmitter().emit(optimize_program(tac, 0)),
                                       0, workdir=workdir)
            self.assertTrue(baseline.compiled,
                            f"[{name}] baseline failed to compile:\n{baseline.compile_error}")
            oracle = baseline.returncode

            bad = []
            for combo in range(1, 64):
                c_src = CEmitter().emit(optimize_program(tac, combo))
                res = compile_and_run(c_src, combo, workdir=workdir)
                if not res.compiled:
                    bad.append(f"combo {combo}: compile error\n{res.compile_error.strip()}")
                elif res.returncode != oracle:
                    bad.append(f"combo {combo}: returned {res.returncode}, oracle {oracle}")
            self.assertFalse(bad, f"[{name}] {len(bad)} combo(s) diverged from the "
                                  f"unoptimized baseline ({oracle}):\n" + "\n".join(bad))
        finally:
            shutil.rmtree(workdir, ignore_errors=True)

    def test_programs(self):
        for name, src in PROGRAMS.items():
            with self.subTest(program=name):
                self._sweep(name, src)


if __name__ == "__main__":
    unittest.main()
