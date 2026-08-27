"""Pass 5 -- Strength Reduction on induction variables.

Targets the pattern

    L_header:
        ...
        j = i * K          # i is a basic induction variable, K a constant
        ...
        i = i + S          # the (single) update of i, S a constant
        goto L_header

and rewrites it to

    L_preheader:
        sr = i * K         # i still holds its pre-loop value here
    L_header:
        ...
        j = sr             # was j = i * K
        ...
        i = i + S
        sr = sr + (K*S)    # inserted right after i's update
        goto L_header

The invariant ``sr == i * K`` is established in the pre-header and preserved by
keeping ``sr += K*S`` adjacent to ``i += S``, so the value read at the use site
is identical whether the use precedes or follows the update.  All arithmetic
uses 32-bit wrap-around, matching the C ``int`` the baseline would compute.

Guards: exactly one basic-induction update ``i = i +/- const`` in the loop, the
derived temp ``j`` defined exactly once, ``K`` and ``S`` non-zero integer
constants, and the loop header in the canonical ``LABEL``-first shape.
"""
from typing import Dict, List, Optional, Set

from ..ir.tac import (
    Opcode, TACInstruction, TACFunction, TACProgram, Constant, Var, Temp, Label,
)
from ..ir.cfg import build_cfg_for_function
from ._util import (
    op_name, defined_name, const_int_value, is_temp_name, wrap32, int_const,
)

_SR_COUNTER = [0]


def run(func: TACFunction, prog: Optional[TACProgram] = None) -> bool:
    changed_overall = False
    for _ in range(64):
        if not _one_reduction(func):
            break
        changed_overall = True
    return changed_overall


def _one_reduction(func: TACFunction) -> bool:
    cfg = build_cfg_for_function(func)
    if not cfg.loops:
        return False

    for loop in sorted(cfg.loops, key=lambda l: -l.depth):
        header = loop.header
        if not header.instructions or header.instructions[0].opcode != Opcode.LABEL:
            continue
        header_label_inst = header.instructions[0]

        loop_insts: List[TACInstruction] = []
        for b in cfg.blocks:
            if b in loop.blocks:
                loop_insts.extend(b.instructions)

        # all definitions in the loop
        def_sites: Dict[str, List[TACInstruction]] = {}
        for i in loop_insts:
            d = defined_name(i)
            if d:
                def_sites.setdefault(d, []).append(i)
            if i.opcode in (Opcode.STORE_ARR_1D, Opcode.STORE_ARR_2D,
                            Opcode.SET_FIELD):
                n = op_name(i.dst)
                if n:
                    def_sites.setdefault(n, []).append(i)

        # basic induction variables.  Two shapes are recognised:
        #   direct :  i = i + c
        #   staged :  tX = i + c ;  i = tX      (what the IR generator emits)
        bivs: Dict[str, int] = {}
        biv_update: Dict[str, TACInstruction] = {}
        for name, sites in def_sites.items():
            if len(sites) != 1:
                continue
            upd = sites[0]
            step = _basic_iv_step(upd, name)
            if step is None and upd.opcode == Opcode.ASSIGN:
                tname = op_name(upd.src1)
                if is_temp_name(tname) and len(def_sites.get(tname, [])) == 1:
                    step = _basic_iv_step(def_sites[tname][0], name)
            if step is not None and step != 0:
                bivs[name] = step
                biv_update[name] = upd  # insert  sr += delta  right after this
        if not bivs:
            continue

        for i in loop_insts:
            if i.opcode != Opcode.MUL:
                continue
            k = biv = None
            n1, n2 = op_name(i.src1), op_name(i.src2)
            c1, c2 = const_int_value(i.src1), const_int_value(i.src2)
            if n1 in bivs and c2 is not None:
                biv, k = n1, c2
            elif n2 in bivs and c1 is not None:
                biv, k = n2, c1
            if biv is None or k == 0:
                continue
            d = defined_name(i)
            if not d or len(def_sites.get(d, [])) != 1:
                continue

            step = bivs[biv]
            delta = wrap32(k * step)
            sr = f"__sr{_next_sr()}"
            func.local_types[sr] = "int"

            upd_inst = biv_update[biv]
            insts = func.instructions
            try:
                mul_idx = next(x for x, ins in enumerate(insts) if ins is i)
                upd_idx = next(x for x, ins in enumerate(insts) if ins is upd_inst)
                hdr_idx = next(x for x, ins in enumerate(insts)
                               if ins is header_label_inst)
            except StopIteration:
                continue

            sr_var = Var(name=sr, type_str="int")
            # 1. use site:  j = i * K   ->   j = sr
            insts[mul_idx] = TACInstruction(Opcode.ASSIGN, dst=i.dst, src1=sr_var)
            # 2. after the induction update:  sr = sr + delta
            insts.insert(upd_idx + 1,
                         TACInstruction(Opcode.ADD, dst=sr_var, src1=sr_var,
                                        src2=int_const(delta)))
            # 3. pre-header seed:  L_pre: ; sr = biv * K
            pre_label = Label(name=f"L_sr_pre_{func.name}_{_SR_COUNTER[0]}")
            seed = [
                TACInstruction(Opcode.LABEL, dst=pre_label),
                TACInstruction(Opcode.MUL, dst=sr_var,
                               src1=Var(name=biv, type_str="int"),
                               src2=int_const(k)),
            ]
            # header index may have shifted if the insert was before it
            hdr_idx = next(x for x, ins in enumerate(insts)
                           if ins is header_label_inst)
            func.instructions = insts[:hdr_idx] + seed + insts[hdr_idx:]
            return True

    return False


def _basic_iv_step(inst: TACInstruction, name: str) -> Optional[int]:
    if inst.opcode == Opcode.ADD:
        if op_name(inst.src1) == name:
            return const_int_value(inst.src2)
        if op_name(inst.src2) == name:
            return const_int_value(inst.src1)
    elif inst.opcode == Opcode.SUB:
        if op_name(inst.src1) == name:
            c = const_int_value(inst.src2)
            return -c if c is not None else None
    return None


def _next_sr() -> int:
    _SR_COUNTER[0] += 1
    return _SR_COUNTER[0]
