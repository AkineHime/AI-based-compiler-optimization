"""Load the sweep CSV into an ML-ready design matrix.

X = 19 static features + 5 flag bits ; y = speedup_ratio ; groups = program_id
(so GroupKFold can hold whole programs out).
"""
import csv
from dataclasses import dataclass
from typing import List, Tuple

from ..features.extractor import FEATURE_NAMES

FEATURE_COLUMNS = [f"f_{n}" for n in FEATURE_NAMES]
FLAG_COLUMNS = ["flag_cf", "flag_dce", "flag_cse", "flag_licm", "flag_sr"]
X_COLUMNS = FEATURE_COLUMNS + FLAG_COLUMNS
TARGET = "speedup_ratio"


@dataclass
class Dataset:
    X: List[List[float]]
    y: List[float]
    groups: List[str]
    combo_ids: List[int]
    feature_names: List[str]

    def __len__(self) -> int:
        return len(self.y)


def load_dataset(csv_path: str, drop_missing: bool = True) -> Dataset:
    X: List[List[float]] = []
    y: List[float] = []
    groups: List[str] = []
    combos: List[int] = []
    with open(csv_path, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            if drop_missing and not row.get(TARGET):
                continue
            try:
                xs = [float(row[c]) for c in X_COLUMNS]
                yy = float(row[TARGET])
            except (KeyError, ValueError):
                continue
            X.append(xs)
            y.append(yy)
            groups.append(row["program_id"])
            combos.append(int(row["combo_id"]))
    return Dataset(X, y, groups, combos, list(X_COLUMNS))


def features_to_x(feature_dict: dict, combo_id: int) -> List[float]:
    """Build one design-matrix row for online prediction."""
    flags = [
        1.0 if combo_id & 1 else 0.0,
        1.0 if combo_id & 2 else 0.0,
        1.0 if combo_id & 4 else 0.0,
        1.0 if combo_id & 8 else 0.0,
        1.0 if combo_id & 16 else 0.0,
    ]
    feats = [float(feature_dict[n]) for n in FEATURE_NAMES]
    return feats + flags
