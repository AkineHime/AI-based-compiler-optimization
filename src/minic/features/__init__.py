"""MiniC Static Feature Extractor."""

from .extractor import FeatureExtractor, FEATURE_NAMES
from .opportunity import extract_opportunity, OPPORTUNITY_NAMES

ALL_FEATURE_NAMES = FEATURE_NAMES + OPPORTUNITY_NAMES


def all_features(ast_prog, tac_prog) -> dict:
    """The full 27-value feature dict: 19 static metrics + 8 opportunity metrics."""
    d = FeatureExtractor().extract(ast_prog, tac_prog)
    d.update(extract_opportunity(tac_prog))
    return d


__all__ = [
    "FeatureExtractor", "FEATURE_NAMES",
    "extract_opportunity", "OPPORTUNITY_NAMES",
    "ALL_FEATURE_NAMES", "all_features",
]
