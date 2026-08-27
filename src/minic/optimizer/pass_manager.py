"""The 5-flag pass controller.

Each of the five passes is toggled by one bit of a ``combo_id`` in ``0..63``::

    bit 0 (1)  -> constant folding            (CF)
    bit 1 (2)  -> dead code elimination       (DCE)
    bit 2 (4)  -> common subexpression elim.  (CSE)
    bit 3 (8)  -> loop-invariant code motion   (LICM)
    bit 4 (16) -> strength reduction           (SR)

Enabled passes always run in one fixed canonical order --

    CF -> CSE -> LICM -> SR -> DCE

-- and the whole sequence is repeated until it reaches a fixed point (or a small
iteration cap), so that a transformation which exposes new work for an
earlier-ordered pass still gets cleaned up.  ``combo_id == 0`` is the untouched
baseline.
"""
import copy
from dataclasses import dataclass
from typing import Callable, List, Optional

from ..ir.tac import TACFunction, TACProgram
from . import constant_folding, dce, cse, licm, strength_reduction

FLAG_CF = 1
FLAG_DCE = 2
FLAG_CSE = 4
FLAG_LICM = 8
FLAG_SR = 16

ALL_FLAGS = FLAG_CF | FLAG_DCE | FLAG_CSE | FLAG_LICM | FLAG_SR
NUM_COMBOS = 64


@dataclass(frozen=True)
class PassSpec:
    flag: int
    name: str
    run: Callable[[TACFunction, Optional[TACProgram]], bool]


# canonical order: CF, CSE, LICM, SR, DCE
CANONICAL_ORDER: List[PassSpec] = [
    PassSpec(FLAG_CF, "constant_folding", constant_folding.run),
    PassSpec(FLAG_CSE, "cse", cse.run),
    PassSpec(FLAG_LICM, "licm", licm.run),
    PassSpec(FLAG_SR, "strength_reduction", strength_reduction.run),
    PassSpec(FLAG_DCE, "dce", dce.run),
]


def combo_flags(combo_id: int) -> dict:
    """Human-readable {flag_name: bool} view of a combo id."""
    return {
        "flag_cf": bool(combo_id & FLAG_CF),
        "flag_dce": bool(combo_id & FLAG_DCE),
        "flag_cse": bool(combo_id & FLAG_CSE),
        "flag_licm": bool(combo_id & FLAG_LICM),
        "flag_sr": bool(combo_id & FLAG_SR),
    }


def combo_label(combo_id: int) -> str:
    on = [s.name for s in CANONICAL_ORDER if combo_id & s.flag]
    return f"combo {combo_id:02d} [" + ", ".join(on) + "]" if on \
        else f"combo {combo_id:02d} [baseline]"


class PassManager:
    def __init__(self, combo_id: int, max_iterations: int = 8):
        if not (0 <= combo_id < NUM_COMBOS):
            raise ValueError(f"combo_id must be in 0..63, got {combo_id}")
        self.combo_id = combo_id
        self.max_iterations = max_iterations
        self.enabled = [s for s in CANONICAL_ORDER if combo_id & s.flag]

    def optimize_program(self, prog: TACProgram) -> TACProgram:
        """Return an optimized *copy* of ``prog`` (input is left untouched)."""
        result = copy.deepcopy(prog)
        if not self.enabled:
            return result
        for func in result.functions:
            self._optimize_function(func, result)
        return result

    def _optimize_function(self, func: TACFunction, prog: TACProgram) -> None:
        for _ in range(self.max_iterations):
            changed = False
            for spec in self.enabled:
                changed |= bool(spec.run(func, prog))
            if not changed:
                break


def optimize(prog: TACProgram, combo_id: int) -> TACProgram:
    return PassManager(combo_id).optimize_program(prog)
