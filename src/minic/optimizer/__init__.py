"""MiniC 5-Bit Optimization Engine Package."""

from .constant_folding import constant_folding_pass
from .dce import dce_pass
from .cse import cse_pass
from .licm import licm_pass
from .strength_reduction import strength_reduction_pass
from .pass_manager import PassManager, optimize_program, get_pass_names, PASS_FLAGS

__all__ = [
    "constant_folding_pass",
    "dce_pass",
    "cse_pass",
    "licm_pass",
    "strength_reduction_pass",
    "PassManager",
    "optimize_program",
    "get_pass_names",
    "PASS_FLAGS",
]
