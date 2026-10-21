"""Online recommendation: MiniC features -> recommended optimization combo.

Dispatches through the model's chosen strategy (argmax / abstain-margin /
per-pass classifiers); see ``SpeedupModel.select_combo``.
"""
import os
import warnings
from typing import Callable, List, Optional, Tuple

from .dataset import features_to_x
from .model import SpeedupModel
from ..optimizer.pass_manager import get_pass_names, NUM_COMBOS

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))))
DEFAULT_MODEL_PATH = os.path.join(REPO_ROOT, "data", "trained_model.pkl")
DEFAULT_DATASET = os.path.join(REPO_ROOT, "data", "benchmark_dataset.csv")


def load_or_train(model_path: str = DEFAULT_MODEL_PATH, csv_path: str = DEFAULT_DATASET,
                  log: Optional[Callable[[str], None]] = print) -> SpeedupModel:
    """Load the trained recommender, training a small one first if needed.

    The model file is not committed (pickles are tied to the scikit-learn version),
    so a fresh clone trains it once from the committed dataset: a HistGradientBoosting
    regressor with the abstain-margin strategy, ~15 s and ~2 MB. That is the
    configuration the full bake-off (``python run_experiment.py --skip-sweep``)
    selects as well.
    """
    if os.path.exists(model_path):
        try:
            from sklearn.exceptions import InconsistentVersionWarning
            with warnings.catch_warnings():
                # pickled with another scikit-learn version -> retrain rather than risk it
                warnings.simplefilter("error", InconsistentVersionWarning)
                return SpeedupModel.load(model_path)
        except Exception as e:  # noqa: BLE001
            if log:
                log(f"Saved model can't be used ({type(e).__name__}); retraining it.")
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"no dataset at {csv_path}: run the sweep first "
                                "(python minic.py experiment --full)")
    if log:
        log("Training the recommender from data/benchmark_dataset.csv "
            "(one-time, about 15 seconds)...")
    from .train import train_final
    return train_final(csv_path, model_path, kind="hist_gradient_boosting",
                       strategy="margin", margin=0.05)


def recommend_combo(feature_dict: dict, model: SpeedupModel,
                    combos=range(NUM_COMBOS)) -> Tuple[int, float, List[str]]:
    combo, pred = model.select_combo(feature_dict, combos)
    return combo, pred, get_pass_names(combo)


def rank_combos(feature_dict: dict, model: SpeedupModel, top: int = 5):
    scored = [
        (c, model.predict([features_to_x(feature_dict, c)])[0])
        for c in range(NUM_COMBOS)
    ]
    scored.sort(key=lambda t: -t[1])
    return scored[:top]
