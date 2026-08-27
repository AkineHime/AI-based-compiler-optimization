import copy
from typing import Dict, List, Set, Optional, Any, Tuple
from ..ir.tac import (
    TACFunction, TACInstruction, Opcode,
    Operand, Temp, Var, Constant, Label
)
from ..ir.cfg import build_cfg_for_function, CFG, BasicBlock


def dce_pass(func: TACFunction) -> TACFunction:
    """Performs Dead Code Elimination (DCE) using backward liveness analysis, unreachable block removal, and unused local pruning."""
    optimized_func = copy.deepcopy(func)
    changed = True
    iteration = 0
    max_iterations = 20

    while changed and iteration < max_iterations:
        changed = False
        iteration += 1

        # Step 1: Remove unreachable blocks
        cfg = build_cfg_for_function(optimized_func)
        reachable_insts, block_removed = _remove_unreachable_blocks(cfg, optimized_func)
        if block_removed:
            optimized_func.instructions = reachable_insts
            changed = True
            cfg = build_cfg_for_function(optimized_func)

        # Step 2: Backward liveness analysis
        live_in, live_out = _compute_liveness(cfg)

        # Step 3: Sweep blocks and eliminate dead instructions
        new_instructions: List[TACInstruction] = []
        for block in cfg.blocks:
            current_live = set(live_out.get(block.id, set()))
            block_kept_insts: List[TACInstruction] = []

            for inst in reversed(block.instructions):
                defs = _get_defs(inst)
                uses = _get_uses(inst)
                has_side_effects = _has_side_effects(inst)

                if not has_side_effects and defs:
                    # If none of the defined variables are live, instruction is dead
                    if defs.isdisjoint(current_live):
                        changed = True
                        continue

                # Instruction is kept
                block_kept_insts.append(inst)
                current_live.difference_update(defs)
                current_live.update(uses)

            block_kept_insts.reverse()
            new_instructions.extend(block_kept_insts)

        if len(new_instructions) != len(optimized_func.instructions):
            changed = True
        optimized_func.instructions = new_instructions

        # Step 4: Remove redundant labels
        cleaned_insts, label_removed = _clean_redundant_labels(optimized_func.instructions)
        if label_removed:
            optimized_func.instructions = cleaned_insts
            changed = True

        # Step 5: Clean up unused ALLOC_LOCAL instructions
        cleaned_allocs, alloc_removed = _clean_unused_allocs(optimized_func.instructions)
        if alloc_removed:
            optimized_func.instructions = cleaned_allocs
            changed = True

    return optimized_func


def _get_operand_key(op: Any) -> Optional[str]:
    if isinstance(op, (Temp, Var)):
        return str(op)
    return None


def _get_defs(inst: TACInstruction) -> Set[str]:
    """Returns set of variable/temp names defined by this instruction."""
    defs: Set[str] = set()
    op = inst.opcode

    if op in (
        Opcode.ASSIGN, Opcode.ADD, Opcode.SUB, Opcode.MUL, Opcode.DIV, Opcode.MOD,
        Opcode.EQ, Opcode.NE, Opcode.LT, Opcode.LE, Opcode.GT, Opcode.GE,
        Opcode.LOGIC_AND, Opcode.LOGIC_OR, Opcode.NEG, Opcode.LOGIC_NOT,
        Opcode.LOAD_ARR_1D, Opcode.LOAD_ARR_2D, Opcode.GET_FIELD, Opcode.CALL
    ):
        k = _get_operand_key(inst.dst)
        if k:
            defs.add(k)

    return defs


def _get_uses(inst: TACInstruction) -> Set[str]:
    """Returns set of variable/temp names read by this instruction."""
    uses: Set[str] = set()
    op = inst.opcode

    # For aggregate writes, base is used/modified
    if op in (Opcode.STORE_ARR_1D, Opcode.STORE_ARR_2D, Opcode.SET_FIELD):
        k = _get_operand_key(inst.dst)
        if k:
            uses.add(k)

    # Inspect sources
    for src in (inst.src1, inst.src2, inst.src3):
        k = _get_operand_key(src)
        if k:
            uses.add(k)

    return uses


