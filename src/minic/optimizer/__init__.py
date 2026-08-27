"""MiniC optimization pass library (Person B).

Five independently toggleable passes over the existing TAC IR, orchestrated by a
5-flag :class:`PassManager` that can run any of the 64 combinations in one fixed
canonical order.
"""
from .pass_manager import (
    PassManager, optimize, combo_flags, combo_label,
    FLAG_CF, FLAG_DCE, FLAG_CSE, FLAG_LICM, FLAG_SR, NUM_COMBOS,
)

__all__ = [
    "PassManager", "optimize", "combo_flags", "combo_label",
    "FLAG_CF", "FLAG_DCE", "FLAG_CSE", "FLAG_LICM", "FLAG_SR", "NUM_COMBOS",
]
