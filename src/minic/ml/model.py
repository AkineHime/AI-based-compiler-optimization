"""Model wrappers for speedup regression + a small bake-off harness."""
import pickle
from dataclasses import dataclass, field
from typing import Callable, Dict, List

from sklearn.ensemble import (
    RandomForestRegressor, HistGradientBoostingRegressor, ExtraTreesRegressor,
)


@dataclass
class SpeedupModel:
    regressor: object
    feature_names: List[str]
    metadata: dict = field(default_factory=dict)

    def predict(self, X):
        return list(self.regressor.predict(X))

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