def _has_side_effects(inst: TACInstruction) -> bool:
    """Check if instruction cannot be removed even if its dst is dead."""
    op = inst.opcode
    if op in (
        Opcode.CALL, Opcode.RETURN, Opcode.PARAM,
        Opcode.LABEL, Opcode.JUMP, Opcode.JUMP_IF_TRUE, Opcode.JUMP_IF_FALSE,
        Opcode.STORE_ARR_1D, Opcode.STORE_ARR_2D, Opcode.SET_FIELD,
        Opcode.ALLOC_LOCAL, Opcode.COMMENT
    ):
        return True
    return False


def _compute_liveness(cfg: CFG) -> Tuple[Dict[int, Set[str]], Dict[int, Set[str]]]:
    """Iterative dataflow analysis for live variables."""
    use_map: Dict[int, Set[str]] = {}
    def_map: Dict[int, Set[str]] = {}

    for block in cfg.blocks:
        b_use: Set[str] = set()
        b_def: Set[str] = set()
        for inst in block.instructions:
            inst_defs = _get_defs(inst)
            inst_uses = _get_uses(inst)
            for u in inst_uses:
                if u not in b_def:
                    b_use.add(u)
            b_def.update(inst_defs)
        use_map[block.id] = b_use
        def_map[block.id] = b_def

    live_in: Dict[int, Set[str]] = {b.id: set() for b in cfg.blocks}
    live_out: Dict[int, Set[str]] = {b.id: set() for b in cfg.blocks}

    changed = True
    while changed:
        changed = False
        for block in reversed(cfg.blocks):
            # LiveOut[B] = Union_{S in succ(B)} LiveIn[S]
            new_out: Set[str] = set()
            for succ in block.successors:
                new_out.update(live_in[succ.id])

            # LiveIn[B] = Use[B] union (LiveOut[B] - Def[B])
            new_in = use_map[block.id] | (new_out - def_map[block.id])

            if new_out != live_out[block.id] or new_in != live_in[block.id]:
                live_out[block.id] = new_out
                live_in[block.id] = new_in
                changed = True

    return live_in, live_out


def _remove_unreachable_blocks(cfg: CFG, func: TACFunction) -> Tuple[List[TACInstruction], bool]:
    if not cfg.blocks:
        return func.instructions, False

    # Find reachable blocks starting from entry
    reachable_ids: Set[int] = set()
    stack = [cfg.entry.id if cfg.entry else cfg.blocks[0].id]

    while stack:
        b_id = stack.pop()
        if b_id in reachable_ids:
            continue
        reachable_ids.add(b_id)
        blk = cfg.get_block_by_id(b_id)
        if blk:
            for s in blk.successors:
                if s.id not in reachable_ids:
                    stack.append(s.id)

    if len(reachable_ids) == len(cfg.blocks):
        return func.instructions, False

    kept_insts: List[TACInstruction] = []
    for b in cfg.blocks:
        if b.id in reachable_ids:
            kept_insts.extend(b.instructions)

    return kept_insts, True


def _clean_redundant_labels(instructions: List[TACInstruction]) -> Tuple[List[TACInstruction], bool]:
    # Collect all targeted labels
    target_labels: Set[str] = set()
    for inst in instructions:
        if inst.opcode in (Opcode.JUMP, Opcode.JUMP_IF_TRUE, Opcode.JUMP_IF_FALSE):
            target_labels.add(str(inst.dst))

    filtered: List[TACInstruction] = []
    removed = False
    for inst in instructions:
        if inst.opcode == Opcode.LABEL:
            lbl_name = str(inst.dst)
            if lbl_name not in target_labels:
                removed = True
                continue
        filtered.append(inst)

    return filtered, removed


def _clean_unused_allocs(instructions: List[TACInstruction]) -> Tuple[List[TACInstruction], bool]:
    # Find all variables referenced in non-alloc instructions
    referenced_vars: Set[str] = set()
    for inst in instructions:
        if inst.opcode != Opcode.ALLOC_LOCAL:
            for op in (inst.dst, inst.src1, inst.src2, inst.src3):
                if isinstance(op, (Var, Temp)):
                    referenced_vars.add(str(op))

    filtered: List[TACInstruction] = []
    removed = False
    for inst in instructions:
        if inst.opcode == Opcode.ALLOC_LOCAL:
            var_name = str(inst.dst)
            if var_name not in referenced_vars:
                removed = True
                continue
        filtered.append(inst)

    return filtered, removed
