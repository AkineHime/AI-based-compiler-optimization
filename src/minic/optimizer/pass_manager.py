import copy
from typing import List, Dict, Tuple
from ..ir.tac import TACProgram, TACFunction
from .constant_folding import constant_folding_pass
from .dce import dce_pass
from .cse import cse_pass
from .licm import licm_pass
from .strength_reduction import strength_reduction_pass
from .loop_unroll import loop_unroll_pass
from ._util import program_global_names


PASS_FLAGS = {
    1: "Constant Folding (CF)",
    2: "Dead Code Elimination (DCE)",
    4: "Common Subexpression Elimination (CSE)",
    8: "Loop-Invariant Code Motion (LICM)",
    16: "Strength Reduction (SR)",
    32: "Loop Unrolling (LU)",
}
PASS_ABBR = {1: "CF", 2: "DCE", 4: "CSE", 8: "LICM", 16: "SR", 32: "LU"}

# 6 independently toggleable passes -> 2**6 = 64 distinct combinations.
NUM_PASSES = 6
NUM_COMBOS = 1 << NUM_PASSES  # 64


def get_pass_names(combo_mask: int) -> List[str]:
    """Names of the passes enabled in a combo mask (0 .. NUM_COMBOS-1)."""
    return [name for bit, name in PASS_FLAGS.items() if combo_mask & bit]


def get_pass_abbrs(combo_mask: int) -> List[str]:
    return [ab for bit, ab in PASS_ABBR.items() if combo_mask & bit]


def combo_from_flags(cf=False, dce=False, cse=False, licm=False, sr=False, lu=False) -> int:
    return ((1 if cf else 0) | (2 if dce else 0) | (4 if cse else 0)
            | (8 if licm else 0) | (16 if sr else 0) | (32 if lu else 0))


class PassManager:
    """Orchestrates the six toggleable optimization passes over the TAC IR.

    Enabled passes run in the canonical order

        CF -> CSE -> LU -> LICM -> SR -> DCE

    and the whole sequence is repeated until the IR stops changing (or a small
    round cap is hit), so a transformation that exposes new work for an
    earlier-ordered pass -- LICM lifting an expression that CF can then fold, LU
    duplicating a body that CSE can then dedupe -- is actually cleaned up.

    LU is placed before LICM/SR on purpose: those passes introduce loop-carried
    temporaries, and the unroller only duplicates a body whose temporaries are
    all iteration-local.
    """

    MAX_ROUNDS = 5

    def __init__(self, combo_mask: int = 0, global_names: frozenset = frozenset()):
        self.combo_mask = combo_mask
        self.global_names = global_names

    def optimize_function(self, func: TACFunction) -> TACFunction:
        optimized = copy.deepcopy(func)
        mask = self.combo_mask
        g = self.global_names
        if not (mask & (NUM_COMBOS - 1)):
            return optimized

        prev_sig = None
        for _ in range(self.MAX_ROUNDS):
            if mask & 1:
                optimized = constant_folding_pass(optimized, g)
            if mask & 4:
                optimized = cse_pass(optimized, g)
            if mask & 32:
                optimized = loop_unroll_pass(optimized, g)
            if mask & 8:
                optimized = licm_pass(optimized, g)
            if mask & 16:
                optimized = strength_reduction_pass(optimized)
            if mask & 2:
                optimized = dce_pass(optimized, g)

            sig = _signature(optimized)
            if sig == prev_sig:
                break
            prev_sig = sig
        return optimized

    def optimize_program(self, program: TACProgram) -> TACProgram:
        optimized_prog = copy.deepcopy(program)
        self.global_names = program_global_names(program)
        optimized_prog.functions = [self.optimize_function(f) for f in program.functions]
        return optimized_prog


def _signature(func: TACFunction) -> tuple:
    return tuple(
        (i.opcode, str(i.dst), str(i.src1), str(i.src2), str(i.src3))
        for i in func.instructions
    )


def optimize_program(tac_prog: TACProgram, combo_mask: int) -> TACProgram:
    """Optimize a whole TACProgram with a given combo bitmask (0 .. 63)."""
    return PassManager(combo_mask).optimize_program(tac_prog)
