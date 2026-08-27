"""Thin wrapper around the speedup-regression model + its persistence."""
import pickle
from dataclasses import dataclass, field
from typing import List, Optional

from sklearn.ensemble import RandomForestRegressor


@dataclass
class SpeedupModel:
    regressor: RandomForestRegressor
    feature_names: List[str]
    metadata: dict = field(default_factory=dict)

    def predict(self, X: List[List[float]]) -> List[float]:
        return list(self.regressor.predict(X))

    def save(self, path: str) -> None:
        with open(path, "wb") as fh:
            pickle.dump(self, fh)

    @staticmethod
    def load(path: str) -> "SpeedupModel":
        with open(path, "rb") as fh:
            return pickle.load(fh)


def make_regressor(n_estimators: int = 300, random_state: int = 0) -> RandomForestRegressor:
    return RandomForestRegressor(
        n_estimators=n_estimators,
        max_depth=None,
        min_samples_leaf=2,
        random_state=random_state,
        n_jobs=-1,
    )
