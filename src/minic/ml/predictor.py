"""Online recommendation: MiniC features -> predicted-best optimization combo."""
from typing import List, Tuple

from .dataset import features_to_x
from .model import SpeedupModel
from ..optimizer.pass_manager import get_pass_names, NUM_COMBOS


def recommend_combo(feature_dict: dict, model: SpeedupModel,
                    combos=range(NUM_COMBOS)) -> Tuple[int, float, List[str]]:
    best_combo, best_pred = 0, -1e9
    for c in combos:
        pred = model.predict([features_to_x(feature_dict, c)])[0]
        if pred > best_pred:
            best_pred, best_combo = pred, c
    return best_combo, best_pred, get_pass_names(best_combo)


def rank_combos(feature_dict: dict, model: SpeedupModel, top: int = 5):
    scored = [
        (c, model.predict([features_to_x(feature_dict, c)])[0])
        for c in range(NUM_COMBOS)
    ]
    scored.sort(key=lambda t: -t[1])
    return scored[:top]
