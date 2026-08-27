"""Load the sweep CSV into an ML-ready design matrix.

X = 19 static features + 6 pass-flag bits ; y = speedup_ratio ; groups = program_id
(so GroupKFold can hold whole programs out).
"""
import csv
from dataclasses import dataclass
from typing import List, Tuple

from ..features.extractor import FEATURE_NAMES
from ..optimizer.pass_manager import PASS_ABBR

FEATURE_COLUMNS = [f"f_{n}" for n in FEATURE_NAMES]
FLAG_COLUMNS = [f"flag_{ab.lower()}" for _bit, ab in sorted(PASS_ABBR.items())]
FLAG_BITS = sorted(PASS_ABBR)   # [1, 2, 4, 8, 16, 32]
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
    feats = [float(feature_dict[n]) for n in FEATURE_NAMES]
    flags = [1.0 if combo_id & bit else 0.0 for bit in FLAG_BITS]
    return feats + flags
