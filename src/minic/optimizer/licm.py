import copy
from typing import Dict, List, Set, Optional, Any, Tuple
from ..ir.tac import (
    TACFunction, TACInstruction, Opcode,
    Operand, Temp, Var, Constant, Label
)
from ..ir.cfg import build_cfg_for_function, CFG, BasicBlock, Loop


def licm_pass(func: TACFunction, global_names: frozenset = frozenset()) -> TACFunction:
    """Performs Loop-Invariant Code Motion (LICM) by hoisting invariant instructions to loop preheaders.

    ``global_names`` lists module-level variables; when a loop contains a call,
    instructions that read one of those are treated as variant (the call may
    rewrite the global on every iteration).
    """
    optimized_func = copy.deepcopy(func)
    cfg = build_cfg_for_function(optimized_func)

    if not cfg.loops:
        return optimized_func

    # Sort loops by nesting depth descending (innermost first)
    sorted_loops = sorted(cfg.loops, key=lambda l: l.depth, reverse=True)

    for loop in sorted_loops:
        # Collect definitions and mutations inside the loop
        loop_defs: Set[str] = set()
        loop_def_counts: Dict[str, int] = {}
        array_writes: Set[str] = set()
        struct_writes: Set[str] = set()
        has_call = False

        for b in loop.blocks:
            for inst in b.instructions:
                if inst.opcode == Opcode.CALL:
                    has_call = True
                if inst.opcode in (Opcode.STORE_ARR_1D, Opcode.STORE_ARR_2D):
                    if inst.dst is not None:
                        array_writes.add(str(inst.dst))
                if inst.opcode == Opcode.SET_FIELD:
                    if inst.dst is not None:
                        struct_writes.add(str(inst.dst))

                for d in _get_instruction_defs(inst):
                    loop_defs.add(d)
                    loop_def_counts[d] = loop_def_counts.get(d, 0) + 1

        # Iteratively identify invariant instructions
        invariant_insts: List[TACInstruction] = []
        invariant_defs: Set[str] = set()

        changed = True
        while changed:
            changed = False
            for b in loop.blocks:
                for inst in b.instructions:
                    if id(inst) in {id(x) for x in invariant_insts}:
                        continue
                    if not _is_hoistable_candidate(inst):
                        continue

                    # Memory load checks
                    if inst.opcode in (Opcode.LOAD_ARR_1D, Opcode.LOAD_ARR_2D):
                        if has_call or (inst.src1 is not None and str(inst.src1) in array_writes):
                            continue
                    if inst.opcode == Opcode.GET_FIELD:
                        if has_call or (inst.src1 is not None and str(inst.src1) in struct_writes):
                            continue

                    # A pre-header runs even on a zero-trip loop, so never move a
                    # divide/remainder unless the divisor is a known non-zero
                    # constant (otherwise we could trap where the baseline would
                    # simply skip the loop body).
                    if inst.opcode in (Opcode.DIV, Opcode.MOD):
                        if not (isinstance(inst.src2, Constant)
                                and isinstance(inst.src2.value, (int, float))
                                and inst.src2.value != 0):
                            continue

                    # Only hoist computations into a temporary.  A named variable
                    # can be read earlier in the loop body than it is written
                    # (use-before-def across iterations); moving its definition
                    # to the pre-header would change what that read observes.
                    if not isinstance(inst.dst, Temp):
                        continue

                    # Check if all operands are loop-invariant
                    if _are_operands_invariant(inst, loop_defs, invariant_defs,
                                               has_call, global_names):
                        # Safety: dst assigned only once
                        dst_name = str(inst.dst) if inst.dst is not None else None
                        if dst_name and loop_def_counts.get(dst_name, 0) == 1:
                            invariant_insts.append(inst)
                            if dst_name:
                                invariant_defs.add(dst_name)
                            changed = True

        if not invariant_insts:
            continue

        # Hoist invariant instructions to before the loop header
        header_block = loop.header
        if not header_block.instructions:
            continue
        first_header_inst = header_block.instructions[0]
        if first_header_inst.opcode != Opcode.LABEL:
            continue
        head_label = str(first_header_inst.dst)

        insts = optimized_func.instructions
        try:
            hidx = next(k for k, x in enumerate(insts) if x is first_header_inst)
        except StopIteration:
            continue

        # If the code textually before the header is not a fall-through (e.g. an
        # unroll block's `goto`), instructions placed there are unreachable and,
        # worse, every jump into the header would skip them.  In that case build
        # a real labelled pre-header and redirect the loop's *entry* edges
        # (everything except the latch's back-edge) to it.
        prev_op = insts[hidx - 1].opcode if hidx > 0 else Opcode.LABEL
        need_label = prev_op in (Opcode.JUMP, Opcode.RETURN,
                                 Opcode.JUMP_IF_TRUE, Opcode.JUMP_IF_FALSE)

        hoisted_ids = {id(inst) for inst in invariant_insts}
        hoist = [copy.deepcopy(h) for h in invariant_insts]
        for h in hoist:
            h.annotation = "LICM Hoisted"

        latch_block = loop.back_edge[0] if getattr(loop, "back_edge", None) else None
        latch_ids = {id(i) for i in latch_block.instructions} if latch_block else set()

        if need_label:
            pre_label = Label(name=f"L_licm_pre_{optimized_func.name}_{_pre_counter()}")
            block = [TACInstruction(Opcode.LABEL, dst=pre_label)] + hoist
            new_instructions = []
            for inst in insts:
                if inst is first_header_inst:
                    new_instructions.extend(block)
                if id(inst) in hoisted_ids:
                    continue
                # redirect entry jumps (not the latch) from header -> pre-header
                if (inst.opcode in (Opcode.JUMP, Opcode.JUMP_IF_TRUE, Opcode.JUMP_IF_FALSE)
                        and str(inst.dst) == head_label and id(inst) not in latch_ids):
                    inst = TACInstruction(inst.opcode, dst=pre_label,
                                          src1=inst.src1, src2=inst.src2,
                                          src3=inst.src3, annotation=inst.annotation)
                new_instructions.append(inst)
            optimized_func.instructions = new_instructions
        else:
            new_instructions = []
            for inst in insts:
                if inst is first_header_inst:
                    new_instructions.extend(hoist)
                if id(inst) not in hoisted_ids:
                    new_instructions.append(inst)
            optimized_func.instructions = new_instructions

    return optimized_func


