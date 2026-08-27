"""Model wrappers for speedup regression + a small bake-off harness."""
import pickle
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional

from sklearn.ensemble import (
    RandomForestRegressor, HistGradientBoostingRegressor, ExtraTreesRegressor,
    HistGradientBoostingClassifier,
)


@dataclass
class SpeedupModel:
    regressor: object
    feature_names: List[str]
    metadata: dict = field(default_factory=dict)
    pass_classifiers: Optional[list] = None  # 6 per-pass clfs (or int consts)

    def predict(self, X):
        return list(self.regressor.predict(X))

    # -- recommendation ---------------------------------------------------- #
    def select_combo(self, feature_dict: dict, combos=None):
        """Apply the model's chosen strategy -> (combo_id, predicted_speedup).
        ``predicted_speedup`` is the regressor's estimate for the picked combo
        (still meaningful under per_pass -- it's just not what drove the pick)."""
        from .dataset import FLAG_BITS, features_to_x
        from ..optimizer.pass_manager import NUM_COMBOS

        strategy = self.metadata.get("strategy", "argmax")
        n_static = self.metadata.get("n_static") or (
            len(self.feature_names) - len(FLAG_BITS))

        if strategy == "per_pass" and self.pass_classifiers:
            row = features_to_x(feature_dict, 0)[:n_static]
            bits = 0
            for b, clf in enumerate(self.pass_classifiers):
                on = clf if isinstance(clf, int) else int(clf.predict([row])[0])
                if on:
                    bits |= FLAG_BITS[b]
            pred = self.predict([features_to_x(feature_dict, bits)])[0]
            return bits, float(pred)

        combos = range(NUM_COMBOS) if combos is None else combos
        best_c, best_p = 0, -1e9
        for c in combos:
            p = self.predict([features_to_x(feature_dict, c)])[0]
            if p > best_p:
                best_p, best_c = p, c
        margin = float(self.metadata.get("margin", 0.0) or 0.0)
        if margin and best_p < 1.0 + margin:
            return 0, float(best_p)
        return best_c, float(best_p)

    def save(self, path: str) -> None:
        with open(path, "wb") as fh:
            pickle.dump(self, fh)

    @staticmethod
    def load(path: str) -> "SpeedupModel":
        with open(path, "rb") as fh:
            return pickle.load(fh)


def _rf(rs=0):
    return RandomForestRegressor(n_estimators=400, min_samples_leaf=2,
                                 random_state=rs, n_jobs=-1)


def _et(rs=0):
    return ExtraTreesRegressor(n_estimators=500, min_samples_leaf=2,
                               random_state=rs, n_jobs=-1)


def _hgb(rs=0):
    return HistGradientBoostingRegressor(
        max_iter=600, learning_rate=0.05, max_leaf_nodes=31,
        l2_regularization=0.1, early_stopping=False, random_state=rs)


REGRESSORS: Dict[str, Callable] = {
    "random_forest": _rf,
    "extra_trees": _et,
    "hist_gradient_boosting": _hgb,
}


def make_regressor(kind: str = "random_forest", random_state: int = 0):
    return REGRESSORS.get(kind, _rf)(random_state)


def make_classifier(random_state: int = 0):
    """Per-pass 'should this pass be on?' classifier (small per-program table)."""
    return HistGradientBoostingClassifier(
        max_iter=300, learning_rate=0.06, max_leaf_nodes=15,
        l2_regularization=0.2, early_stopping=False, random_state=random_state)
