import copy
from typing import Dict, List, Set, Optional, Any, Tuple
from ..ir.tac import (
    TACFunction, TACInstruction, Opcode,
    Operand, Temp, Var, Constant, Label
)
from ..ir.cfg import build_cfg_for_function, CFG, BasicBlock, Loop


def licm_pass(func: TACFunction) -> TACFunction:
    """Performs Loop-Invariant Code Motion (LICM) by hoisting invariant instructions to loop preheaders."""
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

                    # Check if all operands are loop-invariant
                    if _are_operands_invariant(inst, loop_defs, invariant_defs):
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

        # Build new instructions list
        new_instructions: List[TACInstruction] = []
        hoisted_ids = {id(inst) for inst in invariant_insts}
        hoisted_emitted = False

        for inst in optimized_func.instructions:
            if inst == first_header_inst and not hoisted_emitted:
                # Insert hoisted instructions right before loop header
                for h_inst in invariant_insts:
                    h_copy = copy.deepcopy(h_inst)
                    h_copy.annotation = "LICM Hoisted"
                    new_instructions.append(h_copy)
                hoisted_emitted = True

            if id(inst) not in hoisted_ids:
                new_instructions.append(inst)

        optimized_func.instructions = new_instructions

    return optimized_func


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


def _are_operands_invariant(inst: TACInstruction, loop_defs: Set[str], invariant_defs: Set[str]) -> bool:
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
    return True
