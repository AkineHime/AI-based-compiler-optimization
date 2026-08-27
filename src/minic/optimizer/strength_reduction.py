import copy
from typing import Dict, List, Set, Optional, Any, Tuple
from ..ir.tac import (
    TACFunction, TACInstruction, Opcode,
    Operand, Temp, Var, Constant, Label
)
from ..ir.cfg import build_cfg_for_function, CFG, BasicBlock, Loop
from ._util import wrap32


def strength_reduction_pass(func: TACFunction) -> TACFunction:
    """Performs Strength Reduction on loop induction variables (replacing multiplications with additions)."""
    optimized_func = copy.deepcopy(func)
    cfg = build_cfg_for_function(optimized_func)

    if not cfg.loops:
        return optimized_func

    max_temp_id = _get_max_temp_id(optimized_func)

    for loop in cfg.loops:
        # Step 1: Find basic induction variables (e.g. i = i + 1 or t = i + 1; i = t)
        bivs, update_insts = _find_basic_induction_vars(loop)
        if not bivs:
            continue

        # Step 2: Find derived induction variables (e.g. t = i * k)
        divs = _find_derived_induction_vars(loop, bivs)
        if not divs:
            continue

        # Step 3: Apply transformation
        header_inst = loop.header.instructions[0] if loop.header.instructions else None
        if header_inst is None:
            continue

        for div_inst, biv_name, step_const, mult_const, is_addition in divs:
            max_temp_id += 1
            sr_temp = Temp(id=max_temp_id, type_str="int")
            optimized_func.local_types[str(sr_temp)] = "int"

            step_val = wrap32(step_const * mult_const)

            # Pre-header seed: sr_temp = biv * mult_const.  The pre-header is
            # spliced in immediately before the loop header, i.e. *after* the
            # induction variable's initialisation and *before* the back-edge
            # target, so ``biv`` here still holds its pre-loop value.  (The old
            # code scanned backward for an ASSIGN to biv and wrongly picked up
            # the in-loop update, seeding sr_temp from an undefined temporary.)
            preheader_init: List[TACInstruction] = [
                TACInstruction(
                    Opcode.MUL,
                    dst=sr_temp,
                    src1=Var(biv_name, "int"),
                    src2=Constant(wrap32(mult_const), "int"),
                    annotation="SR Init",
                )
            ]

            # Step update instruction: sr_temp = sr_temp +/- step_val, kept
            # adjacent to the biv update so the invariant sr_temp == biv*k holds
            # at every use site.
            step_opcode = Opcode.ADD if is_addition else Opcode.SUB
            step_update_inst = TACInstruction(
                step_opcode,
                dst=sr_temp,
                src1=sr_temp,
                src2=Constant(step_val, "int"),
                annotation="SR Step"
            )

            # Rebuild instruction stream (identity comparisons: these objects all
            # live inside optimized_func.instructions).
            new_instructions: List[TACInstruction] = []
            preheader_emitted = False
            biv_update_targets = update_insts.get(biv_name, [])

            for inst in optimized_func.instructions:
                if inst is header_inst and not preheader_emitted:
                    new_instructions.extend(preheader_init)
                    preheader_emitted = True

                if inst is div_inst:
                    # Replace multiplication with copy from sr_temp
                    new_instructions.append(
                        TACInstruction(
                            Opcode.ASSIGN,
                            dst=inst.dst,
                            src1=sr_temp,
                            annotation="SR Reduced"
                        )
                    )
                else:
                    new_instructions.append(inst)
                    # Check if this is the BIV update instruction
                    if any(inst is upd for upd in biv_update_targets):
                        new_instructions.append(step_update_inst)

            optimized_func.instructions = new_instructions

    return optimized_func


def _get_max_temp_id(func: TACFunction) -> int:
    max_id = 0
    for inst in func.instructions:
        for op in (inst.dst, inst.src1, inst.src2, inst.src3):
            if isinstance(op, Temp):
                if op.id > max_id:
                    max_id = op.id
    return max_id


