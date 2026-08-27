"""Pass 3 -- Common Subexpression Elimination (local value numbering).

Per basic block we assign a *value number* to every operand and to every
computed expression ``(op, vn(a), vn(b))``.  When an expression recurs and none
of its operands has been redefined since (tracked by bumping the operand's value
number on every definition) the recomputation ``t = a OP b`` is rewritten to the
copy ``t = holder``.

Only arithmetic / relational / logical / unary expressions are numbered.  Loads
and field reads are *not* CSE'd (they are only used to invalidate state), which
keeps the pass trivially correct in the presence of aggregate writes.  Value
numbers are local to each block, so nothing crosses a control-flow edge.
"""
from typing import Dict, List, Optional, Tuple

from ..ir.tac import (
    Opcode, TACInstruction, TACFunction, TACProgram, Constant, Var, Temp,
)
from ..ir.cfg import build_cfg_for_function
from ._util import (
    BINARY_ARITH, RELATIONAL, BINARY_LOGIC, UNARY_OPS, COMMUTATIVE,
    op_name, global_names,
)

_NUMBERED = BINARY_ARITH | RELATIONAL | BINARY_LOGIC | UNARY_OPS


def run(func: TACFunction, prog: Optional[TACProgram] = None) -> bool:
    globals_ = global_names(prog)
    cfg = build_cfg_for_function(func)
    if not cfg.blocks:
        return False

    changed = False

    for b in cfg.blocks:
        vn: Dict[str, int] = {}
        const_vn: Dict[Tuple, int] = {}
        expr_table: Dict[Tuple, str] = {}          # expr key -> holder name
        counter = [0]

        def fresh() -> int:
            counter[0] += 1
            return counter[0]

        def vn_of(operand: object) -> int:
            if isinstance(operand, Constant):
                key = ("const", operand.type_str, repr(operand.value))
                if key not in const_vn:
                    const_vn[key] = fresh()
                return const_vn[key]
            name = op_name(operand)
            if name is None:
                return fresh()
            if name not in vn:
                vn[name] = fresh()
            return vn[name]

        def kill(name: str) -> None:
            vn[name] = fresh()
            for k in [k for k, holder in expr_table.items() if holder == name]:
                del expr_table[k]

        new_insts: List[TACInstruction] = []
        for inst in b.instructions:
            op = inst.opcode

            if op in _NUMBERED:
                dname = op_name(inst.dst)
                if op in UNARY_OPS:
                    key = (op, vn_of(inst.src1))
                else:
                    v1, v2 = vn_of(inst.src1), vn_of(inst.src2)
                    if op in COMMUTATIVE and v1 > v2:
                        v1, v2 = v2, v1
                    key = (op, v1, v2)

                if dname is not None and key in expr_table:
                    holder = expr_table[key]
                    holder_operand = _name_to_operand(holder, inst.dst)
                    inst = TACInstruction(Opcode.ASSIGN, dst=inst.dst,
                                          src1=holder_operand)
                    changed = True
                    kill(dname)
                    vn[dname] = vn.get(holder, fresh())
                else:
                    if dname is not None:
                        kill(dname)
                        expr_table[key] = dname
                    new_insts.append(inst)
                    continue
                new_insts.append(inst)
                continue

            if op == Opcode.ASSIGN:
                dname = op_name(inst.dst)
                sv = vn_of(inst.src1)
                if dname is not None:
                    kill(dname)
                    vn[dname] = sv
                new_insts.append(inst)
                continue

            # definitions we do not model precisely -> just invalidate dst
            dname = op_name(inst.dst)
            if op in (Opcode.LOAD_ARR_1D, Opcode.LOAD_ARR_2D, Opcode.GET_FIELD):
                if dname is not None:
                    kill(dname)
            elif op == Opcode.CALL:
                if dname is not None:
                    kill(dname)
                for g in list(vn):
                    if g in globals_:
                        kill(g)
            elif op in (Opcode.STORE_ARR_1D, Opcode.STORE_ARR_2D,
                        Opcode.SET_FIELD):
                if dname is not None:
                    kill(dname)

            new_insts.append(inst)

        b.instructions = new_insts

    if changed:
        func.instructions = [i for b in cfg.blocks for i in b.instructions]
    return changed


def _name_to_operand(name: str, like: object):
    if name and name[0] == "t" and name[1:].isdigit():
        tstr = like.type_str if isinstance(like, (Var, Temp)) else "int"
        return Temp(id=int(name[1:]), type_str=tstr)
    tstr = like.type_str if isinstance(like, (Var, Temp)) else "int"
    return Var(name=name, type_str=tstr)
