"""ML recommendation pipeline (Person C)."""
import warnings

# Harmless scikit-learn/joblib interaction warning, raised once per tree by
# RandomForest(n_jobs=-1); it buries the bake-off output, so silence just this one.
warnings.filterwarnings("ignore", message=r".*sklearn\.utils\.parallel\.delayed.*")

from .dataset import load_dataset, features_to_x, X_COLUMNS
from .model import SpeedupModel, make_regressor
from .predictor import recommend_combo, rank_combos, load_or_train

__all__ = [
    "load_dataset", "features_to_x", "X_COLUMNS",
    "SpeedupModel", "make_regressor",
    "recommend_combo", "rank_combos", "load_or_train",
]