_PRE = [0]


def _pre_counter() -> int:
    _PRE[0] += 1
    return _PRE[0]


def _get_instruction_defs(inst: TACInstruction) -> Set[str]:
    defs = set()
    op = inst.opcode
    if op in (
        Opcode.ASSIGN, Opcode.ADD, Opcode.SUB, Opcode.MUL, Opcode.DIV, Opcode.MOD,
        Opcode.EQ, Opcode.NE, Opcode.LT, Opcode.LE, Opcode.GT, Opcode.GE,
        Opcode.LOGIC_AND, Opcode.LOGIC_OR, Opcode.NEG, Opcode.LOGIC_NOT,
        Opcode.LOAD_ARR_1D, Opcode.LOAD_ARR_2D, Opcode.GET_FIELD
    ):
        if inst.dst is not None and isinstance(inst.dst, (Temp, Var)):
            defs.add(str(inst.dst))
    return defs


def _is_hoistable_candidate(inst: TACInstruction) -> bool:
    op = inst.opcode
    if op in (
        Opcode.ASSIGN, Opcode.ADD, Opcode.SUB, Opcode.MUL, Opcode.DIV, Opcode.MOD,
        Opcode.EQ, Opcode.NE, Opcode.LT, Opcode.LE, Opcode.GT, Opcode.GE,
        Opcode.LOGIC_AND, Opcode.LOGIC_OR, Opcode.NEG, Opcode.LOGIC_NOT,
        Opcode.LOAD_ARR_1D, Opcode.LOAD_ARR_2D, Opcode.GET_FIELD
    ):
        return inst.dst is not None and isinstance(inst.dst, (Temp, Var))
    return False


def _are_operands_invariant(inst: TACInstruction, loop_defs: Set[str],
                            invariant_defs: Set[str], has_call: bool = False,
                            global_names: frozenset = frozenset()) -> bool:
    for src in (inst.src1, inst.src2, inst.src3):
        if src is None:
            continue
        if isinstance(src, Constant):
            continue
        if isinstance(src, (Temp, Var)):
            s_name = str(src)
            # Must be either defined outside loop or already marked invariant
            if s_name in loop_defs and s_name not in invariant_defs:
                return False
            # A call in the loop may clobber any global between iterations.
            if has_call and s_name in global_names:
                return False
    return True
