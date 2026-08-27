"""Pass 1 -- Constant Folding & Constant Propagation.

Strategy
--------
A single forward walk over the instruction list of each function, carrying a
``known`` map ``name -> Constant`` that is only ever populated with facts that
hold along *every* path to the current instruction.  The map is cleared at any
point where that guarantee could break:

* at a ``LABEL`` (a basic-block boundary / potential control-flow join), and
* right after an unconditional ``JUMP`` / ``RETURN`` (start of a region that is
  only reachable via a label anyway).

Straight-line fall-through -- including the not-taken edge of a conditional
branch -- keeps the map, which is exactly where propagation is sound.

With the map in hand the pass:

* substitutes known constants into rvalue operand positions,
* folds ``t = c1 OP c2`` / ``t = OP c1`` to ``t = c`` (32-bit C int semantics),
* rewrites branches with a constant condition
  (``ifFalse 0 goto L`` -> ``goto L``; ``ifFalse 1 goto L`` -> removed;
  ``if 1 goto L`` -> ``goto L``; ``if 0 goto L`` -> removed).

The walk is repeated until it reaches a fixed point.
"""
from typing import Dict, List, Optional

from ..ir.tac import (
    Opcode, TACInstruction, TACFunction, TACProgram, Constant, Var, Temp,
)
from ._util import (
    BINARY_OPS, UNARY_OPS, VALUE_PRODUCING,
    value_operand_slots, op_name, const_int_value, global_names,
    fold_binary, fold_unary, int_const,
)


def run(func: TACFunction, prog: Optional[TACProgram] = None) -> bool:
    globals_ = global_names(prog)
    changed_overall = False

    while True:
        known: Dict[str, Constant] = {}
        out: List[TACInstruction] = []
        changed = False

        for inst in func.instructions:
            op = inst.opcode

            if op == Opcode.LABEL:
                known = {}
                out.append(inst)
                continue

            # 1. substitute known constants into rvalue slots
            for slot in value_operand_slots(inst):
                cur = getattr(inst, slot)
                name = op_name(cur)
                if name is not None and name in known:
                    setattr(inst, slot, known[name])
                    changed = True

            # 2. fold pure arithmetic / relational / logical / unary ops
            if op in BINARY_OPS:
                a = const_int_value(inst.src1)
                b = const_int_value(inst.src2)
                if a is not None and b is not None:
                    folded = fold_binary(op, a, b)
                    if folded is not None:
                        inst = TACInstruction(Opcode.ASSIGN, dst=inst.dst,
                                              src1=int_const(folded))
                        op = Opcode.ASSIGN
                        changed = True
            elif op in UNARY_OPS:
                a = const_int_value(inst.src1)
                if a is not None:
                    folded = fold_unary(op, a)
                    if folded is not None:
                        inst = TACInstruction(Opcode.ASSIGN, dst=inst.dst,
                                              src1=int_const(folded))
                        op = Opcode.ASSIGN
                        changed = True

            # 3. simplify constant-condition branches
            if op in (Opcode.JUMP_IF_FALSE, Opcode.JUMP_IF_TRUE):
                c = const_int_value(inst.src1)
                if c is not None:
                    take = (c == 0) if op == Opcode.JUMP_IF_FALSE else (c != 0)
                    changed = True
                    if take:
                        out.append(TACInstruction(Opcode.JUMP, dst=inst.dst))
                        known = {}
                    # else: branch never taken -> drop instruction entirely
                    continue

            # 4. update the known-constant map
            _update_known(known, inst, op, globals_)

            out.append(inst)

            if op in (Opcode.JUMP, Opcode.RETURN):
                known = {}

        func.instructions = out
        changed_overall |= changed
        if not changed:
            break

    return changed_overall


def _update_known(known: Dict[str, Constant], inst: TACInstruction,
                  op: Opcode, globals_) -> None:
    if op == Opcode.ASSIGN and isinstance(inst.src1, Constant) \
            and isinstance(inst.dst, (Var, Temp)):
        known[str(inst.dst)] = inst.src1
        return

    # any other (re)definition invalidates the destination's constant status
    if op in VALUE_PRODUCING or op == Opcode.CALL:
        name = op_name(inst.dst)
        if name is not None:
            known.pop(name, None)

    if op in (Opcode.STORE_ARR_1D, Opcode.STORE_ARR_2D, Opcode.SET_FIELD):
        name = op_name(inst.dst)
        if name is not None:
            known.pop(name, None)

    # a call may mutate any global
    if op == Opcode.CALL:
        for g in list(known):
            if g in globals_:
                known.pop(g, None)
