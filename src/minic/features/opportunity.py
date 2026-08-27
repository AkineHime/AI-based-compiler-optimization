"""'Opportunity' features -- a cheap static estimate of *how much* each pass
would actually transform a program.

These are computed from the unoptimized TAC only (no timing, no optimization
run), and they turn out to be the strongest signal the recommender has: if LICM
would hoist 30 instructions out of a loop that dominates the estimated dynamic
instruction count, LICM is going to help.
"""
from typing import Dict, List, Set

from ..ir.tac import (
    Opcode, TACInstruction, TACProgram, TACFunction, Constant, Var, Temp,
)
from ..ir.cfg import build_cfg_for_function

OPPORTUNITY_NAMES: List[str] = [
    "opp_const_foldable",       # binary ops with both operands constant / const-propagated
    "opp_cse_redundant",        # repeated pure expressions within a basic block
    "opp_licm_hoistable",       # loop instructions whose operands are all loop-invariant
    "opp_sr_reducible",         # `iv * const` in a loop with a single-step induction var
    "opp_unrollable_loops",     # loops matching the unroller's shape
    "opp_loop_body_insts",      # total instructions inside natural loops
    "opp_hot_invariant_frac",   # invariant fraction of the largest loop body
    "opp_est_dyn_kilo_insts",   # sum of (static trip count * body size) / 1000, when the bound is constant
]

_PURE_BIN = {Opcode.ADD, Opcode.SUB, Opcode.MUL, Opcode.DIV, Opcode.MOD,
             Opcode.EQ, Opcode.NE, Opcode.LT, Opcode.LE, Opcode.GT, Opcode.GE}
_REL = {Opcode.LT, Opcode.LE, Opcode.GT, Opcode.GE}


def _name(o):
    return str(o) if isinstance(o, (Var, Temp)) else None


def _is_const(o):
    return isinstance(o, Constant)


def extract_opportunity(tac: TACProgram) -> Dict[str, float]:
    f = {n: 0.0 for n in OPPORTUNITY_NAMES}
    biggest_body, biggest_inv = 0, 0

    for func in tac.functions:
        insts = func.instructions

        # --- single-assignment literal locals (const propagation candidates) ---
        lit_once: Dict[str, int] = {}
        assign_ct: Dict[str, int] = {}
        for i in insts:
            n = _name(i.dst)
            if n and i.opcode in (_PURE_BIN | {Opcode.ASSIGN, Opcode.NEG,
                                              Opcode.LOAD_ARR_1D, Opcode.LOAD_ARR_2D,
                                              Opcode.GET_FIELD, Opcode.CALL}):
                assign_ct[n] = assign_ct.get(n, 0) + 1
                if i.opcode == Opcode.ASSIGN and _is_const(i.src1):
                    lit_once[n] = 1
        const_locals = {n for n in lit_once if assign_ct.get(n, 0) == 1}

        # --- const-foldable binary ops ---
        for i in insts:
            if i.opcode in _PURE_BIN:
                a = _is_const(i.src1) or _name(i.src1) in const_locals
                b = _is_const(i.src2) or _name(i.src2) in const_locals
                if a and b:
                    f["opp_const_foldable"] += 1

        # --- CSE: repeated pure expr keys per basic block ---
        cfg = build_cfg_for_function(func)
        for blk in cfg.blocks:
            seen: Set[tuple] = set()
            for i in blk.instructions:
                if i.opcode in _PURE_BIN:
                    k = (i.opcode, repr(i.src1), repr(i.src2))
                    if k in seen:
                        f["opp_cse_redundant"] += 1
                    seen.add(k)

        # --- loops: LICM / SR / unroll / body size / dyn estimate ---
        for loop in cfg.loops:
            body = [i for b in cfg.blocks if b in loop.blocks for i in b.instructions]
            f["opp_loop_body_insts"] += len(body)

            defs_in: Set[str] = set()
            for i in body:
                n = _name(i.dst)
                if n:
                    defs_in.add(n)
            bivs = _single_step_bivs(body)

            invariant = 0
            for i in body:
                if i.opcode in (_PURE_BIN | {Opcode.NEG}):
                    ops = [i.src1, i.src2]
                    if all(_is_const(o) or (_name(o) and _name(o) not in defs_in)
                           for o in ops if o is not None):
                        f["opp_licm_hoistable"] += 1
                        invariant += 1
                if i.opcode == Opcode.MUL:
                    for a, c in ((i.src1, i.src2), (i.src2, i.src1)):
                        if _name(a) in bivs and _is_const(c):
                            f["opp_sr_reducible"] += 1

            if len(body) > biggest_body:
                biggest_body, biggest_inv = len(body), invariant

            hdr = loop.header.instructions if loop.header.instructions else []
            if (len(hdr) >= 3 and hdr[0].opcode == Opcode.LABEL
                    and hdr[1].opcode in _REL and hdr[2].opcode == Opcode.JUMP_IF_FALSE):
                iv, bound = _iv_and_bound(hdr[1])
                straight = not any(x.opcode in (Opcode.LABEL, Opcode.JUMP,
                                                Opcode.JUMP_IF_TRUE, Opcode.JUMP_IF_FALSE,
                                                Opcode.RETURN)
                                   for x in body[3:])
                if iv in bivs and straight and 0 < len(body) <= 30:
                    f["opp_unrollable_loops"] += 1
                if bound is not None and iv in bivs:
                    step = abs(bivs[iv]) or 1
                    f["opp_est_dyn_kilo_insts"] += (bound / step) * len(body) / 1000.0

    f["opp_hot_invariant_frac"] = round(biggest_inv / biggest_body, 4) if biggest_body else 0.0
    return f


def _single_step_bivs(body) -> Dict[str, int]:
    """var -> step, for vars updated exactly once by  v = v +/- const  (staged too)."""
    write_ct: Dict[str, int] = {}
    for i in body:
        if isinstance(i.dst, Var):
            write_ct[i.dst.name] = write_ct.get(i.dst.name, 0) + 1
    temp_step: Dict[str, tuple] = {}
    biv: Dict[str, int] = {}
    for i in body:
        if i.opcode in (Opcode.ADD, Opcode.SUB):
            if isinstance(i.dst, Var) and _name(i.src1) == i.dst.name and _is_const(i.src2):
                biv[i.dst.name] = i.src2.value * (1 if i.opcode == Opcode.ADD else -1)
            elif isinstance(i.dst, Temp) and isinstance(i.src1, Var) and _is_const(i.src2):
                temp_step[str(i.dst)] = (i.src1.name, i.src2.value *
                                         (1 if i.opcode == Opcode.ADD else -1))
        elif i.opcode == Opcode.ASSIGN and isinstance(i.dst, Var) and isinstance(i.src1, Temp):
            t = temp_step.get(str(i.src1))
            if t and t[0] == i.dst.name:
                biv[i.dst.name] = t[1]
    return {v: s for v, s in biv.items() if write_ct.get(v, 0) == 1}


def _iv_and_bound(cmp_i: TACInstruction):
    n1, n2 = _name(cmp_i.src1), _name(cmp_i.src2)
    if n1 and _is_const(cmp_i.src2):
        return n1, cmp_i.src2.value
    if n2 and _is_const(cmp_i.src1):
        return n2, cmp_i.src1.value
    return (n1 or n2), None
