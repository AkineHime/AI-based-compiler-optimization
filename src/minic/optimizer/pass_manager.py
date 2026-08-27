import copy
from typing import List, Dict, Tuple
from ..ir.tac import TACProgram, TACFunction
from .constant_folding import constant_folding_pass
from .dce import dce_pass
from .cse import cse_pass
from .licm import licm_pass
from .strength_reduction import strength_reduction_pass
from ._util import program_global_names


PASS_FLAGS = {
    1: "Constant Folding (CF)",
    2: "Dead Code Elimination (DCE)",
    4: "Common Subexpression Elimination (CSE)",
    8: "Loop-Invariant Code Motion (LICM)",
    16: "Strength Reduction (SR)",
}


def get_pass_names(combo_mask: int) -> List[str]:
    """Return list of enabled pass names for a given 5-bit combo mask (0 to 63)."""
    names = []
    for bit, name in PASS_FLAGS.items():
        if combo_mask & bit:
            names.append(name)
    return names


class PassManager:
    """Orchestrates the 5 toggleable optimization passes over TAC IR."""

    def __init__(self, combo_mask: int = 0, global_names: frozenset = frozenset()):
        self.combo_mask = combo_mask
        self.global_names = global_names

    def optimize_function(self, func: TACFunction) -> TACFunction:
        """Apply enabled optimization passes in canonical order: CF -> CSE -> LICM -> SR -> DCE."""
        optimized = copy.deepcopy(func)
        mask = self.combo_mask
        g = self.global_names

        # 1. Constant Folding (Bit 0)
        if mask & 1:
            optimized = constant_folding_pass(optimized, g)

        # 2. Common Subexpression Elimination (Bit 2)
        if mask & 4:
            optimized = cse_pass(optimized, g)

        # 3. Loop-Invariant Code Motion (Bit 3)
        if mask & 8:
            optimized = licm_pass(optimized, g)

        # 4. Strength Reduction (Bit 4)
        if mask & 16:
            optimized = strength_reduction_pass(optimized)

        # 5. Dead Code Elimination (Bit 1 - run last as cleanup)
        if mask & 2:
            optimized = dce_pass(optimized, g)

        return optimized

    def optimize_program(self, program: TACProgram) -> TACProgram:
        """Apply optimizations to all functions in the TACProgram."""
        optimized_prog = copy.deepcopy(program)
        self.global_names = program_global_names(program)
        optimized_prog.functions = [self.optimize_function(f) for f in program.functions]
        return optimized_prog


def optimize_program(tac_prog: TACProgram, combo_mask: int) -> TACProgram:
    """Convenience function to optimize a TACProgram with a given 5-bit bitmask."""
    pm = PassManager(combo_mask)
    return pm.optimize_program(tac_prog)
