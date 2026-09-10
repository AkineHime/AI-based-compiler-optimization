"""Sanity checks for the multi-model comparison plumbing (no training)."""
import os
import unittest

import numpy as np

from src.minic.harness.sweeper import frontend
from src.minic.ml.sequences import tokenize_tac, VOCAB, VOCAB_SIZE, PAD, MAX_LEN

CANON = os.path.join(os.path.dirname(__file__), os.pardir, "canonical_example.mc")


class TestSequences(unittest.TestCase):
    def test_tokenize(self):
        _ast, tac = frontend(open(CANON, encoding="utf-8").read())
        toks = tokenize_tac(tac, MAX_LEN)
        self.assertGreater(len(toks), 20)
        self.assertLessEqual(len(toks), MAX_LEN)
        self.assertTrue(all(0 <= t < VOCAB_SIZE for t in toks))
        self.assertEqual(VOCAB[toks[0]], "<func>")
        self.assertEqual(PAD, 0)

    def test_truncation(self):
        _ast, tac = frontend(open(CANON, encoding="utf-8").read())
        self.assertEqual(len(tokenize_tac(tac, 40)), 40)


class TestModelSpecs(unittest.TestCase):
    def test_registry(self):
        from src.minic.ml.models_compare import MODEL_SPECS, TORCH_MODELS
        for name in ("linear", "random_forest", "hist_gradient_boosting",
                     "mlp", "cnn1d", "gru", "cnn1d_hybrid", "gru_hybrid"):
            self.assertIn(name, MODEL_SPECS)
        self.assertEqual(MODEL_SPECS["linear"], "tabular")
        self.assertEqual(MODEL_SPECS["cnn1d"], "sequence")
        self.assertIn("gru", TORCH_MODELS)
        self.assertNotIn("linear", TORCH_MODELS)

    def test_torch_nets_build(self):
        from src.minic.ml.models_torch import _build
        for k in ("mlp", "cnn1d", "gru", "cnn1d_hybrid", "gru_hybrid"):
            net = _build(k, 27)
            self.assertGreater(sum(p.numel() for p in net.parameters()), 100)

    def test_best_config_prefers_low_regression(self):
        from src.minic.ml.models_compare import best_config
        r = {"reco_speedup_mean": 1.30, "capture": 0.6, "regression_rate": 0.25,
             "by_margin": {0.12: {"reco_speedup_mean": 1.22, "capture": 0.45,
                                  "regression_rate": 0.05}}}
        bc = best_config(r)
        self.assertEqual(bc["margin"], 0.12)  # 25% regress at m=0 is over the cap


class TestProgramArrays(unittest.TestCase):
    def test_shapes(self):
        # a 3-program, 4-combo synthetic Dataset
        from src.minic.ml.dataset import Dataset, X_COLUMNS
        from src.minic.ml.models_compare import to_program_arrays
        rows_X, rows_y, groups, combos = [], [], [], []
        for p in range(3):
            for c in (0, 1, 2, 3):
                rows_X.append([float(p)] * len(X_COLUMNS))
                rows_y.append(1.0 + 0.1 * c)
                groups.append(f"p{p}")
                combos.append(c)
        ds = Dataset(rows_X, rows_y, groups, combos, list(X_COLUMNS))
        pa = to_program_arrays(ds, None)
        self.assertEqual(pa["feats"].shape, (3, 27))
        self.assertEqual(pa["speedup"].shape, (3, 64))
        self.assertTrue(pa["mask"][:, :4].all())
        self.assertFalse(pa["mask"][:, 4:].any())


if __name__ == "__main__":
    unittest.main()
