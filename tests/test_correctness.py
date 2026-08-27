"""Regression: every one of the 64 optimization combinations, compiled with
``gcc -O0``, must reproduce the canonical program's result exactly (83).

A combination that yields anything else is a *pass bug*, not timing noise --
this test names the offending combos rather than glossing over them.
"""
import os
import shutil
import tempfile
import unittest

from src.minic.optimizer import NUM_COMBOS, combo_label
from src.minic.pipeline import source_to_c, compile_and_run

EXPECTED = 83
_HERE = os.path.dirname(__file__)
_CANONICAL = os.path.join(_HERE, os.pardir, "canonical_example.mc")


def _load_canonical() -> str:
    with open(_CANONICAL, "r", encoding="utf-8") as fh:
        return fh.read()


@unittest.skipIf(shutil.which("gcc") is None, "gcc not on PATH")
class TestAll64Combos(unittest.TestCase):
    def test_every_combo_returns_83(self):
        source = _load_canonical()
        workdir = tempfile.mkdtemp(prefix="minic_correctness_")
        failures = []
        try:
            for combo in range(NUM_COMBOS):
                c_src = source_to_c(source, combo)
                res = compile_and_run(c_src, combo, workdir=workdir)
                if not res.compiled:
                    failures.append(
                        f"{combo_label(combo)}: COMPILE FAILED\n"
                        + res.compile_error.strip())
                elif res.returncode != EXPECTED:
                    failures.append(
                        f"{combo_label(combo)}: returned {res.returncode}, "
                        f"expected {EXPECTED}")
        finally:
            shutil.rmtree(workdir, ignore_errors=True)

        if failures:
            self.fail(f"{len(failures)}/{NUM_COMBOS} combos broke correctness:\n"
                      + "\n".join(failures))


if __name__ == "__main__":
    unittest.main()
