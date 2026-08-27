"""Pass 2 -- Dead Code Elimination via backward liveness.

A classic iterative data-flow computation over the CFG:

    live_out(B) = U live_in(S)  for S in succ(B)      (plus globals at exits)
    live_in(B)  = transfer(B, live_out(B))

then a backward sweep inside every block removes any *pure*, value-producing
instruction whose defined name is not live immediately afterwards.  Removing an
instruction can kill its operands, so the whole process is repeated until it
stabilises.

Safety: stores, field-writes, calls, returns, params, jumps, labels and allocs
are never removed.  An assignment to a global is never removed.  Because MiniC
has no aliasing, a dead temporary really is dead -- nothing can observe it.
"""
from typing import Dict, List, Set, Optional

from ..ir.tac import Opcode, TACInstruction, TACFunction, TACProgram
from ..ir.cfg import build_cfg_for_function
from ._util import (
    VALUE_PRODUCING, defined_name, used_names, global_names,
)


def run(func: TACFunction, prog: Optional[TACProgram] = None) -> bool:
    globals_ = global_names(prog)
    changed_overall = False

    while True:
        cfg = build_cfg_for_function(func)
        if not cfg.blocks:
            return changed_overall

        live_in: Dict[int, Set[str]] = {b.id: set() for b in cfg.blocks}
        live_out: Dict[int, Set[str]] = {b.id: set() for b in cfg.blocks}

        # iterative fixed point (blocks visited in reverse for faster convergence)
        while True:
            stable = True
            for b in reversed(cfg.blocks):
                out: Set[str] = set()
                for s in b.successors:
                    out |= live_in[s.id]
                if not b.successors:
                    out |= globals_
                inn = set(out)
                for inst in reversed(b.instructions):
                    d = defined_name(inst)
                    if d is not None:
                        inn.discard(d)
                    inn |= used_names(inst)
                if out != live_out[b.id] or inn != live_in[b.id]:
                    live_out[b.id] = out
                    live_in[b.id] = inn
                    stable = False
            if stable:
                break

        # removal sweep
        removed_here = False
        for b in cfg.blocks:
            live = set(live_out[b.id])
            kept_rev: List[TACInstruction] = []
            for inst in reversed(b.instructions):
                d = defined_name(inst)
                is_pure = inst.opcode in VALUE_PRODUCING  # excludes CALL
                if (is_pure and d is not None
                        and d not in live and d not in globals_):
                    removed_here = True
                    continue  # drop
                if d is not None:
                    live.discard(d)
                live |= used_names(inst)
                kept_rev.append(inst)
            b.instructions = list(reversed(kept_rev))

        if removed_here:
            func.instructions = [i for b in cfg.blocks for i in b.instructions]
            changed_overall = True
        else:
            break

    return changed_overall
