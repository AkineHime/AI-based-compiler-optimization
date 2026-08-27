"""Pass 4 -- Loop-Invariant Code Motion.

For every natural loop we hoist *pure, single-definition temporary* computations
whose operands are all loop-invariant into a freshly created pre-header placed
immediately before the loop header label.

Why this placement is sound for the front-end's loop shape
--------------------------------------------------------
The IR generator emits every ``while`` / ``for`` loop as::

    <code that falls through>
    L_header:               # condition test lives here
        ...
        ifFalse t goto L_end
        <body>
        goto L_header       # back-edge
    L_end:

The only edges into ``L_header`` are (a) fall-through from above and (b) the
back-edge.  Inserting ``L_preheader:`` right before ``L_header:`` puts the
hoisted code on edge (a) only -- the back-edge jumps straight to ``L_header`` and
skips it.  The pre-header therefore dominates the header and runs exactly once
per loop activation, which is what LICM requires.

Conservative guards
-------------------
* only ``t<n>`` temporaries with exactly one definition inside the loop,
* operands must be constants or defined outside the loop (or already hoisted),
* ``DIV`` / ``MOD`` are only hoisted when the divisor is a non-zero constant
  (so the pre-header cannot trap on a zero-trip loop),
* if the loop contains a call, instructions reading a global are left in place.
"""
from typing import List, Optional, Set

from ..ir.tac import Opcode, TACInstruction, TACFunction, TACProgram, Label
from ..ir.cfg import build_cfg_for_function
from ._util import (
    BINARY_ARITH, RELATIONAL, UNARY_OPS,
    value_operand_slots, op_name, defined_name, global_names, is_temp_name,
)

_HOISTABLE = (BINARY_ARITH | RELATIONAL | UNARY_OPS | {Opcode.ASSIGN})


def run(func: TACFunction, prog: Optional[TACProgram] = None) -> bool:
    globals_ = global_names(prog)
    changed_overall = False

    for _ in range(64):  # bounded fixed-point over successive hoists
        if not _one_hoist(func, globals_):
            break
        changed_overall = True
    return changed_overall


def _one_hoist(func: TACFunction, globals_: Set[str]) -> bool:
    cfg = build_cfg_for_function(func)
    if not cfg.loops:
        return False

    # innermost loops first
    for loop in sorted(cfg.loops, key=lambda l: -l.depth):
        header = loop.header
        if not header.instructions or header.instructions[0].opcode != Opcode.LABEL:
            continue
        header_label_inst = header.instructions[0]

        loop_insts: List[TACInstruction] = []
        for b in cfg.blocks:
            if b in loop.blocks:
                loop_insts.extend(b.instructions)

        # names (re)defined anywhere in the loop, with a count
        def_count: dict = {}
        for i in loop_insts:
            d = defined_name(i)
            if d:
                def_count[d] = def_count.get(d, 0) + 1
            if i.opcode in (Opcode.STORE_ARR_1D, Opcode.STORE_ARR_2D,
                            Opcode.SET_FIELD):
                n = op_name(i.dst)
                if n:
                    def_count[n] = def_count.get(n, 0) + 1
        has_call = any(i.opcode == Opcode.CALL for i in loop_insts)

        hoisted_names: Set[str] = set()
        to_move: List[TACInstruction] = []
        moved_ids: Set[int] = set()

        progress = True
        while progress:
            progress = False
            for i in loop_insts:
                if id(i) in moved_ids:
                    continue
                if i.opcode not in _HOISTABLE:
                    continue
                d = defined_name(i)
                if not is_temp_name(d):
                    continue
                if def_count.get(d, 0) != 1:
                    continue
                if not _operands_invariant(i, def_count, hoisted_names,
                                           has_call, globals_):
                    continue
                if i.opcode in (Opcode.DIV, Opcode.MOD):
                    from ._util import const_int_value
                    if const_int_value(i.src2) in (None, 0):
                        continue
                to_move.append(i)
                moved_ids.add(id(i))
                hoisted_names.add(d)
                progress = True

        if not to_move:
            continue

        # --- splice: remove hoisted insts, drop a pre-header in front of header
        pre_label = Label(name=_fresh_preheader_name(func))
        remaining = [ins for ins in func.instructions if id(ins) not in moved_ids]
        try:
            idx = next(k for k, ins in enumerate(remaining)
                       if ins is header_label_inst)
        except StopIteration:
            continue
        new_list = (remaining[:idx]
                    + [TACInstruction(Opcode.LABEL, dst=pre_label)]
                    + to_move
                    + remaining[idx:])
        func.instructions = new_list
        return True

    return False


def _operands_invariant(inst: TACInstruction, def_count: dict,
                        hoisted: Set[str], has_call: bool,
                        globals_: Set[str]) -> bool:
    for slot in value_operand_slots(inst):
        operand = getattr(inst, slot)
        name = op_name(operand)
        if name is None:
            continue  # a constant
        if has_call and name in globals_:
            return False
        if name in def_count and name not in hoisted:
            return False
    return True


_PH_COUNTER = [0]


def _fresh_preheader_name(func: TACFunction) -> str:
    _PH_COUNTER[0] += 1
    return f"L_preheader_{func.name}_{_PH_COUNTER[0]}"
