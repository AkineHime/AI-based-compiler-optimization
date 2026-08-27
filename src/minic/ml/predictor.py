"""Online recommendation: MiniC features -> recommended optimization combo.

Dispatches through the model's chosen strategy (argmax / abstain-margin /
per-pass classifiers); see ``SpeedupModel.select_combo``.
"""
from typing import List, Tuple

from .dataset import features_to_x
from .model import SpeedupModel
from ..optimizer.pass_manager import get_pass_names, NUM_COMBOS


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