def _find_basic_induction_vars(loop: Loop) -> Tuple[Dict[str, Tuple[int, bool]], Dict[str, List[TACInstruction]]]:
    """Returns (biv_map, update_instructions_map)."""
    bivs: Dict[str, Tuple[int, bool]] = {}
    updates: Dict[str, List[TACInstruction]] = {}

    all_insts: List[TACInstruction] = []
    for b in loop.blocks:
        all_insts.extend(b.instructions)

    temp_to_step: Dict[str, Tuple[str, int, bool]] = {}

    for i, inst in enumerate(all_insts):
        # Direct: i = i + c or i = i - c
        if inst.opcode in (Opcode.ADD, Opcode.SUB):
            if isinstance(inst.dst, Var) and isinstance(inst.src1, Var) and inst.dst.name == inst.src1.name:
                if isinstance(inst.src2, Constant) and isinstance(inst.src2.value, int):
                    bivs[inst.dst.name] = (inst.src2.value, inst.opcode == Opcode.ADD)
                    updates.setdefault(inst.dst.name, []).append(inst)
            elif inst.opcode == Opcode.ADD and isinstance(inst.dst, Var) and isinstance(inst.src2, Var) and inst.dst.name == inst.src2.name:
                if isinstance(inst.src1, Constant) and isinstance(inst.src1.value, int):
                    bivs[inst.dst.name] = (inst.src1.value, True)
                    updates.setdefault(inst.dst.name, []).append(inst)

            # Temp step: t = i + c
            elif isinstance(inst.dst, Temp):
                if isinstance(inst.src1, Var) and isinstance(inst.src2, Constant) and isinstance(inst.src2.value, int):
                    temp_to_step[str(inst.dst)] = (inst.src1.name, inst.src2.value, inst.opcode == Opcode.ADD)
                elif inst.opcode == Opcode.ADD and isinstance(inst.src2, Var) and isinstance(inst.src1, Constant) and isinstance(inst.src1.value, int):
                    temp_to_step[str(inst.dst)] = (inst.src2.name, inst.src1.value, True)

        # Assignment from temp step: i = t
        elif inst.opcode == Opcode.ASSIGN:
            if isinstance(inst.dst, Var) and isinstance(inst.src1, Temp):
                t_name = str(inst.src1)
                if t_name in temp_to_step:
                    v_name, step_c, is_add = temp_to_step[t_name]
                    if v_name == inst.dst.name:
                        bivs[v_name] = (step_c, is_add)
                        updates.setdefault(v_name, []).append(inst)

    return bivs, updates


def _find_derived_induction_vars(
    loop: Loop, bivs: Dict[str, Tuple[int, bool]]
) -> List[Tuple[TACInstruction, str, int, int, bool]]:
    """Finds instructions computing t = biv * k."""
    divs: List[Tuple[TACInstruction, str, int, int, bool]] = []

    for b in loop.blocks:
        for inst in b.instructions:
            if inst.opcode == Opcode.MUL:
                if isinstance(inst.src1, Var) and inst.src1.name in bivs and isinstance(inst.src2, Constant) and isinstance(inst.src2.value, int):
                    biv_name = inst.src1.name
                    step_c, is_add = bivs[biv_name]
                    mult_c = inst.src2.value
                    if mult_c != 0:
                        divs.append((inst, biv_name, step_c, mult_c, is_add))
                elif isinstance(inst.src2, Var) and inst.src2.name in bivs and isinstance(inst.src1, Constant) and isinstance(inst.src1.value, int):
                    biv_name = inst.src2.name
                    step_c, is_add = bivs[biv_name]
                    mult_c = inst.src1.value
                    if mult_c != 0:
                        divs.append((inst, biv_name, step_c, mult_c, is_add))

    return divs
