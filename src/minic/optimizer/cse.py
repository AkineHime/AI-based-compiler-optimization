import copy
from typing import Dict, List, Set, Optional, Any, Tuple
from ..ir.tac import (
    TACFunction, TACInstruction, Opcode,
    Operand, Temp, Var, Constant, Label
)
from ..ir.cfg import build_cfg_for_function, CFG, BasicBlock


def cse_pass(func: TACFunction, global_names: frozenset = frozenset()) -> TACFunction:
    """Performs Common Subexpression Elimination (CSE) using Local Value Numbering per Basic Block.

    ``global_names`` lists module-level variables; a ``CALL`` invalidates every
    cached expression that reads one of them, since the callee may have written
    it (locals and temporaries cannot alias in MiniC, so those stay valid).
    """
    optimized_func = copy.deepcopy(func)
    cfg = build_cfg_for_function(optimized_func)

    new_instructions: List[TACInstruction] = []

    for block in cfg.blocks:
        # expr_key -> (result_operand, dependencies_set)
        available_exprs: Dict[str, Tuple[Operand, Set[str]]] = {}

        for inst in block.instructions:
            op = inst.opcode
            expr_key, deps = _get_expression_key(inst)

            if expr_key is not None and expr_key in available_exprs:
                # Common subexpression found!
                prev_dst, _ = available_exprs[expr_key]
                new_inst = TACInstruction(Opcode.ASSIGN, dst=inst.dst, src1=prev_dst, annotation="CSE")
                new_instructions.append(new_inst)

                # Invalidate if destination variable overwrites a dependency
                _invalidate_redefined_var(inst.dst, available_exprs)
                continue

            # If not found or not an eligible expr, keep instruction
            new_instructions.append(inst)

            # If it defines an available expression, record it
            if expr_key is not None and inst.dst is not None:
                available_exprs[expr_key] = (inst.dst, deps)

            # Invalidate any expressions that depend on mutated variables
            _process_mutations(inst, available_exprs, global_names)

    optimized_func.instructions = new_instructions
    return optimized_func


def _get_operand_repr(op: Any) -> str:
    if isinstance(op, Constant):
        return f"Const({op.value!r}:{op.type_str})"
    elif isinstance(op, (Temp, Var)):
        return str(op)
    return str(op)


def _get_expression_key(inst: TACInstruction) -> Tuple[Optional[str], Set[str]]:
    """Returns unique string key for instruction expression and the set of variable dependencies."""
    op = inst.opcode
    deps: Set[str] = set()

    # Binary Arithmetic / Relational / Logical
    if op in (
        Opcode.ADD, Opcode.SUB, Opcode.MUL, Opcode.DIV, Opcode.MOD,
        Opcode.EQ, Opcode.NE, Opcode.LT, Opcode.LE, Opcode.GT, Opcode.GE,
        Opcode.LOGIC_AND, Opcode.LOGIC_OR
    ):
        s1_str = _get_operand_repr(inst.src1)
        s2_str = _get_operand_repr(inst.src2)

        for s in (inst.src1, inst.src2):
            if isinstance(s, (Var, Temp)):
                deps.add(str(s))

        # Commutative operators: normalize operand order
        if op in (Opcode.ADD, Opcode.MUL, Opcode.EQ, Opcode.NE, Opcode.LOGIC_AND, Opcode.LOGIC_OR):
            if s1_str > s2_str:
                s1_str, s2_str = s2_str, s1_str

        return f"{op.name}({s1_str}, {s2_str})", deps

    # Unary
    elif op in (Opcode.NEG, Opcode.LOGIC_NOT):
        s1_str = _get_operand_repr(inst.src1)
        if isinstance(inst.src1, (Var, Temp)):
            deps.add(str(inst.src1))
        return f"{op.name}({s1_str})", deps

    # Array Reads
    elif op == Opcode.LOAD_ARR_1D:
        arr_str = _get_operand_repr(inst.src1)
        idx_str = _get_operand_repr(inst.src2)
        for s in (inst.src1, inst.src2):
            if isinstance(s, (Var, Temp)):
                deps.add(str(s))
        return f"LOAD1D({arr_str}[{idx_str}])", deps

    elif op == Opcode.LOAD_ARR_2D:
        arr_str = _get_operand_repr(inst.src1)
        i_str = _get_operand_repr(inst.src2)
        j_str = _get_operand_repr(inst.src3)
        for s in (inst.src1, inst.src2, inst.src3):
            if isinstance(s, (Var, Temp)):
                deps.add(str(s))
        return f"LOAD2D({arr_str}[{i_str}][{j_str}])", deps

    # Struct Field Reads
    elif op == Opcode.GET_FIELD:
        s_str = _get_operand_repr(inst.src1)
        f_str = str(inst.src2)
        if isinstance(inst.src1, (Var, Temp)):
            deps.add(str(inst.src1))
        return f"GETFIELD({s_str}.{f_str})", deps

    return None, set()


def _invalidate_redefined_var(dst: Optional[Operand], available_exprs: Dict[str, Tuple[Operand, Set[str]]]) -> None:
    if dst is None or not isinstance(dst, (Var, Temp)):
        return
    dst_name = str(dst)
    keys_to_remove = [
        k for k, (_, deps) in available_exprs.items() if dst_name in deps
    ]
    for k in keys_to_remove:
        available_exprs.pop(k, None)


def _process_mutations(inst: TACInstruction, available_exprs: Dict[str, Tuple[Operand, Set[str]]],
                       global_names: frozenset = frozenset()) -> None:
    op = inst.opcode

    if op in (Opcode.STORE_ARR_1D, Opcode.STORE_ARR_2D):
        # Invalidate array loads for this array
        arr_name = str(inst.dst)
        keys_to_remove = [k for k in available_exprs if f"LOAD" in k and arr_name in k]
        for k in keys_to_remove:
            available_exprs.pop(k, None)

    elif op == Opcode.SET_FIELD:
        # Invalidate struct field loads for this struct
        s_name = str(inst.dst)
        keys_to_remove = [k for k in available_exprs if f"GETFIELD({s_name}." in k]
        for k in keys_to_remove:
            available_exprs.pop(k, None)

    elif op == Opcode.CALL:
        # A call may modify arrays/structs (via aggregate returns) and any
        # global, so drop every load/field expression and every arithmetic
        # expression that reads a global.
        keys_to_remove = [
            k for k, (_dst, deps) in available_exprs.items()
            if "LOAD" in k or "GETFIELD" in k or (deps & global_names)
        ]
        for k in keys_to_remove:
            available_exprs.pop(k, None)

    # Invalidate variable defined by dst
    if inst.dst is not None:
        _invalidate_redefined_var(inst.dst, available_exprs)
