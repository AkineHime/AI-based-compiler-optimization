"""Nested aggregate l-values: arrays of structs, structs of structs, structs
containing arrays.  These lower to load / mutate-copy / store-back chains
(MiniC value semantics), and must round-trip under every optimization combo.
"""
import shutil
import tempfile
import unittest

from src.minic.optimizer import optimize_program
from src.minic.codegen import CEmitter
from src.minic.pipeline import source_to_tac, compile_and_run


PROGRAMS = {
    "array_of_structs": ("""
        struct Pt { int x; int y; };
        int main() {
            struct Pt ps[3];
            ps[0].x = 10; ps[0].y = 1;
            ps[1].x = 20; ps[1].y = 2;
            ps[2].x = 30; ps[2].y = 3;
            int s = 0;
            int i = 0;
            while (i < 3) { s = s + ps[i].x + ps[i].y; i = i + 1; }
            return s;
        }
    """, 66),
    "struct_of_structs": ("""
        struct I { int a; int b; };
        struct O { struct I lo; struct I hi; };
        int main() {
            struct O o;
            o.lo.a = 5; o.lo.b = 6;
            o.hi.a = 7; o.hi.b = 8;
            return o.lo.a + o.lo.b + o.hi.a + o.hi.b;
        }
    """, 26),
    "struct_with_array_field": ("""
        struct Buf { int data[4]; int n; };
        int main() {
            struct Buf b;
            b.n = 4;
            b.data[0] = 1; b.data[1] = 2; b.data[2] = 3; b.data[3] = 4;
            int s = 0;
            int i = 0;
            while (i < b.n) { s = s + b.data[i]; i = i + 1; }
            return s;
        }
    """, 10),
    "array_of_structs_2d_index": ("""
        struct Cell { int v; };
        int main() {
            struct Cell grid[2][2];
            grid[0][0].v = 1; grid[0][1].v = 2;
            grid[1][0].v = 3; grid[1][1].v = 4;
            return grid[0][0].v + grid[0][1].v + grid[1][0].v + grid[1][1].v;
        }
    """, 10),
}


@unittest.skipIf(shutil.which("gcc") is None, "gcc not on PATH")
class TestNestedAggregates(unittest.TestCase):
    def test_round_trip_all_combos(self):
        for name, (src, expected) in PROGRAMS.items():
            with self.subTest(program=name):
                tac = source_to_tac(src)
                workdir = tempfile.mkdtemp(prefix=f"minic_agg_{name}_")
                try:
                    bad = []
                    for combo in range(64):
                        c = CEmitter().emit(optimize_program(tac, combo))
                        res = compile_and_run(c, combo, workdir=workdir)
                        if not res.compiled:
                            bad.append(f"combo {combo}: compile error")
                        elif res.returncode != expected:
                            bad.append(f"combo {combo}: {res.returncode} != {expected}")
                    self.assertFalse(bad, f"[{name}] " + "; ".join(bad[:6]))
                finally:
                    shutil.rmtree(workdir, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
